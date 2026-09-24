"""Loading pretrained models for the removal experiments."""

import warnings

import torch

warnings.filterwarnings("ignore", message=".*HookedTransformer.*deprecated.*")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="transformer_lens")


def load(name: str, checkpoint: int | None = None, device: str | None = None,
         dtype: torch.dtype = torch.float32, load_dtype: torch.dtype | None = None):
    """A TransformerLens HookedTransformer with default weight processing (fold_ln,
    centre writing weights, centre unembed). `checkpoint` is a Pythia training step.
    `load_dtype` (e.g. float16) halves host memory during loading, which Pythia-1.4B
    needs on a 15 GB machine; the weights are then cast to `dtype` on the device."""
    from transformer_lens import HookedTransformer
    torch.set_grad_enabled(False)
    device = device or ("cuda" if torch.cuda.is_available() else "cpu")
    kw = {}
    if checkpoint is not None:
        # TransformerLens 3.9 passes token=os.environ.get("HF_TOKEN", "") for Pythia
        # checkpoints, and an empty token becomes the illegal header "Bearer ". Download the
        # checkpoint with transformers (which omits a missing token) and hand it over; the
        # architecture config is the same at every checkpoint.
        from transformers import AutoModelForCausalLM
        kw["hf_model"] = AutoModelForCausalLM.from_pretrained(
            f"EleutherAI/{name}" if "/" not in name else name, revision=f"step{checkpoint}",
            dtype=load_dtype or dtype)
    model = HookedTransformer.from_pretrained(name, device=device, dtype=load_dtype or dtype, **kw)
    if load_dtype is not None and load_dtype != dtype:
        model = model.to(dtype)
    return model
