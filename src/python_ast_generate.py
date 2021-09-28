from __future__ import annotations

from lib import def_type
from lib import def_serialize

from lib.file import write_gen

from lib import python_schema
from lib import schema


type_code = (
    def_type.header +
    "\n\n" +
    "\n\n".join([
        def_type.generate_intersection(
            schema.to_constructor(node))
        for node in python_schema.intersections
    ]) +
    "\n\n" +
    "\n\n".join([
        def_type.generate_union(type_name, [
            schema.to_constructor(node)
            for node in nodes 
        ])
        for type_name, nodes in python_schema.unions.items()
    ])
)


write_gen("python_ast.py", type_code)


serialize_code = (
    def_serialize.header +
    "\n\n" +
    "\n\n".join([
        def_serialize.generate_intersection_def(con)
        for con in python_schema.intersections
    ]) +
    "\n\n" +
    "\n\n".join([
        def_serialize.generate_union_def(type_name,con)
        for type_name, con in python_schema.unions.items()
    ])
)
write_gen("python_ast_serialize.py", serialize_code)




