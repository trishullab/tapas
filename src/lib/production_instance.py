from __future__ import annotations
from typing import Iterator, Optional

from gen.line_format import line_format, LineFormatHandlers, match_line_format
from gen.schema import ChildHandlers
from gen.production_instance import *


from lib import schema


from dataclasses import dataclass

# constructors for type instance

def next_indent_width(prev_iw : int, line_form : line_format) -> int:
    return match_line_format(line_form, LineFormatHandlers[int](
        case_InLine = lambda _ : prev_iw,
        case_NewLine = lambda _ : prev_iw, 
        case_IndentLine = lambda _ : prev_iw + 1 
    ))

def dump(instances : list[instance], indent : int = 4):

    def dump_instance(inst : instance) -> str:
        return match_instance(inst, InstanceHandlers[str](
            case_Grammar=lambda o : (
                indent_str := (' ' * o.depth * indent),
                relation_str := (' = .' + o.relation if (isinstance(o.relation, str)) else ''),
                (
                    indent_str + o.sequence_id + (' (' + o.nonterminal  + ')' if o.nonterminal != o.sequence_id else '') +
                    relation_str
                )
            )[-1],
            case_Vocab=lambda o : (
                indent_str := (' ' * o.depth * indent),
                relation_str := (' = .' + o.relation if (isinstance(o.relation, str)) else ''),
                (
                    indent_str + o.word + ' (' + o.choices_id  + ')' +
                    relation_str
                )
            )[-1]
        ))

    strs = [
        dump_instance(inst)
        for inst in instances 
    ]
    return '\n'.join(strs)


def concretize(schema_node_map : dict[str, schema.Node], instances : list[instance]) -> str:

    result = ""

    inst_iter = iter(instances)

    stack : list[Optional[str]] = [None] # None indicates to take a new node from the iterator

    while stack:

        syntax_part : Optional[str] = stack.pop()
        if isinstance(syntax_part, str):
            result += syntax_part 
        else: 
            # take an element from the iterator
            inst = next(inst_iter)
            assert inst

            def concretize_grammar(inst : Grammar):
                nonlocal stack
                schema_node = schema_node_map[inst.sequence_id]
                for child in reversed(schema_node.children):
                    follower = schema.match_child(child, ChildHandlers[str](
                        case_Grammar=lambda o : (
                            (
                                (match_line_format(o.format, LineFormatHandlers[str](
                                    case_InLine = lambda _ : "",
                                    case_NewLine = lambda _ : "\n" + "    " * inst.indent_width,
                                    case_IndentLine = lambda _ : "\n" + "    " * inst.indent_width
                                )) + o.follower)
                                if o.follower else

                                ""
                            )

                        ),
                        case_Vocab=lambda o : (
                            ""
                        )
                    ))
                    stack += [follower, None]

                prefix = "" if inst.inline else "\n" + "    " * inst.indent_width
                stack += [prefix + schema_node.leader]
            
            def concretize_vocab(inst : Vocab):
                nonlocal stack
                stack += [inst.word]


            match_instance(inst, InstanceHandlers(
                case_Grammar = concretize_grammar,
                case_Vocab = concretize_vocab
            ))

    return result