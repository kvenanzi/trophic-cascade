"""Part B training: one small GPT-2 on TinyStories under one regime (§4.4-4.5).

`train(TrainConfig(...))` trains, measures validation loss and self-repair at eight
evenly spaced points (and at step 0), logs everything to W&B, and optionally logs the
final weights as an artifact. Under a W&B sweep, `train(cfg, sweep=True)` takes the
sweep's parameters (arm, seed, and anything else in the config) from wandb.config.
"""

from __future__ import annotations

import json
import math
import time
from dataclasses import asdict, dataclass, field, fields
from pathlib import Path

import numpy as np
import torch

from . import wb
from .data import Windows, prepare
from .model import build, to_hooked
from .selfrepair import measure


@dataclass
class TrainConfig:
    arm: str = "none"                  # none | standard | drophead
    seed: int = 0
    p: float = 0.1                     # dropout / head-dropout probability for the arm
    tokens: int = 300_000_000          # token budget, identical in every arm (§4.4)
    batch_size: int = 128              # sequences per step
    ctx: int = 256
    n_layer: int = 6
    n_head: int = 8
    d_model: int = 384
    d_mlp: int = 1536
    lr: float = 1e-3
    warmup_frac: float = 0.02
    min_lr_frac: float = 0.1
    weight_decay: float = 0.1
    grad_clip: float = 1.0
    measure_points: int = 8            # self-repair measured after each 1/8 of the budget
    measure_seqs: int = 256            # held-out sequences for self-repair (65,536 positions)
    val_seqs: int = 1024               # held-out sequences for validation loss
    data_dir: str = "data/tinystories"
    output_dir: str = "models"
    log_model: bool = True
    compile: bool = False
    smoke: bool = False                # tiny budget and model: a pipeline check in about a minute
    offline: bool = False
    run_name: str | None = None
    tags: list = field(default_factory=list)

    def resolved(self) -> "TrainConfig":
        if self.smoke:
            self.tokens = min(self.tokens, 40 * self.batch_size * self.ctx)
            self.measure_seqs = min(self.measure_seqs, 16)
            self.val_seqs = min(self.val_seqs, 32)
            self.log_model = False
        return self


def lr_at(step: int, total: int, cfg: TrainConfig) -> float:
    warm = max(1, int(cfg.warmup_frac * total))
    if step < warm:
        return cfg.lr * (step + 1) / warm
    prog = (step - warm) / max(1, total - warm)
    return cfg.lr * (cfg.min_lr_frac + (1 - cfg.min_lr_frac) * 0.5 * (1 + math.cos(math.pi * prog)))


@torch.no_grad()
def val_loss(model, windows: np.ndarray, device, batch_size: int, amp) -> float:
    model.eval()
    tot, n = 0.0, 0
    for b in range(0, len(windows), batch_size):
        x = torch.from_numpy(windows[b:b + batch_size]).to(device)
        with amp():
            out = model(x[:, :-1], labels=None)
        logits = out.logits.float()
        loss = torch.nn.functional.cross_entropy(logits.reshape(-1, logits.size(-1)),
                                                 x[:, 1:].reshape(-1), reduction="sum")
        tot += loss.item()
        n += x[:, 1:].numel()
    model.train()
    return tot / n


def train(cfg: TrainConfig, sweep: bool = False) -> dict:
    import wandb
    torch.set_grad_enabled(True)       # trophic.models.load() turns gradients off globally
    cfg.resolved()
    if not sweep:
        run = wb.init(job_type="train", group="dropout", name=cfg.run_name,
                      mode="offline" if cfg.offline else None, tags=cfg.tags, config=asdict(cfg))
    else:
        run = wb.init(job_type="train", group="dropout", tags=cfg.tags)
        known = {f.name for f in fields(TrainConfig)}
        for k, v in dict(run.config).items():
            if k in known:
                setattr(cfg, k, v)
        cfg.resolved()
        run.config.update({k: v for k, v in asdict(cfg).items() if k not in run.config},
                          allow_val_change=True)
    if cfg.run_name is None:
        run.name = f"{cfg.arm}-s{cfg.seed}" + ("-smoke" if cfg.smoke else "")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    use_bf16 = device.type == "cuda" and torch.cuda.get_device_capability()[0] >= 8
    amp = (lambda: torch.autocast("cuda", dtype=torch.bfloat16)) if use_bf16 \
        else (lambda: torch.autocast(device.type, enabled=False))
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True

    counts = prepare(cfg.data_dir)
    train_w = Windows(Path(cfg.data_dir) / "train.bin", cfg.ctx)
    val_w = Windows(Path(cfg.data_dir) / "validation.bin", cfg.ctx)
    # Held-out sets are fixed across runs: the first val_seqs windows for loss, the
    # next measure_seqs for self-repair.
    val_windows = val_w.get(np.arange(cfg.val_seqs))
    meas_windows = torch.from_numpy(val_w.get(np.arange(cfg.val_seqs, cfg.val_seqs + cfg.measure_seqs)))

    steps = cfg.tokens // (cfg.batch_size * cfg.ctx)
    if steps > train_w.n // cfg.batch_size:
        raise ValueError(f"budget of {steps} steps exceeds one pass over {train_w.n} windows")
    # The data order depends on the seed only, so the three arms of a seed see the
    # same windows in the same order.
    order = np.random.default_rng(cfg.seed).permutation(train_w.n)[:steps * cfg.batch_size]

    model = build(cfg.arm, cfg.seed, p=cfg.p, n_layer=cfg.n_layer, n_head=cfg.n_head,
                  d_model=cfg.d_model, d_mlp=cfg.d_mlp, ctx=cfg.ctx).to(device)
    n_params = sum(p.numel() for p in model.parameters())
    decay = [p for n, p in model.named_parameters() if p.dim() >= 2]
    no_decay = [p for n, p in model.named_parameters() if p.dim() < 2]
    opt = torch.optim.AdamW([{"params": decay, "weight_decay": cfg.weight_decay},
                             {"params": no_decay, "weight_decay": 0.0}],
                            lr=cfg.lr, betas=(0.9, 0.95), fused=device.type == "cuda")
    fwd = torch.compile(model) if cfg.compile else model
    run.summary.update({"n_params": n_params, "steps": steps, "train_tokens_available": counts["train"],
                        "device": torch.cuda.get_device_name() if device.type == "cuda" else "cpu"})
    print(f"{run.name}: {n_params / 1e6:.1f}M params, {steps} steps, {cfg.tokens / 1e6:.0f}M tokens, "
          f"bf16={use_bf16}")

    points = sorted({int(round(steps * k / cfg.measure_points)) for k in range(cfg.measure_points + 1)})
    history = []

    def checkpoint(step: int):
        t = time.time()
        vl = val_loss(model, val_windows, device, 64, amp)
        hooked = to_hooked(model, device)
        sr = measure(hooked, meas_windows)
        del hooked
        row = {"step": step, "tokens": step * cfg.batch_size * cfg.ctx, "val_loss": vl,
               "self_repair_pooled": sr["pooled"], "self_repair_mean": sr["mean"],
               **{f"self_repair_layer{l}": v for l, v in enumerate(sr["per_layer"])},
               "measure_seconds": time.time() - t}
        history.append({**row, "per_head": sr["per_head"].tolist(),
                        "removed_sum": sr["removed_sum"].tolist()})
        run.log({f"measure/{k}": v for k, v in row.items()}, step=step)
        print(f"  step {step:>6}  val {vl:.4f}  self-repair pooled {sr['pooled']:.3f} "
              f"mean {sr['mean']:.3f}  ({row['measure_seconds']:.0f}s)")

    model.train()
    t0 = time.time()
    if 0 in points:
        checkpoint(0)
    for step in range(steps):
        idx = order[step * cfg.batch_size:(step + 1) * cfg.batch_size]
        x = torch.from_numpy(train_w.get(idx)).to(device, non_blocking=True)
        for g in opt.param_groups:
            g["lr"] = lr_at(step, steps, cfg)
        with amp():
            logits = fwd(x[:, :-1]).logits
        loss = torch.nn.functional.cross_entropy(logits.float().reshape(-1, logits.size(-1)),
                                                 x[:, 1:].reshape(-1))
        opt.zero_grad(set_to_none=True)
        loss.backward()
        gn = torch.nn.utils.clip_grad_norm_(model.parameters(), cfg.grad_clip)
        opt.step()
        if step % 50 == 0:
            el = time.time() - t0
            run.log({"train/loss": loss.item(), "train/lr": opt.param_groups[0]["lr"],
                     "train/grad_norm": gn.item(),
                     "train/tokens_per_s": (step + 1) * cfg.batch_size * cfg.ctx / el}, step=step)
        if step + 1 in points:
            checkpoint(step + 1)
    train_seconds = time.time() - t0

    final = history[-1]
    run.summary.update({"final/val_loss": final["val_loss"],
                        "final/self_repair_pooled": final["self_repair_pooled"],
                        "final/self_repair_mean": final["self_repair_mean"],
                        "train_seconds": train_seconds})
    cols = [k for k in history[0] if k not in ("per_head", "removed_sum")]
    run.log({"measurements": wandb.Table(columns=cols, data=[[h[k] for k in cols] for h in history])})

    out = Path(cfg.output_dir) / run.name
    out.mkdir(parents=True, exist_ok=True)
    (out / "history.json").write_text(json.dumps({"config": asdict(cfg), "history": history}))
    art = wandb.Artifact(f"measurements-{run.name}", type="measurements")
    art.add_file(str(out / "history.json"))
    run.log_artifact(art)
    if cfg.log_model:
        model.save_pretrained(out / "model")
        mart = wandb.Artifact(f"model-{run.name}", type="model",
                              metadata={"arm": cfg.arm, "seed": cfg.seed, "n_params": n_params})
        mart.add_dir(str(out / "model"))
        run.log_artifact(mart)
    run.finish()
    return {"history": history, "train_seconds": train_seconds}
