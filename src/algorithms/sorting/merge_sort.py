# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from src.algorithms import Algorithm
from src.data_structures import SortArray


class MergeSort(Algorithm[SortArray]):
    # Constructor
    def __init__(self):
        super().__init__()

    # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self) -> str:
        return "Merge Sort" 
    
    # (In place) Merge Sort Algorithm
    def run(self) -> int: 
        array = self.getDataStructure()
        # Call function to peform splitting into sub arrays 
        self.mergeSortHelper(0, len(array) - 1)
        return 0
    

    def mergeSortHelper(self, leftPtr, rightPtr):   
        # If sub-arrays are of size one, they are considered sorted 
        if(leftPtr >= rightPtr): return  
        # Calculates middle of sub-array
        mid = (leftPtr + rightPtr) // 2 
        # Splits sub-array in half into two subarrays
        self.mergeSortHelper(leftPtr, mid)
        self.mergeSortHelper(mid+1, rightPtr)
        # Merges the sub-arrays by sorting them
        self.mergeArrays(leftPtr, mid, rightPtr)

    def mergeArrays(self, start, mid, end):   
        array = self.getDataStructure()
        leftPtr = start 
        rightPtr = mid + 1 
        # Iterate through both arrays
        while(leftPtr <= mid and rightPtr <= end):  
            array.resetBarColours()
            array.setColourAt(leftPtr, "red")
            self.tick()
            # If elements are out of order 
            if(array.isSwapNeeded(leftPtr, rightPtr)):  
                # Shift all elements left 
                self.shiftArrayElements(leftPtr, rightPtr)
                leftPtr += 1
                mid += 1 
                rightPtr += 1 
            else: 
                leftPtr += 1 

    def shiftArrayElements(self, leftPtr, rightPtr):   
        array = self.getDataStructure()
        # Stores value at index rightPtr (as it is overwritten later)
        value = array.getAt(rightPtr)
        index = rightPtr 
        # Iterate until index = leftPtr
        while(index != leftPtr):   
            # Shift element at index one place to the left
            array.swapAt(index, index - 1)
            array.swapColoursAt(index, index - 1) 
            index -=  1
        
        array.resetBarColours()
        # Change element at leftPtr to stored value 
        array.setAt(leftPtr, value) 
        array.setColourAt(rightPtr, "red")
        self.tick()

# Listen to Wake Me Up When September Ends by Green Day
