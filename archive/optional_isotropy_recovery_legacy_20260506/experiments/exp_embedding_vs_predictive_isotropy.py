"""Experiment 7: embedding isotropy versus predictive isotropy."""

from __future__ import annotations

from pathlib import Path

from experiments.common import ROOT, parse_args, run_from_config


if __name__ == "__main__":
    args = parse_args(
        ROOT / "configs" / "embedding_vs_predictive_isotropy.yaml",
        ROOT / "results" / "exp_embedding_vs_predictive_isotropy.csv",
    )
    run_from_config(
        "embedding_vs_predictive_isotropy",
        Path(args.config),
        Path(args.output),
    )
