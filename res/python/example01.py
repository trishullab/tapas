from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, TypeVar, Any, Generic, Union, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod

from tree_sitter import Language

import tree_sitter

T = TypeVar('T')

# type and constructor AbstractNode
@dataclass
class AbstractNode:
    syntax_part : str
    choice : node_choice



# type node_choice
@dataclass
class node_choice(ABC):
    @abstractmethod
    def _match(self, handlers : NodeChoiceHandlers[T]) -> T: pass


# constructors for type node_choice
@dataclass
class Leaf(node_choice):
    text : str

    def _match(self, handlers : NodeChoiceHandlers[T]) -> T:
        return handlers.case_Leaf(self)

@dataclass
class Branch(node_choice):
    children : list[AbstractNode]

    def _match(self, handlers : NodeChoiceHandlers[T]) -> T:
        return handlers.case_Branch(self)


# case handlers for type node_choice
@dataclass
class NodeChoiceHandlers(Generic[T]):
    case_Leaf : Callable[[Leaf], T]
    case_Branch : Callable[[Branch], T]


# matching for type node_choice
def match_node_choice(o : node_choice, handlers : NodeChoiceHandlers[T]) -> T :
    return o._match(handlers)



def from_tree_sitter_node(node : tree_sitter.Node, source : bytes) -> AbstractNode :

    children_iter = filter(
        lambda child : child.is_named,
        node.children
    )

    children_iter = map(
        lambda child : from_tree_sitter_node(child, source), 
        children_iter
    )

    children : list[tree_sitter.Node] = list(children_iter)

    is_terminal = len(children) == 0

    type = node.type


    if (is_terminal):
        text = source[node.start_byte:node.end_byte].decode('utf8')
        leaf = Leaf(text = text)
        return AbstractNode(syntax_part = type, choice = leaf)
    else:
        branch = Branch(children = children)
        return AbstractNode(syntax_part = type, choice = branch)


def to_dictionary(node : AbstractNode) -> Dict[str, Any]:
    return match_node_choice(node.choice, NodeChoiceHandlers(
        case_Branch = lambda branch : {
            'syntax_part' : node.syntax_part,
            'choice' : 'branch',
            'children' : 
                list(map(
                    lambda child : to_dictionary(child), 
                    branch.children
                ))            
        },
        case_Leaf = lambda leaf : {
            'syntax_part' : node.syntax_part,
            'choice' : 'leaf',
            'text' : leaf.text
        }
    ))



def dump(node : AbstractNode, indent : int = 4, depth : int = 0) -> str:
    return node.syntax_part + (match_node_choice(node.choice, NodeChoiceHandlers(
        case_Branch = lambda branch : (
            (child_depth := depth + 1),
            (indent_str := ' ' * indent * child_depth),
            (str_children := list(map(
                lambda child : indent_str + dump(child, indent, child_depth), 
                branch.children
            ))),
            '\n' + '\n'.join(str_children) 
        )[-1],
        case_Leaf = lambda leaf : ' ' + leaf.text
    )))


num = float(input("Enter a number: "))
if num >= 0:
    if num == 0:
        print("Zero")
    else:
        print("Positive number")
else:
    print("Negative number")

x = 1; x = 2; x = 3

123