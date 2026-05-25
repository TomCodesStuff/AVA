# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from src.algorithms import Algorithm
from src.data_structures import SortArray


class QuickSort(Algorithm[SortArray]):
    # Constructor
    def __init__(self):
        super().__init__()


    # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self) -> str:
        return "Quick Sort"  
    

    # Quick Sort Algorithm
    # Pivot selection using median of three 
    def run(self) -> int:  
        array = self.getDataStructure()
        self.__quickSortHelper(0, len(array) - 1)
        self.invokeDelay()
        return 0
    
    
    # Recusive implementation of quick sort 
    def __quickSortHelper(self, start, end):   
        if(start >= end): return
        # Finds pivot and adjusts elements relative to pivot
        pivotIndex = self.__partition(start, end) 
        self.__quickSortHelper(start, pivotIndex - 1) 
        self.__quickSortHelper(pivotIndex + 1, end)
      

    def __partition(self, start, end):  
        array = self.getDataStructure()
        # Middle of the array 
        mid = (start + end) // 2
        # Pivot is median of the elements at indexes start, mid, end 
        _, startPivotIdx = sorted([(array.getAt(start), start), (array.getAt(mid), mid), (array.getAt(end), end)])[1]   
        # The pivots index can change when elements are moved left/right of it
        pivotIdx = startPivotIdx
        
        # Iterate through any elements between pivot to end of array
        for i in range(startPivotIdx + 1, end + 1):  
            array.resetBarColours()
            array.setColourAt(pivotIdx, "orange")
            array.setColourAt(i, "red") 
            self.invokeDelay()

            # If element is less than/greater than or equal to the pivot 
            if(not array.isSwapNeeded(i, pivotIdx) or array.areElementsEqual(i, pivotIdx)):
                # Shift elements from pivot to i, one place right
                self.__shiftRight(pivotIdx, i)
                # Increment pivotIdx to point to new index of the pivot
                pivotIdx += 1
        
        # Iterate between elements between start of array and the pivot initial index
        i = 0 
        while(i != startPivotIdx): 
            array.resetBarColours()
            array.setColourAt(pivotIdx, "orange")
            array.setColourAt(i, "red") 
            self.invokeDelay()
            # If element is greater/smaller than the pivot 
            if(array.isSwapNeeded(i, pivotIdx) and not array.areElementsEqual(i, pivotIdx)):
                # Shift elements between i and the pivot one place left
                self.__shiftLeft(i, pivotIdx)   
                # Decrement pivotIdx to point to new index of the pivot
                pivotIdx -= 1  
                # Decrement startPivotIdx
                # i is not incremented as elements have been shifted so a different value is now at i
                startPivotIdx -= 1 
            # If element is less than or equal to pivot, move to next element
            else: i+=1
        return pivotIdx
    

    def __shiftRight(self, start, end): 
        array = self.getDataStructure()
        index = end 
        value = array.getAt(end)
        while(index != start):
            array.setAt(index, array.getAt(index - 1))  
            index-=1  
        array.setAt(index, value)
        
        
    def __shiftLeft(self, start, end): 
        array = self.getDataStructure()
        index = start 
        value = array.getAt(start)
        while(index != end):  
            array.setAt(index, array.getAt(index + 1))
            index+=1  
        array.setAt(index, value)  
      

                     
# Listen to Times like these by the Foo Fighters
