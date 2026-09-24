"""Part B models: a small GPT-2 trained from scratch under one of three regimes, and
its conversion to TransformerLens for measurement.

Regimes (§4.4 of the write-up):
  none      no dropout of any kind
  standard  dropout 0.1 on embeddings, attention weights, and residual branches
  drophead  each head's output zeroed per sequence with probability 0.1 and the
            surviving heads scaled by 1/0.9 (Zhou et al 2020), no other dropout

HookedTransformer has no dropout, so training uses Hugging Face's GPT2LMHeadModel and
measurement converts the trained weights (TransformerLens's own GPT-2 conversion,
followed by its default weight processing) into a HookedTransformer.
"""

from __future__ import annotations

import torch

ARMS = ("none", "standard", "drophead")


def gpt2_config(arm: str, n_layer: int = 6, n_head: int = 8, d_model: int = 384,
                d_mlp: int = 1536, ctx: int = 256, p: float = 0.1):
    from transformers import GPT2Config
    if arm not in ARMS:
        raise ValueError(arm)
    drop = p if arm == "standard" else 0.0
    return GPT2Config(vocab_size=50257, n_positions=ctx, n_embd=d_model, n_layer=n_layer,
                      n_head=n_head, n_inner=d_mlp, resid_pdrop=drop, embd_pdrop=drop,
                      attn_pdrop=drop, tie_word_embeddings=True)


def add_drophead(model, p: float) -> list:
    """Register head dropout on every attention layer: a pre-hook on the output
    projection, whose input is the concatenation of the heads' outputs. Active only in
    training mode. Returns the hook handles."""
    n_head = model.config.n_head

    def hook(module, args):
        if not module.training or p == 0:
            return None
        x = args[0]                                              # [B, T, n_head * d_head]
        B, T, D = x.shape
        keep = (torch.rand(B, 1, n_head, 1, device=x.device) >= p).to(x.dtype) / (1 - p)
        return (x.view(B, T, n_head, D // n_head).mul(keep).view(B, T, D),)

    return [blk.attn.c_proj.register_forward_pre_hook(hook) for blk in model.transformer.h]


def build(arm: str, seed: int, p: float = 0.1, **size):
    """A freshly initialised model for one arm; the seed fixes the initialisation."""
    from transformers import GPT2LMHeadModel
    torch.manual_seed(seed)
    cfg = gpt2_config(arm, p=p, **size)
    model = GPT2LMHeadModel(cfg)
    if arm == "drophead":
        add_drophead(model, p)
    return model


def to_hooked(hf_model, device=None):
    """The trained weights as a HookedTransformer with default processing (fold_ln,
    centred writing weights, centred unembed), in evaluation mode."""
    from transformer_lens import HookedTransformer, HookedTransformerConfig
    from transformer_lens.pretrained.weight_conversions.gpt2 import convert_gpt2_weights

    c = hf_model.config
    device = device or next(hf_model.parameters()).device
    cfg = HookedTransformerConfig(
        n_layers=c.n_layer, d_model=c.n_embd, n_ctx=c.n_positions, d_head=c.n_embd // c.n_head,
        n_heads=c.n_head, d_mlp=c.n_inner, d_vocab=c.vocab_size, act_fn="gelu_new",
        normalization_type="LN", eps=c.layer_norm_epsilon, original_architecture="GPT2LMHeadModel",
        device=str(device), dtype=torch.float32, default_prepend_bos=False)
    hooked = HookedTransformer(cfg)
    sd = {k: v.detach().float().clone() for k, v in convert_gpt2_weights(hf_model, cfg).items()}
    hooked.load_and_process_state_dict(sd, fold_ln=True, center_writing_weights=True,
                                       center_unembed=True, fold_value_biases=True)
    return hooked.to(device).eval()
