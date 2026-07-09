# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from src.algorithms import Algorithm
from src.data_structures import SortArray

class BrickSort(Algorithm[SortArray]):
    # Constructor
    def __init__(self,):
       super().__init__()

    # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self) -> str:
        return "Brick Sort" 
    
    # Brick Sort Algorithm
    def run(self) -> int: 
        array = self.getDataStructure()

        # Length of the array
        n = len(array)
        swapped = True 
        
        # While swapped is true
        while(swapped):
            swapped = False
            # Iterate through odd indexes of the array
            for i in range(1, n - 1, 2):
                array.resetBarColours()  
                array.setColourAt(i, "red") 
                self.tick()
                # If elements are in the wrong the order
                if(array.isSwapNeeded(i, i + 1)):
                    # Swap elements
                    array.swapAt(i, i + 1)
                    array.swapColoursAt(i, i + 1)
                    self.tick()
                    swapped = True
            
            array.resetBarColours()
            array.setColourAt(i, "red")  
            self.tick()
            
            # If no swaps are performed
            if(not swapped): break

            swapped = False
            # Iterate through even indexes of the array
            for i in range(0, n - 1, 2):
                array.resetBarColours()
                array.setColourAt(i, "red")  
                self.briefTick
                # If elements are in the wrong the order
                if(array.isSwapNeeded(i, i + 1)):
                    # Swap elements
                    array.swapAt(i, i + 1)
                    array.swapColoursAt(i, i + 1)  
                    self.tick()
                    swapped = True  
        
        self.tick() 
        return 0

# Listen to Lithium by Nirvana 
