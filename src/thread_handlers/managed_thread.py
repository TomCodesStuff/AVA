import threading
from abc import ABC, abstractmethod


THREAD_TIMEOUT = 1


class ManagedThread(ABC, threading.Thread):
    def __init__(self):
        super().__init__() 

        self.__threadStarted = threading.Event()
        self.__threadStopped = threading.Event()
        self.__threadPauseLock = threading.Lock()
    
    def setThreadStopFlag(self) -> None:
        self.__threadStopped.set() 
    
    def clearThreadStopFlag(self) -> None:
        self.__threadStopped.clear()  
    
    def hasThreadStopped(self) -> bool: 
        return self.__threadStopped.is_set() 

    def stopThread(self) -> None:
        if self.isThreadPaused(): self.releasePauseLock() 
        self.setThreadStopFlag()  
        
        if self.isThreadAlive(): self.join(timeout=THREAD_TIMEOUT)
        if self.isThreadAlive(): print("ERROR: Thread did not terminate in time.")        
        else: print("Thread Terminated :)")  
    
    def acquirePauseLock(self) -> None: 
        self.__threadPauseLock.acquire()
    
    def releasePauseLock(self) -> None: 
        self.__threadPauseLock.release()  
    
    def isThreadPaused(self) -> bool: return self.__threadPauseLock.locked() 
    
    def isThreadAlive(self) -> bool: return self.is_alive()
    
    @abstractmethod 
    def threadOnExecute(self) -> None: pass 
    
    def threadOnStart(self) -> None: pass 
    
    def threadOnEnd(self) -> None: pass 

    def run(self) -> None:
        self.__threadStarted.set() 
        self.__threadStarted.wait(timeout=THREAD_TIMEOUT)
        self.threadOnStart() 
        self.threadOnExecute() 
        self.threadOnEnd()

# Listen to No Distance Left To Run by Blur