from __future__ import annotations

from tapas_lib import python_schema_system
from tapas_lib import aux_crawl_stream_def

def generate_content():

    return aux_crawl_stream_def.generate_content(f'''
from tapas_lib.python_ast_construct_autogen import * 
        ''', 
        singles = python_schema_system.singles_schema, 
        choices = python_schema_system.choices_schema
    )



