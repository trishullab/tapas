from __future__ import annotations
from typing import Iterator
from gen.line_format import line_format, LineFormatHandlers, match_line_format

from gen.production import *

import schema

def next_indent_width(prev_iw : int, line_form : line_format) -> int:
    return match_line_format(line_form, LineFormatHandlers[int](
        case_InLine = lambda _ : prev_iw,
        case_NewLine = lambda _ : prev_iw, 
        case_IndentLine = lambda _ : prev_iw + 1 
    ))

def dump(schema_node_map : dict[str, schema.Node], prods : list[production], indent : int = 4):
    strs = [
        match_production(prod, ProductionHandlers[str](
            case_Node = lambda o : (
                node := schema_node_map[o.rhs],
                indent_str := (' ' * o.depth * indent),
                alias_str := (' = .' + o.alias if (isinstance(o.alias, str)) else ''),
                (
                    indent_str + o.rhs + (' (' + o.lhs  + ')' if o.lhs != o.rhs else '') +
                    alias_str
                )
            )[-1],
            case_Symbol= lambda o : (
                indent_str := (' ' * o.depth * indent),
                alias_str := (' = .' + o.alias if (isinstance(o.alias, str)) else ''),
                (
                    indent_str + "Symbol " + o.content + alias_str
                )
            )[-1]
        ))
        for prod in prods
    ]
    return '\n'.join(strs)


def concretize(schema_node_map : dict[str, schema.Node], prods : list[production]) -> str:

    prod_iter = iter(prods)

    def concretize_children(parent : Node, children : list[schema.Child]) -> str:
        if children:
            child = children[-1]
            s = concretize_prods()
            follower = match_line_format(child.line_form, LineFormatHandlers[str](
                case_InLine = lambda _ : "",
                case_NewLine = lambda _ : "\n" + "    " * parent.indent_width,
                case_IndentLine = lambda _ : "\n" + "    " * parent.indent_width
            )) + child.follower
            suffix = concretize_children(parent, children[:-1])
            return s + follower + suffix
        else:
            return ""

    def concretize_prods() -> str:
        prod = next(prod_iter)
        if (prod):
            return match_production(prod, ProductionHandlers[str](
                case_Node = lambda o : (
                    schema_node := schema_node_map[o.rhs],
                    prefix := "" if o.inline else "\n" + "    " * o.indent_width,
                    prefix + schema_node.leader + concretize_children(o, schema_node.children[::-1])
                )[-1],
                case_Symbol= lambda o : (
                    o.content
                )
            ))
        else:
            return ""

    return concretize_prods()




