# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from typing import TYPE_CHECKING, TypeVar
from tkinter import Canvas
from src.data_structures import Graph
from src.graph_visualisation import EventsHandler, CanvasGraph, PhysicsCalculations
from ..algorithm_base import AlgorithmController
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

    def refreshCanvas(self, refreshColours:bool=False) -> None: 
        latestResults = {}
        if self.__physicsCalculations is not None: 
            latestResults = self.__physicsCalculations.getLatestResults()

        for canvasNode in self.__canvasGraph.getNodes():  
            if canvasNode.getID() in latestResults:
                canvasNode.applyForces(latestResults[canvasNode.getID()])

            x0, y0, _, _ = canvasNode.getCoords()
            self.getScreen().getCanvas().moveto(canvasNode.getCanvasID(), round(x0), round(y0))
            self.getScreen().getCanvas().itemconfig(canvasNode.getCanvasID(), fill=canvasNode.getColour())
        
        for canvasEdge in self.__canvasGraph.getEdges(): 
            firstNode, secondNode = canvasEdge.getNodes() 
            x0, y0, _, _ = firstNode.getCoords() 
            x1, y1, _, _ = secondNode.getCoords()    

            canvasEdge.updateCoords((x0 + firstNode.getOffset(), y0 + firstNode.getOffset(), 
                                     x1 + secondNode.getOffset(), y1 + secondNode.getOffset())) 
            
            self.getScreen().getCanvas().coords(canvasEdge.getCanvasID(), canvasEdge.showDirectionArrows())
            self.getScreen().getCanvas().itemconfig(canvasEdge.getCanvasID(), fill=canvasEdge.getColour())
        
        self.getScreen().getWindow().update_idle_tasks()  

    def createEventHandler(self, canvas : Canvas) -> None: 
        self.__eventHandler = EventsHandler(canvas, self.__canvasGraph) 
        # Update screen to show edge options 
        self.__eventHandler.setShowEdgeOptionsFunc(self.getScreen().showEdgeOptions)

    # Draws a circle (node) on the canvas 
    def spawnNode(self, coords: tuple=()): 
        if self.__eventHandler is None: return
        nodeCreated = self.__eventHandler.spawnNode(coords, override=True)        
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

    def deleteEdge(self) -> None: 
        self.__eventHandler.deleteEdge()

    def finishEdgeEdit(self) -> None: 
        self.__eventHandler.finishEdgeEdit()

    def updateEdgeWeight(self, weight : int) -> None:
        edgeBeingEdited = self.__eventHandler.getEdgeBeingEdited() 
        if edgeBeingEdited: edgeBeingEdited.setWeight(weight) 
    
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


# Listen to Paranoid by Black Sabbath
