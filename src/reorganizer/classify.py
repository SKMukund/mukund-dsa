"""Classify a problem into its algorithmic topic.

The primary classification mechanism is a config file (``config/topics.json``)
that maps problem numbers to topic slugs.  This keeps the logic data-driven
and trivially extensible — no heuristics that can silently mis-classify.

For problems not present in the config, the topic is read directly from the
folder layout (because the raw files already live in ``python/{topic}/``).
If that also fails, the problem is placed in ``"uncategorized"``.
"""

from __future__ import annotations

import json
from pathlib import Path

_DEFAULT_TOPIC = "uncategorized"


class TopicClassifier:
    """Load a topic map and resolve problem numbers to topic slugs."""

    def __init__(self, config_path: Path) -> None:
        """
        Args:
            config_path: Path to ``config/topics.json``.
        """
        self._map: dict[int, str] = {}
        if config_path.exists():
            raw = json.loads(config_path.read_text())
            # Keys in JSON must be strings; convert to int for lookups.
            self._map = {int(k): v for k, v in raw.items()}

    def classify(self, number: int, fallback_topic: str | None = None) -> str:
        """Return the topic slug for a problem number.

        Lookup order:
        1. ``config/topics.json`` (authoritative override)
        2. ``fallback_topic`` — the topic already inferred from the folder layout
        3. ``"uncategorized"``
        """
        if number in self._map:
            return self._map[number]
        if fallback_topic:
            return fallback_topic
        return _DEFAULT_TOPIC

    def all_topics(self) -> list[str]:
        """Return all unique topics defined in the config, sorted."""
        return sorted(set(self._map.values()))
