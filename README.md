# On JEPA Isotropy

A finite-sample, empirical-risk-minimization (ERM) theory of Joint-Embedding
Predictive Architectures (JEPA) — and the experiment suite that corroborates it.

## What this work shows

JEPA is a prominent self-supervised paradigm, but its isotropy regularizers
(isotropic-Gaussian embeddings, SIGReg-style penalties) have been heuristic,
targeting the encoder marginal rather than the prediction risk itself. We give
them a rigorous ERM foundation:

- **JEPA is reduced-rank regression.** Casting the embedding bottleneck as a
  rank constraint reformulates multi-target linear JEPA as reduced-rank
  regression, yielding an exact risk decomposition into an *irreducible error*
  and a *finite-sample excess-risk bound*.
- **The irreducible term.** The optimal predictor's rank grows with target
  count and heterogeneity, then saturates at the embedding bottleneck — which
  floors an irreducible spectral tail.
- **The excess-risk bound.** It is governed by the spectral conditioning of the
  whitened end-to-end predictor `T_K`, and is minimized at *predictive
  isotropy*.
- **A principled regularizer.** These conditions prescribe a prediction-side
  isotropic regularizer. Under it, JEPA isotropy *subsumes* the canonical
  encoder-embedding isotropy designs — so the empirical success of existing
  JEPA isotropy heuristics follows as a corollary of empirical risk
  minimization.

The compiled paper is [`main.pdf`](main.pdf).

## This repository

The experiment suite backing every claim: controlled linear-Gaussian
diagnostics — with known population operators, so each assumption,
proposition, and theorem is checked against ground truth — plus real-image
experiments validating the prediction-aware regularizer inside learned
nonlinear networks.

| Path | Contents |
|------|----------|
| `data/` | Linear-Gaussian synthetic generators |
| `models/` | OLS and reduced-rank regression solvers |
| `metrics/` | Rank, spectrum, and subspace-recovery metrics |
| `experiments/` | One `exp_*.py` per claim, plus `run_all.py` |
| `configs/` | Per-experiment YAML configs |
| `plots/` | Figure generation |
| `results/` | Output CSVs |
| `figures/` | Output PDFs |
| `paper/` | LaTeX experiment section and appendix |
| `tests/` | pytest suite |

## Usage

```bash
python -m experiments.run_all                   # synthetic suite + reduction/gauge/digits
python -m experiments.exp_regularizer_mnist_gpu  # scaled MNIST regularizer diagnostic
python -m plots.plot_main                        # generate paper figures
pytest                                           # run tests
```

CSVs are written to `results/`, figures to `figures/`.

For the full list of claims under test, run commands, and a per-figure
interpretation guide, see [`RESULTS_SUMMARY.md`](RESULTS_SUMMARY.md).
