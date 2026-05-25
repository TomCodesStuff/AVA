from __future__ import annotations
from typing import TYPE_CHECKING, Type, Tuple 
from src.data_structures import *
from src.screens import *
from src.enums import ScreenType

if TYPE_CHECKING:
    from src.app_window import Window
    Screen = Type[AlgorithmScreen]
    Controller = Type[AlgorithmController]
    Model = Type[AlgorithmModel]
    DataStruct = Type[DataStructure]

class ScreenCreator(): 
    @staticmethod
    def __createAlgorithmScreen(window : Window, mvcClasses :  Tuple[Screen, Controller, Model, DataStruct]) -> AlgorithmScreen: 
        screenClass, controllerClass, modelClass, dataStructureClass = mvcClasses
        screen = screenClass(window)
        model = modelClass()
        dataStructure = dataStructureClass()
        controller = controllerClass(screen, model, dataStructure)
        
        screen.setController(controller)
        screen.setModel(model)
        screen.setDataStructure(dataStructure)
        return screen 


    @classmethod
    def createScreen(cls, window : Window, screenType : ScreenType) -> ScreenInterface|None:
        match screenType:
            case ScreenType.MAIN_MENU: return MainMenu(window)  
            case ScreenType.SEARCH: 
                return cls.__createAlgorithmScreen(window, (
                    SearchScreen, 
                    SearchController, 
                    SearchModel, 
                    SearchArray))
            case ScreenType.SORT:
               return cls.__createAlgorithmScreen(window, (
                   SortScreen, 
                   SortController, 
                   SortModel, 
                   SortArray))
            case ScreenType.TRAVERSAL:
               return cls.__createAlgorithmScreen(window, (
                   TraversalScreen, 
                   TraversalController, 
                   TraversalModel, 
                   Graph))
            case _: return None


# Listen to Tonight, Tonight by The Smashing Pumpkins
