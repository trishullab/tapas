from __future__ import annotations

from lib.file import write

from lib.def_type import Constructor, Field
from lib import def_type


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




