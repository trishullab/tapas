from __future__ import annotations

from dataclasses import dataclass

import inflection
import jinja2

import lib.rule 
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



single_str = """
def rename_{{ rule.name }}(
    o : {{ rule.name }}, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> {{ rule.name }}:

    return {{ rule.name }}(
{% for child in rule.children %}
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


def is_vocab(o : lib.rule.item):
    return isinstance(o, lib.rule.Vocab)

def generate_single_def(
    rule : lib.rule.Rule 
) -> str:
    
    tmpl = jinja_env.from_string(single_str)
    code : str = tmpl.render(
        rule = rule,
        line_format_string = line_format.to_string,
        is_vocab = is_vocab
    )
    return code 


choice_str = """
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

{% for rule in rules %}
        def handle_{{ rule.name }}(partial_result : {{ rule.name }}): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site

{% set inductive_children = filter_inductive_children(rule.children) %}

            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
{% for each_site in range(0, inductive_children|length) %}
            elif recursion_site == {{ each_site }}:
                next_partial_result = {{ rule.name }}(
{% for arg_child in rule.children %}
{% if arg_child.relation == inductive_children[each_site].relation %}
                    result{% if not loop.last %},
{% endif %}
{% else %}
                    partial_result.{{ arg_child.relation }}{% if not loop.last %},
{% endif %}
{% endif %}
{% endfor %}{# end child arguments #}

                )
{% endfor %}{# end recursion sites #}

            # update the stack with the rule at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= {{ inductive_children|length }}:
                result = next_partial_result
{% for each_site in range(0, inductive_children|length)|reverse %}
            elif recursion_site + 1 == {{ each_site }}:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.{{ inductive_children[each_site].relation }}, -1))
{% endfor %} {# end recursion site conditions #}


{% endfor %} {# end rule function defs #}


        match_{{ type_name }}(partial_result, {{ handlers_name }}(
{% for rule in rules %}
            case_{{ rule.name }} = handle_{{ rule.name }}{% if not loop.last %}, {% endif %} 
{% endfor %} {# end rule cases #}
        ))
    return result


"""

def generate_choice_def(
    type_name : str,
    rules : list[lib.rule.Rule] 
) -> str:
    handlers_name = f"{inflection.camelize(type_name)}Handlers"

    tmpl = jinja_env.from_string(choice_str)
    code : str = tmpl.render(
        type_name = type_name, 
        rules = rules,
        handlers_name = handlers_name,
        line_format_string = line_format.to_string,
        is_vocab = is_vocab,
        filter_inductive_children = lambda children : [child for child in children if isinstance(child, lib.rule.Nonterm) and type_name == child.nonterminal]
    )
    return code 