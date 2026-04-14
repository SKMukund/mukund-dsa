"""Move root-level LeetSync problem folders into python/{topic}/.

LeetSync pushes new submissions to the repository root by default:
    {N}-{slug}/

This module moves them into the organized structure using `git mv`,
so git history is preserved across the relocation.

Design rules:
- Never rename files or folders — only change their location.
- Skip any folder that already exists at the destination (idempotent).
- Create the topic directory if it does not yet exist.
- Use git mv so the move appears in git history.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

_PROBLEM_RE = re.compile(r"^\d+-")
_SKIP_DIRS = frozenset({
    "python", "java", "cpp", "javascript", "typescript",
    "organized", "src", "config", "scripts", ".github",
    ".git", ".venv", "venv", "env", "node_modules", "dist", "build",
})


def find_root_problem_dirs(repo_root: Path) -> list[Path]:
    """Return all LeetSync-style problem folders sitting at the repo root.

    Matches folders whose names begin with digits followed by a dash,
    e.g. ``2-add-two-numbers``, ``994-rotting-oranges``.
    """
    return sorted(
        d for d in repo_root.iterdir()
        if d.is_dir()
        and d.name not in _SKIP_DIRS
        and not d.name.startswith(".")
        and _PROBLEM_RE.match(d.name)
    )


def move_root_problem(
    repo_root: Path,
    problem_dir: Path,
    topic: str,
    verbose: bool = False,
) -> Path | None:
    """Move a root-level problem folder into python/{topic}/ using git mv.

    Args:
        repo_root:    Absolute path to the repository root.
        problem_dir:  Absolute path to the folder at repo root.
        topic:        Target topic slug (e.g. "linked_list").
        verbose:      Print what is happening.

    Returns:
        Destination Path if moved, None if skipped or errored.
    """
    dest_topic_dir = repo_root / "python" / topic
    dest_dir = dest_topic_dir / problem_dir.name

    if dest_dir.exists():
        if verbose:
            print(f"  [skip]  {problem_dir.name} already at python/{topic}/ — nothing to do")
        return None

    if not problem_dir.exists():
        if verbose:
            print(f"  [skip]  {problem_dir.name} — source no longer exists")
        return None

    # Create the topic directory so git mv has a valid destination.
    dest_topic_dir.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        ["git", "mv", problem_dir.name, str(dest_dir.relative_to(repo_root))],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"  [error] git mv failed for {problem_dir.name}: {result.stderr.strip()}")
        return None

    if verbose:
        print(f"  [moved] {problem_dir.name} → python/{topic}/{problem_dir.name}")

    return dest_dir