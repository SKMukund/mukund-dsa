"""Inject a tracker block into README.md between marker comments.

The README must contain (or will have added) these two marker lines:
    <!-- TRACKER_START -->
    <!-- TRACKER_END -->

Everything between the markers is replaced on each run.
Content outside the markers is never touched.

If the markers are absent, a new ## Progress Tracker section with the
markers is appended before the first ## heading that follows the intro,
or at the end of the file if no suitable insertion point is found.
"""

from __future__ import annotations

import datetime
import re
from zoneinfo import ZoneInfo

_PST = ZoneInfo("America/Los_Angeles")
from pathlib import Path

from src.reorganizer.models import Problem
from src.tracker.recent import get_recent
from src.tracker.stats import compute_stats
from src.tracker.utils import DifficultyMap, language_display_name, topic_display_name

MARKER_START = "<!-- TRACKER_START -->"
MARKER_END = "<!-- TRACKER_END -->"

_DIFFICULTY_ORDER = ["Easy", "Medium", "Hard"]


def update_readme(
    readme_path: Path,
    problems: list[Problem],
    difficulty_map: DifficultyMap,
    recent_n: int = 5,
) -> bool:
    """Rewrite the tracker section of README.md.

    Also updates the problem count in the introduction line if present,
    keeping it consistent with the tracker total without requiring manual edits.

    Args:
        readme_path:    Path to the README.md file.
        problems:       Full list of Problem objects.
        difficulty_map: Loaded DifficultyMap for resolving per-problem difficulty.
        recent_n:       Number of recent problems to list.

    Returns:
        True if the file was changed, False if it was already up-to-date.
    """
    original = readme_path.read_text()
    total = len(problems)

    text = _ensure_markers(original)
    tracker_block = _render_tracker(problems, difficulty_map, recent_n)
    text = _inject(text, tracker_block)
    text = _update_intro_count(text, total)

    if text == original:
        return False

    readme_path.write_text(text)
    return True


# ---------------------------------------------------------------------------
# Introduction count
# ---------------------------------------------------------------------------

# Matches the dynamic count line in the introduction, e.g.:
#   **46 problems solved across core algorithmic patterns (automatically tracked and updated).**
_INTRO_COUNT_RE = re.compile(
    r"\*\*\d+ problems solved across core algorithmic patterns"
)


def _update_intro_count(readme: str, total: int) -> str:
    """Replace the problem count in the introduction line with the current total.

    Only touches lines matching the introduction count pattern — never modifies
    anything inside the tracker markers or any other section.
    """
    return _INTRO_COUNT_RE.sub(
        f"**{total} problems solved across core algorithmic patterns",
        readme,
    )


# ---------------------------------------------------------------------------
# Marker management
# ---------------------------------------------------------------------------

def _ensure_markers(readme: str) -> str:
    """Return the readme with markers guaranteed to be present.

    If both markers already exist, return unchanged.
    If either is missing, append a clean ## Progress Tracker section.
    """
    has_start = MARKER_START in readme
    has_end = MARKER_END in readme

    if has_start and has_end:
        return readme

    # Strip any orphaned marker so we start clean
    text = readme.replace(MARKER_START, "").replace(MARKER_END, "").rstrip()

    new_section = (
        "\n\n---\n\n"
        "## Progress Tracker\n\n"
        f"{MARKER_START}\n"
        f"{MARKER_END}\n"
    )
    return text + new_section


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def _render_tracker(
    problems: list[Problem],
    difficulty_map: DifficultyMap,
    recent_n: int,
) -> str:
    """Build the full tracker markdown block (content between the markers)."""
    stats = compute_stats(problems, difficulty_map)
    recent = get_recent(problems, n=recent_n)
    now = datetime.datetime.now(_PST).strftime("%Y-%m-%d")

    lines: list[str] = []

    # ── Summary headline ──────────────────────────────────────────────────
    langs = " · ".join(language_display_name(l) for l in stats["by_language"])
    diff = stats["by_difficulty"]
    diff_parts = [
        f"{diff.get(d, 0)} {d}"
        for d in _DIFFICULTY_ORDER
        if diff.get(d, 0) > 0
    ]
    diff_str = " · ".join(diff_parts)

    lines.append(f"**{stats['total']} problems solved** ({langs})  ")
    lines.append(f"**Difficulty:** {diff_str}  ")
    lines.append(f"**Last updated:** {now}")
    lines.append("")

    # ── Difficulty breakdown table ────────────────────────────────────────
    lines.append("| Easy | Medium | Hard | Total |")
    lines.append("|------|--------|------|-------|")
    easy = diff.get("Easy", 0)
    medium = diff.get("Medium", 0)
    hard = diff.get("Hard", 0)
    lines.append(f"| {easy} | {medium} | {hard} | {stats['total']} |")
    lines.append("")

    # ── Per-topic tables ──────────────────────────────────────────────────
    lines.append("### Problems by Topic")
    lines.append("")

    for topic_slug, topic_problems in stats["by_topic"].items():
        display = topic_display_name(topic_slug)
        count = len(topic_problems)
        lines.append(f"<details>")
        lines.append(f"<summary><strong>{display}</strong> — {count} problem{'s' if count != 1 else ''}</summary>")
        lines.append("")
        lines.append("| # | Problem | Difficulty |")
        lines.append("|---|---------|------------|")
        for p in topic_problems:
            num_str = str(p.number).zfill(4)
            diff_label = difficulty_map.get(p.folder_name)
            lines.append(f"| {num_str} | {p.title} | {diff_label} |")
        lines.append("")
        lines.append("</details>")
        lines.append("")

    # ── Recently added ────────────────────────────────────────────────────
    lines.append("### Recently Added")
    lines.append("")
    lines.append("| # | Problem | Topic | Difficulty |")
    lines.append("|---|---------|-------|------------|")
    for p in recent:
        diff_label = difficulty_map.get(p.folder_name)
        lines.append(
            f"| {p.number} | {p.title} | {topic_display_name(p.topic)} | {diff_label} |"
        )
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Marker injection
# ---------------------------------------------------------------------------

def _inject(readme: str, block: str) -> str:
    """Replace content between TRACKER_START and TRACKER_END markers."""
    start_idx = readme.find(MARKER_START)
    end_idx = readme.find(MARKER_END)

    if start_idx == -1 or end_idx == -1:
        raise ValueError(
            f"README is missing tracker markers. "
            f"Call _ensure_markers() before _inject()."
        )
    if start_idx > end_idx:
        raise ValueError("TRACKER_START appears after TRACKER_END in README.")

    before = readme[: start_idx + len(MARKER_START)]
    after = readme[end_idx:]

    return f"{before}\n{block}\n{after}"
