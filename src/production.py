from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, TypeVar, Any, Generic, Union, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod

import inflection

T = TypeVar('T')

# type and constructor Production 
@dataclass
class Production:
    lhs : str
    rhs : str
    depth : int
    alias : Optional[str] = None
    symbol : Optional[str] = None


def map_option(
    serialize_item : Callable[[T, int, Optional[str]], list[Production]],
    item_op : Optional[T], 
    depth : int = 0, 
    alias : Optional[str] = None
) -> list[Production] : 
    return (serialize_item(item_op, depth + 1, alias)
        if item_op != None else [])

def map_list(
    name : str,
    serialize_item : Callable[[T, int], list[Production]],
    items : list[T], 
    depth : int = 0, 
    alias : Optional[str] = None
) -> list[Production]:
    return [
        Production(
            lhs = f'list[{name}]',
            rhs = f'[...]',
            depth = depth,
            alias = alias
        )
    ] + [
        production 
        for item in items 
        for production in serialize_item(item, depth + 1)
    ]



def dump(prods : list[Production], indent : int = 4):
    strs = list(map(
        lambda prod : (
            (indent_str := (' ' * prod.depth * indent)),
            (prefix := (prod.alias if (isinstance(prod.alias, str)) else '_')),
            indent_str + prefix + ' : ' + prod.lhs + ' = ' + prod.rhs +
            (f" {prod.symbol}" if prod.symbol else '')
        )[-1], 
        prods 
    ))
    return '\n'.join(strs)
