# Trophic cascades in a transformer

Ecologists measure a community by removing a species and recording what the others do,
and have published measures for the result: interaction strength, the log response ratio,
community importance (keystones), mesopredator release, and the hydra effect. This project
applies those measures, as published, to the attention heads of transformer language
models, and trains small models from scratch to test whether dropout produces the
compensation seen when heads are removed. The hypotheses were committed (`cca53fc`)
before any registered experiment was run.

**Results.**
- **GPT-2 small, indirect-object circuit.** Removing the three name-mover heads *raises*
  the logit difference (compensation 1.042, 95% CI 1.023–1.061). Backup and negative name
  movers carry 94.5% of the offset.
- **Keystones.** All four S-inhibition heads and three induction heads are keystones in
  the sense of Power et al (1996).
- **Attenuation.** A removal's effect on head activity attenuates with distance in the
  circuit.
- **Five models.** Compensation ranges from none (Pythia-1.4B) to 1.04, and in
  Pythia-410M it rises during training from −0.87 to 0.41.
- **Dropout (18 models trained from scratch).** The pooled self-repair fraction is 0.36
  without dropout, 0.62 with standard dropout, and 0.67 with head dropout. The order holds
  for all six seeds, including at matched validation loss.

The full write-up is [docs/post/README.md](docs/post/README.md). Every run is in the W&B
project [within-noise/trophic-cascade](https://wandb.ai/within-noise/trophic-cascade),
presented in the
[W&B Report](https://wandb.ai/within-noise/trophic-cascade/reports/Trophic-cascades-in-a-transformer--VmlldzoxODAwMjk2OA==).

## Layout

```
trophic/       the package: IOI prompts, removal runner, ecological measures, Part B model,
               training, self-repair measurement, statistics, plots, W&B constants
scripts/       numbered pipeline (below)
notebooks/     Colab: 01_part_a (removal experiments), 02_dropout_sweep (training sweep)
sweeps/        W&B sweep definition for Part B
tests/         pytest: prompt structure, ablation hooks, direct-effect decomposition,
               DropHead masking, HF-to-TransformerLens conversion, a training smoke run
docs/post/     the write-up, references.bib, figures and figures/data.json
outputs/       local results (gitignored)
```

## Running it

Every experiment runs on a Colab A100 through the two notebooks, which clone this repo
and log to W&B (secrets `WANDB_API_KEY`, and `GITHUB_TOKEN` while the repo is private).
Locally, [uv](https://docs.astral.sh/uv/) sets up the environment for development, tests,
and the analysis scripts:

```bash
uv sync
uv run pytest                                   # 9 tests, about 15 s

# Part A (notebooks/01_part_a.ipynb runs these on Colab)
python scripts/01_ioi_dataset.py                # 600 IOI prompts + ABC twins -> artifact ioi-prompts
python scripts/02_gpt2_removals.py              # GPT-2 small: H1-H3, keystones, interaction matrix
python scripts/03_models.py                     # H4: five models
python scripts/04_checkpoints.py                # H5: eleven Pythia-410M checkpoints

# Part B (notebooks/02_dropout_sweep.ipynb)
python scripts/05_train.py --smoke --arm drophead   # pipeline check, about a minute
python scripts/05_train.py --timing                 # tokens/s -> the registered token budget
python scripts/06_sweep.py --create --tokens <budget>
#   then wandb.agent(...) in the notebook: 3 regimes x 6 seeds

# Analysis and write-up (local)
uv run scripts/07_partb_summarize.py --sweep fhuassaa   # H6, H6c -> outputs/partb/
uv run scripts/08_figures.py                            # docs/post/figures/ (needs outputs/colab/)
uv run scripts/09_report.py --url <report url>          # rebuild the W&B Report in place
```

`scripts/08_figures.py` reads the Part A artifacts downloaded from W&B into
`outputs/colab/<artifact name>/` (for example `gpt2-removals`, `models-pythia-410m`,
`checkpoints-pythia-410m`).

TransformerLens is pinned below 4.0, which removed `HookedTransformer`. Models above
about 500M parameters do not fit in the local machine's memory; run them on Colab.
