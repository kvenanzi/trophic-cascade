"""Matplotlib figures logged to W&B by the Part A scripts, and reused for the write-up."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

CLASS_COLOURS = {
    "previous_token": "#8c6bb1", "duplicate_token": "#6baed6", "induction": "#2171b5",
    "s_inhibition": "#e6550d", "name_mover": "#31a354", "backup_name_mover": "#a1d99b",
    "negative_name_mover": "#de2d26", "": "#bdbdbd",
}


def interaction_heatmap(inter: np.ndarray, L: int, H: int, title: str):
    """Rows: removed head; columns: responding head; colour: change in the responding
    head's direct effect (logit-difference units), symmetric colour scale."""
    fig, ax = plt.subplots(figsize=(8, 7))
    v = np.percentile(np.abs(inter), 99.9) or 1.0
    im = ax.imshow(inter, cmap="RdBu_r", vmin=-v, vmax=v, interpolation="nearest")
    ticks = np.arange(0, L * H, H)
    ax.set_xticks(ticks, [f"L{l}" for l in range(L)])
    ax.set_yticks(ticks, [f"L{l}" for l in range(L)])
    ax.set_xlabel("responding head")
    ax.set_ylabel("removed head")
    ax.set_title(title)
    fig.colorbar(im, ax=ax, label="change in direct effect")
    fig.tight_layout()
    return fig


def release_bars(base_de: np.ndarray, delta: np.ndarray, classes: dict, n: int = 16, title: str = ""):
    """The heads whose direct effect changed most after a removal: before and after."""
    L, H = base_de.shape
    order = np.argsort(-np.abs(delta).ravel())[:n]
    heads = [np.unravel_index(i, (L, H)) for i in order]
    cls = {tuple(h): c for c, hs in classes.items() for h in hs}
    labels = [f"{l}.{h}" for l, h in heads]
    before = [base_de[l, h] for l, h in heads]
    after = [base_de[l, h] + delta[l, h] for l, h in heads]
    x = np.arange(len(heads))
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(x - 0.2, before, 0.4, label="intact", color="#bdbdbd")
    ax.bar(x + 0.2, after, 0.4, label="after removal",
           color=[CLASS_COLOURS[cls.get((l, h), "")] for l, h in heads])
    ax.axhline(0, color="black", lw=0.6)
    ax.set_xticks(x, labels, rotation=45)
    ax.set_ylabel("direct effect on logit difference")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    return fig


def keystone_scatter(df, title: str = ""):
    """Abundance against share of the trait lost on removal; the diagonal is CI = 1."""
    fig, ax = plt.subplots(figsize=(7, 5.5))
    for c, g in df.groupby("class"):
        ax.scatter(g["abundance"].clip(lower=1e-7), g["effect_share"], s=18 if c == "" else 40,
                   color=CLASS_COLOURS.get(c, "#bdbdbd"), label=c or "other", alpha=0.85)
    for _, r in df[df["keystone"] | (df["abundance"] > 0.05)].iterrows():
        ax.annotate(r["head"], (max(r["abundance"], 1e-7), r["effect_share"]), fontsize=7,
                    xytext=(3, 3), textcoords="offset points")
    xs = np.logspace(-7, 0, 50)
    ax.plot(xs, xs, "k--", lw=0.7, label="CI = 1")
    ax.plot(xs, -xs, "k--", lw=0.7)
    ax.set_xscale("log")
    ax.set_xlabel("abundance p (share of summed |direct effect|)")
    ax.set_ylabel("share of logit difference lost on removal")
    ax.axhline(0, color="black", lw=0.5)
    ax.set_title(title)
    ax.legend(fontsize=7, loc="lower right")
    fig.tight_layout()
    return fig


def interval_bars(names, points, los, his, ylabel: str, title: str = ""):
    fig, ax = plt.subplots(figsize=(7, 4))
    x = np.arange(len(names))
    ax.bar(x, points, color="#3182bd")
    ax.errorbar(x, points, yerr=[np.subtract(points, los), np.subtract(his, points)],
                fmt="none", color="black", capsize=4)
    ax.axhline(0, color="black", lw=0.6)
    ax.axhline(1, color="grey", lw=0.6, ls="--")
    ax.set_xticks(x, names, rotation=20)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    fig.tight_layout()
    return fig
