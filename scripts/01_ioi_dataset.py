"""Build the 600 IOI prompts and their ABC twins, save them, and log them as the W&B
artifact `ioi-prompts`.

    uv run scripts/01_ioi_dataset.py [--offline]
"""

import argparse
import json
from pathlib import Path

from trophic import wb
from trophic.ioi import N_PER_TEMPLATE, SEED, TEMPLATES, single_token_vocab, standard_prompts

OUT = Path("outputs/ioi")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true")
    args = ap.parse_args()
    ioi, abc = standard_prompts()
    vocab = single_token_vocab()
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "prompts.jsonl", "w") as f:
        for p, q in zip(ioi, abc):
            f.write(json.dumps({"ioi": p.to_dict(), "abc": q.to_dict()}) + "\n")
    (OUT / "vocab.json").write_text(json.dumps(vocab, indent=1))
    print(f"{len(ioi)} prompts, {len(TEMPLATES)} templates; vocab sizes",
          {k: len(v) for k, v in vocab.items()})
    for p, q in list(zip(ioi, abc))[:3]:
        print(f"  {p.order}: {p.text} ->{p.io}   | ABC: {q.text}")

    import wandb
    run = wb.init(job_type="dataset", name="ioi-prompts", mode="offline" if args.offline else None,
                  config={"n_per_template": N_PER_TEMPLATE, "seed": SEED, "n_templates": len(TEMPLATES)})
    art = wandb.Artifact("ioi-prompts", type="dataset",
                         description="600 IOI prompts (15 templates x 40, ABBA/BABA) with ABC twins",
                         metadata={"n": len(ioi), **{f"n_{k}": len(v) for k, v in vocab.items()}})
    art.add_file(str(OUT / "prompts.jsonl"))
    art.add_file(str(OUT / "vocab.json"))
    run.log_artifact(art)
    table = wandb.Table(columns=["template", "order", "prompt", "io", "s", "abc_prompt"],
                        data=[[p.template, p.order, p.text, p.io, p.s, q.text] for p, q in zip(ioi, abc)])
    run.log({"prompts": table})
    run.finish()


if __name__ == "__main__":
    main()
