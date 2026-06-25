# TODO Will define some base methods here likely append, pop, min, max

from abc import ABC, abstractmethod
from typing import Generic, Iterable, TypeVar, List 


T = TypeVar("T")


class DataStructure(ABC, Generic[T]):

    @abstractmethod
    def get(self) -> List[T]: pass 

    @abstractmethod
    def size(self) -> int: pass 

    @abstractmethod
    def __str__(self) -> str: pass  

    @abstractmethod
    def __iter__(self) -> Iterable: pass


# Listen to Be Quiet and Drive (Far Away) by Deftones

