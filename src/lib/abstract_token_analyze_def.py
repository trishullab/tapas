from __future__ import annotations

from dataclasses import dataclass

import lib.rule
from lib.rule import Rule

from lib import python_schema

import lib.python_schema

nl = "\n"
def generate_analyze_token_inductive_choice_rule(type_name : str, rule : Rule):

    abstract_items = lib.rule.get_abstract_items(rule)
    return f"""
    def analyze_token_{type_name}_{rule.name}(self,
        inher : I, children : tuple[S, ...], stack_result : Optional[S], 
        stack : list[tuple[abstract_token, I, tuple[S, ...]]]
    ) -> Optional[S]:

        {f'''
        if stack_result:
            # get the result from the child in the stack
            children = children + tuple([stack_result]) 
        ''' if lib.rule.is_inductive(type_name, [rule]) else ''}

        total_num_children = {len(abstract_items)}

        index = len(children)
        if index == total_num_children:
            # the processing of the current rule has completed
            # return the analysis result to the previous item in the stack
            return self.synthesize_{type_name}_{rule.name}_attributes(inher, children)
        {nl.join([
            f'''
        elif index == {i}: # index does *not* refer to an inductive child

            child_synth = self.analyze_{lib.rule.type_from_item(item)}({f'self.traverse_{type_name}_{rule.name}_{lib.rule.relation_from_item(item)}(inher, children)'})
            stack.append((Grammar("{type_name}", "{rule.name}"), inher, children + tuple([child_synth])))
            return None
            '''
            for i, item in enumerate(abstract_items)
            if lib.rule.type_from_item(item) != type_name
        ])}
        {nl.join([
            f'''
        elif index == {i} : # index refers to an inductive child
            # put back current node
            stack.append((Grammar("{type_name}", "{rule.name}"), inher, children))

            # add on child node 
            child_inher = {f'self.traverse_{type_name}_{rule.name}_{lib.rule.relation_from_item(item)}(inher, children)'}
            stack.append((self.next(child_inher), child_inher, ()))
            ''' 
            for i, item in enumerate(abstract_items)
            if lib.rule.type_from_item(item) == type_name
        ])}
        else:
            raise AnalysisError()
    """

def generate_traverse_choice_rule(type_name : str, rule : Rule) -> str:
    abstract_items = lib.rule.get_abstract_items(rule)
    return ''.join([f"""
    def traverse_{type_name}_{rule.name}_{lib.rule.relation_from_item(item)}(self, inher : I, synth_preds : tuple[S, ...]) -> I:
        return inher
    """
        for item in abstract_items
    ])

def generate_traverse_single_rule(rule : Rule) -> str:
    abstract_items = lib.rule.get_abstract_items(rule)
    return ''.join([f"""
    def traverse_{rule.name}_{lib.rule.relation_from_item(item)}(self, inher : I, synth_preds : tuple[S, ...]) -> I:
        return inher
    """
        for item in abstract_items
    ])

def generate_analyze_inductive_choice_rules(
    type_name : str, 
    rules : list[Rule]
) -> str:

    return (f"""
    def analyze_token_{type_name}(self, 
        token : Grammar, 
        inher : I, children : tuple[S, ...], stack_result : Optional[S], 
        stack : list[tuple[abstract_token, I, tuple[S, ...]]]
    ) -> Optional[S]:
        assert token.options == "{type_name}"
        rule_name = token.selection

        if False: 
            pass
        {nl.join([
            f'''
        elif rule_name == "{rule.name}": 
            return self.analyze_token_{type_name}_{rule.name}(inher, children, stack_result, stack)
            '''
            for rule in rules
        ])}
        else:
            raise AnalysisError()



    def analyze_{type_name}(self, inher : I) -> S:

        stack : list[tuple[abstract_token, I, tuple[S, ...]]] = [(self.next(inher), inher, ())]

        stack_result : Optional[S] = None 
        while stack:

            (token, inher, children) = stack.pop()

            assert isinstance(token, Grammar)
            stack_result = self.analyze_token_{type_name}(token, inher, children, stack_result, stack)

        assert stack_result
        return stack_result

    """)

def generate_analyze_token_noninduct_choice_rule(type_name : str, rule : Rule) -> str:
    abstract_items = lib.rule.get_abstract_items(rule)
    nl = "\n"

    return (f"""
    def analyze_token_{type_name}_{rule.name}(self, inher : I) -> S:
        synth_children = () 

        {''.join([
            f'''
        synth = self.analyze_{lib.rule.type_from_item(item)}({f'self.traverse_{type_name}_{rule.name}_{lib.rule.relation_from_item(item)}(inher, synth_children)'})
        synth_children += tuple([synth])
        '''
            for item in abstract_items
        ])}

        return self.synthesize_{type_name}_{rule.name}_attributes(inher, synth_children)
    """)

def generate_analyze_noninduct_choice_rules(type_name : str, rules : list[Rule]) -> str:
    nl = "\n"

    return (f"""
    def analyze_token_{type_name}(self, token : Grammar, inher : I) -> S:
        assert token.options == "{type_name}"

        if False:
            pass
        {nl.join([
            f'''
        elif token.selection == "{rule.name}":
            return self.analyze_token_{type_name}_{rule.name}(inher)
            '''
            for rule in rules
        ])}
        else:
            raise AnalysisError()

    def analyze_{type_name}(self, inher : I) -> S:
        token = self.next(inher)
        assert isinstance(token, Grammar)
        return self.analyze_token_{type_name}(token, inher)

    """)

def generate_procedures_choice_rules(type_name : str, rules : list[Rule]) -> str:
    if lib.rule.is_inductive(type_name, rules):
        return (
            f"\n    # {type_name}" +
            generate_analyze_inductive_choice_rules(type_name, rules) +
            "".join([
                (
                    f"\n    # {type_name} <-- {rule.name}" +
                    generate_analyze_token_inductive_choice_rule(type_name, rule) +
                    generate_traverse_choice_rule(type_name, rule) +
                    generate_synthesize_choice_rule(type_name, rule)
                )
                for rule in rules
            ])
        )
    else: 
        return (
            f"\n    # {type_name}" +
            generate_analyze_noninduct_choice_rules(type_name, rules) +
            "".join([
                (

                    f"\n    # {type_name} <-- {rule.name}" +
                    generate_analyze_token_noninduct_choice_rule(type_name, rule) + nl +
                    generate_traverse_choice_rule(type_name, rule) +
                    generate_synthesize_choice_rule(type_name, rule)
                )
                for rule in rules
            ])
        )


def generate_procedures_single_rule(rule : Rule) -> str:
    return (
        f"\n    # {rule.name}" +
        generate_analyze_single_rule(rule) +
        generate_analyze_token_single_rule(rule) +
        generate_traverse_single_rule(rule) +
        generate_synthesize_single_rule(rule)
    )

def generate_analyze_single_rule(rule : Rule) -> str:
    return (f"""
    def analyze_{rule.name}(self, inher : I) -> S:
        token = self.next(inher)
        assert isinstance(token, Grammar)
        assert token.options == "{rule.name}"

        return self.analyze_token_{rule.name}(token, inher)
    """)

def generate_analyze_token_single_rule(rule : Rule) -> str:

    abstract_items = lib.rule.get_abstract_items(rule)
    nl = "\n"

    return (f"""
    def analyze_token_{rule.name}(self, token : Grammar, inher : I) -> S:
        assert token.selection == "{rule.name}"

        synth_children = () 
        {''.join([
            f'''
        synth = self.analyze_{lib.rule.type_from_item(item)}({f'self.traverse_{rule.name}_{lib.rule.relation_from_item(item)}(inher, synth_children)'})
        synth_children += tuple([synth])
            ''' 
            for item in abstract_items
        ])}
        return self.synthesize_{rule.name}_attributes(inher, synth_children)
    """)



def generate_synthesize_choice_rule(type_name : str, rule : Rule) -> str:
    rule_name = rule.name
    return f"""
    def synthesize_{type_name}_{rule_name}_attributes(self, inher : I, synth_children : tuple[S, ...]) -> S:
        return self.default_synth(inher)
    """

def generate_synthesize_single_rule(rule : Rule) -> str:
    return f"""
    def synthesize_{rule.name}_attributes(self, inher : I, synth_children : tuple[S, ...]) -> S:
        return self.default_synth(inher)
    """


def generate_content(singles : list[Rule], choices : dict[str, list[Rule]]) -> str:
    return (f"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, TypeVar, Any, Generic, Union, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod

I = TypeVar('I')
S = TypeVar('S')

import lib.abstract_token
from lib.abstract_token_construct_autogen import abstract_token, Vocab, Grammar
from lib.python_ast_construct_autogen import *
from lib.line_format_construct_autogen import InLine, NewLine, IndentLine

from pyrsistent import s, m, pmap, v, PRecord, field
from pyrsistent.typing import PMap, PSet
from queue import Queue

class AnalysisError(Exception):
    pass

class Server(ABC, Generic[I, S]): 

    def __init__(self, in_stream : Queue[abstract_token], out_stream : Queue[I]):  

        def next(inher : I) -> abstract_token: 
            out_stream.put(inher)
            return in_stream.get()

        self.next = next


    {nl.join([
        generate_procedures_choice_rules(type_name, rules)
        for type_name, rules in choices.items()
    ])} 

    {nl.join([
        generate_procedures_single_rule(rule)
        for rule in singles
    ])} 


    def analyze_token_str(self, token : Vocab, inher : I) -> S:
        return self.default_synth(inher)

    def analyze_str(self, inher : I) -> S:
        token = self.next(inher)
        assert isinstance(token, Vocab)
        return self.analyze_token_str(token, inher)

    @abstractmethod
    def default_synth(self, inher : I) -> S: pass

    """)