# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

import time 
from src.algorithms import Algorithm 
from src.data_structures import Graph, Node

class DijkstraTraverse(Algorithm[Graph]):
    # Constructor
    def __init__(self):
        super().__init__() 
    
    def getName(self) -> str: 
        return "Dijkstra" 

    def __selectNode(self, unvisitedNodes : dict) -> Node|None: 
        selected_node = None 
        shortest_distance = float("inf")

        for (node, distance) in unvisitedNodes.items(): 
            if distance < shortest_distance: 
                selected_node = node 
                shortest_distance = distance 
        
        return selected_node

    def run(self) -> int:  
        graph = self.getDataStructure()
        startNode = graph.getStartNode()
        
        visited_nodes = set()
        unvisitedNodes = {
            node : float("inf") if node != startNode else 0 
            for node in graph.get()
        }

        
        print(unvisitedNodes)
        
        # While there is an unvisited node 
        while((crrntNode := self.__selectNode(unvisitedNodes)) is not None):  
            # For each neighbour 
            for (neighbour, weight) in crrntNode.getNeighbours():  
                if neighbour in unvisitedNodes and unvisitedNodes[crrntNode] + weight < unvisitedNodes[neighbour]:
                    unvisitedNodes[neighbour] = unvisitedNodes[crrntNode] + weight 
                    neighbour.setPrevNode(crrntNode)
            
            del unvisitedNodes[crrntNode]
            visited_nodes.add(crrntNode)
   
        graph.printRoute()

        
        time.sleep(5)
        return 0