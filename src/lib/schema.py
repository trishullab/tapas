from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod

import inflection

from lib import def_type
from lib.line_format import line_format
from lib import line_format as lf


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

def to_dictionary(node: Node):
    return {
        'name' : node.name,
        'leader' : node.leader,
        'children' : [
            {
                'alias' : c.attr,
                'nonterminal' : c.typ,
                'format' : lf.to_string(c.line_form),
                'follower' : c.follower

            }
            for c in node.children
        ]

    }

def to_constructor(n : Node) -> def_type.Constructor:
    return def_type.Constructor(
        n.name,
        [
            def_type.Field(attr = c.attr, typ = c.typ)
            for c in n.children
        ]
    )