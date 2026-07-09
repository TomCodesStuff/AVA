# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from src.algorithms import Algorithm 
from src.data_structures import Graph, Node

class AStarTraverse(Algorithm[Graph]):
    # Constructor
    def __init__(self):
        super().__init__() 
    
    def getName(self) -> str: 
        return "A*" 

    def __selectNode(self, unvisitedNodes : dict) -> Node|None: 
        selected_node = None 
        lowestFCost = float("inf")

        # (Node, (g(n), f(n)))
        for (node, (_, fCost)) in unvisitedNodes.items(): 
            if fCost < lowestFCost: 
                selected_node = node 
                lowestFCost = fCost
        
        return selected_node

    def run(self) -> int:   
        graph = self.getDataStructure()
        startNode = graph.getStartNode()
        goalNode = graph.getGoalNode()
        goalFound = False

        if startNode is None or graph.getGoalNode() is None: return 1 

        # Node : (g(n), f(n))
        unvisitedNodes = {
            node : (float("inf"), float("inf")) if node != startNode else (0, startNode.getHeuristicValue()) 
            for node in graph.get()
        }
   
        # While there is an unvisited node 
        while((crrntNode := self.__selectNode(unvisitedNodes)) is not None and not goalFound):   
            # Reset all colours 
            graph.resetColours()
            
            # Mark current node as red 
            crrntNode.setColour("red")

            crrntCost, _ = unvisitedNodes[crrntNode]

            # Mark all nodes and edges current loop looks at  
            for (neighbour, _) in crrntNode.getNeighbours():
                if neighbour in unvisitedNodes: 
                    crrntNode.setEdgeColour(neighbour, "red")
                else: crrntNode.setEdgeColour(neighbour, "orange")
            self.tick()

            for (neighbour, weight) in crrntNode.getNeighbours(): 
                # Calculate potential new g(n) for the neighbour
                newCost = crrntCost + weight
                heuristic = neighbour.getHeuristicValue()  

                if neighbour in unvisitedNodes:
                    # Get Previous G(n) for neighbour
                    oldCost, _ = unvisitedNodes[neighbour]
                    if newCost < oldCost:
                        crrntNode.setEdgeColour(neighbour, "green")
                        # Update g(n) and f(n) for the neighbour
                        unvisitedNodes[neighbour] = (newCost, newCost + heuristic)
                        neighbour.setPrevNode(crrntNode)

                self.tick()
            
            # Can stop execution when the goal node has been reached
            if crrntNode == goalNode: goalFound = True
            
            # Mark node as visisted 
            del unvisitedNodes[crrntNode]
            
            self.tick()

        return 0

# Listen to Am I Dreaming by Metro Boomin (Feat. A$SP Rocky, Roisee)
# The Across The Spider-Verse Soundtrack was listened to a lot during the creation of this project
# So for the final algorithm it seems fitting to reference a song from the legendary movie here :).  
