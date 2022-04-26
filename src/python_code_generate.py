from __future__ import annotations

from lib.util_system import write_code

from lib import python_analysis_construct_def
write_code("python_analysis_construct",
    python_analysis_construct_def.generate_content()
)

from lib import python_ast_construct_def
write_code("python_ast_construct",
    python_ast_construct_def.generate_content()
)

from lib import python_schema_system
from lib import ast_serialize_def
write_code("python_ast_serialize",
    ast_serialize_def.generate_content("""
from lib.python_ast_system import *
    """, python_schema_system.singles_schema, python_schema_system.choices_schema)
)

from lib import ast_reconstitute_def
write_code("python_ast_reconstitute",
    ast_reconstitute_def.generate_content("""
from lib.python_ast_system import *
    """,python_schema_system.singles_schema, python_schema_system.choices_schema)
)

from lib import python_abstract_token_crawl_def
write_code("python_abstract_token_crawl",
    python_abstract_token_crawl_def.generate_content()
)