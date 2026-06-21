from typing import Callable
from tkinter import Canvas, Event 
from ..graph_components import CanvasGraph, CanvasNode, CanvasEdge
from ..tools import * 

class EventsHandler(): 
    def __init__(self, canvas : Canvas, canvasGraph : CanvasGraph, maxNumNodes : int):
        self.__canvas = canvas
        self.__canvasGraph = canvasGraph
                
        self.__creationTool = CreationTool()
        self.__hoverTool = HoverTool()
        self.__movementTool = MovementTool(self.__canvas.winfo_width(), self.__canvas.winfo_height())

        # Flags to prevent events being incorrectly triggered 
        self.__isNodeBeingDeleted = False 
        self.__isEdgeBeingDrawn = False 
        self.__isEdgeBeingEdited = False  
        self.__isEdgeBeingDeleted = False
        # Disable events when algorithms are running  
        self.__isAlgorithmRunning = False

        self.__edgeBeingDrawn = None  
        self.__edgeBeingEdited = None   

        # Maximum Number of nodes 
        self.__maxNumNodes = maxNumNodes

        # Function to show edge options in the GUI
        self.__showEdgeOptions = None 

        self.__addCanvasEvents()

    def __canSpawnEventTrigger(self) -> bool: 
        if self.__isAlgorithmRunning: return False
        if self.__isNodeBeingDeleted: 
            self.__isNodeBeingDeleted = False
            return False
        if self.__isEdgeBeingDeleted: 
            self.__isEdgeBeingDeleted = False
            return False
        if self.__isEdgeBeingDrawn: return False
        return True 

    def __spawnNodeDoubleClick(self, event : Event) -> None: 
        if not self.__canSpawnEventTrigger(): return 

        circleOffset = CanvasNode.getDefaultSize() // 2
        x0, y0 = event.x - circleOffset, event.y - circleOffset
        x1, y1 = event.x + circleOffset, event.y + circleOffset 
        self.spawnNode((x0, y0, x1, y1)) 
   
    def __deleteEdgeOnClick(self, event : Event) -> None: 
        if any([self.__isAlgorithmRunning, self.__isEdgeBeingDeleted, self.__edgeBeingDrawn is None]): return
        
        object_collisions = self.__canvas.find_overlapping(event.x, event.y , event.x, event.y) 
        if(len(object_collisions) == 1 and self.__edgeBeingDrawn.getCanvasID() in object_collisions): 
            self.__removeCanvasMotionEvent()
            self.__isEdgeBeingDrawn = False

            self.__canvas.delete(self.__edgeBeingDrawn.getCanvasID()) 
            self.__canvasGraph.deleteCanvasEdge(self.__edgeBeingDrawn)
            self.__edgeBeingDrawn = None 

    def __addCanvasEvents(self) -> None: 
        if self.__canvas is None: return 
        # Add event to delete current edge being drawn when the canvas is clicked
        self.__canvas.bind("<Button-1>", lambda event: self.__deleteEdgeOnClick(event))
        self.__canvas.bind("<Double-Button-1>", lambda event: self.__spawnNodeDoubleClick(event))

    def __moveNode(self, event : Event, canvasNode : CanvasNode) -> None:   
        if self.__isAlgorithmRunning: return
        
        self.__resetEdgeDrawingEvent()
        self.__isEdgeBeingDrawn = False 
        # Stops the node from only being partially rendered (not sure why this works, I forgot)
        self.__canvas.config(cursor="arrow")
        canvasNode.setColour(CanvasNode.getHoverColour())
        canvasNode.setDragged()
        self.__movementTool.moveNode(canvasNode, (event.x, event.y)) 
    
    def __resetDragged(self, canvasNode : CanvasNode): 
        canvasNode.resetDragged()

    def deleteNode(self, canvasNode : CanvasNode) -> None:  
        if self.__isAlgorithmRunning or self.__isEdgeBeingEdited: return
        self.__isNodeBeingDeleted = True  

        # The event to draw an edge can still trigger so it needs to be deleted
        self.__deleteEdge(self.__edgeBeingDrawn)
        self.__resetEdgeDrawingEvent()
        
        # Not to thrilled about making a copy here but it's the best option
        for canvasEdge in list(canvasNode.getEdges()): 
            self.__deleteEdge(canvasEdge)
            
        self.__canvas.delete(canvasNode.getCanvasID())  
        self.__canvasGraph.deleteCanvasNode(canvasNode)

    def __drawEdge(self, eventCoords : tuple, canvasEdge : CanvasEdge) -> None: 
        eventX, eventY = eventCoords
        object_collisions = self.__canvas.find_overlapping(eventX, eventY, eventX, eventY)
        if canvasEdge.getFirstNode().getCanvasID() in object_collisions: return 
        self.__movementTool.moveEdge(canvasEdge, eventCoords)
        if canvasEdge.getCanvasID() == -1: 
            self.__creationTool.renderEdge(self.__canvas, canvasEdge)  
        else: self.__creationTool.redrawEdge(self.__canvas, canvasEdge)

    def __removeCanvasMotionEvent(self) -> None: 
        self.__canvas.unbind("<Motion>")

    def __addCanvasMotionEvent(self, canvasEdge : CanvasEdge) -> None:
        self.__canvas.bind("<Motion>", lambda event: self.__drawEdge((event.x, event.y), canvasEdge))

    def __areEdgeNodesDifferent(self, edgeStartNode : CanvasNode, edgeEndNode : CanvasNode) -> bool:
        return edgeStartNode != edgeEndNode

    def __deleteEdge(self, canvasEdge : CanvasEdge) -> None:  
        if canvasEdge is None: return
        self.__canvas.delete(canvasEdge.getCanvasID()) 
        self.__canvasGraph.deleteCanvasEdge(canvasEdge)
        
    def __resetEdgeDrawingEvent(self) -> None:
        self.__removeCanvasMotionEvent() 
        self.__isEdgeBeingDrawn = False 
        self.__edgeBeingDrawn = None  

    def __canEdgeBeCreated(self, canvasEdge : CanvasEdge, canvasNode : CanvasNode) -> None: 
        return self.__areEdgeNodesDifferent(canvasEdge.getFirstNode(), canvasNode)\
            and not self.__canvasGraph.areNodesConnected((canvasEdge.getFirstNode(), canvasNode))

    def __nodeOnClick(self, canvasNode : CanvasNode) -> None: 
        # If an edge is being edited or algorithm is running, prevent a new one from being created
        if self.__isAlgorithmRunning or self.__isEdgeBeingEdited: return
        
        # If an edge is already being drawn on screen
        if self.__isEdgeBeingDrawn:
            if self.__canEdgeBeCreated(self.__edgeBeingDrawn, canvasNode): 
                self.__canvasGraph.addCanvasEdge(self.__edgeBeingDrawn)
                self.__edgeBeingDrawn.setSecondNode(canvasNode)  
                self.__movementTool.connectEdgeToNodes(self.__edgeBeingDrawn)
                self.__addEdgeEvents(self.__edgeBeingDrawn) 
                self.__canvasGraph.addEdgeToNodes(self.__edgeBeingDrawn)
                self.__editEdge(self.__edgeBeingDrawn)
            else: self.__deleteEdge(self.__edgeBeingDrawn)
            self.__resetEdgeDrawingEvent()
        else:
            self.__isEdgeBeingDrawn = True  
            canvasEdge = self.__creationTool.createEdge(canvasNode) 
            self.__edgeBeingDrawn = canvasEdge
            self.__addCanvasMotionEvent(canvasEdge) 
    
    def __editEdge(self, canvasEdge : CanvasEdge) -> None:
        canvasEdge.setColour(CanvasEdge.getEditColour())
        if self.__showEdgeOptions: self.__showEdgeOptions(canvasEdge)
        self.__edgeBeingEdited = canvasEdge
        self.__isEdgeBeingEdited = True

    def __editEdgeOnClick(self, canvasEdge : CanvasEdge) -> None:  
        if any([self.__isAlgorithmRunning, self.__isEdgeBeingDrawn, 
               self.__isEdgeBeingEdited, self.__showEdgeOptions is None]): return
        self.__editEdge(canvasEdge)

    # Add event handlers to edges for interactability 
    def __addEdgeEvents(self, canvasEdge : CanvasEdge) -> None:          
        # TODO -> probably best/easiest to have references to relevant screen functions 
        self.__canvas.tag_bind(canvasEdge.getCanvasID(), "<Button-1>", lambda _: self.__editEdgeOnClick(canvasEdge))
        self.__canvas.tag_bind(canvasEdge.getCanvasID(), "<Enter>", 
                               lambda _: self.__hoverTool.edgeOnHover(self.__canvas, canvasEdge))
        self.__canvas.tag_bind(canvasEdge.getCanvasID(), "<Leave>", 
                               lambda _: self.__hoverTool.edgeOnLeave(self.__canvas, canvasEdge)) 

    # Add event handlers to the newly created node
    def __addNodeEvents(self, canvasNode : CanvasNode) -> None:     
        # Add event to change nodes colour when the mouse hovers over it
        self.__canvas.tag_bind(canvasNode.getCanvasID(), "<Enter>", lambda _: self.__hoverTool.nodeOnHover(canvasNode))
        # Add event to change nodes colour when the mouse stops hovering over it
        self.__canvas.tag_bind(canvasNode.getCanvasID(), "<Leave>", lambda _: self.__hoverTool.nodeOnLeave(canvasNode)) 
        # Add event listener to move node when it's dragged by the mouse 
        self.__canvas.tag_bind(canvasNode.getCanvasID(), "<B1-Motion>", lambda event: self.__moveNode(event, canvasNode))    
        
        # Add event listener to detect when mouse button released 
        self.__canvas.tag_bind(canvasNode.getCanvasID(), "<ButtonRelease-1>", lambda _: self.__resetDragged(canvasNode))
        
        # Add event listener to add an edge when a node is clicked 
        self.__canvas.tag_bind(canvasNode.getCanvasID(), "<Button-1>", lambda _: self.__nodeOnClick(canvasNode))
        # Add event to delete a node when it is double clicked 
        self.__canvas.tag_bind(canvasNode.getCanvasID(), "<Double-Button-1>", lambda _: self.deleteNode(canvasNode)) 

    def spawnNode(self, coords : tuple) -> bool:  
        if self.__isEdgeBeingDrawn: return

        self.__isNodeBeingDeleted = False 
        if not self.__creationTool.canNodeBeSpawned(self.__canvas, coords): return False 
        
        canvasNode = self.__creationTool.createNode(self.__canvasGraph, coords)
        self.__creationTool.renderNode(self.__canvas, canvasNode)
        self.__addNodeEvents(canvasNode) 
        return True   

    def deleteEdge(self) -> None:
        if self.__isAlgorithmRunning: return
        if self.__edgeBeingEdited: self.__deleteEdge(self.__edgeBeingEdited)

    def finishEdgeEdit(self) -> float: 
        if self.__edgeBeingEdited: self.__edgeBeingEdited.setColour(CanvasEdge.getDefaultColour())
        self.__edgeBeingEdited = None 
        self.__isEdgeBeingEdited = False
        
    def setShowEdgeOptionsFunc(self, showEdgeOptionsFunc : Callable) -> None:
        self.__showEdgeOptions = showEdgeOptionsFunc
    
    def getEdgeBeingEdited(self) -> CanvasEdge: return self.__edgeBeingEdited

# Listen to Why does it always rain on me by Travis  
