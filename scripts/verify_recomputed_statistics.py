#!/usr/bin/env python3
"""Compare freshly recomputed primary statistics with the committed validated table.

This check never calls an LLM or network service. Run after
recompute_primary_statistics.py in a clean environment.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

KEYS = ["retrieval_method", "n_noise", "metric"]
BOOL_COLUMNS = ["significant_after_holm"]
NUMERIC_COLUMNS = [
    "baseline_mean", "noisy_mean", "absolute_change", "relative_change_pct",
    "wilcoxon_stat", "p_value", "n", "rank_biserial_correlation",
    "holm_p_value",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("recomputed", type=Path)
    parser.add_argument("validated", type=Path)
    args = parser.parse_args()

    actual = pd.read_csv(args.recomputed).sort_values(KEYS).reset_index(drop=True)
    expected = pd.read_csv(args.validated).sort_values(KEYS).reset_index(drop=True)

    if len(actual) != 27 or len(expected) != 27:
        raise SystemExit(f"Expected 27 rows in each file; got recomputed={len(actual)}, validated={len(expected)}")
    if actual[KEYS].to_dict("records") != expected[KEYS].to_dict("records"):
        raise SystemExit("Comparison keys differ between recomputed and validated tables")

    for column in NUMERIC_COLUMNS:
        if column not in actual or column not in expected:
            raise SystemExit(f"Missing expected numeric column: {column}")
        a = pd.to_numeric(actual[column], errors="raise").to_numpy(dtype=float)
        b = pd.to_numeric(expected[column], errors="raise").to_numpy(dtype=float)
        if not np.allclose(a, b, rtol=1e-8, atol=1e-10, equal_nan=True):
            indices = np.flatnonzero(~np.isclose(a, b, rtol=1e-8, atol=1e-10, equal_nan=True))
            details = [(int(i), float(a[i]), float(b[i])) for i in indices[:5]]
            raise SystemExit(f"Numeric mismatch in {column}; first mismatches (row, recomputed, validated): {details}")

    for column in BOOL_COLUMNS:
        a = actual[column].astype(str).str.lower().to_numpy()
        b = expected[column].astype(str).str.lower().to_numpy()
        if not np.array_equal(a, b):
            raise SystemExit(f"Boolean mismatch in {column}")

    significant = actual[actual["significant_after_holm"].astype(str).str.lower() == "true"]
    print("Validated comparison: PASS")
    print(f"Rows compared: {len(actual)}")
    print(f"Numeric columns compared: {len(NUMERIC_COLUMNS)}")
    print(f"Boolean columns compared: {len(BOOL_COLUMNS)}")
    print(f"Holm-significant comparisons: {len(significant)}")
    if not significant.empty:
        print(significant[KEYS + ["baseline_mean", "noisy_mean", "p_value", "holm_p_value"]].to_string(index=False))


if __name__ == "__main__":
    main()
