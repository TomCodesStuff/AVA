from __future__ import annotations

# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

from typing import Set, TYPE_CHECKING
from src.data_structures import Node 
from .canvas_text import CanvasText

if TYPE_CHECKING: 
    from .canvas_edge import CanvasEdge


class CanvasNode():
    # Static variables shared between each instance 
    nodeID = 0
    defaultSize = 26
    defaultX, defaultY = 5, 5
    defaultCoords = (defaultX, defaultY, defaultX + defaultSize, defaultY + defaultSize)
    defaultColour = "blue" 
    hoverColour = "red"
    startColour = "orange"
    goalColour = "green"
    startGoalColour = "purple"
    minSpawnDist = 10

    def __init__(self, coords : tuple) -> None: 
        # Unique Identifier fot node 
        self.__nodeID = CanvasNode.nodeID 
        CanvasNode.nodeID += 1 
        
        # Reference to abstracted node object
        self.__node = Node(CanvasNode.defaultColour)
        # X-Y Coordindates of the node on screen
        self.__coords = coords
        
        self._displayCoords = (round(coords[0]), round(coords[1]))
        self.__displayedColour = CanvasNode.defaultColour
        
        # Size of the node 
        self.__size = CanvasNode.defaultSize
        # Text displayed in centre of node 
        self.__canvasText = None
        
        # ID of the node on the canvas
        self.__canvasID = None   

        # A set containing references to edges that connects nodes to eachother 
        self.__edges = set()
        # Boolean flag, when a user is moving a node forces are not applied
        self.__isBeingDragged = False  

        # Used to tell refresh loop if nodes needs to be deleted 
        self.__isMarkedForDeletion = False

    # Updates the coordinates of the node to be accurate to the coordinates on screen
    def updateCoords(self, coords : tuple) -> None: 
        if coords: self.__coords = coords

    # Getters 
    def getCanvasID(self) -> int: return self.__canvasID 
    
    def getXCoord(self) -> int: return self.__coords[0]
    
    def getYCoord(self) -> int: return self.__coords[1]
    
    def getCoords(self) -> tuple: return self.__coords
    
    def getID(self) -> int: return self.__nodeID    
    
    def getColour(self) -> str: return self.__node.getColour()
    
    def getEdges(self) -> Set[CanvasEdge]: return self.__edges
    
    def getSize(self) -> int: return self.__size 
    
    def getCanvasText(self) -> CanvasText: return self.__canvasText
    
    def getNode(self) -> Node: return self.__node 
    
    def isMarkedForDeletion(self) -> bool: return self.__isMarkedForDeletion 

    def getDisplayCoords(self) -> tuple: return self._displayCoords 

    def getDisplayedColour(self) -> str: return self.__displayedColour

    def getRequiredPhysicsData(self) -> dict: 
        return {"coords" : list(self.__coords),  "size" : self.__size, "offset" : self.getOffset()}


    # Setters 
    def setCanvasID(self, canvasID : int) -> None:  self.__canvasID = canvasID
    
    def setColour(self, colour : str) -> None: self.__node.setColour(colour)    
    
    def getOffset(self) -> int: return self.__size // 2
    
    def setCanvasText(self, canvasText : CanvasText) -> None: self.__canvasText = canvasText  
    
    def markForDeletion(self) -> None: self.__isMarkedForDeletion = True 

    def updateDisplayCoords(self, newDisplayCoords : tuple) -> None: 
        if not newDisplayCoords: return
        self._displayCoords = newDisplayCoords 

        if self.__canvasText:  
            nodeOffset = self.getOffset()
            self.__canvasText.updateCoords((newDisplayCoords[0] + nodeOffset + 1, 
                                           newDisplayCoords[1] + nodeOffset + 1))


    def updateDisplayedColour(self, newColour : str) -> None: 
        if newColour: self.__displayedColour = newColour

    # Adds a CanvasEdge Object to the list 
    def addEdge(self, canvasEdge : CanvasEdge) -> None: 
        self.__edges.add(canvasEdge) 
        self.__node.addEdge(canvasEdge.getEdge())

    def removeEdge(self, canvasEdge : CanvasEdge) -> None: 
        if canvasEdge in self.__edges: 
            self.__edges.remove(canvasEdge)
            self.__node.removeEdge(canvasEdge.getEdge())

    def applyForces(self, forces : tuple) -> None:  
        # Don't update if node is being dragged by the user here 
        if self.__isBeingDragged: return
        
        forceX, forceY = forces

        # Get top-left coordinates of the node 
        x0, y0, _, _ = self.__coords 
        
        # Calculate new x0 and y0 
        # Coords needed to be rounded to prevent issues with floating point precision 
        newX0 = x0 + forceX
        newY0 = y0 + forceY

        # Update coords
        self.updateCoords((newX0, newY0, newX0 + self.__size, newY0 + self.__size))  
    
    # Function for dragging objects
    def isBeingDragged(self) -> bool: return self.__isBeingDragged
    
    def setDragged(self) -> bool: self.__isBeingDragged = True
    
    def resetDragged(self) -> bool: self.__isBeingDragged = False

    # Used to update on screen ID when a node is deleted 
    def decrementID(self) -> None: 
        self.__nodeID -= 1

    @staticmethod
    def getDefaultSize() -> int: return CanvasNode.defaultSize
    
    @staticmethod 
    def getDefaultCoords() -> tuple: return CanvasNode.defaultCoords 

    @staticmethod 
    def getBaseColour() -> str: return CanvasNode.defaultColour 

    @staticmethod 
    def getHoverColour() -> str: return CanvasNode.hoverColour

    @staticmethod
    def getMinSpawnDistance() -> int: return CanvasNode.minSpawnDist

    @staticmethod
    def resetNodeIDCounter() -> None: CanvasNode.nodeID = 0 

    @staticmethod 
    def decrementNodeIDCounter() -> None: CanvasNode.nodeID -= 1 


# Listen to Paralyzer by Finger Eleven     
