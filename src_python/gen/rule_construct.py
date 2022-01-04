
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, TypeVar, Any, Generic, Union, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod

T = TypeVar('T')


from gen.line_format_construct import line_format


# type item
@dataclass
class item(ABC):
    @abstractmethod
    def _match(self, handlers : ItemHandlers[T]) -> T: pass


# constructors for type item

@dataclass
class Terminal(item):
    terminal : str

    def _match(self, handlers : ItemHandlers[T]) -> T:
        return handlers.case_Terminal(self)

def make_Terminal(terminal : str) -> item:
    return Terminal(terminal)
        

@dataclass
class Nonterm(item):
    relation : str
    nonterminal : str
    format : line_format

    def _match(self, handlers : ItemHandlers[T]) -> T:
        return handlers.case_Nonterm(self)

def make_Nonterm(relation : str, nonterminal : str, format : line_format) -> item:
    return Nonterm(relation, nonterminal, format)
        

@dataclass
class Vocab(item):
    relation : str
    vocab : str

    def _match(self, handlers : ItemHandlers[T]) -> T:
        return handlers.case_Vocab(self)

def make_Vocab(relation : str, vocab : str) -> item:
    return Vocab(relation, vocab)
        

# case handlers for type item
@dataclass
class ItemHandlers(Generic[T]):
    case_Terminal : Callable[[Terminal], T]
    case_Nonterm : Callable[[Nonterm], T]
    case_Vocab : Callable[[Vocab], T]


# matching for type item
def match_item(o : item, handlers : ItemHandlers[T]) -> T :
    return o._match(handlers)
    




# type and constructor Rule
@dataclass
class Rule:
    name : str
    content : list[item]
