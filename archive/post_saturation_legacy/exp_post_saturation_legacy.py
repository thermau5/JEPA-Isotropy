"""Experiment 5: post-saturation relative-conditioning diagnostics."""

from pathlib import Path

from experiments.common import ROOT, parse_args, run_from_config


if __name__ == "__main__":
    args = parse_args(
        ROOT / "archive" / "post_saturation_legacy" / "post_saturation_legacy.yaml",
        ROOT / "archive" / "post_saturation_legacy" / "exp_post_saturation_legacy.csv",
    )
    run_from_config("post_saturation_legacy", Path(args.config), Path(args.output))
