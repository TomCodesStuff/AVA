# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

# TODO -> how to handle 0 or 1 nodes on screen?


import random
import math
from typing import TYPE_CHECKING, TypeVar
from tkinter import Canvas
from src.data_structures import Graph
from src.graph_visualisation import EventsHandler, CanvasGraph, CanvasNode, CanvasEdge, CanvasText, PhysicsCalculations
from src.screens.algorithm_base import AlgorithmController
from src.thread_handlers import PhysicsThread
from src.enums import EdgeDirection, EdgeDirectionOption

if TYPE_CHECKING: 
    from src.screens.graph_traverse import TraversalScreen, TraversalModel


S = TypeVar("S", bound="TraversalScreen")
M = TypeVar("M", bound="TraversalModel")
D = TypeVar("D", bound="Graph")

SIXTY_FPS_IN_MS = 16
MOVEMENT_THRESHOLD = 1

class TraversalController(AlgorithmController[S, M, D]):
    def __init__(self, screen : S, model : M, dataStructure : D):
        super().__init__(screen, model, dataStructure)

        self.__eventHandler = None
        self.__canvasGraph = CanvasGraph(self.getDataStructure())
        self.__physicsCalculations = None   
        self.__cancelCanvasRefreshLoop = False

        # Set ID counter back to 0
        CanvasNode.resetNodeIDCounter()

        # Correctly set the default screen length for newly created edges 
        CanvasEdge.setDefaultScreenLen(self.__calculateScreenLen(CanvasEdge.getDefaultWeight()))
    
    def spawnStarterNodes(self) -> None: 
        if not self.__eventHandler: return 

        # Offset to make sure second node is on screen
        offset = 5
        canvasWidth = self.getScreen().getCanvas().winfo_width()
        canvasHeight = self.getScreen().getCanvas().winfo_height()
        nodeSize = CanvasNode.defaultSize

        # One node will spawn at default coords (top left canvas)
        self.__eventHandler.spawnNode(CanvasNode.defaultCoords)
        # Another node will spawn at bottom-rigth canvas
        self.__eventHandler.spawnNode((canvasWidth - nodeSize - offset, canvasHeight - nodeSize - offset, 
                                       canvasWidth - offset, canvasHeight - offset))

    def startInteractiveGraph(self) -> None:  
        if self.__eventHandler is None: self.createEventHandler(self.getScreen().getCanvas())
        self.__createPhysicsThread() 
        self.startManagedThreads()
        self.__eventHandler.enableAllEvents()
        self.__startCanvasRefreshLoop() 
    
    def stopInteractiveGraph(self) -> None:
        self.stopManagedThreads() 
        self.__eventHandler.disableAllEvents()
        self.__cancelCanvasRefreshLoop = True 
        self.__stopCanvasRefreshLoop()
        self.cancelScheduledProcesses()
        self.__physicsCalculations = None

    def __getCanvasCentre(self) -> tuple: 
        canvas = self.getScreen().getCanvas()
        return (canvas.winfo_width() // 2, canvas.winfo_height() // 2)

    def __applyPositionChanges(self) -> None: 
        if self.__physicsCalculations is None: return  
        
        nodesToUpdatedCoords, edgesToUpdatedCoords = self.__physicsCalculations.getLatestResults()          
        
        for canvasNode in self.__canvasGraph.getCanvasNodes():  
            if canvasNode.getCanvasID() in nodesToUpdatedCoords and not canvasNode.isBeingDragged():
                canvasNode.updateCoords(nodesToUpdatedCoords[canvasNode.getCanvasID()]) 
        
        for canvasEdge in self.__canvasGraph.getCanvasEdges():  
            if canvasEdge.getFirstCanvasNode().isBeingDragged() or canvasEdge.getSecondCanvasNode().isBeingDragged(): 
                x0, y0, _, _ = canvasEdge.getFirstCanvasNode().getCoords() 
                r0 = canvasEdge.getFirstCanvasNode().getOffset()
                x1, y1, _, _ = canvasEdge.getSecondCanvasNode().getCoords()
                r1 = canvasEdge.getSecondCanvasNode().getOffset()
                canvasEdge.updateCoords((x0 + r0, y0 + r0, x1 + r1, y1 + r1))
            elif canvasEdge.getCanvasID() in edgesToUpdatedCoords: 
                canvasEdge.updateCoords(edgesToUpdatedCoords[canvasEdge.getCanvasID()])

    def __canvasRefreshLoop(self) -> None:   
        if self.__cancelCanvasRefreshLoop: return 
        self.__applyPositionChanges()
        self.refreshCanvas() 
        self.getScreen().getWindow().scheduleFunctionExecution(self.__canvasRefreshLoop, SIXTY_FPS_IN_MS)
   
    def __deleteMarkedGraphItems(self) -> None:   
        canvas = self.getScreen().getCanvas()

        edges_to_delete = [canvasEdge for canvasEdge in self.__canvasGraph.getCanvasEdges() 
                           if canvasEdge.isMarkedForDeletion()]     
        nodes_to_delete = [canvasNode for canvasNode in self.__canvasGraph.getCanvasNodes() 
                           if canvasNode.isMarkedForDeletion()]    
        
        for canvasEdge in edges_to_delete: 
            if canvasEdge.getWeightCanvasText() is not None: 
                canvas.delete(canvasEdge.getWeightCanvasText().getCanvasID())
            self.__canvasGraph.deleteCanvasEdge(canvasEdge)
            canvas.delete(canvasEdge.getCanvasID()) 
        
        for canvasNode in nodes_to_delete: 
            self.__canvasGraph.deleteCanvasNode(canvasNode)
            canvas.delete(canvasNode.getCanvasID())
            canvas.delete(canvasNode.getCanvasText().getCanvasID())
        
        if len(self.__canvasGraph.getCanvasNodes()) <= self.getModel().getMinNumNodes(): 
            self.getScreen().disableDeleteNodeButton()
    

    def __resetGraphColours(self) -> None: 
        for canvasNode in self.__canvasGraph.getCanvasNodes(): 
            canvasNode.setColour(canvasNode.getNode().getBaseColour())
            
        for canvasEdge in self.__canvasGraph.getCanvasEdges():
            canvasEdge.setColour(CanvasEdge.defaultColour)

    def __shouldCanvasNodeBeMoved(self, canvasNode : CanvasNode) -> bool: 
        if self.isAlgorithmRunning(): return False 
        if canvasNode.isBeingDragged(): return True

        x0, y0, _, _ = canvasNode.getCoords() 
        vX, vY, = canvasNode.getDisplayCoords()

        rX0 = round(x0)
        rY0 = round(y0)

        if abs(vX - rX0) < MOVEMENT_THRESHOLD and abs(vY - rY0) < MOVEMENT_THRESHOLD: return False 

        canvasNode.updateDisplayCoords((rX0, rY0))        
        return True
    
    def __shouldCanvasEdgeBeMoved(self, canvasEdge : CanvasEdge) -> None: 
        if self.isAlgorithmRunning(): return False 
        if canvasEdge.getFirstCanvasNode().isBeingDragged(): return True
        if canvasEdge.getSecondCanvasNode().isBeingDragged(): return True

        x0, y0, x1, y1 = canvasEdge.getCoords()
        vX0, vY0, vX1, vY1 = canvasEdge.getDisplayCoords()

        if abs(x0 - vX0) < MOVEMENT_THRESHOLD and abs(y0 - vY0) < MOVEMENT_THRESHOLD: return False
        if abs(x1 - vX1) < MOVEMENT_THRESHOLD and abs(y1 - vY1) < MOVEMENT_THRESHOLD: return False
        
        canvasEdge.updateDisplayCoords(canvasEdge.getCoords())
        return True

    # TODO fix crashes (tried and failed, idc)
    def refreshCanvas(self, refreshColours:bool=False) -> None:   
        canvas = self.getScreen().getCanvas()
        if refreshColours: self.__resetGraphColours()
        
        # Draw intermediate egde that is following mouse
        if self.__eventHandler:
            edgeBeingDrawn = self.__eventHandler.getEdgeBeingDrawn() 
            if edgeBeingDrawn and edgeBeingDrawn.getCanvasID() is not None:  
                canvas.coords(edgeBeingDrawn.getCanvasID(), edgeBeingDrawn.getCoords()) 

        # Delete any marked Nodes and Edges (might stop race conditions/crashes)
        self.__deleteMarkedGraphItems()

        for canvasNode in self.__canvasGraph.getCanvasNodes(): 
            if self.__shouldCanvasNodeBeMoved(canvasNode):

                x0, y0 = canvasNode.getDisplayCoords() 
                canvas.moveto(canvasNode.getCanvasID(), x0, y0)                 

                canvasText = canvasNode.getCanvasText()
                cX0, cY0 = canvasText.getCoords()
                canvas.coords(canvasText.getCanvasID(), cX0, cY0)  
                
            if canvasNode.getColour() != canvasNode.getDisplayedColour():
                canvas.itemconfig(canvasNode.getCanvasID(), fill=canvasNode.getColour())  
                canvasNode.updateDisplayedColour(canvasNode.getColour())
            
            canvasNodeText = canvasNode.getCanvasText()
            if canvasNodeText.getText() != str(canvasNode.getID()):
                canvasNodeText.updateText(canvasNode.getID())
                canvas.itemconfig(canvasNodeText.getCanvasID(), text=canvasNodeText.getText())
        
        for canvasEdge in self.__canvasGraph.getCanvasEdges():  
            if self.__shouldCanvasEdgeBeMoved(canvasEdge):
                canvas.coords(canvasEdge.getCanvasID(), canvasEdge.getCoords()) 
             
            if canvasEdge.getDisplayColour() != canvasEdge.getColour():
                canvas.itemconfig(canvasEdge.getCanvasID(), fill=canvasEdge.getColour())
                canvasEdge.updateDisplayColour(canvasEdge.getColour())

    def createEventHandler(self, canvas : Canvas) -> None:  
        model = self.getModel()
        screen = self.getScreen()
        self.__eventHandler = EventsHandler(canvas, self.__canvasGraph, model.getMinNumNodes(), model.getMaxNumNodes()) 
        
        # Reference to Functions event handler needs to call  
        self.__eventHandler.setShowEdgeOptionsCallback(screen.showEdgeOptions)
        self.__eventHandler.setUpdateSelectButtonsCallback(screen.enableNodeSelectionButtons) 
        self.__eventHandler.setEnableDeleteNodeButtonCallaback(self.getScreen().enableDeleteNodeButton)

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
        self.__physicsCalculations = PhysicsCalculations(self.__canvasGraph, self.__getCanvasCentre()) 
        self.addManagedThread(PhysicsThread(self.__physicsCalculations)) 
    
    def enableNodeStartAssignEvent(self) -> None: 
        if self.__eventHandler: 
            self.__eventHandler.enableNodeStartAssignEvent()  
            self.__eventHandler.disableNodeGoalAssignEvent()
    
    def enableNodeGoalAssignEvent(self) -> None: 
        if self.__eventHandler: 
            self.__eventHandler.enableNodeGoalAssignEvent() 
            self.__eventHandler.disableNodeStartAssignEvent()  
    
    def disableAllEvents(self) -> None:
        if self.__eventHandler: self.__eventHandler.disableAllEvents() 
    
    def enableAllEvents(self) -> None:
        if self.__eventHandler: self.__eventHandler.enableAllEvents() 
    
    def __stopCanvasRefreshLoop(self) -> None: 
        self.__cancelCanvasRefreshLoop = True
    
    def __startCanvasRefreshLoop(self) -> None: 
        self.__cancelCanvasRefreshLoop = False 
        self.__canvasRefreshLoop()   
    
    # I asked ChatGPT to help with this 
    def __calculateWeightTextCoords(self, edgeCoords : tuple) -> tuple: 
        x0, y0, x1, y1 = edgeCoords 
        weightTextOffset = self.getModel().getWeightTextOffset()
        
        midX = (x0 + x1) // 2 
        midY = (y0 + y1) // 2 
        
        # Calculate edge's vector 
        dx = x1 - x0
        dy = y1 - y0
        
        length = math.sqrt(dx ** 2 + dy ** 2)
        if length == 0: return(midX, midY)
        
        # Normalise vector -> so we move the correct amount of pixels away 
        ux = dx / length
        uy = dy / length

        # Want text to be perpendicular (90 degrees) to the edges line
        # So calculate the offsets using the opposite normalised lengths 
        xOffset = (uy * weightTextOffset)
        yOffset = (-ux * weightTextOffset)

        # Calculate new initial coords
        xCoord = midX + xOffset
        yCoord = midY + yOffset
        
        # If weight text is going to be offscreen, move to the opposite position
        if yCoord - weightTextOffset <= 0: yCoord = midY - yOffset
        if xCoord + weightTextOffset >= self.getScreen().getCanvas().winfo_width(): 
            xCoord = midX - xOffset

        return (xCoord, yCoord)

    def __createWeightCanvasText(self, canvasEdge : CanvasEdge) -> CanvasText:  
        x0, y0 = weightTextCoords = self.__calculateWeightTextCoords(canvasEdge.getCoords())
        weightCanvasText = CanvasText(str(canvasEdge.getWeight()), weightTextCoords) 
        canvasEdge.setCanvasWeightText(weightCanvasText)
        
        canvasID = self.getScreen().getCanvas().create_text(x0, y0, text=str(weightCanvasText.getText()), 
                                                            font=self.getModel().getWeightTextFont())
        weightCanvasText.setCanvasID(canvasID)

    def showEdgeWeightText(self) -> None:  
        canvas = self.getScreen().getCanvas()
        for canvasEdge in self.__canvasGraph.getCanvasEdges():             
            if canvasEdge.getWeightCanvasText() is None: 
                self.__createWeightCanvasText(canvasEdge) 
            else: 
                weightCanvasText = canvasEdge.getWeightCanvasText()
                x0, y0 = coords = self.__calculateWeightTextCoords(canvasEdge.getCoords()) 
                weightCanvasText.updateCoords(coords)
                canvas.moveto(weightCanvasText.getCanvasID(), x0, y0)  
                canvas.itemconfig(weightCanvasText.getCanvasID(), text=weightCanvasText.getText(), state="normal")
                
    def hideEdgeWeightText(self) -> None: 
        canvas = self.getScreen().getCanvas()
        for canvasEdge in self.__canvasGraph.getCanvasEdges(): 
            if canvasEdge.getWeightCanvasText() is not None: 
                canvas.itemconfig(canvasEdge.getWeightCanvasText().getCanvasID(), state="hidden")

    def selectStartNode(self) -> None: 
        if not self.__canvasGraph.getCanvasNodes(): return 
        # If goal node has node been selected, choose random node
        if self.__canvasGraph.getStartNode() is None:
            self.__canvasGraph.assignStartNode(random.choice(self.__canvasGraph.getCanvasNodes())) 
        # Set start node in Graph data structure 
        self.getDataStructure().setStartNode(self.__canvasGraph.getStartNode().getNode())
    
    def selectGoalNode(self) -> None:  
        if not self.__canvasGraph.getCanvasNodes(): return
        startNode = self.__canvasGraph.getStartNode()
        goalNode = self.__canvasGraph.getGoalNode()

        # Assign start node if it has not already been assigned 
        if startNode is None: self.selectStartNode() 
        # Assign goal node if it as not been assigned
        if goalNode is None:
            # Find all nodes that are not start node 
            candidateNodes = [x for x in self.__canvasGraph.getCanvasNodes() if x != startNode]  
            # If there are no candidate nodes -> set goal node to be start node 
            if not candidateNodes: self.__canvasGraph.assignGoalNode(startNode)
            # Otherwise randomly choose goal node
            else: self.__canvasGraph.assignGoalNode(random.choice(candidateNodes)) 
        # Set goal node in Graph data structure
        self.getDataStructure().setGoalNode(self.__canvasGraph.getGoalNode().getNode())

# Listen to Paranoid by Black Sabbath
