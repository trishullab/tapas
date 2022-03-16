from lib import generic_tree
from lib import python_ast
from lib.abstract_token_construct_autogen import abstract_token
from lib.generic_tree import GenericNode
from lib import python_generic_tree
from lib import python_abstract_token
from lib import util
import os

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
            python_ast.assert_serialize_reconstitute_bidirectional(mod)
        except AssertionError as x:
            seq = python_ast.serialize(mod)
            hr = python_abstract_token.dump(seq) 
            print(f"---serialize reconstitute error: {x.args[0]}---")
            print(hr)
            print(f"---serialize reconstitute error: {x.args[0]}---")
            raise x


        try:
            # assert mod == mod_0
            python_ast.assert_concretize_parse_bidrectional(mod)
        except AssertionError as x:
            concrete_0 = python_ast.concretize(mod)
            mod_0 = python_ast.parse(concrete_0) 
            print(f"---concrete parse error: {mod == mod_0}---")
            # print(concrete)
            # print(python_sequence.dump(python_ast.serialize(mod)))
            print(f"---concrete parse error 0: {mod == mod_0}, {concrete == concrete_0}---")
            print(concrete_0)
            # print(python_sequence.dump(python_ast.serialize(mod_0)))
            print(f"---concrete parse error: {mod == mod_0}---")
            raise x


dirpath = util.project_path("res/test/python/concrete_data")

def inspect_cubert():
    return util.run_jsonl_file(os.path.join(dirpath, "cubert_583.jsonl"), run_concrete)

# inspect_cubert()

def show_tree(concrete : str):
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
        tokens = python_ast.serialize(mod)
        d = python_abstract_token.dump(tokens)
        print(d)



show_tree('''
from typing import Callable

x : Callable[[int], tuple[int, int]] = lambda x : (x, 1)
''')