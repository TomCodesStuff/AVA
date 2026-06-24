MILLISECONDS_TO_SECONDS = 1000

class AlgorithmModel(): 
    def __init__(self):
        self.__delay = 0
        self.__minDelay = 0 
        self.__maxDelay = 0  
        self.__resolution = 0 
        self.__isDelayMilliseconds = False   
        # 1ms -> used by mediator to briefly sleep when applying delay 
        self.__sleepInterval = 0.001

    def setDelay(self, val : float) -> None:
        if val < 0: return 
        if self.__isDelayMilliseconds: self.__delay = val / MILLISECONDS_TO_SECONDS 
        else: self.__delay = val  

    def setMaxDelay(self, val : int) -> None:
        if  val > 0 and (self.__minDelay == 0 or val > self.__minDelay): 
            self.__maxDelay = val
        # Ensures delay is set to an intial value 
        if self.__delay == 0: self.setDelay(self.__maxDelay)
    
    def setMinDelay(self, val : int) -> None:
        if val > 0 and (self.__maxDelay == 0 or val < self.__maxDelay): 
            self.__minDelay = val

    def setResolution(self, val : int) -> None:
        if val > 0: self.__resolution = val  

    def setDelayToMilliseconds(self) -> None:
        self.__isDelayMilliseconds = True

    def setDelayToSeconds(self) -> None:
        self.__isDelayMilliseconds = False

    def getDelay(self) -> float: return self.__delay
    def getMaxDelay(self) -> int: return self.__maxDelay
    def getMinDelay(self) -> int: return self.__minDelay 
    def getResolution(self) -> int: return self.__resolution 
    def isDelayMilliSeconds(self) -> bool: return self.__isDelayMilliseconds 
    def getSleepInterval(self) -> float: return self.__sleepInterval


# Listen to Nancy Boy by Placebo
