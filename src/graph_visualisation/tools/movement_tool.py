from ..events_model import EventsModel
from ..graph_components import CanvasNode, CanvasEdge

# TODO Make NodeOffset be based on nodes actual size not default

class MovementTool(): 
    def __init__(self, eventsModel : EventsModel):
        self.__eventsModel = eventsModel
    

    # This prevents nodes from being dragged off canvas 
    # Could likely do with some refactoring but it just works 
    def __calculateCoords(self, x : int, y : int) -> tuple:  
        # Values needed for calculations
        nodeSize = CanvasNode.getDefaultSize()
        nodeoffset = nodeSize // 2
        canvasWidth = self.__eventsModel.getCanvasWidth()
        canvasHeight = self.__eventsModel.getCanvasHeight()

        # Checks if mouse has gone out of bounds to the left 
        # Stops the node from moving off the canvas
        x0 = max(x - nodeoffset, self.__eventsModel.getCanvasLowerBoundOffset()) 
        # Checks if mouse has gone out of bounds to the right 
        # Stops the node from moving off the canvas
        x0 = min(x0, canvasWidth - self.__eventsModel.getCanvasUpperBoundOffset() - nodeSize) 

        # Checks if mouse has gone out of bounds by going above the canvas
        # Stops the node from moving off the canvas 
        y0 = max(y - nodeoffset, self.__eventsModel.getCanvasLowerBoundOffset()) 
        # Checks if mouse has gone out of bounds by going below the canvas
        # Stops the node from moving off the canvas 
        y0 = min(y0, canvasHeight - self.__eventsModel.getCanvasUpperBoundOffset() - nodeSize)  

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
        canvasEdge.updateCoords((x0 + startNode.getOffset(), y0 + + startNode.getOffset(), 
                                x1 + endNode.getOffset(), y1 + endNode.getOffset()))


    def moveEdge(self, canvasEdge : CanvasEdge, eventCoords : tuple) -> None:
        nodeOffset = canvasEdge.getStartNode().getOffset()
        x0, y0, _, _ = canvasEdge.getStartNode().getCoords()
        event_x, event_y = eventCoords
        canvasEdge.updateCoords((x0 + nodeOffset, y0 + nodeOffset, event_x, event_y)) 


# Listen to Friday I'm In Love by The Cure
