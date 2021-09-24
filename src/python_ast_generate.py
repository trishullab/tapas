from __future__ import annotations

import def_type
import def_serialize

from file import write

import python_schema
import schema


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


write("python_ast", type_code)


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
write("python_ast_serialize", serialize_code)




