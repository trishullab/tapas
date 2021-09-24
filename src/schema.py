from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod
import def_type

import inflection

from gen.line_format import line_format

T = TypeVar('T')

# type and constructor Production 
@dataclass
class Node:
    name: str 
    leader: str
    children: list[Child]

@dataclass
class Child:
    attr: str 
    typ: str
    line_form: line_format 
    follower: str


def to_constructor(n : Node) -> def_type.Constructor:
    return def_type.Constructor(
        n.name,
        [
            def_type.Field(attr = c.attr, typ = c.typ)
            for c in n.children
        ]
    )