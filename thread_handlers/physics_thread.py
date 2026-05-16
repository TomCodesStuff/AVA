from .managed_thread import ManagedThread

class PhysicsThread(ManagedThread):
    def __init__(self):
        super().__init__() 
        self.__panicKillSwitch = False

    

    # retool physics handler 
    # thread runs until stop flag set 
    # implement pause flag(?) -> not needed, thread is either running or stopped
    #  

    def threadOnExecute(self) -> None: 
        while(not self.hasThreadStopped() and not self.__panicKillSwitch): 
            if not self.isThreadPaused(): 
                print("I would run the physics loop here :)")   
            else: print("Thread is paused...") 
