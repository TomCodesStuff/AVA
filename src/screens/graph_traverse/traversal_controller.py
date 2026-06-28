# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from typing import TYPE_CHECKING, TypeVar
from tkinter import Canvas
from src.data_structures import Graph
from src.graph_visualisation import EventsHandler, CanvasGraph, CanvasNode, CanvasEdge, PhysicsCalculations
from src.screens.algorithm_base import AlgorithmController
from src.thread_handlers import PhysicsThread
from src.enums import EdgeDirection, EdgeDirectionOption

if TYPE_CHECKING: 
    from src.screens.graph_traverse import TraversalScreen, TraversalModel


S = TypeVar("S", bound="TraversalScreen")
M = TypeVar("M", bound="TraversalModel")
D = TypeVar("D", bound="Graph")

class TraversalController(AlgorithmController[S, M, D]):
    def __init__(self, screen : S, model : M, dataStructure : D):
        super().__init__(screen, model, dataStructure)

        self.__eventHandler = None
        self.__canvasGraph = CanvasGraph(self.getDataStructure())
        self.__physicsCalculations = None   
        # Set ID counter back to 0
        CanvasNode.resetNodeIDCounter()

        # Correctly set the default screen length for newly created edges 
        CanvasEdge.setDefaultScreenLen(self.__calculateScreenLen(CanvasEdge.getDefaultWeight()))
  

    def init(self) -> None: 
        self.createEventHandler(self.getScreen().getCanvas())
        self.__repeatCanvasRefresh() 
        self.__createPhysicsThread() 
        self.startManagedThreads()

    def __getCanvasCentre(self) -> tuple: 
        canvas = self.getScreen().getCanvas()
        return (canvas.winfo_width() // 2, canvas.winfo_height() // 2)

    # NOTE temp function for testing 
    def __repeatCanvasRefresh(self) -> None:  
        # print("Refreshing canvas")
        self.refreshCanvas() 
        self.getScreen().getWindow().scheduleFunctionExecution(self.__repeatCanvasRefresh, 16)

    def __deleteMarkedGraphItems(self) -> None:   
        canvas = self.getScreen().getCanvas()

        edges_to_delete = [canvasEdge for canvasEdge in self.__canvasGraph.getCanvasEdges() if canvasEdge.isMarkedForDeletion()]     
        nodes_to_delete = [canvasNode for canvasNode in self.__canvasGraph.getCanvasNodes() if canvasNode.isMarkedForDeletion()]    
        
        for canvasEdge in edges_to_delete:  
            self.__canvasGraph.deleteCanvasEdge(canvasEdge)
            canvas.delete(canvasEdge.getCanvasID()) 
        
        for canvasNode in nodes_to_delete: 
            self.__canvasGraph.deleteCanvasNode(canvasNode)
            canvas.delete(canvasNode.getCanvasID())
            canvas.delete(canvasNode.getCanvasText().getCanvasID())
  
    def refreshCanvas(self, refreshColours:bool=False) -> None: 
        latestResults = {} 
        canvas = self.getScreen().getCanvas()

        if self.__eventHandler and self.__eventHandler.getEdgeBeingDrawn():  
            edgeBeingDrawn = self.__eventHandler.getEdgeBeingDrawn() 
            if edgeBeingDrawn.getCanvasID() is not None: 
                canvas.coords(edgeBeingDrawn.getCanvasID(), edgeBeingDrawn.getCoords())

        if self.__physicsCalculations is not None: 
            latestResults = self.__physicsCalculations.getLatestResults()

        # Delete any marked Nodes and Edges (might stop race conditions/crashes)
        self.__deleteMarkedGraphItems()

        for canvasNode in self.__canvasGraph.getCanvasNodes():  
            if canvasNode.getCanvasID() in latestResults:
                canvasNode.applyForces(latestResults[canvasNode.getCanvasID()])

            x0, y0, _, _ = canvasNode.getCoords()
            # NOTE might need changing to .coords here(?)
            canvas.moveto(canvasNode.getCanvasID(), round(x0), round(y0))
            canvas.itemconfig(canvasNode.getCanvasID(), fill=canvasNode.getColour())  

            canvasText = canvasNode.getCanvasText()
            x0, y0 = canvasText.getCoords()
            canvas.coords(canvasText.getCanvasID(), x0, y0)
            canvas.itemconfig(canvasText.getCanvasID(), text=canvasText.getText())

        
        for canvasEdge in self.__canvasGraph.getCanvasEdges(): 
            firstNode, secondNode = canvasEdge.getCanvasNodes() 
            x0, y0, _, _ = firstNode.getCoords() 
            x1, y1, _, _ = secondNode.getCoords()    

            canvasEdge.updateCoords((x0 + firstNode.getOffset(), y0 + firstNode.getOffset(), 
                                     x1 + secondNode.getOffset(), y1 + secondNode.getOffset())) 
            
            canvas.coords(canvasEdge.getCanvasID(), canvasEdge.adjustDirectionArrows())
            canvas.itemconfig(canvasEdge.getCanvasID(), fill=canvasEdge.getColour())
        
    def createEventHandler(self, canvas : Canvas) -> None: 
        self.__eventHandler = EventsHandler(canvas, self.__canvasGraph, self.getModel().getMaxNumNodes()) 
        # Update screen to show edge options 
        self.__eventHandler.setShowEdgeOptionsCallback(self.getScreen().showEdgeOptions)
        self.__eventHandler.setUpdateSelectButtonsCallback(self.getScreen().enableNodeSelectionButtons)

    # Draws a circle (node) on the canvas 
    def spawnNode(self, coords: tuple=()) -> None: 
        if self.__eventHandler is None: return
        nodeCreated = self.__eventHandler.spawnNode(coords)        
        if nodeCreated: 
            self.getScreen().setAddNodeButtonColour("black")
            self.getScreen().setDeleteNodeButtonColour("black")
        else: self.getScreen().setAddNodeButtonColour("red") 
    
    def deleteNode(self) -> None: 
        if self.__eventHandler is None: return 
        canvasNode = self.__canvasGraph.getLastCreatedNode() 
        if canvasNode is None:
            self.getScreen().setDeleteNodeButtonColour("red") 
            return 
        self.getScreen().setDeleteNodeButtonColour("black")
        self.__eventHandler.deleteNode(canvasNode) 

    def deleteEdge(self) -> None:  self.__eventHandler.deleteEdge()

    def __calculateScreenLen(self, newWeight : int) -> None:   
        model = self.getModel()      
        return model.getEdgeMinScreenLen() + model.getRangeSlope() * (newWeight - model.getMinEdgeWeight())

    def finishEdgeEdit(self) -> None: 
        self.__eventHandler.finishEdgeEdit()

    def updateEdgeWeight(self, weight : int) -> None:
        edgeBeingEdited = self.__eventHandler.getEdgeBeingEdited() 
        if edgeBeingEdited: 
            edgeBeingEdited.setWeight(weight) 
            edgeBeingEdited.setScreenLen(self.__calculateScreenLen(weight))

    def changeEdgeDirection(self, directionOption : EdgeDirectionOption) -> None:  
        edgeBeingEdited = self.__eventHandler.getEdgeBeingEdited() 
        if edgeBeingEdited is None: return
        
        x0, _, x1, _ = edgeBeingEdited.getCoords()
        isFirstNodeLeftMost = x0 <= x1

        if (directionOption == EdgeDirectionOption.LEFT_TO_RIGHT and isFirstNodeLeftMost) or \
            (directionOption == EdgeDirectionOption.RIGHT_TO_LEFT and not isFirstNodeLeftMost): 
            direction = EdgeDirection.FIRST_TO_SECOND 
        elif directionOption != EdgeDirectionOption.BIDIRECTIONAL: direction = EdgeDirection.SECOND_TO_FIRST
        else: direction = EdgeDirection.BIDIRECTIONAL

        edgeBeingEdited.setDirection(direction)

    def __createPhysicsThread(self) -> None:
        self.__physicsCalculations= PhysicsCalculations(self.__canvasGraph, self.__getCanvasCentre()) 
        self.addManagedThread(PhysicsThread(self.__physicsCalculations)) 
    
    def enableNodeStartAssignEvent(self) -> None: 
        if self.__eventHandler: 
            self.__eventHandler.enableNodeStartAssignEvent()  
            self.__eventHandler.disableNodeGoalAssignEvent()
    
    def enableNodeGoalAssignEvent(self) -> None: 
        if self.__eventHandler: 
            self.__eventHandler.enableNodeGoalAssignEvent() 
            self.__eventHandler.disableNodeStartAssignEvent() 


# Listen to Paranoid by Black Sabbath
