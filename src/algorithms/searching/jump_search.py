# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


import math 
from src.algorithms import Algorithm
from src.data_structures import SearchArray


class JumpSearch(Algorithm[SearchArray]):
    # Constructor
    def __init__(self):
        super().__init__()

    # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self):
        return "Jump Search" 

    def run(self):        
        array = self.getDataStructure()
        target = array.getTarget()
    
        array.sort()
        self.invokeBriefDelay()

        # length of array
        n = len(array)
        # Square root length of array to find jump size
        step = int(math.sqrt(n))
        # Store index of last jump
        prev = 0
        # Find block closest to target -> if it exists
        while(array.getAt(min(step, n) - 1) < target): 
            array.resetBarColours()
            prev = step 
            array.setColourAt(prev, "red")
            if prev >= n: return 1
            step += int(math.sqrt(n))
            self.invokeBriefDelay()
        
        # Linear search to find target
        # Start at index of last jump and stops at index of next jump 
        for i in range(prev, prev + int(math.sqrt(n))): 
            array.resetBarColours()
            array.setColourAt(i, "red")
            # If current elment > target then target not in array
            if array.getAt(i) > target:
                return 0
            # If current element is equal to target
            if array.getAt(i) == target:#
                array.setColourAt(i, "green")
                return 0
            self.invokeDelay()  
        return 1
    
# Listen to Waiting For The End by Linkin Park
