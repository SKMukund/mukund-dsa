"""Scan the repository for LeetSync problem folders.

LeetSync can push problems in two layouts:

  (A) Organized layout — problems already placed under a topic folder:
        python/{topic}/{N}-{slug}/

  (B) Root layout — LeetSync's default, pushed directly to repo root:
        {N}-{slug}/

This module discovers both layouts and returns a unified list of
(language, topic_or_None, problem_dir) tuples for downstream processing.
"""

from __future__ import annotations

import re
from pathlib import Path

# A LeetSync problem folder always starts with one or more digits + dash.
_PROBLEM_FOLDER_RE = re.compile(r"^\d+-")

# Language root folders (contain organized problems, never raw problem folders).
_LANGUAGE_DIRS = frozenset({"python", "java", "cpp", "javascript", "typescript"})

# Non-language, non-problem dirs to skip when scanning repo root.
_ROOT_SKIP_DIRS = frozenset({
    "organized", "src", "config", "scripts", ".github",
    ".git", ".venv", "venv", "env", "node_modules",
    "dist", "build",
})

# Map file extension → language name.
_EXT_TO_LANG = {
    ".py":   "python",
    ".java": "java",
    ".cpp":  "cpp",
    ".cc":   "cpp",
    ".js":   "javascript",
    ".ts":   "typescript",
}


def find_problem_dirs(
    repo_root: Path,
    languages: list[str] | None = None,
) -> list[tuple[str, str | None, Path]]:
    """Discover all LeetSync problem directories.

    Scans both the organized layout (``python/{topic}/{N}-slug/``) and the
    root layout (``{N}-slug/`` directly under repo_root).

    Args:
        repo_root:  Absolute path to the repository root.
        languages:  Language folders to scan for the organized layout
                    (e.g. ``["python"]``). Auto-detected if None.

    Returns:
        List of ``(language, topic, problem_dir)`` tuples.

        - ``language``: e.g. ``"python"``
        - ``topic``:    topic slug (e.g. ``"arrays_and_hashing"``) when known
                        from the folder layout, or ``None`` for root-level
                        problems (topic resolved later via classify.py).
        - ``problem_dir``: absolute Path to the problem folder.

    The list is sorted: organized problems first (by language → topic → number),
    then root-level problems (by number).
    """
    results: list[tuple[str, str | None, Path]] = []

    # ── Organized layout: python/{topic}/{N}-slug/ ─────────────────────────
    for lang, lang_dir in _discover_language_dirs(repo_root, languages):
        for topic_dir in sorted(lang_dir.iterdir()):
            if not topic_dir.is_dir():
                continue
            topic = topic_dir.name
            for problem_dir in sorted(topic_dir.iterdir()):
                if problem_dir.is_dir() and _PROBLEM_FOLDER_RE.match(problem_dir.name):
                    results.append((lang, topic, problem_dir))

    # ── Root layout: {N}-slug/ at repo root ───────────────────────────────
    for problem_dir in sorted(repo_root.iterdir()):
        if (
            problem_dir.is_dir()
            and problem_dir.name not in _ROOT_SKIP_DIRS
            and problem_dir.name not in _LANGUAGE_DIRS
            and not problem_dir.name.startswith(".")
            and _PROBLEM_FOLDER_RE.match(problem_dir.name)
        ):
            lang = _detect_language(problem_dir)
            results.append((lang, None, problem_dir))  # topic resolved by classifier

    return results


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _discover_language_dirs(
    repo_root: Path, languages: list[str] | None
) -> list[tuple[str, Path]]:
    """Return (language_name, path) pairs for organized language root folders."""
    if languages:
        return [(lang, repo_root / lang) for lang in languages if (repo_root / lang).is_dir()]

    pairs = []
    for candidate in sorted(repo_root.iterdir()):
        if (
            candidate.is_dir()
            and not candidate.name.startswith(".")
            and candidate.name not in _ROOT_SKIP_DIRS
            # Only consider known language dirs or dirs that look like one
            and (candidate.name in _LANGUAGE_DIRS or _contains_organized_problems(candidate))
        ):
            pairs.append((candidate.name, candidate))
    return pairs


def _contains_organized_problems(lang_dir: Path) -> bool:
    """Return True if lang_dir/{topic}/{N}-name/ structure exists."""
    for topic_dir in lang_dir.iterdir():
        if not topic_dir.is_dir():
            continue
        for child in topic_dir.iterdir():
            if child.is_dir() and _PROBLEM_FOLDER_RE.match(child.name):
                return True
    return False


def _detect_language(problem_dir: Path) -> str:
    """Infer language from the file extensions inside a problem folder."""
    for f in problem_dir.iterdir():
        lang = _EXT_TO_LANG.get(f.suffix.lower())
        if lang:
            return lang
    return "unknown"
