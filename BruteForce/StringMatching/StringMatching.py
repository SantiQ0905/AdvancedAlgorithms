def stringMatch(text, pattern):
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


#O(nm)
#Ω(n)