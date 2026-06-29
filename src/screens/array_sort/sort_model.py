# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

from ..array_algorithm import ArrayAlgorithmModel
from src.enums import SortDirection

TEN_MS = 10 
ONE_SECOND = 1000
DELAY_RESOLUTION = 1

class SortModel(ArrayAlgorithmModel):
    def __init__(self):
        super().__init__()
        self.__buttonWidth = 16 
        self.__sortDirection = SortDirection.ASCENDING

        self.setDelayToMilliseconds()
        self.setResolution(DELAY_RESOLUTION)
        self.setMinDelay(TEN_MS)
        self.setMaxDelay(ONE_SECOND)

    # Toggles the sort setting between and ascending and descending
    def toggleSortDirection(self):
        if self.__sortDirection == SortDirection.ASCENDING:
            self.__sortDirection = SortDirection.DESCENDING
        else: self.__sortDirection = SortDirection.ASCENDING

    # Returns the width used for the buttons 
    def getButtonWidth(self) -> int: return self.__buttonWidth 
    # Returns if the sorting direction is ascending or descending
    def getSortDirection(self) -> SortDirection: return self.__sortDirection
    

# Listen to What You Know by Two Door Cinema Club