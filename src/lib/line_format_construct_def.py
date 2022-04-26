from __future__ import annotations

from lib import construct_def
from lib.construct_def import Constructor, Field

type_name = "line_format"

constructors = [

    Constructor("InLine", [], []),

    Constructor("NewLine", [], []),

    Constructor("IndentLine", [], [])
]

def generate_content():
    return construct_def.generate_content("", [], {type_name : constructors})



