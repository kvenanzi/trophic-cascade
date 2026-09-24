"""Part A on GPT-2 small: the reproduction check and hypotheses H1-H3 (§4.3 items 1-2).

    uv run scripts/02_gpt2_removals.py [--offline] [--n-boot 2000]

Writes outputs/gpt2/summary.json (every number the write-up quotes), keystones.csv
(one row per head), and removals.npz (the 144 single-head removals and the
interaction-strength matrix), and logs the same to one W&B run.
"""

import argparse
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

from trophic import wb
from trophic.ablate import IOIRunner
from trophic.effects import CLASSES, LEVELS, heads_str
from trophic.experiments import (attenuation, competence, keystone_table, set_removal,
                                 single_removals, top_heads)
from trophic.ioi import standard_prompts
from trophic.models import load

OUT = Path("outputs/gpt2")


def slim(d):
    """Drop per-prompt arrays from a set_removal result so it can go into JSON."""
    return {k: v for k, v in d.items() if k not in ("run", "delta_de", "delta_de_frozen")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--n-boot", type=int, default=2000)
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    run = wb.init(job_type="removals", name="gpt2-small-removals",
                  mode="offline" if args.offline else None,
                  config={"model": "gpt2", "ablation": "mean", "n_boot": args.n_boot})
    try:
        run.use_artifact("ioi-prompts:latest")
    except Exception as e:                      # offline, or the artifact not yet synced
        print("note: prompts artifact not linked:", type(e).__name__)

    model = load("gpt2")
    ioi, abc = standard_prompts()
    runner = IOIRunner(model, ioi, abc, keep_abc=True)
    base = runner.run()
    summary = {"model": "gpt2", "n_prompts": len(ioi), "baseline": competence(base)}
    de = base["de"].mean(0)
    summary["baseline"]["top_heads_by_abs_de"] = [
        {"head": f"{l}.{h}", "de": float(de[l, h])}
        for l, h in zip(*np.unravel_index(np.argsort(-np.abs(de).ravel())[:12], de.shape))]
    summary["baseline"]["top3_positive"] = heads_str(top_heads(base))
    print("baseline", summary["baseline"])

    # H1: the name movers as a set, mean and resample ablation
    groups = {"backup name movers": CLASSES["backup_name_mover"],
              "negative name movers": CLASSES["negative_name_mover"]}
    h1 = set_removal(runner, base, CLASSES["name_mover"], groups, n_boot=args.n_boot)
    h1r = set_removal(runner, base, CLASSES["name_mover"], groups, mode="resample", n_boot=args.n_boot)
    summary["H1"] = {"mean": slim(h1), "resample": slim(h1r)}
    print("H1 compensation", h1["compensation"], "groups share", h1["offset_share_groups"])
    print("H1 resample compensation", h1r["compensation"])

    # Every class removed as a set, for the class-level food web
    summary["class_removals"] = {c: slim(set_removal(runner, base, hs, n_boot=200))
                                 for c, hs in CLASSES.items()}

    # H2: single-head removals, community importance
    singles = single_removals(runner, base)
    rows = keystone_table(base, singles, CLASSES)
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "keystones.csv", index=False)
    keystones = df[df.keystone].sort_values("effect_share", ascending=False)
    summary["H2"] = {
        "keystones": keystones[["head", "class", "abundance", "effect_share",
                                "community_importance"]].to_dict("records"),
        "name_movers": df[df["class"] == "name_mover"][["head", "abundance", "effect_share",
                                                       "community_importance"]].to_dict("records"),
        "s_inhibition": df[df["class"] == "s_inhibition"][["head", "abundance", "effect_share",
                                                          "community_importance", "keystone"]].to_dict("records"),
    }
    print("H2 keystones:\n", keystones[["head", "class", "abundance", "effect_share",
                                        "community_importance"]].to_string(index=False))

    # Interaction strength matrix: rows = removed head, cols = responding head (own scale)
    base_de = base["de"].mean(0)
    L, H = base_de.shape
    inter = (singles["de"] - base_de[None, None]).reshape(L * H, L * H)
    inter_frozen = (singles["de_frozen"] - base_de[None, None]).reshape(L * H, L * H)
    np.fill_diagonal(inter, 0.0)
    np.fill_diagonal(inter_frozen, 0.0)
    np.savez_compressed(OUT / "removals.npz", ld_single=singles["ld"], de_single=singles["de"],
                        de_frozen_single=singles["de_frozen"], act_single=singles["act"],
                        mlp_single=singles["mlp_de"], interaction=inter,
                        interaction_frozen=inter_frozen, base_de=base["de"], base_ld=base["ld"],
                        base_act=base["act"], nm_delta_de=h1["delta_de"],
                        nm_delta_de_frozen=h1["delta_de_frozen"])

    # H3: attenuation of activity response with circuit distance
    h3 = attenuation(runner, base, LEVELS, n_boot=args.n_boot)
    summary["H3"] = h3
    for r in h3:
        print(f"H3 remove {r['removed']}: |LRR| next {r['lrr_next']:.3f}, after-next "
              f"{r['lrr_after_next']:.3f}, diff {r['difference']}")

    summary["seconds"] = time.time() - t0
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1, default=float))

    import wandb
    run.summary.update({
        "baseline/ld_mean": summary["baseline"]["ld_mean"], "baseline/acc": summary["baseline"]["acc"],
        "H1/compensation": h1["compensation"][0], "H1/compensation_lo": h1["compensation"][1],
        "H1/compensation_hi": h1["compensation"][2],
        "H1/resample_compensation": h1r["compensation"][0],
        "H1/share_backup_negative": h1["offset_share_groups"][0],
        "H1/ln_share": h1["ln_share"][0],
        "H2/n_keystones": int(df.keystone.sum()),
    })
    import matplotlib.pyplot as plt
    from trophic import plots
    ktable = wandb.Table(dataframe=df)
    figs = {
        "charts/interaction_matrix": plots.interaction_heatmap(
            inter, L, H, "GPT-2 small: change in each head's direct effect when one head is removed"),
        "charts/name_mover_removal": plots.release_bars(
            base_de, h1["delta_de"], CLASSES, title="Name movers removed: direct effect before and after"),
        "charts/keystones": plots.keystone_scatter(df, "Community importance of every head (Power et al 1996)"),
    }
    run.log({"keystones": ktable,
             "charts/keystone_scatter": wandb.plot.scatter(ktable, "abundance", "effect_share",
                                                           title="Abundance vs share of trait lost"),
             **{k: wandb.Image(f) for k, f in figs.items()}})
    for f in figs.values():
        plt.close(f)
    art = wandb.Artifact("gpt2-removals", type="results")
    for f in ("summary.json", "keystones.csv", "removals.npz"):
        art.add_file(str(OUT / f))
    run.log_artifact(art)
    run.finish()
    print(f"done in {summary['seconds']:.0f}s")


if __name__ == "__main__":
    main()
