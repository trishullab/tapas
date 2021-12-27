from lib.python_ast_from_generic_ast import from_generic_ast
from gen.python_serialize import serialize_Module
from gen import python_reconstitute 
from gen.python_ast import Module
from gen.instance import instance

def serialize(mod : Module) -> list[instance]:
    return serialize_Module(mod)

def reconstitue(xs : list[instance]) -> Module:
    return python_reconstitute.to_Module([x for x in reversed(xs)])[0] 
