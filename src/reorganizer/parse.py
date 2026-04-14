"""Parse a raw LeetSync problem folder into structured metadata.

LeetSync names folders as:  {number}-{kebab-case-slug}/
e.g.  1-two-sum/   49-group-anagrams/   200-number-of-islands/

This module extracts the problem number and slug from the folder name,
and derives a human-readable title from the slug.
"""

from __future__ import annotations

import re
from pathlib import Path

_FOLDER_RE = re.compile(r"^(\d+)-(.+)$")

# Loaded once on first call; maps str(number) → canonical title.
_title_overrides: dict[str, str] | None = None


def _load_title_overrides(repo_root: Path | None = None) -> dict[str, str]:
    """Load config/titles.json if it exists, else return empty dict."""
    global _title_overrides
    if _title_overrides is not None:
        return _title_overrides
    if repo_root is None:
        # Infer repo root as three levels up from this file (src/reorganizer/parse.py)
        repo_root = Path(__file__).resolve().parent.parent.parent
    titles_path = repo_root / "config" / "titles.json"
    if titles_path.exists():
        import json
        _title_overrides = json.loads(titles_path.read_text())
    else:
        _title_overrides = {}
    return _title_overrides


def parse_problem_dir(problem_dir: Path) -> tuple[int, str, str]:
    """Extract (number, slug, title) from a LeetSync problem folder name.

    Args:
        problem_dir: Path to a folder like ``1-two-sum/``.

    Returns:
        A tuple of:
        - number (int): the LeetCode problem number
        - slug (str):   the kebab-case slug, e.g. "two-sum"
        - title (str):  human-readable title, e.g. "Two Sum"

    Raises:
        ValueError: if the folder name does not match the expected pattern.
    """
    name = problem_dir.name
    m = _FOLDER_RE.match(name)
    if not m:
        raise ValueError(
            f"Folder '{name}' does not match LeetSync pattern '<number>-<slug>'. "
            "Expected something like '1-two-sum' or '200-number-of-islands'."
        )
    number = int(m.group(1))
    slug = m.group(2)
    overrides = _load_title_overrides()
    title = overrides.get(str(number)) or slug_to_title(slug)
    return number, slug, title


def slug_to_title(slug: str) -> str:
    """Convert a kebab-case slug to a title-cased string.

    Examples:
        "two-sum"             → "Two Sum"
        "n-th-tribonacci-number" → "N Th Tribonacci Number"  (no special-casing needed)
        "01-matrix"           → "01 Matrix"
    """
    return " ".join(word.capitalize() for word in slug.split("-"))


def list_problem_files(problem_dir: Path) -> list[Path]:
    """Return all files inside a problem folder (solution + README + any extras).

    Only returns direct children — does not recurse deeper (LeetSync never nests further).
    """
    return [f for f in problem_dir.iterdir() if f.is_file()]


def get_last_modified(problem_dir: Path) -> float:
    """Return the most recent mtime across all files in the problem directory."""
    files = list_problem_files(problem_dir)
    if not files:
        return problem_dir.stat().st_mtime
    return max(f.stat().st_mtime for f in files)
