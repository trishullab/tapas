from __future__ import annotations

from lib.construct_def import Constructor, Field
from lib import construct_def

def generate_content():
    return (
        construct_def.header +
        "\n\n" +
        "from lib.line_format_construct_autogen import line_format" +
        "\n\n" +
        construct_def.generate_choice("item", [
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
        construct_def.generate_single(
            Constructor(
                "Rule",
                [
                    Field('name', 'str'), 
                    Field('content', 'list[item]')
                ]
            )
        )
    )






