# If this isn't at the top the program breaks :/
# If the file is run as is this message is printed and the program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

    
import math
from src.graph_visualisation.graph_components import CanvasGraph, CanvasNode


# Handles all physics-based calculations 
# Need reference to graph AND node size 

class PhysicsCalculations():
    def __init__(self, canvasGraph : CanvasGraph, canvasCentre : tuple) -> None:  
        self.__canvasGraph = canvasGraph
        # Centre X-Y Coordinates the canvas 
        self.__canvasCentreX, self.__canvasCentreY = canvasCentre

        # Values for physics calculations 
        self.__forceConstant = 200
        self.__maxRepulsionDist = 50 
        self.__gravityConstant = 2
        self.__maximumGravityDist = 150
        self.__springConstant = 0.05

        self.__calculationResults = {}

    # Calculates distance between passed coords (pythagoras) 
    def __calculateDistance(self, x0 : float, y0 : float, x1 : float, y1 : float) -> float: 
        return math.sqrt(math.pow(x1 - x0, 2) + math.pow(y1 - y0, 2)) 
    
    def __calculateStandarisedVector(self, coords : tuple, dist : float) -> tuple:
        x0, y0, x1, y1 = coords 
        return ((x1 - x0) / max(dist, 0.1), (y1 - y0) / max(dist, 0.1))

    # Calculates force that drags nodes towards centre of the canvas 
    # Acts as way to stop nodes going offscreen 
    def __calculateGravity(self, nodesSnapshot : dict, nodes_to_forces : dict) -> None:   
        for nodeID, (nodeCoords, nodeOffset) in nodesSnapshot.items():   
            x0, y0, _, _ = nodeCoords
            circleCentreX = x0 + nodeOffset
            circleCentreY = y0 + nodeOffset
            
            dist = self.__calculateDistance(circleCentreX, circleCentreY, 
                                            self.__canvasCentreX, self.__canvasCentreY)
            
            if dist > self.__maximumGravityDist:
                dx, dy = self.__calculateStandarisedVector((circleCentreX, circleCentreY, 
                                                            self.__canvasCentreX, self.__canvasCentreY), dist)

                forceX = dx * self.__gravityConstant 
                forceY = dy * self.__gravityConstant  

                nodes_to_forces[nodeID] = (forceX, forceY)
            else: nodes_to_forces[nodeID] = (0, 0) 
        
    # Calculates node-node repulsion
    def __calculateNodeRepulsion(self, nodesSnapshot : dict, nodes_to_forces) -> None: 
        # Iterate through each pair of nodes 
        nodes = list(nodesSnapshot.items())

        for i, (srcNodeID, (srcNodeCoords, srcNodeOffset)) in enumerate(nodes): 
            for j in range(i + 1, len(nodes)):
                targetNodeID, (targetNodeCoords, targetNodeOffset) = nodes[j]

                # X-Y coordinates of the nodes
                x0, y0, _, _ = srcNodeCoords
                x1, y1, _, _, = targetNodeCoords
                
                # X-Y coords of the centre of each circle
                centreX0, centreY0 = x0 + srcNodeOffset, y0 + srcNodeOffset
                centreX1, centreY1 = x1 + targetNodeOffset, y1 + targetNodeOffset
 
                # Calculated pythagorean distance between the circles
                dist = self.__calculateDistance(centreX0, centreY0, centreX1, centreY1)  
                
                if dist <= self.__maxRepulsionDist:                
                    # Resultant force as a scalar 
                    force = (self.__forceConstant) / max(dist, 1) 
                    # Convert scalar coords into standardised vector form 
                    dx, dy = self.__calculateStandarisedVector((centreX0, centreY0, centreX1, centreY1), dist) 
                    # Calculate X-Y forces to be applied to each node
                    forceX, forceY = dx * force, dy * force
                    
                    # Update forces for each node
                    fx, fy = nodes_to_forces[srcNodeID]
                    nodes_to_forces[srcNodeID] = (fx - forceX, fy - forceY) 

                    fx, fy = nodes_to_forces[targetNodeID]
                    nodes_to_forces[targetNodeID] = (fx + forceX, fy + forceY)
        
        return nodes_to_forces

    def __calculateEdgeRestoration(self, edgesSnapshot : set, nodesSnapshot : dict, nodes_to_forces : dict) -> None: 
        for (startNodeID, endNodeID) in edgesSnapshot: 
            (x0, y0, _, _), startNodeOffset = nodesSnapshot[startNodeID]
            (x1, y1, _, _), endNodeOffset = nodesSnapshot[endNodeID] 
            
            centreX0, centreY0 = x0 + startNodeOffset, y0 + startNodeOffset
            centreX1, centreY1 = x1 + endNodeOffset, y1 + endNodeOffset
            
            dist = self.__calculateDistance(centreX0, centreY0, centreX1, centreY1) 
            # TODO reimplement screen length 
            displacement = dist - 100

            dx, dy = self.__calculateStandarisedVector((centreX0, centreY0, centreX1, centreY1), dist)  
            # Calcalate spring restoration force applied to both nodes 
            springForce = displacement * self.__springConstant
            forceX, forceY = springForce * dx, springForce * dy

            fx, fy = nodes_to_forces[startNodeID]
            nodes_to_forces[startNodeID] = (fx + forceX, fy + forceY)

            fx, fy = nodes_to_forces[endNodeID]
            nodes_to_forces[endNodeID] = (fx - forceX, fy - forceY)

    # Caclulate and apply forces to each object drawn on screen
    def applyPhysics(self) -> None:  
        # Snapshot of node coords and offset
        nodesSnapshot = {x.getID() : (x.getCoords(), x.getOffset()) for x in self.__canvasGraph.getNodes()}
        edgesSnapshot = {(x.getStartNode().getID(), x.getEndNode().getID()) 
                          for x in self.__canvasGraph.getEdges()}

        nodes_to_forces = {}
        
        self.__calculateGravity(nodesSnapshot, nodes_to_forces)
        self.__calculateNodeRepulsion(nodesSnapshot, nodes_to_forces) 
        self.__calculateEdgeRestoration(edgesSnapshot, nodesSnapshot, nodes_to_forces)
        
        self.__calculationResults = nodes_to_forces
        
    def getLatestResults(self) -> dict: return self.__calculationResults


# Listen to Yesterday by The Beatles  
