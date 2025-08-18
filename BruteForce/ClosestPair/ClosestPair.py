# Import necessary built-in modules
import os    # For file and directory operations
import math  # For mathematical functions like sqrt()

def distance_squared(point1, point2):
    """
    Calculate the SQUARED Euclidean distance between two points in 2D space
    
    This is an optimization that avoids the expensive square root calculation.
    Since sqrt() is a monotonic function, comparing squared distances gives
    the same ordering as comparing actual distances:
    If d1² < d2², then d1 < d2
    
    The squared Euclidean distance formula is: d² = (x2-x1)² + (y2-y1)²
    
    Args:
        point1: Tuple containing (x, y) coordinates of first point
        point2: Tuple containing (x, y) coordinates of second point
    
    Returns:
        float: The SQUARED Euclidean distance between the two points
    """
    # Extract x and y coordinates from the first point
    x1, y1 = point1
    # Extract x and y coordinates from the second point
    x2, y2 = point2
    
    # Calculate the SQUARED distance (without square root)
    # This is much faster than calculating the actual distance
    # Step 1: Find the difference in x-coordinates and square it
    # Step 2: Find the difference in y-coordinates and square it  
    # Step 3: Add the squared differences (NO square root!)
    return (x2 - x1) ** 2 + (y2 - y1) ** 2

def distance(point1, point2):
    """
    Calculate Euclidean distance between two points in 2D space
    
    This function is kept for when we need the actual distance value
    (like for final output). For comparisons, we use distance_squared().
    
    The Euclidean distance formula is: d = √[(x2-x1)² + (y2-y1)²]
    
    Args:
        point1: Tuple containing (x, y) coordinates of first point
        point2: Tuple containing (x, y) coordinates of second point
    
    Returns:
        float: The Euclidean distance between the two points
    """
    # Use the squared distance function and then take square root
    # This way we avoid duplicating the calculation logic
    return math.sqrt(distance_squared(point1, point2))

def closest_pair_brute_force(points):
    """
    Find the closest pair of points using brute force algorithm
    
    This algorithm compares every possible pair of points to find the minimum distance.
    It's called "brute force" because it doesn't use any optimization - it simply
    checks all possible combinations.
    
    OPTIMIZATION: This version uses squared distances for comparisons to avoid
    expensive square root calculations. Only the final result is converted to
    actual distance.
    
    Time complexity: O(n²) - where n is the number of points
    Space complexity: O(1) - only uses constant extra space
    
    Args:
        points: List of tuples, where each tuple contains (x, y) coordinates
    
    Returns:
        tuple: (point1, point2, min_distance) where:
               - point1: First point of the closest pair
               - point2: Second point of the closest pair  
               - min_distance: The ACTUAL distance between the closest pair
    """
    # Get the total number of points in the list
    n = len(points)
    
    # Edge case: If we have fewer than 2 points, we can't find a pair
    if n < 2:
        return None, None, float('inf')
    
    # Initialize minimum SQUARED distance to infinity (largest possible value)
    # We use squared distance for efficiency during comparisons
    min_distance_squared = float('inf')
    
    # Initialize the closest pair as empty tuple
    # This will store the two points that are closest to each other
    closest_pair = (None, None)
    
    # Outer loop: iterate through each point as the first point of a pair
    # We go from 0 to n-1 (all points except the last one)
    for i in range(n):
        # Inner loop: iterate through remaining points as the second point of a pair
        # We start from i+1 to avoid comparing a point with itself
        # and to avoid duplicate comparisons (comparing point A with B and B with A)
        for j in range(i + 1, n):
            # Calculate the SQUARED distance between current pair of points
            # This avoids the expensive square root calculation
            dist_squared = distance_squared(points[i], points[j])
            
            # If this squared distance is smaller than our current minimum
            if dist_squared < min_distance_squared:
                # Update the minimum squared distance
                min_distance_squared = dist_squared
                # Update the closest pair with current points
                closest_pair = (points[i], points[j])
    
    # Convert the final squared distance to actual distance for output
    # We only do the square root calculation once, at the very end
    min_distance = math.sqrt(min_distance_squared)
    
    # Return the closest pair and their ACTUAL distance
    return closest_pair[0], closest_pair[1], min_distance

def read_points_from_file(filename):
    """
    Read points from a text file and parse them into a list of coordinate tuples
    
    Expected file format:
    - First line: integer representing the number of points (n)
    - Next n lines: each line contains x and y coordinates separated by tab
    
    Example file content:
    3
    1.5    2.7
    -3.2   4.1
    0.0    -1.8
    
    Args:
        filename: String path to the file containing point data
    
    Returns:
        list: List of tuples where each tuple contains (x, y) coordinates
              Returns empty list if file is not found or has invalid format
    """
    try:
        # Attempt to open and read the file
        # 'r' mode means read-only text mode
        with open(filename, 'r') as file:
            # Read all lines from the file into a list
            # Each line includes the newline character (\n) at the end
            lines = file.readlines()
        
        # Parse the first line to get the number of points
        # strip() removes whitespace and newline characters
        # int() converts the string to an integer
        n = int(lines[0].strip())
        
        # Initialize empty list to store the points
        points = []
        
        # Read each point from lines 1 to n (skip line 0 which contains count)
        # range(1, n + 1) gives us indices 1, 2, 3, ..., n
        for i in range(1, n + 1):
            # Check if the line exists (file might have fewer lines than expected)
            if i < len(lines):
                # Remove whitespace and split by tab character
                # This separates x and y coordinates
                coords = lines[i].strip().split('\t')
                
                # Ensure we have at least 2 coordinates (x and y)
                if len(coords) >= 2:
                    # Convert string coordinates to floating point numbers
                    x = float(coords[0])  # First coordinate is x
                    y = float(coords[1])  # Second coordinate is y
                    
                    # Add the point as a tuple to our points list
                    points.append((x, y))
        
        # Return the list of points
        return points
        
    # Handle case where file doesn't exist
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        return []  # Return empty list
        
    # Handle case where file contains invalid data (non-numeric values, etc.)
    except ValueError:
        print(f"Error: Invalid data format in file {filename}.")
        return []  # Return empty list

def process_test_files():
    """
    Process all test files in the TestFiles folder and find closest pairs
    
    This function:
    1. Locates the TestFiles directory
    2. Finds all .txt files in that directory
    3. Processes each file to find the closest pair of points
    4. Displays the results in a formatted manner
    
    The function handles multiple test files automatically and provides
    comprehensive output for each file processed.
    """
    # Define the directory name where test files are located
    test_files_dir = "BruteForce\ClosestPair\TestFiles"
    
    # Check if the TestFiles directory exists
    # os.path.exists() returns True if the path exists, False otherwise
    if not os.path.exists(test_files_dir):
        print(f"Error: Directory '{test_files_dir}' not found.")
        return  # Exit the function early if directory doesn't exist
    
    # Get list of all files in the TestFiles directory
    # os.listdir() returns a list of all files and folders in the given directory
    # List comprehension filters only files that end with '.txt'
    test_files = [f for f in os.listdir(test_files_dir) if f.endswith('.txt')]
    
    # Sort the files alphabetically for consistent processing order
    # This ensures files are processed in a predictable sequence
    test_files.sort()
    
    # Check if any test files were found
    if not test_files:
        print("No test files found in TestFiles directory.")
        return  # Exit if no test files exist
    
    # Print header for the results section
    print("=== CLOSEST PAIR ALGORITHM RESULTS ===\n")
    
    # Process each test file one by one
    for filename in test_files:
        # Create full file path by joining directory and filename
        # os.path.join() handles path separators correctly for the operating system
        filepath = os.path.join(test_files_dir, filename)
        
        # Print which file is currently being processed
        print(f"Processing file: {filename}")
        print("-" * 40)  # Print a line of dashes for visual separation
        
        # Read points from the current file
        points = read_points_from_file(filepath)
        
        # Check if we have enough points to find a pair
        # We need at least 2 points to calculate distance between them
        if len(points) < 2:
            print("Error: Need at least 2 points to find closest pair.\n")
            continue  # Skip to next file if insufficient points
        
        # Find the closest pair using our brute force algorithm
        point1, point2, min_dist = closest_pair_brute_force(points)
        
        # Check if algorithm successfully found a closest pair
        if point1 is not None and point2 is not None:
            # Display the results in a formatted manner
            print(f"Number of points: {len(points)}")
            print(f"Closest pair:")
            
            # Display coordinates with 3 decimal places for readability
            print(f"  Point 1: ({point1[0]:.3f}, {point1[1]:.3f})")
            print(f"  Point 2: ({point2[0]:.3f}, {point2[1]:.3f})")
            
            # Display distance with 6 decimal places for precision
            print(f"Distance: {min_dist:.6f}")
        else:
            # This should rarely happen, but good to handle edge cases
            print("Error: Could not find closest pair.")
        
        # Print empty line for spacing between files
        print()

def main():
    """
    Main function - entry point of the program
    
    This function serves as the starting point when the script is executed.
    It calls the process_test_files() function to begin the closest pair
    analysis on all test files.
    
    By organizing the code this way, we separate the main logic from the
    execution entry point, making the code more modular and easier to test.
    """
    # Call the function that processes all test files
    process_test_files()

# This is a Python idiom that checks if this file is being run directly
# (not imported as a module by another script)
# 
# __name__ is a special variable that Python sets automatically:
# - When file is run directly: __name__ == "__main__"  
# - When file is imported: __name__ == "filename" (without .py)
#
# This allows the script to be imported without automatically running main()
if __name__ == "__main__":
    # Only run main() if this file is executed directly
    main()
