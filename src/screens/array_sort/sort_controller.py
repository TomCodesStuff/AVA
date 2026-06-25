# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from typing import TYPE_CHECKING, TypeVar
from src.screens.array_algorithm import ArrayAlgorithmController
from src.data_structures import SortArray


if TYPE_CHECKING: 
    from src.screens.array_sort import SortScreen, SortModel


S = TypeVar("S", bound="SortScreen")
M = TypeVar("M", bound="SortModel")
D = TypeVar("D", bound="SortArray")


class SortController(ArrayAlgorithmController[S, M, D]):
    def __init__(self, screen, model, dataStructure):
        super().__init__(screen, model, dataStructure)
    
    # Changes the sort direction 
    def toggleSortDirection(self):
        # Changes the sort direction
        self.getModel().toggleSortDirection()  
        # Disables the button that called the function and enables the currently disabled button
        self.getScreen().toggleSortDirection()


# Listen to ALICE COOPER'S POOL HOUSE by Hot Milk
