# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

import tkinter as tk 
from typing import TYPE_CHECKING, TypeVar
from src.data_structures import Graph
from src.graph_visualisation import CanvasEdge
from src.enums import EdgeDirectionOption
from ..algorithm_base import AlgorithmScreen

if TYPE_CHECKING: 
    from src.screens.graph_traverse import TraversalController, TraversalModel

C = TypeVar("C", bound="TraversalController")
M = TypeVar("M", bound="TraversalModel")
D = TypeVar("D", bound="Graph")


# TODO Make sure to hide graph options when algorithm is run 

INITIAL_WEIGHT = 0


class TraversalScreen(AlgorithmScreen[C, M, D]):  
    def __init__(self, window):
        super().__init__(window)

        self.__graphOptionsFrame = None 
        self.__nodeOptionsFrame = None 
        self.__edgeOptionsFrame = None 
        self.__innerNodeFrame = None 

    # Creates the button that lets users add nodes to the canvas 
    def __createAddNodeButton(self) -> None: 
        self.__addNodeButton = tk.Button(self.__innerNodeFrame, text="Spawn.", width=6, relief="solid", 
                                         font = (self.getFont(), self.getFontSize()), command=self.getController().spawnNode)
        self.__addNodeButton.grid(row = 1, column = 0, pady = (5, 0), padx=(0, 10))  
    
    def __createDeleteNodeButton(self) -> None:
        self.__deleteNodeButton = tk.Button(self.__innerNodeFrame, text="Delete.", width=6, relief="solid", 
                                            font = (self.getFont(), self.getFontSize()), 
                                            command=self.getController().deleteNode)
        self.__deleteNodeButton.grid(row = 1, column = 1, pady = (5, 0), padx=(10, 0))  

    def __createNodeOptions(self) -> None:
        # Hacky solution to make sure everything stays in centre :/
        self.__innerNodeFrame = tk.Frame(self.__nodeOptionsFrame, bg="white") 
        self.__innerNodeFrame.pack()

        tk.Label(self.__innerNodeFrame, text="Node Options:", font=(self.getFont(), self.getFontSize(), "bold", "underline"), bg="white")\
            .grid(row=0, column=0, pady=(10, 0), columnspan=2)

        self.__createAddNodeButton() 
        self.__createDeleteNodeButton()

    # Changes the text colour of the add node button to the passed colour
    def setAddNodeButtonColour(self, colour : str) -> None: 
        self.__addNodeButton.config(fg = colour) 
    
    # Changes the text colour of the delete node button to the passed colour
    def setDeleteNodeButtonColour(self, colour: str) -> None:
        self.__deleteNodeButton.config(fg = colour)

    # Updates text in label above weight slider 
    def __updateWeight(self, value : str|int) -> None:
        value = int(value)
        self.__weightSlider.config(label = f"Weight: {value}")   
        if value > INITIAL_WEIGHT: self.getController().updateEdgeWeight(value)

    # Create option to let users change an edges weight/cost
    def __createWeightSlider(self) -> None:
        # Frame to store entry widget to let users to choose an edges weight
        self.__edgeWeightFrame = tk.Frame(self.__edgeOptionsFrame, background="white") 
        self.__edgeWeightFrame.pack(pady=(5, 0))
        self.__weightSlider = tk.Scale(self.__edgeWeightFrame, from_ = self.getModel().getMinEdgeWeight(), 
                                       to_=self.getModel().getMaxEdgeWeight(), resolution=self.getModel().getWeightSliderResolution(), 
                                       length = self.getOptionsWidgetFrame().winfo_width(), orient="horizontal", showvalue=False, 
                                       bg = "white", highlightbackground="white", command=self.__updateWeight)
        
        self.__updateWeight(INITIAL_WEIGHT)
        self.__weightSlider.pack()

    # Create option to decide if edge is directed/undirected
    def __createEdgeDirectionButtons(self) -> None:
        self.__directionButtonFrame = tk.Frame(self.__edgeOptionsFrame, background="white")
        self.__directionButtonFrame.pack()

        self.__leftArrowButton = tk.Button(self.__directionButtonFrame, text = "<-", width=3, relief = "solid", 
                                           font=(self.getModel().getArrowFont(), self.getFontSize()), 
                                           command=lambda: self.getController().changeEdgeDirection(EdgeDirectionOption.RIGHT_TO_LEFT)) 
        self.__leftArrowButton.grid(row=0, column=0, pady=(10, 0), padx=(0, 10)) 

        self.__doubleArrowButton = tk.Button(self.__directionButtonFrame, text = "<->", width=3, relief = "solid", 
                                             font=(self.getModel().getArrowFont(), self.getFontSize()), 
                                             command=lambda: self.getController().changeEdgeDirection(EdgeDirectionOption.BIDIRECTIONAL)) 
        self.__doubleArrowButton.grid(row=0, column=1, pady=(10, 0)) 

        self.__rightArrowButton = tk.Button(self.__directionButtonFrame, text = "->", width=3, relief = "solid", 
                                            font=(self.getModel().getArrowFont(), self.getFontSize()), 
                                            command=lambda: self.getController().changeEdgeDirection(EdgeDirectionOption.LEFT_TO_RIGHT)) 
        self.__rightArrowButton.grid(row=0, column=2, pady=(10, 0), padx=(10, 0))       
       
    # Create button to save edge 
    def __createFinishButton(self) -> None:
        self.__saveEdgeButton = tk.Button(self.__edgeConfirmationFrame, text = "Finish.", width=6, relief = "solid", 
                                          font=(self.getFont(), self.getFontSize()), command=self.__finishEdgeEdit)
        self.__saveEdgeButton.grid(row=0, column=0, padx=(0, 10)) 

    # Create button to delete edge 
    def __createDeleteEdgeButton(self) -> None:
        self.__deleteEdgeButton = tk.Button(self.__edgeConfirmationFrame, text="Delete.", width=6, relief="solid",
                                            font=(self.getFont(), self.getFontSize()), command=self.__deleteEdge)
        self.__deleteEdgeButton.grid(row=0, column=1, padx=(10, 0))

    # Create buttons to save or delete an edge    
    def __createEdgeConfirmationButtons(self): 
        self.__edgeConfirmationFrame = tk.Frame(self.__edgeOptionsFrame, background="white")
        self.__edgeConfirmationFrame.pack(pady=(10, 0)) 
        self.__createFinishButton()
        self.__createDeleteEdgeButton()

    def __finishEdgeEdit(self) -> None:    
        # This is just calling the event handler function to finish editing the edge  
        self.getController().finishEdgeEdit() 
        # Hides edge edit options from view
        self.__nodeOptionsFrame.tkraise()

    def __deleteEdge(self) -> None:  
        # Deletes newly drawn weight or pre-existing weight 
        # TODO RE-implement this btw 
        self.getController().deleteEdge()
        self.__finishEdgeEdit()
    
    # Resets position and disables weight slider 
    def resetWeightSlider(self) -> None: 
        # Resets text
        self.__updateWeight("No Edge Selected") 
        # Disables slider 
        self.__weightSlider.config(state="disabled")
    
    # Enables egde options so users can toggle them
    def showEdgeOptions(self, canvasEdge : CanvasEdge) -> None: 
        # Update weight slider 
        self.__updateWeight(canvasEdge.getWeight())          
        # Moves thumb of slider to correct value -> scale must be active first 
        self.__weightSlider.set(canvasEdge.getWeight())
        # Show edge options 
        self.__edgeOptionsFrame.tkraise() 

     # Creates options to add edges or edit existing ones
    def __createEdgeOptions(self) -> None: 
        # Label 
        tk.Label(self.__edgeOptionsFrame, text="Edge Options:", font=(self.getFont(), self.getFontSize(), "bold", "underline"), bg="white")\
            .pack(pady=(10, 0))
        # Calls slider to adjust weight
        self.__createWeightSlider() 
        # Create buttons to toggle direction
        self.__createEdgeDirectionButtons() 
        # Create buttons to confirm changes 
        self.__createEdgeConfirmationButtons()

    # Creates the widgets that allows users to toggle the visualisers settings
    def __createOptions(self) -> None:  
        self.__graphOptionsFrame = tk.Frame(self.getOptionsWidgetFrame(), bg = "white")
        self.__graphOptionsFrame.pack(fill="both", expand=True) 

        self.__nodeOptionsFrame = tk.Frame(self.__graphOptionsFrame, bg = "white")
        self.__nodeOptionsFrame.place(relwidth=1, relheight=1)
        
        self.__edgeOptionsFrame = tk.Frame(self.__graphOptionsFrame, bg = "white")
        self.__edgeOptionsFrame.place(relwidth=1, relheight=1)

        self.__createNodeOptions()
        self.__createEdgeOptions()    

        # Show node options as a default
        self.__nodeOptionsFrame.tkraise()

    def render(self) -> None: 
        self.createBaseLayout()
        self.__createOptions()  
        self.getController().init()
    
    # TODO need to create graph 
    def prepare() -> None: pass 
    def animationSetup(self) -> None: pass 
    def coolAnimationFrame(self) -> None: pass  

 


# Listen Glass Spiders by Hot Milk
