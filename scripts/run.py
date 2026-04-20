#!/usr/bin/env python3
"""Main entrypoint: relocate new LeetSync folders + update README tracker.

Usage:
    python scripts/run.py               # normal run
    python scripts/run.py --verbose     # per-problem logging
    python scripts/run.py --dry-run     # show what would move, make no changes

Flow
----
Phase 1 — Relocate
    Detect any {N}-{slug}/ folders at the repo root (LeetSync's default drop
    location).  Classify each via topics.json (then code analysis as fallback)
    and move into python/{topic}/ using git mv.

Phase 2 — Reconcile
    Scan every problem already inside python/{topic}/.  For each, compare its
    current folder to the authoritative topic from topics.json / code analysis.
    Move any that are in the wrong folder.  Also drains python/uncategorized/.
    New classifications are auto-written to topics.json.

Phase 3 — Save topics.json
    Flush any new entries added during Phases 1–2 in one atomic write.

Phase 4 — Track
    Refresh config/difficulty_map.json (parse README badges for new problems).
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
from src.reorganizer.scan import find_problem_dirs
from src.reorganizer.utils import build_problem_list
from src.tracker.readme import update_readme
from src.tracker.utils import DifficultyMap

_FALLBACK_TOPIC = "uncategorized"


# ---------------------------------------------------------------------------
# Phase 1 helpers
# ---------------------------------------------------------------------------

def _phase1_relocate(
    repo_root: Path,
    classifier: TopicClassifier,
    *,
    dry_run: bool,
    verbose: bool,
) -> None:
    """Move new LeetSync drops from the repo root / LeetCode/ into python/."""
    unorganized = find_unorganized_problem_dirs(repo_root)

    if not unorganized:
        print("Phase 1 — No new problem folders detected.")
        return

    print(f"Phase 1 — Relocating {len(unorganized)} new problem folder(s)...")

    for problem_dir in unorganized:
        try:
            _, _, _ = parse_problem_dir(problem_dir)
        except ValueError as exc:
            print(f"  [skip]  {problem_dir.name} — could not parse: {exc}")
            continue

        tr = classifier.classify(
            problem_dir.name,
            fallback_topic=_FALLBACK_TOPIC,
            problem_dir=problem_dir,
            verbose=verbose,
        )
        topic = tr.topic
        src_rel = problem_dir.relative_to(repo_root)
        dest = repo_root / "python" / topic / problem_dir.name

        print(f"  [found] {src_rel} → python/{topic}/")

        if dry_run:
            print(f"  [dry]   would move to {dest.relative_to(repo_root)}")
            continue

        move_problem(repo_root, problem_dir, topic, verbose=verbose)


# ---------------------------------------------------------------------------
# Phase 2 helpers
# ---------------------------------------------------------------------------

def _phase2_reconcile(
    repo_root: Path,
    classifier: TopicClassifier,
    *,
    dry_run: bool,
    verbose: bool,
) -> int:
    """Detect and fix problems sitting in the wrong topic folder.

    For every problem in ``python/{topic}/{folder}/``:
    - Look up the authoritative topic (topics.json → code classifier → fallback).
    - If the authoritative topic differs from the current folder, move it.
    - This also handles ``python/uncategorized/`` as a special case.

    Returns the number of problems that were moved (or would be in dry-run).
    """
    entries = find_problem_dirs(repo_root)
    moved = 0

    for _, raw_topic, problem_dir in entries:
        try:
            _, _, _ = parse_problem_dir(problem_dir)
        except ValueError:
            continue

        tr = classifier.classify(
            problem_dir.name,
            fallback_topic=raw_topic,
            problem_dir=problem_dir,
            verbose=verbose,
        )
        authoritative = tr.topic

        if authoritative == raw_topic:
            continue  # already in the right place

        if authoritative == _FALLBACK_TOPIC:
            # Classifier couldn't improve on "uncategorized" — leave it.
            continue

        dest = repo_root / "python" / authoritative / problem_dir.name
        print(
            f"  [correct] {problem_dir.name}: "
            f"python/{raw_topic}/ → python/{authoritative}/"
        )
        moved += 1

        if dry_run:
            print(f"  [dry]   would move to {dest.relative_to(repo_root)}")
            continue

        move_problem(repo_root, problem_dir, authoritative, verbose=verbose)

    return moved


# ---------------------------------------------------------------------------
# Phase 4 helper
# ---------------------------------------------------------------------------

def _refresh_difficulty_map(
    diff_map: DifficultyMap,
    problems: list,
    verbose: bool = False,
) -> None:
    """Parse README.md badges for new problems and update difficulty_map.json."""
    n_new = 0
    for p in problems:
        added = diff_map.ingest(p.folder_name, p.source_dir)
        if added:
            n_new += 1
            if verbose:
                print(f"  [difficulty] {p.folder_name} → {diff_map.get(p.folder_name)}")

    if n_new:
        diff_map.save()
        print(
            f"  difficulty_map.json updated — "
            f"{n_new} new entr{'y' if n_new == 1 else 'ies'} added."
        )
    elif verbose:
        print(f"  difficulty_map.json already up-to-date ({len(diff_map)} entries).")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="LeetCode repo organizer and tracker.")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Print per-problem details for every phase.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be moved without making any changes.")
    parser.add_argument("--recent", type=int, default=5, metavar="N",
                        help="Number of recently added problems in the README (default: 5).")
    args = parser.parse_args()

    config_path = REPO_ROOT / "config" / "topics.json"
    diff_path   = REPO_ROOT / "config" / "difficulty_map.json"
    readme_path = REPO_ROOT / "README.md"

    classifier = TopicClassifier(config_path)

    # ── Phase 1: Relocate new drops ───────────────────────────────────────
    _phase1_relocate(REPO_ROOT, classifier, dry_run=args.dry_run, verbose=args.verbose)

    # ── Phase 2: Reconcile misplaced problems ─────────────────────────────
    entries = find_problem_dirs(REPO_ROOT)
    total_in_python = len(entries)
    print(f"Phase 2 — Reconciling {total_in_python} organised problem(s)...")

    moved = _phase2_reconcile(
        REPO_ROOT, classifier, dry_run=args.dry_run, verbose=args.verbose
    )

    if moved:
        print(f"  Moved {moved} problem(s) to the correct topic folder.")
    else:
        print("  All problems are in the correct folder.")

    if args.dry_run:
        print("Dry run complete — no changes made.")
        return

    # ── Phase 3: Persist any new topics.json entries ──────────────────────
    if classifier.is_dirty():
        classifier.save()
        print("Phase 3 — topics.json updated with new classification(s).")
    else:
        print("Phase 3 — topics.json already up-to-date.")

    # ── Phase 4: Scan python/ and update README ────────────────────────────
    print("Phase 4 — Scanning python/ and updating tracker...")
    problems = build_problem_list(REPO_ROOT, config_path, verbose=args.verbose)
    print(f"  Found {len(problems)} problem(s) in python/.")

    diff_map = DifficultyMap(diff_path)
    _refresh_difficulty_map(diff_map, problems, verbose=args.verbose)

    changed = update_readme(readme_path, problems, diff_map, recent_n=args.recent)
    print("  README.md updated." if changed else "  README.md already up-to-date.")

    print("Done.")


if __name__ == "__main__":
    main()
