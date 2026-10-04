"""Validate the minimum repository structure expected by the skill."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


REQUIRED = [
    "pyproject.toml",
    "README.md",
    "src/abc_sales/__init__.py",
    "src/abc_sales/config.py",
    "src/abc_sales/schemas.py",
    "src/abc_sales/io_utils.py",
    "src/abc_sales/transformations.py",
    "src/abc_sales/main.py",
    "tests/test_io.py",
    "tests/test_transformations.py",
    "sample_data/sales_sample.csv",
    "sample_data/generate_sample_data.py",
    "project_requirements/requirement_summary.md",
    "prompts/00_master_prompt.md",
    "prompts/sequence.md",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()

    missing = [relative for relative in REQUIRED if not (root / relative).exists()]
    if missing:
        print("Project structure validation FAILED. Missing:")
        for item in missing:
            print(f"- {item}")
        return 1

    print(f"Project structure validation PASSED ({len(REQUIRED)} required files found).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
