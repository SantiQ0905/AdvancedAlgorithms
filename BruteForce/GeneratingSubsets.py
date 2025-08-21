# Analysis and Design of Advanced Algorithms 
# Group #607
# Team 6
# Dr. Katie Brodhead

# Santiago Quintana Moreno A01571222
# Miguel Ángel Álvarez Hermida A01722925

# ------ GENERATING SUBSETS ------

def generate_subsets(n):
    """Generate all subsets of {1, 2, ..., n}."""
    subsets = []
    for mask in range(1 << n):  # 2^n possible subsets
        subset = []
        for i in range(n):
            if mask & (1 << i):  # check if i-th element is included
                subset.append(i + 1)
        subsets.append(subset)
    return subsets


def main():
    print("=== Subset Generator ===")
    n = int(input("Enter a number n (size of the set {1..n}): "))
    subsets = generate_subsets(n)
    
    print(f"\nSubsets of {{1, 2, ..., {n}}}:")
    for s in subsets:
        print(s)


if __name__ == "__main__":
    main()


# Complexity:
# Time (worst-case): O(2^n * n)
#   - There are 2^n subsets; for each mask we may inspect up to n bits and append up to n items.
# Space (worst-case): O(2^n * n) as written
#   - Because we collect and return a list containing all subsets; if instead we streamed/printed subsets,
#     auxiliary space could be O(n) (size of one subset) ignoring output.
