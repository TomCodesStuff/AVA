# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from src.algorithms import Algorithm
from src.data_structures import SearchArray


class BinarySearch(Algorithm[SearchArray]):
    def __init__(self):
        super().__init__()

    # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self):
        return "Binary Search" 
    
    # Binary Search algorithm -> see markdown for explanation
    def run(self):
        array = self.getDataStructure()
        target = array.getTarget()
        array.sort() 
        self.briefTick()

        low, high = 0, array.size() - 1
               
        while(low <= high):
            array.resetBarColours()
            # Calculate new mid
            mid = (low + high) // 2
            array.setColourAt(mid, "red")
            # If element at mid is equal to the target
            if array.getAt(mid) == target:
                array.setColourAt(mid, "green")
                return 0
            # If element at mid is greater than the target
            elif array.getAt(mid) > target:
                # Disreguard upper end of array
                high = mid - 1
            # If element is less than the target
            # Disreguard lower end of the array
            else: low = mid + 1
            self.tick()
        return 1
    
# Listen to Welcome to the DCC by Nothing But Thieves