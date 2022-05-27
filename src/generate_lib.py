from __future__ import annotations

from base.util_system import write_code
from lib import python_aux_construct_def
from lib import python_schema_system
from lib import ast_serialize_def
from lib import ast_reconstitute_def
from lib import python_ast_construct_def
from lib import python_aux_analyze_stream_def

write_code('lib', "python_aux_construct",
    python_aux_construct_def.generate_content()
)

write_code('lib', "python_ast_construct",
    python_ast_construct_def.generate_content()
)

write_code('lib', "python_ast_serialize",
    ast_serialize_def.generate_content("""
from lib.python_ast_construct_autogen import *
    """, python_schema_system.singles_schema, python_schema_system.choices_schema)
)

write_code('lib', "python_ast_reconstitute",
    ast_reconstitute_def.generate_content("""
from lib.python_ast_construct_autogen import *
    """,python_schema_system.singles_schema, python_schema_system.choices_schema)
)

write_code('lib', "python_aux_analyze_stream",
    python_aux_analyze_stream_def.generate_content()
)