from __future__ import annotations

# If this isn't at the top the program breaks :/ 
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, TypeVar, Generic
from mediator import Mediator
from thread_handlers import AlgorithmThread, ManagedThread
from data_structures import DataStructure
from enums import AlgorithmType


if TYPE_CHECKING:
    from algorithm_base import AlgorithmScreen, AlgorithmModel


S = TypeVar("S", bound="AlgorithmScreen")
M = TypeVar("M", bound="AlgorithmModel")
D = TypeVar("D", bound="DataStructure")

# 16MS = ~ 60 FPS
EXECUTION_DELAY = 16

class AlgorithmController(ABC, Generic[S, M, D]):  

    def __init__(self, screen : S, model : M, dataStructure : D):
        self.__screen = screen
        self.__model = model
        self.__dataStructure = dataStructure
        
        self.__algorithmThread = None
        self.__managedThreads = []

    
    @abstractmethod
    def refreshCanvas(self, refreshColours:bool=False) -> None: pass


    # Cancels any scheduled function calls left by a terminated thread
    def cancelScheduledProcesses(self):
        # If there are still processed scheduled from the terminated thread
            if(self.__screen.getWindow().getNumScheduledFunctions() > 0):  
                # Stop all processes 
                self.__screen.getWindow().cancelScheduledFunctions()   
    

    def startAlgorithmThread(self, algorithmType : AlgorithmType, algorithmName : str) -> None:    
        if self.__algorithmThread is not None: self.stopAlgorithmThread()
        
        # Stop Any Managed Threads -> preventing any issues 
        self.stopManagedThreads()
        
        algorithmClass = self.getScreen().getWindow().getAlgorithmClass(algorithmType, algorithmName) 
        if algorithmClass is None: return 
         
        try:
            algorithmObj = algorithmClass()
        except Exception as e: 
            print(f"ERROR: Unable to create algorithm object: {e}")
            self.getScreen().algorithmComplete(playAnimation=False)
            return
        
        self.__algorithmThread = AlgorithmThread(algorithmObj)
        mediator = Mediator(self.getAlgorithmDelay, self.__algorithmThread)

        try:
            algorithmObj.setDataStructure(self.getDataStructure())
            algorithmObj.setMediator(mediator)
        except Exception as e:
            self.getScreen().algorithmComplete(playAnimation=False)
            print(f"ERROR: {e}")
            return


        # Start running algorithm thread, so this project has as use 
        self.__algorithmThread.start()
        self.__handleAlgorithmExecution()


    def stopAlgorithmThread(self) -> None: 
        if self.__algorithmThread is None: return
        self.cancelScheduledProcesses()
        self.__algorithmThread.stopAlgorithm()
        self.__algorithmThread = None 


    def resumeAlgorithm(self) -> None: 
        if self.__algorithmThread is None: return
        self.__algorithmThread.releasePauseLock() 


    def pauseAlgorithm(self) -> None: 
        if self.__algorithmThread is None: return
        self.__algorithmThread.acquirePauseLock() 
    

    def isAlgorithmPaused(self) -> bool: 
        if self.__algorithmThread is None: return False
        return self.__algorithmThread.isThreadPaused()
    
    
    def isAlgorithmRunning(self) -> bool: 
        if self.__algorithmThread is None: return False
        return self.__algorithmThread.isThreadAlive()


    def updateAlgorithmDelay(self, delay : float) -> None: 
        if self.__algorithmThread is None: self.__model.setDelay(delay)
        else:
            self.__algorithmThread.acquireDelayLock() 
            self.__model.setDelay(delay)
            self.__algorithmThread.releaseDelayLock() 


    def getAlgorithmDelay(self) -> float:
        self.__algorithmThread.acquireDelayLock() 
        delay = self.__model.getDelay()
        self.__algorithmThread.releaseDelayLock() 
        return delay


    def getScreen(self) -> S: return self.__screen 
    def getModel(self) -> M: return self.__model
    def getDataStructure(self) -> D: return self.__dataStructure
    

    def scheduleScreenUpdate(self) -> None:
        self.__screen.getWindow().scheduleFunctionExecution(self.refreshCanvas, EXECUTION_DELAY) 

    
    def __handleAlgorithmExecution(self) -> None: 
        if not self.__algorithmThread.isThreadAlive(): 
            self.refreshCanvas(refreshColours=False)
            self.getScreen().algorithmComplete(self.__algorithmThread.wasAlgorithmSuccessful())
            self.__algorithmThread = None
        else: 
            self.refreshCanvas(refreshColours=False)
            self.getScreen().getWindow().scheduleFunctionExecution(self.__handleAlgorithmExecution, EXECUTION_DELAY) 
       
    
    def isAlgorithmRunning(self) -> bool: 
        if self.__algorithmThread is None: return False
        return self.__algorithmThread.isThreadAlive()
    

    def addManagedThread(self, managedThread : ManagedThread) -> None:
        self.__managedThreads.append(managedThread)
    

    def startManagedThreads(self) -> None: 
        for managedThread in self.__managedThreads: 
            if not managedThread.isThreadAlive() and managedThread.ident is None: 
                managedThread.start()
            

    def stopManagedThreads(self) -> None:
        for thread in self.__managedThreads: 
            thread.stopThread()   
        
        # Clear all threads
        self.__managedThreads.clear()

    
    def anyThreadsAlive(self) -> bool: 
        return any([x.isThreadAlive() for x in self.__managedThreads])

    
# Listen to Catch These Fists by Wet Leg     
