# LeetCode Solutions

A continuously maintained, automated log of LeetCode problems, organized by algorithmic patterns and backed by a custom tracking system.

This repository demonstrates consistency in problem-solving, structured learning across core algorithmic patterns, and practical engineering to manage large-scale interview preparation.

**54 problems solved across core algorithmic patterns (automatically tracked and updated).**

---

## Table of Contents

- [Purpose](#purpose)
- [Tracker](#tracker)
- [Progress](#progress)
- [Structure / Naming Convention](#structure--naming-convention)
- [Notes](#notes)
- [License](#license)

---

## Purpose

This repository serves two goals simultaneously:

1. **Progress tracking** — every solution is committed upon completion, providing a verifiable record of problems solved and topics covered over time.
2. **Structured reference** — problems are grouped by algorithmic pattern, making it straightforward to identify coverage gaps and revisit related techniques together.

The repository is intentionally comprehensive rather than curated: every problem solved is included.

This approach emphasizes consistency, pattern recognition, and long-term retention — key skills for technical interviews and real-world problem solving.

---

## Tracker

A GitHub Actions workflow triggers on every push to `main` and runs `scripts/run.py` in two phases:

1. **Relocate** — any `{N}-{slug}/` folder LeetSync dropped at the repo root is classified via `config/topics.json` and moved into `python/{topic}/` using `git mv`, preserving history.
2. **Track** — `python/` is scanned, statistics are recomputed, and this README is rewritten between the tracker markers.

To register a new problem, add its number to `config/topics.json` and `config/titles.json`. Problems not in the config are placed in `uncategorized` automatically.

---

## 📊 Progress

<!-- TRACKER_START -->
**54 problems solved** (Python)  
**Difficulty:** 22 Easy · 31 Medium · 1 Hard  
**Last updated:** 2026-04-20

| Easy | Medium | Hard | Total |
|------|--------|------|-------|
| 22 | 31 | 1 | 54 |

### Problems by Topic

<details>
<summary><strong>Arrays & Hashing</strong> — 8 problems</summary>

| # | Problem | Difficulty |
|---|---------|------------|
| 0001 | Two Sum | Easy |
| 0013 | Roman to Integer | Easy |
| 0049 | Group Anagrams | Medium |
| 0164 | Maximum Gap | Medium |
| 0217 | Contains Duplicate | Easy |
| 0242 | Valid Anagram | Easy |
| 0451 | Sort Characters By Frequency | Medium |
| 0837 | Most Common Word | Easy |

</details>

<details>
<summary><strong>Two Pointers</strong> — 7 problems</summary>

| # | Problem | Difficulty |
|---|---------|------------|
| 0005 | Longest Palindromic Substring | Medium |
| 0011 | Container With Most Water | Medium |
| 0015 | 3Sum | Medium |
| 0026 | Remove Duplicates from Sorted Array | Easy |
| 0125 | Valid Palindrome | Easy |
| 0167 | Two Sum II - Input Array Is Sorted | Medium |
| 0283 | Move Zeroes | Easy |

</details>

<details>
<summary><strong>Sliding Window</strong> — 8 problems</summary>

| # | Problem | Difficulty |
|---|---------|------------|
| 0003 | Longest Substring Without Repeating Characters | Medium |
| 0121 | Best Time to Buy and Sell Stock | Easy |
| 0209 | Minimum Size Subarray Sum | Medium |
| 0567 | Permutation in String | Medium |
| 0643 | Maximum Average Subarray I | Easy |
| 0940 | Fruit Into Baskets | Medium |
| 1046 | Max Consecutive Ones III | Medium |
| 1586 | Longest Subarray of 1's After Deleting One Element | Medium |

</details>

<details>
<summary><strong>Stack</strong> — 6 problems</summary>

| # | Problem | Difficulty |
|---|---------|------------|
| 0020 | Valid Parentheses | Easy |
| 0084 | Largest Rectangle in Histogram | Hard |
| 0150 | Evaluate Reverse Polish Notation | Medium |
| 0496 | Next Greater Element I | Easy |
| 0739 | Daily Temperatures | Medium |
| 0874 | Backspace String Compare | Easy |

</details>

<details>
<summary><strong>Binary Search</strong> — 5 problems</summary>

| # | Problem | Difficulty |
|---|---------|------------|
| 0034 | Find First and Last Position of Element in Sorted Array | Medium |
| 0035 | Search Insert Position | Easy |
| 0069 | Sqrt(x) | Easy |
| 0153 | Find Minimum in Rotated Sorted Array | Medium |
| 0278 | First Bad Version | Easy |

</details>

<details>
<summary><strong>Linked List</strong> — 1 problem</summary>

| # | Problem | Difficulty |
|---|---------|------------|
| 0002 | Add Two Numbers | Medium |

</details>

<details>
<summary><strong>Graphs (BFS / DFS)</strong> — 5 problems</summary>

| # | Problem | Difficulty |
|---|---------|------------|
| 0200 | Number of Islands | Medium |
| 0542 | 01 Matrix | Medium |
| 0695 | Max Area of Island | Medium |
| 0733 | Flood Fill | Easy |
| 1036 | Rotting Oranges | Medium |

</details>

<details>
<summary><strong>Backtracking</strong> — 1 problem</summary>

| # | Problem | Difficulty |
|---|---------|------------|
| 0079 | Word Search | Medium |

</details>

<details>
<summary><strong>Dynamic Programming</strong> — 7 problems</summary>

| # | Problem | Difficulty |
|---|---------|------------|
| 0070 | Climbing Stairs | Easy |
| 0198 | House Robber | Medium |
| 0213 | House Robber II | Medium |
| 0322 | Coin Change | Medium |
| 0509 | Fibonacci Number | Easy |
| 0747 | Min Cost Climbing Stairs | Easy |
| 1236 | N-th Tribonacci Number | Easy |

</details>

<details>
<summary><strong>Greedy</strong> — 2 problems</summary>

| # | Problem | Difficulty |
|---|---------|------------|
| 0055 | Jump Game | Medium |
| 0134 | Gas Station | Medium |

</details>

<details>
<summary><strong>Intervals</strong> — 1 problem</summary>

| # | Problem | Difficulty |
|---|---------|------------|
| 0435 | Non-overlapping Intervals | Medium |

</details>

<details>
<summary><strong>Prefix Sum</strong> — 1 problem</summary>

| # | Problem | Difficulty |
|---|---------|------------|
| 0238 | Product of Array Except Self | Medium |

</details>

<details>
<summary><strong>Uncategorized</strong> — 2 problems</summary>

| # | Problem | Difficulty |
|---|---------|------------|
| 0452 | Minimum Number of Arrows to Burst Balloons | Medium |
| 0890 | Lemonade Change | Easy |

</details>

### Recently Added

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 452 | Minimum Number of Arrows to Burst Balloons | Uncategorized | Medium |
| 5 | Longest Palindromic Substring | Two Pointers | Medium |
| 283 | Move Zeroes | Two Pointers | Easy |
| 26 | Remove Duplicates from Sorted Array | Two Pointers | Easy |
| 167 | Two Sum II - Input Array Is Sorted | Two Pointers | Medium |

<!-- TRACKER_END -->

---

## 🧠 Structure / Naming Convention

Raw solution files are generated by [LeetSync](https://github.com/isamert/leetcode-sync) and are never modified or renamed. This preserves consistency with the original problem source and maintains a reliable history of submissions.

Solutions are organized by algorithmic topic at the directory level, providing a structured view without altering the underlying files.

**Directory layout:**

```
python/
├── arrays_and_hashing/       # Hash maps, frequency counting, anagrams
├── two_pointers/             # Opposite-end and slow/fast pointer patterns
├── sliding_window/           # Fixed and variable-size window problems
├── stack/                    # Monotonic stack, bracket matching, RPN
├── binary_search/            # Search on sorted arrays and answer spaces
├── linked_list/              # Traversal, reversal, cycle detection
├── trees/                    # Binary trees, BST, DFS/BFS on trees
├── heap/                     # Priority queues, top-K problems
├── graphs/                   # BFS, DFS, flood fill, connected components
├── backtracking/             # Constraint-based search and pruning
├── dynamic_programming/      # 1D/2D DP, memoization, tabulation
├── greedy/                   # Locally optimal choices, scheduling
├── intervals/                # Merge, insert, overlap detection
└── prefix_sum/               # Cumulative sums, range queries
```

Each problem lives in its own folder using the original LeetSync naming convention, e.g. `2-add-two-numbers/`, containing:
- `add-two-numbers.py` — the solution (LeetSync-generated filename, never renamed)
- `README.md` — the original problem statement (LeetSync-generated)

**Per-problem folder:**

```
python/{topic}/{N}-{problem-name}/
    {problem-name}.py   # solution (LeetSync name preserved)
    README.md           # problem statement (LeetSync generated)
```

**Key design principles:**
- Non-destructive: raw LeetSync files are never renamed, moved, or overwritten
- Organized by topic for pattern-based learning and coverage tracking
- Fully automated via GitHub Actions — no manual steps after submission

---

## ⚙️ Notes

- **Automation** — a GitHub Actions workflow (`sync.yml`) triggers on every push to `python/**`. It runs `scripts/run.py`, which scans all solution folders, recomputes statistics, and rewrites the Progress section of this README between the tracker markers.
- **Idempotent updates** — the script produces identical output on repeated runs. If the README is already current, no commit is made.
- **Non-destructive design** — raw LeetSync files and folders are never moved, renamed, or overwritten. The automation only writes to `README.md` and (optionally) a separate `organized/` output directory.
- **History preservation** — git history is maintained across all file moves. Use `git log --follow <file>` to trace a file's complete history.
- **Language** — all current solutions are written in Python 3.

---

## License

MIT
