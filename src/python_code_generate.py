from __future__ import annotations

from lib import python_schema
from lib import ast_serialize_def
from lib import ast_reconstitute_def
from lib import ast_construct_def
from lib import python_analysis_construct_def
from lib import abstract_token_analyze_def

from lib.util import write_code

write_code("python_ast_construct",
    ast_construct_def.generate_content(python_schema.singles, python_schema.choices)
)

write_code("python_ast_serialize",
    ast_serialize_def.generate_content(python_schema.singles, python_schema.choices)
)

write_code("python_ast_reconstitute",
    ast_reconstitute_def.generate_content(python_schema.singles, python_schema.choices)
)

write_code("python_analysis_construct",
    python_analysis_construct_def.generate_content()
)

write_code("python_abstract_token_analyze",
    abstract_token_analyze_def.generate_content(python_schema.singles, python_schema.choices)
)