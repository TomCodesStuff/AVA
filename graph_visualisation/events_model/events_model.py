from ..graph_components import CanvasNode

class EventsModel(): 
    def __init__(self):        
        # Account for small border around canvas 
        self.__canvasUpperBoundOffset = 4
        self.__canvasLowerBoundOffset = 2 

        self.__canvasWidth = 0
        self.__canvasHeight = 0

        self.__defaultEdgeWeight = 20
        self.__defaultEdgeColour = "black"
        self.__editEdgeColour = "red"
        self.__defaultEdgeSize = "3" 
        self.__edgeHoverWidth = "5"


    def getCanvasLowerBoundOffset(self) -> tuple: return self.__canvasLowerBoundOffset
    def getCanvasUpperBoundOffset(self) -> tuple:return self.__canvasUpperBoundOffset
    def getCanvasWidth(self) -> int: return self.__canvasWidth
    def getCanvasHeight(self) -> int: return self.__canvasHeight
    
    def setCanvasWidth(self, width : int) -> None: self.__canvasWidth = width
    def setCanvasHeight(self, height : int) -> None: self.__canvasHeight = height 
    
    def getDefaultEdgeWeight(self) -> int: return self.__defaultEdgeWeight
    def getDefaultEdgeColour(self) -> str: return self.__defaultEdgeColour 
    def getEdgeEditColour(self) -> str: return self.__editEdgeColour
    def getDefaultEdgeSize(self) -> str: return self.__defaultEdgeSize 
    def getEdgeHoverWidth(self) -> str: return self.__edgeHoverWidth  


# Listen to Just Like Heaven by The Cure