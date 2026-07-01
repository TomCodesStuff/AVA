from __future__ import annotations
import tkinter as tk 
from abc import abstractmethod
from tkinter import ttk
from typing import TYPE_CHECKING, Generic, TypeVar
from src.data_structures import DataStructure
from src.screens import ScreenInterface
from src.enums import ScreenType, AlgorithmType


# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


if TYPE_CHECKING:
    from src.screens.algorithm_base import AlgorithmController, AlgorithmModel 

C = TypeVar("C", bound="AlgorithmController")
M = TypeVar("M", bound="AlgorithmModel")
D = TypeVar("D", bound="DataStructure")


FRAME_HEIGHT = 50
START_DELAY_MS = 500

# All screens that visualise the algorithms have the same fundamental layout
# This class delegates the reponsiblity of creating the basic layout
class AlgorithmScreen(Generic[C, M ,D], ScreenInterface):
    def __init__(self, window) -> None:
        super().__init__(window)
        
        # Font every widget uses 
        # TODO why are these in caps? 
        self.__FONT = "Arial"
        self.__FONTSIZE = 12 

        self.__selectDefaultText = "Select an algorithm."

        # References to controller, model and data model        
        self.__controller = None 
        self.__model = None
        self.__dataStructure = None

        # What data structures on drawn on
        self.__canvas = None

        # Array containing widgets that are disabled when an algorithm runs 
        # and then renabled when an algorithm ends 
        self.__toggleableWidgets = []

        self.__isAlgorithmRunning = False 
        self.__algorithmType = None   

        self.__animationRunning = False
        self.__frameDelay = 0

    
    # Abstract method, child screens will call before running an algorithm
    @abstractmethod
    def prepare(self) -> None: pass  

    @abstractmethod
    def complete(self) -> None: pass 

    @abstractmethod
    def render(self) -> None: pass 

    @abstractmethod 
    def animationSetup(self) -> None: pass 

    @abstractmethod 
    def coolAnimationFrame(self) -> None: pass  

    def __restore(self) -> None:
        self.__updateWidgets() 
        self.complete()

    def __animationStarting(self) -> None: 
        # Disable Buttons
        self.__runButton.config(state="disabled")
        self.__stateButton.config(state="disabled")
   
        self.animationSetup()
        self.__animationRunning = True

    def __animationEnded(self) -> None:
        self.__runButton.config(state="active")
        self.__stateButton.config(state="active")
        
    def endAnimation(self) -> None: 
        self.__animationRunning = False  
    
    def setFrameDelay(self, delay : int) -> None: 
        self.__frameDelay = max(0, delay)

    def coolEndingAnimation(self) -> None: 
        if(self.__animationRunning): 
            self.coolAnimationFrame()
            self.getController().refreshCanvas(refreshColours=False)
            self.getWindow().scheduleFunctionExecution(self.coolEndingAnimation, self.__frameDelay) 
        else: 
            self.getController().refreshCanvas(refreshColours=True)
            self.__animationEnded()
            self.__restore()

    def runCoolEndingAnimation(self) -> None:
        self.__animationStarting()  
        self.getWindow().scheduleFunctionExecution(self.coolEndingAnimation, START_DELAY_MS)
        
    def displayAlgorithmOptions(self) -> None:  
        if self.__algorithmType is None: return
        self.__algorithmOptions["values"] = self.getWindow().getAlgorithmNames(self.__algorithmType) 

    # Creates frame to display the border
    def __createBorderFrame(self, root : tk.Frame, frameWidth : int, frameHeight : int) -> tk.Frame:
        # Border frame gives appearence of a border between different frames
        borderFrame = tk.Frame(root, bg = "black", width = frameWidth, height = frameHeight)
        borderFrame.pack()
        borderFrame.grid_propagate(False)    
        return borderFrame     

    # Creates frame to display the options
    def __createOptionsFrame(self, root : tk.Frame, frameWidth : int, frameHeight : int) -> tk.Frame:
        # Frame to store the options users can interact with 
        # The size of the frame is calculated using the fixed size of the home frame
        optionsFrame = tk.Frame(root, width = frameWidth,\
            height = frameHeight, bg = "white")
        optionsFrame.grid(row = 0, column = 0) 
        optionsFrame.pack_propagate(False) 
        return optionsFrame

    # Creates frame to display the home button
    def __createHomeButtonFrame(self, root : tk.Frame, frameWidth : int, frameHeight : int) -> tk.Frame:
        # Frame to store button to redirect user back to Introduction Screen
        # This frame should always be fixed in height
        homeButtonFrame = tk.Frame(root, width = frameWidth, height = frameHeight, bg = "white")
        homeButtonFrame.grid(row = 1, column = 0, pady = (2,0))
        homeButtonFrame.pack_propagate(False)
        return homeButtonFrame 
    
    # Creates widget to store options, prevents formatting from breaking on different devices 
    def __createOptionWidget(self, root : tk.Frame, frameWidth : int, frameHeight : int) -> None:
        # This is the frame where the actual option widgets are stored
        # This is needed or otherwise the formatting breaks for different devices
        self.__optionsWidgetsFrame = tk.Frame(root, bg = "white", width = frameWidth,\
             height = frameHeight)
        self.__optionsWidgetsFrame.pack()
        self.__optionsWidgetsFrame.pack_propagate(False)
    
    # Creates the button to let the user navigate back to the main menu
    def __createHomeButton(self, root : tk.Frame) -> None: 
        # Creates and places button in the centre of the frame
        self.__homeButton = tk.Button(root, text = "Home.", font = (self.__FONT, self.__FONTSIZE), 
                                      width = 7, height = 1, borderwidth = 2, relief = "solid", 
                                      command = self.__loadHomeScreen)
        self.__homeButton.place(relx = 0.5, rely = 0.5, anchor = "center") 
    
    # Creates the frame to store the canvas
    def __createCanvasFrame(self, root : tk.Frame, frameWidth : int, frameHeight : int) -> tk.Frame:
        # This frame stores the canvas that displays array
        canvasFrame = tk.Frame(root, width = frameWidth, height = frameHeight, bg = "white")
        canvasFrame.grid(row = 0, column = 1, padx = (2,0)) 
        canvasFrame.pack_propagate(False)
        return canvasFrame
    
    # Creates canvas to display the array
    def __createCanvas(self, root : tk.Frame, canvasWidth : int, canvasHeight : int) -> None:
         # This canvas will be where the array is displayed.    
        self.__canvas = tk.Canvas(root, width = canvasWidth, height = canvasHeight, bg = "white") 
        self.__canvas.pack()
        self.__canvas.pack_propagate(False)
    
    # Creates frame to store the algorithm information
    def __createAlgorithmIntoFrame(self, root : tk.Frame, frameWidth : int, frameHeight : int) -> None:
        # This frame will be where information on the algorithm will be displayed 
        self.__algorithmInfoFrame = tk.Frame(root, width = frameWidth, height = frameHeight, bg = "white")
        self.__algorithmInfoFrame.grid(row = 1, column = 1, pady = (2,0), padx = (2,0)) 
        self.__algorithmInfoFrame.pack_propagate(False) 

    # Creates a combo box which displays all algorithms 
    def __createAlgorithmSelect(self) -> None:
        #combo box, allows the user to choose what algorithm they want
        self.__algorithmOptions = ttk.Combobox(self.getOptionsWidgetFrame(), textvariable = tk.StringVar(), 
                                               state = "readonly", font = (self.getFont(), self.getFontSize()), 
                                               width = self.getOptionsWidgetFrame().winfo_width())
        self.__algorithmOptions.set(self.__selectDefaultText)
        # Removes the blue highlighting when something is selected that annoyed me
        self.__algorithmOptions.bind("<<ComboboxSelected>>", lambda _: self.getOptionsWidgetFrame().focus())
        self.__algorithmOptions.pack(pady = (10,0))  
        self.addToggleableWidget(self.__algorithmOptions)

    # When the slider has changed value a label is added with the relevant speed 
    def __updateDelay(self, value : str) -> None: 
        self.__speedSlider.config(label = f"Delay: {value} {self.__sliderUnitsText}")  

    # Sets the delay that pauses algorithms during execution     
    def __setDelay(self) -> None:   
        self.getController().updateAlgorithmDelay(float(self.__speedSlider.get()))

    # Creates a slider that allows users to adjust an algorithms speed
    def __createSpeedSlider(self) -> None:
        # Creates a slider that goes from the maximum delay to the minmum delay 
        # Every time the sliders value is changed the updateDelay() method is called to update the value seen on screen
        self.__speedSlider = tk.Scale(self.getOptionsWidgetFrame(), from_ = self.__model.getMaxDelay(), 
                                      to_ = self.__model.getMinDelay(), resolution=self.__model.getResolution(), 
                                      length = self.getOptionsWidgetFrame().winfo_width(), orient = "horizontal", 
                                      showvalue = False, bg =  "white", highlightbackground = "white", 
                                      command = self.__updateDelay)
        self.__speedSlider.pack(pady = (10, 0))  
        self.__speedSlider.set(self.__model.getMaxDelay())
        # When the user stops moving the slider the slider is updated in the dataStructure class 
        self.__speedSlider.bind("<ButtonRelease-1>", lambda _ : self.__setDelay()) 
        # Time units of the delay 

        if self.getModel().isDelayMilliSeconds():
            self.__sliderUnitsText = "Milliseconds"
        else: self.__sliderUnitsText = "Seconds"  

    # Creates buttons that lets user execute algorithms or stop them
    def __createRunButton(self) -> None:
        # Frame to store stop and solve buttons in a grid layout
        algorithmToggleFrame = tk.Frame(self.getOptionsWidgetFrame(), bg = "white")
        algorithmToggleFrame.pack(side = "bottom", pady = (0,5))
        # Allows user to see the algorithm in action
        self.__runButton = tk.Button(algorithmToggleFrame, text = "Solve.", width = 7, relief = "solid", 
                                           font = (self.getFont(), self.getFontSize()), 
                                           command = lambda: self.__runAlgorithm())
        self.__runButton.grid(row = 0, column = 0, padx = (0,5)) 
        # Allows user to stop algorithm whilst it's running - button is initially disabled
        self.__stateButton = tk.Button(algorithmToggleFrame, text = "Pause.", width = 7, relief = "solid", 
                                             font = (self.getFont(), self.getFontSize()), 
                                             state = "disabled", command = lambda : self.__pauseAlgorithm())
        self.__stateButton.grid(row = 0, column = 1)  

    # Creates widgets that all algorithm screens use 
    def __createBaseAlgorithmOptions(self) -> None: 
        self.__createAlgorithmSelect()               
        self.__createSpeedSlider()
        self.__createRunButton()

    # Creates the layout all algorithms screens use
    def createBaseLayout(self) -> None:
        # Override default behaviour when exiting GUI -> cleans up running threads
        self.getWindow().setCustomExitFunc(self.__exitCleanUp)
        # Get content Frame to store all widgets
        contentFrame = self.getWindow().getContentFrame()
        # Get content frames width and height
        contentFrameHeight = self.getWindow().getContentFrameHeight()
        contentFrameWidth = self.getWindow().getContentFrameWidth()
        # width of the border
        borderSize = 2
        # Distance between the widgets and the edge of the frame
        padding = 10
        # Height of frame that contains home button       
        homeButtonFrameHeight = 50
        # Width of the home button frame and the options frame
        optionsHomeWidth = 200
        # Width of canvas frame
        canvasFrameWidth = algorithmInfoFrameWidth = contentFrameWidth - optionsHomeWidth - borderSize 
        # Height of canvas frame
        canvasFrameHeight = contentFrameHeight - homeButtonFrameHeight - borderSize

        # Border frame gives appearence of a border between different frames
        borderFrame = self.__createBorderFrame(contentFrame, contentFrameWidth, contentFrameHeight)
        # Frame to store the options users can interact with 
        # The size of the frame is calculated using the fixed size of the home frame
        optionsFrame = self.__createOptionsFrame(borderFrame, optionsHomeWidth, 
                                                 contentFrameHeight - homeButtonFrameHeight - borderSize)
        # Frame to store button to redirect user back to Introduction Screen
        # This frame should always be fixed in height
        homeButtonFrame = self.__createHomeButtonFrame(borderFrame, optionsHomeWidth, homeButtonFrameHeight)
        # Updates sizes of frames
        self.getWindow().update()

        # This is the frame where the actual option widgets are stored
        self.__createOptionWidget(optionsFrame, optionsHomeWidth - padding, optionsFrame.winfo_height())
        # Creates a home button so user can navigate back to the intro screen
        self.__createHomeButton(homeButtonFrame)
        # This frame stores the canvas that displays array
        canvasFrame = self.__createCanvasFrame(borderFrame, canvasFrameWidth, canvasFrameHeight)
        # Updates widths
        self.getWindow().update()  
        # Creates canvas to display the array 
        self.__createCanvas(canvasFrame, canvasFrame.winfo_width(), canvasFrame.winfo_height())
        # This frame will be where information on the algorithm will be displayed 
        self.__createAlgorithmIntoFrame(borderFrame, algorithmInfoFrameWidth, FRAME_HEIGHT) 
        # Create options common across all algorithms
        self.__createBaseAlgorithmOptions()
        # Updates widths
        self.getWindow().update()  

    def __updateStateButton(self, isPaused=False) -> None:
        if isPaused:  
            self.__stateButton.config(text="Resume.", command=self.__resumeAlgorithm) 
        else:
            self.__stateButton.config(text="Pause.", command=self.__pauseAlgorithm)  

    def __updateRunButton(self) -> None: 
        if self.__isAlgorithmRunning: 
            self.__runButton.config(text="Stop.", command=lambda: self.algorithmComplete(playAnimation=False))
        else: 
            self.__runButton.config(text="Solve.", command=self.__runAlgorithm)  

    def __updateToggleWidgets(self) -> None:
        for widget in self.__toggleableWidgets:  
            if self.__isAlgorithmRunning:
                widget.config(state="disabled")   
            else: widget.config(state="active")
    
    def __toggleStateButton(self) -> None: 
        if self.__isAlgorithmRunning:
            self.__stateButton.config(state="active")
        else: self.__stateButton.config(state="disabled")

    def __updateWidgets(self) -> None: 
        self.__updateToggleWidgets()
        self.__updateRunButton() 
        self.__updateStateButton() 
        self.__toggleStateButton()

    # Returns algorithm the user has selected 
    def __getAlgorithmChoice(self) -> str:
        return self.__algorithmOptions.get()  
    
    # Releases the lock, letting the algorithm thread run again
    def __resumeAlgorithm(self) -> None: 
        self.__controller.resumeAlgorithm()
        self.__updateStateButton()

    # Holds the lock, pausing the algorithm Thread
    def __pauseAlgorithm(self) -> None: 
        self.__controller.pauseAlgorithm()
        self.__updateStateButton(isPaused=True) 

    # Call algorithm user has selected
    def __runAlgorithm(self) -> None:   
        # Doesn't do anything if user hasn't chosen an algorithm
        if(self.__getAlgorithmChoice() == self.__selectDefaultText): 
            self.__algorithmOptions.config(foreground = "red")
        else:
            self.__isAlgorithmRunning = True
            self.__algorithmOptions.config(foreground = "black")
            self.__updateWidgets()
            self.prepare()            
            self.__controller.startAlgorithmThread(self.__algorithmType, self.__getAlgorithmChoice())

    def algorithmComplete(self, playAnimation : bool) -> None:  
        self.__stopAlgorithm()
        if playAnimation: 
            self.getWindow().scheduleFunctionExecution(self.runCoolEndingAnimation, START_DELAY_MS) 
        else: self.__restore()
            
    # Forces current running algorithm thread to terminate (safely, I hope)
    def __stopAlgorithm(self) -> None:
        self.__controller.stopAlgorithmThread() 
        self.__isAlgorithmRunning = False  
        # self.__updateWidgets()

    # Loads the home screen 
    # Ensures any algorithm threads are terminated 
    def __loadHomeScreen(self) -> None: 
        # If a thread exists and it is still running
        if(self.__controller.isAlgorithmRunning()): 
            # Tell the thread to stop
            self.__stopAlgorithm()   
        
        if self.__controller.anyThreadsAlive(): 
            self.__controller.stopManagedThreads()

        # Cancel any scheduled function (mostly for traversal screen)
        self.getWindow().cancelScheduledFunctions()
        self.getWindow().loadScreen(ScreenType.MAIN_MENU)

    # Halt running threads when user exits application 
    def __exitCleanUp(self) -> None:
        self.getController().stopAlgorithmThread()
        self.getController().stopManagedThreads()

    # Setters
    def setController(self, controller : C) -> None: self.__controller = controller
    
    def setModel(self, model : M) -> None: self.__model = model 
    
    def setDataStructure(self, dataStructure : D) -> None: self.__dataStructure = dataStructure  
    
    def addToggleableWidget(self, widget : tk.Widget) -> None: self.__toggleableWidgets.append(widget)
    
    def removeToggleableWidget(self, widget : tk.Widget) -> None:  
        if widget in self.__toggleableWidgets: 
            self.__toggleableWidgets.remove(widget) 
    
    def setAlgorithmType(self, algorithmType : AlgorithmType) -> None:
        self.__algorithmType = algorithmType

    # Getters 
    def getController(self) -> C: return self.__controller
    
    def getModel(self) -> M: return self.__model
    
    def getDataStructure(self) -> D: return self.__dataStructure 
    
    def getFont(self) -> str: return self.__FONT 
    
    def getFontSize(self) -> int: return self.__FONTSIZE
    
    def getOptionsWidgetFrame(self) -> tk.Frame: return self.__optionsWidgetsFrame 
    
    def getCanvas(self) -> tk.Canvas: return self.__canvas  
    
    def getAlgorithmType(self) -> AlgorithmType: return self.__algorithmType

# Listen to Under You by Foo Fighters
