from __future__ import annotations

from lib import def_type
from lib import line_format_def_type
from lib import production_instance_def_type

from lib import schema
from lib import python_schema

from lib import def_serialize
# from lib import def_rename

from lib.file import write
import pathlib
import os


base_path = pathlib.Path(__file__).parent.absolute()

dirpath = os.path.join(base_path, 'gen')

write(dirpath, "line_format.py", (
    def_type.header +
    "\n\n" +
    "\n\n".join([
        def_type.generate_choice(line_format_def_type.type_name, line_format_def_type.constructors)
    ])
))

write(dirpath, "production_instance.py", (
    def_type.header +
    "\n\n" +
    "\n\n".join([
        def_type.generate_choice(production_instance_def_type.type_name, production_instance_def_type.constructors)
    ])
))

write(dirpath, "python_ast.py", (
    def_type.header +
    "\n\n" +
    "\n\n".join([
        def_type.generate_single(schema.to_constructor(node))
        for node in python_schema.singles
    ]) +
    "\n\n" +
    "\n\n".join([
        def_type.generate_choice(type_name, [
            schema.to_constructor(node)
            for node in nodes 
        ])
        for type_name, nodes in python_schema.choices.items()
    ])
))


write(dirpath, "python_ast_serialize.py", (
    def_serialize.header +
    "\n\n" +
    "\n\n".join([
        def_serialize.generate_single_def(con)
        for con in python_schema.singles
    ]) +
    "\n\n" +
    "\n\n".join([
        def_serialize.generate_choice_def(type_name,con)
        for type_name, con in python_schema.choices.items()
    ])
))

# write(dirpath, "python_ast_rename.py", (
#     def_rename.header +
#     "\n\n" +
#     "\n\n".join([
#         def_rename.generate_single_def(con)
#         for con in python_schema.singles
#     ]) +
#     "\n\n" +
#     "\n\n".join([
#         def_rename.generate_choice_def(type_name,con)
#         for type_name, con in python_schema.choices.items()
#     ])
# ))





