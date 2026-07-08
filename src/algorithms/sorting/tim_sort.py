# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from src.algorithms import Algorithm
from src.data_structures import SortArray


MIN_NUM_RUNS = 16


class TimSort(Algorithm[SortArray]):
    # Constructor
    def __init__(self): 
        super().__init__()  
    
    # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self) -> str:
        return "Tim Sort"  

    def __calculateRunSize(self, arrayLength : int) -> int:
        if arrayLength <= MIN_NUM_RUNS: return arrayLength
        return max(1, arrayLength // MIN_NUM_RUNS)

    def __insertionSort(self, leftPtr : int, rightPtr : int) -> None:  
        array = self.getDataStructure()
        for i in range(leftPtr + 1, rightPtr): 
            j = i 
            array.resetBarColours()
            array.setColourAt(i - 1, "orange")
            array.setColourAt(j, "red")
            self.tick()

            while(j > leftPtr and array.isSwapNeeded(j - 1, j)): 
                array.swapAt(j, j - 1)
                array.swapColoursAt(j, j - 1)
                self.tick()
                j -= 1

    def __shiftElements(self, start : int, idx : int) -> None: 
        array = self.getDataStructure()
        value = array.getAt(idx)
        while(idx != start): 
            array.resetBarColours()
            array.setAt(idx, array.getAt(idx - 1))
            array.setColourAt(idx - 1, "red")
            self.tick()
            idx -= 1 
        
        array.resetBarColours()
        array.setAt(start, value)
        array.setColourAt(start, "red")
        self.tick()
        return 

    def __mergeSubArrays(self, start : int, mid : int, end : int) -> None:
        array = self.getDataStructure()
        rightPtr = mid + 1 
        while(start <= mid and rightPtr <= end): 
            array.resetBarColours()
            array.setColourAt(start, "red")
            self.tick()
            if array.isSwapNeeded(start, rightPtr): 
                self.__shiftElements(start, rightPtr) 
                start += 1 
                mid += 1 
                rightPtr += 1
            else: 
                start += 1

    # Tim Sort Algorithm
    def run(self) -> int:    
        array = self.getDataStructure()
        n = len(array)
        runSize = self.__calculateRunSize(n)
        for i in range(0, n, runSize):
            self.__insertionSort(i, min(i + runSize, n))
         
        mergeSize = runSize
        while(mergeSize < n): 
            for left in range(0, n, mergeSize * 2): 
                mid = left + mergeSize - 1
                right = min(n - 1, left + (2 * mergeSize) - 1)
                if mid < right: 
                    self.__mergeSubArrays(left, mid, right) 
            mergeSize << 1  
        return 0 
 
# Listen to No Surprises by Radiohead
