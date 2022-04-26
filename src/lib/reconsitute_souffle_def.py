from __future__ import annotations

from dataclasses import dataclass

import lib.rule_system
from lib.rule_system import Rule

import lib.python_schema_system

nl = "\n"

def generate_souffle_rule(type_name : str, rule : Rule) -> str:
    def fail():
        raise Exception()


    def relation_from_item(item : lib.rule_system.item) -> str:
        if isinstance(item, lib.rule_system.Nonterm):
            return item.relation

        elif isinstance(item, lib.rule_system.Vocab):
            return item.relation
        else:
            raise Exception()

    abstract_items = [item
        for item in rule.content
        if not isinstance(item, lib.rule_system.Terminal)
    ]

    rule_items_str = ", ".join([
        relation_from_item(item)
        for item in abstract_items 
    ])



    def type_from_item(item : lib.rule_system.item):
        if isinstance(item, lib.rule_system.Nonterm):
            return item.nonterminal
        elif isinstance(item, lib.rule_system.Vocab):
            return "symbol" 
        else:
            raise Exception()

    if (len(abstract_items) > 0):
        return (f"""
    rel_{type_name}([$Grammar("{type_name}", "{rule.name}"), xs_0], ${rule.name}({rule_items_str}), xs_{len(abstract_items)}) :-
{
f",{nl}".join([
    f"        rel_{type_from_item(item)}(xs_{i}, {relation_from_item(item)}, xs_{i + 1}), tail(xs_{i})"
    for i, item in enumerate(abstract_items)
]) + "."
}""")
    else:
        return (f"""
    rel_{type_name}([$Grammar("{type_name}", "{rule.name}"), xs_0], ${rule.name}({rule_items_str}), xs_0).
        """)


def generate_souffle_relation(type_name : str, rules : list[Rule]) -> str:
    
    return (f"""
    .decl rel_{type_name}(xs : sequence, tree : {type_name}, suffix : sequence)

    {nl.join([
        generate_souffle_rule(type_name, rule) 
        for rule in rules
    ])}
    """)

content = (f"""
#include "instance.dl"
#include "python_ast.dl"
#include "../lib/sequence.dl"
.comp reconstitute {{

    .decl in(xs : sequence)

    .decl tail(xs : sequence)
    tail(xs) :- in(xs).
    tail(xs) :- tail([_, xs]).


    {nl.join([
        generate_souffle_relation(type_name, rules)
        for type_name, rules in lib.python_schema_system.schema.items()
    ])} 

    .decl rel_symbol(xs : sequence, word : symbol, suffix : sequence)
    rel_symbol([$Vocab(_, word), xs], word, xs) :- tail(xs).

}}
""")

    # .init the_split = split 
    # the_split.in(xs) :- in(xs).