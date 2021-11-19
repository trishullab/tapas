
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
class Terminal(child):
    terminal : str

    def _match(self, handlers : ChildHandlers[T]) -> T:
        return handlers.case_Terminal(self)


def make_Terminal(
    terminal : str
) -> child:
    return Terminal(
        terminal
    )


@dataclass
class Nonterm(child):
    relation : str
    nonterminal : str
    format : line_format

    def _match(self, handlers : ChildHandlers[T]) -> T:
        return handlers.case_Nonterm(self)


def make_Nonterm(
    relation : str,
    nonterminal : str,
    format : line_format
) -> child:
    return Nonterm(
        relation,
        nonterminal,
        format
    )


@dataclass
class Vocab(child):
    relation : str
    vocab : str

    def _match(self, handlers : ChildHandlers[T]) -> T:
        return handlers.case_Vocab(self)


def make_Vocab(
    relation : str,
    vocab : str
) -> child:
    return Vocab(
        relation,
        vocab
    )


# case handlers for type child
@dataclass
class ChildHandlers(Generic[T]):
    case_Terminal : Callable[[Terminal], T]
    case_Nonterm : Callable[[Nonterm], T]
    case_Vocab : Callable[[Vocab], T]


# matching for type child
def match_child(o : child, handlers : ChildHandlers[T]) -> T :
    return o._match(handlers)




# type and constructor Node
@dataclass
class Node:
    name : str
    children : list[child]
    