from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod

import inflection

from gen.schema import *
from lib import def_type
from lib import line_format as lf


def to_dictionary(node: Node):
    return {
        'name' : node.name,
        'leader' : node.leader,
        'children' : [
            match_child(c, ChildHandlers[dict](
                case_Grammar = lambda o : ({
                    'kind' : 'fixed',
                    'relation' : o.relation,
                    'nonterminal' : o.nonterminal,
                    'format' : lf.to_string(o.format),
                    'follower' : o.follower
                }),
                case_Vocab = lambda o : ({
                    'kind' : 'flex',
                    'relation' : o.relation,
                    'choices_id' : o.choices_id
                })
            )) 
            for c in node.children
        ]

    }

def to_constructor(n : Node) -> def_type.Constructor:
    return def_type.Constructor(
        n.name,
        [

            match_child(c, ChildHandlers[def_type.Field](
                case_Grammar = lambda o : (
                    def_type.Field(attr = o.relation, typ = o.nonterminal)
                ),
                case_Vocab = lambda o : (
                    def_type.Field(attr = o.relation, typ = 'str')
                )
            )) 
            for c in n.children
        ]
    )