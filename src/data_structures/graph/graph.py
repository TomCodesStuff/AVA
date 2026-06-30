from __future__ import annotations
from src.data_structures import DataStructure
from src.enums import EdgeDirection
from src.graph_visualisation import CanvasNode, CanvasEdge
from typing import Iterable, List, Tuple


class Edge(): 
    def __init__(self, weight : int, colour : str, direction : EdgeDirection):
        self.__colour = colour 
        self.__weight = weight 
        self.__direction = direction
        self.__firstNode = None 
        self.__secondNode = None 

    def getWeight(self) -> int: return self.__weight    
    def getColour(self) -> str: return self.__colour
    def getDirection(self) -> EdgeDirection: return self.__direction
    
    def setColour(self, colour : str) -> None:  
        if colour: self.__colour = colour  
    
    def setWeight(self, weight : int) -> None: 
        if weight > 0: self.__weight = weight 
    
    def setDirection(self, direction : EdgeDirection) -> None: 
        self.__direction = direction
    
    def setFirstNode(self, node : Node) -> Node: self.__firstNode = node

    def setSecondNode(self, node: Node) -> Node: self.__secondNode = node 

    def getNeighbourNode(self, node : Node) -> Node|None: 
        if node == self.__firstNode: return self.__secondNode 
        if node == self.__secondNode: return self.__firstNode
        return None 


# TODO add function to get ID in constructor 
class Node(): 
    def __init__(self, colour : str):
        self.__colour = colour 
        self.__neighbours = {} 
        # Used to reconstruct route when algorithm is complete 
        self.__prevNode = None 

    def getColour(self) -> str: return self.__colour 
    
    def setColour(self, colour : str) -> None:  
        if colour: self.__colour = colour 
    
    def addEdge(self, edge : Edge) -> None:  
        neighbourNode = edge.getNeighbourNode(self) 
        if neighbourNode is not None and neighbourNode not in self.__neighbours: 
            self.__neighbours[neighbourNode] = edge

    def removeEdge(self, edge : Edge) -> None: 
        neighbourNode = edge.getNeighbourNode(self) 
        if neighbourNode in self.__neighbours: 
            del self.__neighbours[neighbourNode]
    
    def getNeighbours(self) -> List[Tuple[Node, int]]: 
        return [(neighbourNode, edge.getWeight()) for neighbourNode, edge in self.__neighbours.items()] 

    def setEdgeColour(self, neighbourNode : Node, colour : str) -> None: 
        if neighbourNode in self.__neighbours and colour: 
            self.__neighbours[neighbourNode].setColour(colour) 
    
    def setPrevNode(self, node : Node) -> None: 
        if node in self.__neighbours: self.__prevNode = node

    def getPrevNode(self) -> Node: return self.__prevNode 

class Graph(DataStructure[Node]): 
    def __init__(self):
        self.__nodes = []
        self.__startNode = None  
        self.__goalNode = None 

    def addNode(self, node : Node) -> None: 
        if node not in self.__nodes:
            self.__nodes.append(node)
    
    def removeNode(self, node : Node) -> None: 
        if node in self.__nodes: 
            self.__nodes.remove(node) 
        
        if node == self.__startNode: self.__startNode = None
        if node == self.__goalNode: self.__goalNode = None
    
    def get(self) -> List[Node]: 
        return self.__nodes.copy()

    def size(self) -> int: return len(self.__nodes)  

    def setStartNode(self, node : Node) -> None: 
        if node in self.__nodes: self.__startNode = node

    def getStartNode(self) -> Node|None: return self.__startNode

    def setGoalNode(self, node : Node) -> None: 
        if node in self.__nodes: self.__goalNode = node

    def getGoalNode(self) -> Node|None: return self.__goalNode

    def resetColours(self) -> None: 
        for node in self.get(): 
            node.setColour(CanvasNode.defaultColour) 
            for (neighbour, _) in node.getNeighbours():
                node.setEdgeColour(neighbour, CanvasEdge.defaultColour)

    def __str__(self) -> str: 
        startNodeID = self.__nodes.index(self.__startNode) if self.__startNode else "<undefined>"
        goalNodeID = self.__nodes.index(self.__goalNode) if self.__goalNode else "<undefined>"

        lines = ["Graph:", 
                 f"Start Node: {startNodeID}",
                 f"End Node: {goalNodeID}"]
        for i, node in enumerate(self.__nodes): 
            line = f"{i}: "
            for (neighbour, weight) in node.getNeighbours(): 
                neighbourID = self.__nodes.index(neighbour) if neighbour in self.__nodes else "<undefined>"
                line += f"{neighbourID} [W={weight}] " 
            lines.append(line)
        return "\n".join(lines)

    def __iter__(self) -> Iterable: 
        return iter(self.get())
    
