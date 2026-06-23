from ..data_structure import DataStructure


# Algorithms only need to see 

class Edge(): 
    def __init__(self, weight : int, colour : str):
        self.__colour = colour 
        self.__weight = weight 
    
    def getWeight(self) -> int: return self.__weight    
   
    def getColour(self) -> str: return self.__colour
    
    def setColour(self, colour : str) -> None:  
        if colour: self.__colour = colour 
    

class Node(): 
    def __init__(self, colour : str):
        self.__colour = colour 
        self.__neighbours = [] 

    def getColour(self) -> str: return self.__colour 
    
    def setColour(self, colour : str) -> None:  
        if colour: self.__colour = colour 
    
    def addNeighbour(self, edge : Edge) -> None: 
        if edge not in self.__neighbours: 
            self.__neighbours.append(edge)

    def removeNeighbour(self, edge : Edge) -> None: 
        if edge in self.__neighbours: 
            self.__neighbours.remove(edge)

class Graph(DataStructure): 
    def __init__(self):
        self.__nodes = []
    
    def append(self, node : Node) -> None: 
        if node not in self.__nodes:
            self.__nodes.append(node)
    
    def get(self) -> list: 
        return self.__nodes

    def size(self) -> int: return len(self.__nodes)
    
