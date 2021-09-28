from __future__ import annotations
from typing import Iterator

from gen.line_format import line_format, LineFormatHandlers, match_line_format
from lib import schema


from dataclasses import dataclass

# constructors for type instance

@dataclass
class Node:
    lhs : str
    rhs : str
    depth : int
    alias : str
    indent_width : int
    inline : bool


def next_indent_width(prev_iw : int, line_form : line_format) -> int:
    return match_line_format(line_form, LineFormatHandlers[int](
        case_InLine = lambda _ : prev_iw,
        case_NewLine = lambda _ : prev_iw, 
        case_IndentLine = lambda _ : prev_iw + 1 
    ))

def dump(instance_nodes : list[Node], indent : int = 4):
    strs = [
        (
            # node := schema_node_map[inst_node.rhs],
            indent_str := (' ' * inst_node.depth * indent),
            alias_str := (' = .' + inst_node.alias if (isinstance(inst_node.alias, str)) else ''),
            (
                indent_str + inst_node.rhs + (' (' + inst_node.lhs  + ')' if inst_node.lhs != inst_node.rhs else '') +
                alias_str
            )
        )[-1]
            # case_Symbol= lambda o : (
            #     indent_str := (' ' * o.depth * indent),
            #     alias_str := (' = .' + o.alias if (isinstance(o.alias, str)) else ''),
            #     (
            #         indent_str + "Symbol " + o.content + alias_str
            #     )
            # )[-1]
        for inst_node in instance_nodes 
    ]
    return '\n'.join(strs)


def concretize(schema_node_map : dict[str, schema.Node], instance_nodes : list[Node]) -> str:

    inst_node_iter = iter(instance_nodes)

    def concretize_children(parent : Node, children : list[schema.Child]) -> str:
        if children:
            child = children[-1]
            s = concretize_instances()
            follower = (
                match_line_format(child.line_form, LineFormatHandlers[str](
                    case_InLine = lambda _ : "",
                    case_NewLine = lambda _ : "\n" + "    " * parent.indent_width,
                    case_IndentLine = lambda _ : "\n" + "    " * parent.indent_width
                )) + child.follower
                if child.follower else

                ""
            )
            suffix = concretize_children(parent, children[:-1])
            return s + follower + suffix
        else:
            return ""

    def concretize_instances() -> str:
        inst_node = next(inst_node_iter)
        if (inst_node):
            if inst_node.lhs == "symbol":
                return inst_node.rhs
            else:
                schema_node = schema_node_map[inst_node.rhs]
                prefix = "" if inst_node.inline else "\n" + "    " * inst_node.indent_width
                return prefix + schema_node.leader + concretize_children(inst_node, schema_node.children[::-1])
        else:
            return ""

    return concretize_instances()




