"""Shared formatting helpers for the tracker package."""

from __future__ import annotations

_DIFFICULTY_MAP: dict[int, str] = {
    # Easy
    1: "Easy", 20: "Easy", 26: "Easy", 35: "Easy", 69: "Easy", 70: "Easy",
    125: "Easy", 217: "Easy", 242: "Easy", 278: "Easy", 496: "Easy",
    509: "Easy", 643: "Easy", 733: "Easy", 747: "Easy", 837: "Easy",
    874: "Easy", 1236: "Easy",
    # Medium (add 34)
    34: "Medium",
    # Medium
    3: "Medium", 5: "Medium", 11: "Medium", 15: "Medium", 49: "Medium",
    121: "Medium", 150: "Medium", 153: "Medium", 167: "Medium", 198: "Medium",
    200: "Medium", 209: "Medium", 213: "Medium", 238: "Medium", 322: "Medium",
    451: "Medium", 542: "Medium", 567: "Medium", 695: "Medium", 739: "Medium",
    79: "Medium", 940: "Medium", 1036: "Medium", 1046: "Medium", 1586: "Medium",
    # Hard
    84: "Hard", 164: "Hard",
}


def get_difficulty(number: int) -> str:
    """Return the difficulty label for a problem number, or empty string if unknown."""
    return _DIFFICULTY_MAP.get(number, "")


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
        "binary_search": "Binary Search",
        "dynamic_programming": "Dynamic Programming",
        "graphs": "Graphs (BFS / DFS)",
        "backtracking": "Backtracking",
        "stack": "Stack",
        "uncategorized": "Uncategorized",
    }
    return replacements.get(topic_slug, topic_slug.replace("_", " ").title())


def language_display_name(lang: str) -> str:
    """Return a display label for a language folder name."""
    return {"python": "Python", "java": "Java", "cpp": "C++"}.get(lang, lang.capitalize())
