# BM-JEPA / Reduced-Rank Regression Experiment Summary

This repository implements the paper-facing experiment suite: controlled
linear-Gaussian diagnostics for the frozen-teacher BM-JEPA theory plus
small-scale real-image regularizer diagnostics for the prediction-aware
Gaussianity objective.

## Claims Under Test

1. Increasing target count `K` increases identifiable predictive structure until
   saturation.
2. Stronger target heterogeneity improves finite-sample subspace recovery.
3. A bottleneck dimension `d` imposes an irreducible approximation floor.
4. At fixed rank and fixed total predictive signal energy, predictive
   isotropy of `H_K = T_K^T T_K` improves finite-sample subspace recovery.

## How To Run

```bash
python -m experiments.exp_k_saturation
python -m experiments.exp_heterogeneity
python -m experiments.exp_bottleneck
python -m experiments.exp_post_saturation
python -m experiments.exp_predictive_isotropy
python -m experiments.exp_gauge_factorization
python -m experiments.exp_regularizer_digits
python -m experiments.exp_regularizer_mnist
python -m experiments.exp_regularizer_mnist_gpu
python -m plots.plot_main
python -m plots.plot_regularizer_digits_samples
```

The per-experiment CSV files are written to `results/`, and the paper figures
are written to `figures/`. To reproduce the synthetic suite, the gauge
diagnostic, the $8\times8$ regularizer diagnostic, and the combined
`results/results.csv`, run `python -m experiments.run_all`. The MNIST MLP and
GPU CNN diagnostics are run separately with the commands listed above.

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
  risk and a fixed-reference-stack representation probe to show why the canonical risk can
  stay nearly flat while the learned subspace improves.
- `exp_bottleneck.pdf`: supports the bottleneck claim if per-target MSE decreases with
  `d`, if model rank follows `min(d, r_star)`, and if the normalized empirical
  excess risk over OLS and plug-in spectral-tail ratio track the population
  spectral-tail ratio in the shared Theorem 3.3 panel.
- `exp_post_saturation.pdf`: post-saturation relative-conditioning diagnostic.
  The target stack is already full rank at `K_star=d`; additional targets are allocated
  to weak predictive directions, making
  `kappa_K^2=lambda_d(H_K)/lambda_1(H_K)` rise over a finite window for
  `H_K=T_K^T T_K` and `T_K=Sigma_YZ Sigma_ZZ^{-1/2}`. The two-row figure keeps
  the eigenvalue, conditioning, effective-dimension, risk-stability bound,
  explicit per-target excess-risk, and finite-sample per-target-risk panels.
  Panels (e) and (f) now include calibrated excess-risk and risk-decomposition
  bounds using `C_hat=1.79` from the proof definition of `epsilon_n` and the
  empirical finite-window `L_hat`.
  The old unwhitened diagnostic is preserved under
  `archive/post_saturation_legacy/`.
- `exp_predictive_isotropy.pdf`: fixed-rank, fixed-trace spectrum ablation for
  the new predictive-isotropy section. It holds `rank(T_K)=d`, `K=d`, and
  `tr(H_K)` fixed while moving only the eigenvalue profile of
  `H_K=T_K^T T_K`, equivalently the intrinsic covariance spectrum of
  `P_K=T_K Z_tilde`. Conditions are plotted against the measured operator
  quantity `kappa_H^2=lambda_d(H_K)/lambda_1(H_K)`, not against vague spectrum
  names. The main 2-by-2 figure now shows predictive energy allocation,
  the weak retained signal, empirical
  perturbation scale, Wedin recovery bound, observed `sinTheta_T`,
  and balanced-reference-stack excess MSE.
- `exp_gauge_factorization.pdf`: appendix diagnostic for Section 3.6.1. It
  fixes one population whitened predictor `T_K=U S V^T`, applies identity,
  random orthogonal, diagonal, and nonlinear Gaussianizing gauges under
  Gaussian and Laplace context laws, and checks that the end-to-end prediction
  is unchanged while encoder covariance/Gaussianity follows the gauge choice.
- `exp_regularizer_digits.pdf`: learned nonlinear regularizer experiment on
  real handwritten digits. The model predicts the right half of an image from
  the left half and compares no regularizer, Encoder Gaussianity,
  prediction-side Gaussianity, and prediction-side plus Encoder auxiliary
  Gaussianity. Pixel MSE is averaged over right-half target pixels normalized
  to `[0,1]`; it is not a percentage. The figure also reports wall-clock train
  time per run.
- `exp_regularizer_digits_samples.pdf`: qualitative held-out digit
  reconstructions for the same task. Rows show held-out samples `4` and `8`;
  columns show context, target, and each method's predicted right half.
- `exp_regularizer_mnist_gpu.pdf`: scaled MNIST 28x28 left-to-right completion
  diagnostic with a GPU-scale CNN encoder and spatial decoder. Prediction-side
  regularization gives the best target-half and foreground MSE, while the
  combined objective gives a similar risk and the smallest train-test gap.

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
  subspace recovery. Per-target MSE is nearly flat because the target stack itself
  becomes richer and less redundant; reference-stack MSE decreases because the learned
  subspace transfers better to a common rich target stack. The loose bound
  diagnostics remain in CSV but are not plotted here; the sharper informative
  recovery-bound visualization is Figure 5. This experiment uses
  `d=r_star=24`,
  so it matches the Section 3.2 predictive-rank setting rather than the
  bottleneck ablation.
- **Bottleneck:** supported. Increasing `d` reduces per-target MSE and also reduces
  the normalized empirical excess risk over OLS, empirical plug-in spectral-tail
  ratio, and population spectral-tail ratio, with all theorem-facing curves
  flattening once `d >= r_star`. The model-rank panel is expected to follow
  `min(d, r_star)` because the target stack has only `r_star` predictive
  directions. The CSV keeps both raw and normalized tail values; the plot clips
  ratios below `1e-4` to a common visible floor so post-saturation points remain
  visible without creating a misleading log-scale gap.
- **Post-saturation relative conditioning:** supported as a finite-window
  diagnostic. The target stack is full rank from `K_star=d` onward, but starts
  imbalanced. Adding targets to the weakest predictive directions raises
  population `kappa_K^2(T_K)` from about `0.02` to about `0.90`, while the
  empirical `kappa_K^2(T_K)` moves from about `0.020` to about `0.749`.
  The ten-seed whitened subspace error falls from about `0.171` to `0.056`,
  per-target MSE falls from about `0.0782` to `0.0699`, and the excess gap to the
  population reference falls from about `7.76e-4` to `3.60e-4`. The
  effective-dimension diagnostic remains bounded over the window
  (`oracle_effdim` about `16.30` to `60.65`; empirical about `16.16` to `55.80`),
  the empirical risk-stability ratio stays below about `7.07e-3` across all
  seeds, and the half-gap diagnostic holds in `100/100` deterministic runs. The
  calibrated concentration diagnostic uses `C_hat=1.79`, covers exactly
  `90/100` normalized perturbation samples by construction, and yields a
  conservative subspace-recovery bound that covers all observed `sinTheta_T`
  values in the plotted window. The same calibrated `C_hat` and empirical
  `L_hat` give the panel (e) excess-risk bound and panel (f) risk-decomposition
  bound.
- **Predictive isotropy:** supported as a fixed-trace second-moment and
  recovery-bound diagnostic. The experiment fixes `r_star=d=K=24` and holds
  `tr(H_K)=22.59` constant across 20 spectrum conditions. The measured
  population `kappa_H^2` values range from `1.0` to `3.30e-3`, with most
  conditions concentrated near the finite-sample transition. As
  `kappa_H^2` decreases, the weakest retained signal `sigma_d(T_K)` falls
  below the empirical perturbation scale, the clipped Wedin bound becomes
  vacuous, and the ten-seed `sinTheta_T` mean increases from about `0.139` to
  `0.420`. The balanced-reference-stack excess MSE rises from about `3.79e-4` to
  `1.91e-3`, while the training-stack per-target MSE remains nearly constant
  (`0.1291` to `0.1294`) because rank and total predictive energy are fixed.
  This separates predictive isotropization from simply adding rank or signal
  energy.
- **Gauge factorization:** supported as an appendix diagnostic for Section
  3.6.1. Across ten seeds, all gauges preserve the same end-to-end prediction
  to numerical precision. Identity and random orthogonal gauges have small
  finite-sample covariance anisotropy under both Gaussian and Laplace contexts
  (`~5.5e-2` to `~5.9e-2`), while the diagonal gauge is intentionally
  anisotropic (`~1.0`). The Laplace identity gauge is covariance-isotropic but
  visibly non-Gaussian (`~4.7e-3` projected Gaussianity score); the nonlinear
  Gaussianizing gauge preserves prediction and reduces this score to the
  Gaussian baseline (`~8e-5`). This validates gauge invariance, covariance
  isotropy, and the nonlinear Gaussianizing-gauge construction in the
  controlled setting.
- **Prediction-aware regularizer:** supported as a low-label real-data
  diagnostic. On handwritten digit half-image prediction with only an 8%
  stratified training split, prediction-side Gaussianity regularization lowers
  test MSE from about `9.23e-2` to `6.00e-2` and the train-test gap from about
  `8.54e-2` to `2.00e-2`; in RMSE units this is roughly `0.304` to `0.245`
  on the `[0,1]` pixel scale. The same runs reduce the predictive Gaussianity
  distance from about `1.14e-1` to `4.33e-2` and raise predictive effective rank
  from about `4.13` to `6.41`. Encoder regularization also helps test MSE
  but does not improve the prediction-side Gaussianity distance. Adding an
  Encoder auxiliary penalty on top of prediction-side regularization gives
  similar test MSE (`6.09e-2`) at higher train time. Mean wall-clock train time
  is about `9.03s` for no regularizer, `12.55s` for encoder-only, `12.23s` for
  prediction-only, and `15.80s` for prediction-plus-encoder. This makes the
  prediction-only condition the better cost-risk tradeoff in the current
  diagnostic and is the expected subsumption-control outcome rather than a
  failure. This is a real learned nonlinear check of the
  proposed regularizer, not a closed-form synthetic identity; it should still be
  framed as a small-scale diagnostic rather than a full image-JEPA result.
- **Scaled MNIST regularizer:** supported as a harder real-image diagnostic.
  The GPU run uses 28x28 left-to-right completion with 10k training images, a
  convolutional encoder, a 256-dimensional predictor representation, and a
  spatial decoder. Over ten seeds, prediction-side regularization improves test
  MSE from about `3.68e-2` to `3.43e-2`, foreground MSE from about `1.29e-1` to
  `1.19e-1`, and the train-test gap by about `24%`. It also reduces the
  prediction-side Gaussianity score from about `3.24e-1` to `1.31e-2` and raises
  predictive effective rank from about `5.86` to `10.03`. The combined
  objective gives similar risk and the smallest gap, but prediction-side
  regularization is the main source of the risk improvement.

## Regularization Implication

The updated theory draft motivates a prediction-aware analogue of SIGReg.
Instead of regularizing only encoder embeddings `AZ`, collect intrinsic
predicted outputs `P_hat_int` over a minibatch and regularize their projected
one-dimensional laws with a Cramer-Wold/Epps-Pulley-style Gaussianity penalty.
A practical schematic objective is:

```text
L = L_pred + lambda_emb L_embedding_iso + lambda_pred L_predictive_iso
```

`L_embedding_iso` remains the task-agnostic non-collapse term. `L_predictive_iso`
acts on the prediction-aware pushforward and is stronger than the
second-moment `H_K` isotropy condition tested in Phase 1. The synthetic figures
motivate this regularizer through the fixed-trace spectral mechanism, and the
digits experiment validates the same idea inside a learned nonlinear predictor.

These results are consistent with the intended Phase 1 theory checks:
multi-target prediction improves identifiable structure when targets are
complementary, bottleneck rank controls the spectral-tail floor, and
post-saturation improvement is governed by conditioning/isotropy of the
already-accessible predictive operator.
