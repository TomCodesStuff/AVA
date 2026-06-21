from ..graph_components import CanvasNode, CanvasEdge

# TODO Make NodeOffset be based on nodes actual size not default

class MovementTool(): 
    def __init__(self, canvasWidth : int, canvasHeight : int): 
        self.canvasWidth = canvasWidth 
        self.canvasHeight = canvasHeight 

        # Account for small border around canvas (Hard coded but should be fine)
        self.__canvasUpperBoundOffset = 4
        self.__canvasLowerBoundOffset = 2 

    
    # This prevents nodes from being dragged off canvas 
    # Could likely do with some refactoring but it just works 
    def __calculateCoords(self, x : int, y : int) -> tuple:  
        # Values needed for calculations
        nodeSize = CanvasNode.getDefaultSize()
        nodeoffset = nodeSize // 2
        
        # Checks if mouse has gone out of bounds to the left 
        # Stops the node from moving off the canvas
        x0 = max(x - nodeoffset, self.__canvasLowerBoundOffset) 
        # Checks if mouse has gone out of bounds to the right 
        # Stops the node from moving off the canvas
        x0 = min(x0, self.canvasWidth - self.__canvasUpperBoundOffset - nodeSize) 

        # Checks if mouse has gone out of bounds by going above the canvas
        # Stops the node from moving off the canvas 
        y0 = max(y - nodeoffset, self.__canvasLowerBoundOffset) 
        # Checks if mouse has gone out of bounds by going below the canvas
        # Stops the node from moving off the canvas 
        y0 = min(y0, self.canvasHeight - self.__canvasUpperBoundOffset - nodeSize)  

        # The above could be done in one line but just because it can doesn't mean it should 
        # Doing it in one line would make the calculations very hard to read  
        return(x0, y0, x0 + nodeSize, y0 + nodeSize)

    def moveNode(self, canvasNode : CanvasNode, eventCoords : tuple) -> None: 
        eventX, eventY = eventCoords
        newCoords = self.__calculateCoords(eventX, eventY)
        canvasNode.updateCoords(newCoords) 

    def connectEdgeToNodes(self, canvasEdge : CanvasEdge) -> None: 
        startNode, endNode = canvasEdge.getNodes()
        
        x0, y0, _, _ = startNode.getCoords() 
        x1, y1, _, _ = endNode.getCoords() 
        canvasEdge.updateCoords((x0 + startNode.getOffset(), y0 + startNode.getOffset(), 
                                x1 + endNode.getOffset(), y1 + endNode.getOffset()))

    def moveEdge(self, canvasEdge : CanvasEdge, eventCoords : tuple) -> None:
        nodeOffset = canvasEdge.getFirstNode().getOffset()
        x0, y0, _, _ = canvasEdge.getFirstNode().getCoords()
        event_x, event_y = eventCoords
        canvasEdge.updateCoords((x0 + nodeOffset, y0 + nodeOffset, event_x, event_y)) 


# Listen to Friday I'm In Love by The Cure
