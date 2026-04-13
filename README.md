# LeetCode Solutions

A complete log of my LeetCode practice, organized by language and algorithmic topic. Every problem I have solved is tracked here — this is a progress log, not a curated highlight reel.

**46 problems solved** | Python | Ongoing

---

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

Each problem lives in its own folder named `XXXX_problem_name/` containing:
- `XXXX_problem_name.py` — the solution
- `README.md` — the original problem statement

---

## Problems by Topic

### Arrays & Hashing — 9 problems
| # | Problem | Difficulty |
|---|---------|------------|
| 0001 | Two Sum | Easy |
| 0049 | Group Anagrams | Medium |
| 0121 | Best Time to Buy and Sell Stock | Easy |
| 0164 | Maximum Gap | Hard |
| 0217 | Contains Duplicate | Easy |
| 0238 | Product of Array Except Self | Medium |
| 0242 | Valid Anagram | Easy |
| 0451 | Sort Characters by Frequency | Medium |
| 0837 | Most Common Word | Easy |

### Two Pointers — 6 problems
| # | Problem | Difficulty |
|---|---------|------------|
| 0011 | Container With Most Water | Medium |
| 0015 | 3Sum | Medium |
| 0026 | Remove Duplicates from Sorted Array | Easy |
| 0125 | Valid Palindrome | Easy |
| 0167 | Two Sum II - Input Array Is Sorted | Medium |
| 0874 | Backspace String Compare | Easy |

### Sliding Window — 7 problems
| # | Problem | Difficulty |
|---|---------|------------|
| 0003 | Longest Substring Without Repeating Characters | Medium |
| 0209 | Minimum Size Subarray Sum | Medium |
| 0567 | Permutation in String | Medium |
| 0643 | Maximum Average Subarray I | Easy |
| 0940 | Fruit Into Baskets | Medium |
| 1046 | Max Consecutive Ones III | Medium |
| 1586 | Longest Subarray of 1's After Deleting One Element | Medium |

### Stack — 5 problems
| # | Problem | Difficulty |
|---|---------|------------|
| 0020 | Valid Parentheses | Easy |
| 0084 | Largest Rectangle in Histogram | Hard |
| 0150 | Evaluate Reverse Polish Notation | Medium |
| 0496 | Next Greater Element I | Easy |
| 0739 | Daily Temperatures | Medium |

### Binary Search — 5 problems
| # | Problem | Difficulty |
|---|---------|------------|
| 0034 | Find First and Last Position of Element in Sorted Array | Medium |
| 0035 | Search Insert Position | Easy |
| 0069 | Sqrt(x) | Easy |
| 0153 | Find Minimum in Rotated Sorted Array | Medium |
| 0278 | First Bad Version | Easy |

### Dynamic Programming — 8 problems
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

### Graphs (BFS / DFS) — 5 problems
| # | Problem | Difficulty |
|---|---------|------------|
| 0200 | Number of Islands | Medium |
| 0542 | 01 Matrix | Medium |
| 0695 | Max Area of Island | Medium |
| 0733 | Flood Fill | Easy |
| 1036 | Rotting Oranges | Medium |

### Backtracking — 1 problem
| # | Problem | Difficulty |
|---|---------|------------|
| 0079 | Word Search | Medium |

---

## Naming Convention

```
python/{topic}/XXXX_problem_name/
    XXXX_problem_name.py   # solution
    README.md              # problem statement
```

- Problem numbers are zero-padded to 4 digits for consistent sorting.
- Folder and file names use `lowercase_snake_case`.
- Topics map to standard interview-prep categories (Blind 75 / NeetCode style).

---

## Notes

- Solutions are synced via [LeetSync](https://github.com/isamert/leetcode-sync) after each submission.
- All solutions are in Python 3.
- This is a living repository — new problems are added continuously.
- Git history is preserved across all renames; use `git log --follow <file>` to trace a file's full history.

---

## License

MIT
