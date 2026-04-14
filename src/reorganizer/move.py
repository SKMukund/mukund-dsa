"""Move unorganized LeetSync problem folders into python/{topic}/.

LeetSync can drop new submissions in two places:
    {repo_root}/{N}-{slug}/          ← repo root (LeetSync default)
    {repo_root}/LeetCode/{N}-{slug}/ ← LeetCode/ subfolder (alternate config)

This module discovers both locations and moves found folders into
python/{topic}/ using `git mv`, preserving history.

Design rules:
- Never rename files or folders — only change their location.
- Skip any folder already at the correct destination (idempotent).
- Create the topic directory if it does not yet exist.
- Use git mv so moves appear in git history.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

_PROBLEM_RE = re.compile(r"^\d+-")

# Directories at repo root that are never LeetSync problem folders.
_ROOT_SKIP_DIRS = frozenset({
    "python", "java", "cpp", "javascript", "typescript",
    "LeetCode",
    "organized", "src", "config", "scripts", ".github",
    ".git", ".venv", "venv", "env", "node_modules", "dist", "build",
})


def find_unorganized_problem_dirs(repo_root: Path) -> list[Path]:
    """Return all unorganized LeetSync problem folders.

    Scans two locations:
    - Repo root: {repo_root}/{N}-{slug}/
    - LeetCode subfolder: {repo_root}/LeetCode/{N}-{slug}/

    Returns a flat sorted list of matching directories.
    """
    found: list[Path] = []

    # ── Repo root ──────────────────────────────────────────────────────────
    for d in sorted(repo_root.iterdir()):
        if (
            d.is_dir()
            and d.name not in _ROOT_SKIP_DIRS
            and not d.name.startswith(".")
            and _PROBLEM_RE.match(d.name)
        ):
            found.append(d)

    # ── LeetCode/ subfolder ────────────────────────────────────────────────
    leetcode_dir = repo_root / "LeetCode"
    if leetcode_dir.is_dir():
        for d in sorted(leetcode_dir.iterdir()):
            if d.is_dir() and _PROBLEM_RE.match(d.name):
                found.append(d)

    return found


def move_problem(
    repo_root: Path,
    problem_dir: Path,
    topic: str,
    verbose: bool = False,
) -> Path | None:
    """Move a problem folder into python/{topic}/ using git mv.

    Works for folders at the repo root OR inside LeetCode/.

    Args:
        repo_root:    Absolute path to the repository root.
        problem_dir:  Absolute path to the problem folder (root or LeetCode/).
        topic:        Target topic slug (e.g. "linked_list").
        verbose:      Print what is happening.

    Returns:
        Destination Path if moved, None if skipped or errored.
    """
    dest_topic_dir = repo_root / "python" / topic
    dest_dir = dest_topic_dir / problem_dir.name

    if dest_dir.exists():
        if verbose:
            src_rel = problem_dir.relative_to(repo_root)
            print(f"  [skip]  {src_rel} already at python/{topic}/ — nothing to do")
        return None

    if not problem_dir.exists():
        if verbose:
            print(f"  [skip]  {problem_dir.name} — source no longer exists")
        return None

    # Create the topic directory so git mv has a valid destination.
    dest_topic_dir.mkdir(parents=True, exist_ok=True)

    # git mv needs paths relative to the repo root.
    src_rel = str(problem_dir.relative_to(repo_root))
    dst_rel = str(dest_dir.relative_to(repo_root))

    result = subprocess.run(
        ["git", "mv", src_rel, dst_rel],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"  [error] git mv failed for {src_rel}: {result.stderr.strip()}")
        return None

    if verbose:
        print(f"  [moved] {src_rel} → {dst_rel}")

    return dest_dir
