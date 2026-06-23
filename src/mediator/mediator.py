import sys
import time
from typing import Callable
from src.thread_handlers import AlgorithmThread


BRIEF_DELAY = 0.5


class Mediator():
    def __init__(self, delayFunc : Callable, algorithmThread : AlgorithmThread): 
        self.__getDelay = delayFunc
        self.__algorithmThread = algorithmThread
        
    def getDelay(self) -> float:  
        return self.__getDelay() 

    def __pauseAlgorithm(self):
        # Attempts to acquire lock, pausing the thread
        self.__algorithmThread.acquirePauseLock()
        # If the lock is not released then the GUI thread will freeze next time pause button is pressed
        self.__algorithmThread.releasePauseLock()

    # Used to check is the algorithm needs to halt
    def __hasAlgorithmStopped(self): 
        # Checks if the algorithm needs to stop
        if(self.__algorithmThread.hasThreadStopped()): 
            # Output message confirming thread termination
            print("Algorithm Thread has terminated safely") 
            # Exit thread
            sys.exit(0) 

    def __handleTick(self, delay : float) -> None:
        interval = delay / 10
        i = 0 
        while(i < delay):
            self.__hasAlgorithmStopped() 
            # Checks if the GUI thread is holding the pause lock
            if(self.__algorithmThread.isThreadPaused()): self.__pauseAlgorithm()
            time.sleep(interval) 
            i += interval  

    def briefTick(self) -> None: 
        self.__handleTick(BRIEF_DELAY)

    def tick(self) -> None:  
        self.__handleTick(self.getDelay())


# Listen to Weak by Skunk Anansie
