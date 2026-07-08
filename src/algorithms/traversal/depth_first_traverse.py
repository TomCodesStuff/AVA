# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from src.algorithms import Algorithm 
from src.data_structures import Graph

class DepthFirstTraverse(Algorithm[Graph]):
    # Constructor
    def __init__(self):
        super().__init__() 
    
    def getName(self) -> str: 
        return "Depth First" 

    def run(self) -> int:  
        graph = self.getDataStructure()
        startNode = graph.getStartNode()
        goalNode = graph.getGoalNode()

        if startNode is None or goalNode is None: return 1 
        
        visitedNodes = set()
        nodeStack = [startNode]
        goalNodeFound = False

        # Whilst there are unvisited nodes or goal has not been found
        while nodeStack and not goalNodeFound:
            # Remove last node from the stack
            crrntNode = nodeStack.pop() 
            crrntNode.setColour("red")
            
            # Set colour of edge connecting node to prior node red 
            prevNode = crrntNode.getPrevNode() 
            if prevNode is not None: prevNode.setEdgeColour(crrntNode, "red")
            
            # Can end loop if the goal has been reached 
            if crrntNode == goalNode: goalNodeFound = True

            visitedNodes.add(crrntNode)            

            # Add all unvisited neighbours to the stacl 
            for (neighbour, _) in crrntNode.getNeighbours(): 
                if neighbour not in visitedNodes and neighbour not in nodeStack: 
                    neighbour.setPrevNode(crrntNode)
                    nodeStack.append(neighbour) 
                    crrntNode.setEdgeColour(neighbour, "orange")
            self.tick()

            # Reset colours for the unexplored edges 
            for (neighbour, _) in crrntNode.getNeighbours():
                if neighbour not in visitedNodes: 
                    crrntNode.resetEdgeColour(neighbour)
            self.briefTick()

        return 0
    
# Listen to A letter to Elise by The Cure
