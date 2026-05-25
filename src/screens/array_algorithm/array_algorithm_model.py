from ..algorithm_base import AlgorithmModel

class ArrayAlgorithmModel(AlgorithmModel):
    def __init__(self) -> None: 
        super().__init__()

        # Current width of bars
        self.__barWidth = 15
        # Smallest width bars can be 
        self.__minBarWidth = 2
        # Largest bar can be 
        self.__maxBarWidth = 15
        # Distance between each bar 
        self.__barDist = 2
        # Minimum distance between displayed array and edge of canvas
        self.__minPadding = 5
        # Maximum distance between displayed array and edge of canvas
        self.__maxPadding = 20
        # Maximum number of pixels that can be used to draw bars on screen
        self.__maximumPixels = None
        # Lowest value that could appear in the array
        self.__randomLow = 100
        # Highest value that could appear in array
        self.__randomHigh = 5000
        # Lowest value that can actually appear in the array
        self.__lowerBound = None
        # Highest value that can actually appear in the array
        self.__higherBound = None
        # Maximum number of bars that can be drawn, ie the maximum size of the array
        self.__maxBars = None 
                
        # Sets the default resolution of the speed slider 
        self.__defaultResolution = 0.1  
        # The buffer used when selecting a target outside the array 
        self.__buffer = 100

        # Used to adjust bar size and padding when array size changes
        self.__arraySize = 0

    #Getters 

    # Returns width of the bars drawn on screen
    def getBarWidth(self) -> int: return self.__barWidth 
    # Sets width of bars drawn on screen to passed value
    def setBarWidth(self, value : int) -> None: self.__barWidth = value 
    # Returns the smallest width the bars can be
    def getMinBarWidth(self) -> int: return self.__minBarWidth 
    # Returns the largest width the bars can be
    def getMaxBarWidth(self) -> int: return self.__maxBarWidth 
    # Returns the distance between each bar
    def getBarDistance(self) -> int: return self.__barDist 
    # Returns minimum padding between the first/last bars and the edges of the canvas
    def getMinPadding(self) -> int: return self.__minPadding 
    # Returns maximium padding between the first/last bars and the edges of the canvas
    def getMaxPadding(self) -> int: return self.__maxPadding 
    # Returns maximum number of pixels that can be used to draw bars
    def getMaximumPixels(self) -> int: return self.__maximumPixels 
    # Gets the absolute lowest number that could appear in the array
    def getLowestRandomBound(self) -> int: return self.__randomLow
    # Gets the absolute highest number that could appear in the array 
    def getHighestRandomBound(self) -> int: return self.__randomHigh 
    # Gets the lowest the number that can appear in the array
    def getLowerBound(self) -> int: return self.__lowerBound 
    # Gets the highest value that can appear in the array
    def getHigherBound(self) -> int: return self.__higherBound 
    # Get maximum bars that can be drawn on screen
    def getMaxBars(self) -> int: return self.__maxBars 
    # Gets the default resolution 
    def getDefaultResolution(self): return self.__defaultResolution
    # Gets the buffer used when selecting a target outside the array 
    def getBuffer(self): return self.__buffer 
    # Get last recorded array size
    def getArraySize(self) -> int: return self.__arraySize

    # Setters

    # Sets the minimum distance between the first/last bars and the edges of the canvas 
    # to the passed value
    def setMinPadding(self, value : int) -> None: self.__minPadding = value
    # Sets maximum pixels to passed value
    def setMaximumPixels(self, value : int) -> None: self.__maximumPixels = value 
    # Sets the lowest number that can appear in the array to the value passed
    def setLowerBound(self, value : int) -> None: self.__lowerBound = value 
    # Set maximum bars that can be drawn on screen to passed value
    def setMaxBars(self, value : int) -> None: self.__maxBars = value 
    # Set the highest value that can appear in the array to the value passed
    def setHigherBound(self, value : int) -> None: self.__higherBound = value 
    # Update array size
    def setArraySize(self, value : int) -> None: self.__arraySize = value

# Listen to The Adults Are Talking by The Strokes
        