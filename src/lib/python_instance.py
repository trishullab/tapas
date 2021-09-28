from __future__ import annotations
from typing import Iterator

import lib.generic_instance as inst 

from lib import python_schema

def dump(nodes : list[inst.Node]):
    return inst.dump(nodes)

def concretize(inst_nodes : list[inst.Node]):
    return inst.concretize(python_schema.node_map, inst_nodes)
