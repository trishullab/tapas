from __future__ import annotations

from lib import abstract_token_system as ats
from lib.abstract_token_construct_autogen import Grammar 
from lib.abstract_token_system import abstract_token 
from lib.generic_tree_system import GenericNode
from lib import python_ast_parse
from lib import python_generic_tree_system as pgs
from lib import python_abstract_token_system as pats

from lib import python_ast_serialize_autogen
from lib import python_ast_reconstitute_autogen 
from lib.python_ast_construct_autogen import * 

def parse_from_generic_tree(gnode : GenericNode) -> module:
    return python_ast_parse.from_generic_tree(gnode)

def parse(concrete : str) -> module:
    gnode = pgs.parse(concrete)
    return python_ast_parse.from_generic_tree(gnode)

def serialize(mod : module) -> tuple[abstract_token, ...]:
    toks = python_ast_serialize_autogen.from_module(mod)
    if isinstance(toks[-1], ats.Hole):
        return toks[:-1]
    else:
        return toks

def reconstitute(xs : tuple[abstract_token, ...]) -> module:
    return python_ast_reconstitute_autogen.to_module(tuple([x for x in reversed(xs)]))[0] 

def reconstitute_expr(xs : list[abstract_token]) -> expr:
    return python_ast_reconstitute_autogen.to_expr(tuple([x for x in reversed(xs)]))[0] 

def concretize(mod: module) -> str:
    seq = serialize(mod)
    return pats.concretize(seq)

def dump(mod: module) -> str:
    seq = serialize(mod)
    return pats.dump(seq)

def assert_serialize_reconstitute_bidirectional(mod: module):
    seq = serialize(mod)
    mod_result = reconstitute(seq)
    assert mod == mod_result

def assert_concretize_parse_bidrectional(mod: module):
    concrete = concretize(mod)
    mod_result = parse(concrete)
    assert mod == mod_result


def from_cmp_rator_to_method_name(ur : cmp_rator) -> str:
    return match_cmp_rator(ur, CmpRatorHandlers[str](
        case_Eq = lambda _: "__eq__",
        case_NotEq = lambda _: "__ne__",
        case_Lt = lambda _: "__lt__",
        case_LtE = lambda _: "__le__",
        case_Gt = lambda _: "__gt__",
        case_GtE = lambda _: "__ge__",
        case_Is = lambda _: "__eq__",
        case_IsNot = lambda _: "__ne__",
        case_In = lambda _: "__contains__",
        case_NotIn = lambda _: "__missing__",
    ))

def from_unary_rator_to_method_name(ur : unary_rator) -> str:
    return match_unary_rator(ur, UnaryRatorHandlers[str](
        case_Invert = lambda _: "__invert__",
        case_Not = lambda _: "__not__",
        case_UAdd = lambda _: "__pos__",
        case_USub = lambda _: "__neg__",
    ))

def from_bin_rator_to_method_name(br : bin_rator) -> str:
    return match_bin_rator(br, BinRatorHandlers[str](
        case_Add = lambda _: "__add__",
        case_Sub = lambda _: "__sub__",
        case_Mult = lambda _: "__mul__",
        case_MatMult = lambda _: "__matmul__",
        case_Div = lambda _: "__truediv__",
        case_Mod = lambda _: "__mod__",
        case_Pow = lambda _: "__pow__",
        case_LShift = lambda _: "__lshift__",
        case_RShift = lambda _: "__rshift__",
        case_BitOr = lambda _: "__or__",
        case_BitXor = lambda _: "__xor__",
        case_BitAnd = lambda _: "__and__",
        case_FloorDiv = lambda _: "__floordiv__",
    ))

def from_bin_rator_to_aug_method_name(br : bin_rator) -> str:
    return match_bin_rator(br, BinRatorHandlers[str](
        case_Add = lambda _: "__iadd__",
        case_Sub = lambda _: "__isub__",
        case_Mult = lambda _: "__imul__",
        case_MatMult = lambda _: "__imatmul__",
        case_Div = lambda _: "__itruediv__",
        case_Mod = lambda _: "__imod__",
        case_Pow = lambda _: "__ipow__",
        case_LShift = lambda _: "__ilshift__",
        case_RShift = lambda _: "__irshift__",
        case_BitOr = lambda _: "__ior__",
        case_BitXor = lambda _: "__ixor__",
        case_BitAnd = lambda _: "__iand__",
        case_FloorDiv = lambda _: "__ifloordiv__",
    ))

def truncate(code : str, k : float) -> str:
    ast = parse(code)
    toks = serialize(ast)
    
    l = len(toks)
    end : int = int(
        l * k
        if 0 <= k < 1 else
        l
        if k < 0 else
        min(k,l)
    ) 
    toks = toks[0:end]
    l = len(toks)
    end : int = int(next(
        l - 1 - j 
        for j, tok in enumerate(reversed(toks))
        if isinstance(tok, Grammar) and tok.options == "statements"
    ))
    toks = toks[0:end]

    result = pats.concretize(toks)
    return result 
