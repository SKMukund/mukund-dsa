"""Scan the raw LeetSync directory tree for problem folders.

Expected layout (source of truth — never modified by this tool):

    {repo_root}/{language}/{topic}/{N}-{slug}/
        {slug}.py          ← solution file
        README.md          ← problem statement

This module discovers all matching problem folders and returns their paths.
"""

from __future__ import annotations

import re
from pathlib import Path

# A LeetSync problem folder always starts with one or more digits followed by a dash.
_PROBLEM_FOLDER_RE = re.compile(r"^\d+-")


def find_problem_dirs(repo_root: Path, languages: list[str] | None = None) -> list[tuple[str, str, Path]]:
    """Walk the repo and return all raw LeetSync problem directories.

    Args:
        repo_root:  Root of the git repository.
        languages:  Language folder names to scan (e.g. ["python", "java"]).
                    Defaults to every top-level folder that contains topic subfolders.

    Returns:
        List of (language, topic, problem_dir) tuples, sorted by language → topic → number.
    """
    results: list[tuple[str, str, Path]] = []

    lang_dirs = _discover_language_dirs(repo_root, languages)

    for lang, lang_dir in lang_dirs:
        for topic_dir in sorted(lang_dir.iterdir()):
            if not topic_dir.is_dir():
                continue
            topic = topic_dir.name
            for problem_dir in sorted(topic_dir.iterdir()):
                if problem_dir.is_dir() and _PROBLEM_FOLDER_RE.match(problem_dir.name):
                    results.append((lang, topic, problem_dir))

    return results


def _discover_language_dirs(repo_root: Path, languages: list[str] | None) -> list[tuple[str, Path]]:
    """Return (language_name, path) pairs for language root folders.

    If `languages` is given, only those folders are checked (they must exist).
    Otherwise, every subfolder of repo_root that contains at least one topic
    subfolder (which itself contains a LeetSync problem folder) is included.
    """
    if languages:
        pairs = []
        for lang in languages:
            p = repo_root / lang
            if p.is_dir():
                pairs.append((lang, p))
        return pairs

    # Auto-discover: look for folders whose children look like topic directories
    # (contain at least one LeetSync problem folder).
    pairs = []
    for candidate in sorted(repo_root.iterdir()):
        if not candidate.is_dir() or candidate.name.startswith("."):
            continue
        # Skip well-known non-language dirs
        if candidate.name in {"src", "organized", "config", "scripts", ".github"}:
            continue
        if _contains_problems(candidate):
            pairs.append((candidate.name, candidate))
    return pairs


def _contains_problems(lang_dir: Path) -> bool:
    """Return True if lang_dir has at least one grandchild that looks like a problem folder."""
    for topic_dir in lang_dir.iterdir():
        if not topic_dir.is_dir():
            continue
        for child in topic_dir.iterdir():
            if child.is_dir() and _PROBLEM_FOLDER_RE.match(child.name):
                return True
    return False
