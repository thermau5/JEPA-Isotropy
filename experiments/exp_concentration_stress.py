"""Stress tests for cross-covariance concentration diagnostics."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DIM = 32
DELTA = 0.1
SEEDS = range(30)
CALIBRATION_N = 512
CALIBRATION_RHO = 1.0
CALIBRATION_NOISE = 1.0


def covariance(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    return (y.T @ x) / x.shape[0]


def op_norm(matrix: np.ndarray) -> float:
    return float(np.linalg.svd(matrix, compute_uv=False)[0])


def old_cross_covariance_scale(sigma_yx: np.ndarray, n_train: int, delta: float) -> float:
    sigma_top = op_norm(sigma_yx)
    if sigma_top <= 1e-12:
        return 0.0
    effective_rank = float(np.sum(sigma_yx**2) / sigma_top**2)
    return sigma_top * np.sqrt((effective_rank + np.log(1.0 / delta)) / n_train)


def corrected_joint_covariance_scale(
    sigma_yx: np.ndarray,
    sigma_yy: np.ndarray,
    sigma_xx: np.ndarray,
    n_train: int,
    delta: float,
) -> float:
    joint = np.block([[sigma_yy, sigma_yx], [sigma_yx.T, sigma_xx]])
    joint = 0.5 * (joint + joint.T)
    evals = np.linalg.eigvalsh(joint)
    joint_op = float(np.max(evals))
    effective_rank = float(np.trace(joint) / max(joint_op, 1e-12))
    window = (effective_rank + np.log(1.0 / delta)) / n_train
    return joint_op * (np.sqrt(window) + window)


def population_moments(rho: float, noise: float, shuffled: bool) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    sigma_xx = np.eye(DIM)
    sigma_yy = rho**2 * np.eye(DIM) + noise**2 * np.eye(DIM)
    sigma_yx = np.zeros((DIM, DIM)) if shuffled else rho * np.eye(DIM)
    return sigma_yx, sigma_yy, sigma_xx


def sample_lhs(
    rng: np.random.Generator,
    n_train: int,
    rho: float,
    noise: float,
    shuffled: bool,
) -> tuple[float, float, float]:
    x = rng.normal(size=(n_train, DIM))
    signal_source = rng.normal(size=(n_train, DIM)) if shuffled else x
    y = rho * signal_source + noise * rng.normal(size=(n_train, DIM))
    sigma_yx, sigma_yy, sigma_xx = population_moments(rho, noise, shuffled)
    lhs = op_norm(covariance(x, y) - sigma_yx)
    old_scale = old_cross_covariance_scale(sigma_yx, n_train, DELTA)
    corrected_scale = corrected_joint_covariance_scale(
        sigma_yx,
        sigma_yy,
        sigma_xx,
        n_train,
        DELTA,
    )
    return lhs, old_scale, corrected_scale


def calibration_constants() -> tuple[float, float]:
    old_ratios = []
    corrected_ratios = []
    for seed in SEEDS:
        rng = np.random.default_rng(10_000 + seed)
        lhs, old_scale, corrected_scale = sample_lhs(
            rng,
            CALIBRATION_N,
            CALIBRATION_RHO,
            CALIBRATION_NOISE,
            shuffled=False,
        )
        old_ratios.append(lhs / max(old_scale, 1e-12))
        corrected_ratios.append(lhs / max(corrected_scale, 1e-12))
    index = int(np.ceil((1.0 - DELTA) * len(old_ratios))) - 1
    return float(np.sort(old_ratios)[index]), float(np.sort(corrected_ratios)[index])


def run() -> pd.DataFrame:
    c_old, c_corrected = calibration_constants()
    rows = []
    settings: list[tuple[str, float, int, float, float, bool]] = []
    for n_train in [64, 96, 128, 192, 256, 384, 512, 768, 1024, 1536]:
        settings.append(("shuffle", float(n_train), n_train, 1.0, 1.0, True))
    for noise in [0.25, 0.5, 1.0, 2.0, 4.0, 8.0]:
        settings.append(("additive_noise", noise, CALIBRATION_N, 1.0, noise, False))
    for rho in [0.0, 0.03, 0.1, 0.25, 0.5, 0.75, 1.0]:
        settings.append(("weak_correlation", rho, CALIBRATION_N, rho, 1.0, False))

    for stress, x_value, n_train, rho, noise, shuffled in settings:
        for seed in SEEDS:
            rng = np.random.default_rng(seed)
            lhs, old_scale, corrected_scale = sample_lhs(
                rng,
                n_train,
                rho,
                noise,
                shuffled,
            )
            rows.append(
                {
                    "stress": stress,
                    "x": x_value,
                    "seed": seed,
                    "n_train": n_train,
                    "rho": rho,
                    "noise": noise,
                    "shuffled": int(shuffled),
                    "lhs": lhs,
                    "old_scale": old_scale,
                    "corrected_scale": corrected_scale,
                    "old_rhs": c_old * old_scale,
                    "corrected_rhs": c_corrected * corrected_scale,
                    "calibrated_c_old": c_old,
                    "calibrated_c_corrected": c_corrected,
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "results" / "exp_concentration_stress.csv",
    )
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    run().to_csv(args.output, index=False)


if __name__ == "__main__":
    main()
