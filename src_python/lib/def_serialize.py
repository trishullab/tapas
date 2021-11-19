from __future__ import annotations

from dataclasses import dataclass

import inflection
import jinja2

from lib import schema
from lib import line_format

jinja_env = jinja2.Environment(trim_blocks=True)
# jinja_env.globals.update(isinstance=isinstance)



header = """
from __future__ import annotations
from lib import production_instance as prod_inst 
from gen.python_ast import *
from gen.line_format import InLine, NewLine, IndentLine
"""



def is_vocab(o : schema.child):
    return isinstance(o, schema.Vocab)

def generate_single_def(
    node : schema.Node 
) -> str:


    def assert_not_terminal(o : schema.child) -> str:
        assert not isinstance(o, schema.Terminal)
        return ""

    nl = "\n"
    code = (f"""


def serialize_{node.name}(
    o : {node.name}
) -> list[prod_inst.instance]:

    return (
        [prod_inst.make_Grammar(
            nonterminal = '{node.name}',
            sequence_id = '{node.name}'
        )]{f' +{nl}' if node.children else ''}
{f' +{nl}'.join([


    schema.match_child(child, schema.ChildHandlers[str](
        case_Vocab = lambda o : (
            "    " * 2 + f"[prod_inst.make_Vocab(choices_id = '{o.vocab}', word = o.{o.relation})]"
        ),
        case_Nonterm = lambda o : (
            "    " * 2 + f"serialize_{o.nonterminal}(o.{o.relation})"
        ),
        case_Terminal = lambda o : (
            assert_not_terminal(o)
        )
    ))

    for child in node.children
    if not isinstance(child, schema.Terminal)
])}

    )
    """)
    
    return code 



def generate_choice_def(
    type_name : str,
    nodes : list[schema.Node] 
) -> str:
    handlers_name = f"{inflection.camelize(type_name)}Handlers"
    nl = "\n"

    def generate_child(child : schema.child):
        return schema.match_child(child, schema.ChildHandlers[str](
            case_Vocab=lambda o : (f"""
                stack.append(
                    [prod_inst.make_Vocab(
                        choices_id = '{o.vocab}',
                        word = o.{o.relation}
                    )]
                )
            """),
            case_Nonterm=lambda o : (
                f"""
                stack.append(
                    o.{o.relation}
                )
                """
                if o.nonterminal == type_name else 

                f"""
                stack.append(
                    serialize_{o.nonterminal}(o.{o.relation})
                )
                """
            ),
            case_Terminal=lambda o : (
                ""
            )
        ))



    def generate_node_handler(node : schema.Node):
        return (f"""

            def handle_{node.name}(o : {node.name}): 
                nonlocal stack
                assert isinstance(o, {type_name})

                {nl.join([
                    generate_child(child)
                    for child in reversed(node.children)
                ])}
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = '{type_name}',
                        sequence_id = '{node.name}'
                    )]
                )
        """)

    code = (f"""


def serialize_{type_name}(
    o : {type_name}
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[{type_name}, list[prod_inst.instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, {type_name}):

            {nl.join([
                generate_node_handler(node)
                for node in nodes
            ])}


            match_{type_name}(stack_item, {handlers_name}(
{f",{nl}".join([
    "    " * 4 + f"case_{node.name} = handle_{node.name}"
    for node in nodes
])}
            ))

        else:
            result += stack_item 

    return result
    """)
    return code 