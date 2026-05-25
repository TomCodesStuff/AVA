# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.") 
    exit()


from src.algorithms import Algorithm 
from src.data_structures import SearchArray


class InterpolationSearch(Algorithm[SearchArray]):
    # Constructor
    def __init__(self):
        super().__init__()  
    
    def getName(self):
        return "Interpolation Search"
     
    def run(self): 
        array = self.getDataStructure()
        target = array.getTarget()

        array.sort()
        self.invokeBriefDelay()

        # Low and high variables, used to calculate pos
        low = 0
        high = len(array) - 1

        # Iterate whilst conditions are met 
        while(low <= high and target >= array.getAt(low) and target <= array.getAt(high)):  
            array.resetBarColours()
            # Calculate pos (where algorithm guesses the target is)
            pos = low + (((target - array.getAt(low)) * (high - low)) // (array.getAt(high) - array.getAt(low)))   
            # target has been found
            if(array.getAt(pos) == target): 
                array.setColourAt(pos, "green")
                return 0
            # If element at index pos is greater than target, adjust high
            if(array.getAt(pos) > target): high = pos - 1 
            # If element at index pos is less than target, adjust low
            elif(array.getAt(pos) < target): low = pos + 1
            array.setColourAt(pos, "red")
            self.invokeDelay()
        return 1

# Listen to Under The Cover Of Darkness by The Strokes