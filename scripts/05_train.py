"""Part B: train one model, or time the training loop to fix the token budget.

    python scripts/05_train.py --arm none --seed 0            # one run (Colab A100)
    python scripts/05_train.py --smoke --arm drophead         # about a minute, tiny budget
    python scripts/05_train.py --timing                        # §4.4: tokens/s -> budget

The timing mode trains the registered model on the real data for --timing-steps steps
after a warm-up and prints the budget rule of §4.4: the largest multiple of ten million
tokens that trains in 20 minutes or less, capped at one pass over the training split.
"""

import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch

from trophic.data import Windows, prepare
from trophic.model import build
from trophic.train import TrainConfig, train


def timing(cfg: TrainConfig, steps: int, warmup: int = 20, minutes: float = 20.0) -> dict:
    device = torch.device("cuda")
    use_bf16 = torch.cuda.get_device_capability()[0] >= 8
    prepare(cfg.data_dir)
    w = Windows(Path(cfg.data_dir) / "train.bin", cfg.ctx)
    results = {}
    for arm in ("none", "standard", "drophead"):
        model = build(arm, 0, p=cfg.p, n_layer=cfg.n_layer, n_head=cfg.n_head, d_model=cfg.d_model,
                      d_mlp=cfg.d_mlp, ctx=cfg.ctx).to(device).train()
        opt = torch.optim.AdamW(model.parameters(), lr=cfg.lr, fused=True)
        idx = np.random.default_rng(0).permutation(w.n)
        for s in range(warmup + steps):
            if s == warmup:
                torch.cuda.synchronize()
                t0 = time.time()
            x = torch.from_numpy(w.get(idx[s * cfg.batch_size:(s + 1) * cfg.batch_size])).to(device)
            with torch.autocast("cuda", dtype=torch.bfloat16, enabled=use_bf16):
                logits = model(x[:, :-1]).logits
            loss = torch.nn.functional.cross_entropy(logits.float().reshape(-1, logits.size(-1)),
                                                     x[:, 1:].reshape(-1))
            opt.zero_grad(set_to_none=True)
            loss.backward()
            opt.step()
        torch.cuda.synchronize()
        results[arm] = steps * cfg.batch_size * cfg.ctx / (time.time() - t0)
        del model, opt
    slowest = min(results.values())
    one_pass = (w.n * cfg.ctx) // 10_000_000 * 10_000_000
    budget = min(int(slowest * minutes * 60) // 10_000_000 * 10_000_000, one_pass)
    return {"tokens_per_s": results, "slowest": slowest, "one_pass_tokens": w.n * cfg.ctx,
            "budget_tokens": budget, "device": torch.cuda.get_device_name()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", default="none")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--tokens", type=int, default=None)
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--compile", action="store_true")
    ap.add_argument("--timing", action="store_true")
    ap.add_argument("--timing-steps", type=int, default=200)
    ap.add_argument("--data-dir", default="data/tinystories")
    args = ap.parse_args()
    cfg = TrainConfig(arm=args.arm, seed=args.seed, smoke=args.smoke, offline=args.offline,
                      compile=args.compile, data_dir=args.data_dir)
    if args.tokens:
        cfg.tokens = args.tokens
    if args.timing:
        r = timing(cfg, args.timing_steps)
        print(json.dumps(r, indent=1))
        Path("outputs").mkdir(exist_ok=True)
        Path("outputs/timing.json").write_text(json.dumps(r, indent=1))
        from trophic import wb
        run = wb.init(job_type="timing", group="dropout", name="timing",
                      mode="offline" if args.offline else None,
                      config={"timing_steps": args.timing_steps, "batch_size": cfg.batch_size,
                              "ctx": cfg.ctx, "rule": "largest 1e7 multiple trained in <= 20 min"})
        run.summary.update({"slowest_tokens_per_s": r["slowest"], "budget_tokens": r["budget_tokens"],
                            **{f"tokens_per_s/{k}": v for k, v in r["tokens_per_s"].items()}})
        run.finish()
        return
    train(cfg)


if __name__ == "__main__":
    main()
