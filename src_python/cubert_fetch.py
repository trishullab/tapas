import requests
import pathlib
from typing import Iterable, Union 

import logging
import os
import pathlib
import json


from lib.file import write 



import re



base_path = pathlib.Path(__file__).parent.absolute()


def fetch_code(d : dict[str,str]) -> Union[str, None]:
    branches = ["master", "main"]

    for branch_idx, branch in enumerate(branches):
        try:
            url = f"https://raw.githubusercontent.com/{d['repository']}/{branch}/{d['filepath']}"

            res = requests.get(url, allow_redirects=True)
            res.status_code
            content : str = res.content.decode('utf-8')
            if res.status_code == 200:
                return content 

            elif branch_idx + 1 == len(branches): 
                pass

        except Exception:
            if branch_idx + 1 == len(branches): 
                pass

    return None


# split = 'train', 'test', or 'validation'
def generate_code() -> Iterable[str]: 
    read_dir = os.path.join(base_path, "../res/cubert/url_data/")

    for fkey in os.listdir(read_dir):
        fpath = f"{read_dir}{fkey}"

        with open(fpath, 'r') as f:
            line = f.readline()
            while (line):
                d = json.loads(line)
                code = fetch_code(d)
                if code != None: 
                    yield (d | {"code" : code})

                line = f.readline()






def write_code():

    logging.basicConfig(level=logging.INFO)
    base_path = pathlib.Path(__file__).parent.absolute()

    page_length = 2000
    page_count=0
    code_count = 0
    prefix = ""

    write_dir = os.path.join(base_path, f'../res/cubert/concrete_data/')

    write(write_dir, f'cubert_{page_count}.jsonl', '')
    for code_record in generate_code():
        write(write_dir, f'cubert_{page_count}.jsonl', prefix + json.dumps(code_record), append=True)
        prefix = "\n"

        code_count += 1
        if code_count >= page_length:
            code_count = 0
            page_count += 1
            write(write_dir, f'cubert_{page_count}.jsonl', '', append=True)
            prefix = ""


write_code()