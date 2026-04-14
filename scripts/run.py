#!/usr/bin/env python3
"""Main entrypoint: relocate new LeetSync folders + update README tracker.

Usage:
    python scripts/run.py               # normal run
    python scripts/run.py --verbose     # per-problem logging
    python scripts/run.py --dry-run     # show what would move, make no changes

Flow
----
Phase 1 — Relocate
    Detect any {N}-{slug}/ folders at the repo root (LeetSync's default drop location).
    Classify each via config/topics.json and move it into python/{topic}/ using git mv.
    This preserves git history and keeps python/ as the single source of truth.

Phase 2 — Track
    Scan python/{topic}/{N}-slug/ for all problems.
    Recompute statistics and rewrite the README tracker between marker comments.

Raw LeetSync file and folder names are never changed — only their location moves.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.reorganizer.classify import TopicClassifier
from src.reorganizer.move import find_unorganized_problem_dirs, move_problem
from src.reorganizer.parse import parse_problem_dir
from src.reorganizer.utils import build_problem_list
from src.tracker.readme import update_readme

_FALLBACK_TOPIC = "uncategorized"


def main() -> None:
    parser = argparse.ArgumentParser(description="LeetCode repo organizer and tracker.")
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print per-problem details for every phase.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be moved without making any changes.",
    )
    parser.add_argument(
        "--recent",
        type=int,
        default=5,
        metavar="N",
        help="Number of recently added problems in the README tracker (default: 5).",
    )
    args = parser.parse_args()

    config_path = REPO_ROOT / "config" / "topics.json"
    readme_path = REPO_ROOT / "README.md"

    # ── Phase 1: Relocate unorganized LeetSync folders ────────────────────
    # Scans both repo root and LeetCode/ subfolder.
    unorganized = find_unorganized_problem_dirs(REPO_ROOT)

    if unorganized:
        print(f"Phase 1 — Relocating {len(unorganized)} unorganized folder(s)...")
        classifier = TopicClassifier(config_path)

        for problem_dir in unorganized:
            try:
                number, _, _ = parse_problem_dir(problem_dir)
            except ValueError as exc:
                print(f"  [skip]  {problem_dir.name} — could not parse: {exc}")
                continue

            topic = classifier.classify(number, fallback_topic=_FALLBACK_TOPIC)
            src_rel = problem_dir.relative_to(REPO_ROOT)
            dest = REPO_ROOT / "python" / topic / problem_dir.name

            print(f"  [found] {src_rel} → python/{topic}/ (#{number})")

            if args.dry_run:
                print(f"  [dry]   would move to {dest.relative_to(REPO_ROOT)}")
                continue

            move_problem(REPO_ROOT, problem_dir, topic, verbose=args.verbose)
    else:
        print("Phase 1 — No unorganized problem folders detected.")

    if args.dry_run:
        print("Dry run complete — no changes made.")
        return

    # ── Phase 2: Scan python/ and update README ────────────────────────────
    print("Phase 2 — Scanning python/ and updating tracker...")
    problems = build_problem_list(REPO_ROOT, config_path, verbose=args.verbose)
    print(f"  Found {len(problems)} problem(s) in python/.")

    changed = update_readme(readme_path, problems, recent_n=args.recent)
    if changed:
        print("  README.md updated.")
    else:
        print("  README.md already up-to-date.")

    print("Done.")


if __name__ == "__main__":
    main()
