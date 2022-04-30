from __future__ import annotations
from typing import Iterator, Optional

from numpy import isin

from lib.line_format_construct_autogen import line_format, LineFormatHandlers, match_line_format
from lib.rule_construct_autogen import ItemHandlers, Terminal
from lib.abstract_token_construct_autogen import *

from lib.rule_system import Rule
import lib.rule_system


from dataclasses import dataclass

def from_primitive(ptok : list[str]) -> abstract_token:
    assert len(ptok) == 4
    assert ptok[0] == "P"
    if ptok[1] == "grammar":
        return make_Grammar(ptok[2], ptok[3])
    else:
        assert ptok[1] == "vocab"
        return make_Vocab(ptok[2], ptok[3])


def raise_exception(e):
    raise e

def to_primitive(inst : abstract_token) -> list[str]:
    return match_abstract_token(inst, AbstractTokenHandlers[list[str]](
        case_Grammar=lambda o : (
            ["P", "grammar", o.options, o.selection]
        ),
        case_Vocab=lambda o : (
            ["P", "vocab", o.options, o.selection]
        ),
        case_Hole=lambda o : ["H"]
    )) 

def to_string(token : abstract_token) -> str:
    return match_abstract_token(token, AbstractTokenHandlers[str](
        case_Grammar= lambda g : f"grammar: {g.selection} <{g.options}>",
        case_Vocab= lambda v : f"vocab: {v.selection} <{v.options}>",
        case_Hole= lambda v : f"hole",
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
            )[-1],
            case_Hole=lambda o : (
                indent_str := (' ' * format.depth * indent),
                relation_str := (' = .' + format.relation if (isinstance(format.relation, str)) else ''),
                (
                    indent_str + 'HOLE' + 
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
            def assert_not_terminal(c : lib.rule_system.item):
                assert not isinstance(c, lib.rule_system.Terminal)
                raise Exception()

            for item in reversed(rule.content):
                if not isinstance(item, lib.rule_system.Terminal):
                    child_format = lib.rule_system.match_item(item, ItemHandlers[Format](
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

        def format_hole_children(inst : Hole):
            pass

        match_abstract_token(inst, AbstractTokenHandlers(
            case_Grammar = format_grammar_children,
            case_Vocab = format_vocab_children, 
            case_Hole = format_hole_children,
        ))

        result_strs += [dump_abstract_token(inst, format)]

    return '\n'.join(result_strs)


from lib import rule_system as rs
def concretize(rule_map : dict[str, Rule], abstract_tokens : tuple[abstract_token, ...]) -> str:

    @dataclass
    class Format:
        inline : bool 
        indent_width : int 

    token_iter = iter(abstract_tokens)
    first_token = next(token_iter)
    assert isinstance(first_token, Grammar)
    stack : list[tuple[Format, Grammar, tuple[str, ...]]] = [(Format(True, 0), first_token, ())]

    stack_result : str | None = None 
    while stack:

        (format, token, children) = stack.pop()

        if stack_result != None:
            # get the result from the child in the stack
            children = children + (stack_result,) 
            stack_result = None

        rule = rule_map[token.selection]
        index = len(children)
        if index == len(rule.content):
            prefix = "" if format.inline else "\n" + "    " * format.indent_width
            stack_result = prefix + "".join(children)

        else:
            item = rule.content[index]

            if isinstance(item, rs.Nonterm):
                child_token = next(token_iter, None)

                stack.append((format, token, children))
                child_format = Format(is_inline(item.format), next_indent_width(format.indent_width, item.format))
                if isinstance(child_token, Grammar):
                    stack.append((child_format, child_token, ()))
                else:
                    break

            elif isinstance(item, rs.Vocab):
                vocab_token = next(token_iter, None)
                if isinstance(vocab_token, Vocab):
                    stack.append((format, token, children + (vocab_token.selection,)))
                else:
                    break

            elif isinstance(item, rs.Terminal):
                prefix = (
                    (
                        pred := rule.content[index - 1],
                        match_line_format(pred.format, LineFormatHandlers[str](
                            case_InLine = lambda _ : "",
                            case_NewLine = lambda _ : "\n" + ("    " * format.indent_width),
                            case_IndentLine = lambda _ : "\n" + ("    " * format.indent_width)
                        ))
                        if isinstance(pred, lib.rule_system.Nonterm) else ""
                    )[-1]
                    if index != 0 and index == len(rule.content) - 1 else "" 
                )
                s = (prefix + item.terminal)
                stack.append((format, token, children + (s,)))



    # if stack is not empty, then input program must be incomplete
    # so clean up the stack
    while stack:
        (format, token, children) = stack.pop()

        if stack_result != None:
            # get the result from the child in the stack
            children = children + (stack_result,) 


        if children:
            rule = rule_map[token.selection]
            prefix = "" if format.inline else "\n" + "    " * format.indent_width
            stack_result = prefix + "".join(children)
        else:
            stack_result = None

    assert stack_result
    return stack_result

# def concretize(rule_map : dict[str, Rule], abstract_tokens : tuple[abstract_token, ...]) -> str:

#     @dataclass
#     class Format:
#         inline : bool 
#         indent_width : int 

#     result = ""

#     token_iter = iter(abstract_tokens)

#     stack : list[Union[str, Format]] = [Format(True, 0)] # str is concrete syntax, and int is indentation of the abstract_token from the iterator 
#     abstract_token_count = 0

#     while stack:

#         stack_item : Union[str, Format] = stack.pop()
#         if isinstance(stack_item, str):
#             result += stack_item 
#         else: 
#             assert isinstance(stack_item, Format)
#             format = stack_item

#             # take an element from the iterator
#             inst = next(token_iter, None)
#             if not inst:
#                 break

#             abstract_token_count += 1

#             def concretize_grammar(inst : Grammar):
#                 nonlocal stack
#                 rule = rule_map[inst.selection]
#                 for i, item in enumerate(reversed(rule.content)):
#                     lib.rule_system.match_item(item, ItemHandlers(
#                         case_Terminal=lambda o : (
#                             j := len(rule.content) - 1 - i,
#                             prefix := (
#                                 (
#                                     pred := rule.content[j - 1],
#                                     match_line_format(pred.format, LineFormatHandlers[str](
#                                         case_InLine = lambda _ : "",
#                                         case_NewLine = lambda _ : "\n" + ("    " * format.indent_width),
#                                         case_IndentLine = lambda _ : "\n" + ("    " * format.indent_width)
#                                     ))
#                                     if isinstance(pred, lib.rule_system.Nonterm) else ""
#                                 )[-1]
#                                 if i == 0 else "" 
#                             ),
#                             stack.append(prefix + o.terminal)
#                         ),
#                         case_Nonterm=lambda o : (
#                             child_format := Format(is_inline(o.format), next_indent_width(format.indent_width, o.format)),
#                             stack.append(child_format),
#                         ),
#                         case_Vocab=lambda o : (
#                             stack.append(format)
#                         )
#                     ))

#                 prefix = "" if format.inline else "\n" + "    " * format.indent_width
#                 stack += [prefix]
            
#             def concretize_vocab(inst : Vocab):
#                 nonlocal stack
#                 stack += [inst.selection]

#             def concretize_hole(_ : Hole):
#                 nonlocal stack
#                 stack += ['(HOLE)']


#             match_abstract_token(inst, AbstractTokenHandlers(
#                 case_Grammar = concretize_grammar,
#                 case_Vocab = concretize_vocab,
#                 case_Hole = concretize_hole,
#             ))

#     return result


from typing import Sequence
def truncate_at_hole(toks : Sequence[abstract_token]) -> Sequence[abstract_token]:
    hole_index = next((i for i, t in enumerate(toks) if isinstance(t, Hole)), None) 
    if hole_index:
        return toks[0:hole_index]
    else:
        return toks


