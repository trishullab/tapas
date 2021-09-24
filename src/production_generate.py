from __future__ import annotations

from file import write

from def_type import Constructor, Field
import def_type


type_name = "production"
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


write("production", type_code)




