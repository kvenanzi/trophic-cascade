# /// script
# requires-python = ">=3.10"
# dependencies = ["plotly>=5.24"]
# ///
"""Run records and the interactive Part B chart for docs/post/.

    uv run scripts/10_post_runs.py [--export wandb-export/trophic-cascade]

Writes:
  docs/post/figures/runs.json         every W&B run of the project: id, name, group, job type,
                                      state, sweep, tags, created time, config, final summary.
                                      Built from the local W&B export (wandb_export.py); skipped
                                      when the export is not present.
  results/partb/<run>/train.json      each Part B run's training loss (one batch every 50 steps,
                                      dropout active), from the export; committed
  docs/post/figures/partb_runs.html   the eighteen Part B runs, one line each, with a metric
                                      selector. Built from results/partb/, which is committed.
"""

import argparse
import json
import math
from pathlib import Path

import plotly.graph_objects as go

FIG = Path("docs/post/figures")
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
ARMS = {"none": ("no dropout", "#b4b2ab"), "standard": ("standard dropout", "#2a78d6"),
        "drophead": ("DropHead", "#eb6834")}
METRICS = [("self_repair_pooled", "pooled self-repair fraction"),
           ("self_repair_mean", "mean self-repair fraction (per head)")] + [
          (f"self_repair_layer{i}", f"self-repair fraction, layer {i}") for i in range(6)] + [
          ("val_loss", "validation loss"),
          ("train_loss", "training loss (one batch, dropout active)")]
PARTB_SWEEP, TOKENS_PER_STEP = "fhuassaa", 128 * 256
# Summary keys that are W&B bookkeeping or references to files, not results.
DROP_SUMMARY = ("_wandb", "_runtime", "_timestamp", "_step")


def clean(v):
    """Scalars and small containers only; table and media references become their path."""
    if isinstance(v, float):
        return None if math.isnan(v) or math.isinf(v) else round(v, 6)
    if isinstance(v, dict):
        if v.get("_type") in ("table-file", "image-file", "html-file", "plotly-file"):
            return {"file": v.get("path")}
        return {k: clean(x) for k, x in v.items()}
    if isinstance(v, list):
        return [clean(x) for x in v]
    return v


def runs_json(export: Path):
    out = []
    for row in json.loads((export / "runs.json").read_text()):
        r = json.loads((export / "runs" / row["id"] / "run.json").read_text())
        config = {k: (v.get("value") if isinstance(v, dict) and "value" in v else v)
                  for k, v in r["config"].items() if not k.startswith("_")}
        summary = {k: clean(v) for k, v in r["summary"].items() if not k.startswith(DROP_SUMMARY)}
        out.append({k: r.get(k) for k in ("id", "name", "group", "job_type", "state", "sweep",
                                          "tags", "notes", "created_at")}
                   | {"config": clean(config), "summary": summary})
    out.sort(key=lambda r: r["created_at"] or "")
    meta = json.loads((export / "export.json").read_text())
    doc = {"source": f"W&B project {meta['project']}, exported {meta['exported_at']}",
           "n_runs": len(out), "runs": out}
    (FIG / "runs.json").write_text(json.dumps(doc, indent=1))
    print("wrote", FIG / "runs.json", f"({len(out)} runs)")


def train_logs(export: Path):
    """The training-loss series of each Part B run, which only the W&B history holds."""
    for row in json.loads((export / "runs.json").read_text()):
        if row["sweep"] != PARTB_SWEEP:
            continue
        hist = json.loads((export / "runs" / row["id"] / "history.json").read_text())
        rows = [{"step": h["_step"], "tokens": h["_step"] * TOKENS_PER_STEP,
                 "loss": round(h["train/loss"], 5), "lr": h["train/lr"]}
                for h in hist if h.get("train/loss") is not None]
        dest = Path("results/partb") / row["name"] / "train.json"
        assert dest.parent.exists(), dest
        dest.write_text(json.dumps({"run": row["id"], "note": "loss of one training batch, logged "
                                    "every 50 steps, with the run's dropout active",
                                    "rows": rows}, indent=1))
    print("wrote results/partb/*/train.json")


def partb_html():
    runs = []
    for f in sorted(Path("results/partb").glob("*/history.json")):
        d = json.loads(f.read_text())
        tf = f.with_name("train.json")
        train = json.loads(tf.read_text())["rows"] if tf.exists() else []
        runs.append((d["config"]["arm"], d["config"]["seed"], d["history"], train))
    runs.sort(key=lambda r: (list(ARMS).index(r[0]), r[1]))

    fig = go.Figure()
    for arm, seed, hist, train in runs:
        label, colour = ARMS[arm]
        for j, (key, name) in enumerate(METRICS):
            pts = [dict(h, train_loss=h["loss"]) for h in train] if key == "train_loss" else hist
            fig.add_trace(go.Scatter(
                x=[h["tokens"] / 1e6 for h in pts], y=[h[key] for h in pts],
                mode="lines" if key == "train_loss" else "lines+markers", visible=(j == 0),
                name=label, legendgroup=arm, showlegend=(seed == 0),
                line=dict(color=colour, width=1.2 if key == "train_loss" else 1.6),
                marker=dict(size=5), opacity=0.85,
                customdata=[[seed, h["step"]] for h in pts],
                hovertemplate=f"{label}, seed %{{customdata[0]}}<br>"
                              "%{x:.0f}M tokens (step %{customdata[1]})<br>"
                              f"{name}: %{{y:.4f}}<extra></extra>"))
    n = len(METRICS)
    buttons = [dict(label=name, method="update",
                    args=[{"visible": [i % n == j for i in range(len(runs) * n)]},
                          {"yaxis.title.text": name} | (
                              # The first steps' loss (10.8 at step 0) would flatten the rest.
                              {"yaxis.range": [1.4, 3.0], "yaxis.autorange": False}
                              if key == "train_loss" else {"yaxis.autorange": True})])
               for j, (key, name) in enumerate(METRICS)]
    fig.update_layout(
        template="simple_white", paper_bgcolor=SURFACE, plot_bgcolor=SURFACE,
        font=dict(family="system-ui, -apple-system, Segoe UI, sans-serif", size=13, color=INK),
        margin=dict(l=70, r=20, t=60, b=55), height=500, hovermode="closest",
        legend=dict(orientation="h", y=1.02, x=1, xanchor="right", yanchor="bottom",
                    title_text="click to hide or show: "),
        updatemenus=[dict(buttons=buttons, direction="down", x=0, xanchor="left", y=1.13,
                          yanchor="bottom", bgcolor=SURFACE, bordercolor=GRID)],
        xaxis=dict(title="training tokens (millions)", gridcolor=GRID, showgrid=True,
                   linecolor=INK2, tickcolor=INK2),
        yaxis=dict(title=METRICS[0][1], gridcolor=GRID, showgrid=True, linecolor=INK2,
                   tickcolor=INK2))
    path = FIG / "partb_runs.html"
    # On a phone-width page the legend moves below the plot, away from the metric menu.
    small = {"legend.y": -0.25, "legend.yanchor": "top", "legend.x": 0, "legend.xanchor": "left",
             "legend.title.text": "", "margin.l": 55, "margin.r": 10, "margin.b": 140}
    wide = {"legend.y": 1.02, "legend.yanchor": "bottom", "legend.x": 1, "legend.xanchor": "right",
            "legend.title.text": "click to hide or show: ", "margin.l": 70, "margin.r": 20,
            "margin.b": 55}
    script = (f"var gd=document.getElementById('{{plot_id}}');var S={json.dumps(small)},"
              f"W={json.dumps(wide)};function fit(){{Plotly.relayout(gd,window.innerWidth<600?S:W);}}"
              "fit();window.addEventListener('resize',fit);")
    fig.write_html(path, include_plotlyjs="cdn", full_html=True, post_script=script,
                   config={"displaylogo": False, "responsive": True,
                           "modeBarButtonsToRemove": ["select2d", "lasso2d"]})
    # The page is shown in an iframe on the blog: no body margin, and the figures' surface colour.
    html = path.read_text().replace(
        "<head>", f"<head><style>html,body{{margin:0;background:{SURFACE}}}</style>", 1)
    path.write_text(html)
    print("wrote", path, f"({len(runs)} runs)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--export", type=Path, default=Path("wandb-export/trophic-cascade"))
    args = ap.parse_args()
    FIG.mkdir(parents=True, exist_ok=True)
    if (args.export / "runs.json").exists():
        runs_json(args.export)
        train_logs(args.export)
    else:
        print(f"no export at {args.export}; runs.json left as it is")
    partb_html()


if __name__ == "__main__":
    main()
