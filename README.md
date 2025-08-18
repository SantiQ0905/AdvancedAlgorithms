Here’s a ready-to-paste **`README.md`** for your repo that includes **Codespaces one-click**, plus instructions for **Knapsack**, **String Matching**, and **Closest Pair**.

```markdown
# Advanced Algorithms — Brute Force Suite

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/SantiQ0905/AdvancedAlgorithms?quickstart=1)

Brute-force reference implementations for three classic problems:

- **0/1 Knapsack (brute force via subset enumeration)**
- **String Matching (naive / brute force)**
- **Closest Pair of Points (naive O(n²))**

This repo is built for quick experimentation in **GitHub Codespaces** or locally.

---

## Repo layout

```

AdvancedAlgorithms/
└── BruteForce/
├── ClosestPair/
│   └── closest\_pair.py
├── Knapsack/
│   ├── knapsack.py
│   └── TestFiles/           # put .txt instances here (see format below)
└── StringMatching/
└── string\_match.py

````

> If your filenames differ, just adjust the commands below.

---

## Quickstart (one click via Codespaces)

1. Click this badge → **“Create codespace”**  
   [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/SantiQ0905/AdvancedAlgorithms?quickstart=1)

2. In the Codespaces terminal (already in the repo root), run any of the following:

```bash
# 0/1 Knapsack (reads all .txt files in BruteForce/Knapsack/TestFiles)
python BruteForce/Knapsack/knapsack.py

# String Matching (see usage below)
python BruteForce/StringMatching/string_match.py

# Closest Pair (see usage below)
python BruteForce/ClosestPair/closest_pair.py
````

> **Python:** tested with 3.10–3.12. Codespaces typically has a recent Python preinstalled.

---

## 0/1 Knapsack (Brute Force)

### What it does

Enumerates **every subset** of items and keeps the best value that does not exceed capacity.

* **Worst-case time:** `O(2^n · n)`
* **Worst-case space:** `O(n)`

### Input format (text files)

Place `.txt` files inside `BruteForce/Knapsack/TestFiles/`. Each file supports:

* Comments begin with `#`
* Comma **or** whitespace separated
* Either `capacity: NUMBER` **or** a single number at the top
* Each item is either:

  * `value weight`
  * `name value weight`

**Example** (`BruteForce/Knapsack/TestFiles/instance1.txt`)

```
# capacity can be header or first lone number
capacity: 50
items:
Camera, 325, 18
Laptop, 500, 28
Tripod, 90, 8
Water 30 3
Notebook 35 2
```

### Run

```bash
python BruteForce/Knapsack/knapsack.py
```

The script will:

* Discover all `.txt` files in `BruteForce/Knapsack/TestFiles/`
* Solve each, and print the **best value**, **weight**, and **chosen indices/items**

---

## String Matching (Naive / Brute Force)

### What it does

Slides the pattern over the text and checks character-by-character equality at each position.

* **Worst-case time:** `O(n · m)` (text length `n`, pattern length `m`)
* **Worst-case space:** `O(1)` besides outputs

### Usage examples

```bash
# Example 1: provide text & pattern via CLI args
python BruteForce/StringMatching/string_match.py --text "abracadabra" --pattern "abra"

# Example 2: read text from a file and pass pattern
python BruteForce/StringMatching/string_match.py --text_file ./some_text.txt --pattern "needle"
```

**Expected output**: starting indices where pattern occurs, e.g. `[0, 7]`.

---

## Closest Pair of Points (Naive)

### What it does

Computes the distance between **every pair** of points and returns the pair with minimal distance.

* **Worst-case time:** `O(n²)`
* **Worst-case space:** `O(1)` besides outputs

### Input options & usage

```bash
# Example 1: inline points (x1 y1 x2 y2 ...)
python BruteForce/ClosestPair/closest_pair.py --points "0 0  3 4  -1 2  4 4"

# Example 2: CSV/whitespace file with "x y" per line
python BruteForce/ClosestPair/closest_pair.py --points_file ./points.txt
```

**Expected output**:

* the minimum distance (float),
* the pair of points (or their indices),
* optionally the number of comparisons.

---

## Troubleshooting

* **“No .txt files found” (Knapsack):**
  Create `BruteForce/Knapsack/TestFiles/` and place one or more `.txt` instances there.

* **Windows path issues:**
  Prefer forward slashes `BruteForce/Knapsack/TestFiles/instance1.txt`.

* **Python not found in Codespaces:**
  Run `python --version`. If needed, try `python3` instead of `python`.

---

## Algorithm Notes (concise)

| Problem         | Approach                       | Time (worst) | Space (worst) |
| --------------- | ------------------------------ | ------------ | ------------- |
| 0/1 Knapsack    | Subset enumeration (bit masks) | `O(2^n · n)` | `O(n)`        |
| String Matching | Naive sliding compare          | `O(n · m)`   | `O(1)`        |
| Closest Pair    | All-pairs distances            | `O(n²)`      | `O(1)`        |

> These brute-force methods are **guaranteed correct** but become impractical at scale. They’re ideal for learning, small instances, and as baselines against more advanced algorithms (DP, divide & conquer, KMP, etc.).


```

If you want, I can also craft minimal **CLI wrappers** for your `string_match.py` and `closest_pair.py` (with `argparse`) to match the README usage exactly.
```
