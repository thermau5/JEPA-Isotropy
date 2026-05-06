"""Publication figure for the GPU MNIST CNN regularizer experiment."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from experiments.common import ROOT
from plots.plot_main import (
    BLUE, TEAL, GOLD, RED, GRAY, GRID, LIGHT_SHADE,
    configure_matplotlib,
)

RESULTS = ROOT / "results" / "exp_regularizer_mnist_gpu.csv"
FIGURES = ROOT / "figures"

METHOD_ORDER = ["baseline", "encoder_gaussian", "predictive_gaussian", "both"]
METHOD_LABELS = ["No reg.", "Enc. reg.", "Pred. reg.", "Pred.+Enc."]
METHOD_COLORS = [GRAY, TEAL, GOLD, RED]
SCATTER_ALPHA = 0.45
SCATTER_SIZE = 14
BAR_WIDTH = 0.55
CAP_SIZE = 2.5


def _bar_panel(
    ax: plt.Axes,
    means: np.ndarray,
    sems: np.ndarray,
    all_seeds: list[np.ndarray],
    ylabel: str,
    title: str,
    highlight_split: bool = True,
) -> None:
    xs = np.arange(len(METHOD_ORDER))
    for i, (m, s, vals, color) in enumerate(zip(means, sems, all_seeds, METHOD_COLORS)):
        ax.bar(xs[i], m, width=BAR_WIDTH, color=color, alpha=0.80, zorder=3)
        ax.errorbar(xs[i], m, yerr=s, fmt="none", color="black",
                    linewidth=0.9, capsize=CAP_SIZE, capthick=0.9, zorder=4)
        jitter = np.random.default_rng(i).uniform(-0.12, 0.12, size=len(vals))
        ax.scatter(xs[i] + jitter, vals, color=color, s=SCATTER_SIZE,
                   alpha=SCATTER_ALPHA, zorder=5, linewidths=0.0)

    if highlight_split:
        # shade to visually separate {no-reg, enc} from {pred, both}
        ax.axvspan(1.5, 3.6, color=GOLD, alpha=0.055, zorder=0)

    ax.set_xticks(xs)
    ax.set_xticklabels(METHOD_LABELS, fontsize=7.5)
    ax.set_ylabel(ylabel)
    ax.set_title(title, pad=4)
    ax.tick_params(axis="x", length=0)
    ax.set_xlim(-0.55, len(METHOD_ORDER) - 0.45)
    ylo = ax.get_ylim()[0]
    ax.set_ylim(bottom=max(0.0, ylo - 0.005))
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.3f"))
    ax.tick_params(axis="y", length=2.5, width=0.65, labelsize=7.5)
    ax.grid(axis="y", color=GRID, linewidth=0.5, alpha=0.7, zorder=0)


def make_figure(csv_path: Path = RESULTS, output_path: Path = FIGURES / "exp_regularizer_mnist_gpu.pdf") -> None:
    df = pd.read_csv(csv_path)
    configure_matplotlib()

    panels = [
        ("test_mse",                    "MSE",          "(a) Test MSE (all pixels)"),
        ("fg_mse",                      "MSE",          "(b) Foreground MSE (digit pixels)"),
        ("gap",                         "MSE",          "(c) Train–test gap"),
        ("predictive_gaussianity_score","Score",        "(d) Pred. Gaussianity score"),
        ("predictive_effective_rank",   "Eff. rank",    "(e) Pred. effective rank"),
        ("train_seconds",               "Seconds",      "(f) Training time (s)"),
    ]

    fig, axes = plt.subplots(2, 3, figsize=(6.5, 4.0), constrained_layout=True)
    axes_flat = axes.flatten()

    for ax, (col, ylabel, title) in zip(axes_flat, panels):
        means, sems, all_seeds = [], [], []
        for method in METHOD_ORDER:
            vals = df[df["method"] == method][col].values
            means.append(vals.mean())
            sems.append(vals.std(ddof=1) / np.sqrt(len(vals)))
            all_seeds.append(vals)
        _bar_panel(ax, np.array(means), np.array(sems), all_seeds,
                   ylabel=ylabel, title=title, highlight_split=True)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    make_figure()
