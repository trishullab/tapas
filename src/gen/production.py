
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, TypeVar, Any, Generic, Union, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod

T = TypeVar('T')



# type production
@dataclass
class production(ABC):
    @abstractmethod
    def _match(self, handlers : ProductionHandlers[T]) -> T: pass


# constructors for type production

@dataclass
class Node(production):
    lhs : str
    rhs : str
    depth : int
    alias : str
    indent_width : int
    inline : bool

    def _match(self, handlers : ProductionHandlers[T]) -> T:
        return handlers.case_Node(self)


def make_Node(
    lhs : str,
    rhs : str,
    depth : int,
    alias : str,
    indent_width : int,
    inline : bool
) -> production:
    return Node(
        lhs,
        rhs,
        depth,
        alias,
        indent_width,
        inline
    )


@dataclass
class Symbol(production):
    content : str
    depth : int
    alias : str

    def _match(self, handlers : ProductionHandlers[T]) -> T:
        return handlers.case_Symbol(self)


def make_Symbol(
    content : str,
    depth : int,
    alias : str
) -> production:
    return Symbol(
        content,
        depth,
        alias
    )


# case handlers for type production
@dataclass
class ProductionHandlers(Generic[T]):
    case_Node : Callable[[Node], T]
    case_Symbol : Callable[[Symbol], T]


# matching for type production
def match_production(o : production, handlers : ProductionHandlers[T]) -> T :
    return o._match(handlers)