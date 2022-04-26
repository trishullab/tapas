
from lib import ast_construct_def
from lib import python_schema_system

nl = "\n"
def generate_content() -> str:
    return f"""

{ast_construct_def.generate_content('from typing import Union', python_schema_system.singles_schema, python_schema_system.choices_schema)}

ast = Union[
{f',{nl}'.join([
    f"    {node_type}"
    for node_type in (list(python_schema_system.node_schema.keys()) + ['str'])
])}
] 
    """