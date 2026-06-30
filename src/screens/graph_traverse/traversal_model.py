# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from src.screens.algorithm_base import AlgorithmModel


RESOLUTION = 1
MIN_DELAY = 1
MAX_DELAY = 1000


class TraversalModel(AlgorithmModel):
    def __init__(self): 
        super().__init__() 

        self.setDelayToMilliseconds()
        self.setResolution(RESOLUTION)
        self.setMinDelay(MIN_DELAY)
        self.setMaxDelay(MAX_DELAY)

        # Mininmum number of nodes that should be on screen
        self.__minNumNodes = 2
        # Number of nodes that can be on screen at once
        self.__maxNumNodes = 20
        
        # Minimum Weight edges can be 
        self.__minWeight = 1
        # Maximum weight edges can be 
        self.__maxWeight = 100  

        # Minimum and Maximum on screen size for edges
        self.__edgeMinScreenLen = 100
        self.__edgeMaxScreenLen = 200

        screenLenRange = self.__edgeMaxScreenLen - self.__edgeMinScreenLen
        edgeWeightRange = self.__maxWeight - self.__minWeight

        # Calculate slope once and store it -> does not need to be calculated each time weight is changed
        self.__slope = screenLenRange // edgeWeightRange

        # Resolution of the weight slider
        self.__weightSliderResolution = 1

        self.__arrowsFont = "Courier New" 

        self.__weightTextFont = ("Arial", 10, "bold") 

        # How far away from edge text will be displayed 
        self.__weightTextOffset = 12

    def getMinNumNodes(self) -> int: return self.__minNumNodes

    def getMaxNumNodes(self) -> int: return self.__maxNumNodes

    # Getters for edge weight 
    def getMinEdgeWeight(self) -> int: return self.__minWeight
    
    def getMaxEdgeWeight(self) -> int: return self.__maxWeight 
    
    def getWeightSliderResolution(self) -> int: return self.__weightSliderResolution 

    def getRangeSlope(self) -> int: return self.__slope

    def getEdgeMinScreenLen(self) -> int: return self.__edgeMinScreenLen
    
    def getEdgeMaxScreenLen(self) -> int: return self.__edgeMaxScreenLen 

    def getArrowFont(self) -> str: return self.__arrowsFont 

    def getWeightTextFont(self) -> tuple: return self.__weightTextFont

    def getWeightTextOffset(self) -> int: return self.__weightTextOffset

# Listen to Jigsaws Falling Into Place by Radiohead
