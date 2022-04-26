from __future__ import annotations

from lib import construct_def
import lib.rule_system
from lib.rule_system import Rule


def generate_content(content_header : str, singles : list[Rule], choices : dict[str, list[Rule]]) -> str:
    return construct_def.generate_content(
        content_header,
        [lib.rule_system.to_constructor(rule) for rule in singles], 
        { 
            type_name : [lib.rule_system.to_constructor(rule) for rule in rules]
            for type_name, rules in choices.items()
        }
    )


