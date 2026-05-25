# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
   print("This is file shouldn't be run on it's own. \nIt should be imported only.")
   exit()


from src.algorithms import Algorithm
from src.data_structures import SortArray


class SelectionSort(Algorithm[SortArray]):
    # Constructor
    def __init__(self):
        super().__init__() 


    # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self) -> str:
        return "Selection Sort"  


    # Stable Selection Sort Algorithm
    def run(self) -> int: 
        array = self.getDataStructure()
        n = len(array)   
        # Iterate through each element in the array
        for i in range(n): 
            array.resetBarColours()
            # Index of the current smallest/largest element in the array
            swapIdx = i 
            # Iterate through elements from i + 1 to the end of the current array 
            for j in range(i + 1, n): 
                array.resetBarColours() 
                array.setColourAt(i, "orange") 
                array.setColourAt(j , "red") 
                self.invokeDelay()
                # If current element smaller/larger than previous smallest/largest element
                if(not array.isSwapNeeded(j, swapIdx)): swapIdx = j   
            # Shift elements right 
            self.__shiftRight(i, swapIdx) 
            
            array.setColourAt(i, "orange") 
            self.invokeDelay()
        
        self.invokeDelay() 
        return 0
    
    # Shifts elements between the specified indexes one place right 
    def __shiftRight(self, start, end): 
        array = self.getDataStructure()
        index = end 
        value = array.getAt(end)
        while(index != start):  
            array.setAt(index, array.getAt(index - 1))
            index-=1  
        array.setAt(index, value)
        
                     
# Listen to Ain't No Rest For The Wicked by Cage the Elephant
