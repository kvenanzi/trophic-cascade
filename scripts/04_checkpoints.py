"""H5: compensation of the top three heads across Pythia-410M training checkpoints
(§4.3 item 4). Run on Colab (notebooks/01_part_a.ipynb).

    python scripts/04_checkpoints.py [--offline] [--model pythia-410m]

Each checkpoint is measured as in scripts/03_models.py, with the top three heads
re-selected at that checkpoint. The script then computes, over the checkpoints that
pass the competence gate, the Spearman correlation between training step and
compensation, with a bootstrap interval that resamples prompts (the same resample at
every checkpoint, since every checkpoint sees the same 600 prompts).
"""

import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch

from trophic import wb
from trophic.effects import compensation
from trophic.experiments import model_study
from trophic.ioi import standard_prompts
from trophic.models import load

OUT = Path("outputs/checkpoints")
STEPS = [1000, 2000, 4000, 8000, 16000, 32000, 48000, 64000, 96000, 128000, 143000]


def spearman(x, y) -> float:
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    return float(np.corrcoef(rx, ry)[0, 1])


def analyse(model_name: str, n_boot: int = 2000) -> dict:
    rows = [json.loads((OUT / f"{model_name}-{s}.json").read_text()) for s in STEPS
            if (OUT / f"{model_name}-{s}.json").exists()]
    arrays = {r["step"]: np.load(OUT / f"{model_name}-{r['step']}.npz") for r in rows}
    gated = [r["step"] for r in rows if r["passes_gate"]]
    c = [compensation(arrays[s]["ld0"], arrays[s]["ld1"], arrays[s]["de_removed"]) for s in gated]
    rng = np.random.default_rng(0)
    n = len(arrays[gated[0]]["ld0"]) if gated else 0
    boots = []
    for _ in range(n_boot if len(gated) >= 3 else 0):
        idx = rng.integers(0, n, n)
        cb = [compensation(arrays[s]["ld0"][idx], arrays[s]["ld1"][idx], arrays[s]["de_removed"][idx])
              for s in gated]
        boots.append(spearman(gated, cb))
    out = {"model": model_name, "steps": [r["step"] for r in rows], "gated_steps": gated,
           "compensation": dict(zip(map(str, gated), c)),
           "spearman": spearman(gated, c) if len(gated) >= 3 else None,
           "spearman_ci": [float(x) for x in np.percentile(boots, [2.5, 97.5])] if boots else None,
           "per_step": rows}
    (OUT / f"{model_name}-H5.json").write_text(json.dumps(out, indent=1, default=float))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--model", default="pythia-410m")
    ap.add_argument("--steps", type=int, nargs="+", default=STEPS)
    ap.add_argument("--n-boot", type=int, default=2000)
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--analyse-only", action="store_true")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if not args.analyse_only:
        ioi, abc = standard_prompts()
        for step in args.steps:
            if (OUT / f"{args.model}-{step}.json").exists():
                print(f"step {step}: done already")
                continue
            t0 = time.time()
            run = wb.init(job_type="checkpoints", group=f"checkpoints-{args.model}",
                          name=f"{args.model}-step{step}", mode="offline" if args.offline else None,
                          config={"model": args.model, "checkpoint": step, "k": 3, "ablation": "mean"})
            model = load(args.model, checkpoint=step)
            res = model_study(model, ioi, abc, n_boot=args.n_boot, batch_size=args.batch_size)
            s = {**res["summary"], "model": args.model, "step": step, "seconds": time.time() - t0}
            (OUT / f"{args.model}-{step}.json").write_text(json.dumps(s, indent=1, default=float))
            np.savez_compressed(OUT / f"{args.model}-{step}.npz", **res["arrays"])
            print(f"step {step}: ld {s['ld_mean']:.2f} acc {s['acc']:.3f} gate {s['passes_gate']} "
                  f"top {s['top_heads']} c {s['compensation']}")
            run.summary.update({"step": step, "ld_mean": s["ld_mean"], "acc": s["acc"],
                                "passes_gate": s["passes_gate"], "compensation": s["compensation"][0],
                                "de_removed": s["de_removed"], "top_heads": s["top_heads"]})
            run.finish()
            del model
            torch.cuda.empty_cache()
    res = analyse(args.model, args.n_boot)
    print("H5:", {k: res[k] for k in ("gated_steps", "compensation", "spearman", "spearman_ci")})

    import wandb
    run = wb.init(job_type="checkpoints-summary", group=f"checkpoints-{args.model}",
                  name=f"{args.model}-H5", mode="offline" if args.offline else None)
    run.define_metric("checkpoint_step")
    for k in ("compensation", "compensation_lo", "compensation_hi", "de_top3", "ld_mean", "acc"):
        run.define_metric(k, step_metric="checkpoint_step")
    for r in res["per_step"]:
        run.log({"checkpoint_step": r["step"], "compensation": r["compensation"][0],
                 "compensation_lo": r["compensation"][1], "compensation_hi": r["compensation"][2],
                 "de_top3": r["de_removed"], "ld_mean": r["ld_mean"], "acc": r["acc"]})
    run.summary.update({"spearman": res["spearman"], "spearman_lo": (res["spearman_ci"] or [None])[0],
                        "spearman_hi": (res["spearman_ci"] or [None, None])[1]})
    art = wandb.Artifact(f"checkpoints-{args.model}", type="results")
    art.add_dir(str(OUT))
    run.log_artifact(art)
    run.finish()


if __name__ == "__main__":
    main()
