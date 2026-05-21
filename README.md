# BM-JEPA / Reduced-Rank Regression Experiments

Controlled experiments for the frozen-teacher BM-JEPA theory. Linear-Gaussian
diagnostics test the JEPA-to-RRR reduction, target-count saturation, target
heterogeneity, the embedding bottleneck, the unified finite-sample risk bound,
predictive isotropy, and gauge factorization; small-scale real-image
experiments test the prediction-aware Gaussianity regularizer.

## Layout

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
python -m experiments.exp_regularizer_mnist_gpu  # scaled MNIST diagnostic
python -m plots.plot_main                        # generate paper figures
pytest                                           # run tests
```

CSVs are written to `results/`, figures to `figures/`.

For the full list of claims under test, run commands, and a per-figure
interpretation guide, see [`RESULTS_SUMMARY.md`](RESULTS_SUMMARY.md).
