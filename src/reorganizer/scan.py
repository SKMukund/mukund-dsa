"""Scan python/{topic}/{N}-{slug}/ for organized LeetSync problems.

After the move phase (see move.py), all problems live under python/.
This module walks that structure and returns (language, topic, problem_dir)
tuples for downstream parsing and classification.
"""

from __future__ import annotations

import re
from pathlib import Path

_PROBLEM_FOLDER_RE = re.compile(r"^\d+-")

# Top-level folders that are language roots (contain topic subfolders).
_LANGUAGE_DIRS = frozenset({"python", "java", "cpp", "javascript", "typescript"})


def find_problem_dirs(
    repo_root: Path,
    languages: list[str] | None = None,
) -> list[tuple[str, str, Path]]:
    """Walk python/{topic}/{N}-slug/ and return all problem directories.

    Args:
        repo_root:  Absolute path to the repository root.
        languages:  Language folder names to scan. Defaults to auto-detection.

    Returns:
        List of (language, topic, problem_dir) sorted by language → topic → name.
    """
    results: list[tuple[str, str, Path]] = []

    for lang, lang_dir in _language_dirs(repo_root, languages):
        for topic_dir in sorted(lang_dir.iterdir()):
            if not topic_dir.is_dir():
                continue
            topic = topic_dir.name
            for problem_dir in sorted(topic_dir.iterdir()):
                if problem_dir.is_dir() and _PROBLEM_FOLDER_RE.match(problem_dir.name):
                    results.append((lang, topic, problem_dir))

    return results


def _language_dirs(repo_root: Path, languages: list[str] | None) -> list[tuple[str, Path]]:
    if languages:
        return [(lang, repo_root / lang) for lang in languages if (repo_root / lang).is_dir()]

    pairs = []
    for candidate in sorted(repo_root.iterdir()):
        if candidate.is_dir() and candidate.name in _LANGUAGE_DIRS:
            pairs.append((candidate.name, candidate))
    return pairs
