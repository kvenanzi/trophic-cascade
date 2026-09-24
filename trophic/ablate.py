"""Removal experiments on attention heads, and what every other head does in response.

A head is removed by mean ablation: its output z (before W_O) at every position is
replaced by the mean of z over the ABC prompts of the same template, position by
position (Wang et al 2022). Resample ablation, which substitutes the z of the paired
ABC prompt instead of the mean, is available as a robustness check.

For each run the runner records, per prompt:

- ld:        logit(IO) - logit(S) at the last position.
- de:        each head's direct effect (DE) on ld: the head's output at the last
             position, relative to its ABC mean, divided by the final LayerNorm scale of
             this run and projected on W_U[IO] - W_U[S]. An ablated head's DE is 0.
- de_frozen: the same with the final LayerNorm scale of the unablated run, so that a
             change in DE can be split into a change in the head's output and a change
             in normalisation (Rushing & Nanda 2024).
- act:       each head's activity: the norm of its output relative to its ABC mean,
             (z - z_mean) W_O, at the three positions where the IOI circuit's head
             classes act: S1+1, S2, and END.
- mlp_de:    each MLP layer's direct effect on ld (not mean-relative).

The model must be loaded with TransformerLens defaults (fold_ln, center_writing_weights,
center_unembed), which make the residual stream a sum of centred per-component terms.
"""

from __future__ import annotations

from collections import defaultdict

import numpy as np
import torch

from .ioi import Prompt

POSITIONS = ("S1+1", "S2", "END")


class IOIRunner:
    def __init__(self, model, ioi: list[Prompt], abc: list[Prompt], batch_size: int = 64,
                 keep_abc: bool = False):
        self.model = model
        self.bs = batch_size
        self.n = len(ioi)
        self.L, self.H = model.cfg.n_layers, model.cfg.n_heads
        dev = model.cfg.device
        tok = model.tokenizer

        def tid(word: str) -> int:
            ids = tok.encode(word, add_special_tokens=False)
            assert len(ids) == 1, (word, ids)
            return ids[0]

        self.groups = defaultdict(list)          # template -> prompt indices
        for i, p in enumerate(ioi):
            self.groups[p.template].append(i)

        self.tokens, self.abc_tokens = {}, {}
        self.io = torch.tensor([tid(p.io) for p in ioi], device=dev)
        self.s = torch.tensor([tid(p.s) for p in ioi], device=dev)
        self.pos = torch.zeros(self.n, 3, dtype=torch.long, device=dev)   # S1+1, S2, END
        for t, idx in self.groups.items():
            toks = model.to_tokens([ioi[i].text for i in idx])
            abc_toks = model.to_tokens([abc[i].text for i in idx])
            pad = model.tokenizer.pad_token_id
            assert toks.shape == abc_toks.shape, f"template {t}: IOI and ABC lengths differ"
            if pad is not None and pad != model.tokenizer.bos_token_id:
                assert not (toks == pad).any(), f"template {t}: prompts differ in token length"
            self.tokens[t], self.abc_tokens[t] = toks, abc_toks
            for row, i in enumerate(idx):
                s_pos = (toks[row] == self.s[i]).nonzero().flatten()
                assert len(s_pos) == 2, (ioi[i].text, s_pos)
                assert (toks[row] == self.io[i]).sum() == 1, ioi[i].text
                self.pos[i] = torch.tensor([s_pos[0] + 1, s_pos[1], toks.shape[1] - 1])

        # ABC reference activations: per-template, per-position mean of z in every layer.
        self.means, self.abc_z = {}, {}
        for t, idx in self.groups.items():
            zs = self._abc_z(self.abc_tokens[t])                  # [n_t, L, pos, H, dh]
            self.means[t] = zs.mean(0)                             # [L, pos, H, dh]
            if keep_abc:
                self.abc_z[t] = zs

    @torch.no_grad()
    def _abc_z(self, toks):
        out = []
        for b in range(0, len(toks), self.bs):
            _, cache = self.model.run_with_cache(toks[b:b + self.bs],
                                                 names_filter=lambda n: n.endswith("attn.hook_z"))
            out.append(torch.stack([cache[f"blocks.{l}.attn.hook_z"] for l in range(self.L)], 1))
        return torch.cat(out)

    def _hooks(self, ablate, mode, t, rows):
        by_layer = defaultdict(list)
        for l, h in ablate:
            by_layer[l].append(h)

        def make(l, heads):
            def hook(z, hook):
                if mode == "mean":
                    z[:, :, heads] = self.means[t][l][:, heads]
                elif mode == "resample":
                    z[:, :, heads] = self.abc_z[t][rows, l][:, :, heads]
                else:
                    raise ValueError(mode)
                return z
            return hook

        return [(f"blocks.{l}.attn.hook_z", make(l, hs)) for l, hs in by_layer.items()]

    @torch.no_grad()
    def run(self, ablate=(), mode: str = "mean", frozen_scale: np.ndarray | None = None) -> dict:
        """One removal experiment. `ablate` is an iterable of (layer, head). Pass the
        `scale` of an unablated run as `frozen_scale` to get `de_frozen`."""
        m = self.model
        W_O = m.W_O                       # [L, H, dh, d_model]
        W_U = m.W_U                       # [d_model, vocab]
        L, H = self.L, self.H
        ld = torch.zeros(self.n)
        de = torch.zeros(self.n, L, H)
        de_frozen = torch.zeros(self.n, L, H)
        act = torch.zeros(self.n, L, H, 3)
        mlp_de = torch.zeros(self.n, L)
        scale = torch.zeros(self.n)
        fs = torch.as_tensor(frozen_scale) if frozen_scale is not None else None
        names = lambda n: n.endswith("attn.hook_z") or n.endswith("hook_mlp_out") \
            or n == "ln_final.hook_scale"

        for t, idx in self.groups.items():
            idx_t = torch.tensor(idx)
            for b in range(0, len(idx), self.bs):
                rows = torch.arange(b, min(b + self.bs, len(idx)))
                gi = idx_t[rows]                                   # global prompt indices
                toks = self.tokens[t][rows]
                with m.hooks(fwd_hooks=self._hooks(ablate, mode, t, rows)):
                    logits, cache = m.run_with_cache(toks, names_filter=names)
                io, s, pos = self.io[gi], self.s[gi], self.pos[gi]
                end = pos[:, 2]
                ar = torch.arange(len(gi))
                last = logits[ar, end]
                ld[gi] = (last[ar, io] - last[ar, s]).float().cpu()
                sc = cache["ln_final.hook_scale"][ar, end, 0]      # [b]
                scale[gi] = sc.float().cpu()
                u = (W_U[:, io] - W_U[:, s]).T                     # [b, d_model]
                for l in range(L):
                    z = cache[f"blocks.{l}.attn.hook_z"]           # [b, pos, H, dh]
                    dz = z - self.means[t][l][None]                # relative to ABC mean
                    # direct effect at END
                    u_head = torch.einsum("hdm,bm->bhd", W_O[l], u)
                    raw = torch.einsum("bhd,bhd->bh", dz[ar, end], u_head)
                    de[gi, l] = (raw / sc[:, None]).float().cpu()
                    if fs is not None:
                        de_frozen[gi, l] = (raw.float().cpu() / fs[gi][:, None])
                    # activity at S1+1, S2, END
                    dzp = torch.stack([dz[ar, pos[:, k]] for k in range(3)], 1)   # [b, 3, H, dh]
                    out = torch.einsum("bkhd,hdm->bkhm", dzp, W_O[l])
                    act[gi, l] = out.norm(dim=-1).permute(0, 2, 1).float().cpu()
                    mo = cache[f"blocks.{l}.hook_mlp_out"][ar, end]
                    mlp_de[gi, l] = ((mo * u).sum(-1) / sc).float().cpu()

        out = {"ld": ld, "de": de, "act": act, "mlp_de": mlp_de, "scale": scale}
        if fs is not None:
            out["de_frozen"] = de_frozen
        return {k: v.numpy() for k, v in out.items()}
