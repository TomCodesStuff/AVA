# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from ..array_algorithm import ArrayAlgorithmModel


class SearchModel(ArrayAlgorithmModel): 
    def __init__(self) -> None:  
        super().__init__()
        
        self.setResolution(0.1)
        self.setMinDelay(0.1)
        self.setMaxDelay(4)
        
        self.__targetSetting = 0

        # Dictionary pairing numbers to speed 
        # This allows the slider to show text rather than just numbers
        self.__numbersToText = {
            0: "Target: Random", 
            1: "Target: In array",
            2: "Target: Not in array"
        } 


    def setTargetSetting(self, value : int) -> None: 
        if value in self.__numbersToText: self.__targetSetting = value


    def getTargetSetting(self) -> int: 
        return self.__targetSetting


    # Returns the text to be displayed above the target slider 
    def getSliderText(self, sliderValue : int) -> str: 
        return self.__numbersToText[sliderValue]
    
# Listen to Creep by Radiohead
