# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from src.algorithms import Algorithm
from src.data_structures import SortArray


class BubbleSort(Algorithm[SortArray]):
    # Constructor
    def __init__(self):
        super().__init__()

    # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self) -> str:
        return "Bubble Sort" 

    # Bubble Sort Algorithm
    def run(self) -> int: 
        array = self.getDataStructure()
        n = len(array)
        # Iterate through array
        for i in range(n): 
            array.resetBarColours()
            # No swaps have been made
            swapped = False
            # Iterate from start of array to last sorted element
            for j in range(0, n - i - 1):  
                array.resetBarColours()
                array.setColourAt(j, "red")
                self.invokeDelay()
                # If adjacent element needs to be swapped with current element
                if(array.isSwapNeeded(j, j + 1)): 
                    array.swapAt(j, j + 1)
                    array.swapColoursAt(j, j + 1)
                    # Swap has been performed
                    swapped = True
            # If no swaps have been made, the array is sorted 
            if(not swapped):
                return 0
        return 0

# Listen to BREATHING UNDERWATER these by the Hot Milk
