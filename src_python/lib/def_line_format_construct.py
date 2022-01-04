from __future__ import annotations

from lib import def_construct
from lib.def_construct import Constructor, Field

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

def generate_content():
    return def_construct.generate_content([], {type_name : constructors})



