from __future__ import annotations

from lib.def_type import Constructor, Field

type_name = "instance"

constructors = [
    Constructor(
        "Grammar",
        [
            Field('nonterminal', 'str'),
            Field('sequence_id', 'str')
        ]
    ),

    Constructor(
        "Vocab",
        [
            Field('choices_id', 'str'),
            Field('word', 'str')
        ]
    )
]



