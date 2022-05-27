from __future__ import annotations

from base import construct_def
from base import rule_system as rs


def generate_content(content_header : str, singles : list[rs.Rule], choices : dict[str, list[rs.Rule]]) -> str:
    return construct_def.generate_content(
        content_header,
        [rs.to_constructor(rule) for rule in singles], 
        { 
            type_name : [rs.to_constructor(rule) for rule in rules]
            for type_name, rules in choices.items()
        }
    )


