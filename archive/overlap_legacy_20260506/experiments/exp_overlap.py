"""Experiment 3: target overlap/redundancy reduces marginal gains."""

from pathlib import Path

from experiments.common import ROOT, parse_args, run_from_config


if __name__ == "__main__":
    args = parse_args(
        ROOT / "configs" / "overlap.yaml",
        ROOT / "results" / "exp_overlap.csv",
    )
    run_from_config("overlap", Path(args.config), Path(args.output))

