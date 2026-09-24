"""Register the Part B sweep (sweeps/dropout.yaml) with the timed token budget.

    python scripts/06_sweep.py --create --tokens 300000000
    python scripts/06_sweep.py --create --smoke            # one-cell throwaway sweep

A grid sweep hands each (arm, seed) cell out once; agents run them with
`wandb.agent(sweep_id, function=..., count=...)` (notebooks/02_dropout_sweep.ipynb).
"""

import argparse
import copy
from pathlib import Path

import wandb
import yaml

from trophic import wb

ROOT = Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--create", action="store_true")
    ap.add_argument("--config", default=str(ROOT / "sweeps" / "dropout.yaml"))
    ap.add_argument("--tokens", type=int, default=None)
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    config = yaml.safe_load(Path(args.config).read_text())
    if args.smoke:
        config = copy.deepcopy(config)
        for name, spec in config["parameters"].items():
            if "values" in spec:
                config["parameters"][name] = {"value": spec["values"][0]}
        config["parameters"]["smoke"] = {"value": True}
        config["name"] = f"smoke-{config['name']}"
    elif not args.tokens:
        raise SystemExit("--tokens is required: the budget from `05_train.py --timing` (§4.4)")
    if args.tokens:
        config["parameters"]["tokens"] = {"value": args.tokens}
    if args.create:
        sid = wandb.sweep(config, entity=wb.ENTITY, project=wb.PROJECT)
        print(f"sweep id: {wb.ENTITY}/{wb.PROJECT}/{sid}")
        print(f"https://wandb.ai/{wb.ENTITY}/{wb.PROJECT}/sweeps/{sid}")
    else:
        print(yaml.safe_dump(config))


if __name__ == "__main__":
    main()
