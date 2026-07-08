import random
from typing import List
from src.data_structures import DataStructure


class Array(DataStructure[int]): 
    # Constructor
    def __init__(self):
        super().__init__()
        self.__array = []
        self.__barColours = []

    def __len__(self)  -> int:
        return len(self.__array)

    # Returns the array
    def get(self) -> List[int]: 
        return self.__array.copy()

    def getBarColours(self) -> List[str]:
        return self.__barColours

    # Appends passed value to the array
    def append(self, value : int) -> None: 
        self.__array.append(value)
        self.__barColours.append("black")
    
    # Removes last element from the array
    def pop(self) -> None: 
        self.__array.pop()
        self.__barColours.pop()

    # Sorts the array
    def sort(self) -> None:
        self.__array.sort()

    # Shuffles the array
    def shuffle(self) -> None:
        random.shuffle(self.__array)

    # Changes the element at the specified index to the passed value
    def setAt(self, index : int, value : int) -> None: 
        if(index >= self.size()): return
        self.__array[index] = value
    
    # Returns element at the specified index 
    def getAt(self, index : int) -> int:
        return self.__array[index]

    # Gets the colour of the bar the index passed
    def getColourAt(self, index : int) -> str:
        if(index >= len(self.__array)): return "" 
        else: return self.__barColours[index]
    
    # Sets the bar colour at the specified index to the specified colour
    def setColourAt(self, index : int, colour: str) -> None: 
        if(index >= len(self.__array)): return 
        else: self.__barColours[index] = colour

    # Resets all the bars colours to the default (black)
    def resetBarColours(self) -> None: 
        self.__barColours = ["black" for _ in range(len(self.__array))] 
    
    def setAllColours(self, colour : str) -> None: 
        for i in range(len(self.__barColours)): 
            self.__barColours[i] = colour
    
    # Returns the size of the array
    def size(self) -> int:
        return len(self.__array)

    # Returns the smallest element in the array
    def getMin(self) -> int:
        return min(self.__array)

    # Returns the largest element in the array 
    def getMax(self) -> int:
        return max(self.__array)

    # Returns true if passed value is in the array, else false
    def isInArray(self, value : int) -> bool: 
        return value in self.__array 
    
    def __str__(self) -> str:
        return "Array: " + ", ".join([str(x) for x in self.__array])

    def __iter__(self):
        return iter(self.__array)


# Listen to Everlong By Foo Fighters
        