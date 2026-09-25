"""Figures for docs/post/ from the Colab reference artifacts, and figures/data.json with
every plotted number.

    uv run scripts/08_figures.py [--src outputs/colab] [--only partA|partB]

Part A reads the W&B artifacts downloaded to outputs/colab/ (gpt2-removals, models-*,
checkpoints-pythia-410m); Part B reads outputs/partb/summary.json from
07_partb_summarize.py. Colours follow the dataviz reference palette: three categorical
slots at most on a scatter, one hue per single-series chart, blue-grey-red diverging.
"""

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

from trophic.effects import CLASSES

FIG = Path("docs/post/figures")
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
BLUE, ORANGE, AQUA, GREY, RED = "#2a78d6", "#eb6834", "#1baf7a", "#b4b2ab", "#e34948"
DIVERGING = LinearSegmentedColormap.from_list("bgr", ["#1c5cab", BLUE, "#f0efec", RED, "#a8302f"])

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2,
    "text.color": INK, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
    "font.size": 10, "axes.titlesize": 11, "axes.titleweight": "bold", "legend.frameon": False,
    "lines.linewidth": 2,
})

GROUP = {}
for c in ("s_inhibition",):
    GROUP.update({tuple(h): "S-inhibition" for h in CLASSES[c]})
for c in ("previous_token", "duplicate_token", "induction"):
    GROUP.update({tuple(h): "previous-token, duplicate, induction" for h in CLASSES[c]})
for c in ("name_mover", "backup_name_mover", "negative_name_mover"):
    GROUP.update({tuple(h): "name movers (main, backup, negative)" for h in CLASSES[c]})
GROUP_COLOUR = {"S-inhibition": BLUE, "previous-token, duplicate, induction": ORANGE,
                "name movers (main, backup, negative)": AQUA, "other": GREY}
SHORT = {"name_mover": "NM", "backup_name_mover": "backup", "negative_name_mover": "neg. NM",
         "s_inhibition": "S-inh.", "induction": "ind.", "duplicate_token": "dup.",
         "previous_token": "prev."}
CLASS_OF = {tuple(h): c for c, hs in CLASSES.items() for h in hs}


def save(fig, name):
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG / name, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print("wrote", FIG / name)


def part_a(src: Path, data: dict):
    s = json.loads((src / "gpt2-removals/summary.json").read_text())
    r = np.load(src / "gpt2-removals/removals.npz")
    df = pd.read_csv(src / "gpt2-removals/keystones.csv", dtype={"head": str}).fillna({"class": ""})
    base_de = r["base_de"].mean(0)
    L, H = base_de.shape

    # Figure 1: name movers removed, the heads whose direct effect changed most
    d = r["nm_delta_de"]
    order = [np.unravel_index(i, (L, H)) for i in np.argsort(-np.abs(d).ravel())[:10]]
    labels = [f"{l}.{h}\n{SHORT.get(CLASS_OF.get((l, h), ''), '')}" for l, h in order]
    before = [float(base_de[l, h]) for l, h in order]
    after = [float(base_de[l, h] + d[l, h]) for l, h in order]
    x = np.arange(len(order))
    fig, ax = plt.subplots(figsize=(8.5, 3.8))
    ax.bar(x - 0.21, before, 0.4, color=GREY, label="intact")
    ax.bar(x + 0.21, after, 0.4, color=BLUE, label="name movers 9.9, 9.6, 10.0 removed")
    ax.axhline(0, color=INK2, lw=0.8)
    ax.set_xticks(x, labels, fontsize=8.5)
    ax.set_ylabel("direct effect on logit difference")
    ax.grid(axis="x", visible=False)
    ax.legend(loc="lower right", fontsize=8.5)
    save(fig, "name_mover_removal.png")
    data["name_mover_removal"] = [{"head": f"{l}.{h}", "class": CLASS_OF.get((l, h), ""),
                                   "intact": b, "removed": a} for (l, h), b, a in zip(order, before, after)]

    # Figure 2: keystones (Power et al 1996)
    fig, ax = plt.subplots(figsize=(7.5, 5.2))
    df["group"] = [GROUP.get((int(a), int(b)), "other") for a, b in zip(df.layer, df["index"])]
    for g in ["other", "previous-token, duplicate, induction", "S-inhibition",
              "name movers (main, backup, negative)"]:
        sub = df[df.group == g]
        ax.scatter(sub.abundance.clip(lower=1e-7), sub.effect_share, s=16 if g == "other" else 42,
                   color=GROUP_COLOUR[g], label=g, edgecolor=SURFACE, linewidth=1.2, zorder=3)
    nudge = {"7.9": (-20, -10), "8.10": (5, 3)}
    for _, row in df[df.keystone | (df.abundance > 0.05)].iterrows():
        ax.annotate(row["head"], (max(row.abundance, 1e-7), row.effect_share), fontsize=7.5,
                    color=INK2, xytext=nudge.get(row["head"], (4, 3)), textcoords="offset points")
    xs = np.logspace(-7, 0, 100)
    ax.plot(xs, xs, color=INK2, lw=0.8, ls="--")
    ax.plot(xs, -xs, color=INK2, lw=0.8, ls="--")
    ax.text(0.09, 0.33, "CI = 1", color=INK2, fontsize=8, ha="right")
    ax.text(0.09, -0.36, "CI = −1", color=INK2, fontsize=8, ha="right")
    ax.set_xscale("log")
    ax.set_ylim(-0.55, 0.45)
    ax.axhline(0, color=INK2, lw=0.6)
    ax.set_xlabel("abundance p: share of summed |direct effect| (log scale)")
    ax.set_ylabel("share of logit difference lost on removal")
    ax.legend(loc="lower left", fontsize=8)
    save(fig, "keystones.png")
    data["keystones"] = df[["head", "class", "abundance", "direct_effect", "total_effect", "effect_share",
                            "community_importance", "keystone"]].to_dict("records")

    # Figure 3: interaction-strength matrix. Rows: every removed head; columns: the heads
    # of layers 9-11, the only layers with a response above 0.05.
    inter = r["interaction"][:, 9 * H:]
    v = float(np.percentile(np.abs(inter), 99.8))
    fig, ax = plt.subplots(figsize=(6.2, 8.2))
    im = ax.imshow(inter, cmap=DIVERGING, vmin=-v, vmax=v, interpolation="nearest", aspect="auto")
    ax.set_xticks(np.arange(0, 3 * H, H) + H / 2 - 0.5, [f"L{l}" for l in range(9, L)])
    ax.set_yticks(np.arange(0, L * H, H) + H / 2 - 0.5, [f"L{l}" for l in range(L)])
    for t in np.arange(H, 3 * H, H):
        ax.axvline(t - 0.5, color=SURFACE, lw=1.2)
    for t in np.arange(H, L * H, H):
        ax.axhline(t - 0.5, color=SURFACE, lw=1.2)
    ax.grid(False)
    ax.set_xlabel("responding head (layers 9-11)")
    ax.set_ylabel("removed head (all layers)")
    cb = fig.colorbar(im, ax=ax, fraction=0.05, pad=0.03)
    cb.set_label("change in direct effect (logit difference)")
    cb.outline.set_visible(False)
    save(fig, "interaction_matrix.png")
    big = np.argsort(-np.abs(r["interaction"]).ravel())[:15]
    rows_, cols_ = np.unravel_index(big, r["interaction"].shape)
    data["interaction_largest"] = [
        {"removed": f"{i // H}.{i % H}", "responding": f"{j // H}.{j % H}",
         "delta_de": float(r["interaction"][i, j])} for i, j in zip(rows_, cols_)]

    # Figure 4: attenuation (H3)
    h3 = s["H3"]
    names = ["previous-token\nremoved", "duplicate + induction\nremoved", "S-inhibition\nremoved"]
    nxt = [x["lrr_next"] for x in h3]
    aft = [x["lrr_after_next"] for x in h3]
    x = np.arange(3)
    fig, ax = plt.subplots(figsize=(7, 3.6))
    b1 = ax.bar(x - 0.21, nxt, 0.4, color=BLUE, label="next level")
    b2 = ax.bar(x + 0.21, aft, 0.4, color=ORANGE, label="level after next")
    for bars in (b1, b2):
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01, f"{bar.get_height():.2f}",
                    ha="center", fontsize=8, color=INK2)
    ax.set_xticks(x, names, fontsize=8.5)
    ax.set_ylabel("mean |log response ratio| of activity")
    ax.grid(axis="x", visible=False)
    ax.legend(fontsize=8.5)
    save(fig, "attenuation.png")
    data["attenuation"] = [{"removed": x["removed"], "next": x["next"], "after_next": x["after_next"],
                            "lrr_next": x["lrr_next"], "lrr_after_next": x["lrr_after_next"],
                            "difference": x["difference"]} for x in h3]

    # Figure 5: compensation by model (H4)
    models = ["gpt2", "gpt2-medium", "pythia-160m", "pythia-410m", "pythia-1.4b"]
    pretty = ["GPT-2 small", "GPT-2 medium", "Pythia-160M", "Pythia-410M", "Pythia-1.4B"]
    rows = [json.loads((src / f"models-{m}/{m}.json").read_text()) for m in models]
    c = np.array([r_["compensation"] for r_ in rows])
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.errorbar(np.arange(5), c[:, 0], yerr=[c[:, 0] - c[:, 1], c[:, 2] - c[:, 0]], fmt="o",
                color=BLUE, ms=8, capsize=4, lw=1.6, mec=SURFACE, mew=1.5)
    for i, v_ in enumerate(c[:, 0]):
        ax.text(i + 0.12, v_, f"{v_:.2f}", va="center", fontsize=8.5, color=INK2)
    ax.axhline(0, color=INK2, lw=0.8)
    ax.axhline(1, color=INK2, lw=0.8, ls="--")
    ax.set_xticks(np.arange(5), pretty)
    ax.set_xlim(-0.4, 4.5)
    ax.set_ylabel("compensation 1 − TE/DE")
    ax.grid(axis="x", visible=False)
    save(fig, "compensation_by_model.png")
    data["compensation_by_model"] = [{"model": p, "top_heads": r_["top_heads"], "ld_mean": r_["ld_mean"],
                                      "acc": r_["acc"], "de_removed": r_["de_removed"], "te": r_["te"],
                                      "compensation": r_["compensation"], "ln_share": r_["ln_share"]}
                                     for p, r_ in zip(pretty, rows)]

    # Figure 6: Pythia-410M checkpoints (H5), two panels sharing the step axis
    h5 = json.loads((src / "checkpoints-pythia-410m/pythia-410m-H5.json").read_text())
    per = sorted(h5["per_step"], key=lambda r_: r_["step"])
    steps = np.array([r_["step"] for r_ in per])
    gate = np.array([r_["passes_gate"] for r_ in per])
    comp = np.array([r_["compensation"] for r_ in per])
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7, 5.6), sharex=True, gridspec_kw={"height_ratios": [3, 2]})
    a1.fill_between(steps[gate], comp[gate, 1], comp[gate, 2], color=BLUE, alpha=0.18, lw=0)
    a1.plot(steps[gate], comp[gate, 0], color=BLUE, marker="o", ms=6, mec=SURFACE, mew=1.2)
    a1.axhline(0, color=INK2, lw=0.8)
    a1.set_ylabel("compensation 1 − TE/DE")
    a1.set_title(f"Spearman ρ = {h5['spearman']:.2f} (95% CI {h5['spearman_ci'][0]:.2f}–{h5['spearman_ci'][1]:.2f})",
                 fontsize=9.5, loc="left", fontweight="normal", color=INK2)
    a2.plot(steps, [r_["ld_mean"] for r_ in per], color=INK2, marker="o", ms=5, lw=1.4, mec=SURFACE)
    a2.scatter(steps[~gate], np.array([r_["ld_mean"] for r_ in per])[~gate], s=46, facecolor=SURFACE,
               edgecolor=RED, lw=1.5, zorder=4, label="fails competence gate")
    a2.axhline(1.0, color=INK2, lw=0.8, ls="--")
    a2.set_ylabel("mean logit difference")
    a2.set_xscale("log")
    a2.set_xlabel("training step (log scale)")
    a2.legend(fontsize=8, loc="lower right")
    save(fig, "checkpoints.png")
    data["checkpoints"] = [{"step": r_["step"], "passes_gate": r_["passes_gate"], "ld_mean": r_["ld_mean"],
                            "acc": r_["acc"], "top_heads": r_["top_heads"], "de_removed": r_["de_removed"],
                            "compensation": r_["compensation"]} for r_ in per]
    data["checkpoints_spearman"] = {"rho": h5["spearman"], "ci": h5["spearman_ci"], "steps": h5["gated_steps"]}


def part_b(data: dict):
    p = Path("outputs/partb/summary.json")
    if not p.exists():
        print("no outputs/partb/summary.json; run 07_partb_summarize.py first")
        return
    s = json.loads(p.read_text())
    colours = {"none": GREY, "standard": BLUE, "drophead": ORANGE}
    fig, ax = plt.subplots(figsize=(7, 3.8))
    for arm, dev in s["development"].items():
        ax.plot(np.array(dev["tokens"]) / 1e6, dev["pooled_mean"], color=colours[arm], marker="o", ms=5,
                mec=SURFACE, label=arm)
    ax.set_xlabel("training tokens (millions)")
    ax.set_ylabel("pooled self-repair fraction\n(mean of six seeds)")
    ax.legend(fontsize=8.5)
    save(fig, "partb_development.png")
    fig, ax = plt.subplots(figsize=(7, 3.8))
    for i, arm in enumerate(["none", "standard", "drophead"]):
        vals = s["per_arm"][arm]
        for seed, v in vals.items():
            ax.scatter(i + (int(seed) - 2.5) * 0.04, v["self_repair_pooled"], color=colours[arm], s=36,
                       edgecolor=SURFACE, zorder=3)
        ax.hlines(np.mean([v["self_repair_pooled"] for v in vals.values()]), i - 0.25, i + 0.25,
                  color=INK, lw=1.6)
    for seed in s["seeds"]:
        ys = [s["per_arm"][a].get(str(seed), s["per_arm"][a].get(seed, {})).get("self_repair_pooled")
              for a in ("none", "standard", "drophead")]
        if None not in ys:
            ax.plot([0, 1, 2], ys, color=GRID, lw=1, zorder=1)
    ax.set_xticks([0, 1, 2], ["none", "standard dropout", "DropHead"])
    ax.set_ylabel("final pooled self-repair fraction")
    ax.grid(axis="x", visible=False)
    save(fig, "partb_final.png")
    data["partb"] = s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="outputs/colab")
    ap.add_argument("--only", choices=["partA", "partB"])
    args = ap.parse_args()
    path = FIG / "data.json"
    data = json.loads(path.read_text()) if path.exists() else {}
    if args.only in (None, "partA"):
        part_a(Path(args.src), data)
    if args.only in (None, "partB"):
        part_b(data)
    FIG.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=1, default=float))
    print("wrote", path)


if __name__ == "__main__":
    main()
