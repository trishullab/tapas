from __future__ import annotations

from dataclasses import dataclass

import lib.rule_system
from lib.rule_system import Rule

import lib.python_schema_system

nl = "\n"

def generate_choice_procedure(type_name : str, rules : list[Rule]) -> str:

    def generate_updates(type_name : str, rule : Rule):
        abstract_items = lib.rule_system.get_abstract_items(rule)
        return f"""
        elif rule_name == "{rule.name}": 
            children = children
            remainder = remainder
            if stack_result:
                # get the result from the child in the stack
                (child, remainder) = stack_result
                children = children + [child]
                stack_result = None

            total_num_children = {len(abstract_items)}

            index = len(children)
            if index == total_num_children:
                # the processing of the current rule has completed
                # return the result to the parent in the stack 
                stack_result = (
                    {rule.name}({', '.join([f"children[{i}]" for i in range(0, len(abstract_items))])}),
                    remainder
                )
            {nl.join([
                f'''
            elif index == {i}: # index does *not* refer to an inductive child
                (child, remainder) = to_{lib.rule_system.type_from_item(item, '')}(remainder)
                stack.append((x, children + [child], remainder))
                '''
                for i, item in enumerate(abstract_items)
                if lib.rule_system.type_from_item(item, '') != type_name
            ])}
            else: # index refers to an inductive child
                stack.append((x, children, remainder))
                stack.append((remainder[-1], [], remainder[:-1]))
        """

    return (f"""
def to_{type_name}(xs : tuple[abstract_token, ...]) -> tuple[{type_name}, tuple[abstract_token, ...]]:

    initial = (xs[-1], [], xs[:-1])
    stack : list[tuple[abstract_token, list[Any], tuple[abstract_token, ...]]] = [initial]

    stack_result = None 
    while stack:
        (x, children, remainder) = stack.pop()
        assert isinstance(x, Grammar)
        assert x.options == "{type_name}"
        rule_name = x.selection

        if False:
            pass
        {nl.join([
            generate_updates(type_name, rule)
            for rule in rules
        ])}

    assert stack_result
    assert isinstance(stack_result[0], {type_name})
    return stack_result
    """)




def generate_single_procedure(rule : Rule) -> str:
    type_name = rule.name

    abstract_items = lib.rule_system.get_abstract_items(rule)
    nl = "\n"

    node_str = f"{rule.name}({', '.join([lib.rule_system.relation_from_item(item) for item in abstract_items])})" 

    return (f"""
def to_{type_name}(xs : tuple[abstract_token, ...]) -> tuple[{type_name}, tuple[abstract_token, ...]]:
    x = xs[-1]
    xs = xs[:-1]
    assert isinstance(x, Grammar)
    assert x.options == "{type_name}"
    assert x.selection == "{rule.name}"

{nl.join([
    f"    ({lib.rule_system.relation_from_item(item)}, xs) = to_{lib.rule_system.type_from_item(item, '')}(xs)"
    for item in abstract_items
])}
    return ({node_str}, xs)
    """)
    
def generate_content(content_header : str, singles : list[Rule], choices : dict[str, list[Rule]]) -> str:

    header = """
from __future__ import annotations
from lib import abstract_token_system as ats
from lib.abstract_token_system import abstract_token, Vocab, Grammar
from lib.line_format_construct_autogen import InLine, NewLine, IndentLine
    """

    return (f"""
{header}

{content_header}

# definitions operate on reversed lists of abstract tokens, starting from the right, going left. 
{nl.join([
    generate_choice_procedure(type_name, rules)
    for type_name, rules in choices.items()
])} 

{nl.join([
    generate_single_procedure(rule)
    for rule in singles
])} 


def to_str(xs : tuple[abstract_token, ...]) -> tuple[str, tuple[abstract_token, ...]]:
    hd = xs[-1]
    tl = xs[:-1]
    assert isinstance(hd, Vocab)
    return (hd.selection, tl)
    """)