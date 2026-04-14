"""Generate the organized/ output directory.

This module COPIES files from the raw LeetSync layout into a clean
organized/{language}/{topic}/{folder}/ structure.

CRITICAL: it never moves, renames, or modifies any source files.
The organized/ directory is a generated view — delete and regenerate at any time.

Output structure (LeetSync names are preserved verbatim):

    organized/
      python/
        arrays_and_hashing/
          1-two-sum/
            two-sum.py
            README.md
        two_pointers/
          ...
"""

from __future__ import annotations

import shutil
from pathlib import Path

from src.reorganizer.models import Problem


def generate_organized(
    problems: list[Problem],
    output_root: Path,
    clean: bool = False,
    verbose: bool = False,
) -> list[Path]:
    """Copy all problem files into the organized output directory.

    Args:
        problems:    List of classified Problem objects.
        output_root: Root of the organized/ directory (created if absent).
        clean:       If True, wipe output_root before regenerating.
                     Useful for CI; leave False for incremental local runs.

    Returns:
        List of destination directories that were written (one per problem).
    """
    if clean and output_root.exists():
        shutil.rmtree(output_root)

    output_root.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    for problem in problems:
        dest_dir = _dest_for(problem, output_root)
        dest_dir.mkdir(parents=True, exist_ok=True)

        for src_file in problem.files:
            dest_file = dest_dir / src_file.name  # preserve original filename
            shutil.copy2(src_file, dest_file)     # copy2 preserves metadata

        if verbose:
            print(f"  [generate] #{problem.number:>4} → {dest_dir.relative_to(output_root.parent)}")

        written.append(dest_dir)

    return written


def _dest_for(problem: Problem, output_root: Path) -> Path:
    """Build the destination path for a problem's folder inside organized/.

    Example:
        organized/python/arrays_and_hashing/1-two-sum/
    """
    return output_root / problem.language / problem.topic / problem.folder_name
