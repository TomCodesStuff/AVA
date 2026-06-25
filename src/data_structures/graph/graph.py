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
        if neighbourNode is not None: 
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
        self.__endNode = None 

    def addNode(self, node : Node) -> None: 
        if node not in self.__nodes:
            self.__nodes.append(node)
    
    def get(self) -> List[Node]: 
        return self.__nodes

    def size(self) -> int: return len(self.__nodes) 

    def __str__(self) -> str:
        return "Graph"
    
    def __iter__(self) -> Iterable: 
        return iter(self.__nodes)
    
