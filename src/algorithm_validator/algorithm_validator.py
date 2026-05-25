# # If this isn't at the top the program breaks :/
# # If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

import inspect
import importlib
import re
from pathlib import Path
from types import ModuleType
from typing import List, Tuple
from src.algorithms import Algorithm
from src.enums import AlgorithmType


FILE_NAME_REGEX = r"^([a-z]+_)+(search|sort|traverse)\.py$"


class AlgorithmValidator(): 
    def __init__(self): 
        self.__algorithmsByType = {
            x.value : {} for x in AlgorithmType 
        }

    def __isFileNameValid(self, x : Path) -> None: 
        return True if re.match(FILE_NAME_REGEX, x.name) else False

    def __getPotentialAlgorithms(self, algorithmType : str) -> List[str]: 
        srcDir = Path(__file__).parent.parent.resolve()
        algorithmsDir = srcDir / "algorithms" / algorithmType 
        if not algorithmsDir.exists(): return []
        return [x.stem for x in algorithmsDir.iterdir() if self.__isFileNameValid(x)]

    def __importModule(self, algorithmType : str, algorithmName : str) -> ModuleType|None:
        try:
            algorithmModule = importlib.import_module(f"src.algorithms.{algorithmType}.{algorithmName}") 
            return algorithmModule
        except Exception as e:
            print(f"FAILED: Unable to import module: algorithms.{algorithmType}.{algorithmName}.\nException: {e}")
            return None

    def __getAlgorithmClassName(self, algorithmModule : ModuleType, algorithmName : str) -> str|None:
        moduleClasses = [name for name, _ in inspect.getmembers(algorithmModule)] 
        algorithmClassName = "".join(map(str.capitalize, algorithmName.split("_")))
        if algorithmClassName not in moduleClasses: 
            print("FAILED: Algorithm class not name not in correct format.")
            return None 
        return algorithmClassName   

    def __getAlgorithmClass(self, algorithmModule : ModuleType, algorithmClassName : str) -> Algorithm|None:
        try:
            algorithmClass = getattr(algorithmModule, algorithmClassName) 
            return algorithmClass
        except Exception as e: 
            print(f"FAILED: Unable to create instance of {algorithmClassName}.\nException: {e}")
            return None

    def __isAlgorithmSubclass(self, algorithmClassName : str, obj : object) -> bool: 
        if(not issubclass(obj, Algorithm)):
            print(f"FAILED: {algorithmClassName} is not a child of `Algorithm` class.") 
            return False 
        return True 
        
    def __isGetNameCorrect(self, algorithm : Algorithm) -> bool:  
        algorithmName = algorithm.getName() 
        if(not isinstance(algorithmName, str)): 
            print("FAILED: `getName()` method returns an invalid data type.")
            return False  
        if(algorithmName == ""): 
            print("FAILED: `getName()` method returns an invalid value.")
            return False
        return True 

    def __validateAlgorithm(self, algorithmType, algorithmName : str) -> Algorithm|None:
        algorithmModule = self.__importModule(algorithmType, algorithmName) 
        if algorithmModule is None: return None 
        
        algorithmClassName = self.__getAlgorithmClassName(algorithmModule, algorithmName)
        if algorithmClassName is None: return None 

        algorithmClass = self.__getAlgorithmClass(algorithmModule, algorithmClassName)
        if algorithmClass is None: return None 
        
        if not self.__isAlgorithmSubclass(algorithmClassName, algorithmClass): return None  

        try:
            algorithmInstance = algorithmClass()  
        except Exception as e: 
            print(f"FAILED: Could not create instance of {algorithmClassName}.\nException {e}")
            return None

        if not self.__isGetNameCorrect(algorithmInstance): return None
        return algorithmClass

    def __addValidAlgorithm(self, algorithmType : str, algorithmClass : type[Algorithm]) -> None: 
        algorithmInstance = algorithmClass()
        self.__algorithmsByType[algorithmType][algorithmInstance.getName()] = algorithmClass

    def findValidAlgorithms(self) -> None:
        for algorithmType in self.__algorithmsByType.keys():
            candidateAlgorithms = self.__getPotentialAlgorithms(algorithmType)
            for algorithm in candidateAlgorithms: 
                algorithmClass = self.__validateAlgorithm(algorithmType, algorithm)
                if algorithmClass is not None: self.__addValidAlgorithm(algorithmType, algorithmClass) 

    def getAlgorithmNames(self, algorithmType : AlgorithmType) -> Tuple:
        if algorithmType.value not in self.__algorithmsByType: return ()
        return tuple(self.__algorithmsByType[algorithmType.value].keys()) 

    def getAlgorithmClass(self, algorithmType : AlgorithmType, algorithmName : str) -> Algorithm:  
        if algorithmType.value not in self.__algorithmsByType: return None 
        if algorithmName not in self.__algorithmsByType[algorithmType.value]: return None 
        return self.__algorithmsByType[algorithmType.value][algorithmName]


# Listen to Last Nite By The Strokes
