from __future__ import annotations

from lib.def_construct import Constructor, Field
from lib import def_construct

type_name = "instance"

constructors = [
    Constructor(
        "Grammar",
        [
            Field('options', 'str'),
            Field('selection', 'str')
        ]
    ),

    Constructor(
        "Vocab",
        [
            Field('options', 'str'),
            Field('selection', 'str')
        ]
    )
]


def generate_content():
    return def_construct.generate_content([], {type_name : constructors})

