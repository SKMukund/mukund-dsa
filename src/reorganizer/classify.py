"""Classify a problem into its algorithmic topic.

Lookup order
------------
1. **Config** (``config/topics.json``): authoritative override keyed by the
   LeetSync folder name, e.g. ``"1-two-sum"``.  If an entry exists here it is
   always used — no further checks.
2. **Code analysis** (``CodeClassifier``): when a ``problem_dir`` is supplied
   *and* the config has no entry, the Python solution file is inspected for
   algorithmic signals.  A successful result is automatically written back to
   ``topics.json`` so future runs use the config path (step 1) and the file
   grows as a permanent record.
3. **Folder-layout fallback**: the topic already inferred from where the file
   lives (e.g. ``python/dynamic_programming/`` → ``"dynamic_programming"``).
4. **Default**: ``"uncategorized"`` as a last resort, with a log line explaining
   why classification was inconclusive.

Auto-update behaviour
---------------------
When the code classifier successfully classifies a *new* problem (one not
already present in ``topics.json``), the inferred topic is stored in the
in-memory map and the ``_dirty`` flag is set.  Call :meth:`save` after all
problems have been processed to flush the updated map to disk in one write.

Key format
----------
``topics.json`` uses ``"{number}-{slug}"`` (the LeetSync folder name) as its
key — the same format as ``config/difficulty_map.json``.  This makes the file
human-readable without needing a separate number-to-slug lookup.
"""

from __future__ import annotations

import json
from pathlib import Path

from src.reorganizer.code_classifier import CodeClassifier

_DEFAULT_TOPIC = "uncategorized"

# Instantiate once at module level; it holds no mutable state.
_code_classifier = CodeClassifier()


def _sort_key(folder_name: str) -> int:
    """Sort key that orders folder names numerically by problem number."""
    try:
        return int(folder_name.split("-")[0])
    except (ValueError, IndexError):
        return 999_999


class TopicClassifier:
    """Load a topic map and resolve folder names to topic slugs.

    The backing file (``config/topics.json``) uses LeetSync folder names as
    keys, e.g.::

        {
          "1-two-sum": "arrays_and_hashing",
          "2-add-two-numbers": "linked_list"
        }
    """

    def __init__(self, config_path: Path) -> None:
        """
        Args:
            config_path: Path to ``config/topics.json``.
        """
        self._path = config_path
        self._map: dict[str, str] = {}   # folder_name → topic
        self._dirty = False

        if config_path.exists():
            raw = json.loads(config_path.read_text())
            self._map = dict(raw)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def classify(
        self,
        folder_name: str,
        fallback_topic: str | None = None,
        problem_dir: Path | None = None,
        verbose: bool = False,
    ) -> str:
        """Return the topic slug for *folder_name*.

        Args:
            folder_name:    LeetSync folder name, e.g. ``"1-two-sum"``.
            fallback_topic: Topic inferred from the current folder layout.
                            Ignored when it equals ``"uncategorized"`` or is
                            ``None``.
            problem_dir:    Path to the problem folder.  When supplied *and*
                            the config has no entry, the code classifier is
                            attempted before falling back.
            verbose:        Print per-problem signal details.

        Returns:
            A topic slug such as ``"linked_list"`` or ``"uncategorized"``.
        """
        # ── 1. Config (authoritative) ──────────────────────────────────────
        if folder_name in self._map:
            return self._map[folder_name]

        # ── 2. Code analysis ───────────────────────────────────────────────
        # Only attempt when we would otherwise fall back to "uncategorized".
        if problem_dir is not None and (
            fallback_topic is None or fallback_topic == _DEFAULT_TOPIC
        ):
            result = _code_classifier.classify(problem_dir)

            if result.category:
                # Auto-write to topics.json so it becomes permanent.
                self._map[folder_name] = result.category
                self._dirty = True

                detected = [sig for cat, sig in result.signals if cat == result.category]
                if verbose:
                    print(
                        f"  [classify] {folder_name} → {result.category} "
                        f"(score={result.scores.get(result.category, 0)}, "
                        f"signals={detected})"
                    )
                else:
                    print(f"  [classify] {folder_name} → {result.category}")
                return result.category

            # Code analysis was inconclusive — log why.
            print(
                f"  [classify] {folder_name} → inconclusive "
                f"({result.reason}); falling back to '{_DEFAULT_TOPIC}'"
            )

        # ── 3. Folder-layout fallback ──────────────────────────────────────
        if fallback_topic and fallback_topic != _DEFAULT_TOPIC:
            return fallback_topic

        # ── 4. Default ────────────────────────────────────────────────────
        return _DEFAULT_TOPIC

    def is_dirty(self) -> bool:
        """Return True if the map has unsaved changes."""
        return self._dirty

    def save(self) -> None:
        """Write the map back to ``topics.json``, sorted by problem number."""
        sorted_map = dict(
            sorted(self._map.items(), key=lambda kv: _sort_key(kv[0]))
        )
        self._path.write_text(json.dumps(sorted_map, indent=2) + "\n")
        self._dirty = False

    def all_topics(self) -> list[str]:
        """Return all unique topics defined in the config, sorted."""
        return sorted(set(self._map.values()))
