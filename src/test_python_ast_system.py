from typing import Callable, Any
from tapas_base import util_system
from tree_sitter import Language

from tapas_lib import generic_tree_system

from tapas_lib import python_ast_system
from tapas_lib.generic_tree_system import GenericNode


def run_concrete(concrete : str):
    mod = python_ast_system.parse(concrete)
    python_ast_system.assert_serialize_reconstitute_bidirectional(mod)
    python_ast_system.assert_concretize_parse_bidrectional(mod)


import os
dirpath = util_system.project_path("res/test/python/concrete_data")

def test_cubert():
    return util_system.run_jsonl_file(os.path.join(dirpath, "cubert_583.jsonl"), run_concrete)