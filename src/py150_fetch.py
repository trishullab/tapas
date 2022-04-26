from datasets import load_dataset
import requests
import re


# split = 'train', 'test', or 'validation'
def generate_code(split : str): 
    data = load_dataset('eth_py150_open', split=split)

    error_count = 0
    success_count = 0
    total_count = 0

    for i, d in enumerate(data):

        branches = ["master", "main"]

        for branch_idx, branch in enumerate(branches):
            try:
                pathlist = d['filepath'].split("/")
                branch_url = pathlist[0] + "/" + pathlist[1] + "/" + branch + "/" + "/".join(pathlist[2:])
                url = f"https://raw.githubusercontent.com/{branch_url}"

                res = requests.get(url, allow_redirects=True)
                res.status_code
                content : str = res.content.decode('utf-8')
                if res.status_code == 200:
                    success_count += 1
                    yield content 
                    break
                elif branch_idx + 1 == len(branches): 
                    error_count += 1

            except Exception:
                if branch_idx + 1 == len(branches): 
                    error_count += 1
        
        total_count += 1

    print(f"total count: {total_count}")
    print(f"error count: {error_count}")
    print(f"success count: {success_count}")


import logging
import json


from lib.util_system import write, project_path

import re

def write_code(split="train"):

    logging.basicConfig(level=logging.INFO)

    page_length = 2000
    page_count=0
    code_count = 0
    prefix = ""

    write_dir = project_path(f'res/py150_{split}/input/')

    write(write_dir, f'py150_{split}_{page_count}.jsonl', '')
    for code in generate_code(split):
        write(write_dir, f'py150_{split}_{page_count}.jsonl', prefix + json.dumps({"code" : code}), append=True)
        prefix = "\n"

        code_count += 1
        if code_count >= page_length:
            code_count = 0
            page_count += 1
            write(write_dir, f'py150_{split}_{page_count}.jsonl', '', append=True)
            prefix = ""

# write_code('train')
write_code('test')
write_code('validation')