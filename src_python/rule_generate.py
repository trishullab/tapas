from __future__ import annotations

from lib.file import write

from lib.def_type import Constructor, Field
from lib import def_type
import pathlib
import os



type_code = (
    def_type.header +
    "\n\n" +
    "from gen.line_format import line_format" +
    "\n\n" +
    def_type.generate_choice("item", [
        Constructor(
            "Terminal",
            [
                Field('terminal', 'str')
            ]
        ),

        Constructor(
            "Nonterm",
            [
                Field('relation', 'str'),
                Field('nonterminal', 'str'),
                Field('format', 'line_format'),
            ]
        ),

        Constructor(
            "Vocab",
            [
                Field('relation', 'str'),
                Field('vocab', 'str'),
            ]
        )
    ]) +

    "\n\n" +
    "\n\n" +
    def_type.generate_single(
        Constructor(
            "Rule",
            [
                Field('name', 'str'), 
                Field('content', 'list[item]')
            ]
        )
    )
)


base_path = pathlib.Path(__file__).parent.absolute()
dirpath = os.path.join(base_path, 'gen')
write(dirpath, "rule.py", type_code)




