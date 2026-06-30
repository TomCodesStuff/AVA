# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

import time 
from src.algorithms import Algorithm
from src.data_structures import Graph

class DijkstraTraverse(Algorithm[Graph]):
    # Constructor
    def __init__(self):
        super().__init__() 
    
    def getName(self) -> str: 
        return "Dijkstra" 

    def run(self) -> int:  
        print("Testing Dummy stub")
        time.sleep(10)
        return 0