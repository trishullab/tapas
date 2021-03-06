from __future__ import annotations

from dataclasses import dataclass

from tapas_base import rule_system
from tapas_base.rule_system import Rule

from typing import Optional


nl = "\n"


def synth_args(rule : Rule, index : int, indent : int = 3):
    abstract_items = rule_system.get_abstract_items(rule)
    return ''.join([
        "," + f'''
{"    " * indent + rule_system.relation_from_item(inner_item)}_tree, 
{"    " * indent + rule_system.relation_from_item(inner_item)}_aux'''
        for i, inner_item in enumerate(abstract_items)
        if i < index 
    ])


def assign_synths(rule : Rule, index : int):
    abstract_items = rule_system.get_abstract_items(rule)
    return ''.join([
        f'''
            {rule_system.relation_from_item(inner_item)}_tree = children[{i}].tree
            assert isinstance({rule_system.relation_from_item(inner_item)}_tree, {rule_system.type_from_item(inner_item)})
            {rule_system.relation_from_item(inner_item)}_aux = children[{i}].aux'''
        for i, inner_item in enumerate(abstract_items)
        if i < index 
    ])



def generate_inspect_inductive_choice_rule(type_name : str, rule : Rule):
    abstract_items = rule_system.get_abstract_items(rule)
    return f"""
    # inspect: {type_name} <-- {rule.name}
    def inspect_{type_name}_{rule.name}(self,
        inher_aux : InherAux, children : tuple[Result[SynthAux], ...], stack_result : Optional[Result[SynthAux]], 
        stack : list[tuple[abstract_token, InherAux, tuple[Result[SynthAux], ...]]]
    ) -> Optional[Result[SynthAux]]:

        {f'''
        if stack_result:
            # get the result from the child in the stack
            children = children + (stack_result,)
        ''' if rule_system.is_inductive(type_name, [rule]) else ''}

        total_num_children = {len(abstract_items)}

        index = len(children)
        if index == total_num_children:
            # the processing of the current rule has completed
            # return the analysis result to the previous item in the stack
            {''.join([
                f'''
            {rule_system.relation_from_item(item)}_tree = children[{i}].tree
            assert isinstance({rule_system.relation_from_item(item)}_tree, {rule_system.type_from_item(item)})
            {rule_system.relation_from_item(item)}_aux = children[{i}].aux
                '''
                for i, item in enumerate(abstract_items)
            ])}
            return self.synthesize_for_{type_name}_{rule.name}(inher_aux{f''.join([
                f''', {rule_system.relation_from_item(item)}_tree, {rule_system.relation_from_item(item)}_aux'''
                for item in abstract_items
            ])})
        {nl.join([
            f'''
        elif index == {i}: # index does *not* refer to an inductive child

            {assign_synths(rule, i)}


            child_inher_aux = self.traverse_{type_name}_{rule.name}_{rule_system.relation_from_item(item)}(
                inher_aux{synth_args(rule, i, 4)}
            )
            child_token = self.next(child_inher_aux)
            child_synth = self.crawl_{rule_system.type_from_item(item, "")}(child_token, child_inher_aux)

            stack.append((make_Grammar("{type_name}", "{rule.name}"), inher_aux, children + (child_synth,)))
            return None
            '''
            for i, item in enumerate(abstract_items)
            if rule_system.type_from_item(item, "") != type_name
        ])}
        {nl.join([
            f'''
        elif index == {i} : # index refers to an inductive child
            # put back current node
            stack.append((make_Grammar("{type_name}", "{rule.name}"), inher_aux, children))

            {assign_synths(rule, i)}

            # add on child node 
            child_inher_aux = self.traverse_{type_name}_{rule.name}_{rule_system.relation_from_item(item)}(
                inher_aux{synth_args(rule, i, 4)}
            )
            stack.append((self.next(child_inher_aux), child_inher_aux, ()))
            ''' 
            for i, item in enumerate(abstract_items)
            if rule_system.type_from_item(item, "") == type_name
        ])}
        else:
            raise SyntaxError()
    """

def generate_traverse_choice_rule(type_name : str, rule : Rule) -> str:
    abstract_items = rule_system.get_abstract_items(rule)
    return ''.join([f"""
    # traverse {type_name} <-- {rule.name}"
    def traverse_{type_name}_{rule.name}_{rule_system.relation_from_item(item)}(self, 
        inher_aux : InherAux{f''.join([
        "," + f'''
        {rule_system.relation_from_item(inner_item)}_tree : {rule_system.type_from_item(inner_item)}, 
        {rule_system.relation_from_item(inner_item)}_aux : SynthAux'''
        for i, inner_item in enumerate(abstract_items)
        if i < index 
        ])}
    ) -> InherAux:
        return self.traverse_auxes(inher_aux, ({f' '.join([
            f"{rule_system.relation_from_item(inner_item)}_aux,"
            for i, inner_item in enumerate(abstract_items)
            if i < index 
        ])}), '{rule_system.type_from_item(item)}') 
    """
        for index, item in enumerate(abstract_items)
    ])

def generate_traverse_single_rule(rule : Rule) -> str:
    abstract_items = rule_system.get_abstract_items(rule)
    return ''.join([f"""
    # traverse {rule.name}
    def traverse_{rule.name}_{rule_system.relation_from_item(item)}(self,
        inher_aux : InherAux{f''.join([
        "," + f'''
        {rule_system.relation_from_item(inner_item)}_tree : {rule_system.type_from_item(inner_item)}, 
        {rule_system.relation_from_item(inner_item)}_aux : SynthAux'''
        for i, inner_item in enumerate(abstract_items)
        if i < index 
        ])}
    ) -> InherAux:
        return self.traverse_auxes(inher_aux, ({f' '.join([
            f"{rule_system.relation_from_item(inner_item)}_aux,"
            for i, inner_item in enumerate(abstract_items)
            if i < index 
        ])}), '{rule_system.type_from_item(item)}') 
    """
        for index, item in enumerate(abstract_items)
    ])

def generate_crawl_inductive_choice_rules(
    type_name : str, 
    rules : list[Rule]
) -> str:
    return (f""" # inspect: {type_name}
    def inspect_{type_name}(self, 
        token : Grammar, 
        inher_aux : InherAux, children : tuple[Result[SynthAux], ...], stack_result : Optional[Result[SynthAux]], 
        stack : list[tuple[abstract_token, InherAux, tuple[Result[SynthAux], ...]]]
    ) -> Optional[Result[SynthAux]]:
        if token.options != "{type_name}": raise SyntaxError()
        rule_name = token.selection

        if False: 
            pass
        {nl.join([
            f'''
        elif rule_name == "{rule.name}": 
            return self.inspect_{type_name}_{rule.name}(inher_aux, children, stack_result, stack)
            '''
            for rule in rules
        ])}
        else:
            raise SyntaxError()



    def crawl_{type_name}(self, token : abstract_token, inher_aux : InherAux) -> Result[SynthAux]:

        stack : list[tuple[abstract_token, InherAux, tuple[Result[SynthAux], ...]]] = [(token, inher_aux, ())]

        stack_result : Optional[Result[SynthAux]] = None 
        while stack:

            (token, inher_aux, children) = stack.pop()

            if not isinstance(token, Grammar): raise SyntaxError()
            stack_result = self.inspect_{type_name}(token, inher_aux, children, stack_result, stack)

        assert stack_result
        return stack_result

    """)



def generate_inspect_noninduct_choice_rule(type_name : str, rule : Rule) -> str:
    abstract_items = rule_system.get_abstract_items(rule)

    return (f"""
    # inspect: {type_name} <-- {rule.name}"
    def inspect_{type_name}_{rule.name}(self, inher_aux : InherAux) -> Result[SynthAux]:


        {''.join([
            f'''
        child_inher_aux = self.traverse_{type_name}_{rule.name}_{rule_system.relation_from_item(item)}(
            inher_aux{synth_args(rule, i, 3)}
        )
        child_token = self.next(child_inher_aux)
        synth = self.crawl_{rule_system.type_from_item(item, "")}(child_token, child_inher_aux)
        {rule_system.relation_from_item(item)}_tree = synth.tree
        assert isinstance({rule_system.relation_from_item(item)}_tree, {rule_system.type_from_item(item)})
        {rule_system.relation_from_item(item)}_aux = synth.aux
        '''
            for i, item in enumerate(abstract_items)
        ])}

        return self.synthesize_for_{type_name}_{rule.name}(inher_aux{f''.join([
            f''', {rule_system.relation_from_item(item)}_tree, {rule_system.relation_from_item(item)}_aux'''
            for item in abstract_items
        ])})
    """)

def generate_crawl_noninduct_choice_rules(type_name : str, rules : list[Rule]) -> str:
    return (f"""
    # inspect {type_name}"
    def inspect_{type_name}(self, token : Grammar, inher_aux : InherAux) -> Result[SynthAux]:
        if token.options != "{type_name}": raise SyntaxError()

        if False:
            pass
        {nl.join([
            f'''
        elif token.selection == "{rule.name}":
            return self.inspect_{type_name}_{rule.name}(inher_aux)
            '''
            for rule in rules
        ])}
        else:
            raise SyntaxError()

    def crawl_{type_name}(self, token : abstract_token, inher_aux : InherAux) -> Result[SynthAux]:
        if not isinstance(token, Grammar): raise SyntaxError()
        return self.inspect_{type_name}(token, inher_aux)

    """)


def generate_crawl_single_rule(rule : Rule) -> str:
    return (f"""
    # crawl {rule.name}" +
    def crawl_{rule.name}(self, token : abstract_token, inher_aux : InherAux) -> Result[SynthAux]:
        if not isinstance(token, Grammar): raise SyntaxError()
        if token.options != "{rule.name}": raise SyntaxError()

        return self.inspect_{rule.name}(token, inher_aux)
    """)

def generate_inspect_single_rule(rule : Rule) -> str:

    abstract_items = rule_system.get_abstract_items(rule)

    return (f"""
    # inspect: {rule.name}"
    def inspect_{rule.name}(self, token : Grammar, inher_aux : InherAux) -> Result[SynthAux]:
        if token.selection != "{rule.name}": raise SyntaxError()
        {''.join([
            f'''

        child_inher_aux = self.traverse_{rule.name}_{rule_system.relation_from_item(item)}(
            inher_aux{synth_args(rule, i, 3)}
        )
        child_token = self.next(child_inher_aux)
        synth = self.crawl_{rule_system.type_from_item(item, "")}(child_token, child_inher_aux)
        {rule_system.relation_from_item(item)}_tree = synth.tree
        assert isinstance({rule_system.relation_from_item(item)}_tree, {rule_system.type_from_item(item)})
        {rule_system.relation_from_item(item)}_aux = synth.aux
            ''' 
            for i, item in enumerate(abstract_items)
        ])}


        return self.synthesize_for_{rule.name}(inher_aux{f''.join([
            f''', {rule_system.relation_from_item(item)}_tree, {rule_system.relation_from_item(item)}_aux'''
            for item in abstract_items
        ])})
    """)

def generate_synthesize_rule(type_name : Optional[str], rule : Rule) -> str:
    abstract_items = rule_system.get_abstract_items(rule)

    function_name = (
        f"synthesize_for_{type_name}_{rule.name}"
        if type_name else
        f"synthesize_for_{rule.name}"
    )

    return f"""
    def {function_name}(self, 
        inher_aux : InherAux{f''.join([
        "," + f'''
        {rule_system.relation_from_item(item)}_tree : {rule_system.type_from_item(item)}, 
        {rule_system.relation_from_item(item)}_aux : SynthAux'''
        for item in abstract_items
        ])}
    ) -> Result[SynthAux]:
        return Result[SynthAux](
            tree = make_{rule.name}({f', '.join([
                f"{rule_system.relation_from_item(item)}_tree"
                for item in abstract_items
            ])}),
            aux = self.synthesize_auxes(({f' '.join([
                f"{rule_system.relation_from_item(item)}_aux,"
                for item in abstract_items
            ])})) 
        )
    """

def generate_synthesize_choice_rule(type_name : str, rule : Rule) -> str:
    return (f"\n    # synthesize: {type_name} <-- {rule.name}" +
        generate_synthesize_rule(type_name, rule)
    )

def generate_synthesize_single_rule(rule : Rule) -> str:
    return (f"\n    # synthesize: {rule.name}" +
        generate_synthesize_rule(None, rule)
    )

def generate_crawl_choice_rules(type_name : str, rules : list[Rule]) -> str:
    if rule_system.is_inductive(type_name, rules):
        return generate_crawl_inductive_choice_rules(type_name, rules)
    else: 
        return generate_crawl_noninduct_choice_rules(type_name, rules)

def generate_inspect_choice_rules(type_name : str, rules : list[Rule]) -> str:
    if rule_system.is_inductive(type_name, rules):
        return ''.join([
            generate_inspect_inductive_choice_rule(type_name, rule)
            for rule in rules
        ])
    else: 
        return ''.join([
            generate_inspect_noninduct_choice_rule(type_name, rule)
            for rule in rules
        ])

def generate_traverse_choice_rules(type_name : str, rules : list[Rule]) -> str:
    return ''.join([
        generate_traverse_choice_rule(type_name, rule)
        for rule in rules
    ])

def generate_synthesize_choice_rules(type_name : str, rules : list[Rule]) -> str:
    return ''.join([
        generate_synthesize_choice_rule(type_name, rule)
        for rule in rules
    ])


from tapas_base.construct_def import Constructor, Field
from tapas_base import construct_def

header = (f"""
from __future__ import annotations

from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Dict, TypeVar, Any, Generic, Union, Optional, Iterable
from collections.abc import Callable

from tapas_base.abstract_token_construct_autogen import abstract_token, Vocab, Grammar, make_Grammar

from queue import Queue
""")

def generate_content(
    content_header : str,
    singles : list[Rule], 
    choices : dict[str, list[Rule]]
) -> str:
    return (f"""

{header}

{content_header}

InherAux = TypeVar('InherAux') 
SynthAux = TypeVar('SynthAux') 

class SyntaxError(Exception):
    pass

@dataclass(frozen=True, eq=True)
class Result(Generic[SynthAux]):
    tree : ast
    aux : SynthAux


class Server(ABC, Generic[InherAux, SynthAux]): 

    def __init__(self, in_stream : Queue[abstract_token | Exception], out_stream : Queue[InherAux | Exception]):  

        def next(inher_aux : InherAux) -> abstract_token: 
            out_stream.put(inher_aux)
            tok = in_stream.get()
            if isinstance(tok, Exception):
                raise tok
            else:
                return tok

        self.next = next


    {''.join([
        generate_crawl_choice_rules(type_name, rules)
        for type_name, rules in choices.items()
    ])} 
    {''.join([
        generate_crawl_single_rule(rule)
        for rule in singles
    ])} 

    {''.join([
        generate_inspect_choice_rules(type_name, rules)
        for type_name, rules in choices.items()
    ])} 
    {''.join([
        generate_inspect_single_rule(rule)
        for rule in singles
    ])} 

    {''.join([
        generate_traverse_choice_rules(type_name, rules)
        for type_name, rules in choices.items()
    ])} 
    {''.join([
        generate_traverse_single_rule(rule)
        for rule in singles
    ])} 

    {''.join([
        generate_synthesize_choice_rules(type_name, rules)
        for type_name, rules in choices.items()
    ])} 
    {''.join([
        generate_synthesize_single_rule(rule)
        for rule in singles
    ])} 



    def inspect_str(self, token : Vocab, inher_aux : InherAux) -> Result[SynthAux]:
        return Result[SynthAux](
            tree = token.selection,
            aux = self.synthesize_auxes(()) 
        ) 

    def crawl_str(self, token : abstract_token, inher_aux : InherAux) -> Result[SynthAux]:
        if not isinstance(token, Vocab): raise SyntaxError()
        return self.inspect_str(token, inher_aux)

    @abstractmethod
    def traverse_auxes(self, inher_aux : InherAux, synth_auxes : tuple[SynthAux, ...], target_syntax_type : str) -> InherAux:
        pass

    @abstractmethod
    def synthesize_auxes(self, auxes : tuple[SynthAux, ...]) -> SynthAux:
        pass

    """)
