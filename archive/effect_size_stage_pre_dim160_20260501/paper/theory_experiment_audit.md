# Theory-to-Experiment Audit

This audit maps the current repository against the updated theory draft
`jepa_thomas (12).pdf`, inspected on April 30, 2026. The main Section 3.4 object
is the whitened raw predictor

```text
T_K = B_OLS,raw Sigma_ZZ^{1/2}
    = Sigma_YZ^{(K)} Sigma_ZZ^{-1/2},
H_K = T_K^T T_K,
kappa_K^2 = lambda_d(H_K) / lambda_1(H_K).
```

Therefore the post-saturation experiment must be audited against `T_K`, not
against the older unwhitened cross-covariance or target-bank Gram alone.
The latest draft also adds Section 3.5, which interprets predictive isotropy as
operator-level Gaussianity: if
`Z_tilde = Sigma_ZZ^{-1/2} Z` is Gaussian, then the covariance spectrum of
`P_K = T_K Z_tilde` on its rank-`d` range is exactly the nonzero spectrum of
`H_K`.

## Findings

1. **The canonical post-saturation experiment is now aligned with the new
   Section 3.4 object.** The result file `results/exp_post_saturation.csv` is
   generated from `configs/post_saturation.yaml` with
   `subspace_operator: whitened_raw`. In `experiments/common.py`, this computes
   `T_hat = Sigmahat_YZ Sigmahat_ZZ^{-1/2}` and
   `T_pop = Sigma_YZ Sigma_ZZ^{-1/2}`, then computes the theorem-facing
   subspace error from their top-`d` right singular subspaces.

2. **The paper-facing Figure 5 path can remain stable.** The canonical figure
   file `figures/exp_post_saturation.pdf` now represents the whitened
   `T_K` diagnostic. The old unwhitened artifacts are preserved under
   `archive/post_saturation_legacy/`.

3. **The canonical result is stronger than the old unwhitened result for the
   half-gap diagnostic.** For the current `exp_post_saturation`, the empirical
   half-gap analogue holds in `100/100` runs. The archived unwhitened legacy
   run held in `97/100` runs, with marginal failures at `K=12`.

4. **The concentration constant can be calibrated empirically.** This is the
   same `C` appearing in the proof definition
   `epsilon_n = C ||T_K||_op sqrt((effdim(T_K)+log(1/delta))/n)`. The auxiliary
   figure `figures/exp_post_saturation_recovery_bound.pdf` fits
   `C_hat=1.49` as the 90% order-statistic constant for
   `eta_hat_K / sqrt((effdim(T_K)+log(1/delta))/n)` with `delta=0.1`. This
   covers exactly `90/100` normalized perturbation samples by construction, and
   the induced Wedin-style subspace bound covers all observed `sinTheta_T`
   values. This is a finite-window diagnostic, not an estimate of a universal
   distribution-free constant.

5. **The operator perturbation now has a theory-facing CSV name.** The
   canonical CSV includes `operator_error_op = ||T_hat-T||_op`. The older
   `cross_cov_error_op` column is retained as a backward-compatible alias for
   existing plotting/tests.

6. **The risk panels are correctly per-target.** `test_mse`,
   `oracle_test_mse`, and `per_target_excess_mse` are means over all target
   coordinates, so they match the normalized risk definition `R_K` in
   `eq:per_target_risk`. This matters for both `K`-saturation and
   post-saturation.

7. **Section 3.5 now has a direct fixed-trace validation.** The new
   `predictive_isotropy` experiment fixes `r_star=d=K=16` and
   `tr(H_K)` while sweeping only the eigenvalue profile of `H_K`. This tests the
   new claim that, once rank and signal energy are controlled, a flatter
   predictive spectrum gives a more isotropic Gaussian predictive signal and
   better finite-sample recovery.

8. **Embedding isotropy is now separated from predictive isotropy.** The new
   `embedding_vs_predictive_isotropy` experiment varies a synthetic embedding
   covariance spectrum independently from the predictive spectrum of `H_K`.
   This constructs explicit cases where embedding covariance is isotropic but
   the predictive operator is badly conditioned, and vice versa.

## New Object Mapping

The new Section 3.4 defines `V_K` and `Vhat_K` as top-`d` right singular
subspaces of `T_K` and `That_K`. In the post-saturation synthetic setup:

```text
context_dim D_x = 32
target_dim      = 1
r_star          = 12
d               = 12
K_star          = 12
T_K shape       = K x 32
V_K ambient     = R^{32}
kept rank       = d = 12
```

This is the nontrivial version of the subspace diagnostic. If one instead used
`Sigma_YX in R^{Kd x d}` and kept top `d` right singular vectors, the right
subspace would be all of `R^d` once rank is `d`, so `sinTheta` would be
trivial. The whitened experiment avoids that mismatch by measuring subspace
recovery in the raw/context coordinate space.

Code path:

```text
configs/post_saturation.yaml
  subspace_operator: whitened_raw

experiments/common.py
  sigma_yz_hat = covariance(z_train, y_train)
  sigma_zz_hat = covariance(z_train, z_train)
  T_hat = sigma_yz_hat @ inv_sqrt_psd(sigma_zz_hat)
  T_pop = population_cross_cov @ inv_sqrt_psd(population_zz_cov)
  theorem_subspace_error =
      ||sinTheta(right_subspace(T_pop,d), right_subspace(T_hat,d))||_op
```

The population context covariance is not the identity:

```text
Sigma_ZZ = C C^T + sigma_z^2 I,
sigma_z = 0.25.
```

Since `C` has orthonormal columns, the population eigenvalues are `1.0625` on
the 12-dimensional signal span and `0.0625` on the orthogonal complement. The
population condition number is `17.0`. In the whitened run, the empirical
condition number of `Sigmahat_ZZ` stays around `20.6`, so the inverse square root
is well-conditioned at `n_train=5000`.

## Figure 5 Audit Against Section 3.4

The table below describes the correct theory-facing interpretation of the
canonical `figures/exp_post_saturation.pdf`.

| Panel | Quantity | Theory piece | Audit |
| --- | --- | --- | --- |
| (a) | `lambda_1(H_K)` and `lambda_d(H_K)` for `H_K=T_K^T T_K` | Equation (3.12), Assumption 3.1 | Correctly shows the top and weakest retained eigenvalues of the object used in the repaired post-saturation theory. |
| (b) | `kappa_K^2(T_K)=lambda_d(H_K)/lambda_1(H_K)` | Equation (3.12), Assumption 3.1 | Direct validation of the finite-window relative-conditioning premise. |
| (c) | `effdim(T_K)` | Assumption 3.1 and Proposition 3.2 | Checks the bounded effective-dimension term appearing in the numerator of the recovery bound. |
| (d) | per-target excess risk vs. empirical `L_hat ||sinTheta_T||_op` | Assumption 3.2 plus the subspace term controlled by Proposition 3.2 / Corollary 3.3.1 | Correct finite-window diagnostic for the subspace-Lipschitz bridge. `L_hat` is the max over all plotted `K` and seeds of `[excess risk]_+ / ||sinTheta_T||_op`; it is not a proof of a global constant. |
| (e) | per-target excess MSE and excess-risk bound | Corollary 3.3.2, label `cor:post_saturation_excess_risk_bound` | Plots the empirical left-hand-side quantity `R_K(Vhat_K)-R_K^*` against the calibrated excess-risk bound using `C_hat=1.49` from `eq:post_saturation_epsilon` and the empirical finite-window `L_hat`. |
| (f) | finite-sample per-target MSE and risk bound | Corollary 3.3.3, label `cor:risk_decomposition` | Plots the left-hand side `R_K(Vhat_K)` against the calibrated risk-decomposition bound. In this post-saturation configuration `d=r_star(K)`, so the spectral-tail term is zero up to numerical precision and the population OLS risk estimate supplies the architectural-floor term. |

## Whitened Post-Saturation Numerics

Configuration:

```text
n_train = 5000
n_test  = 8192
D_x     = 32
r_star  = d = 12
K       = [12, 16, 20, 24, 32, 40, 48, 64, 80, 96]
seeds   = 0,...,9
sigma_z = sigma_y = 0.25
```

The target bank is already full rank at `K_star=d=12`, but it starts
imbalanced. Additional target rows are allocated to the currently weakest
predictive direction. Thus rank is saturated throughout, while relative
conditioning improves over a finite window.

| K | population `kappa_K^2(T_K)` | finite-sample `kappa_K^2(T_K)` | `||sinTheta_T||_op` mean | `effdim(T_K)` population | `effdim(T_K)` finite sample | per-target excess MSE | per-target MSE |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 12 | 0.0200 | 0.0200 | 0.1310 | 3.2946 | 3.3024 | 5.366e-4 | 0.07904 |
| 16 | 0.0830 | 0.0841 | 0.0773 | 3.6946 | 3.7194 | 4.269e-4 | 0.07639 |
| 96 | 0.9103 | 0.8089 | 0.0434 | 11.4653 | 10.8570 | 2.297e-4 | 0.06982 |

This is qualitatively the behavior Section 3.4 predicts: `kappa_K^2(T_K)`
rises after rank saturation, `sinTheta_T` falls, per-target excess MSE falls,
and total per-target MSE also falls.

## Half-Gap Check

The half-gap condition in the new draft is Equation (3.15). The empirical
analogue for the whitened object is

```text
eta_hat_K := ||T_hat - T||_op / ||T||_op <= kappa_K / 2.
```

The condition is non-vacuous and seed-wise valid across the whole plotted
window:

| K | mean `eta_hat_K` | max `eta_hat_K` | `kappa_K/2` | valid seeds |
| ---: | ---: | ---: | ---: | ---: |
| 12 | 0.0469 | 0.0543 | 0.0707 | 10/10 |
| 16 | 0.0489 | 0.0545 | 0.1440 | 10/10 |
| 96 | 0.0713 | 0.0808 | 0.4771 | 10/10 |

Across all plotted settings, the whitened run satisfies the half-gap diagnostic
in `100/100` deterministic runs. This is exactly the empirical fact needed to
make Corollary 3.3.1's simplified finite-window rate applicable rather than
vacuous.

## Calibrated C Diagnostic

The theory proof introduces

```text
epsilon_n = C ||T_K||_op sqrt((effdim(T_K)+log(1/delta))/n).
```

After normalizing by `||T_K||_op`, the empirical version is exactly the
normalized perturbation diagnostic. For `delta=0.1`, define

```text
a_K = sqrt((effdim(T_K)+log(1/delta))/n),
eta_hat_K = ||T_hat_K-T_K||_op / ||T_K||_op,
C_hat_0.9 = Quantile_0.9(eta_hat_K / a_K).
```

The current canonical run gives `C_hat_0.9 = 1.49`. By construction this
calibrated concentration curve covers `90/100` normalized perturbation samples.
Substituting the same constant into

```text
C_hat a_K / (kappa_K - C_hat a_K)
```

gives a conservative Wedin-style recovery bound. Representative mean values:

| K | mean `sinTheta_T` | calibrated subspace bound |
| ---: | ---: | ---: |
| 12 | 0.1310 | 0.5433 |
| 16 | 0.0773 | 0.2179 |
| 96 | 0.0434 | 0.0891 |

The subspace bound covers all observed `sinTheta_T` samples in this window. The
important caveat is that this calibrated `C_hat` is analogous to the empirical
`L_hat` in panel (d): it validates scale and non-vacuity on this finite
experiment window, but it is not a proof of a universal concentration constant.

Using the half-gap simplified rate with the same calibrated constants gives the
panel (e) excess-risk bound and panel (f) risk-decomposition bound:

| K | excess risk | calibrated excess-risk bound | finite-sample risk | calibrated risk bound |
| ---: | ---: | ---: | ---: | ---: |
| 12 | 5.366e-4 | 4.879e-3 | 7.904e-2 | 8.338e-2 |
| 16 | 4.269e-4 | 2.480e-3 | 7.639e-2 | 7.844e-2 |
| 96 | 2.297e-4 | 1.134e-3 | 6.982e-2 | 7.072e-2 |

## Old vs. New Post-Saturation Runs

The old unwhitened run is archived in `archive/post_saturation_legacy/`. It
remains useful as a fallback/control, but it is no longer the primary validation
of the revised Section 3.4.

| Diagnostic | Unwhitened `Sigma_YZ` run | Whitened `T_K` run |
| --- | ---: | ---: |
| `sinTheta` at K=12 | 0.0388 | 0.1310 |
| `sinTheta` at K=96 | 0.0274 | 0.0434 |
| decay ratio K=96/K=12 | 0.705 | 0.331 |
| half-gap valid runs | 97/100 | 100/100 |
| max empirical risk-stability ratio | 1.626e-2 | 6.943e-3 |

The whitened subspace error starts larger because whitening exposes
perturbations in the full raw/context coordinate metric, but it decays much
more clearly as relative conditioning improves. This is good for the revised
theory: the curve is nontrivial, theory-facing, and still decreases over the
finite window.

## Figure 6 Audit Against Section 3.5

The new `figures/exp_predictive_isotropy.pdf` is the direct validation of the
predictive-isotropy subsection. The experiment keeps rank and total energy
fixed:

```text
D_x      = 32
r_star   = d = 16
K        = 16
tr(H_K)  = 15.0588 for every spectrum condition
sigma_z  = sigma_y = 0.25
```

The target bank is built so that

```text
A^T A = Q diag(lambda_1,...,lambda_d) Q^T,
lambda_i proportional to rho^{i-1},
sum_i lambda_i fixed.
```

Since `C^T C=I` and `sigma_z` is fixed, the nonzero eigenvalues of
`H_K=T_K^T T_K` are the same spectrum up to the common context-noise scale.
Thus the sweep isolates predictive spectral balance rather than rank growth or
total target energy.

| Panel | Quantity | Theory piece | Audit |
| --- | --- | --- | --- |
| (a) | eigenvalues of `H_K` for each decay profile | Section 3.5 predictive-signal spectrum proposition | Shows that the only intervention is spectral shape; all spectra have the same trace. |
| (b) | `kappa_K^2(T_K)=lambda_d(H_K)/lambda_1(H_K)` | Section 3.5 isotropy equivalence and Corollary 3.3.4 | Directly measures spectral balance; flat spectrum reaches the ceiling `1`. |
| (c) | entropy gap `(1/d) sum log lambda_i - log(mean lambda_i)` | Corollary 3.3.4 fixed-trace entropy statement | Zero for flat spectrum and more negative for anisotropic predictive signals. |
| (d) | `||sinTheta_T||_op` against entropy gap | Wedin recovery mechanism used by Section 3.4 plus the fixed-trace Section 3.5 corollary | Recovery gets worse as predictive isotropy decreases, even though rank and trace are fixed. |
| (e) | common flat-bank excess MSE | Risk-stability bridge applied as a representation diagnostic | Shows the recovered subspace degrades on a common evaluation bank when predictive energy is anisotropic. |
| (f) | training-bank per-target MSE | Average per-target risk normalization `eq:per_target_risk` | Stays nearly flat, as intended, because the sweep fixes total target energy; this prevents mistaking signal-strength changes for isotropy effects. |

Representative ten-seed readout:

| rho | `kappa_K^2(T_K)` | entropy gap | `sinTheta_T` mean | common-bank excess MSE | training-bank MSE |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1.00 | 1.0000 | 0.000 | 0.136 | 2.96e-4 | 0.1291 |
| 0.85 | 8.74e-2 | -0.266 | 0.159 | 3.74e-4 | 0.1292 |
| 0.65 | 1.56e-3 | -1.507 | 0.497 | 2.79e-3 | 0.1293 |
| 0.45 | 6.27e-6 | -3.814 | 0.988 | 9.14e-2 | 0.1293 |

The half-gap diagnostic is valid for the flat and mild settings at the current
sample size and intentionally fails for the medium/strong anisotropic settings.
That is acceptable for this experiment: the point is to show the continuum from
well-conditioned isotropic recovery to nearly unrecoverable weak directions at
fixed trace. The post-saturation experiment remains the clean finite-window
bound-validation figure; predictive isotropy is the stronger mechanism
diagnostic.

## Embedding-Isotropy Counterexample Diagnostic

The exploratory figure `figures/exp_embedding_vs_predictive_isotropy.pdf`
checks whether embedding isotropy alone explains the finite-sample behavior.
The construction keeps the same linear-Gaussian data generator and predictive
target banks, but assigns an independent embedding covariance spectrum with
fixed trace. The grid is

```text
embedding decay  rho_emb  in {1.00, 0.65, 0.45}
predictive decay rho_pred in {1.00, 0.85, 0.65, 0.45}
seeds 0,...,9
```

This creates four important regimes:

| Regime | Embedding covariance | Predictive operator | Expected risk |
| --- | --- | --- | --- |
| flat/flat | isotropic | isotropic | low |
| flat/anisotropic | isotropic | badly conditioned | high |
| anisotropic/flat | anisotropic | isotropic | low |
| anisotropic/anisotropic | anisotropic | badly conditioned | high |

Observed readout:

```text
mean common-bank excess MSE by embedding decay:
rho_emb = 1.00 -> 0.02371
rho_emb = 0.65 -> 0.02371
rho_emb = 0.45 -> 0.02371

mean common-bank excess MSE by predictive decay:
rho_pred = 1.00 -> 2.96e-4
rho_pred = 0.85 -> 3.74e-4
rho_pred = 0.65 -> 2.79e-3
rho_pred = 0.45 -> 9.14e-2
```

The Spearman correlation between embedding entropy gap and common-bank excess
MSE is `0.00`, while the correlation between predictive entropy gap and the same
risk is about `-0.91`. This validates the conceptual distinction in Section
3.5: embedding isotropy can be a useful proxy in learned systems, but the
operator appearing in the recovery theory is the predictive operator `H_K`.

## Coverage Summary

| Theory item | Current validation | Status |
| --- | --- | --- |
| Theorem 3.1 and Corollary 3.1.1 | `models/rrr.py` implements closed-form RRR through covariance whitening and rank truncation; tests cover rank constraints. | Covered |
| Lemma 3.1 | CSV stores `rrr_effective_rank`, `rank_equality_target`, and `rank_equality_gap`. | Covered |
| Definition 3.1 / Theorem 3.2 | `exp_k_saturation` sweeps `K`, showing per-target MSE and effective rank saturation. | Covered |
| Definition 3.2 / Proposition 3.1 | `exp_heterogeneity` uses measured empirical `lambda_het` as the x-axis and shows finite-sample rank/subspace improvement. | Covered qualitatively |
| Remark 3.1 | `exp_overlap` separately varies redundancy and shows degraded rank, MSE, and heterogeneity. | Covered |
| Theorem 3.3 | `exp_bottleneck` uses `population_spectrum = svd(B_OLS,raw Sigma_ZZ^{1/2})`, so the plotted spectral-tail ratio is already based on the correct `T` object. | Covered |
| Assumption 3.1 | `exp_post_saturation` fixes `r_star(K)=d=12`, has `rank(T_K)=d`, increases `kappa_K^2(T_K)`, and plots bounded `effdim(T_K)`. | Covered |
| Proposition 3.2 | `theorem_subspace_error` in the whitened CSV is computed from top-`d` right singular subspaces of `T_K` and `T_hat_K`. | Covered |
| Corollary 3.3.1 | The whitened half-gap diagnostic holds in `100/100` runs, and `sinTheta_T` decreases as `kappa_K^2(T_K)` rises. | Covered |
| Assumption 3.2 | Panel (d) gives a finite-window diagnostic via one empirical constant `L_hat`. | Empirically diagnosed, not proven globally |
| Corollary 3.3.2 | Panel (e) plots the normalized per-target excess-risk left-hand side and the calibrated excess-risk bound. | Covered |
| Corollary 3.3.3 | Panel (f) plots the finite-sample per-target risk left-hand side and the calibrated risk-decomposition bound; Figure 4 diagnoses the spectral-tail floor term in the bottleneck setting. | Covered as a decomposition readout |
| Section 3.5 predictive isotropy | `exp_predictive_isotropy` fixes rank and trace, sweeps the spectrum of `H_K`, and plots entropy, `kappa_K^2(T_K)`, `sinTheta_T`, common-bank excess MSE, and training-bank per-target MSE. | Covered |
| Embedding-vs-predictive isotropy distinction | `exp_embedding_vs_predictive_isotropy` varies embedding covariance isotropy independently from predictive isotropy and shows risk follows the predictive spectrum. | Covered as an exploratory diagnostic |

## Canonicalization Status

The repo now uses the whitened result as the only root-level post-saturation
experiment:

```text
configs/post_saturation.yaml      -> whitened_raw config
experiments/exp_post_saturation.py -> canonical runner
results/exp_post_saturation.csv    -> whitened T_K result
figures/exp_post_saturation.pdf    -> whitened T_K figure
```

The old unwhitened files are preserved as legacy artifacts:

```text
archive/post_saturation_legacy/post_saturation_legacy.yaml
archive/post_saturation_legacy/exp_post_saturation_legacy.py
archive/post_saturation_legacy/exp_post_saturation_legacy.csv
archive/post_saturation_legacy/exp_post_saturation_legacy.pdf
```

The paper-facing text has also been updated to refer to
`H_K=T_K^T T_K`, `kappa_K^2(T_K)`, `effdim(T_K)`, and
`||T_hat_K-T_K||_op / ||T_K||_op` for Figure 5.

## Bottom Line

The new experiment result can save and sharpen the post-saturation validation,
and it is now the canonical post-saturation result in the repo. The archived
legacy run is useful only as a control; the paper-facing result should be read
through the whitened `T_K` object from Section 3.4.
