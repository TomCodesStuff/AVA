# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from typing import Tuple
from src.algorithms import Algorithm 
from src.data_structures import Graph, Node

class UniformCostTraverse(Algorithm[Graph]):
    # Constructor
    def __init__(self):
        super().__init__() 
    
    def getName(self) -> str: 
        return "Uniform Cost Search" 

    def __selectNode(self, priorityQueue : dict) -> Tuple[Node,int]: 
        selected_node = None 
        shortest_distance = float("inf")

        for (node, distance) in priorityQueue.items(): 
            if distance < shortest_distance: 
                selected_node = node 
                shortest_distance = distance 
        
        return (selected_node, shortest_distance)

    def run(self) -> int:  
        graph = self.getDataStructure()
        startNode = graph.getStartNode()     
        goalNode = graph.getGoalNode()  

        if startNode is None or graph.getGoalNode() is None: return 1 

        visitedNodes = {}
        priorityQueue = {startNode : 0}
        goalFound = False

        crrntNode, crrntCost = self.__selectNode(priorityQueue)
        while (crrntNode is not None and not goalFound): 
            # Reset all colours 
            graph.resetColours()
            
            # Mark current node as red 
            crrntNode.setColour("red") 

            # Mark all nodes and edges current loop will look at  
            for (neighbour, _) in crrntNode.getNeighbours():
                if neighbour not in visitedNodes: 
                    crrntNode.setEdgeColour(neighbour, "red")
                else: crrntNode.setEdgeColour(neighbour, "orange")
            self.tick()   

            for (neighbour, weight) in crrntNode.getNeighbours(): 
                totalCost = crrntCost + weight 
                if neighbour not in visitedNodes or totalCost < visitedNodes[neighbour]: 
                    visitedNodes[neighbour] = totalCost
                    priorityQueue[neighbour] = totalCost
                    crrntNode.setEdgeColour(neighbour, "green")
                    neighbour.setPrevNode(crrntNode)
            self.tick()   

            if crrntNode == goalNode: goalFound = True

            del priorityQueue[crrntNode]
            crrntNode, crrntCost = self.__selectNode(priorityQueue)

        return 0

# Listen to Kingslayer (feat. BABYMETAL) by Bring Me The Horizon
