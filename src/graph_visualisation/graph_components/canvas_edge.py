# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit() 


import math
from typing import Tuple
from .canvas_node import CanvasNode
from src.data_structures import Edge 
from src.enums import EdgeDirection

class CanvasEdge(): 
    # Static variables shared between each instance 
    defaultWeight = 20 
    defaultScreenLen = 150
    defaultColour = "black"
    editColour = "red"
    defaultSize = "3" 
    hoverSize = "5"
    defaultDirection = EdgeDirection.BIDIRECTIONAL

    def __init__(self, coords : tuple) -> None: 
        self.__edge = Edge(CanvasEdge.defaultWeight, CanvasEdge.defaultColour, CanvasEdge.defaultDirection)

        # On screen coords of the edge
        self.__coords = coords
        # Visible length on screen
        self.__screenLen = CanvasEdge.defaultScreenLen
        
        # ID used to identify edge on the canvas
        self.__canvasID = -1
        
        # The node that the edges XY coords start at 
        self.__firstCanvasNode = None  
        # The node that the edges XY coords end at
        self.__secondCanvasNode = None 
        

    # Getters
    def getCanvasID(self): return self.__canvasID
    
    def getWeight(self) -> int: return self.__edge.getWeight() 
    
    def getScreenLen(self) -> int: return self.__screenLen
    
    def getCoords(self) -> tuple: return self.__coords
    
    def getFirstNode(self) -> CanvasNode|None: return self.__firstCanvasNode
    
    def getSecondNode(self) -> CanvasNode|None: return self.__secondCanvasNode
    
    def getNodes(self) -> Tuple[CanvasNode, CanvasNode]: return (self.__firstCanvasNode, self.__secondCanvasNode) 
    
    def getColour(self) -> str: return self.__edge.getColour() 
    
    def getDirection(self) -> EdgeDirection: return self.__edge.getDirection()
    
    # Setters
    def setWeight(self, weight : int) -> None: 
        if weight > 0: self.__edge.setWeight(weight) 
    
    def setScreenLen(self, screenLen : int) -> None: 
        if screenLen > 0: self.__screenLen = screenLen
    
    def setFirstNode(self, canvasNode : CanvasNode) -> None: self.__firstCanvasNode = canvasNode 
    
    def setSecondNode(self, canvasNode : CanvasNode) -> None: self.__secondCanvasNode = canvasNode 
    
    def setCanvasID(self, val : int) -> None: self.__canvasID = val  
    
    def setColour(self, colour : str) -> None: self.__edge.setColour(colour) 
    
    def setDirection(self, direction : EdgeDirection) -> None: self.__edge.setDirection(direction) 
    
    def updateCoords(self, coords : tuple) -> None: self.__coords = coords 


    # Stole from ChatGPT would take me way to long to find an acceptable solution :/
    # I dislike using AI as I think it's kinda cheating but I'll make an exception to finish this project
    # Makes arrows indicating edge direction visible rather than just being hidden behind each node
    def adjustDirectionArrows(self) -> tuple:
        x0, y0, x1, y1 = self.__coords 
        r0 = self.__firstCanvasNode.getOffset()
        r1 = self.__secondCanvasNode.getOffset()

        dx = x1 - x0 
        dy = y1 - y0

        dist = math.sqrt(dx ** 2 + dy ** 2)

        if dist == 0: return (x0, y0, x1, y1)

        adjustedX0, adjustedY0 = x0, y0 
        adjustedX1, adjustedY1 = x1, y1

        if self.__edge.getDirection() in (EdgeDirection.SECOND_TO_FIRST, EdgeDirection.BIDIRECTIONAL):
            adjustedX0 = math.ceil(x0 + (dx / dist) * r0)
            adjustedY0 = math.ceil(y0 + (dy / dist) * r0)
        if self.__edge.getDirection() in (EdgeDirection.FIRST_TO_SECOND, EdgeDirection.BIDIRECTIONAL):
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

    @staticmethod 
    def setDefaultScreenLen(defaultScreenLen : int): CanvasEdge.defaultScreenLen = defaultScreenLen

# Listen to Live Forever by Oasis 
