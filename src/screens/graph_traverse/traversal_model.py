# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

from typing import Set
from ..algorithm_base import AlgorithmModel
from src.graph_visualisation.graph_components import CanvasNode, CanvasEdge


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

        # Number of nodes that can be on screen at once
        self.__maxNumNodes = 20
        
        # Minimum Weight edges can be 
        self.__minWeight = 1
        # Maximum weight edges can be 
        self.__maxWeight = 100 
        # Default weight given to each edge on creation 
        self.__defaultWeight = 20
        # Resolution of the weight slider
        self.__weightSliderResolution = 1

        # Minimum and Maximum on screen size for edges
        self.__edgeMinScreenLen = 55
        self.__edgeMaxScreenLen = 200

        # Smallest distance nodes can be apart on screen 
        self.__minScreenDist = 50
        # Largest distance nodes can be apart on screen 
        self.__maxScreenDist = 50 

        # Time delay when updating the canvas   
        self.__updateDelay = 50 

        self.__arrowsFont = "Courier New"

    # Getters for distances between nodes on screen 
    def getMinScreenDist(self) -> int: return self.__minScreenDist
    def getMaxScreenDist(self) -> int: return self.__maxScreenDist
    def getMaxNumNodes(self) -> int: return self.__maxNumNodes

    # Getters for edge weight 
    def getMinWeight(self) -> int: return self.__minWeight
    def getMaxWeight(self) -> int: return self.__maxWeight 
    def getDefaultWeight(self) -> int: return self.__defaultWeight
    def getWeightSliderResolution(self) -> int: return self.__weightSliderResolution 

    # Getter for delay used when updating the canvas
    def getUpdateDelay(self) -> int: return self.__updateDelay 

    def getEdgeMinScreenLen(self) -> int: return self.__edgeMinScreenLen
    def getEdgeMaxScreenLen(self) -> int: return self.__edgeMaxScreenLen 

    def getArrowFont(self) -> str: return self.__arrowsFont 


# Listen to Jigsaws Falling Into Place by Radiohead
