# Legacy Post-Saturation Artifacts

This folder preserves the pre-whitening post-saturation experiment that used the
unwhitened stacked cross-covariance diagnostic. It is kept only as a historical
fallback/control.

The canonical repo-level post-saturation experiment now uses the repaired
theory object

```text
T_K = Sigma_YZ^{(K)} Sigma_ZZ^{-1/2},
H_K = T_K^T T_K.
```

Canonical files:

```text
configs/post_saturation.yaml
experiments/exp_post_saturation.py
results/exp_post_saturation.csv
figures/exp_post_saturation.pdf
```
