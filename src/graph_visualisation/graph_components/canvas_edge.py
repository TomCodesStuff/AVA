# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit() 


import math
from typing import Tuple
from .canvas_node import CanvasNode
from .canvas_text import CanvasText
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
        self.__canvasID = None
        
        # The node that the edges XY coords start at 
        self.__firstCanvasNode = None  
        # The node that the edges XY coords end at
        self.__secondCanvasNode = None 

        self.__isMarkedForDeletion = False

        # Displays weights next to the edge when algorithm is running
        self.__canvasWeightText = None

        self.__displayedCoords = coords
        self.__displayedColour = CanvasEdge.defaultColour
        
    # Getters
    def getCanvasID(self): return self.__canvasID

    def getWeight(self) -> int: return self.__edge.getWeight() 
    
    def getScreenLen(self) -> int: return self.__screenLen
    
    def getCoords(self) -> tuple: return self.__coords
    
    def getFirstCanvasNode(self) -> CanvasNode|None: return self.__firstCanvasNode
    
    def getSecondCanvasNode(self) -> CanvasNode|None: return self.__secondCanvasNode
    
    def getCanvasNodes(self) -> Tuple[CanvasNode, CanvasNode]: return (self.__firstCanvasNode, self.__secondCanvasNode) 
    
    def getColour(self) -> str: return self.__edge.getColour() 
    
    def getDirection(self) -> EdgeDirection: return self.__edge.getDirection() 

    def getEdge(self) -> Edge: return self.__edge 

    def getWeightCanvasText(self) -> CanvasText | None: return self.__canvasWeightText 

    def isMarkedForDeletion(self) -> bool: return self.__isMarkedForDeletion

    def getDisplayCoords(self) -> tuple: return self.__displayedCoords

    def getDisplayColour(self) -> str: return self.__displayedColour
    
    def getRequiredPhysicsData(self) -> dict: 
        return {"firstNode" : self.__firstCanvasNode.getCanvasID(), 
                "secondNode" : self.__secondCanvasNode.getCanvasID(), 
                "screenlen" : self.__screenLen, 
                "direction" : self.__edge.getDirection()}

    # Setters
    def setWeight(self, weight : int) -> None:  
        if weight <= 0: return
        self.__edge.setWeight(weight) 
        if self.__canvasWeightText: self.__canvasWeightText.updateText(str(weight))
    
    def setScreenLen(self, screenLen : int) -> None: 
        if screenLen > 0: self.__screenLen = screenLen
    
    def setFirstCanvasNode(self, canvasNode : CanvasNode) -> None: 
        if self.__firstCanvasNode is not None: return
        self.__firstCanvasNode = canvasNode  
        self.__edge.setFirstNode(canvasNode.getNode())
    
    def syncDirection(self) -> None:
        if self.__edge.getDirection() == EdgeDirection.BIDIRECTIONAL:
            self.__firstCanvasNode.getNode().addEdge(self.__edge) 
            self.__secondCanvasNode.getNode().addEdge(self.__edge)  
        elif self.__edge.getDirection() == EdgeDirection.FIRST_TO_SECOND: 
            self.__firstCanvasNode.getNode().addEdge(self.__edge)
            self.__secondCanvasNode.getNode().removeEdge(self.__edge)
        elif self.__edge.getDirection() == EdgeDirection.SECOND_TO_FIRST: 
            self.__firstCanvasNode.getNode().removeEdge(self.__edge)
            self.__secondCanvasNode.getNode().addEdge(self.__edge)

    def setSecondCanvasNode(self, canvasNode : CanvasNode) -> None: 
        if self.__secondCanvasNode is not None: return
        self.__secondCanvasNode = canvasNode 
        self.__edge.setSecondNode(canvasNode.getNode())
    
    def setCanvasID(self, val : int) -> None: self.__canvasID = val  
    
    def setColour(self, colour : str) -> None: self.__edge.setColour(colour) 
    
    def setDirection(self, direction : EdgeDirection) -> None: 
        self.__edge.setDirection(direction) 
        self.syncDirection()
    
    def updateCoords(self, coords : tuple) -> None: 
        if coords: self.__coords = coords  
        
    def markForDeletion(self) -> None: self.__isMarkedForDeletion = True 

    def updateDisplayCoords(self, newCoords : tuple) -> None: 
        if newCoords: self.__coords = newCoords

    def updateDisplayColour(self, newColour : str) -> None: 
        if newColour: self.__displayedColour = newColour

    def setCanvasWeightText(self, canvasWeightText : CanvasText) -> None: 
        self.__canvasWeightText = canvasWeightText

    @staticmethod
    def getDefaultWeight() -> int: return CanvasEdge.defaultWeight

    @staticmethod
    def getBaseColour() -> int: return CanvasEdge.defaultColour

    @staticmethod
    def getEditColour() -> str: return CanvasEdge.editColour

    @staticmethod
    def getDefaultSize() -> str: return CanvasEdge.defaultSize

    @staticmethod
    def getHoverSize() -> str: return CanvasEdge.hoverSize 

    @staticmethod 
    def setDefaultScreenLen(defaultScreenLen : int): CanvasEdge.defaultScreenLen = defaultScreenLen

# Listen to Live Forever by Oasis 
