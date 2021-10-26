from __future__ import annotations

from dataclasses import dataclass

import inflection
import jinja2

from lib import schema
from lib import line_format

jinja_env = jinja2.Environment(trim_blocks=True)
# jinja_env.globals.update(isinstance=isinstance)

# When local and global keywords are seen, copy renaming entry to local renaming. 
# When identifier is used in assignment target or expression, look up renaming in local map or create a new renaming entry

# if context is class or params, add reflexive (A -> A) renaming to the local map

# collect all function def identifiers to pass into local scope of all nested scopes. 

# create stack machine that places target and its children as a row on stack, with flag to indicate if a child has been processed

# use type inference in order to rename class field names and function parameter names
# generate `if isinstance` condition switch for each type that is inferred, if there is more than one type inferred

header = """
from __future__ import annotations
from lib import production_instance as prod_inst 
from gen.python_ast import *
from gen.line_format import InLine, NewLine, IndentLine
"""



intersection_str = """
def rename_{{ node.name }}(
    o : {{ node.name }}, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> {{ node.name }}:

    return {{ node.name }}(
{% for child in node.children %}
{% if is_vocab(child) %}
        o.{{ child.relation }}{% if not loop.last %}, {% endif %}
{% else %}
        rename_{{ child.nonterminal }}(
            o.{{ child.relation }},
            global_map,
            nonlocal_map,
            local_map
        ){% if not loop.last %}, {% endif %}
{% endif %}
{% endfor %}
    )

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
def rename_{{ type_name }}(
    o : {{ type_name }}, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> {{ type_name }}:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[{{ type_name }}, int]] = [(o, -1)]
    result : {{ type_name }} = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 
{% for node in nodes %}

        def handle_{{ node.name }}(o : {{ node.name }}): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
{% for child in filter_recursion_children(node.children) %}
                "{{ child.relation }}"{% if not loop.last %},
{% endif %}

{% endfor %}
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
{% for site_child in filter_recursion_children(node.children) %}
                elif recursion_sites[recursion_site] == "{{ site_child.relation }}":
                    stack.append(({{ node.name }}(
{% for arg_child in node.children %}
{% if arg_child.relation == site_child.relation %}
                        result{% if not loop.last %}, {% endif %}
{% else %}
                        o.{{ arg_child.relation }}{% if not loop.last %}, {% endif %}{% endif %}
{% endfor %}{# end child arguments #}
                    ), recursion_site + 1))
{% endfor %}{# end recursion sites #}



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
{% for site_child in filter_recursion_children(node.children) %}
                elif recursion_sites[recursion_site + 1] == "{{ site_child.relation }}":
                    stack.append((o.{{ site_child.relation }}, recursion_site + 1))
{% endfor %} {# end recursion site conditions #}


{% endfor %} {# end node function defs #}


        match_{{ type_name }}(o, {{ handlers_name }}(
{% for node in nodes %}
            case_{{ node.name }} = handle_{{ node.name }}{% if not loop.last %}, {% endif %} 
{% endfor %} {# end node cases #}
        ))
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
        is_vocab = is_vocab,
        filter_recursion_children = lambda children : [child for child in children if isinstance(child, schema.Grammar) and type_name == child.nonterminal]
    )
    return code 