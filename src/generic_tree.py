from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar, Any, Generic, Union, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod

from tree_sitter import Language

import tree_sitter

from utils import fail


T = TypeVar('T')


# type and constructor GenericNode
@dataclass
class GenericNode:
    syntax_part : str
    text : str
    children : list[GenericNode]



def from_tree_sitter_node(node : tree_sitter.Node, source_bytes : bytes, encoding : str) -> GenericNode :

    text = source_bytes[node.start_byte:node.end_byte].decode(encoding)

    children = [
        from_tree_sitter_node(n, source_bytes, encoding) 
        for n in node.children 
    ]
    return GenericNode(
        syntax_part = node.type, 
        text = text,
        children = children 
    )


def parse(lang_name : str, source : str, encoding : str) -> GenericNode:
    grammar = Language('build/grammars.so', lang_name)

    parser = tree_sitter.Parser()
    parser.set_language(grammar)
    sitter_tree = parser.parse(bytes(source, encoding))

    source_bytes = bytes(source, encoding)

    return from_tree_sitter_node(sitter_tree.root_node, source_bytes, encoding)



def dump(
    node : GenericNode, 
    indent : int = 4, depth : int = 0,
    alias = None,
    text_cond = lambda n : True
) -> str:
    indent_str = ' ' * depth * indent
    alias_str = (f"{alias} | " if alias else "")
    return indent_str + alias_str + node.syntax_part + (
        (' -> ' + node.text if node.text != '' and text_cond(node) else '') + 
        (
            (
                str_children := [
                    dump(child, indent, depth + 1, str(i), text_cond)
                    for i, child in enumerate(node.children)
                ],

                '\n' + '\n'.join(str_children) 
            )[-1]
            if len(node.children) > 0 else 
            ''
        )
    )