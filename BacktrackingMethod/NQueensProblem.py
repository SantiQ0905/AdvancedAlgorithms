# Analysis and Design of Advanced Algorithms 
# Group #607
# Team 3
# Luis Salomón Flores Ugalde 

# Santiago Quintana Moreno A01571222
# Miguel Ángel Álvarez Hermida A01722925

# ------ N-QUEENS PROBLEM - BACKTRACKING ALGORITHMS ------

# Total Complexity: O(n!) time, O(n) space - dominated by the depth of the recursion stack

class NQueensBacktracking:
    def __init__(self, n):
        # Initialize the N-Queens solver
        self.n = n
        self.board = [[0 for _ in range(n)] for _ in range(n)]
        self.solutions = []
        
    def is_safe(self, row, col):
        # Check if it's safe to place a queen at position (row, col)

        for j in range(col):
            if self.board[row][j] == 1:
                return False
        
        i, j = row, col
        while i >= 0 and j >= 0:
            if self.board[i][j] == 1:
                return False
            i -= 1
            j -= 1
        
        i, j = row, col
        while i < self.n and j >= 0:
            if self.board[i][j] == 1:
                return False
            i += 1
            j -= 1
        
        return True
    
    def solve_nqueens_util(self, col):
        # Recursive utility function to solve N-Queens problem using backtracking
        if col >= self.n:
            # Store the current solution
            solution = []
            for i in range(self.n):
                for j in range(self.n):
                    if self.board[i][j] == 1:
                        solution.append((i, j))
            self.solutions.append(solution)
            return True
        
        # Consider this column and try placing queens in all rows one by one
        res = False
        for i in range(self.n):
            if self.is_safe(i, col):
                self.board[i][col] = 1
                res = self.solve_nqueens_util(col + 1) or res
                self.board[i][col] = 0
        
        return res
    
    def solve_nqueens(self, find_all=True):
        # Solve the N-Queens problem
        self.solutions = []
        
        if find_all:
            self.solve_nqueens_util(0)
        else:
            if self.solve_nqueens_util(0):
                self.solutions = [self.solutions[0]] if self.solutions else []
        
        return self.solutions
    
    def print_board(self, solution=None):
        if solution:
            temp_board = [[0 for _ in range(self.n)] for _ in range(self.n)]
            for row, col in solution:
                temp_board[row][col] = 1
            board_to_print = temp_board
        else:
            board_to_print = self.board
        
        print("+" + "---+" * self.n)
        for i in range(self.n):
            print("|", end="")
            for j in range(self.n):
                if board_to_print[i][j] == 1:
                    print(" Q ", end="|")
                else:
                    print("   ", end="|")
            print()
            print("+" + "---+" * self.n)
    
    def print_all_solutions(self):
        # Print all found solutions
        if not self.solutions:
            print(f"No solutions found for {self.n}-Queens problem")
            return
        
        print(f"Found {len(self.solutions)} solution(s) for {self.n}-Queens problem:")
        print()
        
        for i, solution in enumerate(self.solutions):
            print(f"Solution {i + 1}:")
            print(f"Queen positions: {solution}")
            self.print_board(solution)
            print()


def demonstrate_nqueens():
    # Demonstrate the N-Queens solver with different board sizes
    print("N-Queens Problem Solver using Backtracking")
    print("=" * 50)
    
    # Test with different values of N
    test_cases = [4, 6, 8]
    
    for n in test_cases:
        print(f"\nSolving {n}-Queens Problem:")
        print("-" * 30)
        
        solver = NQueensBacktracking(n)
        solutions = solver.solve_nqueens(find_all=True)
        
        if solutions:
            print(f"Found {len(solutions)} solution(s)")
            print("\nFirst solution:")
            solver.print_board(solutions[0])
        else:
            print("No solutions found")
        
        print()


def interactive_nqueens():
    # Interactive N-Queens solver
    print("\nInteractive N-Queens Solver")
    print("=" * 30)
    
    while True:
        try:
            n = int(input("Enter the value of N (or 0 to exit): "))
            if n == 0:
                break
            
            if n < 1:
                print("N must be a positive integer")
                continue
            
            if n == 2 or n == 3:
                print(f"No solutions exist for {n}-Queens problem")
                continue
            
            find_all = input("Find all solutions? (y/n): ").lower().startswith('y')
            
            solver = NQueensBacktracking(n)
            solutions = solver.solve_nqueens(find_all=find_all)
            
            if solutions:
                if find_all:
                    solver.print_all_solutions()
                else:
                    print(f"\nFound a solution for {n}-Queens:")
                    solver.print_board(solutions[0])
            else:
                print(f"No solutions found for {n}-Queens problem")
            
            print()
            
        except ValueError:
            print("Please enter a valid integer")
        except KeyboardInterrupt:
            print("\nExiting...")
            break


if __name__ == "__main__":
    # Run demonstrations
    demonstrate_nqueens()
    
    # Run interactive solver
    interactive_nqueens()