from typing import List
from .canvas_node import CanvasNode
from .canvas_edge import CanvasEdge
from src.data_structures import Graph


class CanvasGraph():
    def __init__(self, graph : Graph): 
        self.__graph = graph
        self.__nodes = []
        self.__edges = []
        self.__nodesToEdges = {} 

        self.__startNode = None 
        self.__goalNode = None 

    def addCanvasNode(self, canvasNode : CanvasNode) -> None: 
        self.__nodes.append(canvasNode) 
        self.__graph.addNode(canvasNode.getNode()) 

    def __decrementNodeIDs(self, deletedNodeID : int) -> None:
        for canvasNode in self.getCanvasNodes(): 
            if deletedNodeID < canvasNode.getID(): 
                canvasNode.decrementID()
                canvasNode.getCanvasText().updateText(str(canvasNode.getID()))  
        CanvasNode.decrementNodeIDCounter()
 
    def deleteCanvasNode(self, canvasNode : CanvasNode) -> None:
        if canvasNode not in self.__nodes: return
        self.__nodes.remove(canvasNode)
        
        if canvasNode == self.__startNode: self.__startNode = None
        if canvasNode == self.__goalNode: self.__goalNode = None

        self.__graph.removeNode(canvasNode.getNode())
        self.__decrementNodeIDs(canvasNode.getID())
     

    # NOTE: 
    # if only one node AND it's the goal node -> assign as start node and goal node
    # elif passed node is goal node -> unassign goal node
    #   
    # if there is a current start node -> reset it's colours 

    def assignStartNode(self, canvasNode : CanvasNode) -> None: 
        if canvasNode not in self.__nodes: return 
        
        # Assign passed node with start colours 
        canvasNode.setColour(CanvasNode.startColour)
        canvasNode.setPrevColour(CanvasNode.startColour)
        
        # Only allow start and goal nodes to be the same if there is one node
        if canvasNode == self.__goalNode: 
            if len(self.__nodes) == 1: 
                canvasNode.setPrevColour(CanvasNode.startGoalColour)
                canvasNode.setColour(CanvasNode.startGoalColour)
            else: self.__goalNode = None 
        
        # If previous start node -> reset it's colours 
        if self.__startNode: 
            self.__startNode.setColour(CanvasNode.defaultColour)
            self.__startNode.setPrevColour(CanvasNode.defaultColour)

        # Assign passed node as start node 
        self.__startNode = canvasNode  
        # TODO avoid duplicate logic here -> move assignment to when algorithm runs
        self.__graph.setStartNode(canvasNode.getNode())

    def assignGoalNode(self, canvasNode : CanvasNode) -> None: 
        if canvasNode not in self.__nodes: return 
        
        # Assign passed node with goal colours
        canvasNode.setColour(CanvasNode.goalColour) 
        canvasNode.setPrevColour(CanvasNode.goalColour)

        # Only allow start and goal nodes to be the same if there is one node
        if canvasNode == self.__startNode: 
            if len(self.__nodes) == 1: 
                canvasNode.setPrevColour(CanvasNode.startGoalColour)
                canvasNode.setColour(CanvasNode.startGoalColour)
            else: self.__startNode = None 

        # Update previous goal nodes colours to default (if there is one)
        if self.__goalNode: 
            self.__goalNode.setColour(CanvasNode.defaultColour)
            self.__goalNode.setPrevColour(CanvasNode.defaultColour)           
            
        self.__goalNode = canvasNode
        # TODO remove redundant logic -> maybe a flag 
        self.__graph.setGoalNode(canvasNode.getNode())

    def getStartNode(self) -> CanvasNode | None: return self.__startNode

    def getGoalNode(self) -> CanvasNode | None: return self.__goalNode

    def getLastCreatedNode(self) -> CanvasNode|None: 
        if len(self.__nodes) == 0: return None 
        return self.__nodes[-1]

    def areNodesConnected(self, nodes : tuple) -> bool:
        return nodes in self.__nodesToEdges or nodes[::-1] in self.__nodesToEdges

    def addCanvasEdge(self, canvasEdge : CanvasEdge) -> None:  
        if canvasEdge not in self.__edges:
            self.__edges.append(canvasEdge)

    def addEdgeToNodes(self, canvasEdge : CanvasEdge) -> None: 
        # Assume default directional is bidirectional and add edge to both nodes
        startNode, endNode = canvasEdge.getCanvasNodes() 
        startNode.addEdge(canvasEdge) 
        endNode.addEdge(canvasEdge)   
        if not self.areNodesConnected((startNode, endNode)):
            self.__nodesToEdges[(startNode, endNode)] = canvasEdge
        
        # Handle if default direction has been changed from bidirectional 
        canvasEdge.syncDirection()
         
    def deleteCanvasEdge(self, canvasEdge : CanvasEdge) -> None:  
        if canvasEdge not in self.__edges: return
        self.__edges.remove(canvasEdge)
        nodes = canvasEdge.getCanvasNodes() 
        if not self.areNodesConnected(nodes): return
        
        if nodes in self.__nodesToEdges: self.__nodesToEdges.pop(nodes)
        elif nodes[::-1] in self.__nodesToEdges: self.__nodesToEdges.pop(nodes[::-1])

        startNode, endNode = nodes 
        if startNode: startNode.removeEdge(canvasEdge)
        if endNode: endNode.removeEdge(canvasEdge) 

    def getEdgeConnectingNodes(self, nodes : tuple) -> CanvasEdge|None:
        canvasEdge = self.__nodesToEdges.get(nodes, None)
        if canvasEdge: return canvasEdge
        return self.__nodesToEdges.get(nodes[::-1], None)

    def getCanvasNodes(self) -> List[CanvasNode]: return self.__nodes  
    
    def getCanvasEdges(self) -> List[CanvasEdge]: return self.__edges

    def getCanvasNodeAt(self, index : int) -> None: 
        return self.__nodes[min(index, len(self.__nodes) - 1)]


# Listen to Hertz by Amyl and the Sniffers 
