#!/usr/bin/env python3
"""Main entrypoint: reorganize + update README tracker.

Usage:
    python scripts/run.py                      # incremental update
    python scripts/run.py --clean-organized    # wipe and regenerate organized/
    python scripts/run.py --no-organized       # skip organized/, only update README
    python scripts/run.py --verbose            # detailed per-problem logging

This script:
1. Scans raw LeetSync folders — both root-level ({N}-slug/) and organized
   (python/{topic}/{N}-slug/) layouts are discovered automatically.
2. Classifies each problem via config/topics.json (falls back to uncategorized).
3. Copies files into organized/ (preserving LeetSync names).
4. Rewrites the tracker section of README.md between <!-- TRACKER_START/END -->.
5. Also updates the problem count in the introduction line.

Raw LeetSync files are NEVER modified or moved.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

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
        help="Wipe organized/ before regenerating (always used in CI).",
    )
    parser.add_argument(
        "--no-organized",
        action="store_true",
        help="Skip generating organized/ output (README update only).",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print per-problem scan, parse, classify, and output details.",
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

    # ── 1. Scan + parse + classify ─────────────────────────────────────────
    print("Scanning for LeetSync problem folders...")
    problems = build_problem_list(REPO_ROOT, config_path, verbose=args.verbose)
    print(f"  Found {len(problems)} problem(s).")

    if not problems:
        print("  WARNING: no problems found. Check repo structure and config.")

    # ── 2. Generate organized/ ─────────────────────────────────────────────
    if not args.no_organized:
        print(f"Generating organized/ (clean={args.clean_organized})...")
        written = generate_organized(
            problems,
            output_root=organized_root,
            clean=args.clean_organized,
            verbose=args.verbose,
        )
        print(f"  Wrote {len(written)} problem director(ies) into organized/.")
    else:
        print("Skipping organized/ generation (--no-organized).")

    # ── 3. Update README tracker ───────────────────────────────────────────
    print("Updating README.md tracker...")
    changed = update_readme(readme_path, problems, recent_n=args.recent)
    if changed:
        print("  README.md updated.")
    else:
        print("  README.md already up-to-date.")

    print("Done.")


if __name__ == "__main__":
    main()
