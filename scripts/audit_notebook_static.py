#!/usr/bin/env python3
"""Static safety/reproducibility audit for the saved Kaggle notebook.

This script does not execute notebook cells and makes no network/API calls.
It reports code cells that may install packages, inspect remote APIs, or call
Groq so reviewers can avoid accidentally rerunning the LLM evaluation.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

API_PATTERNS = {
    "Groq client / generation": re.compile(
        r"Groq\(|chat\.completions\.create|GROQ_API_KEY|groq_client", re.I
    ),
    "HTTP request": re.compile(r"requests\.(get|post|put|delete)\(", re.I),
    "Package installation": re.compile(r"(^|\n)\s*!pip\s+install\b", re.I),
}
STALE_PATTERNS = {
    "obsolete 36-test family": re.compile(r"36\s+(planned\s+)?(paired\s+)?comparisons", re.I),
    "obsolete latency result": re.compile(r"0\.4137|0\.6246|50\.99%|0\.0130|0\.8286"),
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "notebook",
        type=Path,
        nargs="?",
        default=Path("notebook/rag-retrieval-robustness-study.ipynb"),
    )
    args = parser.parse_args()

    nb = json.loads(args.notebook.read_text(encoding="utf-8"))
    cells = nb.get("cells", [])
    if not cells:
        raise SystemExit("Notebook has no cells.")

    executed = sum(
        c.get("cell_type") == "code" and c.get("execution_count") is not None
        for c in cells
    )
    print(f"Notebook JSON: valid ({len(cells)} cells)")
    print(f"Code cells with saved execution counts: {executed}")
    print("Execution mode: STATIC ONLY; no cells were executed.")

    risky = []
    stale = []
    for i, cell in enumerate(cells):
        source = "".join(cell.get("source", []))
        if cell.get("cell_type") == "code":
            for label, pattern in API_PATTERNS.items():
                if pattern.search(source):
                    risky.append((i, label))
        for label, pattern in STALE_PATTERNS.items():
            if pattern.search(source):
                stale.append((i, label))

    print("\nCells requiring caution before any manual execution:")
    if risky:
        for index, label in risky:
            print(f"  cell {index}: {label}")
    else:
        print("  none detected")

    print("\nObsolete primary-result wording in cell source:")
    if stale:
        for index, label in stale:
            print(f"  cell {index}: {label}")
    else:
        print("  none detected")

    intro = "".join(cells[0].get("source", [])) if cells else ""
    print("\nProminent no-Run-All warning:", "do not use" in intro.lower() and "run all" in intro.lower())
    print("Note: this is a static audit, not a clean runtime reproducibility test.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
