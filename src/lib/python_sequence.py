from __future__ import annotations
from typing import Iterator

from lib.instance import instance
import lib.instance

from lib import python_schema

def dump(instances : list[instance]):
    return lib.instance.dump(python_schema.rule_map, instances)

def concretize(instances : list[instance]):
    return lib.instance.concretize(python_schema.rule_map, instances)
