# Analysis and Design of Advanced Algorithms 
# Group #607
# Team 6
# Dr. Katie Brodhead

# Santiago Quintana Moreno A01571222
# Miguel Ángel Álvarez Hermida A01722925

# ------ QUICKSELECT GCD ------

import random

# Module implementing the QuickSelect algorithm to find the k-th smallest element in an unsorted list.
# The worst-case time complexity of the QuickSelect algorithm is O(n^2), which occurs when the pivot selection results 
# in highly unbalanced partitions (e.g., always picking the smallest or largest element as the pivot). However, with 
# random pivot selection, the expected time complexity is O(n).

def quickselect(arr, k):
    # Finds and returns the k-th smallest element (0-based index) in the input list `arr` using the QuickSelect algorithm.
    # The function uses a randomized pivot selection to partition the array into elements less than, equal to, and greater
    # than the pivot.

    if len(arr) == 1:
        return arr[0]
    
    pivot = random.choice(arr)
    lows = [el for el in arr if el < pivot]
    highs = [el for el in arr if el > pivot]
    pivots = [el for el in arr if el == pivot]

    if k < len(lows):
        return quickselect(lows, k)
    elif k < len(lows) + len(pivots):
        return pivots[0]
    else:
        return quickselect(highs, k - len(lows) - len(pivots))

# Example usage:
if __name__ == "__main__":
    arr = [7, 10, 4, 3, 20, 15]
    k = 2  # Find the 3rd smallest element (0-based index)
    print(f"{k+1}-th smallest element is {quickselect(arr, k)}")

