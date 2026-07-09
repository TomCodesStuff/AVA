# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from src.algorithms import Algorithm
from src.data_structures import SearchArray

class LinearSearch(Algorithm[SearchArray]):
    # Constructor
    def __init__(self):
        super().__init__()

    # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self) -> str:
        return "Linear Search" 
    
    # Linear Search Algorithm
    def run(self) -> int: 
        array = self.getDataStructure()       
        # Iterate through array one element at a time
        for index, num in enumerate(array.get()):
            array.resetBarColours()
            # If current element is equal to the target
            if num == array.getTarget():
                # Set bar to green as target has been found 
                array.setColourAt(index, "green") 
                # self.updateArrayOnScreen()
                return 0
            else: array.setColourAt(index, "red")
            self.tick()     
        return 1

# Listen to Karma Police By Radiohead
