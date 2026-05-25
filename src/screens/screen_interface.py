from __future__ import annotations

# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:  
    from src.app_window import Window


# Abstract class - every screen must implement the render method
class ScreenInterface(ABC):
    def __init__(self, window : Window):
        self.__window = window


    @abstractmethod
    def render(self): pass 


    def getWindow(self) -> Window: 
        return self.__window


# Listen to Runnin' Wild by Airbourne
