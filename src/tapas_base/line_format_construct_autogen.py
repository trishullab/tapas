# THIS FILE IS AUTOGENERATED
# CHANGES MAY BE LOST



from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, TypeVar, Any, Generic, Union, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod

T = TypeVar('T')


@dataclass(frozen=True, eq=True)
class SourceFlag: 
    pass





# type line_format
@dataclass(frozen=True, eq=True)
class line_format(ABC):
    # @abstractmethod
    def match(self, handlers : LineFormatHandlers[T]) -> T:
        raise Exception()


# constructors for type line_format

@dataclass(frozen=True, eq=True)
class InLine(line_format):


    def match(self, handlers : LineFormatHandlers[T]) -> T:
        return handlers.case_InLine(self)

def make_InLine(
) -> line_format:
    return InLine(
    )

def update_InLine(source_InLine : InLine
) -> InLine:
    return InLine(
    )

        

@dataclass(frozen=True, eq=True)
class NewLine(line_format):


    def match(self, handlers : LineFormatHandlers[T]) -> T:
        return handlers.case_NewLine(self)

def make_NewLine(
) -> line_format:
    return NewLine(
    )

def update_NewLine(source_NewLine : NewLine
) -> NewLine:
    return NewLine(
    )

        

@dataclass(frozen=True, eq=True)
class IndentLine(line_format):


    def match(self, handlers : LineFormatHandlers[T]) -> T:
        return handlers.case_IndentLine(self)

def make_IndentLine(
) -> line_format:
    return IndentLine(
    )

def update_IndentLine(source_IndentLine : IndentLine
) -> IndentLine:
    return IndentLine(
    )

        

# case handlers for type line_format
@dataclass(frozen=True, eq=True)
class LineFormatHandlers(Generic[T]):
    case_InLine : Callable[[InLine], T]
    case_NewLine : Callable[[NewLine], T]
    case_IndentLine : Callable[[IndentLine], T]


# matching for type line_format
def match_line_format(o : line_format, handlers : LineFormatHandlers[T]) -> T :
    return o.match(handlers)


line_format_union = Union[InLine, NewLine, IndentLine]

# unguarding for type line_format
def unguard_line_format(o : line_format) -> line_format_union :
    return match_line_format(o, LineFormatHandlers(
        case_InLine = lambda x : x, 
        case_NewLine = lambda x : x, 
        case_IndentLine = lambda x : x

    ))
     

 
    