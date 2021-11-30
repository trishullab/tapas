from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod

import inflection

from gen.rule import *
from lib import def_type
from lib import line_format as lf


def to_dictionary(node: Rule):
    return {
        'name' : node.name,
        'children' : [
            match_item(item, ItemHandlers[dict](
                case_Terminal = lambda o : ({
                    'kind' : 'terminal',
                    'terminal' : o.terminal
                }),
                case_Nonterm = lambda o : ({
                    'kind' : 'grammar',
                    'relation' : o.relation,
                    'nonterminal' : o.nonterminal,
                    'format' : lf.to_string(o.format),
                }),
                case_Vocab = lambda o : ({
                    'kind' : 'vocab',
                    'relation' : o.relation,
                    'vocab' : o.vocab
                })
            )) 
            for item in node.content
        ]

    }

def to_constructor(n : Rule) -> def_type.Constructor:

    def fail():
        assert False 

    return def_type.Constructor(
        n.name,
        [
            match_item(item, ItemHandlers[def_type.Field](
                case_Terminal = lambda o : (
                    fail()
                ),
                case_Nonterm = lambda o : (
                    def_type.Field(attr = o.relation, typ = o.nonterminal)
                ),
                case_Vocab = lambda o : (
                    def_type.Field(attr = o.relation, typ = 'str')
                )
            )) 
            for item in n.content
            if not isinstance(item, Terminal)
        ]
    )