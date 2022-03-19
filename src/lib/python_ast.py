from __future__ import annotations

from lib import python_ast_serialize_autogen
from lib import python_ast_reconstitute_autogen 
from lib.python_ast_construct_autogen import * 
from lib.abstract_token_construct_autogen import abstract_token 
from lib.generic_tree import GenericNode
from lib import python_ast_parse
from lib import python_generic_tree
from lib import python_abstract_token

from pyrsistent import m 
from pyrsistent.typing import PMap, PSet

from lib.python_ast_parse import Unsupported, ConcreteParsingError


def parse_from_generic_tree(gnode : GenericNode) -> module:
    return python_ast_parse.from_generic_tree(gnode)

def parse(concrete : str) -> module:
    gnode = python_generic_tree.parse(concrete)
    return python_ast_parse.from_generic_tree(gnode)

def serialize(mod : module) -> tuple[abstract_token, ...]:
    return python_ast_serialize_autogen.from_module(mod)

def reconstitute(xs : tuple[abstract_token, ...]) -> module:
    return python_ast_reconstitute_autogen.to_module(tuple([x for x in reversed(xs)]))[0] 

def reconstitute_expr(xs : list[abstract_token]) -> expr:
    return python_ast_reconstitute_autogen.to_expr(tuple([x for x in reversed(xs)]))[0] 

def concretize(mod: module) -> str:
    seq = serialize(mod)
    return python_abstract_token.concretize(seq)

def dump(mod: module) -> str:
    seq = serialize(mod)
    return python_abstract_token.dump(seq)

def assert_serialize_reconstitute_bidirectional(mod: module):
    seq = serialize(mod)
    mod_result = reconstitute(seq)
    assert mod == mod_result

def assert_concretize_parse_bidrectional(mod: module):
    concrete = concretize(mod)
    mod_result = parse(concrete)
    assert mod == mod_result



# TODO FUTURE: implement to generate PMap[str, Typ]
# def unify(target : expr, source : typ) -> PMap[str, typ]:
#     # TODO: just have cases for target patterns; accumulate PMap result 

#     result : PMap = m() 
#     stack : list[tuple[expr, expr]] = [(target, source)]
#     while stack:
#         (target, source) = stack.pop()

#         # isinstance(target, Name):
#         # isinstance(target, List)
#         # isinstance(target, EmptyList)
#         # isinstance(target, Tuple)
#         # isinstance(target, EmptyTuple)

#     raise NotImplementedError()


# Stack machine template:
#
# def from_expr(
#     o : expr
# ) -> list[abstract_token]:

#     result = []
#     stack : list[Union[expr, list[abstract_token]]] = [o]
#     while stack:
#         stack_item = stack.pop()
#         if isinstance(stack_item, expr):
            
#             def handle_BoolOp(o : BoolOp): 
#                 stack.append(o.right)
#                 stack.append(from_boolop(o.op))
#                 stack.append(o.left)
#                 stack.append(
#                     [lib.abstract_token.make_Grammar(
#                         options = 'expr',
#                         selection = 'BoolOp'
#                     )]
#                 )

#             match_expr(stack_item, ExprHandlers(
#                 case_BoolOp = handle_BoolOp,
#             ))
#
#         else:
#             result += stack_item 
    

