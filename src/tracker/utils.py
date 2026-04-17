"""Shared formatting helpers and difficulty management for the tracker package."""

from __future__ import annotations

import json
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# Difficulty map
# ---------------------------------------------------------------------------

# Matches the difficulty badge that LeetSync embeds in each problem's README.md:
#   <img src='...badge/Difficulty-Easy-brightgreen' alt='Difficulty: Easy' />
_DIFFICULTY_BADGE_RE = re.compile(
    r"""alt=['"]Difficulty:\s*(Easy|Medium|Hard)['"]""",
    re.IGNORECASE,
)


class DifficultyMap:
    """File-backed mapping from problem folder names to difficulty labels.

    The backing file is ``config/difficulty_map.json``.  It maps
    ``"{number}-{slug}"`` keys (the LeetSync folder name) to
    ``"Easy"`` / ``"Medium"`` / ``"Hard"`` values.

    The file is auto-updated whenever the pipeline encounters a problem whose
    difficulty has not yet been recorded — no manual edits needed.

    Example entry::

        "1-two-sum": "Easy"
    """

    def __init__(self, config_path: Path) -> None:
        """Load the map from *config_path*, or start empty if absent.

        Args:
            config_path: Path to ``config/difficulty_map.json``.
        """
        self._path = config_path
        self._map: dict[str, str] = {}
        if config_path.exists():
            raw = config_path.read_text()
            self._map = json.loads(raw) if raw.strip() else {}
        self._dirty = False

    # ------------------------------------------------------------------
    # Querying
    # ------------------------------------------------------------------

    def get(self, folder_name: str) -> str:
        """Return the difficulty for *folder_name*, or ``""`` if unknown.

        Args:
            folder_name: LeetSync folder name, e.g. ``"1-two-sum"``.
        """
        return self._map.get(folder_name, "")

    def __len__(self) -> int:
        return len(self._map)

    # ------------------------------------------------------------------
    # Updating
    # ------------------------------------------------------------------

    def ingest(self, folder_name: str, problem_dir: Path) -> bool:
        """Parse difficulty from *problem_dir*/README.md and store it.

        Does nothing if *folder_name* is already in the map (existing entries
        are never overwritten, keeping manual edits safe).

        Args:
            folder_name:  LeetSync folder name, e.g. ``"1-two-sum"``.
            problem_dir:  Absolute path to the problem folder.

        Returns:
            True if the map was modified (a new entry was added).
        """
        if folder_name in self._map:
            return False
        diff = _parse_difficulty(problem_dir)
        if diff:
            self._map[folder_name] = diff
            self._dirty = True
            return True
        return False

    def is_dirty(self) -> bool:
        """Return True if the map has unsaved changes."""
        return self._dirty

    def save(self) -> None:
        """Write the map to disk, sorted by key for stable diffs."""
        self._path.write_text(
            json.dumps(self._map, indent=2, sort_keys=True) + "\n"
        )
        self._dirty = False


# ---------------------------------------------------------------------------
# README badge parser
# ---------------------------------------------------------------------------

def _parse_difficulty(problem_dir: Path) -> str | None:
    """Extract the difficulty label from the LeetSync README.md badge.

    LeetSync generates a badge line like::

        <img src='https://img.shields.io/badge/Difficulty-Easy-brightgreen'
             alt='Difficulty: Easy' />

    Args:
        problem_dir: Path to the problem folder.

    Returns:
        ``"Easy"``, ``"Medium"``, ``"Hard"``, or ``None`` if no badge found.
    """
    readme = problem_dir / "README.md"
    if not readme.is_file():
        return None
    content = readme.read_text(errors="replace")
    m = _DIFFICULTY_BADGE_RE.search(content)
    return m.group(1).capitalize() if m else None


# ---------------------------------------------------------------------------
# Display name helpers (unchanged)
# ---------------------------------------------------------------------------

def topic_display_name(topic_slug: str) -> str:
    """Convert a topic slug to a display-friendly heading.

    Example:
        "arrays_and_hashing" → "Arrays & Hashing"
        "two_pointers"       → "Two Pointers"
    """
    replacements = {
        "arrays_and_hashing": "Arrays & Hashing",
        "two_pointers": "Two Pointers",
        "sliding_window": "Sliding Window",
        "stack": "Stack",
        "binary_search": "Binary Search",
        "linked_list": "Linked List",
        "trees": "Trees",
        "heap": "Heap / Priority Queue",
        "graphs": "Graphs (BFS / DFS)",
        "backtracking": "Backtracking",
        "dynamic_programming": "Dynamic Programming",
        "greedy": "Greedy",
        "intervals": "Intervals",
        "prefix_sum": "Prefix Sum",
        "uncategorized": "Uncategorized",
    }
    return replacements.get(topic_slug, topic_slug.replace("_", " ").title())


def language_display_name(lang: str) -> str:
    """Return a display label for a language folder name."""
    return {"python": "Python", "java": "Java", "cpp": "C++"}.get(lang, lang.capitalize())
