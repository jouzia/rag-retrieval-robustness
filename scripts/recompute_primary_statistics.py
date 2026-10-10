#!/usr/bin/env python3
"""Recompute the primary appended-context experiment's 27 paired tests.

This script reads the frozen 240-row CSV, makes no LLM/API calls, verifies its
SHA-256 and experiment structure, then writes the statistical table used for
publication review.

Usage:
    python scripts/recompute_primary_statistics.py path/to/retrieval_noise_results.csv --output results/statistical_analysis_recomputed.csv

Dependencies: pandas, scipy, statsmodels, numpy.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata, wilcoxon
from statsmodels.stats.multitest import multipletests

EXPECTED_SHA256 = "1e666b0b81608dcf3a6995f4c203dd3078a941768a38c627ae801ed0501d653b"
METHODS = ["bm25", "dense", "hybrid"]
NOISE_LEVELS = [1, 2, 4]
METRICS = ["token_f1", "semantic_similarity", "latency_seconds"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def paired_rank_biserial(noisy: np.ndarray, baseline: np.ndarray) -> float:
    """Positive values mean noisy-condition values tend to exceed baseline."""
    differences = noisy - baseline
    differences = differences[differences != 0]
    if differences.size == 0:
        return 0.0
    ranks = rankdata(np.abs(differences), method="average")
    positive = ranks[differences > 0].sum()
    negative = ranks[differences < 0].sum()
    return float((positive - negative) / ranks.sum())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path, help="Frozen 240-row primary CSV")
    parser.add_argument("--output", type=Path, required=True, help="Output CSV path")
    parser.add_argument(
        "--skip-hash-check",
        action="store_true",
        help="Only use for a deliberately changed dataset; not for reproducing the published result",
    )
    args = parser.parse_args()

    actual_hash = sha256(args.csv)
    if not args.skip_hash_check and actual_hash != EXPECTED_SHA256:
        raise SystemExit(
            f"SHA-256 mismatch: expected {EXPECTED_SHA256}, got {actual_hash}. "
            "Refusing to analyze a dataset other than the frozen primary CSV."
        )

    data = pd.read_csv(args.csv)
    required = {
        "question_id", "retrieval_method", "n_noise",
        "latency_seconds", "token_f1", "semantic_similarity",
    }
    missing_columns = required - set(data.columns)
    if missing_columns:
        raise SystemExit(f"Missing required columns: {sorted(missing_columns)}")
    if len(data) != 240:
        raise SystemExit(f"Expected 240 rows; found {len(data)}")
    if data[list(required)].isna().any().any():
        raise SystemExit("Missing values detected in required analysis columns")
    if data.duplicated(["question_id", "retrieval_method", "n_noise"]).any():
        raise SystemExit("Duplicate question/method/noise keys detected")
    if set(data["retrieval_method"].unique()) != set(METHODS):
        raise SystemExit("Unexpected retrieval methods in frozen dataset")
    if set(data["n_noise"].unique()) != {0, 1, 2, 4}:
        raise SystemExit("Unexpected distractor levels in frozen dataset")

    rows: list[dict[str, object]] = []
    for method in METHODS:
        method_data = data[data["retrieval_method"] == method]
        for noise in NOISE_LEVELS:
            baseline = method_data[method_data["n_noise"] == 0].set_index("question_id")
            noisy = method_data[method_data["n_noise"] == noise].set_index("question_id")
            common = sorted(set(baseline.index) & set(noisy.index))
            if len(common) != 20:
                raise SystemExit(f"Expected 20 matched pairs for {method=} {noise=}; got {len(common)}")

            for metric in METRICS:
                x = baseline.loc[common, metric].astype(float).to_numpy()
                y = noisy.loc[common, metric].astype(float).to_numpy()
                test = wilcoxon(y, x, alternative="two-sided", method="auto")
                baseline_mean = float(np.mean(x))
                noisy_mean = float(np.mean(y))
                change = noisy_mean - baseline_mean
                relative = (change / abs(baseline_mean) * 100.0) if baseline_mean != 0 else np.nan
                rows.append({
                    "retrieval_method": method,
                    "n_noise": noise,
                    "metric": metric,
                    "baseline_mean": baseline_mean,
                    "noisy_mean": noisy_mean,
                    "absolute_change": change,
                    "relative_change_pct": relative,
                    "wilcoxon_stat": float(test.statistic),
                    "p_value": float(test.pvalue),
                    "n": len(common),
                    "rank_biserial_correlation": paired_rank_biserial(y, x),
                })

    if len(rows) != 27:
        raise SystemExit(f"Expected 27 planned comparisons; produced {len(rows)}")

    adjusted = multipletests(
        [float(row["p_value"]) for row in rows], alpha=0.05, method="holm"
    )[1]
    for row, p_adjusted in zip(rows, adjusted):
        row["holm_p_value"] = float(p_adjusted)
        row["significant_after_holm"] = bool(p_adjusted < 0.05)

    output = pd.DataFrame(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(args.output, index=False)

    significant = output[output["significant_after_holm"]]
    print(f"Frozen CSV SHA-256: {actual_hash}")
    print(f"Validated rows: {len(data)}; paired tests: {len(output)}")
    print(f"Significant after Holm correction: {len(significant)}")
    if not significant.empty:
        print(significant[[
            "retrieval_method", "n_noise", "metric", "baseline_mean",
            "noisy_mean", "p_value", "holm_p_value",
            "rank_biserial_correlation", "n",
        ]].to_string(index=False))
    print(f"Wrote: {args.output}")


if __name__ == "__main__":
    main()
