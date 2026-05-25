from .array import Array
from src.enums import SortDirection


class SortArray(Array): 
    def __init__(self):
        super().__init__()
        self.__sortDirection = SortDirection.ASCENDING 
    

    def setSortingDirecion(self, value : SortDirection) -> None:
        self.__sortDirection = value 
    

    def getSortingDirection(self) -> SortDirection:
        return self.__sortDirection 
    

    def isSortAcending(self) -> bool: 
        return True if self.__sortDirection == SortDirection.ASCENDING else False   

    
    def isSortDescending(self) -> bool: 
        return True if self.__sortDirection == SortDirection.DESCENDING else False  


    # Swaps the elements at the specified indexes
    def swapAt(self, i : int, j : int) -> None:  
        array = self.get()
        if i < 0 or j < 0: return 
        if i >= len(array) or j >= len(array): return 
        array[i], array[j] = array[j], array[i]
    

    # TODO implement better checking
    # Swaps the colour values of the two indexes specified
    def swapColoursAt(self, i : int, j : int) -> None:   
        barColoursArray = self.getBarColours()
        if i < 0 or j < 0: return 
        if i >= len(barColoursArray) or j >= len(barColoursArray): return 
        barColoursArray[i], barColoursArray[j] =\
            barColoursArray[j], barColoursArray[i]
    

    # Checks if elements need to be swapped 
    def isSwapNeeded(self, i : int, j : int) -> bool: 
        if(self.getSortingDirection() == SortDirection.ASCENDING):
            return self.getAt(i) > self.getAt(j) 
        else: return self.getAt(i) < self.getAt(j) 
    

    def areElementsEqual(self, i : int, j : int) -> bool:
        return self.getAt(i) == self.getAt(j)


# Listen to Snuff by Slipknot
