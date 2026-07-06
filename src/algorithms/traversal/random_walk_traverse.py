# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

import random 
from src.algorithms import Algorithm 
from src.data_structures import Graph

class RandomWalkTraverse(Algorithm[Graph]):
    # Constructor
    def __init__(self):
        super().__init__() 
    
    def getName(self) -> str: 
        return "Random Walk" 

    def run(self) -> int:  
        graph = self.getDataStructure()
        startNode = graph.getStartNode()
        goalNode = graph.getGoalNode()

        if startNode is None or goalNode is None: return 1 
        
        visitedNodes = set()
        crrntNode = startNode
        goalNodeFound = False

        # Whilst there are unvisited nodes or goal has not been found
        while crrntNode is not None and not goalNodeFound:
            crrntNode.setColour("red")
            # Set colour of edge connecting node to prior node red 
            prevNode = crrntNode.getPrevNode() 
            if prevNode is not None: prevNode.setEdgeColour(crrntNode, "red")
            # Mark node as  visited
            visitedNodes.add(crrntNode)            


            neighbours = []
            # Add all unvisited neighbours to the stacl 
            for (neighbour, _) in crrntNode.getNeighbours(): 
                if neighbour not in visitedNodes: 
                    neighbour.setPrevNode(crrntNode)
                    neighbours.append(neighbour) 
                    crrntNode.setEdgeColour(neighbour, "orange")
            self.tick()

            # Reset colours for the unexplored edges 
            for (neighbour, _) in crrntNode.getNeighbours():
                if neighbour not in visitedNodes: 
                    crrntNode.resetEdgeColour(neighbour)
            self.briefTick()

            if crrntNode == goalNode: goalNodeFound = True

            if not neighbours: crrntNode = None 
            else: crrntNode = random.choice(neighbours)

        return 0
    
# Listen to Waste a moment by Kings of Leon
