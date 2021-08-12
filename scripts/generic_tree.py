from type_def import header, to_shape_list, generate_type_union_def, generate_type_intersection_def
from file import write



abstract_node_code = generate_type_intersection_def(
    "GenericNode", 
    [
        ("syntax_part", "str"),
        ("text", "str"),
        ("children", "list[GenericNode]")
    ]
)

code = f"""
{header}

{abstract_node_code}

"""

write("generic_tree", code)
