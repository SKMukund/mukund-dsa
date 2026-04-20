"""Heuristic classifier that infers an algorithmic category from solution code.

When a problem is absent from ``config/topics.json`` and has no valid folder
fallback, this module reads the Python solution file and scores its content
against a table of code-pattern signals.  The category with the highest score
(above a minimum threshold) is returned.

Scoring weights
---------------
* **3 — strong**: a keyword or structural pattern that almost exclusively
  appears in one category (e.g. ``heapq``, ``ListNode``, ``@cache``).
* **2 — medium**: a pattern that is characteristic but could occasionally
  appear in neighbouring categories.
* **1 — weak**: an auxiliary cue that nudges the score without being decisive
  on its own.

Minimum score to classify: ``MIN_SCORE = 2`` (at least one medium or two weak
signals must fire before a category is assigned).

Tie-breaking
------------
When two categories have the same score, the one with the higher inherent
priority in ``_SIGNAL_TABLE`` (i.e. the more specific category) wins.  This
means specialised patterns (heap, linked_list, trees) beat more general ones
(arrays_and_hashing, greedy) when evidence is ambiguous.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

# Minimum cumulative score required to make a classification.
MIN_SCORE = 2

# Canonical category set.
VALID_TOPICS: frozenset[str] = frozenset({
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
})

# ---------------------------------------------------------------------------
# Signal table
# ---------------------------------------------------------------------------
# Each entry is (category, [(regex_pattern_string, weight), ...]).
# Patterns are compiled once at module load with re.MULTILINE so that ^ / $
# anchors work per-line.  re.IGNORECASE is intentionally NOT set for most
# patterns so that ``ListNode`` and ``listnode`` are distinguished.
# ---------------------------------------------------------------------------
_RAW_SIGNALS: list[tuple[str, list[tuple[str, int]]]] = [
    # ── Linked list ─────────────────────────────────────────────────────────
    ("linked_list", [
        (r"\bListNode\b", 3),
        (r"\bself\.next\b", 3),
        (r"\b(?:curr|current|prev|node)\.next\b", 2),
        (r"\.next\s*=", 2),
    ]),

    # ── Trees ────────────────────────────────────────────────────────────────
    ("trees", [
        (r"\bTreeNode\b", 3),
        (r"\broot\.(?:left|right)\b", 3),
        (r"\bnode\.(?:left|right)\b", 2),
        (r"\b(?:inorder|preorder|postorder|levelorder|level_order)\b", 2),
        (r"\bbst\b", 2),
    ]),

    # ── Heap ─────────────────────────────────────────────────────────────────
    ("heap", [
        (r"\bheapq\b", 3),
        (r"\bheap(?:push|pop|ify|pushpop|replace)\b", 3),
    ]),

    # ── Binary search ────────────────────────────────────────────────────────
    ("binary_search", [
        (r"\bbisect(?:_left|_right)?\b", 3),
        # Classic mid calculation with full names
        (r"\bmid\s*=\s*\(?(?:left|lo)\s*\+\s*(?:right|hi)\b", 3),
        (r"\bmid\s*=\s*(?:left|lo)\s*\+\s*\((?:right|hi)", 3),
        # Loop conditions with full names
        (r"\bwhile\s+(?:left|lo)\s*<=\s*(?:right|hi)\b", 3),
    ]),

    # ── Graphs ───────────────────────────────────────────────────────────────
    ("graphs", [
        (r"\bvisited\s*=\s*(?:set|dict)\s*\(\)", 3),
        (r"\badj(?:acent|acency)?\b", 3),
        (r"\bgraph\s*=\s*(?:defaultdict|dict|\{|\[)", 2),
        (r"\bdirections\s*=\s*\[", 2),
        (r"\bqueue\s*=\s*(?:collections\.)?deque\b", 2),
        # BFS/DFS in comments or docstrings — only weight 1 because function
        # names like `def dfs` appear in backtracking problems too.
        (r"\b(?:BFS|DFS)\b", 1),
        (r"\bdeque\b", 1),
    ]),

    # ── Dynamic programming ──────────────────────────────────────────────────
    ("dynamic_programming", [
        (r"@(?:cache|lru_cache)\b", 3),
        (r"\bfunctools\.(?:cache|lru_cache)\b", 3),
        (r"\bdp\s*=\s*\[", 3),
        (r"\bdp\[", 2),
        (r"\bmemo\s*=\s*\{", 2),
        (r"\bmemo\b", 1),
    ]),

    # ── Backtracking ─────────────────────────────────────────────────────────
    ("backtracking", [
        (r"\bdef\s+backtrack\b", 3),
        (r"\bbacktrack\s*\(", 2),
        (r"\bpath\.(?:append|pop)\b", 2),
        (r"\b(?:res|result)\.append\s*\(\s*path\[:\]\s*\)", 3),
        (r"\b(?:permutations?|combinations?)\b", 1),
        # In-place cell marking & restore — canonical board backtracking
        (r"""board\[.*\]\s*=\s*["']#["']""", 3),
        (r"\btemp\s*=\s*board\b", 2),
    ]),

    # ── Stack ────────────────────────────────────────────────────────────────
    # Patterns cover both plain `stack` and named variants like `stack_s`,
    # `stack_t`, `left_stack`, etc.
    ("stack", [
        (r"\b\w*[Ss]tack\w*\s*=\s*\[\]", 3),           # any *stack* = []
        (r"\b\w*[Ss]tack\w*\.(?:append|pop)\b", 2),     # push / pop
        (r"\b\w*[Ss]tack\w*\[-1\]", 2),                 # peek at top
        (r"\bmonotonic\b", 2),
    ]),

    # ── Intervals ────────────────────────────────────────────────────────────
    ("intervals", [
        (r"\bintervals\b", 2),
        (r"\bend\s*=\s*max\s*\(\s*end\s*,", 3),
        (r"\.sort\s*\(\s*key\s*=\s*lambda\s+\w+\s*:\s*\w+\[0\]\)", 2),
    ]),

    # ── Prefix sum ───────────────────────────────────────────────────────────
    # Covers both array-based (prefix[i] = ...) and scalar running-product/sum
    # accumulation (prefix *= ..., suffix *= ...).
    ("prefix_sum", [
        (r"\bprefix(?:_sums?|es?)?\s*=\s*\[", 3),       # prefix array init
        (r"\bprefix\[", 2),                              # array indexing
        (r"\bpresum\b", 3),
        (r"\brunning_sum\b", 3),
        (r"\bcumulative\b", 2),
        # Scalar running-product/sum (e.g. product-except-self)
        (r"\bprefix\s*[*+]=\s*\S", 2),                  # prefix *= / prefix +=
        (r"\bsuffix\s*[*+]=\s*\S", 2),                  # suffix *= / suffix +=
    ]),

    # ── Sliding window ───────────────────────────────────────────────────────
    ("sliding_window", [
        (r"\bwindow\b", 2),
        (r"\bmax_(?:len|length)\b", 2),
        (r"\bmin_(?:len|length)\b", 2),
        (r"\bchar_(?:count|freq)\b", 2),
        (r"\bCounter\s*\(\s*(?:s|t|word|string|text)\b", 2),
        (r"\bshrink\b", 2),
    ]),

    # ── Two pointers ─────────────────────────────────────────────────────────
    # Covers both full names (left/right) and single-letter (l/r) variants,
    # plus the expand-around-center pattern used in palindrome problems.
    ("two_pointers", [
        # Slow / fast pointers
        (r"\bslow\b", 2),
        (r"\bfast\b", 2),
        # Convergence loops — full names
        (r"\bwhile\s+left\s*<\s*right\b", 2),
        # Array access at both ends — full names
        (r"\bnums\[left\]", 2),
        (r"\bnums\[right\]", 2),
        # Symmetric steps — full names
        (r"\bright\s*-=\s*1", 1),
        (r"\bleft\s*\+=\s*1", 1),
        # ── Short-form l / r variants ────────────────────────────────────────
        # Expand-around-center (palindrome problems)
        (r"\bdef\s+expand\b", 3),
        # Classic l/r convergence loop
        (r"\bwhile\s+l\s*<\s*r\b", 2),
        # Weak lone cues (only useful when combined with others)
        (r"\bl\s*=\s*0\b", 1),
        (r"\br\s*=\s*\d+\b", 1),
    ]),

    # ── Greedy ───────────────────────────────────────────────────────────────
    ("greedy", [
        (r"\bmax_reach\b", 3),
        (r"\btank\b", 2),
        (r"\blocal_(?:max|min)\b", 2),
        (r"\bglobal_(?:max|min)\b", 1),
    ]),

    # ── Arrays and hashing (most general — checked last) ────────────────────
    ("arrays_and_hashing", [
        (r"\bCounter\s*\(", 3),
        (r"\bdefaultdict\s*\(", 2),
        (r"\b(?:char|num|index|val)_map\b", 2),
        (r"\bseen\s*=\s*(?:set|dict)\s*\(\)", 2),
        (r"\bfreq(?:uency)?\s*=\s*(?:\{|Counter|defaultdict)", 2),
        (r"\bcount\s*=\s*\{", 1),
    ]),
]

# Compile all patterns once at import time.
_SIGNAL_TABLE: list[tuple[str, list[tuple[re.Pattern[str], int]]]] = [
    (cat, [(re.compile(pat, re.MULTILINE), w) for pat, w in sigs])
    for cat, sigs in _RAW_SIGNALS
]

# Tie-break priority: earlier in _RAW_SIGNALS → higher priority (more specific).
_PRIORITY: dict[str, int] = {cat: i for i, (cat, _) in enumerate(_RAW_SIGNALS)}


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------

@dataclass
class ClassificationResult:
    """Outcome of a code-based classification attempt.

    Attributes:
        category:   Winning category slug, or ``None`` if classification failed.
        confidence: "high" | "medium" | "low" | "" (empty when category is None).
        scores:     Raw score per category (only non-zero categories included).
        signals:    List of ``(category, pattern_string)`` for every match.
        reason:     Human-readable explanation of the outcome.
    """
    category: str | None
    confidence: str = ""          # "high" | "medium" | "low"
    scores: dict[str, int] = field(default_factory=dict)
    signals: list[tuple[str, str]] = field(default_factory=list)
    reason: str = ""


# ---------------------------------------------------------------------------
# Classifier
# ---------------------------------------------------------------------------

class CodeClassifier:
    """Infer an algorithmic category from a problem's Python solution code."""

    def classify(self, problem_dir: Path) -> ClassificationResult:
        """Analyse the solution file in *problem_dir* and return a result.

        Args:
            problem_dir: Path to the LeetSync problem folder (e.g. ``1-two-sum/``).

        Returns:
            A :class:`ClassificationResult`.  ``category`` is ``None`` if
            classification was inconclusive.
        """
        code = _read_solution(problem_dir)
        if code is None:
            return ClassificationResult(
                category=None,
                scores={},
                reason="no Python solution file found",
            )
        if not code.strip():
            return ClassificationResult(
                category=None,
                scores={},
                reason="solution file is empty",
            )

        scores: dict[str, int] = {}
        strong_hits: dict[str, int] = {}   # weight-3 signal count per category
        signals: list[tuple[str, str]] = []

        for category, patterns in _SIGNAL_TABLE:
            for compiled, weight in patterns:
                if compiled.search(code):
                    scores[category] = scores.get(category, 0) + weight
                    signals.append((category, compiled.pattern))
                    if weight == 3:
                        strong_hits[category] = strong_hits.get(category, 0) + 1

        if not scores:
            return ClassificationResult(
                category=None,
                reason="no signals detected in code",
            )

        # Sort: highest score first; break ties by category priority (most
        # specific category wins).
        ranked = sorted(
            scores.items(),
            key=lambda kv: (-kv[1], _PRIORITY.get(kv[0], 999)),
        )
        best_cat, best_score = ranked[0]

        if best_score < MIN_SCORE:
            return ClassificationResult(
                category=None,
                scores=scores,
                signals=signals,
                reason=(
                    f"best score {best_score} for '{best_cat}' is below "
                    f"minimum threshold {MIN_SCORE}"
                ),
            )

        confidence = _compute_confidence(best_score, strong_hits.get(best_cat, 0))

        return ClassificationResult(
            category=best_cat,
            confidence=confidence,
            scores=scores,
            signals=signals,
            reason="classified by code analysis",
        )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _compute_confidence(score: int, strong_hit_count: int) -> str:
    """Map a category score + strong-signal count to a confidence label.

    High:   score ≥ 6 AND at least 2 weight-3 signals fired.
    Medium: score ≥ 3 (but not high).
    Low:    score < 3 (just meets MIN_SCORE=2 — weak or ambiguous signals).
    """
    if score >= 6 and strong_hit_count >= 2:
        return "high"
    if score >= 3:
        return "medium"
    return "low"


def _read_solution(problem_dir: Path) -> str | None:
    """Return the content of the Python solution file, or ``None`` if absent."""
    if not problem_dir.is_dir():
        return None

    py_files = sorted(
        f for f in problem_dir.iterdir()
        if f.is_file() and f.suffix == ".py" and f.name != "__init__.py"
    )
    if not py_files:
        return None

    # Prefer a file whose stem matches the folder slug.
    folder_slug = problem_dir.name.split("-", 1)[1] if "-" in problem_dir.name else ""
    for f in py_files:
        if f.stem == folder_slug:
            return f.read_text(errors="replace")

    return py_files[0].read_text(errors="replace")
