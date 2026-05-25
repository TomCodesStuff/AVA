# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from typing import TYPE_CHECKING, TypeVar
from tkinter import Canvas, Event 
from src.data_structures import Graph
from src.graph_visualisation import EventsHandler, CanvasGraph, PhysicsCalculations
from ..algorithm_base import AlgorithmController
from src.thread_handlers import PhysicsThread


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
            self.getScreen().getCanvas().coords(canvasEdge.getCanvasID(), canvasEdge.getCoords())
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
        self.__eventHandler.updateEdgeWeight(weight)


    # Calculates and returns coords of the centre of the canvas  
    def __getCanvasCentreCoords(self) -> tuple: 
        canvas = self.__screen.getCanvas() 
        return (canvas.winfo_width() // 2, 
                canvas.winfo_height() // 2)
 

    def __createPhysicsThread(self) -> None:
        self.__physicsCalculations= PhysicsCalculations(self.__canvasGraph, self.__getCanvasCentre()) 
        self.addManagedThread(PhysicsThread(self.__physicsCalculations))


    def centreEdge(self) -> tuple: 
        circleOffset = self.__model.getCircleSize() // 2 
        # Reference to canvas 
        canvas = self.__screen.getCanvas()  
        x0, y0, _, _ = self.__edgeHandler.getEdgeStartNode().getCoords()
        # Get Coords of the destination node 
        x1, y1, _, _ = self.__edgeHandler.getEdgeEndNode().getCoords() 
        coords = (x0 + circleOffset, y0 + circleOffset, 
                  x1 + circleOffset, y1 + circleOffset)
        # Send updated coords to the canvas
        canvas.coords(self.__edgeHandler.getCurrentEdgeID(), coords)  
        # Return the updated coords of the edge 
        return coords 


    def __drawEdge(self, event : Event, canvasNode) -> None:  
        canvas = self.__screen.getCanvas()   
        circleOffset = self.__model.getCircleSize() // 2
        x0, y0, _, _ = canvasNode.getCoords() 
        lineCoords, edgeID = None, None 

        # Checks if mouse has left the node the edge starts from
        collisions = canvas.find_overlapping(event.x, event.y, event.x, event.y)  
        # If the mouse is still in the node, the edge is not drawn yet
        if(canvasNode.getCanvasID() in collisions): return  
        # If there is no current edge 
        if(self.__edgeHandler.getCurrentEdgeID() is None): 
            # Create a new edge on screen
            edgeID = canvas.create_line(x0 + circleOffset, y0 + circleOffset, 
                                                    event.x, event.y, width = "3")   
            self.__edgeHandler.setCurrentEdgeID(edgeID)
            # Lowers the priority of the edge, so it appears below nodes 
            canvas.tag_lower(edgeID) 
        # If there is an edge being drawn on screen
        else:    
            # Updates edge to follow mouse 
            # (Also if the node has moved the edges starting position is updated)
            lineCoords = (x0 + circleOffset, y0 + circleOffset, event.x, event.y)
            # Updates the lines coordinates 
            canvas.coords(self.__edgeHandler.getCurrentEdgeID(), lineCoords)

            
    # Update positions of edges on the canvas 
    def __redrawEdges(self):  
        circleOffset = self.__model.getCircleSize() // 2
        canvas = self.__screen.getCanvas()
        for edge in self.__model.getEdges():   
            startNode, endNode = edge.getNodes()
            x0, y0, _, _ = startNode.getCoords()
            x1, y1, _, _ = endNode.getCoords()
            canvas.coords(edge.getCanvasID(), round(x0 + circleOffset), round(y0 + circleOffset),
                          round(x1 + circleOffset), round(y1 + circleOffset))

        # If the user is creating an edge, the edges position is updated
        # (In case the start node is being moved on screen) 
        if self.__edgeHandler.isEdgeBeingDrawn() and self.__edgeHandler.getCurrentEdgeID(): 
            x0, y0, _, _ = self.__edgeHandler.getEdgeStartNode().getCoords()
            _, _, x1, y1 = canvas.coords(self.__edgeHandler.getCurrentEdgeID())
            newCoords = (x0 + circleOffset, y0 + circleOffset, x1, y1)
            # Updates the lines coordinates  
            canvas.coords(self.__edgeHandler.getCurrentEdgeID(), newCoords)


# Listen to Paranoid by Black Sabbath
