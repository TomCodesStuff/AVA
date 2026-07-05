# If this isn't at the top the program breaks :/
# If the file is run as is this message is printed and the program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

    
import math
from src.graph_visualisation.graph_components import CanvasGraph
from src.enums import EdgeDirection

# Handles all physics-based calculations 
# Need reference to graph AND node size 

class PhysicsCalculations():
    def __init__(self, canvasGraph : CanvasGraph, canvasCentre : tuple) -> None:  
        self.__canvasGraph = canvasGraph
        # Centre X-Y Coordinates the canvas 
        self.__canvasCentreX, self.__canvasCentreY = canvasCentre

        # Values for physics calculations 
        self.__forceConstant = 200
        self.__maxRepulsionDist = 40
        self.__gravityConstant = 3
        self.__maximumGravityDist = 200
        self.__springConstant = 0.025

        self.__calculationResults = [{}, {}]

    # Calculates distance between passed coords (pythagoras) 
    def __calculateDistance(self, x0 : float, y0 : float, x1 : float, y1 : float) -> float: 
        return math.sqrt(math.pow(x1 - x0, 2) + math.pow(y1 - y0, 2)) 
    
    def __calculateStandarisedVector(self, coords : tuple, dist : float) -> tuple:
        x0, y0, x1, y1 = coords 
        return ((x1 - x0) / max(dist, 0.1), (y1 - y0) / max(dist, 0.1))

    # Calculates force that drags nodes towards centre of the canvas 
    # Acts as way to stop nodes going offscreen 
    def __calculateGravity(self, nodesSnapshot : dict, nodesToForces : dict) -> None:   
        for nodeID, nodeData in nodesSnapshot.items():   
            x0, y0, _, _ = nodeData["coords"]
            circleCentreX = x0 + nodeData["offset"]
            circleCentreY = y0 + nodeData["offset"]
            
            dist = self.__calculateDistance(circleCentreX, circleCentreY, 
                                            self.__canvasCentreX, self.__canvasCentreY)
            
            if dist > self.__maximumGravityDist:
                dx, dy = self.__calculateStandarisedVector((circleCentreX, circleCentreY, 
                                                            self.__canvasCentreX, self.__canvasCentreY), dist)

                forceX = dx * self.__gravityConstant 
                forceY = dy * self.__gravityConstant  

                nodesToForces[nodeID] = (forceX, forceY)
            else: nodesToForces[nodeID] = (0, 0) 
        
    # Calculates node-node repulsion
    def __calculateNodeRepulsion(self, nodesSnapshot : dict, nodesToForces : dict) -> None: 
        # Iterate through each pair of nodes 
        nodes = list(nodesSnapshot.items())

        for i, (srcNodeID, srcNodeData) in enumerate(nodes): 
            for j in range(i + 1, len(nodes)):
                targetNodeID, targeNodeData = nodes[j]

                # X-Y coordinates of the nodes
                x0, y0, _, _ = srcNodeData["coords"]
                x1, y1, _, _, = targeNodeData["coords"]
                
                # X-Y coords of the centre of each circle
                centreX0, centreY0 = x0 + srcNodeData["offset"], y0 + srcNodeData["offset"]
                centreX1, centreY1 = x1 + targeNodeData["offset"], y1 + targeNodeData["offset"]
 
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
                    fx, fy = nodesToForces[srcNodeID]
                    nodesToForces[srcNodeID] = (fx - forceX, fy - forceY) 

                    fx, fy = nodesToForces[targetNodeID]
                    nodesToForces[targetNodeID] = (fx + forceX, fy + forceY)
        
        return nodesToForces

    def __calculateEdgeRestoration(self, edgesSnapshot : dict, nodesSnapshot : dict, nodesToForces : dict) -> None: 
        for edgeData in edgesSnapshot.values(): 

            x0, y0, _, _ = nodesSnapshot[edgeData["firstNode"]]["coords"]
            firstNodeOffset = nodesSnapshot[edgeData["firstNode"]]["offset"]
            
            x1, y1, _, _ = nodesSnapshot[edgeData["secondNode"]]["coords"]
            secondNodeOffset = nodesSnapshot[edgeData["secondNode"]]["offset"]

            
            centreX0, centreY0 = x0 + firstNodeOffset, y0 + firstNodeOffset
            centreX1, centreY1 = x1 + secondNodeOffset, y1 + secondNodeOffset
            
            dist = self.__calculateDistance(centreX0, centreY0, centreX1, centreY1) 
            displacement = dist - edgeData["screenlen"]

            dx, dy = self.__calculateStandarisedVector((centreX0, centreY0, centreX1, centreY1), dist)  
            # Calcalate spring restoration force applied to both nodes 
            springForce = displacement * self.__springConstant
            forceX, forceY = springForce * dx, springForce * dy

            fx, fy = nodesToForces[edgeData["firstNode"]]
            nodesToForces[edgeData["firstNode"]] = (fx + forceX, fy + forceY)

            fx, fy = nodesToForces[edgeData["secondNode"]]
            nodesToForces[edgeData["secondNode"]] = (fx - forceX, fy - forceY)

    def __applyForcesToNodes(self, nodesSnapshot : dict, nodesToForces : dict) -> dict:
        nodeToUpdatedCoords = {} 
        for nodeID, nodeData in nodesSnapshot.items():
            if nodeID in nodesToForces:  
                forceX, forceY = nodesToForces[nodeID]
                x0, y0, _, _ = nodesSnapshot[nodeID]["coords"] 
                nodeSize = nodesSnapshot[nodeID]["size"]
                newX0, newY0 = x0 + forceX, y0 + forceY 
                nodeToUpdatedCoords[nodeID] = (newX0, newY0, newX0 + nodeSize, newY0 + nodeSize)
            else: nodeToUpdatedCoords[nodeID] = nodeData["coords"]
        return nodeToUpdatedCoords

    # Stole from ChatGPT, would take me way to long to find an acceptable solution :/
    # I dislike using AI as I think it's kinda cheating but I'll make an exception to finish this project
    # Makes arrows indicating edge direction visible rather than just being hidden behind each node
    def __applyForcesToEdges(self, nodesSnapshot : dict, edgesSnapshot : dict, nodesToUpdatedCoords : dict) -> None: 
        edgesToUpdatedCoords = {}
        for edgeID, edgeData in edgesSnapshot.items():
            x0, y0, _, _ = nodesToUpdatedCoords[edgeData["firstNode"]]
            firstNodeOffset = nodesSnapshot[edgeData["firstNode"]]["offset"]
            
            x1, y1, _, _ = nodesToUpdatedCoords[edgeData["secondNode"]]
            secondNodeOffset = nodesSnapshot[edgeData["secondNode"]]["offset"]

            centreX0, centreY0 = x0 + firstNodeOffset, y0 + firstNodeOffset
            centreX1, centreY1 = x1 + secondNodeOffset, y1 + secondNodeOffset
            
            dx = centreX1 - centreX0
            dy = centreY1 - centreY0 

            adjustedX0, adjustedY0 = centreX0, centreY0
            adjustedX1, adjustedY1 = centreX1, centreY1

            dist = math.sqrt(dx ** 2 + dy ** 2)
            if dist < firstNodeOffset + secondNodeOffset + 5: edgesToUpdatedCoords[edgeID] = (centreX0, centreY0, centreX1, centreY1) 
            
            if edgeData["direction"] in (EdgeDirection.SECOND_TO_FIRST, EdgeDirection.BIDIRECTIONAL): 
                adjustedX0 = round(centreX0 + (dx / dist) * firstNodeOffset)
                adjustedY0 = round(centreY0 + (dy / dist) * firstNodeOffset)
            if edgeData["direction"] in (EdgeDirection.FIRST_TO_SECOND, EdgeDirection.BIDIRECTIONAL): 
                adjustedX1 = round(centreX1 - (dx / dist) * secondNodeOffset)
                adjustedY1 = round(centreY1 - (dy / dist) * secondNodeOffset)
            
            edgesToUpdatedCoords[edgeID] = (adjustedX0, adjustedY0, adjustedX1, adjustedY1) 
                      
        return edgesToUpdatedCoords
        
    # Calculate and apply forces to each object drawn on screen
    def applyPhysics(self) -> None:  
                
        # Snapshot of node coords and offset, copies of lists used to prevent crashes(?)
        nodesSnapshot = {x.getCanvasID() : x.getRequiredPhysicsData() 
                         for x in self.__canvasGraph.getCanvasNodes().copy()}
        edgesSnapshot = {x.getCanvasID() : x.getRequiredPhysicsData() 
                         for x in self.__canvasGraph.getCanvasEdges().copy()}

        nodesToForces = {} 

        # Calculate forces applied to each node -> gravity, repulsion
        self.__calculateGravity(nodesSnapshot, nodesToForces)
        self.__calculateNodeRepulsion(nodesSnapshot, nodesToForces)         
        self.__calculateEdgeRestoration(edgesSnapshot, nodesSnapshot, nodesToForces) 

        nodesToUpdatedCoords = self.__applyForcesToNodes(nodesSnapshot, nodesToForces)
        edgesToUpdatedCoords = self.__applyForcesToEdges(nodesSnapshot, edgesSnapshot, nodesToUpdatedCoords)

        # Update results after all calculations done 
        self.__calculationResults = [nodesToUpdatedCoords, edgesToUpdatedCoords]
        
    def getLatestResults(self) -> dict: return self.__calculationResults.copy()


# Listen to Yesterday by The Beatles  
