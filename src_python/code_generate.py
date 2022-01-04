from __future__ import annotations

from lib import def_construct
from lib import def_line_format_construct
from lib import def_instance_construct

import lib.rule
from lib import python_schema

from lib import def_ast_serialize
from lib import def_ast_reconstitute

from lib.file import write
import pathlib
import os

from lib import def_ast_construct
from src_python.lib import def_rule_construct


base_path = pathlib.Path(__file__).parent.absolute()

dirpath = os.path.join(base_path, 'gen')

write(dirpath, "line_format_construct.py",
    def_line_format_construct.generate_content()
)

write(dirpath, "instance_construct.py", 
    def_instance_construct.generate_content()
)

write(dirpath, "rule_construct.py", 
    def_rule_construct.generate_content()
)

write(dirpath, "python_ast_construct.py",
    def_ast_construct.generate_content(python_schema.singles, python_schema.choices)
)

write(dirpath, "python_ast_serialize.py",
    def_ast_serialize.generate_content(python_schema.singles, python_schema.choices)
)

write(dirpath, "python_ast_reconstitute.py",
    def_ast_reconstitute.generate_content(python_schema.singles, python_schema.choices)
)