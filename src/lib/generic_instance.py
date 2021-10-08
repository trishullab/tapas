from __future__ import annotations
from typing import Iterator, Optional

from gen.line_format import line_format, LineFormatHandlers, match_line_format
from lib import schema


from dataclasses import dataclass

# constructors for type instance

@dataclass
class Node:
    lhs : str
    rhs : str
    depth : int
    relation : str
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
            indent_str := (' ' * inst_node.depth * indent),
            relation_str := (' = .' + inst_node.relation if (isinstance(inst_node.relation, str)) else ''),
            (
                indent_str + inst_node.rhs + (' (' + inst_node.lhs  + ')' if inst_node.lhs != inst_node.rhs else '') +
                relation_str
            )
        )[-1]
        for inst_node in instance_nodes 
    ]
    return '\n'.join(strs)


def concretize(schema_node_map : dict[str, schema.Node], instance_nodes : list[Node]) -> str:

    result = ""

    inst_node_iter = iter(instance_nodes)

    stack : list[Optional[str]] = [None] # None indicates to take a new node from the iterator

    while stack:

        syntax_part : Optional[str] = stack.pop()
        if isinstance(syntax_part, str):
            result += syntax_part 
        else: 
            # take an element from the iterator
            inst_node = next(inst_node_iter)
            if inst_node:
                if inst_node.lhs == "symbol":
                    stack += [inst_node.rhs]
                else:
                    # add follower syntax of children to the stack
                    schema_node = schema_node_map[inst_node.rhs]
                    for child in reversed(schema_node.children):
                        follower = (
                            (match_line_format(child.line_form, LineFormatHandlers[str](
                                case_InLine = lambda _ : "",
                                case_NewLine = lambda _ : "\n" + "    " * inst_node.indent_width,
                                case_IndentLine = lambda _ : "\n" + "    " * inst_node.indent_width
                            )) + child.follower)
                            if child.follower else

                            ""
                        )
                        stack += [follower, None]

                    prefix = "" if inst_node.inline else "\n" + "    " * inst_node.indent_width
                    stack += [prefix + schema_node.leader]
            else:
                assert False

    return result