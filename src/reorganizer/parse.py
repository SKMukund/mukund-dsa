"""Parse a raw LeetSync problem folder into structured metadata.

LeetSync names folders as:  {number}-{kebab-case-slug}/
e.g.  1-two-sum/   49-group-anagrams/   200-number-of-islands/

This module extracts the problem number and slug from the folder name, and
derives a human-readable title by reading the ``<h2>`` tag in the LeetSync
README.md (which always contains the exact LeetCode title).  The slug-based
fallback is retained for the rare case where no README is present.
"""

from __future__ import annotations

import re
from pathlib import Path

_FOLDER_RE = re.compile(r"^(\d+)-(.+)$")

# Extracts the problem title from the LeetSync README <h2> anchor:
#   <h2><a href="...">Two Sum</a></h2>
_TITLE_RE = re.compile(r"<h2[^>]*>\s*<a[^>]*>([^<]+)</a>", re.IGNORECASE)


def _parse_title_from_readme(problem_dir: Path) -> str | None:
    """Read the LeetSync README.md and return the exact problem title.

    LeetSync always writes the title inside the first ``<h2>`` anchor::

        <h2><a href="https://leetcode.com/problems/two-sum">Two Sum</a></h2>

    Returns the title string (e.g. ``"Two Sum"``) or ``None`` if the README
    is absent or does not contain the expected markup.
    """
    readme = problem_dir / "README.md"
    if not readme.is_file():
        return None
    m = _TITLE_RE.search(readme.read_text(errors="replace"))
    return m.group(1).strip() if m else None


def parse_problem_dir(problem_dir: Path) -> tuple[int, str, str]:
    """Extract (number, slug, title) from a LeetSync problem folder name.

    Title resolution order:
    1. ``<h2>`` anchor text in the LeetSync ``README.md`` (exact LeetCode title).
    2. ``slug_to_title(slug)`` as a fallback when no README is present.

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
    title = _parse_title_from_readme(problem_dir) or slug_to_title(slug)
    return number, slug, title


def slug_to_title(slug: str) -> str:
    """Convert a kebab-case slug to a title-cased string (fallback only).

    Examples:
        "two-sum"             → "Two Sum"
        "n-th-tribonacci-number" → "N Th Tribonacci Number"
        "01-matrix"           → "01 Matrix"
    """
    return " ".join(word.capitalize() for word in slug.split("-"))


def list_problem_files(problem_dir: Path) -> list[Path]:
    """Return all files inside a problem folder (solution + README + any extras).

    Only returns direct children — does not recurse deeper.
    """
    return [f for f in problem_dir.iterdir() if f.is_file()]


def get_last_modified(problem_dir: Path) -> float:
    """Return the most recent mtime across all files in the problem directory."""
    files = list_problem_files(problem_dir)
    if not files:
        return problem_dir.stat().st_mtime
    return max(f.stat().st_mtime for f in files)
