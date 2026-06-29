class CanvasText():  
    def __init__(self, text : str, coords : tuple):
        self.__canvasID = None 
        self.__text = text 
        self.__coords = coords

    def updateText(self, newText : str) -> None: 
        if newText: self.__text = newText

    def updateCoords(self, newCoords : tuple) -> tuple:
        if newCoords: self.__coords = newCoords   
    
    def setCanvasID(self, canvasID : int) -> None: 
        if canvasID: self.__canvasID  = canvasID

    def getCanvasID(self) -> int: return self.__canvasID
    
    def getText(self) -> str: return self.__text 
    
    def getCoords(self) -> str: return self.__coords 

# Listen to crushcrushcrush by Paramore