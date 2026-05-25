# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from src.algorithms import Algorithm
from src.data_structures import SortArray


class InsertionSort(Algorithm[SortArray]):
    # Constructor
    def __init__(self):
        super().__init__() 

    # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self) -> str:
        return "Insertion Sort"  
    

    # Stable Insertion Sort Algorithm
    def run(self) -> int: 
        array = self.getDataStructure()
        n = len(array)
        # Iterate through array, the first element is considered as sorted 
        for i in range(1, n): 
            array.resetBarColours()
            array.setColourAt(i - 1, "orange")
            array.setColourAt(i, "red")
            self.invokeDelay()

            # The left pointer keeps track of sorted element being compared to the sorted element
            leftPtr = i - 1
            # The right pointer keeps track of the unsorted element
            rightPtr = i 
            # Iterate until the start of the sorted array or 
            # the unsorted element is in the right place 
            while(leftPtr >= 0 and array.isSwapNeeded(leftPtr, rightPtr)): 
                # Swap elements indexes leftPtr, rightPtr
                array.swapAt(leftPtr, rightPtr)
                leftPtr -= 1
                rightPtr -= 1  
                array.resetBarColours()
                array.setColourAt(i, "orange")
                array.setColourAt(rightPtr, "red")
                self.invokeDelay()
        
        return 0 

                     
# Listen to Highway to Hell by ACDC
