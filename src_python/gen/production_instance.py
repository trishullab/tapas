
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, TypeVar, Any, Generic, Union, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod

T = TypeVar('T')



# type instance
@dataclass
class instance(ABC):
    @abstractmethod
    def _match(self, handlers : InstanceHandlers[T]) -> T: pass


# constructors for type instance

@dataclass
class Grammar(instance):
    nonterminal : str
    sequence_id : str

    def _match(self, handlers : InstanceHandlers[T]) -> T:
        return handlers.case_Grammar(self)

def make_Grammar(nonterminal : str, sequence_id : str) -> instance:
    return Grammar(nonterminal, sequence_id)
        

@dataclass
class Vocab(instance):
    choices_id : str
    word : str

    def _match(self, handlers : InstanceHandlers[T]) -> T:
        return handlers.case_Vocab(self)

def make_Vocab(choices_id : str, word : str) -> instance:
    return Vocab(choices_id, word)
        

# case handlers for type instance
@dataclass
class InstanceHandlers(Generic[T]):
    case_Grammar : Callable[[Grammar], T]
    case_Vocab : Callable[[Vocab], T]


# matching for type instance
def match_instance(o : instance, handlers : InstanceHandlers[T]) -> T :
    return o._match(handlers)

    