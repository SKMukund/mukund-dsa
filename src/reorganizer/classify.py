"""Classify a problem into its algorithmic topic.

Lookup order
------------
1. **Config** (``config/topics.json``): authoritative override keyed by problem
   number.  If a mapping exists here it is always used, no further checks.
2. **Code analysis** (``CodeClassifier``): when a ``problem_dir`` is supplied
   *and* the config has no entry, the Python solution file is inspected for
   algorithmic signals (data structures, variable names, patterns).  This step
   fires only when the folder-layout fallback would produce ``"uncategorized"``.
3. **Folder-layout fallback**: the topic already inferred from where the file
   lives (e.g. ``python/dynamic_programming/`` → ``"dynamic_programming"``).
4. **Default**: ``"uncategorized"`` as a last resort, accompanied by a log line
   that explains why classification was inconclusive.
"""

from __future__ import annotations

import json
from pathlib import Path

from src.reorganizer.code_classifier import CodeClassifier

_DEFAULT_TOPIC = "uncategorized"

# Instantiate once; it carries no mutable state.
_code_classifier = CodeClassifier()


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

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def classify(
        self,
        number: int,
        fallback_topic: str | None = None,
        problem_dir: Path | None = None,
        verbose: bool = False,
    ) -> str:
        """Return the topic slug for a problem number.

        Args:
            number:         LeetCode problem number.
            fallback_topic: Topic inferred from the current folder layout,
                            e.g. ``"dynamic_programming"``.  Ignored when it
                            equals ``"uncategorized"`` or is ``None``.
            problem_dir:    Path to the problem folder.  When supplied *and*
                            the result would otherwise be ``"uncategorized"``,
                            the code classifier is attempted first.
            verbose:        Print per-problem signal details.

        Returns:
            A topic slug such as ``"linked_list"`` or ``"uncategorized"``.
        """
        # ── 1. Config (authoritative) ──────────────────────────────────────
        if number in self._map:
            return self._map[number]

        # ── 2. Code analysis ───────────────────────────────────────────────
        # Only attempt when we would otherwise fall back to "uncategorized".
        if problem_dir is not None and (
            fallback_topic is None or fallback_topic == _DEFAULT_TOPIC
        ):
            result = _code_classifier.classify(problem_dir)

            if result.category:
                detected = [sig for cat, sig in result.signals if cat == result.category]
                if verbose:
                    print(
                        f"  [classify] #{number} → {result.category} "
                        f"(score={result.scores.get(result.category, 0)}, "
                        f"signals={detected})"
                    )
                else:
                    print(
                        f"  [classify] #{number} {problem_dir.name} → "
                        f"{result.category}"
                    )
                return result.category

            # Code analysis failed — log why and fall through.
            print(
                f"  [classify] #{number} {problem_dir.name} → inconclusive "
                f"({result.reason}); falling back to '{_DEFAULT_TOPIC}'"
            )

        # ── 3. Folder-layout fallback ──────────────────────────────────────
        if fallback_topic and fallback_topic != _DEFAULT_TOPIC:
            return fallback_topic

        # ── 4. Default ────────────────────────────────────────────────────
        return _DEFAULT_TOPIC

    def all_topics(self) -> list[str]:
        """Return all unique topics defined in the config, sorted."""
        return sorted(set(self._map.values()))
