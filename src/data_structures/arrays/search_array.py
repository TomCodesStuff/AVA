# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from .array import Array


class SearchArray(Array): 
    def __init__(self):
        super().__init__()
        self.__target = 0 


    # Sets the element being looked for to the passed value
    def setTarget(self, value : int) -> None:
        self.__target = value   


    # Returns the target (the element being looked for)
    def getTarget(self) -> int: return self.__target


# Listen to Dakota by Stereophonics
 