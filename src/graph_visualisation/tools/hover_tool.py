from tkinter import Canvas
from ..graph_components import CanvasNode, CanvasEdge


class HoverTool():    
    def nodeOnHover(self, canvasNode : CanvasNode) -> None: 
        if canvasNode.getColour() != CanvasNode.getHoverColour():
            canvasNode.setPrevColour(canvasNode.getColour())
        canvasNode.setColour(CanvasNode.getHoverColour())

    def nodeOnLeave(self, canvasNode : CanvasNode) -> None:
        canvasNode.setColour(canvasNode.getPrevColour())  
    
    def edgeOnHover(self, canvas : Canvas, canvasEdge : CanvasEdge) -> None:
        canvas.itemconfig(canvasEdge.getCanvasID(), width=CanvasEdge.getHoverSize())

    def edgeOnLeave(self, canvas : Canvas, canvasEdge : CanvasEdge) -> None:
        canvas.itemconfig(canvasEdge.getCanvasID(), width=CanvasEdge.getDefaultSize()) 
    

# Listen to Hey Jude by The Beatles
