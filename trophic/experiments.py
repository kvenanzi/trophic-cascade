"""Part A experiments: set removals, single-head removals, keystones, attenuation.

Every function takes an IOIRunner and the intact run `base` (runner.run() with no
ablation), and returns plain dicts of numbers so the scripts can log and save them.
"""

from __future__ import annotations

import numpy as np

from .ablate import IOIRunner
from .effects import (abundance, bootstrap, community_importance, compensation,
                      heads_str)


def ratio_of_means(a, b):
    return a.mean() / b.mean()


def competence(base: dict) -> dict:
    return {"ld_mean": float(base["ld"].mean()), "acc": float((base["ld"] > 0).mean())}


def passes_gate(base: dict, min_acc: float = 0.8, min_ld: float = 1.0) -> bool:
    c = competence(base)
    return c["acc"] >= min_acc and c["ld_mean"] >= min_ld


def top_heads(base: dict, k: int = 3) -> list[tuple[int, int]]:
    """The k heads with the largest positive mean direct effect."""
    de = base["de"].mean(0)
    flat = np.argsort(-de.ravel())[:k]
    return [tuple(int(x) for x in np.unravel_index(i, de.shape)) for i in flat]


def unembed_bias_diff(runner: IOIRunner) -> np.ndarray:
    b = runner.model.b_U
    return (b[runner.io] - b[runner.s]).float().cpu().numpy()


def set_removal(runner: IOIRunner, base: dict, heads, groups: dict | None = None,
                mode: str = "mean", n_boot: int = 2000) -> dict:
    """Remove `heads` together. Compensation with a bootstrap interval, and the
    offset (the part of the removed heads' direct effect that did not reach the logit
    difference) split into components: each named group of heads, the other heads,
    the MLP layers, the remaining constant terms, and, separately, the share that runs
    through the final LayerNorm scale."""
    heads = [tuple(h) for h in heads]
    ab = runner.run(heads, mode=mode, frozen_scale=base["scale"])
    ld0, ld1 = base["ld"], ab["ld"]
    de_removed = sum(base["de"][:, l, h] for l, h in heads)
    comp = bootstrap(lambda a, b, c: compensation(a, b, c), [ld0, ld1, de_removed], n_boot)

    offset = ld1 - ld0 + de_removed                      # per prompt
    ddelta = ab["de"] - base["de"]                        # own-scale change, [n, L, H]
    for l, h in heads:
        ddelta[:, l, h] = 0.0                             # removed heads are the removal itself
    parts = {}
    assigned = np.zeros(base["de"].shape[1:], bool)
    for name, hs in (groups or {}).items():
        hs = [h for h in hs if tuple(h) not in heads]
        parts[name] = sum((ddelta[:, l, h] for l, h in hs), np.zeros_like(offset))
        for l, h in hs:
            assigned[l, h] = True
    for l, h in heads:
        assigned[l, h] = True
    parts["other heads"] = (ddelta * ~assigned).sum((1, 2))
    parts["MLP layers"] = (ab["mlp_de"] - base["mlp_de"]).sum(1)
    parts["constant terms"] = offset - sum(parts.values())
    bu = unembed_bias_diff(runner)
    ln_part = (ld1 - bu) * (1 - ab["scale"] / base["scale"])

    shares = {k: bootstrap(ratio_of_means, [v, offset], n_boot) for k, v in parts.items()}
    grouped = sum(parts[k] for k in (groups or {}))
    return {
        "heads": heads_str(heads), "mode": mode,
        "ld_intact": float(ld0.mean()), "ld_removed": float(ld1.mean()),
        "de_removed": float(de_removed.mean()),
        "te": float((ld0 - ld1).mean()),
        "compensation": comp,
        "offset": float(offset.mean()),
        "offset_parts": {k: float(v.mean()) for k, v in parts.items()},
        "offset_shares": shares,
        "offset_share_groups": bootstrap(ratio_of_means, [grouped, offset], n_boot) if groups else None,
        "ln_share": bootstrap(ratio_of_means, [ln_part, offset], n_boot),
        "scale_ratio": float((ab["scale"] / base["scale"]).mean()),
        "delta_de": ddelta.mean(0),                       # [L, H], own scale
        "delta_de_frozen": (ab["de_frozen"] - base["de"]).mean(0),
        "run": ab,
    }


def single_removals(runner: IOIRunner, base: dict, mode: str = "mean") -> dict:
    """Every head removed alone. Per-prompt logit differences, and mean direct effect,
    frozen-scale direct effect, and activity of every head in every removal."""
    L, H = runner.L, runner.H
    n = runner.n
    ld = np.zeros((L, H, n), np.float32)
    de = np.zeros((L, H, L, H), np.float32)
    de_frozen = np.zeros((L, H, L, H), np.float32)
    act = np.zeros((L, H, L, H, 3), np.float32)
    mlp = np.zeros((L, H, L), np.float32)
    for l in range(L):
        for h in range(H):
            ab = runner.run([(l, h)], mode=mode, frozen_scale=base["scale"])
            ld[l, h] = ab["ld"]
            de[l, h] = ab["de"].mean(0)
            de_frozen[l, h] = ab["de_frozen"].mean(0)
            act[l, h] = ab["act"].mean(0)
            mlp[l, h] = ab["mlp_de"].mean(0)
    return {"ld": ld, "de": de, "de_frozen": de_frozen, "act": act, "mlp_de": mlp}


def keystone_table(base: dict, singles: dict, classes: dict | None = None,
                   min_effect: float = 0.05, min_ci: float = 2.0) -> list[dict]:
    """One row per head: abundance, direct effect, total effect of its removal,
    community importance, compensation, and whether it meets the registered keystone
    criteria (|t_N - t_D| / t_N >= min_effect and |CI| >= min_ci)."""
    p = abundance(base["de"])
    de = base["de"].mean(0)
    t_n = float(base["ld"].mean())
    cls = {tuple(h): c for c, hs in (classes or {}).items() for h in hs}
    rows = []
    L, H = de.shape
    for l in range(L):
        for h in range(H):
            t_d = float(singles["ld"][l, h].mean())
            effect = (t_n - t_d) / t_n
            ci = community_importance(base["ld"], singles["ld"][l, h], p[l, h])
            rows.append({
                "head": f"{l}.{h}", "layer": l, "index": h, "class": cls.get((l, h), ""),
                "abundance": float(p[l, h]), "direct_effect": float(de[l, h]),
                "total_effect": t_n - t_d, "effect_share": effect,
                "community_importance": ci,
                "compensation": float(1 - (t_n - t_d) / de[l, h]) if abs(de[l, h]) > 1e-6 else None,
                "keystone": bool(abs(effect) >= min_effect and abs(ci) >= min_ci),
            })
    return rows


def attenuation(runner: IOIRunner, base: dict, levels, n_boot: int = 2000) -> list[dict]:
    """For each level k removed as a set, the mean absolute log response ratio of the
    activity of the heads of levels k+1 and k+2, and the bootstrap interval of their
    difference (H3)."""
    def mean_abs_lrr(act_ab, act_0, heads, pos):
        vals = [np.log(act_ab[:, l, h, pos].mean() / act_0[:, l, h, pos].mean()) for l, h in heads]
        return float(np.mean(np.abs(vals)))

    out = []
    for k in range(len(levels) - 2):
        name, heads, _ = levels[k]
        ab = runner.run([tuple(h) for h in heads])
        (n1, h1, p1), (n2, h2, p2) = levels[k + 1], levels[k + 2]
        a0, a1 = base["act"], ab["act"]

        def diff(x0, x1):
            return mean_abs_lrr(x1, x0, h1, p1) - mean_abs_lrr(x1, x0, h2, p2)

        out.append({
            "removed": name, "next": n1, "after_next": n2,
            "lrr_next": mean_abs_lrr(a1, a0, h1, p1),
            "lrr_after_next": mean_abs_lrr(a1, a0, h2, p2),
            "difference": bootstrap(diff, [a0, a1], n_boot),
            "per_head_next": {f"{l}.{h}": float(np.log(a1[:, l, h, p1].mean() / a0[:, l, h, p1].mean()))
                              for l, h in h1},
            "per_head_after_next": {f"{l}.{h}": float(np.log(a1[:, l, h, p2].mean() / a0[:, l, h, p2].mean()))
                                    for l, h in h2},
            "ld_removed": float(ab["ld"].mean()),
        })
    return out


def model_study(model, ioi, abc, k: int = 3, n_boot: int = 2000, batch_size: int = 32) -> dict:
    """H4/H5 on one model: competence, the top-k heads, and their removal as a set.
    Returns the summary and the per-prompt arrays needed to bootstrap across models or
    checkpoints."""
    runner = IOIRunner(model, ioi, abc, batch_size=batch_size)
    base = runner.run()
    out = {"n_layers": runner.L, "n_heads": runner.H, **competence(base),
           "passes_gate": passes_gate(base)}
    top = top_heads(base, k)
    rem = set_removal(runner, base, top, n_boot=n_boot)
    de = base["de"].mean(0)
    d = rem["delta_de"]
    responders = np.argsort(-np.abs(d).ravel())[:8]
    out.update({
        "top_heads": heads_str(top),
        "top_heads_de": [float(de[l, h]) for l, h in top],
        "top_heads_relative_depth": [l / (runner.L - 1) for l, _ in top],
        "de_removed": rem["de_removed"], "te": rem["te"], "ld_removed": rem["ld_removed"],
        "compensation": rem["compensation"], "ln_share": rem["ln_share"],
        "offset_shares": rem["offset_shares"], "scale_ratio": rem["scale_ratio"],
        "largest_responders": [{"head": f"{l}.{h}", "delta_de": float(d[l, h]), "de": float(de[l, h])}
                               for l, h in zip(*np.unravel_index(responders, d.shape))],
    })
    arrays = {"ld0": base["ld"], "ld1": rem["run"]["ld"],
              "de_removed": sum(base["de"][:, l, h] for l, h in top)}
    return {"summary": out, "arrays": arrays}
