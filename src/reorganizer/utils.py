"""Utility helpers for the reorganizer package."""

from __future__ import annotations

from pathlib import Path

from src.reorganizer.classify import TopicClassifier
from src.reorganizer.models import Problem
from src.reorganizer.parse import get_last_modified, list_problem_files, parse_problem_dir
from src.reorganizer.scan import find_problem_dirs

_FALLBACK_TOPIC = "uncategorized"


def build_problem_list(
    repo_root: Path,
    config_path: Path,
    verbose: bool = False,
) -> list[Problem]:
    """Full pipeline: scan → parse → classify → deduplicate → return Problem list.

    Discovers both organized (python/{topic}/{N}-slug/) and root-level
    ({N}-slug/) LeetSync folders.  If the same problem number appears in
    both, the organized copy takes precedence.

    Args:
        repo_root:   Root of the git repository.
        config_path: Path to ``config/topics.json``.
        verbose:     If True, print per-problem scan/classify details.

    Returns:
        List of Problem objects sorted by problem number.
    """
    classifier = TopicClassifier(config_path)

    # number → Problem; organized wins over root if both exist
    seen: dict[int, Problem] = {}
    skipped: list[str] = []

    raw_entries = find_problem_dirs(repo_root)
    if verbose:
        print(f"  [scan] found {len(raw_entries)} candidate folder(s)")

    for language, raw_topic, problem_dir in raw_entries:
        # ── Parse ──────────────────────────────────────────────────────────
        try:
            number, slug, title = parse_problem_dir(problem_dir)
        except ValueError as exc:
            reason = f"parse error: {exc}"
            skipped.append(f"  [skip] {problem_dir} — {reason}")
            continue

        # ── Classify ───────────────────────────────────────────────────────
        topic = classifier.classify(number, fallback_topic=raw_topic or _FALLBACK_TOPIC)

        if verbose:
            source = "root" if raw_topic is None else f"python/{raw_topic}"
            print(f"  [parse]    #{number:>4} {title} ({source}) → topic={topic}")

        # ── Deduplicate ────────────────────────────────────────────────────
        # Organized copy (raw_topic is not None) takes precedence over root copy.
        if number in seen:
            existing = seen[number]
            existing_is_organized = existing.source_dir.parent != repo_root
            this_is_organized = raw_topic is not None

            if existing_is_organized and not this_is_organized:
                if verbose:
                    print(f"  [dedup]    #{number} keeping organized copy, skipping root copy")
                continue
            elif not existing_is_organized and this_is_organized:
                if verbose:
                    print(f"  [dedup]    #{number} replacing root copy with organized copy")
            else:
                if verbose:
                    print(f"  [dedup]    #{number} duplicate — keeping first seen")
                continue

        files = list_problem_files(problem_dir)
        last_modified = get_last_modified(problem_dir)

        seen[number] = Problem(
            number=number,
            slug=slug,
            title=title,
            language=language,
            topic=topic,
            source_dir=problem_dir,
            files=files,
            last_modified=last_modified,
        )

    if skipped:
        for msg in skipped:
            print(msg)

    problems = sorted(seen.values(), key=lambda p: p.number)

    if verbose:
        print(f"  [result]   {len(problems)} unique problem(s) after deduplication")

    return problems
