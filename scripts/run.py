#!/usr/bin/env python3
"""Main entrypoint: reorganize + update README tracker.

Usage:
    python scripts/run.py                    # incremental update
    python scripts/run.py --clean-organized  # wipe and regenerate organized/
    python scripts/run.py --no-organized     # skip generating organized/, only update README

This script:
1. Scans raw LeetSync folders (python/{topic}/{N}-{slug}/)
2. Classifies each problem via config/topics.json
3. Copies files into organized/ (preserving LeetSync names)
4. Rewrites the tracker section of README.md between <!-- TRACKER_START/END -->

Raw LeetSync files are NEVER modified or moved.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow running as `python scripts/run.py` from repo root without installing the package.
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.reorganizer.generate import generate_organized
from src.reorganizer.utils import build_problem_list
from src.tracker.readme import update_readme


def main() -> None:
    parser = argparse.ArgumentParser(description="LeetCode repo organizer and tracker.")
    parser.add_argument(
        "--clean-organized",
        action="store_true",
        help="Wipe the organized/ directory before regenerating.",
    )
    parser.add_argument(
        "--no-organized",
        action="store_true",
        help="Skip generating organized/ output (README update only).",
    )
    parser.add_argument(
        "--recent",
        type=int,
        default=5,
        metavar="N",
        help="Number of recently added problems to show in the tracker (default: 5).",
    )
    args = parser.parse_args()

    config_path = REPO_ROOT / "config" / "topics.json"
    readme_path = REPO_ROOT / "README.md"
    organized_root = REPO_ROOT / "organized"

    # ── 1. Build problem list ──────────────────────────────────────────────
    print("Scanning raw LeetSync directories...")
    problems = build_problem_list(REPO_ROOT, config_path)
    print(f"  Found {len(problems)} problems.")

    # ── 2. Generate organized/ ────────────────────────────────────────────
    if not args.no_organized:
        print(f"Generating organized/ output (clean={args.clean_organized})...")
        written = generate_organized(
            problems,
            output_root=organized_root,
            clean=args.clean_organized,
        )
        print(f"  Wrote {len(written)} problem directories into organized/.")
    else:
        print("Skipping organized/ generation (--no-organized).")

    # ── 3. Update README tracker ──────────────────────────────────────────
    print("Updating README.md tracker...")
    changed = update_readme(readme_path, problems, recent_n=args.recent)
    if changed:
        print("  README.md updated.")
    else:
        print("  README.md already up-to-date (no changes).")

    print("Done.")


if __name__ == "__main__":
    main()
