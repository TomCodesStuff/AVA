# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from src.algorithms import Algorithm
from src.data_structures import SortArray


class BogoSort(Algorithm[SortArray]):
    # Constructor
    def __init__(self):
        super().__init__()

    # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self) -> str:
        return "Bogo Sort" 
    
    # Bogo Sort Algorithm
    def run(self) -> int: 
        array = self.getDataStructure() 
        sortedArray = sorted(array.get(), reverse=array.isSortDescending())
        # Continue until array is sorted
        while(sortedArray != array.get()): 
            # Randomly shuffle array
            array.shuffle()
            self.invokeDelay()
        return 0

# Listen to Times like these by the Foo Fighters
