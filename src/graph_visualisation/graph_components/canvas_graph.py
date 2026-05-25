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

    def addCanvasNode(self, canvasNode : CanvasNode) -> None: 
        self.__nodes.append(canvasNode) 

    def deleteCanvasNode(self, canvasNode : CanvasNode) -> None: 
        if canvasNode in self.__nodes:
            self.__nodes.remove(canvasNode)
    
    def getLastCreatedNode(self) -> CanvasNode|None: 
        if len(self.__nodes) == 0: return None 
        return self.__nodes[-1]

    def areNodesConnected(self, nodes : tuple) -> bool:
        return nodes in self.__nodesToEdges or nodes[::-1] in self.__nodesToEdges

    def addCanvasEdge(self, canvasEdge : CanvasEdge) -> None:  
        if canvasEdge not in self.__edges:
            self.__edges.append(canvasEdge)

    def addEdgeToNodes(self, canvasEdge : CanvasEdge) -> None: 
        startNode, endNode = canvasEdge.getNodes() 
        startNode.addEdge(canvasEdge) 
        endNode.addEdge(canvasEdge)   
        if not self.areNodesConnected((startNode, endNode)):
            self.__nodesToEdges[(startNode, endNode)] = canvasEdge
         
    def deleteCanvasEdge(self, canvasEdge : CanvasEdge) -> None:  
        if canvasEdge not in self.__edges: return
        self.__edges.remove(canvasEdge)
        nodes = canvasEdge.getNodes() 
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

    def getNodes(self) -> List[CanvasNode]: return self.__nodes  
    def getEdges(self) -> List[CanvasEdge]: return self.__edges

    def getNodeAt(self, index : int) -> None: 
        return self.__nodes[min(index, len(self.__nodes) - 1)]


# Listen to Hertz by Amyl and the Sniffers 
