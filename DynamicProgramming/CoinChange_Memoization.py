# Analysis and Design of Advanced Algorithms 
# Group #607
# Team 3
# Dr. Katie Brodhead

# Santiago Quintana Moreno A01571222
# Miguel Ángel Álvarez Hermida A01722925

# ------ COIN CHANGE - MEMOIZATION ------

from typing import List

def coin_change_memo(coins: List[int], K: int) -> int:
    # Filter out non-positive coin values
    coins = [c for c in coins if c > 0]
    n = len(coins)
    # Initialize memoization table with -1
    T = [[-1] * (K + 1) for _ in range(n + 1)]

    def ways(i: int, amount: int) -> int:
        # Base case: exact change made
        if amount == 0:
            T[i][amount] = 1
            return 1
        # Base case: no coins left or negative amount
        if i <= 0 or amount < 0:
            return 0

        # Return cached result if available
        if T[i][amount] != -1:
            return T[i][amount]

        # Include current coin
        include = ways(i, amount - coins[i - 1])
        # Exclude current coin
        exclude = ways(i - 1, amount)

        # Store result in memoization table
        T[i][amount] = include + exclude
        return T[i][amount]

    # Start recursion with all coins and target amount
    return ways(n, K)


if __name__ == "__main__":
    # Example 1
    coins = [1, 2, 5, 10]
    K = 17
    print("Through Memoization - Number of ways to make change for", K, "with coins", coins, "is:", coin_change_memo(coins, K))
    
    # Example 2
    coins2 = [2, 3, 7]
    K2 = 12
    print("Through Memoization - Number of ways to make change for", K2, "with coins", coins2, "is:", coin_change_memo(coins2, K2))

    # Example 3
    coins3 = [1, 5, 10, 25]
    K3 = 30
    print("Through Memoization - Number of ways to make change for", K3, "with coins", coins3, "is:", coin_change_memo(coins3, K3))

    # Example 4
    coins4 = [3, 4, 6]
    K4 = 8
    print("Through Memoization - Number of ways to make change for", K4, "with coins", coins4, "is:", coin_change_memo(coins4, K4))