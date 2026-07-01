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
    
        unvisitedNodes = {
            node : float("inf") if node != startNode else 0 
            for node in graph.get()
        }
   
        # While there is an unvisited node 
        while((crrntNode := self.__selectNode(unvisitedNodes)) is not None):   
            # Reset all colours 
            graph.resetColours()
            # Mark current node as red 
            crrntNode.setColour("red")

            # Mark all nodes and edges current loop looks at  
            for (neighbour, weight) in crrntNode.getNeighbours():
                if neighbour in unvisitedNodes: 
                    crrntNode.setEdgeColour(neighbour, "red")
                    neighbour.setColour("black")
                self.tick()

            # For each neighbour    
            for (neighbour, weight) in crrntNode.getNeighbours():
                # If new shortest path for a node has been found 
                if neighbour in unvisitedNodes and unvisitedNodes[crrntNode] + weight < unvisitedNodes[neighbour]:
                    crrntNode.setEdgeColour(neighbour, "green")
                    unvisitedNodes[neighbour] = unvisitedNodes[crrntNode] + weight 
                    neighbour.setPrevNode(crrntNode) 
                self.tick()
            # Mark node as visisted 
            del unvisitedNodes[crrntNode]
            
            self.tick()

        return 0