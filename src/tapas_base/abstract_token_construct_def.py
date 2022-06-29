from __future__ import annotations

from tapas_base.construct_def import Constructor, Field
from tapas_base import construct_def

type_name = "abstract_token"

constructors = [
    Constructor(
        "Grammar", [], [
            Field('options', 'str', ""),
            Field('selection', 'str', ""),
            Field('source_start', 'int', "0"),
            Field('source_end', 'int', "0"),
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

