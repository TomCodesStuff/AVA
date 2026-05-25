from .managed_thread import ManagedThread
from ..graph_visualisation import PhysicsCalculations, CanvasGraph
import time 

class PhysicsThread(ManagedThread):
    def __init__(self, physicsCalculations : PhysicsCalculations):
        super().__init__() 
        self.__panicKillSwitch = False
        self.__physicsCalulcations = physicsCalculations

    
    # retool physics handler 
    # thread runs until stop flag set 
    # implement pause flag(?) -> not needed, thread is either running or stopped
    
    def threadOnExecute(self) -> None: 
        while(not self.hasThreadStopped() and not self.__panicKillSwitch): 
            if not self.isThreadPaused(): 
                self.__physicsCalulcations.applyPhysics()  
                # Time delay to hand over execution to GUI thread :/
                time.sleep(0.05)
            else: print("Thread is paused...")  
    

