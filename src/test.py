
from tree_sitter import Language
import tree_sitter
import ast
import json

import generic_tree

from python_ast_from_generic_ast import from_generic_ast
from gen.python_ast_serialize import serialize_Module
import python_production
import production as pro

    

def test_python_ast(source):
    t = ast.dump(ast.parse(source), indent=4)

    print("--Library Python AST--")
    print(t)
    print("")
    print("\n")


def test_string(sourceCode): 

    generic_syntax_tree = generic_tree.parse('python', sourceCode, 'utf8')

    print(f"""--Generic Tree--\n{
        generic_tree.dump(generic_syntax_tree, 
            text_cond = lambda n : len(n.children) == 0 or n.syntax_part == "string"
        )
    }\n""")

    mod = from_generic_ast(generic_syntax_tree)

    prod_list = serialize_Module(mod)

    print(f"--Production List--\n")
    for p in prod_list: print(p)
    print(f"\n")

    print(f"--Production Tree--\n{python_production.dump(prod_list)}\n")

    print(f"--Concretized--\n{python_production.concretize(prod_list)}\n")

def test_filename(fname):
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

    test_string(sourceCode)



def test_mbpp():

    import logging
    import os
    import pathlib


    logging.basicConfig(level=logging.INFO)
    base_path = pathlib.Path(__file__).parent.absolute()
    dirpath = os.path.join(base_path, "../res")
    fpath = os.path.join(dirpath, "mbpp.jsonl")

    with open(fpath, 'r') as f:
        count = 0
        while f and count < 1:
            line = f.readline()
            line_obj = json.loads(line)
            print("-----Prompt------")
            print(line_obj['text'])
            # print("\n\n")

            print("-----Source Code------")
            source_code = line_obj['code']
            print(source_code)

            test_string(source_code)
            print("\n\n")

            count += 1



# test_mbpp()

test_filename('scratch')