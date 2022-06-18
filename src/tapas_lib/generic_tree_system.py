from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar, Any, Generic, Union, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod

from tree_sitter import Language
import tree_sitter

from tapas_base import util_system

T = TypeVar('T')


# type and constructor GenericNode
@dataclass
class GenericNode:
    syntax_part : str
    text : str
    children : list[GenericNode]



#
# Recursive version:
#
# def from_tree_sitter_node(node : tree_sitter.Node, source_bytes : bytes, encoding : str) -> GenericNode :

#     text = source_bytes[node.start_byte:node.end_byte].decode(encoding)

#     children = [
#         from_tree_sitter_node(n, source_bytes, encoding) 
#         for n in node.children 
#         if n.type != "comment"
#     ]

#     return GenericNode(
#         syntax_part = node.type, 
#         text = text,
#         children = children 
#     )


# Stack version
def from_tree_sitter_node(node : tree_sitter.Node, source_bytes : bytes, encoding : str) -> GenericNode :

    def sans_comments(ns):
        return [
            n
            for n in ns 
            if n.type != "comment"
        ]

    text_0 = source_bytes[node.start_byte:node.end_byte].decode(encoding)
    stack : list[tuple[str, str, list[GenericNode], list[tree_sitter.Node]]] = [(node.type, text_0, [], sans_comments(node.children))]

    result = None 

    while stack:
        (syntax_part, text, gnodes, tsnodes) = stack.pop()

        next_gnodes = gnodes
        if result:
            next_gnodes = gnodes + [result]
            result = None

        if len(next_gnodes) == len(tsnodes):
            result = GenericNode(
                syntax_part = syntax_part, 
                text = text,
                children = next_gnodes 
            )

        else: 
            stack.append((syntax_part, text, next_gnodes, tsnodes))
            child_index = len(next_gnodes) 
            child_tsnode = tsnodes[child_index]
            child_text = source_bytes[child_tsnode.start_byte:child_tsnode.end_byte].decode(encoding)
            stack.append((child_tsnode.type, child_text, [], sans_comments(child_tsnode.children)))

    assert result
    return result 


import pathlib
import os

base_path = pathlib.Path(__file__).parent.absolute()

def parse(lang_name : str, source : str, encoding : str) -> GenericNode:
    grammars_path = util_system.project_path('tapas_res/grammars.so')
    grammar = Language(grammars_path, lang_name)

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