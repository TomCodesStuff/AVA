# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit() 

from typing import Tuple
from .canvas_node import CanvasNode


class CanvasEdge(): 
    # Static variables shared between each instance 
    defaultWeight = 20
    defaultColour = "black"
    editColour = "red"
    defaultSize = "3" 
    hoverSize = "5"


    def __init__(self, coords : tuple) -> None: 
        # On screen coords of the edge
        self.__coords = coords
        # Weight/cost
        self.__weight = CanvasEdge.defaultWeight 
        # On screen colour
        self.__colour = CanvasEdge.defaultColour
        
        # ID used to identify edge on the canvas
        self.__canvasID = -1
        
        # The node that the edges XY coords start at 
        self.__startNode = None  
        # The node that the edges XY coords end at
        self.__endNode = None 
        
        # Size edge should be onscreen 
        self.__screenLen = 0 


    # Getters
    def getCanvasID(self): return self.__canvasID
    def getWeight(self) -> int: return self.__weight 
    def getCoords(self) -> tuple: return self.__coords
    def getStartNode(self) -> CanvasNode|None: return self.__startNode
    def getEndNode(self) -> CanvasNode|None: return self.__endNode
    def getNodes(self) -> Tuple[CanvasNode, CanvasNode]: return (self.__startNode, self.__endNode) 
    def getScreenLen(self) -> int: return self.__screenLen
    def getColour(self) -> str: return self.__colour
    

    # Setters
    def setWeight(self, weight : int) -> None: 
        if weight > 0: self.__weight = weight
    
    def updateCoords(self, coords : tuple) -> None: self.__coords = coords 
    def setStartNode(self, canvasNode : CanvasNode) -> None: self.__startNode = canvasNode 
    def setEndNode(self, canvasNode : CanvasNode) -> None: self.__endNode = canvasNode 
    # TODO error handling and adjustment for screen size
    def setscreenLen(self, val : int): self.__screenLen = val
    def setCanvasID(self, val : int) -> None: self.__canvasID = val  
    def setColour(self, colour : str) -> None: self.__colour = colour


    @staticmethod
    def getDefaultWeight() -> int: return CanvasEdge.defaultWeight

    @staticmethod
    def getDefaultColour() -> int: return CanvasEdge.defaultColour

    @staticmethod
    def getEditColour() -> str: return CanvasEdge.editColour

    @staticmethod
    def getDefaultSize() -> str: return CanvasEdge.defaultSize

    @staticmethod
    def getHoverSize() -> str: return CanvasEdge.hoverSize

# Listen to Live Forever by Oasis 
