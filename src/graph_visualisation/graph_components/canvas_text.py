class CanvasText():  
    def __init__(self, canvasID : int, text : str, coords : tuple):
        self.__canvasID = canvasID
        self.__text = text 
        self.__coords = coords

    def updateText(self, newText : str) -> None: 
        if newText: self.__text = newText

    def updateCoords(self, newCoords : tuple) -> tuple:
        if newCoords: self.__coords = newCoords   
    

    def getCanvasID(self) -> int: return self.__canvasID
    def getText(self) -> str: return self.__text 
    def getCoords(self) -> str: return self.__coords 

# Listen to crushcrushcrush by Paramore