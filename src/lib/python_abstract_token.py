from __future__ import annotations
from typing import Iterator

from lib.abstract_token import abstract_token 
import lib.abstract_token

from lib.python_ast_construct_autogen import * 
from lib.abstract_token_construct_autogen import abstract_token, Grammar

from lib.python_analysis import Inher
from lib import python_analysis

from pyrsistent import s, m, pmap, v
from typing import Iterator
from pyrsistent.typing import PMap 

from lib.python_analysis_construct_autogen import LocalEnvSynth


from lib import python_schema

def dump(instances : tuple[abstract_token, ...]):
    return lib.abstract_token.dump(python_schema.rule_map, instances)

def concretize(instances : tuple[abstract_token, ...]):
    return lib.abstract_token.concretize(python_schema.rule_map, instances)

