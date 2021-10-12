from __future__ import annotations
from typing import Iterator

import lib.production_instance as prod_inst 

from lib import python_schema

def dump(instances : list[prod_inst.instance]):
    return prod_inst.dump(instances)

def concretize(instances : list[prod_inst.instance]):
    return prod_inst.concretize(python_schema.node_map, instances)
