from __future__ import annotations
from typing import Iterator

from gen.production import *
import lib.production as pro

from lib import python_schema

def dump(prods : list[production]):
    return pro.dump(python_schema.node_map, prods)

def concretize(prods : list[production]):
    return pro.concretize(python_schema.node_map, prods)
