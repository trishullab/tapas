from __future__ import annotations

from lib import generic_tree_system
from lib.generic_tree_system import GenericNode

def parse(concrete : str) -> GenericNode:
    return generic_tree_system.parse('python', concrete, 'utf8')

def dump(gnode : GenericNode) -> str:
    return generic_tree_system.dump(gnode, 
        text_cond = lambda n : ( 
            len(n.children) == 0 or 
            n.syntax_part == "string"
        )
    )
