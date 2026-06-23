# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from src.algorithms import Algorithm
from src.data_structures import SortArray

class GnomeSort(Algorithm[SortArray]):
    # Constructor
    def __init__(self):
        super().__init__()

    # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self) -> str:
        return "Gnome Sort" 

    # Gnome Sort Algorithm
    def run(self) -> int: 
        array = self.getDataStructure()
        # Length of the array
        n = len(array)
        pos = 0  
        # While pos is less than the length of the array
        while(pos < n): 
            array.resetBarColours()
            array.setColourAt(pos, "red")
            self.tick()

            # If pos is at the start of the array, increment pos
            if(pos == 0): pos += 1 
            # If element at pos and pos - 1 need to be swapped
            if(array.isSwapNeeded(pos - 1, pos)):
                array.swapAt(pos, pos - 1)
                array.swapColoursAt(pos, pos - 1)
                self.tick()
                # Decrement pos
                pos -= 1
            # If elements at pos and pos - 1 are in the right place
            else: 
                # Increment pos 
                pos += 1  

        self.tick()
        return 0
        
# Listen to Smells Like Teen Spirit by Nirvana 
