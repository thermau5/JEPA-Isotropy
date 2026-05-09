# Theory/Experiment Audit

Updated May 7, 2026 after the uploaded `501.pdf` draft. This
note audits the current repo results against the numbering and statements in that draft. The canonical
post-saturation and predictive-isotropy object is the whitened raw predictor

```text
T_K = Sigma_YZ^(K) Sigma_ZZ^(-1/2),
H_K = T_K^T T_K,
kappa_K^2 = lambda_d(H_K) / lambda_1(H_K).
```

The archived unwhitened post-saturation run is under
`archive/post_saturation_legacy/`; the root-level post-saturation config,
result, and figure now use `T_K`.

Current paper-readiness status: the synthetic paper-facing figures are
regenerated from ten-seed CSVs, the scaled MNIST regularizer diagnostic now uses
a ten-seed GPU CNN run, all referenced PDF figures exist, terminology has been aligned to
target/reference **stack** language, and the newest regularizer diagnostics are
learned nonlinear real-data experiments rather than closed-form synthetic
operators. The remaining scope caveat is intentional: large-scale masked-image
JEPA training is still future work, not claimed by this experiment section.

## Latest Draft Delta

Compared with the previous audit target, `501.pdf` exposes the following
numbered statements that matter for experiment references:

| Draft item | Current experiment mapping |
| --- | --- |
| Proposition 3.8, heterogeneity controls predictive-subspace identifiability | `exp_heterogeneity` is the direct validation; it uses measured `lambda_het` as the x-axis and reports rank/risk recovery. |
| Lemma A.8, cross-covariance concentration | `figures/exp_concentration_lemmas.pdf` panel (a) plots `||Sigma_hat_YZ-Sigma_YZ||_op` against both the earlier cross-covariance effective-rank RHS and the corrected joint-covariance RHS on the heterogeneity sweep. |
| Lemma A.9, concentration of the whitened raw predictor | `figures/exp_concentration_lemmas.pdf` panel (b) plots `||T_hat_K-T_K||_op` against both the old square-root RHS and the corrected square-root-plus-linear RHS on the post-saturation sweep. Panel (c) repeats the same A.9 comparison on real 8x8 digit halves using the full dataset as a reference operator. |
| Corrected concentration stress tests | `figures/exp_concentration_stress.pdf` deliberately decouples cross-covariance signal from marginal variance through shuffle, additive-noise, and weak-correlation designs. It shows where the old RHS fails and the corrected RHS has the right scale. |
| Proposition 3.12, post-saturation risk decomposition | `exp_post_saturation` is the main validation. |
| Theorem 3.15, unified finite-sample risk decomposition | Synthetic risk panels plus the post-saturation calibrated bounds. |
| Lemma 4.1 and Theorem 4.2, predictive isotropy | `exp_predictive_isotropy` fixes rank and trace and varies the spectrum of `H_K=T_K^T T_K`. |
| Lemma 4.4, Theorem 4.5, Theorem 4.6, and Corollary 4.7 | `exp_gauge_factorization` validates gauge invariance and encoder covariance/Gaussianity consequences. |

The current repo TeX still uses symbolic `\cref` labels where available; the
compiled draft displays the corresponding numeric names above.

## Experiment Text Synchronization Warning

Any compiled experiment section generated before this update is stale relative
to this repository. Older drafts may still contain:

- `target bank` / `fixed-bank` / `common-bank` / `training-bank` wording;
- the older small-dimensional configuration table (`D_x=32`, `r_star=16`,
  predictive isotropy with 4 spectrum points);
- the older six-panel predictive-isotropy description with entropy and
  training-stack-risk controls in the main figure;
- Figure 6 wording that says a flatter spectrum gives larger entropy score and
  lower excess MSE, without the current perturbation/gap panels.

The current repo-facing files use the newer terminology and design:

- target **stack** / reference **stack** language;
- `configs/predictive_isotropy.yaml` has 20 spectrum settings concentrated near
  the perturbative transition;
- `figures/exp_predictive_isotropy.pdf` is a 2-by-2 figure with intrinsic
  covariance spectrum, signal-vs-perturbation, Wedin recovery, and
  balanced-reference-stack excess MSE;
- no seed-level scatter/control figure is generated or referenced.

When updating the paper source, paste from `paper/experiments_section.tex` and
`paper/experiments_appendix.tex`; the compiled `501.pdf` should be treated as a
numbering/reference target, not as editable source.

## Current Configurations

| Experiment | Config | Key dimensions |
| --- | --- | --- |
| K saturation | `configs/k_saturation.yaml` | `D_x=160`, `r_star=d=64`, `n_train=1024`, `K=1..256` |
| Heterogeneity | `configs/heterogeneity.yaml` | `D_x=64`, `r_star=d=24`, `K=48`, `n_train=32768` |
| Bottleneck | `configs/bottleneck.yaml` | `D_x=64`, `r_star=24`, `K=48`, `d` swept |
| Post-saturation | `configs/post_saturation.yaml` | `D_x=160`, `r_star=d=64`, `K=64..512`, `n_train=16384`, `subspace_operator=whitened_raw` |
| Predictive isotropy | `configs/predictive_isotropy.yaml` | `D_x=64`, `r_star=d=K=24`, fixed `tr(H_K)` |
| Gauge factorization | `configs/gauge_factorization.yaml` | `D_x=64`, `r_star=d=K=24`, identity/orthogonal/diagonal gauges |
| Regularizer digits | `configs/regularizer_digits.yaml` | nonlinear half-digit prediction, 10 seeds, encoder/predictive Gaussianity penalties |
| Regularizer MNIST MLP | `configs/regularizer_mnist.yaml` | 28x28 half-image prediction, 10 seeds, low-label MLP diagnostic |
| Regularizer MNIST CNN | `configs/regularizer_mnist_gpu.yaml` | 28x28 half-image prediction, 10 seeds, GPU CNN encoder and spatial decoder |

## Figure 1 Audit: Post-Saturation

`figures/exp_post_saturation.pdf` is the main post-saturation diagnostic in the
updated draft.

| Panel | Quantity | Theory role |
| --- | --- | --- |
| (a) | `lambda_1(H_K)` and `lambda_d(H_K)` | Checks the retained spectrum of `H_K=T_K^T T_K`. |
| (b) | `kappa_K^2=lambda_d(H_K)/lambda_1(H_K)` | Directly checks the finite-window relative-conditioning premise. |
| (c) | `effdim(T_K)` | Checks the bounded effective-dimension term in the concentration bound. |
| (d) | per-target excess risk vs. `L_hat ||sinTheta_T||_op` | Empirical finite-window diagnostic for the subspace-Lipschitz bridge. |
| (e) | per-target excess risk vs. calibrated excess-risk bound | Checks the finite-sample excess term inside `eq:risk_decomposition`. |
| (f) | finite-sample per-target risk vs. calibrated risk-decomposition bound | Checks Proposition 3.12 and the risk-decomposition equation; in this config the spectral-tail term is zero up to numerical precision because `d=r_star(K)`. |

Current ten-seed readout:

| K | population `kappa_K^2` | finite `kappa_K^2` | `sinTheta_T` mean | `effdim(T_K)` population | `effdim(T_K)` finite | excess MSE | per-target MSE |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 64 | 0.0200 | 0.0195 | 0.1705 | 16.30 | 16.16 | 7.756e-4 | 7.823e-2 |
| 96 | 0.1226 | 0.1160 | 0.0921 | 19.50 | 19.31 | 6.102e-4 | 7.504e-2 |
| 160 | 0.2652 | 0.2504 | 0.0734 | 25.90 | 25.65 | 4.898e-4 | 7.246e-2 |
| 256 | 0.4612 | 0.4235 | 0.0647 | 35.50 | 35.05 | 4.124e-4 | 7.107e-2 |
| 512 | 0.9019 | 0.7488 | 0.0564 | 60.65 | 55.80 | 3.601e-4 | 6.985e-2 |

This validates the repaired qualitative mechanism: after rank has saturated,
extra targets help only when they improve relative conditioning of the already
accessible predictive directions. Here `r_star(K)=d=64` throughout, while
`kappa_K^2` rises and both `sinTheta_T` and excess risk decrease.

## Half-Gap Check

The empirical half-gap analogue is

```text
eta_hat_K = ||T_hat_K - T_K||_op / ||T_K||_op <= kappa_K / 2.
```

For the current run it holds in `100/100` deterministic runs. The weakest
endpoint, `K=64`, is deliberately closest to the boundary and remains just
inside the half-gap window.

| K | mean `eta_hat_K` | max `eta_hat_K` | `kappa_K/2` | valid seeds |
| --- | ---: | ---: | ---: | ---: |
| 64 | 0.0613 | 0.0656 | 0.0707 | 10/10 |
| 80 | 0.0619 | 0.0663 | 0.1162 | 10/10 |
| 96 | 0.0626 | 0.0688 | 0.1751 | 10/10 |
| 160 | 0.0675 | 0.0711 | 0.2575 | 10/10 |
| 256 | 0.0744 | 0.0780 | 0.3395 | 10/10 |
| 512 | 0.0929 | 0.0947 | 0.4748 | 10/10 |

The paper text should therefore describe the simplified rate as non-vacuous on
the perturbative portion of the plotted window, not uniformly over every
displayed endpoint.

## Calibrated Constants

The concentration constant is calibrated from the proof definition

```text
epsilon_n = C ||T_K||_op sqrt((effdim(T_K)+log(1/delta))/n).
```

With `delta=0.1`, the current plotted run uses

```text
C_hat_0.9 = 1.78662
L_hat     = 0.0070651
```

`C_hat_0.9` is the 90% order-statistic calibration of
`eta_hat_K / sqrt((effdim(T_K)+log(1/delta))/n)`, so it covers exactly 90 of
the 100 plotted perturbation samples by construction. `L_hat` is the finite
window maximum of `[excess risk]_+ / ||sinTheta_T||_op`; it diagnoses the
subspace-Lipschitz assumption on this experimental window and should not be
phrased as a proof of a global constant.

## Coverage Summary

| Theory item | Current validation | Status |
| --- | --- | --- |
| RRR/rank truncation | `models/rrr.py`; unit tests cover rank constraints and deterministic behavior. | Covered |
| Predictive-rank growth | `exp_k_saturation` shows rank growth and per-target MSE decrease until saturation at `r_star=d=64`. | Covered |
| Proposition 3.8, heterogeneity identifiability | `exp_heterogeneity` uses measured `lambda_het` as the x-axis and reports per-target plus reference-stack risk and recovered rank. Larger `lambda_het` improves finite-sample identifiability in the plotted sweep. | Covered qualitatively |
| Lemma A.8, cross-covariance concentration | `exp_concentration_lemmas.pdf` panel (a) plots the empirical cross-covariance perturbation against the old RHS (`C_hat_0.9=2.87`) and the corrected joint-covariance RHS (`C_hat_0.9=0.07`) on the heterogeneity sweep. | Direct LHS/RHS diagnostic |
| Lemma A.9, whitened raw predictor concentration | `exp_concentration_lemmas.pdf` panel (b) plots `||T_hat_K-T_K||_op` against the old RHS (`C_hat_0.9=1.79`) and the corrected RHS with the extra linear term (`C_hat_0.9=1.73`) on the post-saturation sweep. Panel (c) is a real 8x8 digit finite-data proxy with `C_hat_0.9=1.17` old and `1.02` corrected. | Direct LHS/RHS diagnostic |
| Corrected concentration stress tests | `exp_concentration_stress.pdf` calibrates constants once on a correlated Gaussian baseline and then tests shuffle, additive-noise, and weak-correlation regimes. The old RHS collapses or stays fixed when marginal sampling noise remains nonzero; the corrected RHS tracks that noise scale. | Validity stress test |
| Bottleneck spectral tail | `exp_bottleneck` compares normalized excess risk with population and plug-in spectral-tail ratios. | Covered |
| Proposition 3.12, post-saturation risk decomposition | `exp_post_saturation` keeps `r_star(K)=d=64`, increases `kappa_K^2`, plots bounded `effdim(T_K)`, and compares empirical risk with calibrated bounds. | Covered |
| Post-saturation recovery | `theorem_subspace_error` is computed from top-`d` right singular subspaces of `T_K` and `T_hat_K`. | Covered |
| Half-gap simplified rate | Valid seed-wise for all plotted `K`. | Covered |
| Risk-stability bridge | Panel (d) uses one empirical finite-window `L_hat`. | Diagnosed, not globally proven |
| Excess-risk and total-risk corollaries | Panels (e) and (f) compare empirical left-hand sides with calibrated bounds. | Covered as finite-window diagnostics |
| Lemma 4.1, predictive-isotropy equivalence | `exp_predictive_isotropy` fixes rank and trace while varying the intrinsic covariance spectrum of `P_K=T_K Z_tilde`, whose nonzero eigenvalues equal those of `H_K`. | Covered at second-moment level |
| Theorem 4.2, fixed-trace minimization | Figure 6 plots `sigma_d(T_K)`, `||T_hat_K-T_K||_op`, the clipped Wedin bound, and observed `sinTheta_T` across a dense fixed-trace `kappa_H^2` sweep. | Covered as a finite-sample diagnostic |
| Lemma 4.4, gauge invariance | `exp_gauge_factorization` constructs multiple gauges of the same population `T_K` and measures end-to-end prediction error. | Covered |
| Theorem 4.5, covariance-isotropy subsumption | The same diagnostic compares encoder covariance anisotropy under identity, orthogonal, and diagonal gauges for Gaussian and Laplace contexts. | Covered |
| Theorem 4.6 / Corollary 4.7, Gaussian gauge | The diagnostic reports projected standard-normal discrepancy for SVD-aligned, orthogonal, and nonlinear Gaussianizing gauges. | Covered in controlled Gaussian/Laplace setting |
| Section 3.6.2 predictive Gaussianity regularizer | `exp_regularizer_digits` trains a nonlinear encoder-predictor on real digit halves with Encoder and prediction-side projected-Gaussianity regularizers. | Covered as small-scale real-data diagnostic |
| Scaled predictive Gaussianity regularizer | `exp_regularizer_mnist_gpu` repeats the left-to-right completion diagnostic with 28x28 MNIST, a convolutional encoder, and a spatial decoder. | Covered as scaled real-image diagnostic |

## Bottom Line

The current experiments validate the revised theory in the right operator
coordinates. Rank saturation starts at `K=64`, and after tuning the sample size
the empirical half-gap guarantee is valid throughout the plotted window.

## Figure 6 Audit: Predictive Isotropy

The updated theory draft changes the isotropy statement from a generic
conditioning diagnostic to a statement about the predictive pushforward
`P_K = T_K Z_tilde` and its intrinsic covariance on the rank-`d` range.
Because the synthetic context is Gaussian after whitening, the nonzero
covariance eigenvalues of `P_K` are exactly the eigenvalues of `H_K=T_K^T T_K`.

| Panel | Quantity | Theory role |
| --- | --- | --- |
| (a) | intrinsic covariance eigenvalues of `P_K` | Direct check of `lem:predictive_isotropy`: predictive isotropy means these eigenvalues are equal. |
| (b) | `sigma_d(T_K)` versus `||T_hat_K-T_K||_op` | The denominator ingredients in the Wedin term used by `thm:predictive_isotropy_opt`. |
| (c) | observed `sinTheta_T` and clipped Wedin bound | Shows that isotropy improves finite-sample subspace recovery by making the weak retained direction larger relative to perturbation. |
| (d) | balanced-reference-stack excess MSE | Representation/risk probe that values all predictive directions equally, so weak-direction recovery matters. |

The experiment uses 20 spectrum conditions rather than four categories, with
population `kappa_H^2` ranging from `1.0` to `3.30e-3`. The sweep is
concentrated near the finite-sample transition: 16 of 20 settings have
`sigma_d(T_K) > ||T_hat_K-T_K||_op` for every seed, and 10 of 20 satisfy the
half-gap condition for every seed. The training-stack risk
remaining flat is expected: the target stack becomes anisotropic at the same time
as `H_K`, so weak directions carry little weight under the canonical
target-stack risk. The balanced-reference-stack probe is therefore the informative risk
diagnostic for this specific fixed-trace isotropy test.

## Section 3.6.1 Audit: Gauge Factorization

`figures/exp_gauge_factorization.pdf` validates the two gauge-factorization
theorems in the controlled setting. The construction fixes
`T_K=U_K S_K V_K^T` and evaluates
`Lambda_G(Z)=G V_K^T Sigma_ZZ^{-1/2} Z`,
`F_G=U_K S_K G^{-1}` for identity, random orthogonal, diagonal, and nonlinear
Gaussianizing gauges under Gaussian and standardized Laplace context laws.

Current ten-seed readout:

| Context | Gauge | relative prediction error | covariance anisotropy | projected Gaussianity score |
| --- | --- | ---: | ---: | ---: |
| Gaussian | identity | 0.00e+00 | 5.48e-02 | 8.4e-05 |
| Gaussian | orthogonal | 5.22e-16 | 5.48e-02 | 8.2e-05 |
| Gaussian | diagonal | 9.49e-17 | 1.00e+00 | 2.74e-02 |
| Laplace | identity | 0.00e+00 | 5.93e-02 | 4.72e-03 |
| Laplace | orthogonal | 5.54e-16 | 5.93e-02 | 4.39e-04 |
| Laplace | Gaussianized | 1.77e-13 | 5.58e-02 | 8.3e-05 |
| Laplace | diagonal | 9.45e-17 | 1.00e+00 | 2.81e-02 |

The prediction error column checks `lem:gauge_invariance`: the factorization
gauge does not change the end-to-end predictor. The covariance column checks
`thm:subsumes_cov_isotropy`: identity and orthogonal gauges are isotropic up to
finite-sample covariance error, whereas the diagonal gauge intentionally breaks
isotropy while preserving prediction. The Laplace rows separate covariance
isotropy from Gaussianity: identity is covariance-isotropic but non-Gaussian,
while the nonlinear Gaussianizing gauge preserves prediction and reduces the
projected standard-normal discrepancy to the Gaussian baseline. This checks the
role of the nonlinear gauge in `thm:subsumes_gaussian_isotropy`.

## Section 3.6.2 Audit: Regularization

The newest draft frames the practical regularizer as a prediction-aware
Gaussianity penalty `R_PI(P_hat_K^int; A)` on the intrinsic predicted output,
using random one-dimensional projections and an Epps-Pulley statistic motivated
by Cramer-Wold. This is stronger than `lem:predictive_isotropy`'s second-moment isotropy:
matching standard-normal projections implies isotropic covariance and Gaussian
shape, while the current experiment only varies the eigenvalues of `H_K`.

Therefore the current experimental claim should be precise:

- Figure 6 validates the second-moment spectral mechanism behind
  `lem:predictive_isotropy` and `thm:predictive_isotropy_opt`.
`figures/exp_regularizer_digits.pdf` now gives a learned low-label validation
of the regularizer on real digit images. It is not a large-scale image JEPA
claim, but it does move beyond closed-form synthetic operators: a nonlinear
encoder-predictor is trained to predict the right half of each digit from the
left half using only an 8% stratified training split.

Current ten-seed readout:

| Method | train MSE | test MSE | train-test gap | predictive Gaussianity | predictive rank |
| --- | ---: | ---: | ---: | ---: | ---: |
| none | 6.89e-03 | 9.23e-02 | 8.54e-02 | 1.14e-01 | 4.13 |
| encoder only | 1.58e-02 | 7.86e-02 | 6.29e-02 | 1.54e-01 | 4.24 |
| prediction only | 4.01e-02 | 6.00e-02 | 2.00e-02 | 4.33e-02 | 6.41 |
| prediction + encoder auxiliary | 3.81e-02 | 6.09e-02 | 2.27e-02 | 4.09e-02 | 6.82 |

This is now a risk-facing result: prediction-side regularization gives the
largest test-MSE and generalization-gap improvement. The
prediction-plus-encoder condition is a subsumption control: it is similar on
test risk, so Encoder isotropy is not providing an additional risk
mechanism once the prediction-side condition is present. The Gaussianity score
is a manipulation check for the proposed penalty, not the main outcome; the
main outcome is the lower test risk.
