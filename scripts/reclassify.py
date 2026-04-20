#!/usr/bin/env python3
"""Reclassify problems stuck in python/uncategorized/.

Usage:
    python scripts/reclassify.py               # attempt reclassification
    python scripts/reclassify.py --verbose     # per-problem signal details
    python scripts/reclassify.py --dry-run     # show what would move, no changes

This script targets only python/uncategorized/.  Already-categorized folders
are never touched.  Safe and idempotent — run as many times as you like.

Flow
----
1. Scan python/uncategorized/ for all valid problem folders.
2. For each, run the classification pipeline:
     topics.json override → heuristic code classifier → fallback
3. Any problem whose authoritative topic is no longer "uncategorized" is moved
   via git mv into python/<topic>/.
4. New topic entries are flushed to topics.json in one write.
5. README tracker is refreshed to reflect the updated layout.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.reorganizer.classify import TopicClassifier
from src.reorganizer.move import move_problem
from src.reorganizer.parse import parse_problem_dir
from src.reorganizer.scan import find_problem_dirs
from src.reorganizer.utils import build_problem_list
from src.tracker.readme import update_readme
from src.tracker.utils import DifficultyMap

_UNCATEGORIZED = "uncategorized"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Reclassify problems in python/uncategorized/."
    )
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Print per-problem signal details.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would move without making any changes.")
    parser.add_argument("--recent", type=int, default=5, metavar="N",
                        help="Number of recently added problems in the README (default: 5).")
    args = parser.parse_args()

    config_path = REPO_ROOT / "config" / "topics.json"
    diff_path   = REPO_ROOT / "config" / "difficulty_map.json"
    readme_path = REPO_ROOT / "README.md"

    classifier = TopicClassifier(config_path)

    # ── Find all problems currently in uncategorized ─────────────────────────
    all_entries = find_problem_dirs(REPO_ROOT)
    uncategorized = [
        (lang, topic, pdir)
        for lang, topic, pdir in all_entries
        if topic == _UNCATEGORIZED
    ]

    if not uncategorized:
        print("No problems in python/uncategorized/ — nothing to do.")
        return

    print(f"Scanning {len(uncategorized)} problem(s) in python/uncategorized/...")
    print()

    moved: list[tuple[str, str]] = []      # (folder_name, new_topic)
    remaining: list[str] = []              # folder_names still uncategorized

    for _, _, problem_dir in uncategorized:
        try:
            number, _, title = parse_problem_dir(problem_dir)
        except ValueError as exc:
            print(f"  [skip]  {problem_dir.name} — could not parse: {exc}")
            continue

        tr = classifier.classify(
            problem_dir.name,
            fallback_topic=_UNCATEGORIZED,
            problem_dir=problem_dir,
            verbose=args.verbose,
        )

        if tr.topic == _UNCATEGORIZED:
            remaining.append(problem_dir.name)
            print(f"  [stays]  #{number:>4} {title} → still uncategorized")
            continue

        moved.append((problem_dir.name, tr.topic))
        dest = REPO_ROOT / "python" / tr.topic / problem_dir.name
        print(
            f"  [move]   #{number:>4} {title} "
            f"→ python/{tr.topic}/ ({tr.confidence}, {tr.source})"
        )

        if args.dry_run:
            print(f"  [dry]    would move to {dest.relative_to(REPO_ROOT)}")
            continue

        move_problem(REPO_ROOT, problem_dir, tr.topic, verbose=args.verbose)

    # ── Summary ───────────────────────────────────────────────────────────────
    print()
    print(f"Results: {len(moved)} reclassified · {len(remaining)} still uncategorized")
    if moved:
        for folder, topic in moved:
            print(f"  ✓ {folder} → {topic}")
    if remaining:
        for folder in remaining:
            print(f"  · {folder} (unchanged)")

    if args.dry_run:
        print()
        print("Dry run complete — no changes made.")
        return

    # ── Persist new topics.json entries ──────────────────────────────────────
    if classifier.is_dirty():
        classifier.save()
        print()
        print("topics.json updated with new classification(s).")

    if not moved:
        print()
        print("Nothing moved — README unchanged.")
        return

    # ── Refresh README tracker ────────────────────────────────────────────────
    print()
    print("Refreshing README tracker...")
    problems = build_problem_list(REPO_ROOT, config_path, verbose=False)
    diff_map = DifficultyMap(diff_path)

    # Ingest difficulty for any newly classified problems
    n_new = sum(1 for p in problems if diff_map.ingest(p.folder_name, p.source_dir))
    if n_new:
        diff_map.save()

    changed = update_readme(readme_path, problems, diff_map, recent_n=args.recent)
    print("  README.md updated." if changed else "  README.md already up-to-date.")

    print()
    print("Done.")


if __name__ == "__main__":
    main()
