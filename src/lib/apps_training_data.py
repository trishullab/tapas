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
from lib.file import write 
from lib import training_data

import re

base_path = pathlib.Path(__file__).parent.absolute()

def compile():
    logging.basicConfig(level=logging.INFO)
    base_path = pathlib.Path(__file__).parent.absolute()
    read_path = os.path.join(base_path, "../../../apps_data/")

    solution_count = 0
    page_count = 0
    prefix = ""

    write_dir = os.path.join(base_path, '../../res/apps')

    write(write_dir, f'apps_{0}.jsonl', '')
    for dirkey in os.listdir(read_path):
        if re.match("\d\d\d\d", dirkey):
            fpath = f"{read_path}{dirkey}/solutions.json"

            with open(fpath, 'r') as f:
                solutions_txt = f.read()
                solutions = json.loads(solutions_txt)
                for sol in solutions:
                    # print(f"solution: {sol}")
                    write(write_dir, f'apps_{page_count}.jsonl', prefix + json.dumps({"code" : sol}), append=True)
                    prefix = "\n"


        solution_count += 1
        if solution_count > 100:
            solution_count = 0
            page_count += 1
            write(write_dir, f'apps_{page_count}.jsonl', '', append=True)
            prefix = ""
        