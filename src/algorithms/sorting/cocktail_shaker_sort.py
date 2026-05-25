# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from src.algorithms import Algorithm
from src.data_structures import SortArray

class CocktailShakerSort(Algorithm[SortArray]):
    # Constructor
    def __init__(self):
        super().__init__()


    # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self) -> str:
        return "Cocktail Shaker Sort" 


    # Cocktail Shaker Sort Algorithm
    def run(self) -> int: 
        array = self.getDataStructure()
        start = 0 
        end = len(array) - 1 
        swapped = True

        # While elements have been swapped 
        while(swapped):
            # Set swapped to false
            swapped = False
            # Iterate between indexes start and end
            for i in range(start, end): 
                array.resetBarColours()
                array.setColourAt(i, "red")  
                self.invokeDelay()
                
                # If elements need to be swapped
                if(array.isSwapNeeded(i, i + 1)):
                    # Swap them
                    array.swapAt(i, i + 1) 
                    array.swapColoursAt(i, i + 1)
                    # Set swapped to true
                    swapped = True
            
            array.setColourAt(i, "red")  
            self.invokeDelay()

            # If no swaps were made, stop algorithm 
            if(not swapped): 
                self.invokeDelay()
                return 0 
            
            # Decrement end 
            end -= 1
            # Iterate between indexes end - 1 and start + 1
            for i in range(end - 1, max(start - 1, 0), -1):
                array.resetBarColours()
                array.setColourAt(i, "red")  
                self.invokeDelay()
                
                # If elmenents need to be swapped, swap them
                if(array.isSwapNeeded(i, i + 1)): 
                    array.swapAt(i, i + 1)
                    array.swapColoursAt(i, i + 1)
                    # Set swapped to True 
                    swapped = True 
            # Increment start
            start += 1 

        self.invokeDelay()
        return 0

# Listen to What You Know by Two Door Cinema Club 
