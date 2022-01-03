
from typing import Callable, Any

from tree_sitter import Language
import tree_sitter
import ast
import json

from lib import generic_tree

from lib import python_ast
from lib.generic_tree import GenericNode


def run_concrete(concrete : str):
    mod = None
    try:
        mod = python_ast.parse(concrete)
    except python_ast.ConcreteParsingError:
        pass
    else:
        assert mod
        python_ast.assert_serialize_reconstitute_bidirectional(mod)
        python_ast.assert_concretize_parse_bidrectional(mod)


from lib import utils
import os
dirpath = utils.path_from_relative(__file__, "../res/test/python/concrete_data")

def test_cubert():
    return utils.run_file(os.path.join(dirpath, "cubert_583.jsonl"), run_concrete)