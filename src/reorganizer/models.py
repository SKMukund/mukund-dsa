"""Data models shared across the reorganizer and tracker packages."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Problem:
    """Represents one LeetCode problem discovered from the raw LeetSync layout.

    Attributes:
        number:        LeetCode problem number (e.g. 1, 49, 200).
        slug:          Kebab-case slug as LeetSync generated it (e.g. "two-sum").
        title:         Human-readable title derived from the slug (e.g. "Two Sum").
        language:      Programming language folder the problem lives under (e.g. "python").
        topic:         Algorithmic topic folder (e.g. "arrays_and_hashing").
        source_dir:    Absolute path to the raw LeetSync problem folder.
        files:         All files inside source_dir (solution + README, etc.).
        last_modified: mtime of the most recently modified file in source_dir.
    """

    number: int
    slug: str
    title: str
    language: str
    topic: str
    source_dir: Path
    files: list[Path] = field(default_factory=list)
    last_modified: float = 0.0

    @property
    def folder_name(self) -> str:
        """Return the original LeetSync folder name, e.g. '1-two-sum'."""
        return self.source_dir.name

    def __repr__(self) -> str:
        return f"Problem({self.number}, {self.title!r}, lang={self.language}, topic={self.topic})"
