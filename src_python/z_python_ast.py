from typing import Callable, Any

from tree_sitter import Language
import tree_sitter
import ast
import json

from lib import generic_tree

from lib import python_ast
from lib.generic_tree import GenericNode
from lib import python_generic_tree
from lib import python_sequence


def run_concrete(concrete : str):
    mod = None
    try:
        mod = python_ast.parse(concrete)

    except python_ast.ConcreteParsingError:
        gnode = python_generic_tree.parse(concrete)
        hr = python_generic_tree.dump(gnode)
        print(f"---concrete parsing error---")
        print(hr)
        print(f"---concrete parsing error---")

    except python_ast.Unsupported as x:
        gnode = python_generic_tree.parse(concrete)
        hr = python_generic_tree.dump(gnode)
        print(f"---unsupported: {x.args[0]}---")
        print(hr)
        print(f"---unsupported: {x.args[0]}---")

    else:
        assert mod
        try:
            python_ast.serialize_reconstitute_bidirectional(mod)
        except AssertionError as x:
            seq = python_ast.serialize(mod)
            hr = python_sequence.dump(seq) 
            print(f"---serialize reconstitute error: {x.args[0]}---")
            print(hr)
            print(f"---serialize reconstitute error: {x.args[0]}---")
            raise x


        concrete_0 = python_ast.concretize(mod)
        mod_0 = python_ast.parse(concrete_0) 
        try:
            assert mod == mod_0
            # assert python_ast.concretize_parse_bidrectional(mod)
        except AssertionError as x:
            print(f"---concrete parse error: {mod == mod_0}---")
            print(concrete)
            print(f"---concrete parse error 0: {mod == mod_0}, {concrete == concrete_0}---")
            # print(python_sequence.dump(python_ast.serialize(mod)))
            print(concrete_0)
            print(f"---concrete parse error: {mod == mod_0}---")
            print(f"x args: {x.args}")
            raise x


from lib import utils
import os
dirpath = utils.path_from_relative(__file__, "../res/test/python/concrete_data")

def inspect_cubert():
    return utils.run_file(os.path.join(dirpath, "cubert_583.jsonl"), run_concrete)

inspect_cubert()