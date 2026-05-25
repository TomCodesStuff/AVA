import threading
from src.algorithms import Algorithm
from .managed_thread import ManagedThread


THREAD_TIMEOUT = 1


class AlgorithmThread(ManagedThread):
    def __init__(self, algorithm : Algorithm):   
        super().__init__()     
        self.__delayLock = threading.Lock() 
        self.__algorithmSuccess = False 
        self.__algorithm = algorithm


    def acquireDelayLock(self) -> None: 
        self.__delayLock.acquire() 
    

    def releaseDelayLock(self) -> None: 
        self.__delayLock.release()


    def wasAlgorithmSuccessful(self) -> bool:
        return self.__algorithmSuccess 
    

    def stopAlgorithm(self) -> None: 
        if(self.__delayLock.locked()): self.releaseDelayLock()
        self.stopThread()


    def threadOnExecute(self): 
        self.__algorithmSuccess = False
        if self.__algorithm is None: return
        try:
            self.__algorithm.run()
            self.__algorithmSuccess = True 
        except Exception as e:
            print(f"ERROR: Algorithm broke at some point :(.\nException: {e}") 
            self.__algorithmSuccess = False


    def threadOnStart(self) -> None:  
        # Ensure various locks are released 
        # TODO Delete Not Needed 
        if(self.hasThreadStopped()): self.clearThreadStopFlag()  
        if(self.isThreadPaused()): self.releasePauseLock() 
        if(self.__delayLock.locked()): self.releaseDelayLock()
        print("Starting Thread :)")
        
        
    def threadOnEnd(self) -> None: 
        self.__algorithm = None

    
# Listen to Disarm by The Smashing Pumpkins
