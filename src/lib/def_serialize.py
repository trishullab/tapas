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
from lib.generic_instance import instance, InstanceHandlers
from lib import generic_instance as inst 
from gen.python_ast import *
from gen.line_format import InLine, NewLine, IndentLine
"""

intersection_str = """
def serialize_{{ node.name }}(
    o : {{ node.name }}, depth : int = 0, alias : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[instance]:
    return (
        [inst.make_Node(
            lhs = '{{ node.name }}',
            rhs = '{{ node.name }}',
            depth = depth,
            alias = alias,
            indent_width = indent_width,
            inline = inline
        )] +
{% for child in node.children %}
{% if child.typ == "str" %}
        [inst.make_Symbol(o.{{ child.attr }}, depth + 1, "{{ child.attr }}")] +
{% else %}
        serialize_{{ child.typ }}(o.{{ child.attr }}, depth + 1, "{{ child.attr }}", 
            inst.next_indent_width(indent_width,  {{ line_format_string(child.line_form) }}),
            {{ "True" if line_format_string(child.line_form) == "InLine()" else "False"  }},
        ) +
{% endif %}
{% endfor %}
        []
    )
"""

def generate_intersection_def(
    node : schema.Node 
) -> str:
    
    tmpl = jinja_env.from_string(intersection_str)
    code : str = tmpl.render(
        node = node,
        line_format_string = line_format.to_string
    )
    return code 


union_str = """
def serialize_{{ type_name }}(
    o : {{ type_name }}, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[instance]:
    return match_{{ type_name }}(o, {{ handlers_name }}[list[instance]](
{% for node in nodes %}
        case_{{ node.name }} = lambda o : (
            [inst.make_Node(
                lhs = '{{ type_name }}',
                rhs = '{{ node.name }}',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
{% for child in node.children %}
{% if child.typ == "str" %}
            [inst.make_Symbol(o.{{ child.attr }}, depth + 1, "{{ child.attr }}")] +
{% else %}
            serialize_{{ child.typ }}(o.{{ child.attr }}, depth + 1, "{{ child.attr }}", 
                inst.next_indent_width(indent_width, {{ line_format_string(child.line_form) }}),
                {{ "True" if line_format_string(child.line_form) == "InLine()" else "False"  }},
            ) + 
{% endif %}
{% endfor %}
            []
        ){% if not loop.last %},{% endif %}

{% endfor %}
    ))
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
        line_format_string = line_format.to_string
    )
    return code 