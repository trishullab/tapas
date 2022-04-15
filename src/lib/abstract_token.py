from __future__ import annotations
from typing import Iterator, Optional

from lib.line_format_construct_autogen import line_format, LineFormatHandlers, match_line_format
from lib.rule_construct_autogen import ItemHandlers
from lib.abstract_token_construct_autogen import *

from lib.rule import Rule
import lib.rule


from dataclasses import dataclass

def to_primitive(inst : abstract_token) -> list[str]:
    return match_abstract_token(inst, AbstractTokenHandlers[list[str]](
        case_Grammar=lambda o : (
            ["P", "grammar", o.options, o.selection]
        ),
        case_Vocab=lambda o : (
            ["P", "vocab", o.options, o.selection]
        )
    )) 

def from_primitive(prim : list[str]) -> abstract_token:
    assert len(prim) == 4
    assert prim[0] == "P"
    if prim[1] == "grammar":
        return Grammar(options=prim[2], selection=prim[3])
    elif prim[1] == "vocab":
        return Vocab(options=prim[2], selection=prim[3])
    else:
        assert False



def to_string(token : abstract_token) -> str:
    return match_abstract_token(token, AbstractTokenHandlers[str](
        case_Grammar= lambda g : f"grammar: {g.selection} <{g.options}>",
        case_Vocab= lambda v : f"vocab: {v.selection} <{v.options}>"
    ))


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

def dump(rule_map : dict[str, Rule], abstract_tokens : tuple[abstract_token, ...], indent : int = 4):

    @dataclass
    class Format:
        relation : str 
        depth : int 

    def dump_abstract_token(inst : abstract_token, format : Format) -> str:
        return match_abstract_token(inst, AbstractTokenHandlers[str](
            case_Grammar=lambda o : (
                indent_str := (' ' * format.depth * indent),
                relation_str := (' = .' + format.relation if (isinstance(format.relation, str)) else ''),
                (
                    indent_str + o.selection + (' (' + o.options  + ')' if o.options != o.selection else '') +
                    relation_str
                )
            )[-1],
            case_Vocab=lambda o : (
                indent_str := (' ' * format.depth * indent),
                relation_str := (' = .' + format.relation if (isinstance(format.relation, str)) else ''),
                (
                    indent_str + o.selection + ' (' + o.options  + ')' +
                    relation_str
                )
            )[-1]
        ))





    result_strs = [] 

    inst_iter = iter(abstract_tokens)

    stack : list[Format] = [Format("", 0)]

    while stack:

        format : Format = stack.pop()
        inst = next(inst_iter)
        assert inst


        def format_grammar_children(inst : Grammar):
            nonlocal stack
            nonlocal format
            rule = rule_map[inst.selection]
            def assert_not_terminal(c : lib.rule.item):
                assert not isinstance(c, lib.rule.Terminal)
                raise Exception()

            for item in reversed(rule.content):
                if not isinstance(item, lib.rule.Terminal):
                    child_format = lib.rule.match_item(item, ItemHandlers[Format](
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

        match_abstract_token(inst, AbstractTokenHandlers(
            case_Grammar = format_grammar_children,
            case_Vocab = format_vocab_children 
        ))

        result_strs += [dump_abstract_token(inst, format)]

    return '\n'.join(result_strs)



def concretize(rule_map : dict[str, Rule], abstract_tokens : tuple[abstract_token, ...]) -> str:

    @dataclass
    class Format:
        inline : bool 
        indent_width : int 

    result = ""

    inst_iter = iter(abstract_tokens)

    stack : list[Union[str, Format]] = [Format(True, 0)] # str is concrete syntax, and int is indentation of the abstract_token from the iterator 
    abstract_token_count = 0

    while stack:

        stack_item : Union[str, Format] = stack.pop()
        if isinstance(stack_item, str):
            result += stack_item 
        else: 
            assert isinstance(stack_item, Format)
            format = stack_item

            # take an element from the iterator
            inst = next(inst_iter, None)
            if not inst:
                break

            abstract_token_count += 1

            def concretize_grammar(inst : Grammar):
                nonlocal stack
                rule = rule_map[inst.selection]
                for i, item in enumerate(reversed(rule.content)):
                    lib.rule.match_item(item, ItemHandlers(
                        case_Terminal=lambda o : (
                            j := len(rule.content) - 1 - i,
                            prefix := (
                                (
                                    pred := rule.content[j - 1],
                                    match_line_format(pred.format, LineFormatHandlers[str](
                                        case_InLine = lambda _ : "",
                                        case_NewLine = lambda _ : "\n" + ("    " * format.indent_width),
                                        case_IndentLine = lambda _ : "\n" + ("    " * format.indent_width)
                                    ))
                                    if isinstance(pred, lib.rule.Nonterm) else ""
                                )[-1]
                                if i == 0 else "" 
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
                stack += [inst.selection]


            match_abstract_token(inst, AbstractTokenHandlers(
                case_Grammar = concretize_grammar,
                case_Vocab = concretize_vocab
            ))

    return result



