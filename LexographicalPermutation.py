# Analysis and Design of Advanced Algorithms 
# Group #607
# Team 6
# Dr. Katie Brodhead

# Santiago Quintana Moreno A01571222
# Miguel Ángel Álvarez Hermida A01722925

# ------ LEXICOGRAPHICAL PERMUTATION ------

def next_permutation(seq):
    """Generate the next lexicographic permutation of seq in-place.
    Returns False if it was the last permutation, True otherwise.
    """
    # Step 1: Find the longest non-increasing suffix
    i = len(seq) - 2
    while i >= 0 and seq[i] >= seq[i + 1]:
        i -= 1
    if i == -1:
        return False  # Last permutation reached

    # Step 2: Find the rightmost successor to pivot
    j = len(seq) - 1
    while seq[j] <= seq[i]:
        j -= 1

    # Step 3: Swap pivot with successor
    seq[i], seq[j] = seq[j], seq[i]

    # Step 4: Reverse suffix
    seq[i + 1:] = reversed(seq[i + 1:])
    return True


def generate_permutations(word):
    """Generate all permutations of the given word in lexicographic order."""
    seq = sorted(word)  # start with sorted version
    print("".join(seq))
    while next_permutation(seq):
        print("".join(seq))


def main():
    print("=== Permutations in Lexicographic Order ===")
    word = input("Enter a string (e.g., 'ABC'): ").strip()
    print(f"\nPermutations of '{word}' in lexicographic order:")
    generate_permutations(word)


if __name__ == "__main__":
    main()


# Complexity:
# Time (worst-case): O(n! * n)
#   - There are n! permutations; each "next_permutation" step is O(n) (finding pivot, successor, and reversing suffix),
#     and we also spend O(n) to print/join the sequence. Asymptotically O(n! * n).
# Space (worst-case): O(n)
#   - The permutation is stored in-place (size n). Ignoring output size (n! lines), auxiliary space is O(n).
