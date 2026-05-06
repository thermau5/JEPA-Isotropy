# BM-JEPA / Reduced-Rank Regression Experiment Summary

This repository implements Phase 1 of the staged experiment plan: controlled
linear-Gaussian experiments for the frozen-teacher BM-JEPA theory. Phase 2
real-data JEPA validation is documented in `paper/experiments_section.tex` as
the next empirical layer rather than run in this initial package.

## Claims Under Test

1. Increasing target count `K` increases identifiable predictive structure until
   saturation.
2. Stronger target heterogeneity improves finite-sample subspace recovery.
3. Target overlap/redundancy reduces the marginal benefit of larger `K`.
4. A bottleneck dimension `d` imposes an irreducible approximation floor.
5. At fixed rank and fixed total predictive signal energy, predictive
   isotropy of `H_K = T_K^T T_K` improves finite-sample subspace recovery.

## How To Run

```bash
python -m experiments.exp_k_saturation
python -m experiments.exp_heterogeneity
python -m experiments.exp_overlap
python -m experiments.exp_bottleneck
python -m experiments.exp_post_saturation
python -m experiments.exp_predictive_isotropy
python -m experiments.exp_embedding_vs_predictive_isotropy
python -m plots.plot_main
```

The per-experiment CSV files are written to `results/`, and the paper figures
are written to `figures/`. To reproduce the complete suite and combined
`results/results.csv`, run `python -m experiments.run_all`.

Plot convention: solid curves are finite-sample estimates averaged over seeds;
dashed gray curves are population values computed from the known synthetic
operators.

## Interpretation Guide

- `exp_k_saturation.pdf`: supports the rank-growth claim if recovered rank
  grows with `K` and average per-target MSE decreases before flattening near the
  bottleneck/effective rank, while the rank-index conditioning proxy improves.
- `exp_heterogeneity.pdf`: supports the heterogeneity claim if larger measured
  empirical heterogeneity `lambda_het` raises effective rank and improves
  finite-sample identifiability. The figure includes both average per-target
  risk and a fixed-bank representation probe to show why the canonical risk can
  stay nearly flat while the learned subspace improves.
- `exp_overlap.pdf`: supports the redundancy claim if higher overlap lowers the
  effective rank, raises average per-target MSE, and degrades conditioning.
- `exp_bottleneck.pdf`: supports the bottleneck claim if per-target MSE decreases with
  `d`, if model rank follows `min(d, r_star)`, and if the normalized empirical
  excess risk over OLS and plug-in spectral-tail ratio track the population
  spectral-tail ratio in the shared Theorem 3.3 panel.
- `exp_post_saturation.pdf`: post-saturation relative-conditioning diagnostic.
  The bank is already full rank at `K_star=d`; additional targets are allocated
  to weak predictive directions, making
  `kappa_K^2=lambda_d(H_K)/lambda_1(H_K)` rise over a finite window for
  `H_K=T_K^T T_K` and `T_K=Sigma_YZ Sigma_ZZ^{-1/2}`. The two-row figure keeps
  the eigenvalue, conditioning, effective-dimension, risk-stability bound,
  explicit per-target excess-risk, and finite-sample per-target-risk panels.
  Panels (e) and (f) now include calibrated excess-risk and risk-decomposition
  bounds using `C_hat=1.49` from the proof definition of `epsilon_n` and the
  empirical finite-window `L_hat`.
  The old unwhitened diagnostic is preserved under
  `archive/post_saturation_legacy/`.
- `exp_post_saturation_recovery_bound.pdf`: calibrated Proposition 3.2
  diagnostic. It fits an empirical 90% version of the concentration constant
  `C` from the proof definition of `epsilon_n`, giving `C_hat=1.49` for the
  normalized perturbation and plotting the induced Wedin-style subspace
  recovery bound against the observed `sinTheta_T` curve.
- `exp_predictive_isotropy.pdf`: fixed-rank, fixed-trace spectrum ablation for
  the new predictive-isotropy section. It holds `rank(T_K)=d`, `K=d`, and
  `tr(H_K)` fixed while moving only the eigenvalue profile of
  `H_K=T_K^T T_K`. Flatter spectra have larger `kappa_K^2`, larger entropy
  score, smaller `sinTheta_T`, and lower common-bank excess MSE.
- `exp_predictive_isotropy_scatter.pdf`: seed-level scatter version of the same
  ablation, showing common-bank excess MSE against entropy gap and
  `kappa_K^2(T_K)`.
- `exp_embedding_vs_predictive_isotropy.pdf`: independent embedding-spectrum
  and predictive-spectrum grid. It constructs cases where embedding covariance
  is isotropic but the predictive operator is badly conditioned, and conversely,
  showing that the common-bank excess MSE follows predictive isotropy more
  directly than embedding isotropy.

## Current Ten-Seed Readout

- **K saturation:** supported on per-target MSE and rank diagnostics. This sweep
  sets `d=r_star` so the curve isolates target-count saturation rather than the
  smaller bottleneck floor, which is tested separately. The model
  learns and is evaluated on the first `K` targets using the average
  per-target normalization from `R_K`. Per-target MSE decreases as `K`
  grows, while recovered effective rank increases and then
  saturates once the latent predictive rank is exhausted.
- **Heterogeneity:** supported as a direct `lambda_het` diagnostic. The
  generator still uses `alpha` to produce different target dictionaries, but the
  paper-facing figure uses measured empirical heterogeneity as the x-axis.
  Larger `lambda_het` recovers more predictive directions and improves
  subspace recovery. Per-target MSE is nearly flat because the target bank itself
  becomes richer and less redundant; fixed-bank MSE decreases because the learned
  subspace transfers better to a common rich target bank. The loose bound
  diagnostics remain in CSV but are not plotted here; the sharper informative
  recovery-bound visualization is Figure 5. This experiment uses
  `d=r_star=16`,
  so it matches the Section 3.2 predictive-rank setting rather than the
  bottleneck ablation.
- **Overlap/redundancy:** supported on effective rank and per-target MSE.
  Increasing overlap concentrates coverage on a small subset of atoms and
  weakens coverage of the remaining atoms, reducing the number of recovered
  predictive directions and raising per-target MSE. This experiment also uses
  `d=r_star=16`; bottleneck effects are isolated in the bottleneck ablation.
- **Bottleneck:** supported. Increasing `d` reduces per-target MSE and also reduces
  the normalized empirical excess risk over OLS, empirical plug-in spectral-tail
  ratio, and population spectral-tail ratio, with all theorem-facing curves
  flattening once `d >= r_star`. The model-rank panel is expected to follow
  `min(d, r_star)` because the target bank has only `r_star` predictive
  directions. The CSV keeps both raw and normalized tail values; the plot clips
  ratios below `1e-4` to a common visible floor so post-saturation points remain
  visible without creating a misleading log-scale gap.
- **Post-saturation relative conditioning:** supported as a finite-window
  diagnostic. The target bank is full rank from `K_star=d` onward, but starts
  imbalanced. Adding targets to the weakest predictive directions raises
  population `kappa_K^2(T_K)` from about `0.02` to about `0.91`, while the
  ten-seed whitened subspace error falls from about `0.131` to `0.043`,
  per-target MSE falls from about `0.079` to `0.070`, and the excess gap to the
  population reference falls from about `5.4e-4` to `2.3e-4`. The
  effective-dimension diagnostic remains bounded over the window
  (`oracle_effdim` about `3.29` to `11.47`; empirical about `3.30` to `10.86`),
  the empirical risk-stability ratio stays below about `6.95e-3` across all
  seeds, and the half-gap diagnostic holds in `100/100` deterministic runs. The
  calibrated concentration diagnostic uses `C_hat=1.49`, covers exactly
  `90/100` normalized perturbation samples by construction, and yields a
  conservative subspace-recovery bound that covers all observed `sinTheta_T`
  values in the plotted window. The same calibrated `C_hat` and empirical
  `L_hat` give the panel (e) excess-risk bound and panel (f) risk-decomposition
  bound.
- **Predictive isotropy:** supported as a fixed-trace operator-level
  diagnostic. The experiment fixes `r_star=d=K=16` and holds
  `tr(H_K)=15.06` constant across spectrum conditions. Moving from flat to
  strong geometric decay changes population `kappa_K^2(T_K)` from `1.0` to
  `6.27e-6` and entropy gap from `0.0` to `-3.814`, while the ten-seed
  `sinTheta_T` mean increases from about `0.136` to `0.988`. The common flat
  evaluation-bank excess MSE rises from about `2.96e-4` to `9.14e-2`.
  Meanwhile, the training-bank per-target MSE remains nearly constant
  (`0.1291` to `0.1293`), as intended, because rank and total predictive
  energy are fixed. This separates predictive isotropization from simply adding
  rank or signal energy.
- **Embedding versus predictive isotropy:** supported as a controlled
  distinction. The experiment varies an embedding covariance spectrum
  independently from the predictive spectrum of `H_K`. Averaging over predictive
  spectra, common-bank excess MSE is identical across embedding decay values
  (`0.02371` mean in each group). Averaging over embedding spectra, the same
  risk changes from `2.96e-4` at flat predictive spectrum to `9.14e-2` at strong
  predictive anisotropy. Spearman correlation is `0.00` for embedding entropy
  gap versus risk and about `-0.91` for predictive entropy gap versus risk.

These results are consistent with the intended Phase 1 theory checks:
multi-target prediction improves identifiable structure when targets are
complementary, redundant targets do not create new rank, and post-saturation
improvement is governed by conditioning/isotropy of the already-accessible
predictive operator.
