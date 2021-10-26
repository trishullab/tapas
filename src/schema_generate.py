from __future__ import annotations

from lib.file import write

from lib.def_type import Constructor, Field
from lib import def_type
import pathlib
import os


type_name = "child"

constructors = [
    Constructor(
        "Grammar",
        [
            Field('relation', 'str'),
            Field('nonterminal', 'str'),
            Field('format', 'line_format'),
            Field('follower', 'str')
        ]
    ),

    Constructor(
        "Vocab",
        [
            Field('relation', 'str'),
            Field('choices_id', 'str'),
            Field('follower', 'str')
        ]
    )
]

type_code = (
    def_type.header +
    "\n\n" +
    "from gen.line_format import line_format" +
    "\n\n" +
    "\n\n".join([
        def_type.generate_union(type_name, constructors)
    ]) +

    "\n\n" +
    "\n\n" +
    "\n\n".join([
        def_type.generate_intersection(
            Constructor(
                "Node",
                [
                    Field('name', 'str'), 
                    Field('leader', 'str'),
                    Field('children', 'list[child]')
                ]
            )
        )
    ])
)


base_path = pathlib.Path(__file__).parent.absolute()
dirpath = os.path.join(base_path, 'gen')
write(dirpath, "schema.py", type_code)




