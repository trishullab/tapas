import logging
import os
import pathlib

import inflection
import jinja2

# logging.basicConfig(level=logging.INFO)


base_path = pathlib.Path(__file__).parent.absolute()


def write(fname : str, code : str, dir : str, append : bool = False):
    dirpath = os.path.join(base_path, dir)

    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    fpath = os.path.join(dirpath, f"{fname}")

    with open(fpath, 'a' if append else 'w') as f:
        # logging.info(f"Writing file: {fpath}")
        f.write(code)


def write_gen(fname : str, code : str):
    return write(fname, code, "../gen")


def write_res(fname : str, code : str):
    return write(fname, code, "../../res")

def write_append_res(fname : str, code : str):
    return write(fname, code, "../../res", append = True)

def write_res_gen(fname : str, code : str):
    return write(fname, code, "../../res/gen")

def write_append_res_gen(fname : str, code : str):
    return write(fname, code, "../../res/gen", append = True)
