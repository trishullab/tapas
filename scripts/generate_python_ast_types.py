from __future__ import annotations


from type_def import header, to_shape_list, generate_type_union_def, generate_type_intersection_def
from file import write

import python_ast

(unions, intersections) = python_ast.get()

code = (

    "\n\n".join([
        generate_type_union_def(k,v)
        for k, v in unions.entries()
    ]) + 
    "\n\n" +
    "\n\n".join([
        generate_type_intersection_def(k,v)
        for k, v in intersections.entries()
    ])
)

code = f"""
{header}

{code}

"""

write("python_ast", code)
