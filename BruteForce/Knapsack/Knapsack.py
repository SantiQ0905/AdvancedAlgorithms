import os

# -----------------------------------------------------------------------------
# Brute-force 0/1 Knapsack using subset enumeration (bit masks).
#
# Worst-case time complexity: O(2^n * n)
#   - Enumerates all 2^n subsets; for each subset we may inspect up to n items.
# Worst-case auxiliary space complexity: O(n)
#   - To store the best set of indices (output) and a few counters.
#
# Inputs:
#   values  : list of item values
#   weights : list of item weights
#   capacity: maximum allowed weight
#
# Outputs:
#   (best_value, best_indices)
# -----------------------------------------------------------------------------
def brute_force_knapsack(values, weights, capacity):
    if len(values) != len(weights):
        raise ValueError("values and weights must have the same length")
    if capacity < 0:
        raise ValueError("capacity must be non-negative")

    n = len(values)
    best_value = 0
    best_indices = []

    for mask in range(1 << n):  # iterate all subsets
        total_w = 0
        total_v = 0
        chosen = []

        for i in range(n):
            if mask & (1 << i):  # include item i
                total_w += weights[i]
                if total_w > capacity:   # skip overweight
                    break
                total_v += values[i]
                chosen.append(i)

        if total_w <= capacity and total_v > best_value:
            best_value = total_v
            best_indices = chosen

    return best_value, best_indices


# -----------------------------------------------------------------------------
# Utilities to load knapsack instances from a text file
# -----------------------------------------------------------------------------
def _coerce_int(s):
    """Convert string to int if possible, else float→int if whole number."""
    try:
        return int(s)
    except ValueError:
        f = float(s)
        if f.is_integer():
            return int(f)
        raise ValueError("Invalid number: " + s)

def load_knapsack_from_file(path):
    """
    Parse a knapsack instance file.
    Supports:
      - Lines starting with '#' are ignored.
      - Comma- or space-separated fields.
      - Item lines can be:
          value weight
          name value weight
      - First non-comment line must specify 'capacity:' or a number.
    Returns: (capacity, values, weights, names_or_None)
    """
    capacity = None
    values = []
    weights = []
    names = []

    in_items_section = False

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue

            lower = line.lower()
            if lower.startswith("capacity"):
                _, _, rhs = line.partition(":")
                capacity = _coerce_int(rhs.strip())
                continue
            if lower.startswith("items"):
                in_items_section = True
                continue

            parts = [p.strip() for p in (line.split(",") if "," in line else line.split())]
            if not parts:
                continue

            if capacity is None and not in_items_section:
                # if first line is just a number, treat as capacity
                if len(parts) == 1:
                    capacity = _coerce_int(parts[0])
                    continue
                else:
                    raise ValueError("Capacity must be specified at the start of file.")

            # item line
            if len(parts) == 2:
                v, w = _coerce_int(parts[0]), _coerce_int(parts[1])
                values.append(v)
                weights.append(w)
            elif len(parts) >= 3:
                v, w = _coerce_int(parts[-2]), _coerce_int(parts[-1])
                name = " ".join(parts[:-2])
                values.append(v)
                weights.append(w)
                names.append(name)
            else:
                raise ValueError("Bad line in file: " + line)

    if capacity is None:
        raise ValueError("No capacity found in file " + path)
    if len(values) != len(weights):
        raise ValueError("Mismatch of values and weights count in " + path)

    if names and len(names) != len(values):
        names = []

    return capacity, values, weights, (names if names else None)


def solve_file(path):
    """Load a file, run brute-force knapsack, and print results."""
    capacity, values, weights, names = load_knapsack_from_file(path)
    best_value, best_idx = brute_force_knapsack(values, weights, capacity)
    best_weight = sum(weights[i] for i in best_idx)

    print(f"\n===== {os.path.basename(path)} =====")
    print(f"Capacity: {capacity}")
    print(f"Items: {len(values)}")
    print(f"Best value: {best_value}")
    print(f"Best weight: {best_weight}")
    print("Chosen indices:", best_idx)
    if names:
        print("Chosen items (name, value, weight):")
        for i in best_idx:
            print(f"  - {names[i]} | {values[i]} | {weights[i]}")
    else:
        print("Chosen items (value, weight):")
        for i in best_idx:
            print(f"  - {values[i]} | {weights[i]}")


if __name__ == "__main__":
    ROOT = "BruteForce\Knapsack\TestFiles"

    if not os.path.isdir(ROOT):
        raise SystemExit(f"Directory not found: {ROOT}")

    files = sorted(
        os.path.join(ROOT, f) for f in os.listdir(ROOT)
        if f.lower().endswith(".txt")
    )

    if not files:
        raise SystemExit(f"No .txt files found in {ROOT}")

    print(f"Found {len(files)} file(s). Running brute-force knapsack...")
    for p in files:
        try:
            solve_file(p)
        except Exception as e:
            print(f"\n[ERROR] {os.path.basename(p)}: {e}")
