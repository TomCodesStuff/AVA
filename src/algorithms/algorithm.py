# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

from abc import ABC, abstractmethod
from src.data_structures import DataStructure
from typing import Generic, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from src.screens import Mediator


D = TypeVar("D", bound="DataStructure")

# Abstract class - every algorithm must implement the getName() method
class Algorithm(Generic[D], ABC):     
    def __init__(self):
        self.__dataStructure = None 
        self.__mediator = None 


    @abstractmethod
    def getName(self): pass 

    @abstractmethod 
    def run(self) -> int: pass

    def setDataStructure(self, dataStructure : D) -> None: 
        if self.__dataStructure is not None: raise Exception("ERROR: Data Structure has already been set")
        self.__dataStructure = dataStructure 
    
    def setMediator(self, mediator : "Mediator") -> None: 
        if self.__mediator is not None: raise Exception("ERROR: Mediator has already been set")
        self.__mediator = mediator 
    
    def invokeBriefDelay(self) -> None: self.__mediator.briefDelay()
    
    def invokeDelay(self) -> None: self.__mediator.delay()
    
    def getDataStructure(self) -> D: 
        return self.__dataStructure

    # Checks if elements at the specified indexes are equal
    # def areElementsEqual(self, i : int, j : int) -> bool: 
    #     return self.getElement(i) == self.getElement(j)


# Listen to American Idiot by Green Day
