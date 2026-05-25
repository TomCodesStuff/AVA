import tkinter as tk
from typing import Callable, Tuple, Type 
from src.algorithm_validator import AlgorithmValidator
from src.algorithms import Algorithm
from src.screen_creator import ScreenCreator
from src.enums import ScreenType, AlgorithmType

# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


# Window Class - Creates a blank tkinter window
class Window():
    def __init__(self, width : int, height : int) -> None:
        self.__algorithmValidator = AlgorithmValidator()
        self.__algorithmValidator.findValidAlgorithms()
        
        # Variables to store minimum width and height - means they can be easily changed
        minWidth = 750 
        minHeight = 500
        # This prevents screens being made smaller than 750x500
        if(width < minWidth or height < minHeight):
            self.__width = minWidth
            self.__height = minHeight
        else:
            self.__width = width
            self.__height = height  
    
    def create(self) -> None:
        # Dimensions for the frame all widgets stored in
        # Stored as attributes so they can be accessed by other objects later
        self.__contentFrameWidth = self.__width - 20
        self.__contentFrameHeight = self.__height - 20
        
        # Declaring window
        self.__window = tk.Tk()
        self.__window.title('Useful Algorithms')

        # windows dimensions
        self.__window.geometry(f'{self.__width}x{self.__height}')
        self.__window.resizable(False, False) 

        #changed window colour to grey 
        # gives window solid black border
        self.__window.config(bg = "#CCCCCC", borderwidth = 2, relief = "solid")
        
        # Size of border
        borderSize = 2

        # This gives the appearance that the content frame has a border
        # There are built in hyperparamters for adding a border but this caused issues with widgets being centred
        tk.Frame(self.__window, bg = "black", width = self.__contentFrameWidth + (borderSize * 2),\
            height = self.__contentFrameHeight + (borderSize * 2)).place(relx = 0.5, rely = 0.5, anchor = "center")

        # Declaring and customising the frame
        # This is where all the displayed content 
        self.__contentFrame = tk.Frame(self.__window, height = self.__contentFrameHeight, width = self.__contentFrameWidth, bg = "white")
        
        # Makes the frame centred in the GUI window
        self.__contentFrame.place(relx = 0.5, rely = 0.5, anchor = "center")

        # Stops frame resizing to same size as widgets inside it 
        self.__contentFrame.pack_propagate(False) 

    # Draws window
    def show(self) -> None:
        self.__window.mainloop() 

    # Removes every widget from the passed frame
    def removeScreen(self) -> None: 
        for widget in self.__contentFrame.winfo_children():
            widget.destroy()

    # Clears current screen and loads new one
    def loadScreen(self, screenType : ScreenType) -> None:  
        # Clear previous screen
        self.removeScreen() 
        newScreen = ScreenCreator.createScreen(self, screenType)
        if newScreen is not None: newScreen.render()

    # Refreshes the screen, so any changes can be displayed
    def update(self) -> None:
        self.__window.update() 
    
    def update_idle_tasks(self) -> None:
        self.__window.update_idletasks()
    
    # Schedule the passed function to be executed after the passed amount of time
    # Assumes function has no parameters
    def scheduleFunctionExecution(self, function : Callable, delay : int) -> None:
        self.__window.after(delay, function)
    
    def getNumScheduledFunctions(self) -> int:
        return len(self.__window.tk.call('after', 'info'))

    def cancelScheduledFunctions(self) -> None:
        for functionID in self.__window.tk.call('after', 'info'): 
            self.__window.after_cancel(functionID)

    # Returns the frame widgets are displayed in
    def getContentFrame(self) -> tk.Frame:
        return self.__contentFrame

    # Returns the content frames height
    def getContentFrameHeight(self) -> int:
        return self.__contentFrameHeight 

    # Returns the content frames width
    def getContentFrameWidth(self) -> int:
        return self.__contentFrameWidth 
    
    def getAlgorithmNames(self, algorithmType : AlgorithmType) -> Tuple:
        return self.__algorithmValidator.getAlgorithmNames(algorithmType)

    def getAlgorithmClass(self, algorithmType : AlgorithmType, algorithmName : str) -> Type[Algorithm]: 
        return self.__algorithmValidator.getAlgorithmClass(algorithmType, algorithmName)


# Listen to Killing In The Name by Rage Against The Machine
