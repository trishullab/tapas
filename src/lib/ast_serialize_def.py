from __future__ import annotations

import inflection

import lib.rule
from lib.rule import Rule

def is_vocab(o : lib.rule.item):
    return isinstance(o, lib.rule.Vocab)

def generate_single_procedure(
    rule : Rule 
) -> str:

    def assert_not_terminal(o : lib.rule.item) -> str:
        assert not isinstance(o, lib.rule.Terminal)
        return ""

    nl = "\n"
    return (f"""

def from_{rule.name}(
    o : {rule.name}
) -> tuple[abstract_token, ...]:

    return (
        tuple([lib.abstract_token.make_Grammar(
            options = '{rule.name}',
            selection = '{rule.name}'
        )]){f' +{nl}' if rule.content else ''}
{f' +{nl}'.join([

    lib.rule.match_item(item, lib.rule.ItemHandlers[str](
        case_Vocab = lambda o : (
            "    " * 2 + f"tuple([lib.abstract_token.make_Vocab(options = '{o.vocab}', selection = o.{o.relation})])"
        ),
        case_Nonterm = lambda o : (
            "    " * 2 + f"from_{o.nonterminal}(o.{o.relation})"
        ),
        case_Terminal = lambda o : (
            assert_not_terminal(o)
        )
    ))

    for item in rule.content 
    if not isinstance(item, lib.rule.Terminal)
])}

    )
    """)

def generate_item(type_name : str, item : lib.rule.item):
    return lib.rule.match_item(item, lib.rule.ItemHandlers[str](
        case_Vocab=lambda o : (f"""
                stack.append(
                    tuple([lib.abstract_token.make_Vocab(
                        options = '{o.vocab}',
                        selection = o.{o.relation}
                    )])
                )
        """),
        case_Nonterm=lambda o : (
            f"""
                stack.append(o.{o.relation})"""
            if o.nonterminal == type_name else 

            f"""
                stack.append(from_{o.nonterminal}(o.{o.relation}))"""
        ),
        case_Terminal=lambda o : (
            ""
        )
    ))



def generate_rule_handler(type_name : str, rule : Rule):
    nl = "\n"

    return (f"""
            def handle_{rule.name}(o : {rule.name}): 
                {nl.join([
                    generate_item(type_name, child)
                    for child in reversed(rule.content)
                ])}
                stack.append(
                    tuple([lib.abstract_token.make_Grammar(
                        options = '{type_name}',
                        selection = '{rule.name}'
                    )])
                )
    """)


def generate_choice_procedure(
    type_name : str,
    rules : list[Rule] 
) -> str:
    handlers_name = f"{inflection.camelize(type_name)}Handlers"
    nl = "\n"

    return (f"""

def from_{type_name}(
    o : {type_name}
) -> tuple[abstract_token, ...]:

    result = () 

    stack : list[Union[{type_name}, tuple[abstract_token, ...]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, {type_name}):

            {nl.join([
                generate_rule_handler(type_name, rule)
                for rule in rules 
            ])}


            match_{type_name}(stack_item, {handlers_name}(
{f",{nl}".join([
    "    " * 4 + f"case_{rule.name} = handle_{rule.name}"
    for rule in rules 
])}
            ))

        else:
            result += stack_item 

    return result
    """)


def generate_content(singles : list[Rule], choices : dict[str, list[Rule]]) -> str:

    header = """
from __future__ import annotations
import lib.abstract_token
from lib.abstract_token_construct_autogen import abstract_token
from lib.python_ast_construct_autogen import *
from lib.line_format_construct_autogen import InLine, NewLine, IndentLine
"""

    nl = "\n"

    return (f"""
{header}

{nl.join([
    generate_choice_procedure(type_name, rules)
    for type_name, rules in choices.items()
])} 

{nl.join([
    generate_single_procedure(rule)
    for rule in singles
])} 

    """)