from __future__ import annotations

from lib import construct_def
import lib.rule
from lib.rule import Rule

def generate_content(singles : list[Rule], choices : dict[str, list[Rule]]) -> str:
    return construct_def.generate_content(
        [lib.rule.to_constructor(rule) for rule in singles], 
        { 
            type_name : [lib.rule.to_constructor(rule) for rule in rules]
            for type_name, rules in choices.items()
        }
    )


