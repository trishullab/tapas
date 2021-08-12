import logging
import os
import pathlib

import inflection
import jinja2

logging.basicConfig(level=logging.INFO)


base_path = pathlib.Path(__file__).parent.absolute()
dirpath = os.path.join(base_path, "../src/gen")

if not os.path.exists(dirpath):
    os.makedirs(dirpath)

def write(fname : str, code : str):

    fpath = os.path.join(dirpath, f"{fname}.py")

    with open(fpath, 'w') as f:
        logging.info(f"Writing file: {fpath}")
        f.write(code)