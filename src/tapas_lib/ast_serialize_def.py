from __future__ import annotations

import inflection

from tapas_base import rule_system as rs 
from tapas_base.rule_system import Rule

def is_vocab(o : rs.item):
    return isinstance(o, rs.Vocab)

def generate_single_procedure(
    rule : Rule 
) -> str:

    def assert_not_terminal(o : rs.item) -> str:
        assert not isinstance(o, rs.Terminal)
        return ""

    nl = "\n"
    return (f"""

def from_{rule.name}(
    o : {rule.name} | None
) -> tuple[abstract_token, ...]:
    if o == None:
        return (Hole(),)

    return (
        tuple([make_Grammar(
            options = '{rule.name}',
            selection = '{rule.name}',
            source_start = o.source_start,
            source_end = o.source_end
        )]){f' +{nl}' if rule.content else ''}
{f' +{nl}'.join([

    rs.match_item(item, rs.ItemHandlers[str](
        case_Vocab = lambda o : (
            "    " * 2 + f"tuple([make_Vocab(options = '{o.vocab}', selection = o.{o.relation})])"
        ),
        case_Nonterm = lambda o : (
            "    " * 2 + f"from_{o.nonterminal}(o.{o.relation})"
        ),
        case_Terminal = lambda o : (
            assert_not_terminal(o)
        )
    ))

    for item in rule.content 
    if not isinstance(item, rs.Terminal)
])}

    )
    """)

def generate_item(type_name : str, item : rs.item):
    return rs.match_item(item, rs.ItemHandlers[str](
        case_Vocab=lambda o : (f"""
                stack.append(
                    tuple([make_Vocab(
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
                    tuple([make_Grammar(
                        options = '{type_name}',
                        selection = '{rule.name}',
                        source_start = o.source_start,
                        source_end = o.source_end
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
    o : {type_name} | None
) -> tuple[abstract_token, ...]:
    if o == None:
        return (Hole(),)

    result = () 

    stack : list[{type_name} | None | tuple[abstract_token, ...]] = [o]
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

        elif stack_item == None:
            result += (Hole(),) 
        else:
            result += stack_item 

    return result
    """)


def generate_content(content_header : str, singles : list[Rule], choices : dict[str, list[Rule]]) -> str:

    header = """
from __future__ import annotations
import tapas_base.abstract_token_system
from tapas_base.abstract_token_construct_autogen import abstract_token
from tapas_base.abstract_token_construct_autogen import Hole, make_Grammar, make_Vocab
from tapas_base.line_format_construct_autogen import InLine, NewLine, IndentLine
"""

    nl = "\n"

    return (f"""
{header}

{content_header}

{nl.join([
    generate_choice_procedure(type_name, rules)
    for type_name, rules in choices.items()
])} 

{nl.join([
    generate_single_procedure(rule)
    for rule in singles
])} 

    """)