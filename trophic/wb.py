"""Weights & Biases constants, and the run and sweep IDs the write-up is built from."""

ENTITY = "within-noise"
PROJECT = "trophic-cascade"

# The Colab A100 reference runs of Part A (notebooks/01_part_a.ipynb). The same
# experiments on the local GTX 1070 are tagged `local-gtx1070` and agree to the fifth
# decimal place.
STORY_RUNS: dict[str, str] = {
    "ioi-prompts": "ves877bz",
    "gpt2-removals": "iiltnel1",
    "models-gpt2": "rjc6ndi6",
    "models-gpt2-medium": "ke9tk0qt",
    "models-pythia-160m": "of54j7j7",
    "models-pythia-410m": "dnxf74lk",
    "models-pythia-1.4b": "esc71gqc",
    "models-H4": "3zy48ays",
    "checkpoints-H5": "bngnyxjp",
    "timing": "fmdm39r6",
    "smoke": "5gnva5ju",
}
MODEL_RUNS = [STORY_RUNS[k] for k in ("models-gpt2", "models-gpt2-medium", "models-pythia-160m",
                                      "models-pythia-410m", "models-pythia-1.4b")]
SWEEP_IDS: dict[str, str] = {"dropout": "fhuassaa"}
REPORT_URL = "https://wandb.ai/within-noise/trophic-cascade/reports/Trophic-cascades-in-a-transformer--VmlldzoxODAwMjk2OA=="


def init(**kw):
    import wandb
    kw.setdefault("entity", ENTITY)
    kw.setdefault("project", PROJECT)
    return wandb.init(**kw)
