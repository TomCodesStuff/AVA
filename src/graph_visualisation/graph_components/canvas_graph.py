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
        self.__graph.addNode(canvasNode.getNode(), canvasNode.getID()) 

        print(str(self.__graph))

    def __decrementNodeIDs(self, deletedNodeID : int) -> None:
        for canvasNode in self.getCanvasNodes(): 
            if deletedNodeID < canvasNode.getID(): 
                canvasNode.decrementID()
                self.__graph.updateNodeID(canvasNode.getNode(), canvasNode.getID())
                canvasNode.getCanvasText().updateText(str(canvasNode.getID()))  
        CanvasNode.decrementNodeIDCounter()
 
    def deleteCanvasNode(self, canvasNode : CanvasNode) -> None:
        if canvasNode not in self.__nodes: return
        self.__nodes.remove(canvasNode)
        self.__graph.removeNode(canvasNode.getNode())

        self.__decrementNodeIDs(canvasNode.getID())

        print(str(self.__graph))

    def assignStartNode(self, canvasNode : CanvasNode) -> None: 
        if canvasNode not in self.__nodes: return 
        if self.__startNode: self.__startNode.setColour(CanvasNode.defaultColour)
        canvasNode.setColour(CanvasNode.startColour)
        canvasNode.setPrevColour(CanvasNode.startColour)
        self.__startNode = canvasNode 
    
    def assignGoalNode(self, canvasNode : CanvasNode) -> None: 
        if canvasNode not in self.__nodes: return 
        if self.__goalNode: self.__goalNode.setColour(CanvasNode.defaultColour)
        canvasNode.setColour(CanvasNode.goalColour) 
        canvasNode.setPrevColour(CanvasNode.goalColour)
        self.__goalNode = canvasNode

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
