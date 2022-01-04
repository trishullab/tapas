from __future__ import annotations

from lib import generic_tree
from lib.generic_tree import GenericNode

def parse(concrete : str) -> GenericNode:
    return generic_tree.parse('python', concrete, 'utf8')

def dump(gnode : GenericNode) -> str:
    return generic_tree.dump(gnode, 
        text_cond = lambda n : ( 
            len(n.children) == 0 or 
            n.syntax_part == "string"
        )
    )
