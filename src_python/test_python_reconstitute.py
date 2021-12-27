
from tree_sitter import Language
import tree_sitter
import ast
import json

from lib import generic_tree

import lib.python_sequence
from lib.generic_tree import GenericNode
from lib import python_ast

    

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

    mod = python_ast.from_generic_ast(generic_syntax_tree)
    instance_list = python_ast.serialize(mod)


    # print(f"--Instance Sequence--\n")
    # for p in instance_list: print(p)
    # print(f"\n")

    # print(f"--Formatted Instance Sequence --\n{python_instance.dump(instance_list)}\n")

    print(f"--Concretized--\n{lib.python_sequence.concretize(instance_list)}\n")
    # print(f"\n")
    # print(f"---Source Code---")
    # print(sourceCode)

    # except RecursionError:
    #     print(f"\n\n")

    #     print(f"""--Generic Tree--\n{
    #         generic_tree.dump(generic_syntax_tree, 
    #             text_cond = lambda n : len(n.children) == 0 or n.syntax_part == "string"
    #         )
    #     }\n""")

    #     print(f"\n\n")
    #     print(f"---Source Code---")
    #     print(sourceCode)
    #     print(f"-------------------------")
    #     print("RECURSION ERROR")
    #     return

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
    dirpath = os.path.join(base_path, "../res/mbpp/concrete_data")
    fpath = os.path.join(dirpath, "mbpp.jsonl")

    with open(fpath, 'r') as f:
        #note: example 101 originally had a typo of using equality '==' instead of assignment '='
        count = 1

        line = f.readline()
        while line: 
            print(f"---------------------------")
            print(f"mbpp.jsonl line #: {count}")

            line_obj = json.loads(line)
            print("-----Prompt------")
            print(line_obj['text'])
            print("\n")

            source_code = line_obj['code']
            print("-----Source Code------")
            print(source_code)

            test_string(source_code)
            print("\n\n")

            # update
            line = f.readline()
            count += 1


def test_cubert():

    import logging
    import os
    import pathlib


    error_count = 0

    logging.basicConfig(level=logging.INFO)
    base_path = pathlib.Path(__file__).parent.absolute()
    dirpath = os.path.join(base_path, "../res/cubert/concrete_data")
    fpath = os.path.join(dirpath, "cubert_583.jsonl")

    with open(fpath, 'r') as f:
        #note: example 101 originally had a typo of using equality '==' instead of assignment '='
        count = 1

        line = f.readline()
        while line: 
            line_obj = json.loads(line)

            source_code = line_obj['code']
            generic_syntax_tree = GenericNode("", "", []) 
            generic_syntax_tree = generic_tree.parse('python', source_code, 'utf8')

            # print(f"--OOGA: {count}\n")
            # print(f"--OOGA SOURCE------------\n{source_code}")
            # print(f"""--OOGA Generic Tree--\n{
            #     generic_tree.dump(generic_syntax_tree, 
            #         text_cond = lambda n : len(n.children) == 0 or n.syntax_part == "string"
            #     )
            # }\n""")
            mod = python_ast.from_generic_ast(generic_syntax_tree)
            instance_list = python_ast.serialize(mod)
            concrete_A = lib.python_sequence.concretize(instance_list)
            mod_reconstituted = python_ast.reconstitute(instance_list)
            instance_list_B = python_ast.serialize(mod_reconstituted)
            concrete_B = lib.python_sequence.concretize(instance_list_B)

            print(f"concrete_B: {concrete_B}")
            if concrete_A != concrete_B:
                print("Reconstitute Failed")
            else:
                print("Reconstitute Works")

            # print(f"--Count: {count}\n")
            # print(f"--Concretized--\n{lib.python_sequence.concretize(instance_list)}\n")

            # update
            line = f.readline()
            count += 1

        print(f"ERROR COUNT {error_count}")

# test_string("""
# try:
#     pass
# except A , x:
#     pass
# """)

test_cubert()