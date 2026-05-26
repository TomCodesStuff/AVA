# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit() 


import math
from typing import Tuple
from .canvas_node import CanvasNode
from src.enums import EdgeDirection

class CanvasEdge(): 
    # Static variables shared between each instance 
    defaultWeight = 20
    defaultColour = "black"
    editColour = "red"
    defaultSize = "3" 
    hoverSize = "5"
    defaultDirection = EdgeDirection.BIDIRECTIONAL

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
        self.__firstNode = None  
        # The node that the edges XY coords end at
        self.__secondNode = None 
        # Set direction to default (Bidirectional)
        self.__direction = CanvasEdge.defaultDirection
        

    # Getters
    def getCanvasID(self): return self.__canvasID
    def getWeight(self) -> int: return self.__weight 
    def getCoords(self) -> tuple: return self.__coords
    def getFirstNode(self) -> CanvasNode|None: return self.__firstNode
    def getSecondNode(self) -> CanvasNode|None: return self.__secondNode
    def getNodes(self) -> Tuple[CanvasNode, CanvasNode]: return (self.__firstNode, self.__secondNode) 
    def getColour(self) -> str: return self.__colour 
    def getDirection(self) -> EdgeDirection: return self.__direction
    
    # Setters
    def setWeight(self, weight : int) -> None: 
        if weight > 0: self.__weight = weight
    
    def updateCoords(self, coords : tuple) -> None: self.__coords = coords 
    def setFirstNode(self, canvasNode : CanvasNode) -> None: self.__firstNode = canvasNode 
    def setSecondNode(self, canvasNode : CanvasNode) -> None: self.__secondNode = canvasNode 
    def setCanvasID(self, val : int) -> None: self.__canvasID = val  
    def setColour(self, colour : str) -> None: self.__colour = colour 
    def setDirection(self, direction : EdgeDirection) -> None: self.__direction = direction 


    # Stole from ChatGPT would take me way to long to find an acceptable solution :/
    # I dislike using AI as I think it's kinda cheating but I'll make an exception to finish this project
    # Makes arrows indicating edge direction visible rather than just being hidden behind each node
    def showDirectionArrows(self) -> tuple:
        x0, y0, x1, y1 = self.__coords 

        r0 = self.__firstNode.getOffset()
        r1 = self.__secondNode.getOffset()

        dx = x1 - x0 
        dy = y1 - y0

        dist = math.sqrt(dx ** 2 + dy ** 2)

        if dist == 0: return (x0, y0, x1, y1)

        adjustedX0, adjustedY0 = x0, y0 
        adjustedX1, adjustedY1 = x1, y1

        if self.__direction in (EdgeDirection.SECOND_TO_FIRST, EdgeDirection.BIDIRECTIONAL):
            adjustedX0 = math.ceil(x0 + (dx / dist) * r0)
            adjustedY0 = math.ceil(y0 + (dy / dist) * r0)
        if self.__direction in (EdgeDirection.FIRST_TO_SECOND, EdgeDirection.BIDIRECTIONAL):
            adjustedX1 = math.ceil(x1 - (dx / dist) * r1)
            adjustedY1 = math.ceil(y1 - (dy / dist) * r1)

        return (adjustedX0, adjustedY0, adjustedX1, adjustedY1)


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
