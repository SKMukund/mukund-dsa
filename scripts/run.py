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
    Classify each via config/topics.json (then code analysis as fallback) and move it
    into python/{topic}/ using git mv.  This preserves git history.

Phase 1.5 — Drain uncategorized/
    Scan python/uncategorized/ for problems that the code classifier can now resolve.
    Move each one to its inferred topic folder using git mv.

Phase 2 — Track
    Scan python/{topic}/{N}-slug/ for all problems.
    Refresh config/difficulty_map.json — parse each problem's README.md badge and add
    any missing entries.  Recompute statistics and rewrite the README tracker.

Raw LeetSync file and folder names are never changed — only their location moves.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.reorganizer.classify import TopicClassifier
from src.reorganizer.move import find_unorganized_problem_dirs, move_problem
from src.reorganizer.parse import parse_problem_dir
from src.reorganizer.utils import build_problem_list
from src.tracker.readme import update_readme
from src.tracker.utils import DifficultyMap

_FALLBACK_TOPIC = "uncategorized"
_PROBLEM_RE = re.compile(r"^\d+-")


def _drain_uncategorized(
    repo_root: Path,
    classifier: TopicClassifier,
    *,
    dry_run: bool,
    verbose: bool,
) -> None:
    """Move problems out of python/uncategorized/ when code analysis classifies them.

    This is idempotent: problems that cannot be classified stay in uncategorized/.
    """
    uncategorized_dir = repo_root / "python" / "uncategorized"
    if not uncategorized_dir.is_dir():
        return

    candidates = sorted(
        d for d in uncategorized_dir.iterdir()
        if d.is_dir() and _PROBLEM_RE.match(d.name)
    )
    if not candidates:
        return

    print(
        f"Phase 1.5 — Checking {len(candidates)} problem(s) in uncategorized/ "
        "for code-based reclassification..."
    )

    for problem_dir in candidates:
        try:
            number, _, _ = parse_problem_dir(problem_dir)
        except ValueError as exc:
            print(f"  [skip]  {problem_dir.name} — could not parse: {exc}")
            continue

        # Only reclassify if not pinned in topics.json (that mapping is authoritative).
        topic = classifier.classify(
            number,
            fallback_topic=_FALLBACK_TOPIC,
            problem_dir=problem_dir,
            verbose=verbose,
        )

        if topic == _FALLBACK_TOPIC:
            if verbose:
                print(f"  [keep]  {problem_dir.name} — stays in uncategorized/")
            continue

        dest = repo_root / "python" / topic / problem_dir.name
        print(f"  [found] uncategorized/{problem_dir.name} → python/{topic}/")

        if dry_run:
            print(f"  [dry]   would move to {dest.relative_to(repo_root)}")
            continue

        move_problem(repo_root, problem_dir, topic, verbose=verbose)


def _refresh_difficulty_map(
    diff_map: DifficultyMap,
    problems: list,
    verbose: bool = False,
) -> None:
    """Parse README.md badges and update difficulty_map.json with new entries.

    Existing entries are never overwritten — manual edits to the JSON are safe.
    Only newly encountered problems (missing from the map) are added.

    Args:
        diff_map:  Loaded DifficultyMap (modified in place if new entries found).
        problems:  Full problem list from build_problem_list().
        verbose:   Print per-problem lines for newly added entries.
    """
    n_new = 0
    for p in problems:
        added = diff_map.ingest(p.folder_name, p.source_dir)
        if added:
            n_new += 1
            if verbose:
                level = diff_map.get(p.folder_name)
                print(f"  [difficulty] {p.folder_name} → {level}")

    if n_new:
        diff_map.save()
        print(f"  difficulty_map.json updated — {n_new} new entr{'y' if n_new == 1 else 'ies'} added.")
    elif verbose:
        print(f"  difficulty_map.json already up-to-date ({len(diff_map)} entries).")


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
    diff_path = REPO_ROOT / "config" / "difficulty_map.json"
    readme_path = REPO_ROOT / "README.md"

    classifier = TopicClassifier(config_path)

    # ── Phase 1: Relocate unorganized LeetSync folders ────────────────────
    # Scans both repo root and LeetCode/ subfolder.
    unorganized = find_unorganized_problem_dirs(REPO_ROOT)

    if unorganized:
        print(f"Phase 1 — Relocating {len(unorganized)} unorganized folder(s)...")

        for problem_dir in unorganized:
            try:
                number, _, _ = parse_problem_dir(problem_dir)
            except ValueError as exc:
                print(f"  [skip]  {problem_dir.name} — could not parse: {exc}")
                continue

            topic = classifier.classify(
                number,
                fallback_topic=_FALLBACK_TOPIC,
                problem_dir=problem_dir,
                verbose=args.verbose,
            )
            src_rel = problem_dir.relative_to(REPO_ROOT)
            dest = REPO_ROOT / "python" / topic / problem_dir.name

            print(f"  [found] {src_rel} → python/{topic}/ (#{number})")

            if args.dry_run:
                print(f"  [dry]   would move to {dest.relative_to(REPO_ROOT)}")
                continue

            move_problem(REPO_ROOT, problem_dir, topic, verbose=args.verbose)
    else:
        print("Phase 1 — No unorganized problem folders detected.")

    # ── Phase 1.5: Drain uncategorized/ ───────────────────────────────────
    _drain_uncategorized(
        REPO_ROOT,
        classifier,
        dry_run=args.dry_run,
        verbose=args.verbose,
    )

    if args.dry_run:
        print("Dry run complete — no changes made.")
        return

    # ── Phase 2: Scan python/ and update README ────────────────────────────
    print("Phase 2 — Scanning python/ and updating tracker...")
    problems = build_problem_list(REPO_ROOT, config_path, verbose=args.verbose)
    print(f"  Found {len(problems)} problem(s) in python/.")

    # Refresh difficulty_map.json before rendering the README.
    diff_map = DifficultyMap(diff_path)
    _refresh_difficulty_map(diff_map, problems, verbose=args.verbose)

    changed = update_readme(readme_path, problems, diff_map, recent_n=args.recent)
    if changed:
        print("  README.md updated.")
    else:
        print("  README.md already up-to-date.")

    print("Done.")


if __name__ == "__main__":
    main()
