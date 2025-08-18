def stringMatch(text, pattern):
    """
    Searches for all occurrences of a pattern string within a given text string using the brute-force approach.
    Args:
        text (str): The text string to be searched.
        pattern (str): The pattern string to search for within the text.
    Returns:
        list: A list of starting indices where the pattern is found in the text.
    Worst-case complexity: O(n * m), where n is the length of the text and m is the length of the pattern.
    """
def main():
    """
    Reads the text and pattern from a file, performs string matching, and prints the result.
    The file "BruteForce/StringMatching/TestFiles/stringMatch.txt" should contain the text on the first line and the pattern on the second line.
    Worst-case complexity: Dominated by stringMatch, which is O(n * m).
    """
# The worst-case complexity for the stringMatch algorithm is O(n * m), where n is the length of the text and m is the length of the pattern.
    n = len(text) #Obtains length of the entire inputed text
    m = len(pattern) #Obtains length of the entire inputted pattern
    matches = [] #Empty array used for storing matches as they're found

    for i in range(n - m + 1):
        matchFound = True #for loop used for determining if the patter has been found
        for j in range(m):
            if text[i + j] != pattern[j]:
                matchFound = False
                break #for loop used for ruling out non-matches
        if matchFound:
            matches.append(i) #if a match has been found, it will be added to the array

    return matches #returns array with the completed pattern found from the text




def main(): #main function that opens and reads chosen file
    with open("BruteForce/StringMatching/TestFiles/stringMatch.txt", "r", encoding="utf-8") as txt:
        lines = txt.read().splitlines()
        text = lines[0] #whole text is the first line of the file
        pattern = lines[1] #pattern is the second line of the text

    result = stringMatch(text, pattern)

    if result: #if-else statement for displaying the final result, whether the pattern was found or not
        print(f"Pattern found at positions: {result}")
    else:
        print("Pattern not found")


main()



