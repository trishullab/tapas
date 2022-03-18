from __future__ import annotations

from dataclasses import dataclass
from tkinter.messagebox import NO
from typing import Dict, TypeVar, Any, Generic, Union, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod
from _distutils_hack import override

from numpy import isin
from pkg_resources import declare_namespace

T = TypeVar('T')

from lib.abstract_token_construct_autogen import abstract_token, Vocab, Grammar
from lib.python_ast_construct_autogen import *
from lib.line_format_construct_autogen import InLine, NewLine, IndentLine

from pyrsistent import pmap, m, s
from pyrsistent.typing import PMap, PSet

from queue import Queue

from lib.python_abstract_token_analyze_autogen import Server as BaseServer, AnalysisError

from lib import python_ast

from lib import python_util

from lib.python_util import Declaration, Inher, from_Inher_to_string, \
    set_delete_mode, set_attribute_mode, set_local_env, set_class_mode, set_function_mode, set_pattern_target_mode, set_name_target_mode, set_source_mode, set_import_mode, set_open_mode, \
    synth, NoSynth, DeleteSynth, LocalEnvSynth, SourceSynth, TargetSynth, MultiTargetSynth, OpenSynth, ImportSynth, \
    mode, DeleteMode, ModuleMode, ClassMode, FunctionMode, PatternTargetMode, NameTargetMode, SourceMode, OpenMode, ImportMode, AttributeMode

# definitions operate on a mutable queue (i.e. stream) of abstract_tokens 

# if assignment is used on a name in both target and source, and it's not in local scope, 
# then either global or nonlocal keyword is required 

# When entering a definition or lambda body, local inher flows:
# - into global inher if it's at module level,
# - into nonlocal inher if it's *not* at module level,

# collect names from target expression 
# traverse source expression. NOTE: This order is necessary due to incremental processing from left tree to right.
# There are three types of context for traversing of expressions:
# - target context, source context, statement context  
# - source context carries names from target
# For a source name, if it is a target name but not local, raise error - name update out of scope.
# at assignment (statement) level, add target names to local inher
# When nonlocal or global keywords are seen, copy names from respective inherironment to local inher. 

# ISSUE: how to handle forward references with incremental processing?
# collect all function and class def identifiers to pass into local scope of all nested scopes. 



def target_synth_f(children : tuple[synth, ...]) -> TargetSynth:
    # merge targets from child synths
    names : PSet[str] = s() 
    for child_synth in children:
        if isinstance(child_synth, TargetSynth):
            names = names.update(child_synth.env_names)
        else:
            pass
            # assert isinstance(child_synth, NoSynth)

    tokens : tuple[abstract_token, ...] = ()
    for child_synth in children:
        if isinstance(child_synth, TargetSynth):
            tokens = tokens + child_synth.tokens
        else:
            pass
            # assert isinstance(child_synth, NoSynth)

    return TargetSynth(
        env_names = names,
        tokens = tokens 
    )


def specialize_tuple_SourceSynth(things : tuple[synth, ...]) -> tuple[SourceSynth, ...]:
    ss_acc : list[SourceSynth] = []
    for c in things:
        if isinstance(c, SourceSynth):
            ss_acc.append(c)

    return tuple(ss_acc)

def source_synth_f(children : tuple[synth, ...]) -> SourceSynth:

    ss_children = specialize_tuple_SourceSynth(children)


    declarations : PMap[str, Declaration] = m()
    used_names : PSet[str] = s() 
    tokens : tuple[abstract_token, ...] = ()
    for child_synth in ss_children:
        declarations = declarations + child_synth.env_additions
        used_names = used_names.update(child_synth.env_refs)
        tokens = tokens + child_synth.tokens

    return SourceSynth(
        env_additions = declarations,
        env_refs = used_names,
        tokens = tokens 
    )

def local_env_synth_f(children : tuple[synth, ...]) -> LocalEnvSynth:
    declarations : PMap[str, Declaration] = m()
    for child_synth in children:
        assert isinstance(child_synth, LocalEnvSynth)
        declarations = declarations + child_synth.additions

    return LocalEnvSynth(subtractions = s(), additions = declarations)

class Server(BaseServer[Union[Exception, Inher], synth]):

    def __init__(self, in_stream : Queue[abstract_token], out_stream : Queue[Union[Inher, Exception]]):  
        super().__init__(in_stream, out_stream)

    def default_synth(self, inher : Inher) -> synth:
        return NoSynth()


    # module <-- FutureMod
    def synthesize_module_FutureMod_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return synth_children[-1] 

    # module <-- SimpleMod
    def synthesize_module_SimpleMod_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return synth_children[-1] 

    # statements <-- ConsStmt
    def traverse_statements_ConsStmt_head(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return inher
    
    def traverse_statements_ConsStmt_tail(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        assert len(synth_preds) == 1
        head_synth = synth_preds[0]



        if isinstance(head_synth, LocalEnvSynth):
            env = inher.local_env
            for x in head_synth.subtractions:
                env = env.remove(x)

            return set_local_env(inher, env + head_synth.additions)
        else:
            assert isinstance(head_synth, NoSynth)
            return inher
    
    def synthesize_statements_ConsStmt_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:

        assert len(synth_children) == 2
        hd = synth_children[0]
        tl = synth_children[1]

        hd_additions : PMap[str, Declaration] = m()
        subtractions : PSet[str] = s()
        if isinstance(hd, LocalEnvSynth):
            hd_additions = hd.additions
            subtractions = hd.subtractions
        else:
            assert isinstance(hd, NoSynth)

        assert isinstance(tl, LocalEnvSynth)

        for sub in tl.subtractions:
            if hd_additions.get(sub):
                hd_additions = hd_additions.remove(sub)

        for sub in tl.subtractions:
            subtractions.add(sub)

        return LocalEnvSynth(subtractions = subtractions, additions = hd_additions + tl.additions)

    # stmt <-- DecClassDef

    # def traverse_stmt_DecClassDef_decs(self, inher : I, synth_preds : tuple[S, ...]) -> I:
    #     return inher
    
    # def traverse_stmt_DecClassDef_class_def(self, inher : I, synth_preds : tuple[S, ...]) -> I:
    #     return inher
    
    def synthesize_stmt_DecClassDef_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 2
        class_synth = synth_children[1]
        return class_synth

    # ClassDef
    def traverse_ClassDef_name(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_name_target_mode(inher)
    
    def traverse_ClassDef_bs(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return inher
    
    def traverse_ClassDef_body(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_class_mode(inher)

    
    def synthesize_ClassDef_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 3 
        name_synth = synth_children[0]
        assert isinstance(name_synth, TargetSynth)

        declaration_map : PMap[str, Declaration] = m()
        for name in name_synth.env_names:
            declaration_map = declaration_map.set(name, Declaration(initialized=True))

        return LocalEnvSynth(s(), declaration_map)


    # statements <-- SingleStmt
    def synthesize_statements_SingleStmt_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 1
        stmt_synth = synth_children[0]
        if isinstance(stmt_synth, LocalEnvSynth):
            return stmt_synth
        else:
            assert isinstance(stmt_synth, NoSynth)
            return LocalEnvSynth(s(), m())

    # stmt <-- DecFunctionDef
    # def traverse_stmt_DecFunctionDef_decs(self, inher : I, synth_preds : tuple[S, ...]) -> I:
    #     return inher
    
    # def traverse_stmt_DecFunctionDef_fun_def(self, inher : I, synth_preds : tuple[S, ...]) -> I:
    #     return inher
    
    def synthesize_stmt_DecFunctionDef_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 2
        fun_synth = synth_children[1]
        return fun_synth


    # function_def <-- FunctionDef
    def traverse_function_def_FunctionDef_name(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_name_target_mode(inher)
    
    # def traverse_function_def_FunctionDef_params(self, inher : I, synth_preds : tuple[S, ...]) -> I:
    #     return inher
    
    # def traverse_function_def_FunctionDef_ret_anno(self, inher : I, synth_preds : tuple[S, ...]) -> I:
    #     return inher
    
    def traverse_function_def_FunctionDef_body(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        len(synth_preds) == 3
        params_synth = synth_preds[1]
        assert isinstance(params_synth, LocalEnvSynth)
        assert len(params_synth.subtractions) == 0
        inher = set_function_mode(inher)
        return set_local_env(inher, inher.local_env + params_synth.additions) 
    
    def synthesize_function_def_FunctionDef_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 4
        name_synth = synth_children[0]
        assert isinstance(name_synth, TargetSynth)

        declaration_map : PMap[str, Declaration] = m()
        for name in name_synth.env_names:
            declaration_map = declaration_map.set(name, Declaration(initialized=True))

        return LocalEnvSynth(s(), declaration_map)

    # function_def <-- AsyncFunctionDef

    def traverse_function_def_AsyncFunctionDef_name(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_name_target_mode(inher)
    
    # def traverse_function_def_AsyncFunctionDef_params(self, inher : I, synth_preds : tuple[S, ...]) -> I:
    #     return inher
    
    # def traverse_function_def_AsyncFunctionDef_ret_anno(self, inher : I, synth_preds : tuple[S, ...]) -> I:
    #     return inher

    def traverse_function_def_AsyncFunctionDef_body(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        len(synth_preds) == 3
        params_synth = synth_preds[1]
        assert isinstance(params_synth, LocalEnvSynth)
        assert len(params_synth.subtractions) == 0
        inher = set_function_mode(inher)
        return set_local_env(inher, inher.local_env + params_synth.additions) 

    def synthesize_function_def_AsyncFunctionDef_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 4
        name_synth = synth_children[0]
        assert isinstance(name_synth, TargetSynth)

        declaration_map : PMap[str, Declaration] = m()
        for name in name_synth.env_names:
            declaration_map = declaration_map.set(name, Declaration(initialized=True))

        return LocalEnvSynth(s(), declaration_map)

    # target_expsrs <-- ConsTargetExpr
    def synthesize_target_exprs_ConsTargetExpr_attributes(self, inher : Inher, children: tuple[synth, ...]) -> synth:
        assert len(children) == 2
        hd_synth = children[0]
        assert isinstance(hd_synth, TargetSynth)
        tl_synth = children[1]
        assert isinstance(tl_synth, MultiTargetSynth)

        names : PSet[str] = hd_synth.env_names.update(tl_synth.names)
        tokens : PSet[tuple[abstract_token, ...]] = s(hd_synth.tokens).update(tl_synth.tokens)

        return MultiTargetSynth(
            names = names,
            tokens = tokens 
        )


    # target_exprs <-- SingleTargetExpr
    def traverse_target_exprs_SingleTargetExpr_content(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return inher
    
    def synthesize_target_exprs_SingleTargetExpr_attributes(self, inher : Inher, children: tuple[synth, ...]) -> synth:
        assert len(children) == 1
        synth = children[0]
        if isinstance(synth, TargetSynth):
            return MultiTargetSynth(
                names = synth.env_names,
                tokens = s(synth.tokens)
            )
        else:
            assert isinstance(synth, SourceSynth)
            return MultiTargetSynth(
                names = s(),
                tokens = s(synth.tokens)
            )

    # stmt <-- Expr
    def traverse_stmt_Expr_content(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_source_mode(inher)

    def synthesize_stmt_Expr_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 1
        content_synth = synth_children[0] 
        assert isinstance(content_synth, SourceSynth)
        return LocalEnvSynth(s(), content_synth.env_additions)

    # stmt <-- ReturnSomething
    def traverse_stmt_ReturnSomething_content(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_source_mode(inher)

    def synthesize_stmt_ReturnSomething_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return LocalEnvSynth(s(), m())



    # return_annotation <-- NoReturnAnno
    def synthesize_return_annotation_NoReturnAnno_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return NoSynth()

    # return_annotation <-- SomeReturnAnno
    def synthesize_return_annotation_SomeReturnAnno_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return NoSynth()

    # stmt <-- Delete 
    def traverse_stmt_Delete_targets(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_delete_mode(inher)
    
    def synthesize_stmt_Delete_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 1
        delete_synth = synth_children[0]
        assert isinstance(delete_synth, DeleteSynth)
        return LocalEnvSynth(subtractions = delete_synth.names, additions = m())

    # stmt <-- Assign
    def traverse_stmt_Assign_targets(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_pattern_target_mode(inher)
    
    def traverse_stmt_Assign_content(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        assert len(synth_preds) == 1
        multi_target_synth = synth_preds[0]
        return set_source_mode(inher)
    
    def synthesize_stmt_Assign_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 2
        multi_target_synth = synth_children[0]
        assert isinstance(multi_target_synth, MultiTargetSynth)

        content_synth = synth_children[1]
        assert isinstance(content_synth, SourceSynth)

        # check name compatability between target and source expressions 
        for env_ref in content_synth.env_refs:
            assert (
                not (env_ref in multi_target_synth.names) or (
                    env_ref in inher.local_env
                    # FUTURE: check if forward reference or initialized  
                    # inher.local_env[name].initialized
                )
            )

        declaration_map : PMap[str, Declaration] = content_synth.env_additions
        for env_ref in multi_target_synth.names:
            declaration_map = declaration_map.set(env_ref, Declaration(initialized=True))

        return LocalEnvSynth(subtractions=s(), additions=declaration_map)
    
    # stmt <-- AugAssign
    def traverse_stmt_AugAssign_target(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_pattern_target_mode(inher)
    
    def traverse_stmt_AugAssign_op(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return inher
    
    def traverse_stmt_AugAssign_content(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_source_mode(inher)
    
    def synthesize_stmt_AugAssign_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 3

        target_synth = synth_children[0] 
        names = s()
        tokens = ()
        if isinstance(target_synth, SourceSynth):
            names = target_synth.env_refs
            tokens = target_synth.tokens
        else:
            assert isinstance(target_synth, TargetSynth)
            names = target_synth.env_names
            tokens = target_synth.tokens

        # target name is being updated, so must already exist in local_decl
        # FUTURE: type check the type of lhs with rhs of assignment
        for name in names:
            pass
            # FUTURE: load standard lib into local environment
            # assert (
            #     name in inher.local_env and 
            #     inher.local_env[name].initialized
            # )

        
        # if made it to this point without error then add names 
        # then names in assignment have already been declared and initialized
        
        # create AddDeclSynth containing the unified names 
        # FUTURE: modify to include type information 
        declaration_map : PMap[str, Declaration] = m()
        for name in names:
            declaration_map = declaration_map.set(name, Declaration(initialized=True))

        return LocalEnvSynth(subtractions = s(), additions = declaration_map)


    # stmt <-- AnnoAssign
    def traverse_stmt_AnnoAssign_target(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_name_target_mode(inher)
    
    def traverse_stmt_AnnoAssign_anno(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return inher
    
    def traverse_stmt_AnnoAssign_content(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_source_mode(inher)
    
    def synthesize_stmt_AnnoAssign_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 3
        target_synth = synth_children[0] 
        assert isinstance(target_synth, TargetSynth)

        # FUTURE: extract type info in a TypeSynth object
        # Which cases of expression correspond to type annotations?
        # create AddDeclSynth containing the unified names 
        # FUTURE: modify to include type information 
        declaration_map : PMap[str, Declaration] = m()
        for name in target_synth.env_names:
            declaration_map = declaration_map.set(name, Declaration(initialized=True))

        return LocalEnvSynth(subtractions=s(), additions=declaration_map)

    # stmt <-- AnnoDeclar
    def traverse_stmt_AnnoDeclar_target(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_name_target_mode(inher)
    
    def traverse_stmt_AnnoDeclar_anno(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        # TODO: switch to set_anno_mode. Should it be called type or annotation? 'annotation' refers to the the syntax, 'type' refers to the semantics
        return set_source_mode(inher)
    
    def synthesize_stmt_AnnoDeclar_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 2
        target_synth = synth_children[0] 
        assert isinstance(target_synth, TargetSynth)

        # create AddDeclSynth containing the unified names 
        # FUTURE: modify to include type information 
        declaration_map : PMap[str, Declaration] = m()
        for name in target_synth.env_names:
            declaration_map = declaration_map.set(name, Declaration(initialized=False))

        return LocalEnvSynth(subtractions=s(), additions=declaration_map)

    # stmt <-- For
    def traverse_stmt_For_target(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_pattern_target_mode(inher)
    
    def traverse_stmt_For_iter(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_source_mode(inher)
    
    def traverse_stmt_For_body(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        assert len(synth_preds) == 2
        target_synth = synth_preds[0] 
        assert isinstance(target_synth, TargetSynth)
        source_synth = synth_preds[1] 
        assert isinstance(source_synth, SourceSynth)

        env_additions : PMap[str, Declaration] = source_synth.env_additions 
        for name in target_synth.env_names:
            env_additions = env_additions.set(name, Declaration(initialized=True))

        return set_local_env(inher, inher.local_env + env_additions) 
    
    def synthesize_stmt_For_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 3
        target_synth = synth_children[0] 
        assert isinstance(target_synth, TargetSynth)
        source_synth = synth_children[1] 
        assert isinstance(source_synth, SourceSynth)
        body_synth = synth_children[2]
        assert isinstance(body_synth, LocalEnvSynth)

        source_synth_additions = source_synth.env_additions
        for sub in body_synth.subtractions:
            source_synth_additions = source_synth_additions.remove(sub)

        declaration_map : PMap[str, Declaration] = source_synth_additions + body_synth.additions
        for name in target_synth.env_names:
            declaration_map = declaration_map.set(name, Declaration(initialized=True))

        return LocalEnvSynth(subtractions=body_synth.subtractions, additions=declaration_map)

    # stmt <-- ForElse
    def traverse_stmt_ForElse_target(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_pattern_target_mode(inher)
    
    def traverse_stmt_ForElse_iter(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_source_mode(inher)
    
    def traverse_stmt_ForElse_body(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return self.traverse_stmt_For_body(inher, synth_preds)
    
    def traverse_stmt_ForElse_orelse(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return inher
    
    def synthesize_stmt_ForElse_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 4
        target_synth = synth_children[0] 
        assert isinstance(target_synth, TargetSynth)

        # FUTURE: add type inference and collection of type attributes

        declaration_map : PMap[str, Declaration] = m()
        for name in target_synth.env_names:
            declaration_map = declaration_map.set(name, Declaration(initialized=True))

        return LocalEnvSynth(subtractions=s(), additions=declaration_map)


    # stmt <-- AsyncFor
    def traverse_stmt_AsyncFor_target(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_pattern_target_mode(inher)
    
    def traverse_stmt_AsyncFor_iter(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_source_mode(inher)
    
    def traverse_stmt_AsyncFor_body(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return self.traverse_stmt_For_body(inher, synth_preds)
    
    def synthesize_stmt_AsyncFor_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 3
        target_synth = synth_children[0] 
        assert isinstance(target_synth, TargetSynth)

        # FUTURE: add type inference and collection of type attributes

        declaration_map : PMap[str, Declaration] = m()
        for name in target_synth.env_names:
            declaration_map = declaration_map.set(name, Declaration(initialized=True))

        return LocalEnvSynth(subtractions=s(), additions=declaration_map)

    # stmt <-- AsyncForElse
    def traverse_stmt_AsyncForElse_target(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_pattern_target_mode(inher)
    
    def traverse_stmt_AsyncForElse_iter(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_source_mode(inher)
    
    def traverse_stmt_AsyncForElse_body(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return inher
    
    def traverse_stmt_AsyncForElse_orelse(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return inher
    
    def synthesize_stmt_AsyncForElse_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 4
        target_synth = synth_children[0] 
        assert isinstance(target_synth, TargetSynth)

        # FUTURE: add type inference and collection of type attributes

        declaration_map : PMap[str, Declaration] = m()
        for name in target_synth.env_names:
            declaration_map = declaration_map.set(name, Declaration(initialized=True))

        return LocalEnvSynth(subtractions=s(), additions=declaration_map)

    # import_name <-- ImportNameAlias
    def traverse_import_name_ImportNameAlias_name(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return inher
    
    def traverse_import_name_ImportNameAlias_alias(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_name_target_mode(inher)
    
    def synthesize_import_name_ImportNameAlias_attributes(self, inher : Inher, synth_children: tuple[synth, ...]) -> synth:
        assert len(synth_children) == 2
        # FUTURE: use import to determine type 
        alias_synth = synth_children[1] 
        assert isinstance(alias_synth, TargetSynth) 

        # FUTURE: use tail to enable path in signature of module/package
        declarations : PMap[str, Declaration] = m()
        for name in alias_synth.env_names:
            declarations = declarations.set(name, Declaration(True))

        return LocalEnvSynth(subtractions=s(), additions=declarations)
    

    # import_name <-- ImportNameOnly
    def traverse_import_name_ImportNameOnly_name(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_import_mode(inher, "")
    
    def synthesize_import_name_ImportNameOnly_attributes(self, inher : Inher, synth_children: tuple[synth, ...]) -> synth:
        assert len(synth_children) == 1
        import_synth = synth_children[0] 
        assert isinstance(import_synth, ImportSynth)
        name = import_synth.path.split(".")[0]

        # FUTURE: use tail to enable path in signature of module/package
        return LocalEnvSynth(subtractions=s(), additions=pmap({name : Declaration(True)}))

    
    
    # sequence_import_name <-- ConsImportName
    def synthesize_sequence_import_name_ConsImportName_attributes(self, inher : Inher, synth_children: tuple[synth, ...]) -> synth:
        return local_env_synth_f(synth_children) 

    # sequence_import_name <-- SingleImportName
    def synthesize_sequence_import_name_SingleImportName_attributes(self, inher : Inher, synth_children: tuple[synth, ...]) -> synth:
        return local_env_synth_f(synth_children) 

    # stmt <-- Import
    def traverse_stmt_Import_names(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_import_mode(inher, "")
    
    def synthesize_stmt_Import_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 1 
        return synth_children[0]

    # stmt <-- ImportFrom 
    def traverse_stmt_ImportFrom_module(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_open_mode(inher)
    
    def traverse_stmt_ImportFrom_names(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        assert len(synth_preds) == 1 
        open_synth = synth_preds[0]
        assert isinstance(open_synth, OpenSynth)
        return set_import_mode(inher, open_synth.path)
    
    def synthesize_stmt_ImportFrom_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 2 
        return synth_children[1]

    # stmt <-- ImportWildCard 
    # FUTURE: both checking and synthesizing attributes requires 

    # sequence_name <-- ConsId 
    def synthesize_sequence_name_ConsId_attributes(self, inher : Inher, children: tuple[synth, ...]) -> synth:
        return target_synth_f(children)

    # sequence_name <-- SingleId 
    def synthesize_sequence_name_SingleId_attributes(self, inher : Inher, children: tuple[synth, ...]) -> synth:
        return target_synth_f(children)

    # stmt <-- Global 
    def traverse_stmt_Global_names(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_name_target_mode(inher)
    
    def synthesize_stmt_Global_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 1

        target_synth = synth_children[0] 
        assert isinstance(target_synth, TargetSynth)

        contents : PMap[str, Declaration] = m()
        for name in target_synth.env_names:
            # FUTURE: don't do assertion here. global name might be a forward reference. must wait until end of module to make assertion
            # Make the following assertion at the top module level to capture forward references: assert name in inher.global_env
            contents = contents.set(name, inher.global_env[name] if inher.global_env.get(name) else Declaration(False))
        
        return LocalEnvSynth(subtractions=s(), additions=contents)

    # stmt <-- Nonlocal 
    def traverse_stmt_Nonlocal_names(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_name_target_mode(inher)
    
    def synthesize_stmt_Nonlocal_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 1

        target_synth = synth_children[0] 
        assert isinstance(target_synth, TargetSynth)

        contents : PMap[str, Declaration] = m()
        for name in target_synth.env_names:
            assert name in inher.nonlocal_env
            contents = contents.set(name, inher.nonlocal_env[name])
        
        return LocalEnvSynth(s(), contents)


    def synthesize_operator_Add_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert not synth_children
        return source_synth_f(())

    def synthesize_operator_Sub_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert not synth_children
        return source_synth_f(())

    def synthesize_operator_Mult_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert not synth_children
        return source_synth_f(())

    def synthesize_operator_MatMult_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert not synth_children
        return source_synth_f(())

    def synthesize_operator_Div_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert not synth_children
        return source_synth_f(())

    def synthesize_operator_Mod_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert not synth_children
        return source_synth_f(())

    def synthesize_operator_Pow_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert not synth_children
        return source_synth_f(())

    def synthesize_operator_LShift_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert not synth_children
        return source_synth_f(())

    def synthesize_operator_RShift_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert not synth_children
        return source_synth_f(())

    def synthesize_operator_BitOr_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert not synth_children
        return source_synth_f(())

    def synthesize_operator_BitXor_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert not synth_children
        return source_synth_f(())

    def synthesize_operator_BitAnd_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert not synth_children
        return source_synth_f(())

    def synthesize_operator_FloorDiv_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert not synth_children
        return source_synth_f(())

    def synthesize_expr_attributes(self, inher : Inher, children: tuple[synth, ...]) -> synth:
        if isinstance(inher.mode, PatternTargetMode):
            return target_synth_f(children)

        elif isinstance(inher.mode, NameTargetMode):
            return target_synth_f(children)

        elif isinstance(inher.mode, SourceMode):
            return source_synth_f(children)

        elif isinstance(inher.mode, DeleteMode):
            names : PSet[str] = s()
            for c in children:
                if isinstance(c, DeleteSynth):
                    names = names.update(c.names)
            return DeleteSynth(names)

        else:
            assert False


    # expr 

    def analyze_token_expr(self, 
        token : Grammar, 
        inher : Inher, children : tuple[synth, ...], stack_result : Optional[synth], 
        stack : list[tuple[abstract_token, Union[Inher, Exception], tuple[synth, ...]]]
    ) -> Optional[synth]:
        if isinstance(inher.mode, PatternTargetMode):
            assert token.options == "expr"
            rule_name = token.selection

            if rule_name == "Name": 
                return self.analyze_token_expr_Name(inher, children, stack_result, stack)

            elif rule_name == "List": 
                return self.analyze_token_expr_List(inher, children, stack_result, stack)

            elif rule_name == "EmptyList": 
                return self.analyze_token_expr_EmptyList(inher, children, stack_result, stack)

            elif rule_name == "Tuple": 
                return self.analyze_token_expr_Tuple(inher, children, stack_result, stack)

            elif rule_name == "EmptyTuple": 
                return self.analyze_token_expr_EmptyTuple(inher, children, stack_result, stack)

            elif rule_name == "Subscript": 

                return self.analyze_token_expr_Subscript(inher, children, stack_result, stack)

            elif rule_name == "Attribute": 
                return self.analyze_token_expr_Attribute(inher, children, stack_result, stack)
                
            else:
                raise AnalysisError()

        if isinstance(inher.mode, DeleteMode):
            assert token.options == "expr"
            rule_name = token.selection

            if rule_name == "Name": 
                return self.analyze_token_expr_Name(inher, children, stack_result, stack)

            elif rule_name == "Subscript": 
                return self.analyze_token_expr_Subscript(set_source_mode(inher), children, stack_result, stack)

            elif rule_name == "Attribute": 
                return self.analyze_token_expr_Attribute(inher, children, stack_result, stack)
                
            else:
                raise AnalysisError()

        elif isinstance(inher.mode, NameTargetMode):
            assert isinstance(token, Grammar)
            assert token.options == "expr"
            assert token.selection == "Name"
            target_synth = self.analyze_str(inher)
            assert isinstance(target_synth, TargetSynth)
            tokens = tuple([token]) + target_synth.tokens
            return TargetSynth(env_names = target_synth.env_names, tokens = tokens) 

        else:
            return super().analyze_token_expr(token, set_source_mode(inher), children, stack_result, stack)

    # expr <-- Subscript 
    def traverse_expr_Subscript_content(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_source_mode(inher)
    
    def traverse_expr_Subscript_slice(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_source_mode(inher)
    
    def synthesize_expr_Subscript_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- BoolOp 
    def synthesize_expr_BoolOp_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- AssignExpr
    def traverse_expr_AssignExpr_target(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_name_target_mode(inher)
    
    def traverse_expr_AssignExpr_content(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_source_mode(inher)
    
    def synthesize_expr_AssignExpr_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        target_synth = synth_children[0]
        assert isinstance(target_synth, TargetSynth)

        expr_synth = synth_children[1]
        assert isinstance(expr_synth, SourceSynth)

        # check name compatability between target and source expressions 
        for name in expr_synth.env_refs:
            assert (
                not (name in target_synth.env_names) or (
                    name in inher.local_env and
                    inher.local_env[name].initialized
                )
            )

        # FUTURE: check that the source and target expressions are compatible
        # using type inference

        declaration_map : PMap[str, Declaration] = expr_synth.env_additions
        for name in target_synth.env_names:
            declaration_map = declaration_map.set(name, Declaration(initialized=True))

        return SourceSynth(
            env_additions = (declaration_map),
            env_refs = expr_synth.env_refs,
            tokens = target_synth.tokens + expr_synth.tokens
        )


    # expr <-- BinOp 
    def synthesize_expr_BinOp_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- UnaryOp 
    def synthesize_expr_UnaryOp_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- Lambda
    def synthesize_expr_Lambda_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- IfExp 
    def synthesize_expr_IfExp_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- Dictionary 
    def synthesize_expr_Dictionary_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- EmptyDictionary 
    def synthesize_expr_EmptyDictionary_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- Set 
    def synthesize_expr_Set_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- ListComp 
    def synthesize_expr_ListComp_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- SetComp 
    def synthesize_expr_SetComp_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- DictionaryComp 
    def synthesize_expr_DictionaryComp_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- GeneratorExp 
    def synthesize_expr_GeneratorExp_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- Await 
    def synthesize_expr_Await_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- YieldNothing 
    def synthesize_expr_YieldNothing_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- Yield 
    def synthesize_expr_Yield_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- YieldFrom 
    def synthesize_expr_YieldFrom_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- Compare 
    def synthesize_expr_Compare_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- Call 
    def synthesize_expr_Call_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- CallArgs
    def synthesize_expr_CallArgs_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- Integer 
    def synthesize_expr_Integer_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- Float 
    def synthesize_expr_Float_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- ConcatString 
    def synthesize_expr_ConcatString_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- True_ 
    def synthesize_expr_True__attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- False_ 
    def synthesize_expr_False__attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- None_ 
    def synthesize_expr_None__attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- Ellip 
    def synthesize_expr_Ellip_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- Attribute 
    def traverse_expr_Attribute_content(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_source_mode(inher)
    
    def traverse_expr_Attribute_name(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_attribute_mode(inher)
    
    def synthesize_expr_Attribute_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- Starred 
    def synthesize_expr_Starred_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- Name 
    def synthesize_expr_Name_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- List 
    def synthesize_expr_List_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- EmptyList 
    def synthesize_expr_EmptyList_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- Tuple 
    def synthesize_expr_Tuple_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- EmptyTuple 
    def synthesize_expr_EmptyTuple_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # expr <-- Slice 
    def synthesize_expr_Slice_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, synth_children)

    # bases_a <-- ConsBase
    def traverse_bases_a_ConsBase_head(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_source_mode(inher)
    
    def traverse_bases_a_ConsBase_tail(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return inher
    
    def synthesize_bases_a_ConsBase_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.default_synth(inher)
    
    # bases_a <-- SingleBase
    
    def traverse_bases_a_SingleBase_content(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_source_mode(inher)
    
    def synthesize_bases_a_SingleBase_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.default_synth(inher)
    
    # comma_exprs <-- ConsExpr 
    def synthesize_comma_exprs_ConsExpr_attributes(self, inher : Inher, children: tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, children)

    # comma_exprs <-- SingleExpr 
    def synthesize_comma_exprs_SingleExpr_attributes(self, inher : Inher, children: tuple[synth, ...]) -> synth:
        return self.synthesize_expr_attributes(inher, children)


    # Param 
    def traverse_Param_name(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_name_target_mode(inher) 
    
    def traverse_Param_anno(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        # TODO: set_anno_mode(inher)
        return set_source_mode(inher) 
    
    def traverse_Param_default(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_source_mode(inher) 
    
    def synthesize_Param_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 3
        target_synth = synth_children[0]
        assert isinstance(target_synth, TargetSynth)

        declaration_map : PMap[str, Declaration] = m()
        for name in target_synth.env_names:
            declaration_map = declaration_map.set(name, Declaration(initialized=True))
        return LocalEnvSynth(subtractions=s(), additions=declaration_map)


    # parameters_d <-- ConsKwParam
    def synthesize_parameters_d_ConsKwParam_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return local_env_synth_f(synth_children)

    # parameters_d <-- SingleKwParam
    def synthesize_parameters_d_SingleKwParam_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return local_env_synth_f(synth_children)

    # parameters_d <-- DictionarySplatParam
    def synthesize_parameters_d_DictionarySplatParam_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return local_env_synth_f(synth_children)

    # parameters_c <-- SingleListSplatParam
    def synthesize_parameters_c_SingleListSplatParam_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return local_env_synth_f(synth_children)

    # parameters_c <-- TransListSplatParam
    def synthesize_parameters_c_TransListSplatParam_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return local_env_synth_f(synth_children)

    # parameters_c <-- ParamsD
    def synthesize_parameters_c_ParamsD_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return local_env_synth_f(synth_children)

    # parameters_b <-- ConsParam
    def synthesize_parameters_b_ConsParam_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return local_env_synth_f(synth_children)

    # parameters_b <-- SingleParam
    def synthesize_parameters_b_SingleParam_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return local_env_synth_f(synth_children)

    # parameters_b <-- ParamsC
    def synthesize_parameters_b_ParamsC_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return local_env_synth_f(synth_children)

    # parameters_a <-- ConsPosParam
    def synthesize_parameters_a_ConsPosParam_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return local_env_synth_f(synth_children)

    # parameters_a <-- SinglePosParam
    def synthesize_parameters_a_SinglePosParam_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return local_env_synth_f(synth_children)

    # parameters_a <-- TransPosParam
    def synthesize_parameters_a_TransPosParam_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return local_env_synth_f(synth_children)

    # parameters <-- ParamsA
    def synthesize_parameters_ParamsA_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return local_env_synth_f(synth_children)

    # parameters <-- ParamsB
    def synthesize_parameters_ParamsB_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return local_env_synth_f(synth_children)

    # parameters <-- NoParam 
    def synthesize_parameters_NoParam_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return local_env_synth_f(synth_children)

    # ElifBlock
    def traverse_ElifBlock_test(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_source_mode(inher)
    
    def traverse_ElifBlock_body(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return inher
    
    def synthesize_ElifBlock_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return self.default_synth(inher)

    # stmt <-- While
    def traverse_stmt_While_test(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_source_mode(inher)
    
    def traverse_stmt_While_body(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        assert len(synth_preds) == 1
        test_synth = synth_preds[0]
        assert isinstance(test_synth, SourceSynth)
        return set_local_env(inher, inher.local_env + test_synth.env_additions)
    
    def synthesize_stmt_While_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 2
        test_synth = synth_children[0]
        assert isinstance(test_synth, SourceSynth)
        return LocalEnvSynth(subtractions=s(), additions=test_synth.env_additions)
    
    # stmt <-- WhileElse
    def traverse_stmt_WhileElse_test(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_source_mode(inher)
    
    def traverse_stmt_WhileElse_body(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        assert len(synth_preds) == 1
        test_synth = synth_preds[0]
        assert isinstance(test_synth, SourceSynth)
        return set_local_env(inher, inher.local_env + test_synth.env_additions)
    
    def traverse_stmt_WhileElse_orelse(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        assert len(synth_preds) == 2
        test_synth = synth_preds[0]
        assert isinstance(test_synth, SourceSynth)
        return set_local_env(inher, inher.local_env + test_synth.env_additions)
    
    def synthesize_stmt_WhileElse_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 3
        test_synth = synth_children[0]
        assert isinstance(test_synth, SourceSynth)
        return LocalEnvSynth(subtractions=s(), additions=test_synth.env_additions)
    

    # stmt <-- If
    def traverse_stmt_If_test(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_source_mode(inher)
    
    def traverse_stmt_If_body(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        assert len(synth_preds) == 1
        test_synth = synth_preds[0]
        assert isinstance(test_synth, SourceSynth)
        return set_local_env(inher, inher.local_env + test_synth.env_additions)
    
    def traverse_stmt_If_orelse(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        assert len(synth_preds) == 2
        test_synth = synth_preds[0]
        assert isinstance(test_synth, SourceSynth)
        return set_local_env(inher, inher.local_env + test_synth.env_additions)
    
    def synthesize_stmt_If_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 3
        test_synth = synth_children[0]
        assert isinstance(test_synth, SourceSynth)
        return LocalEnvSynth(subtractions=s(), additions=test_synth.env_additions)


    # stmt <-- RaiseExc
    def traverse_stmt_RaiseExc_exc(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_source_mode(inher)
    
    # def synthesize_stmt_RaiseExc_attributes(self, inher : I, synth_children : tuple[S, ...]) -> S:
    #     return synth_children[-1] if synth_children else self.default_synth(inher)
    
    # stmt <-- RaiseFrom
    def traverse_stmt_RaiseFrom_exc(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_source_mode(inher)
    
    def traverse_stmt_RaiseFrom_caus(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_source_mode(inher)
    
    # def synthesize_stmt_RaiseFrom_attributes(self, inher : I, synth_children : tuple[S, ...]) -> S:
    #     return synth_children[-1] if synth_children else self.default_synth(inher)

    # except_arg <-- SomeExceptArg
    def traverse_except_arg_SomeExceptArg_content(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_source_mode(inher)
    
    def synthesize_except_arg_SomeExceptArg_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 1

        source_synth = synth_children[0]
        assert isinstance(source_synth, SourceSynth)

        return LocalEnvSynth(subtractions=s(), additions=source_synth.env_additions)
    
    # except_arg <-- SomeExceptArgName
    def traverse_except_arg_SomeExceptArgName_content(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_source_mode(inher)
    
    def traverse_except_arg_SomeExceptArgName_name(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_name_target_mode(inher)
    
    def synthesize_except_arg_SomeExceptArgName_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 2

        source_synth = synth_children[0]
        assert isinstance(source_synth, SourceSynth)

        target_synth = synth_children[1]
        assert isinstance(target_synth, TargetSynth)

        declaration_map : PMap[str, Declaration] = source_synth.env_additions
        for name in target_synth.env_names:
            declaration_map = declaration_map.set(name, Declaration(initialized=False))

        return LocalEnvSynth(subtractions=s(), additions=declaration_map)
    
    # except_arg <-- NoExceptArg
    def synthesize_except_arg_NoExceptArg_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return LocalEnvSynth(subtractions=s(), additions=m())

    # ExceptHandler 
    def traverse_ExceptHandler_body(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        len(synth_preds) == 1
        arg_synth = synth_preds[0]
        assert isinstance(arg_synth, LocalEnvSynth)

        assert len(arg_synth.subtractions) == 0
        return set_local_env(inher, inher.local_env + arg_synth.additions) 

    # sequence_with_item <-- ConsWithItem
    def synthesize_sequence_with_item_ConsWithItem_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return local_env_synth_f(synth_children) 

    # sequence_with_item <-- SingleWithItem
    def synthesize_sequence_with_item_SingleWithItem_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return local_env_synth_f(synth_children) 


    # with_item <-- WithItemAlias
    def traverse_with_item_WithItemAlias_content(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_source_mode(inher)
    
    def traverse_with_item_WithItemAlias_alias(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_pattern_target_mode(inher)
    
    def synthesize_with_item_WithItemAlias_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 2
        
        source_synth = synth_children[0] 
        assert isinstance(source_synth, SourceSynth)
        
        target_synth = synth_children[1] 
        assert isinstance(target_synth, TargetSynth)

        # check name compatability between target and source expressions 
        for name in source_synth.env_refs:
            assert (
                not (name in target_synth.env_names) or (
                    name in inher.local_env and
                    inher.local_env[name].initialized
                )
            )

        # FUTURE: check that the source and target expressions are compatible
        # using type inference

        declaration_map : PMap[str, Declaration] = source_synth.env_additions
        for name in target_synth.env_names:
            declaration_map = declaration_map.set(name, Declaration(initialized=False))

        return LocalEnvSynth(s(), declaration_map)
    
    # with_item <-- WithItemOnly
    def traverse_with_item_WithItemOnly_content(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return set_source_mode(inher)

    def synthesize_with_item_WithItemOnly_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 1
        synth = synth_children[0] 
        assert isinstance(synth, SourceSynth)
        return LocalEnvSynth(s(), synth.env_additions)

    
    # stmt <-- With
    def traverse_stmt_With_items(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return inher
    
    def traverse_stmt_With_body(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        assert len(synth_preds) == 1
        synth = synth_preds[0] 
        assert isinstance(synth, LocalEnvSynth)
        assert len(synth.subtractions) == 0
        return set_local_env(inher, inher.local_env + synth.additions)
    
    def synthesize_stmt_With_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        assert len(synth_children) == 2
        items_synth = synth_children[0] 
        return items_synth


    # stmt <-- AsyncWith
    def traverse_stmt_AsyncWith_items(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        return inher
    
    def traverse_stmt_AsyncWith_body(self, inher : Inher, synth_preds : tuple[synth, ...]) -> Inher:
        assert len(synth_preds) == 1
        synth = synth_preds[0] 
        assert isinstance(synth, LocalEnvSynth)
        assert len(synth.subtractions) == 0
        return set_local_env(inher, inher.local_env + synth.additions)
    
    def synthesize_stmt_AsyncWith_attributes(self, inher : Inher, synth_children : tuple[synth, ...]) -> synth:
        return LocalEnvSynth(s(), m()) 


    # str
    def analyze_token_str(self, token : Vocab, inher : Inher) -> synth:
        if token.options == "identifier":
            name = token.selection

            if (
                isinstance(inher.mode, PatternTargetMode) or
                isinstance(inher.mode, NameTargetMode)
            ):

                return TargetSynth(
                    env_names = s(name),
                    tokens = tuple([token])
                )  

            elif isinstance(inher.mode, SourceMode):

                # TODO: move this check to a higher level 
                # in order to distinguish between 
                # forward references to functions and back references to variable declarations
                # 
                # assert (
                #     (name in inher.local_decl and inher.local_decl[name].initialized) or 
                #     (name in inher.nonlocal_decl and inher.nonlocal_decl[name].initialized) or 
                #     (name in inher.global_decl and inher.global_decl[name].initialized)
                # )

                return SourceSynth(
                    env_additions = m(),
                    env_refs = s(name),
                    tokens = tuple([token])
                )  
            elif isinstance(inher.mode, AttributeMode):
                # name is an attribute, not in local env, so not part of used_names
                return SourceSynth(
                    env_additions = m(),
                    env_refs = s(),
                    tokens = tuple([token])
                )  

            elif isinstance(inher.mode, DeleteMode):
                return DeleteSynth(names = s(name))  

            elif isinstance(inher.mode, ImportMode):
                return ImportSynth(path = name)  

            elif isinstance(inher.mode, OpenMode):
                return OpenSynth(path = name)  

            else:
                return NoSynth()

        else:
            if isinstance(inher.mode, SourceMode):
                return SourceSynth(
                    env_additions = m(),
                    env_refs = s(),
                    tokens = tuple([token])
                )  
            else:
                raise AnalysisError()
