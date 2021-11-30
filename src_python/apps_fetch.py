from tree_sitter import Language

import logging
import os
import pathlib
import json


from lib.file import write 

import re

base_path = pathlib.Path(__file__).parent.absolute()

def compile():
    logging.basicConfig(level=logging.INFO)
    read_path = os.path.join(base_path, "../../apps_data/")

    solution_count = 0
    page_count = 0
    prefix = ""

    write_dir = os.path.join(base_path, '../res/apps/input/')

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
        
compile()