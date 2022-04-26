from __future__ import annotations
from typing import Iterator

from lib.abstract_token_system import abstract_token 
import lib.abstract_token_system

from lib.python_ast_construct_autogen import * 
from lib.abstract_token_construct_autogen import abstract_token, Grammar

from pyrsistent import s, m, pmap, v
from typing import Iterator
from pyrsistent.typing import PMap 

from lib import python_analysis_system as pus 
from lib import python_analysis_system

from lib import python_schema_system

def dump(instances : tuple[abstract_token, ...]):
    return lib.abstract_token_system.dump(python_schema_system.node_schema, instances)

def concretize(instances : tuple[abstract_token, ...]):
    return lib.abstract_token_system.concretize(python_schema_system.node_schema, instances)

