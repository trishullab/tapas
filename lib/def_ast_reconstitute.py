from __future__ import annotations

from dataclasses import dataclass

import lib.rule
from lib.rule import Rule

import lib.python_schema

nl = "\n"

def get_relation_from_item(item : lib.rule.item) -> str:
    if isinstance(item, lib.rule.Nonterm):
        return item.relation

    elif isinstance(item, lib.rule.Vocab):
        return item.relation
    else:
        raise Exception()

def get_abstract_items(rule : Rule): 
    return [item
        for item in rule.content
        if not isinstance(item, lib.rule.Terminal)
    ]


def type_from_item(item : lib.rule.item):
    if isinstance(item, lib.rule.Nonterm):
        return item.nonterminal
    elif isinstance(item, lib.rule.Vocab):
        return "str" 
    else:
        raise Exception()


def generate_choice_procedure(type_name : str, rules : list[Rule]) -> str:

    def generate_updates(type_name : str, rule : Rule):
        abstract_items = get_abstract_items(rule)
        return f"""
        elif rule_name == "{rule.name}": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = {len(abstract_items)}

            index = len(next_children)
            if index == total_num_children:
                result = (
                    {rule.name}({', '.join([f"next_children[{i}]" for i in range(0, len(abstract_items))])}),
                    next_remainder
                )
            {nl.join([
                f'''
            elif index == {i}:
                (next_child, next_remainder) = to_{type_from_item(item)}(next_remainder)
                stack.append(("{rule.name}", next_children + [next_child], next_remainder))
                '''
                for i, item in enumerate(abstract_items)
                if type_from_item(item) != type_name
            ])}
            else:
                stack.append(("{rule.name}", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        """

    return (f"""
def to_{type_name}(xs : list[instance]) -> tuple[{type_name}, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "{type_name}"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        {nl.join([
            generate_updates(type_name, rule)
            for rule in rules
        ])}

    assert result
    assert isinstance(result[0], {type_name})
    return result
    """)




def generate_single_procedure(rule : Rule) -> str:
    type_name = rule.name

    abstract_items = get_abstract_items(rule)
    nl = "\n"


    node_str = f"{rule.name}({', '.join([get_relation_from_item(item) for item in abstract_items])})" 

    return (f"""
def to_{type_name}(xs : list[instance]) -> tuple[{type_name}, list[instance]]:
    x_0 = xs[-1]
    xs_0 = xs[:-1]
    assert isinstance(x_0, Grammar)
    assert x_0.selection == "{rule.name}"

{nl.join([
    f"    ({get_relation_from_item(item)}, xs_{i + 1}) = to_{type_from_item(item)}(xs_{i})"
    for i, item in enumerate(abstract_items)
])}
    return ({node_str}, xs_{len(abstract_items)})
    """)
    







def generate_content(singles : list[Rule], choices : dict[str, list[Rule]]) -> str:

    header = """
from __future__ import annotations
import lib.instance
from gen.instance import instance, Vocab, Grammar
from gen.python_ast import *
from gen.line_format import InLine, NewLine, IndentLine
    """

    return (f"""
{header}

# definitions operate on reversed lists of instances, starting from the right, going left. 
{nl.join([
    generate_choice_procedure(type_name, rules)
    for type_name, rules in choices.items()
])} 

{nl.join([
    generate_single_procedure(rule)
    for rule in singles
])} 


def to_str(xs : list[instance]) -> tuple[str, list[instance]]:
    hd = xs[-1]
    tl = xs[:-1]
    assert isinstance(hd, Vocab)
    return (hd.selection, tl)
    """)