
from tree_sitter import Language
import tree_sitter
import ast
import json

from lib import generic_tree

from lib import python_ast
from lib.instance import match_instance, InstanceHandlers 
import lib.instance
from gen.instance_construct import instance

import pathlib
import os

import subprocess
from subprocess import TimeoutExpired, PIPE, STDOUT

import lib.souffle


base_path = pathlib.Path(__file__).parent.absolute()
    

def test_string(sourceCode): 

    generic_syntax_tree = generic_tree.parse('python', sourceCode, 'utf8')

    mod = python_ast.parse_from_generic_tree(generic_syntax_tree)

    instance_list = python_ast.serialize(mod)

    souffle_input = lib.souffle.from_sequence(instance_list) + "\n"
    print("---------souffle input---------")
    print(souffle_input)

    print("---------souffle output---------")
    result = lib.souffle.call("test.dl", souffle_input)
    print(result)



def test_mbpp():

    import logging
    import os
    import pathlib


    logging.basicConfig(level=logging.INFO)
    base_path = pathlib.Path(__file__).parent.absolute()
    dirpath = os.path.join(base_path, "../res/mbpp/input")
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

            if count > 10:
                break



test_mbpp()