from tree_sitter import Language

import logging
import os
import pathlib
import tree_sitter
import json

from lib import generic_tree

from lib.python_ast_from_generic_ast import from_generic_ast
from gen.python_ast_serialize import serialize_Module
from lib import python_instance
from lib import generic_instance as inst 
from lib.file import write_res, write_append_res, write_append_res_gen
from lib import training_data

import re

def compile():
    logging.basicConfig(level=logging.INFO)
    base_path = pathlib.Path(__file__).parent.absolute()
    dirpath = os.path.join(base_path, "../../../apps_data/")

    solution_count = 0
    page_count = 0
    prefix = ""

    write_res(f'apps_{0}.jsonl', '')
    for dirkey in os.listdir(dirpath):
        if re.match("\d\d\d\d", dirkey):
            fpath = f"{dirpath}{dirkey}/solutions.json"

            with open(fpath, 'r') as f:
                solutions_txt = f.read()
                solutions = json.loads(solutions_txt)
                for sol in solutions:
                    # print(f"solution: {sol}")
                    write_append_res(f'apps_{page_count}.jsonl', prefix + json.dumps({"code" : sol}))
                    prefix = "\n"


        solution_count += 1
        if solution_count > 100:
            solution_count = 0
            page_count += 1
            write_res(f'apps_{page_count}.jsonl', '')
            prefix = ""
        