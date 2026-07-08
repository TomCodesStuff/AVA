# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.") 
    exit()


from src.algorithms import Algorithm
from src.data_structures import SearchArray


class ExponentialSearch(Algorithm[SearchArray]):
    def __init__(self):
        super().__init__()  
    
     # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self):
        return "Exponential Search" 
    
    def run(self): 
        array = self.getDataStructure()
        target = array.getTarget()

        array.sort() 
        self.briefTick()

        # If the target is the first element of the array
        if(array.getAt(0) == target): 
            array.setColourAt(0, "green")
            return 0
        
        # Start at index 1
        i = 1
        n = array.size()
        
        # Find the range the target could be in 
        # While i is less than the length of the array 
        # and the current value is less than or equal to the target
        while(i < n and array.getAt(i) <= target):  
            # Double the value i
            i = i << 1 
        
        # Perform a binary search within the calculated range i // 2 - min(i, n - 1)
        # min(i, n - 1) is needed as i could be larger than the size of the array
        return self.binarySearch(i // 2, min(i, n - 1)) 
    
    def binarySearch(self, left : int, right : int) -> int:
        array = self.getDataStructure()
        target = array.getTarget()
        upperBound = right 
        lowerBound = left 

        # Loop until left pointer is greater than the right pointer
        while(left <= right):  
            array.resetBarColours() 
            array.setColourAt(lowerBound, "orange")
            array.setColourAt(upperBound, "orange")
            # Calculate new mid
            mid = (left + right) // 2  
            # If value at index mid is the target
            if(array.getAt(mid) == target): 
                array.setColourAt(mid, "green")
                return 0
            # If the value at index mid is greater than the target, reduce right pointer
            if(array.getAt(mid) > target): right = mid - 1
            # If the value at index mid is less than the target, increase left pointer
            elif(array.getAt(mid) < target): left = mid + 1
            
            array.setColourAt(mid, "red")
            self.tick()
        
        # Element is not in array
        return 1
    
# Listen to Welcome To Paradise By Green Day
