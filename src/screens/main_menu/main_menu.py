# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

import tkinter as tk 
from src.screens import ScreenInterface
from src.enums import ScreenType


# Ideally this should be the first screen the user sees 
class MainMenu(ScreenInterface):
    def __init__(self, window):
        super().__init__(window)
        # Stores reference to Window object
        self.__FONT = "Arial"


    # Creates the screen
    def render(self) -> None:
        # Get content Frame to store all widgets
        self.__contentFrame = self.getWindow().getContentFrame()
        self.__createTitle()
        self.__createIntroParagraph()
        self.__createNavigationButtons()


    # Creates the title displaying the projects name
    def __createTitle(self) -> None:
        # Header label
        tk.Label(self.__contentFrame, text = "Welcome to AVA.", 
                 font = (self.__FONT, 18, "underline"), bg = "white")\
            .pack(pady = 10) 


    # Create introduction paragraph
    def __createIntroParagraph(self) -> None:
        # The introductory text is kept as a string 
        # as it makes it easier to change (and makes code easier to read)
        introText = "AVA (Algorithms Visualised Amazingly) makes algorithms fun!\n" +\
            "Press a button to start visualising."
        # Label that contains the introduction text
        tk.Label(self.__contentFrame, text = introText, font = (self.__FONT, 14), justify = "center", bg = "white")\
            .pack(pady = 5) 
    

    # Creates buttons that allow users to navigate the rest of the project
    def __createNavigationButtons(self) -> None:
        # Adds a frame for the buttons widgets 
        # Adding this frame makes positioning the buttons much easier
        buttonsFrame = tk.Frame(self.__contentFrame, bg = "white")
        buttonsFrame.pack()
        # Navigate to path finding algorithms screen
        tk.Button(buttonsFrame, text = "Path Finding", font = (self.__FONT, 12), height = 2, width = 15, relief = "solid",\
                  command = lambda: self.getWindow().loadScreen(ScreenType.TRAVERSAL)).pack(pady=15)  
        # Navigate to array searching screen
        tk.Button(buttonsFrame, text = "Array Searching",  font = (self.__FONT, 12), height = 2, width = 15, relief = "solid",\
                  command=lambda: self.getWindow().loadScreen(ScreenType.SEARCH)).pack(side = "left", pady = 15, padx = (100, 0)) 
       
        # Navigate to array sorting screen
        tk.Button(buttonsFrame, text = "Array Sorting",  font = (self.__FONT, 12), height = 2, width = 15, relief = "solid",\
                  command=lambda: self.getWindow().loadScreen(ScreenType.SORT)).pack(side = "left", padx = 100)  
        
        
        tk.Label(self.__contentFrame, text = "Created by Thomas Gibson", bg = "white", justify = "left")\
            .pack(side = "bottom", anchor = "w", pady = 5, padx = 5) 
        
        
# Listen to 99' Benz by A Story Told
