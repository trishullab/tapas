from __future__ import annotations

from lib.file import write

from lib.def_construct import Constructor, Field
from lib import def_construct
import pathlib
import os


def generate_content():
    return (
        def_construct.header +
        "\n\n" +
        "from gen.line_format_construct import line_format" +
        "\n\n" +
        def_construct.generate_choice("item", [
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
        def_construct.generate_single(
            Constructor(
                "Rule",
                [
                    Field('name', 'str'), 
                    Field('content', 'list[item]')
                ]
            )
        )
    )






