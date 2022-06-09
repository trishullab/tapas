from __future__ import annotations

from base.construct_def import Constructor, Field
from base import construct_def

type_name = "abstract_token"

constructors = [
    Constructor(
        "Grammar", [], [
            Field('options', 'str', ""),
            Field('selection', 'str', "")
        ]
    ),

    Constructor(
        "Vocab", [], [
            Field('options', 'str', ""),
            Field('selection', 'str', "")
        ]
    ),

    Constructor(
        "Hole", [], []
    )
]


def generate_content():
    return construct_def.generate_content("", [], {type_name : constructors})
