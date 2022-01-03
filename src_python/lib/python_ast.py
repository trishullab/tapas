from __future__ import annotations

from gen import python_serialize

from gen import python_reconstitute 
from gen.python_ast import Module
from gen.instance import instance
from lib import generic_tree
from lib.generic_tree import GenericNode
from lib import python_ast_parse
from lib import python_generic_tree
from lib import python_sequence

from lib.python_ast_parse import Unsupported, ConcreteParsingError

def parse_from_generic_tree(gnode : GenericNode) -> Module:
    return python_ast_parse.from_generic_tree(gnode)

def parse(concrete : str) -> Module:
    gnode = python_generic_tree.parse(concrete)
    return python_ast_parse.from_generic_tree(gnode)

def serialize(mod : Module) -> list[instance]:
    return python_serialize.from_Module(mod)

def reconstitute(xs : list[instance]) -> Module:
    return python_reconstitute.to_Module([x for x in reversed(xs)])[0] 

def concretize(mod: Module) -> str:
    seq = serialize(mod)
    return python_sequence.concretize(seq)

def assert_serialize_reconstitute_bidirectional(mod: Module):
    seq = serialize(mod)
    mod_result = reconstitute(seq)
    assert mod == mod_result

def assert_concretize_parse_bidrectional(mod: Module):
    concrete = concretize(mod)
    mod_result = parse(concrete)
    assert mod == mod_result