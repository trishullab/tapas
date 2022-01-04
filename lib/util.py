from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, TypeVar, Any, Generic, Union, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod
import json

T = TypeVar('T')

X = TypeVar('X')


def fail(msg : str):
    raise Exception(msg)

def map_option(f : Callable[[T], X], o : Optional[T]) -> Optional[X]:
    return f(o) if o != None else None

def match_d(k : T, d : dict[T, Callable[[], Any]], error_msg):
    return d.get(k, lambda: fail(error_msg))()

import os
import pathlib
# import logging

# logging.basicConfig(level=logging.INFO)


def project_path(rel_path : str):
    base_path = os.path.join(pathlib.Path(__file__).parent.absolute(), '..')
    return os.path.join(base_path, rel_path)


def write(dirpath : str, fname : str, code : str, append : bool = False):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    fpath = os.path.join(dirpath, f"{fname}")

    with open(fpath, 'a' if append else 'w') as f:
        # logging.info(f"Writing file: {fpath}")
        f.write(code)

# def path_from_relative(base : str, relative_path : str):
#     base_path = pathlib.Path(base).parent.absolute()
#     return os.path.join(base_path, relative_path)

def run_file(fpath : str, func : Callable[[str], Any]):
    error_count = 0

    with open(fpath, 'r') as f:
        #note: example 101 originally had a typo of using equality '==' instead of assignment '='
        count = 1

        line = f.readline()
        while line: 
            line_obj = json.loads(line)

            concrete = line_obj['code']
            func(concrete)

            # update
            line = f.readline()
            count += 1

        print(f"ERROR COUNT {error_count}")
