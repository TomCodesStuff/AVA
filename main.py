from src.app_window import Window
from src.enums import ScreenType

WIDTH = 750
HEIGHT = 500

if(__name__ == "__main__"):
    window = Window(WIDTH, HEIGHT) 
    window.create()
    window.loadScreen(ScreenType.MAIN_MENU)
    window.show() 
else:
    print("This file has no functions to import :(")
    
# Listen to Walk  by Foo Fighters  
# Seriously listen to it, it means a lot to me   
