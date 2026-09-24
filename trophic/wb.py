"""Weights & Biases constants, and the run and sweep IDs the write-up is built from."""

ENTITY = "within-noise"
PROJECT = "trophic-cascade"

# Filled in as the runs are made, in story order (docs/post/README.md Appendix A).
STORY_RUNS: dict[str, str] = {}
SWEEP_IDS: dict[str, str] = {}


def init(**kw):
    import wandb
    kw.setdefault("entity", ENTITY)
    kw.setdefault("project", PROJECT)
    return wandb.init(**kw)
