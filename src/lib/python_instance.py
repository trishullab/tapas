from __future__ import annotations
from typing import Iterator

from gen.generic_instance import *
import lib.generic_instance as inst 

from lib import python_schema

def dump(prods : list[instance]):
    return inst.dump(python_schema.node_map, prods)

def concretize(prods : list[instance]):
    return inst.concretize(python_schema.node_map, prods)
