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

single_str = """

def serialize_{{ node.name }}(
    o : {{ node.name }}
) -> list[prod_inst.instance]:

    return (
        [prod_inst.make_Grammar(
            nonterminal = '{{ node.name }}',
            sequence_id = '{{ node.name }}'
        )]{% if node.children %} +
{% endif %}
{% for child in node.children %}
{% if is_vocab(child) %}
        [prod_inst.make_Vocab(
            choices_id = '{{ child.choices_id }}',
            word = o.{{ child.relation }}
        )]{% if not loop.last %} +
{% endif %}
{% else %}
        serialize_{{ child.nonterminal }}(o.{{ child.relation }}){% if not loop.last %} +
{% endif %}

{% endif %}
{% endfor %}
    )
"""


def is_vocab(o : schema.child):
    return isinstance(o, schema.Vocab)

def generate_single_def(
    node : schema.Node 
) -> str:
    
    tmpl = jinja_env.from_string(single_str)
    code : str = tmpl.render(
        node = node,
        line_format_string = line_format.to_string,
        is_vocab = is_vocab
    )
    return code 


choice_str = """


def serialize_{{ type_name }}(
    o : {{ type_name }}
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[{{ type_name }}, list[prod_inst.instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, {{ type_name }}):

{% for node in nodes %}
            def handle_{{ node.name }}(o : {{ node.name }}): 
                nonlocal stack
                assert isinstance(o, {{ type_name }})

{% for child in node.children|reverse %}
{% if is_vocab(child) %}
                stack.append(
                    [prod_inst.make_Vocab(
                        choices_id = '{{ child.choices_id }}',
                        word = o.{{ child.relation }}
                    )]
                )
{% elif child.nonterminal == type_name %}
                stack.append(
                    o.{{ child.relation }}
                )
{% else %}
                stack.append(
                    serialize_{{ child.nonterminal }}(o.{{ child.relation }})
                )
{% endif %}
{% endfor %}
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = '{{ type_name }}',
                        sequence_id = '{{ node.name }}'
                    )]
                )

{% endfor %}

            match_{{ type_name }}(stack_item, {{ handlers_name }}(
{% for node in nodes %}
                case_{{ node.name }} = handle_{{ node.name }}{% if not loop.last %}, {% endif %} 
{% endfor %}
            ))

        else:
            result += stack_item 

    return result
"""

def generate_choice_def(
    type_name : str,
    nodes : list[schema.Node] 
) -> str:
    handlers_name = f"{inflection.camelize(type_name)}Handlers"

    tmpl = jinja_env.from_string(choice_str)
    code : str = tmpl.render(
        type_name = type_name, 
        nodes = nodes,
        handlers_name = handlers_name,
        line_format_string = line_format.to_string,
        is_vocab = is_vocab
    )
    return code 