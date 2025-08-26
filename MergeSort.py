# Analysis and Design of Advanced Algorithms 
# Group #607
# Team 3
# Dr. Katie Brodhead

# Santiago Quintana Moreno A01571222
# Miguel Ángel Álvarez Hermida A01722925

# ----- CLASS ACTIVITY 2: DECREASE AND CONQUER -----

# O(n log n) - Merge Sort divides the array into halves recursively (log n levels),
# and merges each level in linear time (n), resulting in overall O(n log n) complexity.


def merge_sort(array):
    if len(array) <= 1:
        return
    else:
        middle = len(array) // 2  #This is used to find the middle index of the array
        
        #List-splicing is utilized to separate the array into left and right halfs
        leftArray = array[:middle] 
        rightArray = array[middle:]

        #Recursive call of the function to keep on splitting the array, assuming the length of each 
        # portion is greater than one (no more splicing / base case)
        merge_sort(leftArray) 
        merge_sort(rightArray)
        
        
    merge(array, leftArray, rightArray) #secondary/helper function is called
 
def merge(array, leftArray, rightArray):
    i=0
    j=0
    k=0
    #i is left index, j is right index, and k is the index of the original array, all initilizaed 
    # at cero for looping
    #elements from each half of the array are compared, smallest element is 
    # added to the original array
    while i < len(leftArray) and j < len(rightArray): 
        if leftArray[i] <= rightArray[j]:
            array[k] = leftArray[i]
            i += 1
        else:
            array[k] = rightArray[j]
            j += 1
        k += 1

    #if elements remain on the left array, these will be copied to the original
    while i < len(leftArray): 
        array[k] = leftArray[i]
        i += 1
        k += 1

    #if elements remain on the right array, these will be copied to the original
    while j < len(rightArray): 
        array[k] = rightArray[j]
        j += 1
        k += 1


def main():
    array = [38, 223, 331, 441, 2, 10, 5, 998, 206, 3, 1] #example array (unsorted)
    merge_sort(array)
    print("Array after merge sort: ", array) #Prints the sorted array
    
main()

#O(nlogn) 