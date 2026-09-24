import numpy as np
import torch

from trophic.ablate import IOIRunner


def test_no_ablation_matches_model_and_hooks_apply(gpt2, prompts):
    ioi, abc = prompts
    r = IOIRunner(gpt2, ioi, abc)
    base = r.run()
    # the runner's logit difference equals a plain forward pass
    i = 0
    logits = gpt2(r.tokens[ioi[i].template][:1])[0, -1]
    expect = (logits[r.io[i]] - logits[r.s[i]]).item()
    assert abs(base["ld"][i] - expect) < 1e-3
    # an ablated head's direct effect is zero, and ablating nothing changes nothing
    ab = r.run([(9, 9)], frozen_scale=base["scale"])
    assert np.abs(ab["de"][:, 9, 9]).max() < 1e-4
    assert np.abs(ab["act"][:, 9, 9]).max() < 1e-3
    again = r.run([])
    assert np.allclose(again["ld"], base["ld"], atol=1e-4)
    # with frozen scale equal to the run's own, de_frozen == de
    same = r.run([], frozen_scale=base["scale"])
    assert np.allclose(same["de_frozen"], same["de"], atol=1e-4)


def test_direct_effects_sum_to_logit_difference(gpt2, prompts):
    """With TransformerLens's centred weights, the final residual is the sum of the
    embeddings, every head's z W_O, the attention biases, and the MLP outputs; divided
    by the final LayerNorm scale and projected on W_U[IO] - W_U[S] it gives the logit
    difference exactly (plus the unembedding bias difference)."""
    ioi, _ = prompts
    m = gpt2
    toks = m.to_tokens(ioi[0].text)
    io = m.tokenizer.encode(ioi[0].io)[0]
    s = m.tokenizer.encode(ioi[0].s)[0]
    logits, cache = m.run_with_cache(toks)
    ld = (logits[0, -1, io] - logits[0, -1, s]).item()
    u = m.W_U[:, io] - m.W_U[:, s]
    resid = cache["hook_embed"][0, -1] + cache["hook_pos_embed"][0, -1]
    for l in range(m.cfg.n_layers):
        z = cache[f"blocks.{l}.attn.hook_z"][0, -1]                 # [H, dh]
        resid = resid + torch.einsum("hd,hdm->m", z, m.W_O[l]) + m.b_O[l]
        resid = resid + cache[f"blocks.{l}.hook_mlp_out"][0, -1]
    total = (resid / cache["ln_final.hook_scale"][0, -1, 0]) @ u + (m.b_U[io] - m.b_U[s])
    assert abs(total.item() - ld) < 1e-2
