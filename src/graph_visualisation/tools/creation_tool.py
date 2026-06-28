from tkinter import Canvas, BOTH
from ..graph_components import CanvasGraph, CanvasNode, CanvasEdge, CanvasText


class CreationTool():
    # TODO re-add max number nodes check 
    def canNodeBeSpawned(self, canvas : Canvas, nodeCoords : tuple) -> bool:
        if nodeCoords == (): nodeCoords = CanvasNode.getDefaultCoords()
        x0, y0, x1, y1 = nodeCoords 
        overlapOffset = CanvasNode.getMinSpawnDistance() + CanvasNode.getDefaultSize()
        overlapping_nodes = canvas.find_overlapping(x0 - overlapOffset, y0 - overlapOffset, 
                                                    x1 + overlapOffset, y1 + overlapOffset)
        return True if len(overlapping_nodes) == 0 else False

    def createText(self, textCanvasID : int, text : str, textCoords : tuple) -> CanvasText:
        return CanvasText(textCanvasID, text, textCoords)
    
    def renderNode(self, canvas : Canvas, canvasNode : CanvasNode) -> None: 
        x0, y0, x1, y1 = canvasNode.getCoords() 
        cx, cy = x0 + canvasNode.getOffset(), y0 + canvasNode.getOffset() 
        nodeCanvasID = canvas.create_oval(x0, y0, x1, y1, outline="black", fill=canvasNode.getColour())
        textCanvasID = canvas.create_text(cx, cy, text=str(canvasNode.getID()), fill="white", font=("Arial", 10, "bold"))
        canvasText = self.createText(textCanvasID, str(canvasNode.getID()), (cx, cy))
        
        canvasNode.setCanvasID(nodeCanvasID) 
        canvasNode.setCanvasText(canvasText)

    def createNode(self, canvasGraph : CanvasGraph, coords : tuple) -> CanvasNode:
        if coords == (): coords = CanvasNode.getDefaultCoords()
        canvasNode = CanvasNode(coords)  
        canvasGraph.addCanvasNode(canvasNode)
        return canvasNode

    def renderEdge(self, canvas : Canvas, canvasEdge : CanvasEdge) -> None: 
        x0, y0, x1, y1 = canvasEdge.getCoords() 
        canvasID = canvas.create_line(x0, y0, x1, y1, fill=canvasEdge.getColour(), 
                                      width = CanvasEdge.getDefaultSize(), arrow=BOTH)
        canvasEdge.setCanvasID(canvasID)
        canvas.tag_lower(canvasID)
    
    def createEdge(self, canvasNode : CanvasNode) -> CanvasEdge:
        nodeOffset = canvasNode.getOffset()
        x0, y0, _, _ = canvasNode.getCoords()
        canvasEdge = CanvasEdge((x0 + nodeOffset, y0 + nodeOffset, x0 + nodeOffset, y0 + nodeOffset))
        canvasEdge.setFirstCanvasNode(canvasNode)  
        return canvasEdge  

# Listen to Perfect by The Smashing Pumpkins
