import random
from typing import TYPE_CHECKING, TypeVar
from ..algorithm_base import AlgorithmController
from src.data_structures import Array

if TYPE_CHECKING: 
    from src.screens.array_algorithm import ArrayAlgorithmScreen, ArrayAlgorithmModel

S = TypeVar("S", bound="ArrayAlgorithmScreen")
M = TypeVar("M", bound="ArrayAlgorithmModel")
D = TypeVar("D", bound="Array")

CANVAS_OFFSET = 2
ELEMENT_OFFSET = 20 


class ArrayAlgorithmController(AlgorithmController[S, M, D]):
    def __init__(self, screen : S, model : M, dataStructure : D) -> None: 
        super().__init__(screen, model, dataStructure)

    def calculateArrayBounds(self) -> None:
        # Returns the height of the canvas - maximum number of pixels an element can possibly have
        self.getModel().setMaximumPixels(self.__calculateMaximumPixels())
        # Calculates spacing between canvas border and displayed array 
        # Is also used to calculate the largest possible size of the array
        self.getModel().setMinPadding(self.__calculateBestPadding())
        # Calculate largest and smallest values that can be put in the array
        self.__calculateArrayBounds()

    # Largest number that can be displayed on screen
    def __calculateMaximumPixels(self) -> int:
        # Two is taken from the canvas' height because the canvas widget has a border where no pixels are drawn   
        return self.getScreen().getCanvas().winfo_height() - CANVAS_OFFSET

    # Finds the best distance between the displayed array and the edges of canvas, 
    # to maximise the number of elements and centre the array as best as possible
    def __calculateBestPadding(self) -> int:
        for i in range(self.getModel().getMinPadding(), self.getModel().getMaxPadding()):
            # Calculates how many bars can be displayed on the screen 
            bars = self.__calculateMaxBars(self.getModel().getMinBarWidth(), i)  
            # If the number of bars is a whole number
            if(bars.is_integer()):  
                # Maximum size the array can be 
                self.getModel().setMaxBars(int(bars))
                # Function terminates - returning the best padding (i)
                return i
        # If no whole number can be found, just use the max padding (the array being off centre is less noticeable) 
        maxBars = round(self.__calculateMaxBars(self.getModel().getMinBarWidth(), self.getModel().getMaxPadding())) 
        self.getModel().setMaxBars(maxBars)
        return self.getModel().getMaxPadding()

    # Calculates maximum number of bars that can be displayed given the padding
    def __calculateMaxBars(self, barWidth, padding) -> int:
        return ((self.getScreen().getCanvas().winfo_width()) - (padding * 2)) / (barWidth + self.getModel().getBarDistance())


    # Calculates the padding to centre the array of a given size
    def __calculatePadding(self) -> int:
        return ((self.getScreen().getCanvas().winfo_width() - (len(self.getDataStructure().get()) 
                                                               * (self.getModel().getBarDistance() + self.getModel().getBarWidth()))) // 2) \
                                                                + self.getModel().getBarDistance()

    def __clampArray(self) -> None:
        if self.getDataStructure().size() <= self.getModel().getMaxBars(): return 
        for _ in range(self.getModel().getMaxBars(), self.getDataStructure().size()): 
            self.getDataStructure().pop()  
        self.getModel().setArraySize(self.getDataStructure().size())

    def adjustArray(self, value : int) -> None: 
        # Add or remove elements depending on slider value
        if(value < len(self.getDataStructure().get())): self.__deleteElements(value)
        else: self.__addElements(value)
        self.refreshCanvas()

    # Adjusts size of bars so amount of elements can fit on screen and stay in the canvas' centre
    def __adjustBarLayout(self) -> None: 
        prevArraySize = self.getModel().getArraySize()
        # Clamp array to Maximum Number bars if too big 
        self.__clampArray()
        
        if prevArraySize < self.getDataStructure().size():
            self.__decreaseBarSize()
        elif prevArraySize > self.getDataStructure().size(): 
            self.__increaseBarSize()

        # Only recalculate padding if array size changed
        if prevArraySize != self.getDataStructure().size():
            # Calculate padding if maximum bar size not reached
            if(len(self.getDataStructure().get()) != self.getModel().getMaxBars()): 
                self.__padding = self.__calculatePadding()
            else: self.__padding = self.getModel().getMinPadding()
            
        # The amount each elements is stretched along the y-axis 
        # Means the elements are scaled with the largest element
        self.yStretch = self.getModel().getMaximumPixels() / max(self.getDataStructure().get())
        self.getModel().setArraySize(self.getDataStructure().size())

    # Iterates through array, drawing each bar
    def refreshCanvas(self, refreshColours : bool=True) -> None:
            # Do Checks with padding here 
            self.__adjustBarLayout()
            
            if refreshColours:
                self.getDataStructure().resetBarColours()

            # Clear displayed array on screen
            self.__clearDisplayedArray()
            for x, y in enumerate(self.getDataStructure().get()):
                # Calculate where each bar is placed on screen
                # Bottom left co-ord
                x1 = x * self.getModel().getBarDistance() + x * self.getModel().getBarWidth() + self.__padding
                # Top left coord
                y1 = self.getScreen().getCanvas().winfo_height() - (y * self.yStretch)  
                # Bottom right coord
                x2 = x * self.getModel().getBarDistance() + x * self.getModel().getBarWidth()+ self.getModel().getBarWidth() + self.__padding
                # Top right coord
                y2 = self.getScreen().getCanvas().winfo_height() 
                # Chooses correct colour for bar to be filled in with
                self.getScreen().getCanvas().create_rectangle(x1, y1, x2, y2, fill = self.getDataStructure().getColourAt(x)) 
            
            # Updates screen so bars can be seen onscreen
            self.getScreen().getWindow().update_idle_tasks() 
            
    # Wipes everything off the canvas
    def __clearDisplayedArray(self) -> None:
        self.getScreen().getCanvas().delete("all")

    # Adds amount of elements corresponding to the value
    def __addElements(self, value):
        for _ in range(len(self.getDataStructure().get()), value):
            # Choose random number inbetween upper and lower bounds
            self.getDataStructure().append(random.randint(self.getModel().getLowerBound(), self.getModel().getHigherBound()))

    # Deletes number of elements corresponding to the value
    def __deleteElements(self, value) -> None:
        for _ in range(len(self.getDataStructure().get()), value, -1):
            self.getDataStructure().pop()

    # Determines if bars need to shrink in size as array grows
    def __decreaseBarSize(self) -> None:
        for i in range(self.getModel().getBarWidth(), self.getModel().getMinBarWidth(), -1):
            if(len(self.getDataStructure().get()) < round(self.__calculateMaxBars(i, self.getModel().getMaxPadding()))):
                self.getModel().setBarWidth(i)
                return 
        self.getModel().setBarWidth(self.getModel().getMinBarWidth())

    # Determines if bars needs to increase in size as array shrinks
    def __increaseBarSize(self) -> None:
        for i in range(self.getModel().getBarWidth() + 1, self.getModel().getMaxBarWidth() + 1):
             if(len(self.getDataStructure().get()) < round(self.__calculateMaxBars(i, self.getModel().getMaxPadding()))): 
                self.getModel().setBarWidth(i)

    # Calculate upper and lower bounds of the array
    def __calculateArrayBounds(self) -> None:
        # Calculate maximum value the array can have by:
        # Choosing an arbitrary number between randomLow and randomHigh and doubling it 
        higherBound = random.randint(self.getModel().getLowestRandomBound(), self.getModel().getHighestRandomBound()) * 2  
        self.getModel().setHigherBound(higherBound)
        
        # Long explanation time...
        # Lower is the absolute minimum value that can appear on screen 
        # Bars are only visible if the top right coorindate is less than or equal to the value of maximumPixels - 0.5 
        # So lower can be calculated be rearranging the y1 coord equation to solve for y
        # 0.5 was rounded up to 1 because it looks nicer
        lowerBound = round((self.getScreen().getCanvas().winfo_height() - self.getModel().getMaximumPixels() + 1) 
                                  / (self.getModel().getMaximumPixels() / self.getModel().getHigherBound()))  
        self.getModel().setLowerBound(lowerBound)
        
# Listen to Generator by Foo Fighters 
        