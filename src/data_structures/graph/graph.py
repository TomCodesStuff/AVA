from __future__ import annotations
from src.data_structures import DataStructure
from src.enums import EdgeDirection
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
        self.__nodesToID = {}
        self.__startNode = None  
        self.__endNode = None 

    def addNode(self, node : Node, nodeID : int) -> None: 
        if node not in self.__nodesToID:
            self.__nodesToID[node] = nodeID
    
    def removeNode(self, node : Node) -> None: 
        if node in self.__nodesToID: 
            del self.__nodesToID[node]
    
    def updateNodeID(self, node : Node, newID : int) -> None:
        if node not in self.__nodesToID: return 
        self.__nodesToID[node] = newID 

    def get(self) -> List[Tuple[int, Node]]: 
        return list(self.__nodesToID.keys())

    def size(self) -> int: return len(self.__nodesToID) 

    def __str__(self) -> str: 
        lines = ["Graph:"]
        for node, nodeID in self.__nodesToID.items(): 
            line = f"{nodeID}: "
            for (neighbour, weight) in node.getNeighbours(): 
                line += f"{self.__nodesToID.get(neighbour, "None")} [W={weight}] "
            lines.append(line)
        return "\n".join(lines)
    
    def __iter__(self) -> Iterable: 
        return iter(self.get())
    
