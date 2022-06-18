from __future__ import annotations

from tapas_base.util_system import write_code
from tapas_lib import python_aux_construct_def
from tapas_lib import python_schema_system
from tapas_lib import ast_serialize_def
from tapas_lib import ast_reconstitute_def
from tapas_lib import python_ast_construct_def
from tapas_lib import python_aux_crawl_stream_def

write_code('tapas_lib', "python_aux_construct",
    python_aux_construct_def.generate_content()
)

write_code('tapas_lib', "python_ast_construct",
    python_ast_construct_def.generate_content()
)

write_code('tapas_lib', "python_ast_serialize",
    ast_serialize_def.generate_content("""
from tapas_lib.python_ast_construct_autogen import *
    """, python_schema_system.singles_schema, python_schema_system.choices_schema)
)

write_code('tapas_lib', "python_ast_reconstitute",
    ast_reconstitute_def.generate_content("""
from tapas_lib.python_ast_construct_autogen import *
    """,python_schema_system.singles_schema, python_schema_system.choices_schema)
)

write_code('tapas_lib', "python_aux_crawl_stream",
    python_aux_crawl_stream_def.generate_content()
)