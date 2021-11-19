from __future__ import annotations
from typing import Iterator, Optional

from gen.line_format import line_format, LineFormatHandlers, match_line_format
from gen.schema import ChildHandlers
from gen.production_instance import *


from lib import schema


from dataclasses import dataclass

# constructors for type instance

def is_inline(line_form : line_format) -> bool:
    return match_line_format(line_form, LineFormatHandlers[bool](
        case_InLine = lambda _ : True,
        case_NewLine = lambda _ : False, 
        case_IndentLine = lambda _ : False 
    ))

def next_indent_width(prev_iw : int, line_form : line_format) -> int:
    return match_line_format(line_form, LineFormatHandlers[int](
        case_InLine = lambda _ : prev_iw,
        case_NewLine = lambda _ : prev_iw, 
        case_IndentLine = lambda _ : prev_iw + 1 
    ))

def dump(schema_node_map : dict[str, schema.Node], instances : list[instance], indent : int = 4):

    @dataclass
    class Format:
        relation : str 
        depth : int 

    def dump_instance(inst : instance, format : Format) -> str:
        return match_instance(inst, InstanceHandlers[str](
            case_Grammar=lambda o : (
                indent_str := (' ' * format.depth * indent),
                relation_str := (' = .' + format.relation if (isinstance(format.relation, str)) else ''),
                (
                    indent_str + o.sequence_id + (' (' + o.nonterminal  + ')' if o.nonterminal != o.sequence_id else '') +
                    relation_str
                )
            )[-1],
            case_Vocab=lambda o : (
                indent_str := (' ' * format.depth * indent),
                relation_str := (' = .' + format.relation if (isinstance(format.relation, str)) else ''),
                (
                    indent_str + o.word + ' (' + o.choices_id  + ')' +
                    relation_str
                )
            )[-1]
        ))





    result_strs = [] 

    inst_iter = iter(instances)

    stack : list[Format] = [Format("", 0)]

    while stack:

        format : Format = stack.pop()
        inst = next(inst_iter)
        assert inst


        def format_grammar_children(inst : Grammar):
            nonlocal stack
            nonlocal format
            schema_node = schema_node_map[inst.sequence_id]
            def assert_not_terminal(c : schema.child):
                assert not isinstance(c, schema.Terminal)
                raise Exception()

            for child in reversed(schema_node.children):
                if not isinstance(child, schema.Terminal):
                    child_format = schema.match_child(child, ChildHandlers[Format](
                        case_Terminal=lambda o : (
                            assert_not_terminal(o)
                        ),
                        case_Nonterm=lambda o : (
                            Format(o.relation, format.depth + 1)
                        ),
                        case_Vocab=lambda o : (
                            Format(o.relation, format.depth + 1)
                        )
                    ))
                    stack += [child_format]

        def format_vocab_children(inst : Vocab):
            pass

        match_instance(inst, InstanceHandlers(
            case_Grammar = format_grammar_children,
            case_Vocab = format_vocab_children 
        ))

        result_strs += [dump_instance(inst, format)]

    return '\n'.join(result_strs)



def concretize(schema_node_map : dict[str, schema.Node], instances : list[instance]) -> str:

    @dataclass
    class Format:
        inline : bool 
        indent_width : int 

    result = ""

    inst_iter = iter(instances)

    stack : list[Union[str, Format]] = [Format(True, 0)] # str is concrete syntax, and int is indentation of the instance from the iterator 
    instance_count = 0

    while stack:


        stack_item : Union[str, Format] = stack.pop()
        if isinstance(stack_item, str):
            result += stack_item 
        else: 
            assert isinstance(stack_item, Format)
            format = stack_item
            # take an element from the iterator

            inst = next(inst_iter)
            assert inst
            instance_count += 1

            def concretize_grammar(inst : Grammar):
                nonlocal stack
                schema_node = schema_node_map[inst.sequence_id]
                for i, child in enumerate(reversed(schema_node.children)):
                    schema.match_child(child, ChildHandlers(
                        case_Terminal=lambda o : (
                            j := len(schema_node.children) - 1 - i,
                            prefix := (
                                (
                                    pred := schema_node.children[j - 1],
                                    match_line_format(pred.format, LineFormatHandlers[str](
                                        case_InLine = lambda _ : "",
                                        case_NewLine = lambda _ : "\n<NewLine>" + ("    " * format.indent_width),
                                        case_IndentLine = lambda _ : "\n<IndentLine>" + ("    " * format.indent_width)
                                    ))
                                    if isinstance(pred, schema.Nonterm) else ""
                                )[-1]
                                if j > 0 else "" 
                            ),
                            stack.append(prefix + o.terminal)
                        ),
                        case_Nonterm=lambda o : (
                            child_format := Format(is_inline(o.format), next_indent_width(format.indent_width, o.format)),
                            stack.append(child_format),
                        ),
                        case_Vocab=lambda o : (
                            stack.append(format)
                        )
                    ))

                prefix = "" if format.inline else "\n" + "    " * format.indent_width
                stack += [prefix]
            
            def concretize_vocab(inst : Vocab):
                nonlocal stack
                stack += [inst.word]


            match_instance(inst, InstanceHandlers(
                case_Grammar = concretize_grammar,
                case_Vocab = concretize_vocab
            ))

    return result