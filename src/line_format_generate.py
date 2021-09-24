from __future__ import annotations

from file import write

from def_type import Constructor, Field
import def_type


type_name = "line_format"

constructors = [

    Constructor(
        "InLine",
        []
    ),

    Constructor(
        "NewLine",
        []
    ),

    Constructor(
        "IndentLine",
        []
    )
]

type_code = (
    def_type.header +
    "\n\n" +
    "\n\n".join([
        def_type.generate_union(type_name, constructors)
    ])
)


write("line_format", type_code)




