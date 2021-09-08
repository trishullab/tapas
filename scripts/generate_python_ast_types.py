from __future__ import annotations


from type_def import header, to_shape_list, generate_type_union_def, generate_type_intersection_def
from file import write

import python_ast_data


code = (

    "\n\n".join([
        generate_type_union_def(k,v)
        for k, v in python_ast_data.unions.items()
    ]) + 
    "\n\n" +
    "\n\n".join([
        generate_type_intersection_def(k,v)
        for k, v in python_ast_data.intersections.items()
    ])
)

code = f"""
{header}

{code}

"""

write("python_ast", code)
