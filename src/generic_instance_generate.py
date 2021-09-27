from __future__ import annotations

from lib.file import write

from lib.def_type import Constructor, Field
from lib import def_type


type_name = "instance"
constructors = [
    Constructor(
        "Node",
        [
            Field("lhs", "str"),
            Field("rhs", "str"),
            Field("depth", "int"),
            Field("alias", "str"),
            Field("indent_width", "int"),
            Field("inline", "bool"),
        ]
    ),

    Constructor(
        "Symbol",
        [
            Field("content", "str"),
            Field("depth", "int"),
            Field("alias", "str")
        ]
    ),
]

type_code = (
    def_type.header +
    "\n\n" +
    "\n\n".join([
        def_type.generate_union(type_name, constructors)
    ])
)


write("generic_instance", type_code)




