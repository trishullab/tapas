
from __future__ import annotations

from dataclasses import dataclass

import lib.rule_system
from lib.rule_system import Rule

from lib import python_schema_system

import lib.python_schema_system
import inflection

nl = "\n"
def generate_crawl_inductive_choice_rules(
    type_name : str, 
    rules : list[Rule]
) -> str:

    handlers_name = f"{inflection.camelize(type_name)}Handlers"

    return (f"""
    def crawl_{type_name}(self, part : {type_name}, inher : Inher) -> Synth:

        stack : list[tuple[{type_name}, I, tuple[Synth, ...]]] = [(part, inher, ())]

        stack_result : Optional[Synth] = None 
        while stack:

            (inher, children) = stack.pop()

            stack_result = match_{type_name}(part, {handlers_name}(
            {f",{nl}".join([
                f'''case_{rule.name} = self.crawl_{type_name}_{rule.name}(part, inher, children, stack_result, stack)'''
                for rule in rules 
            ])}
            ))


        assert stack_result
        return stack_result

    """)


def generate_crawl_noninduct_choice_rules(type_name : str, rules : list[Rule]) -> str:

    handlers_name = f"{inflection.camelize(type_name)}Handlers"

    return (f"""
    def crawl_{type_name}(self, part : {type_name}, inher : Inher) -> Synth:

        return match_{type_name}(part, {handlers_name}(
        {f",{nl}".join([
            f'''case_{rule.name} = self.crawl_{type_name}_{rule.name}(part, inher)'''
            for rule in rules 
        ])}
        ))
    """)

def generate_crawl_inductive_choice_rule(type_name : str, rule : Rule):

    abstract_items = lib.rule_system.get_abstract_items(rule)
    return f"""
    def crawl_{type_name}_{rule.name}(self,
        part : {rule.name},
        inher : Inher, children : tuple[Synth, ...], stack_result : Optional[Synth], 
        stack : list[tuple[{type_name}, I, tuple[Synth, ...]]]
    ) -> Optional[Synth]:

        {f'''
        if stack_result:
            # get the result from the child in the stack
            children = children + tuple([stack_result]) 
        ''' if lib.rule_system.is_inductive(type_name, [rule]) else ''}

        total_num_children = {len(abstract_items)}

        index = len(children)
        if index == total_num_children:
            # the processing of the current rule has completed
            # return the analysis result to the previous item in the stack
            return self.synthesize_{type_name}_{rule.name}_attributes(inher, children)
        {nl.join([
            f'''
        elif index == {i}: # index does *not* refer to an inductive child

            child_synth = self.crawl_{lib.rule_system.type_from_item(item, '')}(
                {f'part.{lib.rule_system.relation_from_item(item)}, inher'}
            )
            stack.append((part, inher, children + tuple([child_synth])))
            return None
            '''
            for i, item in enumerate(abstract_items)
            if lib.rule_system.type_from_item(item, '') != type_name
        ])}
        {nl.join([
            f'''
        elif index == {i} : # index refers to an inductive child
            # put back current node
            stack.append((part, inher, children))

            # add on child node 
            stack.append((part.{lib.rule_system.relation_from_item(item)}, inher, ()))
            ''' 
            for i, item in enumerate(abstract_items)
            if lib.rule_system.type_from_item(item, '') == type_name
        ])}
        else:
            raise AnalysisError()
    """

def generate_crawl_noninduct_choice_rule(type_name : str, rule : Rule) -> str:
    abstract_items = lib.rule_system.get_abstract_items(rule)

    return (f"""
    def crawl_{type_name}_{rule.name}(self, part : {rule.name}, inher : Inher) -> Synth:
        {''.join([
            f'''
        {lib.rule_system.relation_from_item(item)}_synth : {lib.rule_system.type_from_item(item, 'ast_sys')} = self.crawl_{lib.rule_system.type_from_item(item, '')}(
            {f'part.{lib.rule_system.relation_from_item(item)}'}
        )
            ''' 
            for item in abstract_items
        ])}
        return self.synthesize_for_{rule.name}(inher, 
            {','.join([
                f'''{lib.rule_system.relation_from_item(item)}_synth''' 
                for item in abstract_items
            ])}
        )
    """)



def generate_crawl_single_rule(rule : Rule) -> str:

    abstract_items = lib.rule_system.get_abstract_items(rule)

    return (f"""
    def crawl_{rule.name}(self, part : {rule.name}, inher : Inher) -> Synth:
        {''.join([
            f'''
        {lib.rule_system.relation_from_item(item)}_synth : {lib.rule_system.type_from_item(item, 'ast_sys')} = self.crawl_{lib.rule_system.type_from_item(item, '')}(
            {f'part.{lib.rule_system.relation_from_item(item)}'}
        )
            ''' 
            for item in abstract_items
        ])}
        return self.synthesize_for_{rule.name}(inher, 
            {','.join([
                f'''{lib.rule_system.relation_from_item(item)}_synth''' 
                for item in abstract_items
            ])}
        )
    """)



def generate_synthesize_choice_rule(type_name : str, rule : Rule) -> str:
    abstract_items = lib.rule_system.get_abstract_items(rule)

    return f"""
    def synthesize_for_{type_name}_{rule.name}(self, inher : Inher, 
        {','.join([
            f'''{lib.rule_system.relation_from_item(item)}_synth : Synth''' 
            for item in abstract_items
        ])}
    ) -> Synth:
        return self.default_synth(inher)
    """

def generate_synthesize_single_rule(rule : Rule) -> str:
    abstract_items = lib.rule_system.get_abstract_items(rule)
    return f"""
    def synthesize_for_{rule.name}(self, inher : Inher, 
        {','.join([
            f'''{lib.rule_system.relation_from_item(item)}_synth : Synth''' 
            for item in abstract_items
        ])}
    ) -> Synth:
        return self.default_synth(inher)
    """


def generate_procedures_choice_rules(type_name : str, rules : list[Rule]) -> str:
    if lib.rule_system.is_inductive(type_name, rules):
        return (
            f"\n    # {type_name}" +
            generate_crawl_inductive_choice_rules(type_name, rules) +
            "".join([
                (
                    f"\n    # {type_name} <-- {rule.name}" +
                    generate_crawl_inductive_choice_rule(type_name, rule) +
                    generate_synthesize_choice_rule(type_name, rule)
                )
                for rule in rules
            ])
        )
    else: 
        return (
            f"\n    # {type_name}" +
            generate_crawl_noninduct_choice_rules(type_name, rules) +
            "".join([
                (

                    f"\n    # {type_name} <-- {rule.name}" +
                    generate_crawl_noninduct_choice_rule(type_name, rule) + nl +
                    generate_synthesize_choice_rule(type_name, rule)
                )
                for rule in rules
            ])
        )


def generate_procedures_single_rule(rule : Rule) -> str:
    return (
        f"\n    # {rule.name}" +
        generate_crawl_single_rule(rule) +
        generate_synthesize_single_rule(rule)
    )

header = (f"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, TypeVar, Any, Generic, Union, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod

I = TypeVar('I')
S = TypeVar('S')

from lib.python_ast_construct_autogen import *
from lib.line_format_construct_autogen import InLine, NewLine, IndentLine

from pyrsistent import PMap, m, pmap, PSet, s, pset, v, PRecord, field
from queue import Queue
from lib.abstract_token_system import abstract_token, Vocab, Grammar

""")


from lib.construct_def import Constructor, Field
from lib import construct_def

def generate_content(content_header : str, singles : list[Rule], choices : dict[str, list[Rule]]) -> str:
    return (f"""

{header}

{content_header}

class Error(Exception):
    pass

{construct_def.generate_single(
    Constructor("Synth", [], [
        Field("content", "Optional[Aux]", "None"),
    ])
)}


class Server(Generic[Inher, Aux]): 

    def __init__(self):  
        pass


    {nl.join([
        generate_procedures_choice_rules(type_name, rules)
        for type_name, rules in choices.items()
    ])} 

    {nl.join([
        generate_procedures_single_rule(rule)
        for rule in singles
    ])} 


    def crawl_str(self, part : str, vocab : str, inher : Inher) -> Synth:
        return self.default_synth(inher)

    """)