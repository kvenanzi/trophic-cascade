"""Build (or rebuild) the W&B Report with live panels, embedded in the write-up.

    uv run scripts/09_report.py                 # create a new report; prints its URL
    uv run scripts/09_report.py --url <url>     # replace the blocks of an existing report

Panels are bound to the reference runs by ID (trophic/wb.py) and to the Part B sweep by
sweep ID, so a crashed or duplicate run in the same project never lands in a panel.
The Part B results table is read from outputs/partb/summary.md when it exists.
"""

import argparse
from pathlib import Path

import wandb_workspaces.reports.v2 as wr

from trophic.wb import ENTITY, MODEL_RUNS, PROJECT, STORY_RUNS, SWEEP_IDS

TITLE = "Trophic cascades in a transformer"
DESCRIPTION = ("Ecological removal experiments applied to attention heads: mesopredator release, keystones, "
               "attenuation, and whether dropout produces self-repair.")
GITHUB = "https://github.com/kvenanzi/trophic-cascade"
W = 24


def ids(*run_ids) -> str:
    return "ID in [" + ", ".join(f"'{i}'" for i in run_ids) + "]"


def blocks() -> list:
    gpt2 = wr.Runset(entity=ENTITY, project=PROJECT, name="GPT-2 small removals",
                     filters=ids(STORY_RUNS["gpt2-removals"]))
    models = wr.Runset(entity=ENTITY, project=PROJECT, name="Five models", filters=ids(*MODEL_RUNS))
    h4 = wr.Runset(entity=ENTITY, project=PROJECT, name="H4 summary", filters=ids(STORY_RUNS["models-H4"]))
    h5 = wr.Runset(entity=ENTITY, project=PROJECT, name="Pythia-410M checkpoints",
                   filters=ids(STORY_RUNS["checkpoints-H5"]))
    sweep = wr.Runset(entity=ENTITY, project=PROJECT, name="Part B sweep (18 runs)",
                      filters=f"Metric('Sweep') == '{SWEEP_IDS['dropout']}'")
    table = Path("outputs/partb/summary.md")
    partb_table = table.read_text() if table.exists() else "*The Part B table is added when the sweep is complete.*"

    return [
        wr.TableOfContents(),
        wr.H1("What this is"),
        wr.P("Ecologists measure a community by removing a species and recording what the others do. "
             "Interpretability researchers measure a transformer by ablating a head and recording what the "
             "other heads do. This report is the live record of an experiment that applies the ecologists' "
             "measures (interaction strength, mesopredator release, community importance, the log response "
             "ratio) to attention heads, and trains eighteen small models to test whether dropout produces the "
             "compensation seen when heads are removed. The hypotheses were committed before the runs."),
        wr.P([wr.Link(text="Code, pre-registration, and write-up on GitHub", url=GITHUB)]),

        wr.H1("Part A: GPT-2 small"),
        wr.P("Removing the three name-mover heads (9.9, 9.6, 10.0) of the indirect-object circuit removes 4.76 "
             "units of direct effect and raises the logit difference from 3.65 to 3.85: compensation 1.042 "
             "(95% CI 1.023-1.061). The backup name movers and the negative name movers carry 94.5% of the "
             "offset; the final LayerNorm carries 5.8%. All four S-inhibition heads and three induction heads "
             "are keystones in the sense of Power et al (1996): small direct effect, large total effect."),
        wr.PanelGrid(runsets=[gpt2], panels=[
            wr.MediaBrowser(title="Name movers removed: direct effect before and after",
                            media_keys=["charts/name_mover_removal"], num_columns=1,
                            layout=wr.Layout(x=0, y=0, w=W, h=10)),
            wr.MediaBrowser(title="Interaction-strength matrix (144 single-head removals)",
                            media_keys=["charts/interaction_matrix"], num_columns=1,
                            layout=wr.Layout(x=0, y=10, w=W // 2, h=14)),
            wr.MediaBrowser(title="Community importance of every head",
                            media_keys=["charts/keystones"], num_columns=1,
                            layout=wr.Layout(x=W // 2, y=10, w=W // 2, h=14)),
        ]),

        wr.H1("Part A: five models and Pythia-410M's training"),
        wr.P("The same removal of the three largest heads in five pretrained models. Every model solves the task; "
             "four compensate, Pythia-1.4B does not (0.009, 95% CI -0.023 to 0.037). Across Pythia-410M's "
             "training checkpoints, compensation begins strongly negative (-0.87 at step 4,000), crosses zero by "
             "step 16,000, and settles near 0.4 (Spearman rho 0.92)."),
        wr.PanelGrid(runsets=[models], panels=[
            wr.BarPlot(title="Compensation by model", metrics=["compensation"],
                       layout=wr.Layout(x=0, y=0, w=W // 2, h=8)),
            wr.BarPlot(title="Mean logit difference by model", metrics=["ld_mean"],
                       layout=wr.Layout(x=W // 2, y=0, w=W // 2, h=8)),
        ]),
        wr.PanelGrid(runsets=[h4], panels=[
            wr.MediaBrowser(title="Compensation by model, with 95% intervals",
                            media_keys=["charts/compensation_by_model"], num_columns=1,
                            layout=wr.Layout(x=0, y=0, w=W, h=9)),
        ]),
        wr.PanelGrid(runsets=[h5], panels=[
            wr.LinePlot(title="Compensation across training (Pythia-410M)", x="checkpoint_step",
                        y=["compensation", "compensation_lo", "compensation_hi"], log_x=True,
                        layout=wr.Layout(x=0, y=0, w=W // 2, h=9)),
            wr.LinePlot(title="Mean logit difference across training", x="checkpoint_step", y=["ld_mean"],
                        log_x=True, layout=wr.Layout(x=W // 2, y=0, w=W // 2, h=9)),
        ]),

        wr.H1("Part B: does dropout produce self-repair?"),
        wr.P("Result: yes, by a large margin and in the predicted order. Mean pooled self-repair is 0.36 without "
             "dropout, 0.62 with standard dropout, and 0.67 with head dropout; every contrast is positive for all "
             "six seeds, and the difference remains (+0.25 and +0.31) when each dropout model is compared with the "
             "no-dropout checkpoint of the same seed at the same validation loss. Head dropout also reaches a lower "
             "validation loss than standard dropout."),
        wr.P("Eighteen 30M-parameter GPT-2 models trained from scratch on 200M tokens of TinyStories: no dropout, "
             "standard dropout 0.1, or head dropout 0.1, six seeds each, paired by seed (same initialisation, "
             "same data order). Every run measures validation loss and the pooled self-repair fraction, the "
             "share of a removed head's direct effect that the rest of the model restores, at initialisation "
             "and after each eighth of training."),
        wr.PanelGrid(runsets=[sweep], panels=[
            wr.LinePlot(title="Pooled self-repair fraction during training (mean ± stderr by arm)",
                        y=["measure/self_repair_pooled"], groupby="arm", groupby_aggfunc="mean",
                        groupby_rangefunc="stderr", layout=wr.Layout(x=0, y=0, w=W // 2, h=9)),
            wr.LinePlot(title="Validation loss during training (by arm)", y=["measure/val_loss"],
                        groupby="arm", groupby_aggfunc="mean", groupby_rangefunc="stderr",
                        layout=wr.Layout(x=W // 2, y=0, w=W // 2, h=9)),
            wr.LinePlot(title="Training loss (by arm)", y=["train/loss"], groupby="arm",
                        groupby_aggfunc="mean", smoothing_factor=0.6,
                        layout=wr.Layout(x=0, y=9, w=W // 2, h=8)),
            wr.BarPlot(title="Final pooled self-repair fraction (by arm)", metrics=["final/self_repair_pooled"],
                       groupby="arm", groupby_aggfunc="mean", groupby_rangefunc="stderr",
                       layout=wr.Layout(x=W // 2, y=9, w=W // 2, h=8)),
            wr.ParallelCoordinatesPlot(title="Arm, seed, and outcome", columns=[
                wr.ParallelCoordinatesPlotColumn(metric=wr.Config("arm"), display_name="regime"),
                wr.ParallelCoordinatesPlotColumn(metric=wr.Config("seed"), display_name="seed"),
                wr.ParallelCoordinatesPlotColumn(metric=wr.SummaryMetric("final/val_loss")),
                wr.ParallelCoordinatesPlotColumn(metric=wr.SummaryMetric("final/self_repair_pooled")),
            ], layout=wr.Layout(x=0, y=17, w=W, h=9)),
        ]),
        wr.H2("Paired analysis"),
        wr.MarkdownBlock(partb_table),
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", help="existing report to update in place")
    args = ap.parse_args()
    if args.url:
        report = wr.Report.from_url(args.url)
        report.blocks = blocks()
    else:
        report = wr.Report(entity=ENTITY, project=PROJECT, title=TITLE, description=DESCRIPTION,
                           blocks=blocks(), width="fluid")
    report.save()
    print(report.url)


if __name__ == "__main__":
    main()
