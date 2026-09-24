"""H6 and H6c: paired analysis of the Part B sweep (§4.6).

    uv run scripts/07_partb_summarize.py --sweep <sweep id>      # from W&B
    uv run scripts/07_partb_summarize.py --local models/          # from history.json files

For each seed, the three arms' final pooled self-repair fractions give the contrasts
standard - none, drophead - standard, drophead - none. H6c compares each dropout run's
final value with the checkpoint of the same seed's no-dropout run whose validation loss
is closest to the dropout run's final validation loss. Writes outputs/partb/summary.json
and summary.md.
"""

import argparse
import json
from pathlib import Path

import numpy as np

from trophic import wb
from trophic.stats import paired

OUT = Path("outputs/partb")
CONTRASTS = [("standard", "none"), ("drophead", "standard"), ("drophead", "none")]


def load_histories(sweep: str | None, local: str | None) -> dict:
    runs = {}
    if local:
        for f in Path(local).glob("*/history.json"):
            d = json.loads(f.read_text())
            if not d["config"].get("smoke"):
                runs[(d["config"]["seed"], d["config"]["arm"])] = d
        return runs
    import wandb
    api = wandb.Api()
    sw = api.sweep(f"{wb.ENTITY}/{wb.PROJECT}/{sweep}")
    for r in sw.runs:
        if r.state != "finished" or r.config.get("smoke"):
            continue
        arts = [a for a in r.logged_artifacts() if a.type == "measurements"]
        if not arts:
            continue
        d = json.loads((Path(arts[0].download()) / "history.json").read_text())
        d["run_id"] = r.id
        key = (d["config"]["seed"], d["config"]["arm"])
        if key in runs:
            print(f"note: duplicate cell {key}; keeping the first ({runs[key].get('run_id')})")
            continue
        runs[key] = d
    return runs


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--sweep")
    g.add_argument("--local")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    runs = load_histories(args.sweep, args.local)
    seeds = sorted({s for s, _ in runs})
    arms = ["none", "standard", "drophead"]
    missing = [(s, a) for s in seeds for a in arms if (s, a) not in runs]
    final = {k: v["history"][-1] for k, v in runs.items()}

    table = {a: {s: {m: final[(s, a)][m] for m in ("self_repair_pooled", "self_repair_mean", "val_loss")}
                 for s in seeds if (s, a) in final} for a in arms}
    out = {"n_runs": len(runs), "seeds": seeds, "missing": missing, "per_arm": table}
    for metric in ("self_repair_pooled", "self_repair_mean", "val_loss"):
        out[metric] = {f"{a}-{b}": paired({s: final[(s, a)][metric] - final[(s, b)][metric]
                                           for s in seeds if (s, a) in final and (s, b) in final})
                       for a, b in CONTRASTS}

    # H6c: matched validation loss against the paired no-dropout run's checkpoints
    matched = {}
    for arm in ("standard", "drophead"):
        diffs, detail = {}, {}
        for s in seeds:
            if (s, arm) not in runs or (s, "none") not in runs:
                continue
            vl = final[(s, arm)]["val_loss"]
            ref = runs[(s, "none")]["history"]
            j = int(np.argmin([abs(h["val_loss"] - vl) for h in ref]))
            diffs[s] = final[(s, arm)]["self_repair_pooled"] - ref[j]["self_repair_pooled"]
            detail[s] = {"val_loss": vl, "none_step": ref[j]["step"], "none_val_loss": ref[j]["val_loss"]}
        matched[f"{arm}-none"] = {**paired(diffs), "matched": detail}
    out["H6c_matched_val_loss"] = matched

    # Development: pooled self-repair at each measurement point, mean over seeds per arm
    out["development"] = {a: {"tokens": [h["tokens"] for h in runs[(seeds[0], a)]["history"]],
                              "pooled_mean": np.mean([[h["self_repair_pooled"] for h in runs[(s, a)]["history"]]
                                                      for s in seeds if (s, a) in runs], 0).tolist(),
                              "val_loss_mean": np.mean([[h["val_loss"] for h in runs[(s, a)]["history"]]
                                                        for s in seeds if (s, a) in runs], 0).tolist()}
                          for a in arms if (seeds[0], a) in runs}
    (OUT / "summary.json").write_text(json.dumps(out, indent=1, default=float))

    lines = ["| contrast | metric | mean | 95% CI | positive seeds | sign-test p |", "|---|---|---|---|---|---|"]
    for metric in ("self_repair_pooled", "self_repair_mean", "val_loss"):
        for c, r in out[metric].items():
            ci = f"{r['ci95'][0]:+.4f} to {r['ci95'][1]:+.4f}" if r["ci95"] else "–"
            lines.append(f"| {c} | {metric} | {r['mean']:+.4f} | {ci} | {r['n_pos']} / {r['n']} | {r['sign_p']:.3f} |")
    for c, r in matched.items():
        ci = f"{r['ci95'][0]:+.4f} to {r['ci95'][1]:+.4f}" if r["ci95"] else "–"
        lines.append(f"| {c} (matched val loss) | self_repair_pooled | {r['mean']:+.4f} | {ci} | {r['n_pos']} / {r['n']} | {r['sign_p']:.3f} |")
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    if missing:
        print("missing cells:", missing)


if __name__ == "__main__":
    main()
