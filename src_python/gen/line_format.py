
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, TypeVar, Any, Generic, Union, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod

T = TypeVar('T')



# type line_format
@dataclass
class line_format(ABC):
    @abstractmethod
    def _match(self, handlers : LineFormatHandlers[T]) -> T: pass


# constructors for type line_format

@dataclass
class InLine(line_format):


    def _match(self, handlers : LineFormatHandlers[T]) -> T:
        return handlers.case_InLine(self)

def make_InLine() -> line_format:
    return InLine()
        

@dataclass
class NewLine(line_format):


    def _match(self, handlers : LineFormatHandlers[T]) -> T:
        return handlers.case_NewLine(self)

def make_NewLine() -> line_format:
    return NewLine()
        

@dataclass
class IndentLine(line_format):


    def _match(self, handlers : LineFormatHandlers[T]) -> T:
        return handlers.case_IndentLine(self)

def make_IndentLine() -> line_format:
    return IndentLine()
        

# case handlers for type line_format
@dataclass
class LineFormatHandlers(Generic[T]):
    case_InLine : Callable[[InLine], T]
    case_NewLine : Callable[[NewLine], T]
    case_IndentLine : Callable[[IndentLine], T]


# matching for type line_format
def match_line_format(o : line_format, handlers : LineFormatHandlers[T]) -> T :
    return o._match(handlers)

    