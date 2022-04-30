from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod

import inflection

from lib.rule_construct_autogen import *
from lib import construct_def
from lib import line_format_system as lf


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

def to_constructor(n : Rule) -> construct_def.Constructor:

    def fail():
        assert False 

    return construct_def.Constructor(
        n.name, [], [
            match_item(item, ItemHandlers[construct_def.Field](
                case_Terminal = lambda o : (
                    fail()
                ),
                case_Nonterm = lambda o : (
                    construct_def.Field(attr = o.relation, typ = f'{o.nonterminal} | None', default = "")
                ),
                case_Vocab = lambda o : (
                    construct_def.Field(attr = o.relation, typ = 'str', default = "")
                )
            )) 
            for item in n.content
            if not isinstance(item, Terminal)
        ]
    )


def get_abstract_items(rule : Rule): 
    return [item
        for item in rule.content
        if not isinstance(item, Terminal)
    ]


def type_from_item(item : item, prefix : str = ""):
    if isinstance(item, Nonterm):
        if prefix:
            return f"{prefix}.{item.nonterminal}"
        else:
            return item.nonterminal

    elif isinstance(item, Vocab):
        return "str" 
    else:
        raise Exception()

def relation_from_item(item : item):
    if isinstance(item, Nonterm):
        return item.relation
    elif isinstance(item, Vocab):
        return item.relation 
    else:
        raise Exception()


def is_inductive(type_name : str, rules : list[Rule]) -> bool:
    for rule in rules:
        for item in rule.content:
            if not isinstance(item, Terminal) and type_name == type_from_item(item, ""):
                return True
    return False


