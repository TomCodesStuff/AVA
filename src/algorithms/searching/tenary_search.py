# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from src.algorithms import Algorithm 
from src.data_structures import SearchArray


class TenarySearch(Algorithm[SearchArray]): 
    # Constructor
    def __init__(self):
        super().__init__()
    

    def getName(self):
        return "Tenary Search"
    

    def run(self): 
        array = self.getDataStructure()
        target = array.getTarget() 

        array.sort()
        self.invokeBriefDelay()

        # Left and right variables, used to adjust mid1 and mid2
        left = 0 
        right = len(array) - 1

        # loop while left variable is less than or equal to the right variable 
        while(left <= right):  
            array.resetBarColours()
            # Calculate mid1 and mid2 values
            mid1 = left + (right - left) // 3 
            mid2 = right - (right - left) // 3  
            
            # Sets bar colours
            array.setColourAt(mid1, "red")
            array.setColourAt(mid2, "red")

            # If value at mid1 is the target
            if(array.getAt(mid1) == target): 
                array.setColourAt(mid1, "green")
                array.setColourAt(mid2, "black")
                return 0
            # If value at mid2 is the target
            if(array.getAt(mid2) == target): 
                array.setColourAt(mid1, "black")
                array.setColourAt(mid2, "green")
                return 0

            # If target is less than value at mid1, adjust right variable
            if(target < array.getAt(mid1)): right = mid1 - 1 
            # If target is greater than value at mid2, adjust left variable
            elif(target > array.getAt(mid2)): left = mid2 + 1  
            # If target is somewhere inbetween mid1 and mid2, adjust left and right variables 
            else: 
                left = mid1 + 1 
                right = mid2 - 1 
            self.invokeDelay()
        return 1

# Listen to Times Like These By Foo Fighters 
