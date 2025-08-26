from typing import List

def coin_change_memo(coins: List[int], K: int) -> int:
    coins = [c for c in coins if c > 0]
    n = len(coins)
    T = [[-1] * (K + 1) for _ in range(n + 1)]

    def ways(i: int, amount: int) -> int:
        if amount == 0:
            T[i][amount] = 1
            return 1
        if i <= 0 or amount < 0:
            return 0

        if T[i][amount] != -1:
            return T[i][amount]

        include = ways(i, amount - coins[i - 1])
        exclude = ways(i - 1, amount)

        T[i][amount] = include + exclude
        return T[i][amount]

    return ways(n, K)


if __name__ == "__main__":
    coins = [1, 2, 5, 10]
    K = 17
    print("Number of ways to make change for", K, "with coins", coins, "is:", coin_change_memo(coins, K))
