
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, TypeVar, Any, Generic, Union, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod

T = TypeVar('T')


from gen.line_format import line_format


# type child
@dataclass
class child(ABC):
    @abstractmethod
    def _match(self, handlers : ChildHandlers[T]) -> T: pass


# constructors for type child

@dataclass
class Grammar(child):
    relation : str
    nonterminal : str
    format : line_format
    follower : str

    def _match(self, handlers : ChildHandlers[T]) -> T:
        return handlers.case_Grammar(self)


def make_Grammar(
    relation : str,
    nonterminal : str,
    format : line_format,
    follower : str
) -> child:
    return Grammar(
        relation,
        nonterminal,
        format,
        follower
    )


@dataclass
class Vocab(child):
    relation : str
    choices_id : str

    def _match(self, handlers : ChildHandlers[T]) -> T:
        return handlers.case_Vocab(self)


def make_Vocab(
    relation : str,
    choices_id : str
) -> child:
    return Vocab(
        relation,
        choices_id
    )


# case handlers for type child
@dataclass
class ChildHandlers(Generic[T]):
    case_Grammar : Callable[[Grammar], T]
    case_Vocab : Callable[[Vocab], T]


# matching for type child
def match_child(o : child, handlers : ChildHandlers[T]) -> T :
    return o._match(handlers)




# type and constructor Node
@dataclass
class Node:
    name : str
    leader : str
    children : list[child]
    