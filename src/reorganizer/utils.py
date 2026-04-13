"""Utility helpers for the reorganizer package."""

from __future__ import annotations

from pathlib import Path

from src.reorganizer.classify import TopicClassifier
from src.reorganizer.models import Problem
from src.reorganizer.parse import get_last_modified, list_problem_files, parse_problem_dir
from src.reorganizer.scan import find_problem_dirs


def build_problem_list(repo_root: Path, config_path: Path) -> list[Problem]:
    """Full pipeline: scan → parse → classify → return Problem list.

    This is the main entry point for consumers that need a list of all problems.

    Args:
        repo_root:   Root of the git repository.
        config_path: Path to ``config/topics.json``.

    Returns:
        List of Problem objects, sorted by problem number.
    """
    classifier = TopicClassifier(config_path)
    problems: list[Problem] = []

    for language, raw_topic, problem_dir in find_problem_dirs(repo_root):
        try:
            number, slug, title = parse_problem_dir(problem_dir)
        except ValueError as exc:
            print(f"[WARN] Skipping {problem_dir}: {exc}")
            continue

        topic = classifier.classify(number, fallback_topic=raw_topic)
        files = list_problem_files(problem_dir)
        last_modified = get_last_modified(problem_dir)

        problems.append(
            Problem(
                number=number,
                slug=slug,
                title=title,
                language=language,
                topic=topic,
                source_dir=problem_dir,
                files=files,
                last_modified=last_modified,
            )
        )

    problems.sort(key=lambda p: p.number)
    return problems
