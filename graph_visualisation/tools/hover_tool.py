from tkinter import Canvas
from ..graph_components import CanvasNode, CanvasEdge
from ..events_model import EventsModel

class HoverTool():
    def __init__(self, eventsModel : EventsModel):
        self.__eventsModel = eventsModel
    

    def nodeOnHover(self, canvasNode : CanvasNode) -> None:
        canvasNode.setColour(CanvasNode.getHoverColour())


    def nodeOnLeave(self, canvasNode : CanvasNode) -> None:
        canvasNode.setColour(CanvasNode.getDefaultColour())  
    

    def edgeOnHover(self, canvas : Canvas, canvasEdge : CanvasEdge) -> None:
        canvas.itemconfig(canvasEdge.getCanvasID(), width=self.__eventsModel.getEdgeHoverWidth())


    def edgeOnLeave(self, canvas : Canvas, canvasEdge : CanvasEdge) -> None:
        canvas.itemconfig(canvasEdge.getCanvasID(), width=self.__eventsModel.getDefaultEdgeSize()) 
    

# Listen to Hey Jude by The Beatles
