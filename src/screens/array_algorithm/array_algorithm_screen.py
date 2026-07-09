
# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

import tkinter as tk
from typing import TYPE_CHECKING, TypeVar
from src.screens.algorithm_base import AlgorithmScreen
from src.data_structures import Array


if TYPE_CHECKING:
    from src.screens.array_algorithm import ArrayAlgorithmController, ArrayAlgorithmModel


C = TypeVar("C", bound="ArrayAlgorithmController")
M = TypeVar("M", bound="ArrayAlgorithmModel")
D = TypeVar("D", bound="Array")


TINY_DELAY_MS = 50
NUM_BAR_FLASHES = 3


class ArrayAlgorithmScreen(AlgorithmScreen[C, M, D]):
    def __init__(self, window):
        super().__init__(window) 
        self.__animationIndex = 0

    # Creates a slider that allows users to alter an arrays size
    def __createArrayAdjuster(self) -> None:
        self.__arraySizeSlider = tk.Scale(self.getOptionsWidgetFrame(), from_ = 1, to_ = self.getModel().getMaxBars(), 
                                          length = self.getOptionsWidgetFrame().winfo_width(), 
                                          orient = "horizontal", bg = "white", highlightbackground = "white", 
                                          command = lambda x: self.getController().adjustArray(int(x)))
        self.__arraySizeSlider.pack(pady = (10, 0))
        self.addToggleableWidget(self.__arraySizeSlider)

    # Creates buttons the allow algorithms to be sorted and shuffled
    def __createSortShuffleButtons(self) -> None: 
        self.__arraySortShuffleFrame = tk.Frame(self.getOptionsWidgetFrame(), bg = "white") 
        self.__arraySortShuffleFrame.pack(pady=(20, 0)) 

        self.__sortButton = tk.Button(self.__arraySortShuffleFrame, text="Sort.", width = 7, relief = "solid", 
                                      font = (self.getFont(), self.getFontSize()), command=self.__sortArray)
        self.__sortButton.grid(row = 0, column = 0, padx = (9,5)) 
        self.__shuffleButton = tk.Button(self.__arraySortShuffleFrame, text="Shuffle.", width = 7, relief = "solid", 
                                         font = (self.getFont(), self.getFontSize()), command=self.__shuffleArray)
        self.__shuffleButton.grid(row = 0, column = 1, padx = (3,8)) 
        self.addToggleableWidget(self.__sortButton)
        self.addToggleableWidget(self.__shuffleButton)
    
    # Sorts and displays the array
    def __sortArray(self) -> None:
        self.getDataStructure().sort()
        self.getController().refreshCanvas() 
        
    # Shuffles and displays the array
    def __shuffleArray(self) -> None:
        self.getDataStructure().shuffle()
        self.getController().refreshCanvas() 

    # This functions handles creating and displaying the options the user is presented with
    def createArrayOptions(self) -> None: 
        self.__createArrayAdjuster()
        self.__createSortShuffleButtons()

    def createBaseArrayLayout(self):
        self.createBaseLayout()
        self.getController().calculateArrayBounds()
        self.createArrayOptions() 
        self.getController().adjustArray(1)
    
    def animationSetup(self) -> None: 
        # Reset bar colours
        self.getDataStructure().resetBarColours() 
        self.getController().refreshCanvas()
        self.__animationIndex = 0 

    def coolAnimationFrame(self) -> None:  
        array = self.getDataStructure() 
        array.setColourAt(self.__animationIndex, "green")
        self.__animationIndex += 1
        self.setFrameDelay(TINY_DELAY_MS)
        if self.__animationIndex == array.size(): self.endAnimation()
    
    def complete(self) -> None:
        self.getController().refreshCanvas(refreshColours=True)

# Listen to Almost by Bowling For Soup
   