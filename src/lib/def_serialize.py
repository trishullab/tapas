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

intersection_str = """
def serialize_{{ node.name }}(
    o : {{ node.name }}, depth : int = 0, relation : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    @dataclass
    class SP:
        o : {{ node.name }} 
        depth : int
        relation : str
        indent_width : int 
        inline : bool

    stack : list[Union[SP, list[prod_inst.instance]]] = [SP(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP):
            o = item.o

            stack += [
{% for child in node.children|reverse %}
{% if is_vocab(child) %}
                [prod_inst.make_Vocab(
                    choices_id = '{{ child.choices_id }}',
                    word = o.{{ child.relation }},
                    depth = item.depth + 1,
                    relation = "{{ child.relation }}"
                )],
{% elif child.nonterminal == node.name %}
                serialize_{{ child.nonterminal }}(o.{{ child.relation }}, item.depth + 1, "{{ child.relation }}", 
                    prod_inst.next_indent_width(item.indent_width, {{ line_format_string(child.format) + "()" }}),
                    {{ "True" if line_format_string(child.format) == "InLine" else "False"  }},
                ),
{% else %}
                serialize_{{ child.nonterminal }}(o.{{ child.relation }}, item.depth + 1, "{{ child.relation }}", 
                    prod_inst.next_indent_width(item.indent_width, {{ line_format_string(child.format) + "()" }}),
                    {{ "True" if line_format_string(child.format) == "InLine" else "False"  }},
                ),
{% endif %}
{% endfor %}
                [prod_inst.make_Grammar(
                    nonterminal = '{{ node.name }}',
                    sequence_id = '{{ node.name }}',
                    depth = item.depth,
                    relation = item.relation,
                    indent_width = item.indent_width,
                    inline = item.inline
                )]
            ]
        else:
            result += item

    return result
"""


def is_vocab(o : schema.child):
    return isinstance(o, schema.Vocab)

def generate_intersection_def(
    node : schema.Node 
) -> str:
    
    tmpl = jinja_env.from_string(intersection_str)
    code : str = tmpl.render(
        node = node,
        line_format_string = line_format.to_string,
        is_vocab = is_vocab
    )
    return code 


union_str = """
def serialize_{{ type_name }}(
    o : {{ type_name }}, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    @dataclass
    class SP:
        o : {{ type_name }} 
        depth : int
        relation : str
        indent_width : int 
        inline : bool

    stack : list[Union[SP, list[prod_inst.instance]]] = [SP(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP):
            o = item.o

{% for node in nodes %}
            def handle_{{ node.name }}(o : {{ node.name }}): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP)

                stack += [
{% for child in node.children|reverse %}
{% if is_vocab(child) %}
                    [prod_inst.make_Vocab(
                        choices_id = '{{ child.choices_id }}',
                        word = o.{{ child.relation }},
                        depth = item.depth + 1,
                        relation = "{{ child.relation }}"
                    )],
{% elif child.nonterminal == type_name %}
                    SP(o.{{ child.relation }}, item.depth + 1, "{{ child.relation }}", 
                        prod_inst.next_indent_width(item.indent_width, {{ line_format_string(child.format) + "()" }}),
                        {{ "True" if line_format_string(child.format) == "InLine" else "False"  }},
                    ), 
{% else %}
                    serialize_{{ child.nonterminal }}(o.{{ child.relation }}, item.depth + 1, "{{ child.relation }}", 
                        prod_inst.next_indent_width(item.indent_width, {{ line_format_string(child.format) + "()" }}),
                        {{ "True" if line_format_string(child.format) == "InLine" else "False"  }},
                    ), 
{% endif %}
{% endfor %}
                    [prod_inst.make_Grammar(
                        nonterminal = '{{ type_name }}',
                        sequence_id = '{{ node.name }}',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                ]

{% endfor %}

            match_{{ type_name }}(o, {{ handlers_name }}(
{% for node in nodes %}
                case_{{ node.name }} = handle_{{ node.name }}{% if not loop.last %}, {% endif %} 
{% endfor %}
            ))

        else:
            result += item

    return result
"""

def generate_union_def(
    type_name : str,
    nodes : list[schema.Node] 
) -> str:
    handlers_name = f"{inflection.camelize(type_name)}Handlers"

    tmpl = jinja_env.from_string(union_str)
    code : str = tmpl.render(
        type_name = type_name, 
        nodes = nodes,
        handlers_name = handlers_name,
        line_format_string = line_format.to_string,
        is_vocab = is_vocab
    )
    return code 