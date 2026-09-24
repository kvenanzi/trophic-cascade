"""H4: the top three heads removed as a set in five pretrained models (§4.3 item 3).

    uv run scripts/03_models.py [--offline] [--models gpt2 gpt2-medium ...]

Writes outputs/models/<model>.json and logs one W&B run per model (group `models`).
"""

import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch

from trophic import wb
from trophic.experiments import model_study
from trophic.ioi import standard_prompts
from trophic.models import load

OUT = Path("outputs/models")
MODELS = ["gpt2", "gpt2-medium", "pythia-160m", "pythia-410m", "pythia-1.4b"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--models", nargs="+", default=MODELS)
    ap.add_argument("--n-boot", type=int, default=2000)
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--load-fp16", nargs="*", default=["pythia-1.4b"],
                    help="models loaded in float16 and cast to float32 on the GPU (host memory)")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    ioi, abc = standard_prompts()
    for name in args.models:
        t0 = time.time()
        run = wb.init(job_type="models", group="models", name=f"models-{name}",
                      mode="offline" if args.offline else None,
                      config={"model": name, "k": 3, "ablation": "mean", "n_boot": args.n_boot,
                              "load_fp16": name in args.load_fp16})
        model = load(name, load_dtype=torch.float16 if name in args.load_fp16 else None)
        res = model_study(model, ioi, abc, n_boot=args.n_boot, batch_size=args.batch_size)
        s = res["summary"]
        s.update({"model": name, "seconds": time.time() - t0,
                  "device": torch.cuda.get_device_name() if torch.cuda.is_available() else "cpu"})
        (OUT / f"{name}.json").write_text(json.dumps(s, indent=1, default=float))
        np.savez_compressed(OUT / f"{name}.npz", **res["arrays"])
        print(f"{name}: ld {s['ld_mean']:.2f} acc {s['acc']:.3f} gate {s['passes_gate']} "
              f"top {s['top_heads']} DE {s['de_removed']:.2f} TE {s['te']:.2f} "
              f"c {s['compensation']} ({s['seconds']:.0f}s)")
        run.summary.update({"ld_mean": s["ld_mean"], "acc": s["acc"], "passes_gate": s["passes_gate"],
                            "compensation": s["compensation"][0], "compensation_lo": s["compensation"][1],
                            "compensation_hi": s["compensation"][2], "ln_share": s["ln_share"][0]})
        import wandb
        art = wandb.Artifact(f"models-{name}", type="results")
        art.add_file(str(OUT / f"{name}.json"))
        art.add_file(str(OUT / f"{name}.npz"))
        run.log_artifact(art)
        run.finish()
        del model
        torch.cuda.empty_cache()

    # One summary run with the cross-model chart (H4)
    import wandb
    from trophic import plots
    done = [m for m in MODELS if (OUT / f"{m}.json").exists()]
    rows = [json.loads((OUT / f"{m}.json").read_text()) for m in done]
    run = wb.init(job_type="models-summary", group="models", name="models-H4",
                  mode="offline" if args.offline else None)
    table = wandb.Table(columns=["model", "passes_gate", "ld_mean", "acc", "top_heads", "de_removed",
                                 "te", "compensation", "compensation_lo", "compensation_hi", "ln_share"],
                        data=[[r["model"], r["passes_gate"], r["ld_mean"], r["acc"], r["top_heads"],
                               r["de_removed"], r["te"], *r["compensation"], r["ln_share"][0]] for r in rows])
    fig = plots.interval_bars(done, [r["compensation"][0] for r in rows],
                              [r["compensation"][1] for r in rows], [r["compensation"][2] for r in rows],
                              "compensation 1 - TE/DE", "Top-3 heads removed: compensation by model (95% CI)")
    run.log({"models": table, "charts/compensation_by_model": wandb.Image(fig),
             "charts/compensation_bar": wandb.plot.bar(table, "model", "compensation",
                                                       title="Compensation by model")})
    run.finish()


if __name__ == "__main__":
    main()
