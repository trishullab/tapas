from __future__ import annotations

from lib.def_type import Constructor, Field

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



