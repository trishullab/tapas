from __future__ import annotations

from lib.file import write_gen

from lib.def_type import Constructor, Field
from lib import def_type


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

type_code = (
    def_type.header +
    "\n\n" +
    "\n\n".join([
        def_type.generate_union(type_name, constructors)
    ])
)


write_gen("production_instance.py", type_code)




