# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


import tkinter as tk 
from typing import TYPE_CHECKING, TypeVar
from src.screens.array_algorithm import ArrayAlgorithmScreen
from src.data_structures import SortArray
from src.enums import SortDirection, AlgorithmType


if TYPE_CHECKING:
    from src.screens.array_sort import SortController, SortModel


C = TypeVar("C", bound="SortController")
M = TypeVar("M", bound="SortModel")
D = TypeVar("D", bound="SortArray")


class SortScreen(ArrayAlgorithmScreen[C, M, D]): 
    def __init__(self, window):
        super().__init__(window)   
    
    # Creates the buttons that lets userr change between sorting by ascending or descending order
    def __createSortOptionButtons(self):
        self.__radioButtonsFrame = tk.Frame(self.getOptionsWidgetFrame(), background="white")
        self.__radioButtonsFrame.pack(pady=(10, 0)) 
        self.__createSortAscendingButton()
        self.__createSortDescendingButton() 

    # Creates the button to toggle ascending order
    def __createSortAscendingButton(self):
        self.__ascendingOption = tk.Button(self.__radioButtonsFrame, text="Sort Ascending.", 
                                           width = self.getModel().getButtonWidth(), relief = "solid", 
                                           font = (self.getFont(), self.getFontSize()), state="disabled", 
                                           command=self.getController().toggleSortDirection)
        self.__ascendingOption.pack() 

    # Creates the button to toggle descending order
    def __createSortDescendingButton(self):
        self.__descendingOption = tk.Button(self.__radioButtonsFrame, text="Sort Descending.", 
                                            width = self.getModel().getButtonWidth(), relief = "solid", 
                                            font = (self.getFont(), self.getFontSize()), 
                                            command=self.getController().toggleSortDirection)
        self.__descendingOption.pack(pady=(5, 0))
        self.addToggleableWidget(self.__descendingOption)

    # Disable and enables the sort direction buttons when one is pressed 
    def toggleSortDirection(self): 
        if(self.getModel().getSortDirection() == SortDirection.ASCENDING): 
            self.__ascendingOption.config(state="disabled")
            self.__descendingOption.config(state="active")  
            self.removeToggleableWidget(self.__ascendingOption)
            self.addToggleableWidget(self.__descendingOption)
        else:
            self.__ascendingOption.config(state="active")
            self.__descendingOption.config(state="disabled") 
            self.addToggleableWidget(self.__ascendingOption)
            self.removeToggleableWidget(self.__descendingOption)

    def prepare(self): 
        self.getDataStructure().setSortingDirecion(self.getModel().getSortDirection())

    def render(self) -> None: 
        self.createBaseArrayLayout() 
        self.setAlgorithmType(AlgorithmType.SORTING)
        self.displayAlgorithmOptions()
        self.__createSortOptionButtons()


# Listen to Minority by Green Day