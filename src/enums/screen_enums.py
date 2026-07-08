from enum import Enum

class ScreenType(Enum):
    MAIN_MENU = "main_menu"
    SEARCH = "search"
    SORT = "sort"
    TRAVERSAL = "traversal"


class AlgorithmType(Enum): 
    SEARCHING = "searching"
    SORTING = "sorting"
    TRAVERSAL = "traversal"


class SortDirection(Enum):
    ASCENDING = 0
    DESCENDING = 1 


class EdgeDirection(Enum):  
    BIDIRECTIONAL = 0 
    FIRST_TO_SECOND = 1
    SECOND_TO_FIRST = 2 


class EdgeDirectionOption(Enum): 
    BIDIRECTIONAL = 0
    RIGHT_TO_LEFT = 1 
    LEFT_TO_RIGHT = 2


# Listen to Cherry Waves by Deftones
