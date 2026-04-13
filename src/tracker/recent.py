"""Determine recently added/modified problems."""

from __future__ import annotations

from src.reorganizer.models import Problem


def get_recent(problems: list[Problem], n: int = 5) -> list[Problem]:
    """Return the N most recently modified problems, newest first.

    "Recently modified" is determined by the mtime of the newest file
    inside each problem's source directory — populated by parse.get_last_modified().

    Args:
        problems: Full list of Problem objects.
        n:        How many recent problems to return.

    Returns:
        List of up to n Problems, sorted newest → oldest.
    """
    return sorted(problems, key=lambda p: p.last_modified, reverse=True)[:n]
