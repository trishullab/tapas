from __future__ import annotations


from typing import Optional

from base import construct_def
from base.construct_def import Constructor, Field

from lib import python_schema_system
from lib import aux_analyze_stream_def

def generate_content():

    return aux_analyze_stream_def.generate_content(f'''
from lib.python_ast_construct_autogen import * 
        ''', 
        singles = python_schema_system.singles_schema, 
        choices = python_schema_system.choices_schema
    )



