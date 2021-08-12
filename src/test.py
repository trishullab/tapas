
from tree_sitter import Language
import tree_sitter
import ast
import json

import generic_tree

from python_ast_from_generic_ast import from_generic_ast
from python_ast_serialize import serialize
import production as pro

    

def test_python_ast(source):
    t = ast.dump(ast.parse(source), indent=4)

    print("--Library Python AST--")
    print(t)
    print("")
    print("\n")


def test_translation(sourceCode): 

    generic_syntax_tree = generic_tree.parse('python', sourceCode, 'utf8')

    print("--Generic Tree--")
    print("")
    print(generic_tree.dump(generic_syntax_tree, 
        text_cond = lambda n : len(n.children) == 0 or n.syntax_part == "string"
    ))
    print("\n")

    ast = from_generic_ast(generic_syntax_tree)

    prod_list = serialize(ast)

    print("--Production List--")
    print("")
    print(prod_list)
    print("\n")

    print("--Production Tree--")
    print("")
    print(pro.dump(prod_list))
    print("\n")

def test(fname):
    import logging
    import os
    import pathlib


    logging.basicConfig(level=logging.INFO)
    base_path = pathlib.Path(__file__).parent.absolute()
    dirpath = os.path.join(base_path, "../res/python")
    fpath = os.path.join(dirpath, f"{fname}.py")

    with open(fpath, 'r') as f:
        sourceCode = f.read() 

    #print trees

    print(f"--{fname}--")
    print("\n")

    # print("--Python source code--")
    # print("")
    # print(sourceCode)
    # print("\n")

    # test_python_ast(sourceCode)

    test_translation(sourceCode)




test('scratch')