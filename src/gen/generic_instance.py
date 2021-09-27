
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
class Node(instance):
    lhs : str
    rhs : str
    depth : int
    alias : str
    indent_width : int
    inline : bool

    def _match(self, handlers : InstanceHandlers[T]) -> T:
        return handlers.case_Node(self)


def make_Node(
    lhs : str,
    rhs : str,
    depth : int,
    alias : str,
    indent_width : int,
    inline : bool
) -> instance:
    return Node(
        lhs,
        rhs,
        depth,
        alias,
        indent_width,
        inline
    )


@dataclass
class Symbol(instance):
    content : str
    depth : int
    alias : str

    def _match(self, handlers : InstanceHandlers[T]) -> T:
        return handlers.case_Symbol(self)


def make_Symbol(
    content : str,
    depth : int,
    alias : str
) -> instance:
    return Symbol(
        content,
        depth,
        alias
    )


# case handlers for type instance
@dataclass
class InstanceHandlers(Generic[T]):
    case_Node : Callable[[Node], T]
    case_Symbol : Callable[[Symbol], T]


# matching for type instance
def match_instance(o : instance, handlers : InstanceHandlers[T]) -> T :
    return o._match(handlers)