from __future__ import annotations
from typing import Iterator

from tapas_base.abstract_token_system import abstract_token 
import tapas_base.abstract_token_system

from tapas_lib.python_ast_construct_autogen import * 
from tapas_base.abstract_token_construct_autogen import abstract_token, Grammar

from pyrsistent import s, m, pmap, v
from typing import Iterator
from pyrsistent.typing import PMap 

from tapas_lib import python_aux_system as pus 
from tapas_lib import python_aux_system

from tapas_lib import python_schema_system

def dump(instances : tuple[abstract_token, ...]):
    return tapas_base.abstract_token_system.dump(python_schema_system.node_schema, instances)

def concretize(instances : tuple[abstract_token, ...]):
    return tapas_base.abstract_token_system.concretize(python_schema_system.node_schema, instances)

def concretize_old(instances : tuple[abstract_token, ...]):
    return tapas_base.abstract_token_system.concretize_old(python_schema_system.node_schema, instances)