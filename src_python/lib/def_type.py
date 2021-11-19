from __future__ import annotations

from dataclasses import dataclass

import inflection

@dataclass
class Field:
    attr : str
    typ : str

@dataclass
class Constructor:
    name: str 
    fields: list[Field]


header = """
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, TypeVar, Any, Generic, Union, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod

T = TypeVar('T')
"""

def generate_single(
    constructor : Constructor 
) -> str:
    nl = "\n" 

    code = (f"""
# type and constructor {constructor.name}
@dataclass
class {constructor.name}:
{nl.join([
    f"    {field.attr} : {field.typ}" 
    for field in constructor.fields 
])}
""")
    return code 



def generate_choice(
    type_name : str,
    constructors : list[Constructor] 
) -> str:
    handlers_name = f"{inflection.camelize(type_name)}Handlers"
    nl = "\n"

    def generate_constructor(constructor : Constructor) -> str:
        nonlocal handlers_name
        return (f"""
@dataclass
class {constructor.name}({type_name}):
{nl.join([
    f"    {field.attr} : {field.typ}"
    for field in constructor.fields
])}

    def _match(self, handlers : {handlers_name}[T]) -> T:
        return handlers.case_{constructor.name}(self)

def make_{constructor.name}({", ".join([
    f"{field.attr} : {field.typ}"
    for field in constructor.fields
])}) -> {type_name}:
    return {constructor.name}({f", ".join([
        field.attr
        for field in constructor.fields
    ])})
        """)

    code = (f"""
# type {type_name}
@dataclass
class {type_name}(ABC):
    @abstractmethod
    def _match(self, handlers : {handlers_name}[T]) -> T: pass


# constructors for type {type_name}
{nl.join([
    generate_constructor(constructor)
    for constructor in constructors
])}

# case handlers for type {type_name}
@dataclass
class {handlers_name}(Generic[T]):
{nl.join([
    f"    case_{constructor.name} : Callable[[{constructor.name}], T]"
    for constructor in constructors 
])}


# matching for type {type_name}
def match_{type_name}(o : {type_name}, handlers : {handlers_name}[T]) -> T :
    return o._match(handlers)

    """)
    return code 


