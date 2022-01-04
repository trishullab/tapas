from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod

import inflection

from gen.rule_construct import *
from lib import def_construct
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

def to_constructor(n : Rule) -> def_construct.Constructor:

    def fail():
        assert False 

    return def_construct.Constructor(
        n.name,
        [
            match_item(item, ItemHandlers[def_construct.Field](
                case_Terminal = lambda o : (
                    fail()
                ),
                case_Nonterm = lambda o : (
                    def_construct.Field(attr = o.relation, typ = o.nonterminal)
                ),
                case_Vocab = lambda o : (
                    def_construct.Field(attr = o.relation, typ = 'str')
                )
            )) 
            for item in n.content
            if not isinstance(item, Terminal)
        ]
    )