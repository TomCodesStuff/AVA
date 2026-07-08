import sys
import time
from typing import Callable
from src.thread_handlers import AlgorithmThread


BRIEF_DELAY = 0.5
SUCCESS_EXIT_CODE = 0

class Mediator():
    def __init__(self, getDelayCallback : Callable, algorithmThread : AlgorithmThread, sleepInterval : float): 
        self.__getDelay = getDelayCallback 
        self.__algorithmThread = algorithmThread
        self.__sleepInterval = sleepInterval
        
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
            sys.exit(SUCCESS_EXIT_CODE) 

    def __handleTick(self, delay : float) -> None: 
        delay_loop_running = True 
        start = time.time() 
        while(delay_loop_running):
            # Halt Algorithm if stop flag set
            self.__hasAlgorithmStopped() 
            # Checks if the GUI thread is holding the pause lock
            if(self.__algorithmThread.isThreadPaused()): self.__pauseAlgorithm()
            if time.time() - start >= delay: delay_loop_running  = False 
            time.sleep(self.__sleepInterval)
 
    def briefTick(self) -> None: 
        self.__handleTick(BRIEF_DELAY)

    def tick(self) -> None:  
        self.__handleTick(self.getDelay())

# Listen to Weak by Skunk Anansie
