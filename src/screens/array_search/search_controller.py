# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


import random
from typing import TYPE_CHECKING, TypeVar
from ..array_algorithm import ArrayAlgorithmController
from src.data_structures import SearchArray

if TYPE_CHECKING: 
    from src.screens.array_search import SearchScreen, SearchModel

S = TypeVar("S", bound="SearchScreen")
M = TypeVar("M", bound="SearchModel")
D = TypeVar("D", bound="SearchArray")

TARGET_SETTING_COIN_FLIP = 0.5


class SearchController(ArrayAlgorithmController[S, M, D]):
    def __init__(self, screen, model, dataStructure):
        super().__init__(screen, model, dataStructure)
    
    # Returns the text to be displayed above the slider
    def updateSliderText(self, value : str) -> str: 
        self.getModel().setTargetSetting(int(value))
        return self.getModel().getSliderText(int(value))

    # Gets options user has selected from the slider and calls the paired function
    # Each function returns an integer -> the target 
    # The target is then set in the dataStructure class 
    def generateTarget(self, value : int) -> int:  
        match value:
            case 0: self.getDataStructure().setTarget(self.__targetRandom())
            case 1: self.getDataStructure().setTarget(self.__targetIn()) 
            case 2: self.getDataStructure().setTarget(self.__targetOut())
            case _: self.getDataStructure().setTarget(self.__targetRandom())

    # Makes sure that target generated has (almost) equal chance to be in the array or not 
    def __targetRandom(self) -> int:         
        # Coin flip to decide if target will be in or out of array 
        if(random.random() < TARGET_SETTING_COIN_FLIP):  return self.__targetIn()
        else: return self.__targetOut()

    # Guarantees target is in the array
    def __targetIn(self) -> int: 
       # Randomly chooses element from array
       return random.choice(self.getDataStructure().get())

    # Guarantees target is not in array
    def __targetOut(self) -> int:   
        array = self.getDataStructure().get()
        return random.choice(list(set([x for x in range(max(array))]) - set(array)))
   
                    
# Listen to Give Me Novacaine by Green Day
