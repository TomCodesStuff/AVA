from ..data_structure import DataStructure


# Algorithms only need to see 
class Node(): 
    def __init__(self, colour : str):
        self.__colour = colour
    

    def getColour(self) -> str: return self.__colour
    
    
    def setColour(self, colour : str) -> None: 
        self.__colour = colour 



class Graph(DataStructure): 
    def __init__(self):
        self.__nodes = []
    

    def append(self, node : Node) -> None: 
        if node not in self.__nodes:
            self.__nodes.append(node)
    

    def get(self) -> list: 
        return self.__nodes
    

    