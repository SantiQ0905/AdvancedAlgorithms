# Analysis and Design of Advanced Algorithms 
# Group #607
# Team 3
# Dr. Katie Brodhead

# Santiago Quintana Moreno A01571222
# Miguel Ángel Álvarez Hermida A01722925

# ------ COIN CHANGE - TABULATION ------

def coin_change_ways(coins, change):
    
    n = len(coins) #Obtains the length of the array coins
    table = [[0 for _ in range(change + 1)] for _ in range(n + 1)] 
    #creates the matrix with n+1 rows and k+1 columns
    
    table[0][0] = 1 #Base case
    
    for i in range(1, n + 1): 
        #Runs through all coins in the table 
        for j in range(change + 1): 
            #Runs through all possible amounts (from 0 to the change amount)
        
            table[i][j] = table[i-1][j] 
            #Doesn't use the current coin to reach change amount
            
            
            if j >= coins[i-1]: 
                #Checks to see if the same coin can be used twice to reach change amount
                table[i][j] += table[i][j - coins[i-1]] 
                #Uses the current coin 
    
    return table[n][change] 
#Returns the number of possible combinations for the introduced scenario



def main():
    
    # Example 1
    coins = [1, 2, 5, 10, 20]
    change = 10
    print("Through Tabulation - Number of ways to make change for", change, "with coins", coins, "is:", coin_change_ways(coins, change))

    # Example 2
    coins = [1, 3, 4]
    change = 6
    print("Through Tabulation - Number of ways to make change for", change, "with coins", coins, "is:", coin_change_ways(coins, change))

    # Example 3
    coins = [2, 5, 7]
    change = 12
    print("Through Tabulation - Number of ways to make change for", change, "with coins", coins, "is:", coin_change_ways(coins, change))

    # Example 4
    coins = [1, 2]
    change = 5
    print("Through Tabulation - Number of ways to make change for", change, "with coins", coins, "is:", coin_change_ways(coins, change))
    
main()
