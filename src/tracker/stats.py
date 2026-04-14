"""Compute statistics from a list of Problem objects."""

from __future__ import annotations

from collections import defaultdict

from src.reorganizer.models import Problem
from src.tracker.utils import get_difficulty

# Topics in the order they are typically studied (used for display ordering).
TOPIC_STUDY_ORDER = [
    "arrays_and_hashing",
    "two_pointers",
    "sliding_window",
    "stack",
    "binary_search",
    "linked_list",
    "trees",
    "heap",
    "graphs",
    "backtracking",
    "dynamic_programming",
    "greedy",
    "intervals",
    "prefix_sum",
    "uncategorized",
]


def compute_stats(problems: list[Problem]) -> dict:
    """Return a stats dict suitable for rendering into the README tracker.

    Returns:
        {
            "total": int,
            "by_language": {"python": 46, ...},
            "by_difficulty": {"Easy": 17, "Medium": 27, "Hard": 2, "": 0},
            "by_topic": OrderedDict following TOPIC_STUDY_ORDER,
                        value is list[Problem] sorted by number
        }
    """
    by_language: dict[str, int] = defaultdict(int)
    by_difficulty: dict[str, int] = defaultdict(int)
    by_topic: dict[str, list[Problem]] = defaultdict(list)

    for p in problems:
        by_language[p.language] += 1
        diff = get_difficulty(p.number)
        by_difficulty[diff] += 1
        by_topic[p.topic].append(p)

    # Sort problems within each topic by number
    for topic_list in by_topic.values():
        topic_list.sort(key=lambda p: p.number)

    # Order topics by study progression; unknown topics go at the end alphabetically
    known = [t for t in TOPIC_STUDY_ORDER if t in by_topic]
    unknown = sorted(t for t in by_topic if t not in TOPIC_STUDY_ORDER)
    ordered_topics = {t: by_topic[t] for t in known + unknown}

    return {
        "total": len(problems),
        "by_language": dict(sorted(by_language.items())),
        "by_difficulty": dict(by_difficulty),
        "by_topic": ordered_topics,
    }
