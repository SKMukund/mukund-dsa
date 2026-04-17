"""Build the full problem list from python/{topic}/ after the move phase."""

from __future__ import annotations

from pathlib import Path

from src.reorganizer.classify import TopicClassifier
from src.reorganizer.models import Problem
from src.reorganizer.parse import get_last_modified, list_problem_files, parse_problem_dir
from src.reorganizer.scan import find_problem_dirs


def build_problem_list(
    repo_root: Path,
    config_path: Path,
    verbose: bool = False,
) -> list[Problem]:
    """Scan python/ and return a sorted list of Problem objects.

    Called after move.py has already relocated any root-level folders,
    so python/ is the complete source of truth at this point.

    Args:
        repo_root:   Root of the git repository.
        config_path: Path to config/topics.json.
        verbose:     Print per-problem parse/classify details.

    Returns:
        List of Problems sorted by number.
    """
    classifier = TopicClassifier(config_path)
    problems: list[Problem] = []

    entries = find_problem_dirs(repo_root)
    if verbose:
        print(f"  [scan]  {len(entries)} folder(s) found in python/")

    for language, raw_topic, problem_dir in entries:
        try:
            number, slug, title = parse_problem_dir(problem_dir)
        except ValueError as exc:
            print(f"  [skip]  {problem_dir} — {exc}")
            continue

        # Pass problem_dir so that problems already sitting in "uncategorized/"
        # are re-evaluated by the code classifier instead of staying there.
        topic = classifier.classify(
            number,
            fallback_topic=raw_topic,
            problem_dir=problem_dir,
            verbose=verbose,
        )

        if verbose:
            print(f"  [parse] #{number:>4} {title} (python/{raw_topic}) → topic={topic}")

        problems.append(
            Problem(
                number=number,
                slug=slug,
                title=title,
                language=language,
                topic=topic,
                source_dir=problem_dir,
                files=list_problem_files(problem_dir),
                last_modified=get_last_modified(problem_dir),
            )
        )

    problems.sort(key=lambda p: p.number)

    if verbose:
        print(f"  [total] {len(problems)} problem(s)")

    return problems
