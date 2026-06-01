from tkinter import Canvas, BOTH
from ..graph_components import CanvasGraph, CanvasNode, CanvasEdge


class CreationTool():
    # TODO re-add max number nodes check 
    def canNodeBeSpawned(self, canvas : Canvas, nodeCoords : tuple) -> bool:
        if nodeCoords == (): nodeCoords = CanvasNode.getDefaultCoords()
        x0, y0, x1, y1 = nodeCoords 
        overlapOffset = CanvasNode.getMinSpawnDistance() + CanvasNode.getDefaultSize()
        overlapping_nodes = canvas.find_overlapping(x0 - overlapOffset, y0 - overlapOffset, 
                                                    x1 + overlapOffset, y1 + overlapOffset)
        return True if len(overlapping_nodes) == 0 else False

    def renderNode(self, canvas : Canvas, canvasNode : CanvasNode) -> None: 
        x0, y0, x1, y1 = canvasNode.getCoords() 
        canvasID = canvas.create_oval(x0, y0, x1, y1, outline="black", fill=canvasNode.getColour())
        canvasNode.setCanvasID(canvasID)

    def createNode(self, canvasGraph : CanvasGraph, coords : tuple) -> CanvasNode:
        if coords == (): coords = CanvasNode.getDefaultCoords()
        canvasNode = CanvasNode(coords) 
        canvasGraph.addCanvasNode(canvasNode)
        return canvasNode

    def deleteNode(self, canvasGraph : CanvasGraph, canvasNode : CanvasNode):
        canvasGraph.deleteCanvasNode(canvasNode) 

    def renderEdge(self, canvas : Canvas, canvasEdge : CanvasEdge) -> None: 
        x0, y0, x1, y1 = canvasEdge.getCoords() 
        canvasID = canvas.create_line(x0, y0, x1, y1, fill=canvasEdge.getColour(), 
                                      width = CanvasEdge.getDefaultSize(), arrow=BOTH)
        canvasEdge.setCanvasID(canvasID)
        canvas.tag_lower(canvasID)
    
    def redrawEdge(self, canvas : Canvas, canvasEdge : CanvasEdge) -> None:
        canvas.coords(canvasEdge.getCanvasID(), canvasEdge.getCoords())

    def createEdge(self, canvasNode : CanvasNode) -> CanvasEdge:
        nodeOffset = canvasNode.getOffset()
        x0, y0, _, _ = canvasNode.getCoords()
        canvasEdge = CanvasEdge((x0 + nodeOffset, y0 + nodeOffset, x0 + nodeOffset, y0 + nodeOffset))
        canvasEdge.setFirstNode(canvasNode)  
        return canvasEdge  

    def deleteEdge(self, canvasGraph : CanvasGraph, canvasEdge : CanvasEdge) -> None: 
        canvasGraph.deleteCanvasEdge(canvasEdge)


# Listen to Perfect by The Smashing Pumpkins
