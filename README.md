# LeetCode Solutions

A complete log of my LeetCode practice, organized by language and algorithmic topic. Every problem I have solved is tracked here — this is a progress log, not a curated highlight reel.

## Purpose

This repository serves two goals simultaneously:

1. **Progress tracking** — every solution I write gets committed here, so I have a complete record of what I have worked through and when.
2. **Structured reference** — problems are organized by pattern so I can revisit related techniques together and spot gaps in my coverage.

---

## Structure

```
python/
├── arrays_and_hashing/       # Hash maps, frequency counting, prefix sums
├── two_pointers/             # Opposite-end and slow/fast pointer patterns
├── sliding_window/           # Fixed and variable-size window problems
├── stack/                    # Monotonic stack, bracket matching, RPN
├── binary_search/            # Search on sorted arrays and answer spaces
├── dynamic_programming/      # 1D/2D DP, memoization, tabulation
├── graphs/                   # BFS, DFS, flood fill, connected components
└── backtracking/             # Constraint-based search and pruning
```

Each problem lives in its own folder using the original LeetSync naming convention, e.g. `1-two-sum/`, containing:
- `two-sum.py` — the solution (LeetSync-generated filename)
- `README.md` — the original problem statement

---

## Progress

<!-- TRACKER_START -->
**46 problems solved** &nbsp;|&nbsp; Python &nbsp;|&nbsp; 18 Easy · 26 Medium · 2 Hard
*Last updated: 2026-04-13*

| Easy | Medium | Hard | Total |
|------|--------|------|-------|
| 18 | 26 | 2 | 46 |

### Problems by Topic

<details>
<summary><strong>Arrays & Hashing</strong> — 9 problems</summary>

| # | Problem | Difficulty |
|---|---------|------------|
| 0001 | Two Sum | Easy |
| 0049 | Group Anagrams | Medium |
| 0121 | Best Time to Buy and Sell Stock | Medium |
| 0164 | Maximum Gap | Hard |
| 0217 | Contains Duplicate | Easy |
| 0238 | Product of Array Except Self | Medium |
| 0242 | Valid Anagram | Easy |
| 0451 | Sort Characters by Frequency | Medium |
| 0837 | Most Common Word | Easy |

</details>

<details>
<summary><strong>Two Pointers</strong> — 6 problems</summary>

| # | Problem | Difficulty |
|---|---------|------------|
| 0011 | Container With Most Water | Medium |
| 0015 | 3Sum | Medium |
| 0026 | Remove Duplicates from Sorted Array | Easy |
| 0125 | Valid Palindrome | Easy |
| 0167 | Two Sum II - Input Array Is Sorted | Medium |
| 0874 | Backspace String Compare | Easy |

</details>

<details>
<summary><strong>Sliding Window</strong> — 7 problems</summary>

| # | Problem | Difficulty |
|---|---------|------------|
| 0003 | Longest Substring Without Repeating Characters | Medium |
| 0209 | Minimum Size Subarray Sum | Medium |
| 0567 | Permutation in String | Medium |
| 0643 | Maximum Average Subarray I | Easy |
| 0940 | Fruit Into Baskets | Medium |
| 1046 | Max Consecutive Ones III | Medium |
| 1586 | Longest Subarray of 1's After Deleting One Element | Medium |

</details>

<details>
<summary><strong>Stack</strong> — 5 problems</summary>

| # | Problem | Difficulty |
|---|---------|------------|
| 0020 | Valid Parentheses | Easy |
| 0084 | Largest Rectangle in Histogram | Hard |
| 0150 | Evaluate Reverse Polish Notation | Medium |
| 0496 | Next Greater Element I | Easy |
| 0739 | Daily Temperatures | Medium |

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
<summary><strong>Dynamic Programming</strong> — 8 problems</summary>

| # | Problem | Difficulty |
|---|---------|------------|
| 0005 | Longest Palindromic Substring | Medium |
| 0070 | Climbing Stairs | Easy |
| 0198 | House Robber | Medium |
| 0213 | House Robber II | Medium |
| 0322 | Coin Change | Medium |
| 0509 | Fibonacci Number | Easy |
| 0747 | Min Cost Climbing Stairs | Easy |
| 1236 | N-th Tribonacci Number | Easy |

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

### Recently Added

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 940 | Fruit Into Baskets | Sliding Window | Medium |
| 874 | Backspace String Compare | Two Pointers | Easy |
| 84 | Largest Rectangle in Histogram | Stack | Hard |
| 837 | Most Common Word | Arrays & Hashing | Easy |
| 79 | Word Search | Backtracking | Medium |

<!-- TRACKER_END -->

---

## Naming Convention

```
python/{topic}/{N}-{problem-name}/
    {problem-name}.py   # solution (LeetSync-generated)
    README.md           # problem statement (LeetSync-generated)
```

- Folder and file names preserve the original LeetSync format: `{number}-{kebab-case-name}`.
- Topic folders use `lowercase_snake_case` and are the only layer added on top of LeetSync output.
- New problems synced by LeetSync drop into the correct topic folder with no renaming needed.

---

## Notes

- Solutions are synced via [LeetSync](https://github.com/isamert/leetcode-sync) after each submission.
- All solutions are in Python 3.
- This is a living repository — new problems are added continuously.
- Git history is preserved across all renames; use `git log --follow <file>` to trace a file's full history.

---

## License

MIT
