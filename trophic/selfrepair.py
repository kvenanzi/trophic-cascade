"""Self-repair on held-out text (Part B, §4.5; the measure of Rushing & Nanda 2024).

For every head and every position of a set of held-out sequences:

- DE:      the head's direct effect on the logit of the correct next token y,
           z W_O W_U[:, y] / s, with s the final LayerNorm scale of the intact run;
- dlogit:  the change in the logit of y when the head is resample-ablated, its z
           replaced by the z of the next sequence in the batch at the same position;
- dDE:     the change in the head's own direct effect under that ablation, with the
           intact run's scale, so compensation through normalisation counts as
           self-repair;
- self-repair = dlogit - dDE.

Each head's statistics are taken over the 2% of positions where its intact DE is
largest. The pooled self-repair fraction is sum(self-repair) / sum(-dDE) over all
heads and their selected positions: the share of removed direct effect that the rest
of the model restores. The mean over heads of each head's own fraction is secondary.
Logits are those of a HookedTransformer with centred unembedding.
"""

from __future__ import annotations

import numpy as np
import torch


@torch.no_grad()
def measure(model, tokens: torch.Tensor, top_frac: float = 0.02, batch_size: int = 32) -> dict:
    """`tokens`: [N, ctx + 1] held-out windows. Returns pooled and mean fractions, and
    per-head arrays [L, H] of summed self-repair, summed -dDE, and mean selected DE."""
    L, H = model.cfg.n_layers, model.cfg.n_heads
    dev = model.cfg.device
    inp, tgt = tokens[:, :-1].to(dev), tokens[:, 1:].to(dev)
    N, T = inp.shape
    de_all = torch.zeros(L, H, N, T)
    dlogit_all = torch.zeros(L, H, N, T)
    dde_all = torch.zeros(L, H, N, T)
    W_O, W_U = model.W_O, model.W_U

    for b in range(0, N, batch_size):
        x, y = inp[b:b + batch_size], tgt[b:b + batch_size]
        B = len(x)
        if B < 2:
            continue                                                   # resampling needs a partner
        logits, cache = model.run_with_cache(
            x, names_filter=lambda n: n.endswith("attn.hook_z") or n == "ln_final.hook_scale")
        logit_y = logits.gather(-1, y[..., None])[..., 0]              # [B, T]
        scale = cache["ln_final.hook_scale"][..., 0]                   # [B, T]
        u = W_U.T[y]                                                   # [B, T, d_model]
        perm = torch.roll(torch.arange(B, device=dev), -1)
        for l in range(L):
            z = cache[f"blocks.{l}.attn.hook_z"]                       # [B, T, H, dh]
            u_head = torch.einsum("hdm,btm->bthd", W_O[l], u)
            de = (z * u_head).sum(-1) / scale[..., None]               # [B, T, H]
            z_new = z[perm]
            dde = ((z_new - z) * u_head).sum(-1) / scale[..., None]
            de_all[l, :, b:b + B] = de.permute(2, 0, 1).float().cpu()
            dde_all[l, :, b:b + B] = dde.permute(2, 0, 1).float().cpu()
            for h in range(H):
                def hook(zz, hook, h=h, z_new=z_new):
                    zz[:, :, h] = z_new[:, :, h]
                    return zz
                abl = model.run_with_hooks(x, fwd_hooks=[(f"blocks.{l}.attn.hook_z", hook)])
                dlogit_all[l, h, b:b + B] = (abl.gather(-1, y[..., None])[..., 0] - logit_y).float().cpu()

    k = max(1, int(round(top_frac * N * T)))
    sr_sum = np.zeros((L, H))
    rem_sum = np.zeros((L, H))
    de_sel = np.zeros((L, H))
    for l in range(L):
        for h in range(H):
            idx = torch.topk(de_all[l, h].flatten(), k).indices
            dl = dlogit_all[l, h].flatten()[idx]
            dd = dde_all[l, h].flatten()[idx]
            sr_sum[l, h] = float((dl - dd).sum())
            rem_sum[l, h] = float((-dd).sum())
            de_sel[l, h] = float(de_all[l, h].flatten()[idx].mean())
    valid = rem_sum > 0
    per_head = np.where(valid, sr_sum / np.where(valid, rem_sum, 1), np.nan)
    return {
        "pooled": float(sr_sum[valid].sum() / rem_sum[valid].sum()),
        "mean": float(np.nanmean(per_head)),
        "per_layer": [float(sr_sum[l][valid[l]].sum() / rem_sum[l][valid[l]].sum())
                      if valid[l].any() else float("nan") for l in range(L)],
        "per_head": per_head, "sr_sum": sr_sum, "removed_sum": rem_sum, "de_selected": de_sel,
        "n_positions": N * T, "k": k,
    }
