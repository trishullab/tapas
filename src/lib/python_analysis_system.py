from __future__ import annotations
from ast import NamedExpr
from copy import copy

from dataclasses import dataclass
from re import A
from typing import Callable, Iterator, Iterable, Mapping
from numpy import empty

from pyrsistent import pmap, m, pset, s, PMap, PSet

from queue import Queue
import os

from lib.line_format_construct_autogen import InLine, NewLine, IndentLine
from lib.abstract_token_construct_autogen import abstract_token, Vocab, Grammar
from lib import abstract_token_system as ats

from lib import util_system as us

from lib.python_ast_construct_autogen import ConsTargetExpr, SomeParamDefault, decorators

from lib import python_generic_tree_system as pgs 
from lib import python_ast_system as pas
from lib import python_abstract_token_system as pats 

from lib import python_abstract_token_crawl_autogen as crawler
from lib.python_analysis_construct_autogen import *


T = TypeVar('T')

class ArgParamMismatchError(Exception): pass

def unionize_all_types(ts : Iterable[type]) -> type:
    union_type = None 
    for t in ts:
        if union_type:
            union_type = unionize_types(union_type, t)
        else:
            union_type = t
    assert union_type
    return union_type



def unionize_types(a : type, b : type) -> type:

    if isinstance(a, AnyType):
        return b
    elif isinstance(b, AnyType):
        return a
    elif isinstance(a, UnionType) and isinstance(b, UnionType):
        return UnionType(
            type_choices = (a.type_choices + b.type_choices)
        )
    elif isinstance(a, UnionType):
        return UnionType(
            type_choices = a.type_choices + (b,)
        )
    elif isinstance(b, UnionType):
        return UnionType(
            type_choices = (a,) + b.type_choices
        )
    else:
        return UnionType(
            type_choices = (a, b)
        )

def get_type_args(t : type) -> tuple[type, ...]:

    # TODO: should this return a single type annotation?
    # type_arg = (
    #     None
    #     if len(spec_type_args) == 0 else
    #     AnnoType(spec_type_args[0])
    #     if len(spec_type_args) == 1 else
    #     FixedTupleType(
    #         item_types=tuple(
    #             AnnoType(ta)
    #             for ta in spec_type_args
    #         )
    #     )
    # )


    return match_type(t, TypeHandlers(
        case_TypeType = lambda t : (t.content,),
        case_VarType = lambda t : (),
        case_EllipType = lambda t : (),
        case_AnyType = lambda t : (),
        case_ObjectType = lambda t : (),
        case_NoneType = lambda t : (), 
        case_ModuleType = lambda t : (),
        case_FunctionType = lambda t : (),
        case_UnionType = lambda t : t.type_choices,
        case_InterType = lambda t : t.type_components,
        case_RecordType = lambda t : t.type_args,
        case_FixedTupleType = lambda t : t.item_types,
        case_VariedTupleType = lambda t : (t.item_type,),
        case_MappingType = lambda t : (t.key_type, t.value_type),
        case_DictType = lambda t : (t.key_type, t.value_type),
        case_SetType = lambda t : (t.item_type,),
        case_IterableType = lambda t : (t.item_type,),
        case_DictKeysType = lambda t : (t.item_type,),
        case_DictValuesType = lambda t : (t.item_type,),
        case_DictItemsType = lambda t : (t.item_type,),
        case_SequenceType = lambda t : (t.item_type,),
        case_RangeType = lambda t : (t.item_type,),
        case_ListType = lambda t : (t.item_type,),
        case_ListLitType = lambda t : (unionize_all_types(t.item_types),),
        case_GeneratorType = lambda t : (t.yield_type, t.return_type,),
        case_BoolType = lambda t : (),
        case_TrueType = lambda t : (),
        case_FalseType = lambda t : (),
        case_IntType = lambda t : (),
        case_IntLitType = lambda t : (),
        case_FloatType = lambda t : (),
        case_FloatLitType = lambda t : (),
        case_StrType = lambda t : (),
        case_StrLitType = lambda t : (),
        case_SliceType = lambda t : (),
    ))

from typing import Union  

def get_class_key(t : type) -> str:
    return match_type(t, TypeHandlers(
        case_TypeType = lambda t : "typing.type",
        case_VarType = lambda t : "typing.TypeVar",
        case_EllipType = lambda t : "builtins.ellipsis",
        case_AnyType = lambda t : "typing.Any",
        case_ObjectType = lambda t : "builtins.object",
        case_NoneType = lambda t : "", 
        case_ModuleType = lambda t : "",
        case_FunctionType = lambda t : "_collections_abc.Callable",
        case_UnionType = lambda t : "typing.Union",
        case_InterType = lambda t : "",
        case_RecordType = lambda t : t.class_key,
        case_FixedTupleType = lambda t : "builtins.tuple",
        case_VariedTupleType = lambda t : "builtins.tuple",
        case_MappingType = lambda t : "_collections_abc.Mapping",
        case_DictType = lambda t : "builtins.dict",
        case_SetType = lambda t : "builtins.set",
        case_IterableType = lambda t : "_collections_abc.Iterable",
        case_DictKeysType = lambda t : "_collections_abc.dict_keys",
        case_DictValuesType = lambda t : "_collections_abc.dict_values",
        case_DictItemsType = lambda t : "_collections_abc.dict_items",
        case_SequenceType = lambda t : "_collections_abc.Sequence",
        case_RangeType = lambda t : "builtins.range",
        case_ListType = lambda t : "builtins.list",
        case_ListLitType = lambda t : "builtins.list",
        case_GeneratorType = lambda t : "_collections_abc.Generator",
        case_BoolType = lambda t : "builtins.bool",
        case_TrueType = lambda t : "builtins.bool",
        case_FalseType = lambda t : "builtins.bool",
        case_IntType = lambda t : "builtins.int",
        case_IntLitType = lambda t : "builtins.int",
        case_FloatType = lambda t : "builtins.float",
        case_FloatLitType = lambda t : "builtins.float",
        case_StrType = lambda t : "builtins.str",
        case_StrLitType = lambda t : "builtins.str",
        case_SliceType = lambda t : "builtins.slice"
    ))

def coerce_to_type(t) -> type:
    assert isinstance(t, type)
    return t

def coerce_to_TypeType(t : type) -> TypeType:
    if isinstance(t, AnyType):
        return TypeType(AnyType())
    elif isinstance(t, NoneType):
        return TypeType(NoneType())
    else:
        assert isinstance(t, TypeType)
        return t

def coerce_to_FixedTupleType(t : type) -> FixedTupleType:
    assert isinstance(t, FixedTupleType)
    return t

def coerce_to_ListLitType(t : type) -> ListLitType:
    assert isinstance(t, ListLitType)
    return t

def from_anno_seq_to_instance_types(ts : Iterable[type]) -> tuple[type, ...]:
    return tuple(
        coerce_to_TypeType(t).content
        for t in ts 
    ) 

def from_anno_option_to_instance_type(t : type | None) -> type:
    if t:
        return coerce_to_TypeType(t).content
    else:
        return AnyType()

def from_anno_pair_option_to_instance_type(t : type | None) -> tuple[type, type]: 
    if t:
        ftt = coerce_to_FixedTupleType(t)
        ts = from_anno_seq_to_instance_types(ftt.item_types)
        assert len(ts) == 2
        return (ts[0], ts[1])
    else:
        return (AnyType(), AnyType()) 

def from_class_key_to_type(inher_aux : InherAux, class_key : str, type_arg : Optional[type] = None) -> type:

    if class_key == "builtins.type":
        item_type = from_anno_option_to_instance_type(type_arg)
        return TypeType(content = item_type)

    elif class_key == "builtins.ellipsis":
        assert not type_arg
        return EllipType()
    elif class_key == "_collections_abc.Any":
        assert not type_arg
        return AnyType()
    elif class_key == "_collections_abc.Callable":
        assert isinstance(type_arg, FixedTupleType)
        type_args = coerce_to_FixedTupleType(type_arg).item_types
        assert len(type_args) == 2
        param_type_args = coerce_to_ListLitType(type_args[0]).item_types
        pos_param_types = from_anno_seq_to_instance_types(param_type_args)
        return_type = coerce_to_TypeType(type_arg.item_types[1]).content
        return make_FunctionType(
            pos_param_types=pos_param_types,
            return_type=return_type
        )
    elif class_key == "typing.Union":
        assert type_arg
        ts = from_anno_seq_to_instance_types(coerce_to_FixedTupleType(type_arg).item_types)
        return make_UnionType(type_choices=ts)

    elif class_key == "builtins.tuple":
        
        if (
            isinstance(type_arg, FixedTupleType) and
            len(type_arg.item_types) == 2 and
            isinstance(type_arg.item_types[1], EllipType)
        ):
            return VariedTupleType(item_type = coerce_to_TypeType(type_arg.item_types[0]).content)

        elif isinstance(type_arg, FixedTupleType):
            item_types = from_anno_seq_to_instance_types(type_arg.item_types)
            return FixedTupleType(item_types=item_types)

        elif type_arg:
            item_types = coerce_to_TypeType(type_arg).content,
            return FixedTupleType(item_types=item_types)

        else:
            return FixedTupleType(item_types=())

    elif class_key == "builtins.dict":
        (key_type, value_type) = from_anno_pair_option_to_instance_type(type_arg)
        return DictType(key_type=key_type, value_type=value_type)

    elif class_key == "builtins.set":
        item_type = from_anno_option_to_instance_type(type_arg)
        return SetType(item_type = item_type)
    elif class_key == "_collections_abc.Iterable":
        item_type = from_anno_option_to_instance_type(type_arg)
        return IterableType(item_type=item_type)
    elif class_key == "_collections_abc.dict_keys":
        item_type = from_anno_option_to_instance_type(type_arg)
        return DictKeysType(item_type=item_type)

    elif class_key == "_collections_abc.dict_values":
        item_type = from_anno_option_to_instance_type(type_arg)
        return DictValuesType(item_type=item_type)

    elif class_key == "_collections_abc.dict_items":
        item_type = from_anno_option_to_instance_type(type_arg)
        return DictItemsType(item_type=item_type)

    elif class_key == "_collections_abc.Sequence":
        item_type = from_anno_option_to_instance_type(type_arg)
        return SequenceType(item_type=item_type)
    elif class_key == "builtins.range":
        item_type = from_anno_option_to_instance_type(type_arg)
        return RangeType(item_type=item_type)
    elif class_key == "builtins.list":
        item_type = from_anno_option_to_instance_type(type_arg)
        return ListType(item_type=item_type)
    elif class_key == "_collections_abc.Generator":
        if type_arg:
            ftt = coerce_to_FixedTupleType(type_arg)
            ts = from_anno_seq_to_instance_types(ftt.item_types)
            assert len(ts) == 3
            return GeneratorType(yield_type=ts[0], return_type=ts[2])
        else:
            return GeneratorType(AnyType(), AnyType())
    elif class_key == "builtins.bool":
        return BoolType()
    elif class_key == "builtins.int":
        return IntType()
    elif class_key == "builtins.float":
        return FloatType()
    elif class_key == "builtins.str":
        return StrType()
    elif class_key == "builtins.slice":

        if type_arg:
            ftt = coerce_to_FixedTupleType(type_arg)
            ts = from_anno_seq_to_instance_types(ftt.item_types)
            assert len(ts) == 3
            return SliceType(ts[0], ts[1], ts[2])
        else:
            return SliceType(AnyType(), AnyType(), AnyType())

    else:
        type_args = (
            from_anno_seq_to_instance_types(type_arg.item_types)  
            if isinstance(type_arg, FixedTupleType) else
            (coerce_to_TypeType(type_arg).content,)
            if type_arg else
            ()
        )

        return make_RecordType(
            class_key=class_key,
            type_args=type_args
        )


def generalize_type(inher_aux : InherAux, spec_type : type) -> type:
    class_key = get_class_key(spec_type)
    class_record = from_static_path_to_ClassRecord(inher_aux, class_key)
    if class_record:
        spec_type_args = get_type_args(spec_type)
        type_arg = (
            None
            if len(spec_type_args) == 0 else
            TypeType(spec_type_args[0])
            if len(spec_type_args) == 1 else
            FixedTupleType(
                item_types=tuple(
                    TypeType(ta)
                    for ta in spec_type_args
                )
            )
        )
        gen_type = from_class_key_to_type(inher_aux, class_key, type_arg)
        return gen_type
    else:
        return AnyType()


def coerce_to_VarType(t : type) -> VarType:
    assert isinstance(t, VarType)
    return t


def subsumes_RecordType(sub_type : RecordType, super_type : RecordType, inher_aux : InherAux) -> bool:
    assert sub_type.class_key == super_type.class_key 
    class_record = from_static_path_to_ClassRecord(inher_aux, sub_type.class_key)
    assert class_record
    type_params = class_record.type_params

    assert len(type_params) == len(sub_type.type_args) == len(super_type.type_args)

    subsumptions = [
        (
            subsumes(sub_type.type_args[i], super_type.type_args[i], inher_aux)
            if isinstance(tp.variant, CoVariant) else
            subsumes(super_type.type_args[i], sub_type.type_args[i], inher_aux)
            if isinstance(tp.variant, ContraVariant) else
            sub_type.type_args[i] == super_type.type_args[i]
        )
        for i, tp in enumerate(type_params)
    ]

    return us.every(subsumptions, lambda x : x)

def subsumes_FunctionType(sub_type : FunctionType, super_type : FunctionType, inher_aux : InherAux) -> bool:
    param_subsumptions = [ 
        subsumes(super_type.pos_param_types[i], t, inher_aux)
        for i, t in enumerate(sub_type.pos_param_types)
    ] + [ 
        subsumes(super_type.pos_kw_param_sigs[i].type, s.type, inher_aux)
        for i, s in enumerate(sub_type.pos_kw_param_sigs)
    ] + [
        subsumes(super_type.splat_pos_param_type, sub_type.splat_pos_param_type, inher_aux)
    ] if sub_type.splat_pos_param_type and super_type.splat_pos_param_type else [] + [
        subsumes(super_type.kw_param_sigs[i].type, s.type, inher_aux)
        for i, s in enumerate(sub_type.kw_param_sigs)
    ] + [
        subsumes(super_type.splat_kw_param_type, sub_type.splat_kw_param_type, inher_aux)
    ] if sub_type.splat_kw_param_type and super_type.splat_kw_param_type else [] 

    return_subsumption = subsumes(sub_type.return_type, super_type.return_type, inher_aux)

    return us.every(param_subsumptions, lambda x : x) and return_subsumption


def type_args_subsume(sub_type : type, super_type : type, inher_aux : InherAux) -> bool:
    if get_class_key(sub_type) != get_class_key(super_type):
        return False
    
    if isinstance(sub_type, FunctionType):
        assert isinstance(super_type, FunctionType)
        return subsumes_FunctionType(sub_type, super_type, inher_aux)
    elif isinstance(sub_type, RecordType):
        assert isinstance(super_type, RecordType)
        return subsumes_RecordType(sub_type, super_type, inher_aux)
    else:
        assert get_class_key(sub_type) == get_class_key(super_type)
        sub_type_args = get_type_args(sub_type)
        super_type_args = get_type_args(super_type)
        

        if len(sub_type_args) != len(super_type_args):
            return False
        else: 
            subsumptions = [
                subsumes(t, super_type_args[i], inher_aux)
                for i, t in enumerate(sub_type_args)
            ]

            return us.every(subsumptions, lambda x : x)
    



def subsumes(sub_type : type, super_type : type, inher_aux : InherAux) -> bool:

    return (
        not isinstance(sub_type, VarType) or

        not isinstance(sub_type, ModuleType) or 

        isinstance(sub_type, AnyType) or 

        isinstance(super_type, AnyType) or 

        type_args_subsume(sub_type, super_type, inher_aux) or

        sub_type == super_type or 

        (isinstance(sub_type, InterType) and 
            us.exists(sub_type.type_components, lambda tc : subsumes(tc, super_type, inher_aux))) or 

        (isinstance(super_type, UnionType) and 
            us.exists(super_type.type_choices, lambda tc : subsumes(sub_type, tc, inher_aux))) or

        (parent_type := get_parent_type(sub_type, inher_aux),
            parent_type != None and subsumes(parent_type, super_type, inher_aux))[-1]
    )


def instance_parent_type(t : RecordType, inher_aux : InherAux) -> type:
    class_record = from_static_path_to_ClassRecord(inher_aux, t.class_key) 
    if not class_record:   
        return ObjectType()

    assert len(t.type_args) == len(class_record.type_params)
    subst_map = pmap({
        var_type.name : t.type_args[i]
        for i, var_type in enumerate(class_record.type_params)
    })
    parent_types = tuple(
        substitute_type_args(st, subst_map)
        for st in class_record.super_types
    )
    if len(parent_types) == 1:
        return parent_types[0]
    else:
        return InterType(parent_types)
    
    
def get_parent_type(t : type, inher_aux : InherAux) -> Optional[type]:

    return match_type(t, TypeHandlers(
        case_TypeType = lambda t : ObjectType(),
        case_VarType = lambda t : None,
        case_EllipType = lambda t : ObjectType(),
        case_AnyType = lambda t : None,
        case_ObjectType = lambda t : None,
        case_NoneType = lambda t : ObjectType(), 
        case_ModuleType = lambda t : None,
        case_FunctionType = lambda t : ObjectType(),
        case_UnionType = lambda t : ObjectType(),
        case_InterType = lambda t : ObjectType(),
        case_RecordType = lambda t : instance_parent_type(t, inher_aux),
        case_FixedTupleType = lambda t : VariedTupleType(unionize_all_types(t.item_types)),
        case_VariedTupleType = lambda t : SequenceType(t.item_type),
        case_MappingType = lambda t : ObjectType(),
        case_DictType = lambda t : MappingType(t.key_type, t.value_type),
        case_SetType = lambda t : IterableType(t.item_type),
        case_IterableType = lambda t : ObjectType(),
        case_DictKeysType = lambda t : IterableType(t.item_type),
        case_DictValuesType = lambda t : IterableType(t.item_type),
        case_DictItemsType = lambda t : IterableType(t.item_type),
        case_SequenceType = lambda t : IterableType(t.item_type),
        case_RangeType = lambda t : SequenceType(t.item_type),
        case_ListType = lambda t : SequenceType(t.item_type),
        case_ListLitType = lambda t : ListType(unionize_all_types(t.item_types)),
        case_GeneratorType = lambda t : IterableType(t.yield_type),
        case_BoolType = lambda t : ObjectType(),
        case_TrueType = lambda t : BoolType(),
        case_FalseType = lambda t : BoolType(),
        case_IntType = lambda t : ObjectType(),
        case_IntLitType = lambda t : IntType(),
        case_FloatType = lambda t : ObjectType(),
        case_FloatLitType = lambda t : FloatType(),
        case_StrType = lambda t : SequenceType(item_type=StrType()),
        case_StrLitType = lambda t : StrType(),
        case_SliceType = lambda t : ObjectType() 
    )) 

def infer_class_record(t : type, inher_aux : InherAux) -> ClassRecord | None:
    class_key = get_class_key(t)
    class_record = from_static_path_to_ClassRecord(inher_aux, class_key) 
    if class_record:
        type_args : tuple[type, ...] = get_type_args(t)
        subst_map = pmap({
            tp.name : (type_args[i] if i < len(type_args) else AnyType())
            for i, tp in enumerate(class_record.type_params) 
        })

        return update_ClassRecord(class_record,
            static_fields = pmap({
                k : substitute_type_args(t, subst_map)  
                for k, t in class_record.static_fields.items()
            }), 
            instance_fields = pmap({
                k : substitute_type_args(t, subst_map)  
                for k, t in class_record.instance_fields.items()
            })
        )
    else:
        return None


def static_field_type(class_record : ClassRecord, field_name : str, inher_aux : InherAux) -> Optional[type]:
    fields = class_record.static_fields 
    result = fields.get(field_name)
    if result:
        return result
    else:
        super_class_type_unresolved = False
        for st in reversed(class_record.super_types):
            super_class_type = infer_class_record(st, inher_aux)
            if super_class_type:
                result = static_field_type(super_class_type, field_name, inher_aux)
                if result:
                    return result
            else:
                super_class_type_unresolved = True
        if super_class_type_unresolved:
            return AnyType()
        else:
            return None

            

def field_type(anchor_type : type, field_name : str, inher_aux : InherAux) -> type | None:

    if isinstance(anchor_type, ModuleType):
        assert anchor_type.key
        path = f"{anchor_type.key}.{field_name}" 
        return from_static_path_to_type(inher_aux, path)

    elif isinstance(anchor_type, TypeType) or isinstance(anchor_type, TypeType):
        content_class_record = infer_class_record(anchor_type.content, inher_aux)
        if content_class_record:
            return static_field_type(content_class_record, field_name, inher_aux)
        else:
            return AnyType()

    else:
        class_record = infer_class_record(anchor_type, inher_aux)
        if class_record:
            fields = class_record.instance_fields
            result = fields.get(field_name)
            if result:
                return result 
            else:
                for super_type in reversed(class_record.super_types):
                    result = field_type(super_type, field_name, inher_aux)
                    if result:
                        return result
        return AnyType()




def substitute_type_args(t : type, subst_map : PMap[str, type]) -> type:
    return match_type(t, TypeHandlers(
        case_TypeType = lambda t : substitute_type_args(t.content, subst_map),
        case_VarType = lambda t : subst_map[t.name],
        case_EllipType = lambda t : t,
        case_AnyType = lambda t : t,
        case_ObjectType = lambda t : t,
        case_NoneType = lambda t : t, 
        case_ModuleType = lambda t : t,
        case_FunctionType = lambda t : (

            FunctionType(
                pos_param_types = tuple(
                    substitute_type_args(param_type, subst_map)
                    for param_type in t.pos_param_types
                ), # tuple[type, ...]
                pos_kw_param_sigs = tuple(
                    ParamSig(
                        key = sig.key,
                        type = substitute_type_args(sig.type, subst_map),
                        optional = sig.optional 
                    )
                    for sig in t.pos_kw_param_sigs
                ), # tuple[ParamSig, ...]
                splat_pos_param_type = (
                    substitute_type_args(t.splat_pos_param_type, subst_map)
                    if t.splat_pos_param_type else
                    None
                ), # Optional[type]
                kw_param_sigs = tuple(
                    ParamSig(
                        key = sig.key,
                        type = substitute_type_args(sig.type, subst_map),
                        optional = sig.optional 
                    )
                    for sig in t.kw_param_sigs
                ), # tuple[ParamSig, ...]
                splat_kw_param_type = (
                    substitute_type_args(t.splat_kw_param_type, subst_map)
                    if t.splat_kw_param_type else
                    None
                ), # Optional[type]
                return_type = substitute_type_args(t.return_type, subst_map) # type
            )
            
        ),
        case_UnionType = lambda t : (

            UnionType(
                type_choices = tuple(
                    substitute_type_args(type_choice, subst_map)
                    for type_choice in t.type_choices
                ), # tuple[type, ...]
            )
        ),
        case_InterType = lambda t : (
            InterType(
                type_components = tuple(
                    substitute_type_args(type_component, subst_map)
                    for type_component in t.type_components
                ), # tuple[type, ...]
            )
        ),
        case_RecordType = lambda t : (
            update_RecordType(t,
                type_args = tuple(
                    substitute_type_args(type_arg, subst_map)
                    for type_arg in t.type_args
                )
            )
        ),
        case_FixedTupleType = lambda t : (
            update_FixedTupleType(t,
                item_types = tuple(
                    substitute_type_args(item_type, subst_map)
                    for item_type in t.item_types
                )
            )
        ),
        case_VariedTupleType = lambda t : (
            VariedTupleType(
                item_type = substitute_type_args(t.item_type, subst_map)
            )
        ),
        case_MappingType = lambda t : (
            MappingType(
                key_type = substitute_type_args(t.key_type, subst_map),
                value_type = substitute_type_args(t.value_type, subst_map),
            )
        ),
        case_DictType = lambda t : (
            DictType(
                key_type = substitute_type_args(t.key_type, subst_map),
                value_type = substitute_type_args(t.value_type, subst_map),
            )
        ),
        case_SetType = lambda t : (
            SetType(
                item_type = substitute_type_args(t.item_type, subst_map)
            )
        ),
        case_IterableType = lambda t : (
            IterableType(
                item_type = substitute_type_args(t.item_type, subst_map)
            )
        ),

        case_DictKeysType = lambda t : (
            DictKeysType(
                item_type = substitute_type_args(t.item_type, subst_map)
            )
        ),
        case_DictValuesType = lambda t : (
            DictValuesType(
                item_type = substitute_type_args(t.item_type, subst_map)
            )
        ),
        case_DictItemsType = lambda t : (
            DictItemsType(
                item_type = substitute_type_args(t.item_type, subst_map)
            )
        ),

        case_SequenceType = lambda t : (
            SequenceType(
                item_type = substitute_type_args(t.item_type, subst_map)
            )
        ),
        case_RangeType = lambda t : (
            RangeType(
                item_type = substitute_type_args(t.item_type, subst_map)
            )
        ),
        case_ListType = lambda t :( 
            ListType(
                item_type = substitute_type_args(t.item_type, subst_map)
            )
        ),

        case_ListLitType = lambda t :( 
            ListLitType(
                item_types = tuple(
                    substitute_type_args(item_type, subst_map)
                    for item_type in t.item_types
                )
            )
        ),
        case_GeneratorType = lambda t : ( 
            GeneratorType(
                yield_type = substitute_type_args(t.yield_type, subst_map),
                return_type = substitute_type_args(t.return_type, subst_map)
            )
        ),
        case_BoolType = lambda t : t,
        case_TrueType = lambda t : t,
        case_FalseType = lambda t : t,
        case_IntType = lambda t : t,
        case_IntLitType = lambda t : t,
        case_FloatType = lambda t : t,
        case_FloatLitType = lambda t : t,
        case_StrType = lambda t : t,
        case_StrLitType = lambda t : t,
        case_SliceType = lambda t : t
    ))


class UnifyError(Exception): pass

def get_mapping_key_value_types(t : type, inher_aux : InherAux) -> tuple[type, type]:
    if isinstance(t, DictType):
        return (t.key_type, t.value_type)
    elif isinstance(t, MappingType):
        return (t.key_type, t.value_type)
    elif isinstance(t, RecordType):
        class_record = from_static_path_to_ClassRecord(inher_aux, t.class_key)
        if class_record:
            substitution_map : PMap[str, type] = pmap({
                class_record.type_params[i].name : type_arg
                for i, type_arg in enumerate(t.type_args) 
            })

            for super_type in class_record.super_types:
                super_type = substitute_type_args(super_type, substitution_map)
                result = get_mapping_key_value_types(super_type, inher_aux)
                return result

            assert False 
        else:
            return (AnyType(), AnyType())
    else:
        assert False


def get_iterable_item_type_from_RecordType(t : RecordType, inher_aux : InherAux) -> type:
    class_record = from_static_path_to_ClassRecord(inher_aux, t.class_key)

    if class_record:
        substitution_map : PMap[str, type] = pmap({
            class_record.type_params[i].name : type_arg
            for i, type_arg in enumerate(t.type_args) 
        })

        for super_type in reversed(class_record.super_types):
            super_type = substitute_type_args(super_type, substitution_map)
            result = get_iterable_item_type(super_type, inher_aux)
            return result

        assert False
    else:
        return AnyType()

def get_iterable_item_type_from_UnionType(t : UnionType, inher_aux : InherAux) -> type:
    assert len(t.type_choices) > 0

    item = t.type_choices[0]
    for tc in t.type_choices[1:]:
        tc_item = get_iterable_item_type(tc, inher_aux)
        item = unionize_types(item, tc_item)
    return item

def get_iterable_item_type(t : type, inher_aux : InherAux) -> type:
    def fail():
        assert False

    return match_type(t, TypeHandlers(
        case_TypeType = lambda t : fail(),
        case_VarType = lambda t : fail(),
        case_EllipType = lambda t : fail(),
        case_AnyType = lambda t : AnyType(),
        case_ObjectType = lambda t : fail(),
        case_NoneType = lambda t : fail(), 
        case_ModuleType = lambda t : fail(),
        case_FunctionType = lambda t : fail(),
        case_UnionType = lambda t : get_iterable_item_type_from_UnionType(t, inher_aux),
        case_InterType = lambda t : fail(),
        case_RecordType = lambda t : get_iterable_item_type_from_RecordType(t, inher_aux),
        case_FixedTupleType = lambda t : unionize_all_types(t.item_types),
        case_VariedTupleType = lambda t : t.item_type,
        case_MappingType = lambda t : fail(),
        case_DictType = lambda t : t.key_type,
        case_SetType = lambda t : t.item_type,
        case_IterableType = lambda t : t.item_type,
        case_DictKeysType = lambda t : t.item_type,
        case_DictValuesType = lambda t : t.item_type,
        case_DictItemsType = lambda t : t.item_type,
        case_SequenceType = lambda t : t.item_type,
        case_RangeType = lambda t : t.item_type,
        case_ListType = lambda t : t.item_type,
        case_ListLitType = lambda t : unionize_all_types(t.item_types),
        case_GeneratorType = lambda t : t.yield_type,
        case_BoolType = lambda t : fail(),
        case_TrueType = lambda t : fail(),
        case_FalseType = lambda t : fail(),
        case_IntType = lambda t : fail(),
        case_IntLitType = lambda t : fail(),
        case_FloatType = lambda t : fail(),
        case_FloatLitType = lambda t : fail(),
        case_StrType = lambda t : StrType(),
        case_StrLitType = lambda t : StrType(),
        case_SliceType = lambda t : fail(),
    ))



def unify(pattern : pas.expr, type : type, inher_aux : InherAux) -> PMap[str, type]: 

    from typing import Iterator 
    def generate_items(exprs : pas.comma_exprs) -> Iterator[pas.expr]:
        while isinstance(exprs, pas.ConsExpr):
            assert exprs.head
            yield exprs.head
            assert exprs.tail
            exprs = exprs.tail 
        assert isinstance(exprs, pas.SingleExpr)
        assert exprs.content
        yield exprs.content

    if isinstance(pattern, pas.Name):
        return pmap({pattern.content : type})
    elif isinstance(pattern, pas.List):
        type_env : PMap[str, type] = m()
        assert pattern.content
        for p in generate_items(pattern.content):
            item_type = get_iterable_item_type(type, inher_aux)
            type_env += unify(p, item_type, inher_aux)

        return type_env 
    elif isinstance(pattern, pas.Tuple):
        if isinstance(type, FixedTupleType):

            type_env : PMap[str, type] = m()
            assert pattern.content
            for i, p in enumerate(generate_items(pattern.content)):
                type_env += unify(p, type.item_types[i], inher_aux)

            return type_env 
        else:
            type_env : PMap[str, type] = m()
            assert pattern.content
            for p in generate_items(pattern.content):
                item_type = get_iterable_item_type(type, inher_aux)
                type_env += unify(p, item_type, inher_aux)

            return type_env 
    elif isinstance(pattern, pas.Attribute):
        return m()
    elif isinstance(pattern, pas.Subscript):
        return m()
    else:
        raise UnifyError()


def from_static_path_to_ClassRecord(inher_aux : InherAux, path : str) -> ClassRecord | None:
    if path.startswith(inher_aux.external_path + "."):
        return inher_aux.class_env.get(path[len(inher_aux.external_path + ".")])

    sep = "."
    levels = path.split(sep)
    l = len(levels)
    package : PMap[str, ModulePackage] = pmap(inher_aux.package)

    for i, level in enumerate(levels):
        if package.get(level):

            mod_pack = package[level]

            class_env = mod_pack.class_env
            package = mod_pack.package
            if i + 1 < l: 
                remaining_path = ".".join(levels[i + 1:])
                class_record = class_env.get(remaining_path)
                if class_record: return class_record

    return None

def from_static_path_to_type(inher_aux : InherAux, path : str) -> type:

    if path == inher_aux.external_path:
        return  ModuleType(inher_aux.external_path) 

    elif path.startswith(inher_aux.external_path + "."):
        name = path[len(inher_aux.external_path + "."):]
        if not inher_aux.internal_path: 
            if inher_aux.local_env.get(name):
                return inher_aux.local_env[name].type
            else:
                return AnyType()
        elif inher_aux.global_env.get(name): 
            return inher_aux.global_env[name].type
        else:
            return AnyType()

    sep = "."
    levels = path.split(sep)
    l = len(levels)
    package : PMap[str, ModulePackage] = pmap(inher_aux.package)

    for i, level in enumerate(levels):
        if package.get(level):

            mod_pack = package[level]

            module = mod_pack.module
            package = mod_pack.package
            if i + 2 == l and module.get(levels[i + 1]):
                module_level = levels[i + 1]
                return module[module_level]
        else:
            return AnyType()
    
    return ModuleType(key = path)




def lookup(inher_aux : InherAux, key : str) -> Provenance:

    if inher_aux.local_env.get(key):
        return inher_aux.local_env[key]
    else:
        t = from_static_path_to_type(inher_aux, f"builtins.{key}")
        return make_Provenance(initialized=True, type=t)


from typing import Sequence
def args_params_compatible(
    pos_arg_types : Sequence[type],
    kw_arg_types : Mapping[str, type], 
    function_type : FunctionType,
    inher_aux : InherAux 
) -> bool:

    pos_param_compat : Iterable[bool] = [
        (
            i < len(pos_arg_types) and
            subsumes(pos_arg_types[i], param_type, inher_aux)
        )
        for i, param_type in enumerate(function_type.pos_param_types) 
    ] + [
        (
            j < len(pos_arg_types) and
            subsumes(pos_arg_types[j], param_sig.type, inher_aux)
        )
        for i, param_sig in enumerate(function_type.pos_kw_param_sigs) 
        for j in [i + len(function_type.pos_param_types)]
    ] + [
        subsumes(pos_type_arg, function_type.splat_pos_param_type, inher_aux)
        for i, pos_type_arg in enumerate(pos_arg_types)
        if i >= len(function_type.pos_param_types) + len(function_type.pos_kw_param_sigs)
        if function_type.splat_pos_param_type != None
    ]


    kw_param_compat : Iterable[bool] = [
        param_sig.optional or
        (
            kw_arg_types.get(param_sig.key) != None and
            subsumes(kw_arg_types[param_sig.key], param_sig.type, inher_aux)
        ) 
        for i, param_sig in enumerate(function_type.pos_kw_param_sigs) 
        for j in [i + len(function_type.pos_param_types)]
        if j >= len(pos_arg_types) 
    ] + [
        param_sig.optional or
        (
            kw_arg_types.get(param_sig.key) != None and
            subsumes(kw_arg_types[param_sig.key], param_sig.type, inher_aux)
        ) 
        for param_sig in function_type.kw_param_sigs 
    ] + [
        subsumes(kw_arg_type, function_type.splat_kw_param_type, inher_aux)
        for kw, kw_arg_type in kw_arg_types.items()
        if function_type.splat_kw_param_type != None
        if (
            not kw in {sig.key for sig in function_type.pos_kw_param_sigs} and
            not kw in {sig.key for sig in function_type.kw_param_sigs}
        )
    ]
    
    compatible =  (
        us.every(pos_param_compat, lambda x : x) and
        us.every(kw_param_compat, lambda x : x)
    )


    if not compatible:
        # TODO: this could be due to overloaded methods, which isn't currently supported
        raise ArgParamMismatchError()

    return compatible


def is_literal_string(content : str) -> bool:
    try:
        result = eval(content)
        return isinstance(result, str)
    except:
        return False


def from_inher_aux_to_primitive(inher_aux : InherAux):
    return ['A', 
        [from_type_to_primitive(t) for t in inher_aux.expr_types], 
        from_env_to_primitive(inher_aux.local_env), 
        from_env_to_primitive(inher_aux.nonlocal_env), 
        from_env_to_primitive(inher_aux.global_env)
    ]


def from_variant_to_primitive(v : variant) -> str:
    return match_variant(v, VariantHandlers(
        case_ContraVariant= lambda _ : "ContraVariant",
        case_CoVariant= lambda _ : "CoVariant",
        case_NoVariant= lambda _ : "NoVariant"
    ))


def from_module_to_primitive(module : PMap[str, type]) -> dict[str, list]:
    return {
        k : from_type_to_primitive(t) 
        for k, t in module.items()
    }

def from_package_to_primitive(package : PMap[str, ModulePackage]) -> dict[str, list]:
    return {
        k : [
            from_module_to_primitive(mp.module),
            from_package_to_primitive(mp.package)
        ]
        for k, mp in package.items()
    }


def from_ParamSig_to_primitive(p : ParamSig) -> list:
    return [p.key, from_type_to_primitive(p.type), p.optional]
    
def from_type_to_primitive(t : type) -> list:
    return match_type(t, TypeHandlers(
        case_TypeType = lambda t : ["TypeType", from_type_to_primitive(t.content)],
        case_VarType = lambda t : ["VarType", t.name, from_variant_to_primitive(t.variant)],
        case_EllipType = lambda t : ["EllipType"],
        case_AnyType = lambda t : ["AnyType"],
        case_ObjectType = lambda t : ["ObjectType"],
        case_NoneType = lambda t : ["NoneType"], 
        case_ModuleType = lambda t : ["ModuleType", t.key],
        case_FunctionType = lambda t : ["FunctionType",
            [from_type_to_primitive(t) for t in t.pos_param_types],
            [from_ParamSig_to_primitive(p) for p in t.pos_kw_param_sigs],
            [from_type_to_primitive(t.splat_pos_param_type)] if t.splat_pos_param_type else [],
            [from_ParamSig_to_primitive(p) for p in t.kw_param_sigs],
            [from_type_to_primitive(t.splat_kw_param_type)] if t.splat_kw_param_type else [],
            from_type_to_primitive(t.return_type)
        ],
        case_UnionType = lambda t : ["UnionType", [from_type_to_primitive(tc) for tc in t.type_choices]],
        case_InterType = lambda t : ["InterType", [from_type_to_primitive(tc) for tc in t.type_components]],
        case_RecordType = lambda t : ["RecordType", t.class_key, t.class_uid, [
            from_type_to_primitive(ta)
            for ta in t.type_args
        ]],
        case_FixedTupleType = lambda t : ["FixedTupleType", [from_type_to_primitive(it) for it in t.item_types]],
        case_VariedTupleType = lambda t : ["VariedTupleType", from_type_to_primitive(t.item_type)],
        case_MappingType = lambda t : ["MappingType", from_type_to_primitive(t.key_type), from_type_to_primitive(t.value_type)],
        case_DictType = lambda t : ["DictType", from_type_to_primitive(t.key_type), from_type_to_primitive(t.value_type)],
        case_SetType = lambda t : ["SetType", from_type_to_primitive(t.item_type)],
        case_IterableType = lambda t : ["IterableType", from_type_to_primitive(t.item_type)],
        case_DictKeysType = lambda t : ["DictKeysType", from_type_to_primitive(t.item_type)],
        case_DictValuesType = lambda t : ["DictValuesType", from_type_to_primitive(t.item_type)],
        case_DictItemsType = lambda t : ["DictItemsType", from_type_to_primitive(t.item_type)],
        case_SequenceType = lambda t : ["SequenceType", from_type_to_primitive(t.item_type)],
        case_RangeType = lambda t : ["RangeType", from_type_to_primitive(t.item_type)],
        case_ListType = lambda t : ["ListType", from_type_to_primitive(t.item_type)],
        case_ListLitType = lambda t : ["ListLitType", [from_type_to_primitive(it) for it in t.item_types]],
        case_GeneratorType = lambda t : ["GeneratorType", from_type_to_primitive(t.yield_type), from_type_to_primitive(t.return_type)],
        case_BoolType = lambda t : ["BoolType"],
        case_TrueType = lambda t : ["TrueType"],
        case_FalseType = lambda t : ["FalseType"],
        case_IntType = lambda t : ["IntType"],
        case_IntLitType = lambda t : ["IntLitType", t.literal],
        case_FloatType = lambda t : ["FloatType"],
        case_FloatLitType = lambda t : ["FloatLitType", t.literal],
        case_StrType = lambda t : ["StrType"],
        case_StrLitType = lambda t : ["StrLitType", t.literal],
        case_SliceType = lambda t : ["SliceType",
            from_type_to_primitive(t.start),
            from_type_to_primitive(t.stop),
            from_type_to_primitive(t.step)
        ],
    ))



def analyze_code(
    package : PMap[str, ModulePackage], 
    module_name, 
    code : str
) -> PMap[str, ModulePackage]:
    client : Client = spawn_analysis(package, module_name)

    gnode = pgs.parse(code)
    mod = pas.parse_from_generic_tree(gnode)
    abstract_tokens = pas.serialize(mod)

    last_inher_aux : InherAux = client.init
    a_keys_len = len(last_inher_aux.package.keys())
    for token in abstract_tokens:
        result = client.next(token)
        last_inher_aux = result

    b_keys_len = len(last_inher_aux.package.keys())
    assert b_keys_len >= a_keys_len

    return last_inher_aux.package 


from os import path
def analyze_modules_once(
    root_dir : str, 
    module_paths : Sequence[str], 
    package : PMap[str, ModulePackage]
) -> PMap[str, ModulePackage]:

    root_dir = path.abspath(root_dir)
    package_start = len(root_dir) + 1 

    file_paths = sorted(list(module_paths))
    success_count = 0
    for i, file_path in enumerate(file_paths):

        file_path_split = file_path.split(".") 
        if file_path_split[1] != "pyi": continue 
        module_segments = file_path_split[0][package_start:].split("/")
        module_path = (
            ".".join(module_segments[:-1])
            if module_segments[-1] == "__init__" else
            ".".join(module_segments)
        )
        assert path.isfile(file_path)

        # print(f"###############################")
        # print(f"## file_path : {file_path}")
        # print(f"## module_path : {module_path}")
        # print(f"###############################")

        try:
            with open(file_path) as f:
                code = f.read().strip()
                if code:
                    inher_aux = analyze_code(package, module_path, code)
                else:
                    package = insert_module(package, module_path, m())
                success_count += 1
        except Exception as ex:
            raise ex
        finally:
            print("")
            print("")
            print("-------------------------------")
            print(f"-- index : {i}")
            print(f"-- total : {len(file_paths)}")
            print(f"-- distance : {len(file_paths) - i}")
            print(f"-- file_path : {file_path}")
            print(f"-- module_path : {module_path}")
            # print(f"-- inher_aux.package : {from_package_to_primitive(inher_aux.package)}")
            print(f"-- success_count : {success_count}")
            print("-------------------------------")
            pass


    return package 


def collect_module_paths(dirpath : str) -> Sequence[str]:
    result = []
    for root, _, files in os.walk(dirpath):
        if "@python2" in root: continue
        for f in files:
            if f == "VERSIONS": continue
            file_path = path.abspath(f"{root}/{f}")
            result.append(file_path)
    return result

def analyze_modules_fixpoint(
    root_dir : str, 
    module_paths : Sequence[str], 
    package : PMap[str, ModulePackage]
) -> PMap[str, ModulePackage]:

    # print(f"fixpoint iteration count: {0}")
    in_package = package 
    in_package_prim = from_package_to_primitive(package)
    out_package = analyze_modules_once(root_dir, module_paths, in_package) 
    out_package_prim = from_package_to_primitive(out_package)
    count = 1
    # print(f"fixpoint iteration count: {count}")
    while out_package_prim != in_package_prim:
        in_package = out_package
        in_package_prim = out_package_prim 
        out_package = analyze_modules_once(root_dir, module_paths, in_package) 
        out_package_prim = from_package_to_primitive(out_package)
        count += 1
        # print(f"fixpoint iteration count: {count}")

    return out_package

def analyze_typeshed() -> PMap[str, ModulePackage]:
    stdlib_dirpath = us.project_path(f"../typeshed/stdlib")
    stdlib_module_paths = collect_module_paths(stdlib_dirpath)

    package : PMap[str, ModulePackage] = m()
    package = analyze_modules_fixpoint(stdlib_dirpath, stdlib_module_paths, package) 

    # other_libs_dirpath = us.project_path(f"../typeshed/stubs")
    # other_module_paths = collect_module_paths(other_libs_dirpath)
    # package = analyze_modules_fixpoint(other_libs_dirpath, other_module_paths, package, limit) 
    return package 

def make_demo(module_name : str, code : str, package : PMap[str, ModulePackage]) -> Iterator[tuple[pats.abstract_token, str, InherAux]]:
    gnode = pgs.parse(code)
    mod = pas.parse_from_generic_tree(gnode)
    abstract_tokens = pas.serialize(mod)

    partial_tokens = () 
    client : Client = spawn_analysis(package, module_name)

    for token in abstract_tokens:
        result = client.next(token)
        if isinstance(result, Exception):
            raise result
        else:
            inher_aux = result
            partial_tokens += (token,)

            yield (token, pats.concretize(partial_tokens), inher_aux)



def from_env_to_primitive(env : PMap[str, Provenance]) -> dict:
    return {
        symbol : [p.initialized, from_type_to_primitive(p.type)]
        for symbol, p in env.items()
    }


def copy_env(inher_aux : InherAux, path_extension : str) -> InherAux:
    if not inher_aux.internal_path:
        return update_InherAux(inher_aux,
            # copy local_decl into global_decl
            global_env = inher_aux.local_env,
            internal_path = path_extension 
        )
    else:
        return update_InherAux(inher_aux,
            # copy local_decl into nonlocal_decl
            nonlocal_env = inher_aux.nonlocal_env + inher_aux.local_env, 
            internal_path = f"{inher_aux.internal_path}.{path_extension}"
        )


def shift_env(inher_aux : InherAux, path_extension : str) -> InherAux:
    if not inher_aux.internal_path:
        return update_InherAux(inher_aux,
            # move local_decl into global_decl
            global_env = inher_aux.local_env,
            # reset local_decl
            local_env = m(), 
            internal_path = path_extension 
        )
    else:
        return update_InherAux(inher_aux,
            # move local_decl into nonlocal_decl 
            nonlocal_env = inher_aux.nonlocal_env + inher_aux.local_env, 
            # reset local_decl
            local_env = m(), 
            internal_path = f"{inher_aux.internal_path}.{path_extension}"
        )


def traverse_aux(inher_aux : InherAux, synth_aux : SynthAux) -> InherAux:
    local_env = inher_aux.local_env 
    for sub in synth_aux.env_subtractions:
        local_env.remove(sub)

    return update_InherAux(inher_aux, 
        local_env = local_env + synth_aux.env_additions,
        class_env = inher_aux.class_env + synth_aux.class_additions,
        expr_types = synth_aux.expr_types
    )

def cross_join_aux(true_body_aux : SynthAux, false_body_aux : SynthAux) -> SynthAux:

    subtractions : PSet[str] = s()
    for sub in true_body_aux.env_subtractions:
        if sub in false_body_aux.env_subtractions:
            subtractions = subtractions.add(sub)

    body_additions : PMap[str, Provenance] = m()
    for target, dec in true_body_aux.env_additions.items():
        if (
            dec and 
            dec.initialized and 
            target in false_body_aux.env_additions.keys() and 
            (not false_body_aux.env_additions[target] or
                (false_body_aux.env_additions[target]).initialized)
        ):
            body_additions = body_additions.set(target, dec)

    return make_SynthAux(
        env_subtractions = subtractions,
        env_additions = body_additions
    )


import threading
from queue import Queue

@dataclass
class Client: 
    init : InherAux
    init_prim : list 
    next : Callable[[abstract_token], InherAux]
    next_prim : Callable[[list], list | None]


def insert_module(package : PMap[str, ModulePackage], rpath : Sequence[str], module : PMap[str, type]) -> PMap[str, ModulePackage]:

    assert len(rpath) > 0 
    hd = rpath[-1]
    tl = rpath[:-1]

    if not tl:
        new_module_package = (
            update_ModulePackage(package[hd], module = module) 
            if package.get(hd) else
            make_ModulePackage(module = module)
        )

        return package + pmap({hd : new_module_package})
    else:
        empty_package : PMap[str, ModulePackage] = m()
        next_package : PMap[str, ModulePackage] = (
            package[hd].package
            if package.get(hd) else
            empty_package
        )
        return package + insert_module(next_package, tl, module)


def from_package_get_ModulePackage(package : PMap[str, ModulePackage], external_path : str) -> ModulePackage | None:
    assert external_path
    levels = external_path.split(".")
    result : ModulePackage | None = package.get(levels[0])

    for level in levels[1:]:

        if result:
            result = result.package.get(level)
        else:
            return None


    return result



def spawn_analysis(package : PMap[str, ModulePackage], module_name : str) -> Client:

    in_stream : Queue[abstract_token] = Queue()
    out_stream : Queue[Union[InherAux, Exception]] = Queue()

    server : Server = Server(in_stream, out_stream)

    mp = from_package_get_ModulePackage(package, module_name)
    inher_aux = (
        make_InherAux(
            external_path = module_name, 
            package = package,
            local_env = pmap((sym, make_Provenance(initialized=True, type=t)) for sym, t in mp.module.items()),
            class_env = mp.class_env
        )
        if mp else
        make_InherAux(external_path = module_name, package = package)
    )

    def run():
        try:
            nonlocal inher_aux
            token = in_stream.get()
            synth = server.crawl_module(token, inher_aux)

            module : PMap[str, type] = pmap({
                k : p.type
                for k, p in synth.aux.env_additions.items()
            })

            rpath = [s for s in reversed(inher_aux.external_path.split("."))]
            final_inher_aux = update_InherAux(inher_aux,
                external_path = "",
                global_env = m(),
                nonlocal_env = m(),
                local_env = m(),
                class_env = m(), 
                package = insert_module(inher_aux.package, rpath, module)
            )
            out_stream.put(final_inher_aux)
        except Exception as ex:
            out_stream.put(ex)


    thread = threading.Thread(target = run)
    thread.start()

    def next(tok : abstract_token) -> InherAux:
        in_stream.put(tok) 
        out = out_stream.get() 
        if isinstance(out, Exception):
            raise out
        else:
            return out


    last_inher_prim = from_inher_aux_to_primitive(inher_aux)
    def next_prim(ptok : list) -> list | None:
        nonlocal last_inher_prim
        tok = ats.from_primitive(ptok)
        out_inher = next(tok)
        out_inher_prim = from_inher_aux_to_primitive(out_inher)
        if (out_inher_prim == last_inher_prim):
            return None
        else:
            last_inher_prim = out_inher_prim
            return out_inher_prim

    return Client(
        init = inher_aux, 
        init_prim = from_inher_aux_to_primitive(inher_aux), 
        next = next, 
        next_prim = next_prim
    ) 



class AnalysisError(crawler.Error):
    pass


def unify_iteration(inher_aux : InherAux, pattern : pas.expr, iter_type : type) -> PMap[str, type]:
    item_type = get_iterable_item_type(iter_type, inher_aux)
    target_types = unify(pattern, item_type, inher_aux)

    for k, t in target_types.items():
        prov = lookup(inher_aux, k)
        assert subsumes(t, prov.type, inher_aux)
    return target_types


def check_forward_references(inher_aux : InherAux, body_aux : SynthAux, body_tree : pas.statements):

    for body_aux_name in body_aux.names:
        assert (
            body_aux.env_additions.get(body_aux_name) != None or
            body_aux_name in inher_aux.local_env
        )

    body_inher_aux = traverse_aux(inher_aux, body_aux)
    analyze_statements(body_tree, body_inher_aux)

def analyze_statements(statements_ast : pas.statements, inher_aux : InherAux) -> SynthAux:

    in_stream : Queue[abstract_token] = Queue()
    out_stream : Queue[Union[InherAux, Exception]] = Queue()

    return_stream : Queue[SynthAux] = Queue()

    server : Server = Server(in_stream, out_stream)

    def run():
        tok = in_stream.get()
        synth = server.crawl_statements(tok, inher_aux)
        out_stream.put(inher_aux)
        return_stream.put(synth.aux)

    import threading
    thread = threading.Thread(target = run)
    thread.start()

    from lib.python_ast_serialize_autogen import from_statements as serialize_statements
    tokens : tuple[abstract_token, ...] = serialize_statements(statements_ast)
    for tok in tokens:
        in_stream.put(tok)
        out_stream.get()

    return return_stream.get()


def analyze_expr(expr_ast : pas.expr, inher_aux : InherAux) -> SynthAux:

    in_stream : Queue[abstract_token] = Queue()
    out_stream : Queue[Union[InherAux, Exception]] = Queue()

    return_stream : Queue[SynthAux] = Queue()

    server : Server = Server(in_stream, out_stream)

    def run():
        tok = in_stream.get()
        synth = server.crawl_expr(tok, inher_aux)
        out_stream.put(inher_aux)
        return_stream.put(synth.aux)

    import threading
    thread = threading.Thread(target = run)
    thread.start()

    from lib.python_ast_serialize_autogen import from_expr as serialize_expr
    tokens : tuple[abstract_token, ...] = serialize_expr(expr_ast)
    for tok in tokens:
        in_stream.put(tok)
        out_stream.get()

    return return_stream.get()

class Server(crawler.Server[InherAux, SynthAux]):

    def __init__(self, in_stream : Queue[abstract_token], out_stream : Queue[Union[InherAux, Exception]]):  
        super().__init__(in_stream, out_stream)

    # override parent class method
    def traverse_auxes(self, inher_aux : InherAux, synth_auxes : tuple[SynthAux]) -> InherAux:
        last_synth_aux = (
            synth_auxes[-1]
            if len(synth_auxes) > 0 else
            None
        )
        if last_synth_aux:
            return traverse_aux(inher_aux, last_synth_aux)
        else:
            return inher_aux

    # override parent class method
    def synthesize_auxes(self, auxes : tuple[SynthAux]) -> SynthAux:

        class_additions : PMap[str, ClassRecord] = m()
        env_subtractions : PSet[str] = s()
        env_additions : PMap[str, Provenance] = m()
        names : PSet[str] = s()

        method_names : tuple[str, ...] = ()
        expr_types : tuple[type, ...] = ()

        kw_types : PMap[str, type] = m()

        return_types : tuple[type, ...] = ()
        yield_types : tuple[type, ...] = ()

        var_types : tuple[VarType, ...] = ()

        param_sig : Optional[ParamSig] = None 
        pos_param_types : tuple[type, ...] = ()
        pos_kw_param_sigs : tuple[ParamSig, ...] = ()
        list_splat_param_type : Optional[type] = None
        kw_param_sigs : tuple[ParamSig, ...] = ()
        dict_splat_param_type : Optional[type] = None

        import_names  : PMap[str, str] = m()


        for aux in auxes:

            class_additions = class_additions + aux.class_additions

            for sub in aux.env_subtractions:
                if env_additions.get(sub):
                    env_additions = env_additions.remove(sub)

            env_subtractions = env_subtractions.update(aux.env_subtractions)
            env_additions = env_additions + aux.env_additions
            names = names.update(aux.names)

            method_names = method_names + aux.method_names

            expr_types = expr_types + aux.expr_types

            kw_types = kw_types + aux.kw_types

            return_types = return_types + aux.return_types
            yield_types = yield_types + aux.yield_types

            var_types = var_types + aux.var_types

            param_sig = param_sig if param_sig else aux.param_sig

            pos_param_types = pos_param_types + aux.pos_param_types
            pos_kw_param_sigs = pos_kw_param_sigs + aux.pos_kw_param_sigs
            list_splat_param_type = list_splat_param_type if list_splat_param_type else aux.splat_pos_param_type
            kw_param_sigs = kw_param_sigs + aux.kw_param_sigs 
            dict_splat_param_type = dict_splat_param_type if dict_splat_param_type else aux.splat_kw_param_type 

            import_names = import_names + aux.import_names

        return SynthAux(
            class_additions,
            env_subtractions, env_additions, 
            names, 
            method_names,
            expr_types, 
            kw_types,
            return_types,
            yield_types,
            var_types,
            param_sig, 
            pos_param_types, pos_kw_param_sigs, list_splat_param_type, kw_param_sigs, dict_splat_param_type,
            import_names
        )

    # synthesize: expr <-- BoolOp
    def synthesize_for_expr_BoolOp(self, 
        inher_aux : InherAux,
        left_tree : pas.expr, 
        left_aux : SynthAux,
        rator_tree : pas.bool_rator, 
        rator_aux : SynthAux,
        right_tree : pas.expr, 
        right_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        # TODO: check that the rator and rhs operand correspond to a method on the lhs operand

        bool_type = make_BoolType()

        synth_aux = update_SynthAux(
            self.synthesize_auxes(tuple([left_aux, rator_aux, right_aux])),
            expr_types = (bool_type,)
        )

        return crawler.Synth[SynthAux](
            tree = pas.BoolOp(left_tree, rator_tree, right_tree),
            aux = synth_aux
        )
    

    # synthesize: expr <-- AssignExpr
    def synthesize_for_expr_AssignExpr(self, 
        inher_aux : InherAux,
        target_tree : pas.expr, 
        target_aux : SynthAux,
        content_tree : pas.expr, 
        content_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:

        # TODO: if source is of AnnoType(VarType), check that target symbol matches VarType's symbol

        # check name compatability between target and source expressions 
        for name in content_aux.names:
            assert (
                not (name in target_aux.names) or (
                    name in inher_aux.local_env
                )
            )
        assert len(content_aux.expr_types) == 1
        content_type = content_aux.expr_types[0]
        return crawler.Synth[SynthAux](
            tree = pas.AssignExpr(target_tree, content_tree),
            aux = update_SynthAux(content_aux,
                env_additions = (
                    content_aux.env_additions +
                    pmap({
                        k : make_Provenance(initialized=True, type = t)
                        for k, t in unify(target_tree, content_type, inher_aux).items() 
                    })
                ),
            )
        )

    
    # synthesize: expr <-- BinOp
    def synthesize_for_expr_BinOp(self, 
        inher_aux : InherAux,
        left_tree : pas.expr, 
        left_aux : SynthAux,
        rator_tree : pas.bin_rator, 
        rator_aux : SynthAux,
        right_tree : pas.expr, 
        right_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:

        assert len(left_aux.expr_types) == 1
        left_type = left_aux.expr_types[0]
        assert len(right_aux.expr_types) == 1
        right_type = right_aux.expr_types[0]

        expr_type = AnyType()
        if (
            (isinstance(left_type, TypeType) or isinstance(right_type, TypeType)) and
            isinstance(rator_tree, pas.BitOr)
        ):
            left_instance_type = coerce_to_TypeType(left_type).content
            right_instance_type = coerce_to_TypeType(right_type).content
            union_type = unionize_types(left_instance_type, right_instance_type)
            expr_type = TypeType(union_type)
        else:

            method_name = pas.from_bin_rator_to_method_name(rator_tree)
            method_type = field_type(left_type, method_name, inher_aux)

            if isinstance(method_type, FunctionType):
                assert args_params_compatible(
                    [right_type], {}, 
                    method_type, inher_aux
                )
                expr_type = method_type.return_type

        return crawler.Synth[SynthAux](
            tree = pas.BinOp(left_tree, rator_tree, right_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([left_aux, right_aux])),
                expr_types = (expr_type,)
            )
        )
    

    # synthesize: expr <-- UnaryOp 
    def synthesize_for_expr_UnaryOp(self, 
        inher_aux : InherAux,
        rator_tree : pas.unary_rator, 
        rator_aux : SynthAux,
        rand_tree : pas.expr, 
        rand_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert len(rand_aux.expr_types) == 1
        rand_type = rand_aux.expr_types[0]
        method_name = pas.from_unary_rator_to_method_name(rator_tree)
        method_type = field_type(rand_type, method_name, inher_aux)
        return_type = AnyType()
        if isinstance(method_type, FunctionType):
            assert args_params_compatible(
                [], {}, 
                method_type, inher_aux
            )
        else:
            return_type = AnyType() 

        return crawler.Synth[SynthAux](
            tree = pas.UnaryOp(rator_tree, rand_tree),
            aux = update_SynthAux(rand_aux, 
                expr_types = (return_type,)
            )
        )

    # synthesize: expr <-- Lambda
    def synthesize_for_expr_Lambda(self, 
        inher_aux : InherAux,
        params_tree : pas.parameters, 
        params_aux : SynthAux,
        body_tree : pas.expr, 
        body_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert len(body_aux.expr_types) == 1
        inferred_type = make_FunctionType(
            pos_param_types = params_aux.pos_param_types,
            return_type = body_aux.expr_types[0]
        )
        return crawler.Synth[SynthAux](
            tree = pas.Lambda(params_tree, body_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([params_aux, body_aux])),
                expr_types = (inferred_type,)
            )  
        )
    
    # synthesize: expr <-- IfExp 
    def synthesize_for_expr_IfExp(self, 
        inher_aux : InherAux,
        body_tree : pas.expr, 
        body_aux : SynthAux,
        test_tree : pas.expr, 
        test_aux : SynthAux,
        orelse_tree : pas.expr, 
        orelse_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert len(body_aux.expr_types) == 1
        body_type = body_aux.expr_types[0]
        assert len(orelse_aux.expr_types) == 1
        orelse_type = orelse_aux.expr_types[0]
        return crawler.Synth[SynthAux](
            tree = pas.IfExp(body_tree, test_tree, orelse_tree),
            aux = update_SynthAux(test_aux,
                expr_types=(unionize_types(body_type, orelse_type),)
            )
        )


    # synthesize: dictionary_item <-- Field
    def synthesize_for_dictionary_item_Field(self, 
        inher_aux : InherAux,
        key_tree : pas.expr, 
        key_aux : SynthAux,
        content_tree : pas.expr, 
        content_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert len(key_aux.expr_types) == 1
        key_type = key_aux.expr_types[0]
        assert len(content_aux.expr_types) == 1
        content_type = content_aux.expr_types[0]
        return crawler.Synth[SynthAux](
            tree = pas.Field(key_tree, content_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([key_aux, content_aux])),
                expr_types = (key_type, content_type)
            ) 
        )

    # synthesize: dictionary_content <-- ConsDictionaryItem
    def synthesize_for_dictionary_content_ConsDictionaryItem(self, 
        inher_aux : InherAux,
        head_tree : pas.dictionary_item, 
        head_aux : SynthAux,
        tail_tree : pas.dictionary_content, 
        tail_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert len(head_aux.expr_types) == 2
        assert len(tail_aux.expr_types) == 2

        head_key_type = head_aux.expr_types[0]
        head_value_type = head_aux.expr_types[1]

        tail_key_type = head_aux.expr_types[0]
        tail_value_type = head_aux.expr_types[1]

        key_type = head_key_type
        if head_key_type != tail_key_type:
            key_type = unionize_types(head_key_type, tail_key_type)

        value_type = head_value_type
        if head_value_type != tail_value_type:
            value_type = unionize_types(head_value_type, tail_value_type)
        
        return crawler.Synth[SynthAux](
            tree = pas.ConsDictionaryItem(head_tree, tail_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([head_aux, tail_aux])),
                expr_types = (key_type, value_type)
            )
        )
    
    # synthesize: expr <-- Dictionary
    def synthesize_for_expr_Dictionary(self, 
        inher_aux : InherAux,
        content_tree : pas.dictionary_content, 
        content_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert len(content_aux.expr_types) == 2

        dict_type = DictType(
            key_type = content_aux.expr_types[0],
            value_type = content_aux.expr_types[1]
        )

        return crawler.Synth[SynthAux](
            tree = pas.Dictionary(content_tree),
            aux = update_SynthAux(content_aux,
                expr_types = (dict_type,)
            )
        )
    
    # synthesize: expr <-- EmptyDictionary
    def synthesize_for_expr_EmptyDictionary(self, 
        inher_aux : InherAux
    ) -> crawler.Synth[SynthAux]:


        dict_type = DictType(
            key_type = AnyType(),
            value_type = AnyType()
        )

        return crawler.Synth[SynthAux](
            tree = pas.EmptyDictionary(),
            aux = make_SynthAux(
                expr_types = (dict_type,) 
            )
        )


    # synthesize: expr <-- Set
    def synthesize_for_expr_Set(self, 
        inher_aux : InherAux,
        content_tree : pas.comma_exprs, 
        content_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert len(content_aux.expr_types) > 0

        item_type = content_aux.expr_types[0] 
        for t in content_aux.expr_types[1:]:
            item_type = unionize_types(t, item_type)

        set_type = make_SetType(
            item_type = item_type 
        )

        return crawler.Synth[SynthAux](
            tree = pas.Set(content_tree),
            aux = update_SynthAux(content_aux,
                expr_types = (set_type,)
            )
        )

    # synthesize: constraint <-- AsyncConstraint
    def synthesize_for_constraint_AsyncConstraint(self, 
        inher_aux : InherAux,
        target_tree : pas.expr, 
        target_aux : SynthAux,
        search_space_tree : pas.expr, 
        search_space_aux : SynthAux,
        filts_tree : pas.constraint_filters, 
        filts_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert len(search_space_aux.expr_types) == 1
        search_space_type = search_space_aux.expr_types[0]

        return crawler.Synth[SynthAux](
            tree = pas.AsyncConstraint(target_tree, search_space_tree, filts_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([target_aux, search_space_aux, filts_aux])),
                env_additions = pmap({
                    k : make_Provenance(initialized=True, type=t)
                    for k, t in unify_iteration(inher_aux, target_tree, search_space_type).items()
                })
            )
        )
    
    # synthesize: constraint <-- Constraint
    def synthesize_for_constraint_Constraint(self, 
        inher_aux : InherAux,
        target_tree : pas.expr, 
        target_aux : SynthAux,
        search_space_tree : pas.expr, 
        search_space_aux : SynthAux,
        filts_tree : pas.constraint_filters, 
        filts_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert len(search_space_aux.expr_types) == 1
        search_space_type = search_space_aux.expr_types[0]
        return crawler.Synth[SynthAux](
            tree = pas.Constraint(target_tree, search_space_tree, filts_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([target_aux, search_space_aux, filts_aux])),
                env_additions = pmap({
                    k : make_Provenance(initialized=True, type=t)
                    for k, t in unify_iteration(inher_aux, target_tree, search_space_type).items()
                })
            )
        )
     
    
    # synthesize: expr <-- ListComp
    def synthesize_for_expr_ListComp(self, 
        inher_aux : InherAux,
        content_tree : pas.expr, 
        content_aux : SynthAux,
        constraints_tree : pas.comprehension_constraints, 
        constraints_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        # analysis needs to pass information from right to left, so must reanalyze left element
        content_aux = analyze_expr(content_tree, traverse_aux(inher_aux, constraints_aux))
        assert len(content_aux.expr_types) == 1
        content_type = content_aux.expr_types[0]

        return crawler.Synth[SynthAux](
            tree = pas.ListComp(content_tree, constraints_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([content_aux, constraints_aux])),
                expr_types = (ListType(
                    item_type = content_type
                ),)
            )
        )
    
    # synthesize: expr <-- SetComp
    def synthesize_for_expr_SetComp(self, 
        inher_aux : InherAux,
        content_tree : pas.expr, 
        content_aux : SynthAux,
        constraints_tree : pas.comprehension_constraints, 
        constraints_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        # analysis needs to pass information from right to left, so must reanalyze left element
        content_aux = analyze_expr(content_tree, traverse_aux(inher_aux, constraints_aux))
        assert len(content_aux.expr_types) == 1
        content_type = content_aux.expr_types[0]

        return crawler.Synth[SynthAux](
            tree = pas.SetComp(content_tree, constraints_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([content_aux, constraints_aux])),
                expr_types = (SetType(
                    item_type = content_type
                ),)
            )
        )
    
    # synthesize: expr <-- DictionaryComp
    def synthesize_for_expr_DictionaryComp(self, 
        inher_aux : InherAux,
        key_tree : pas.expr, 
        key_aux : SynthAux,
        content_tree : pas.expr, 
        content_aux : SynthAux,
        constraints_tree : pas.comprehension_constraints, 
        constraints_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        # analysis needs to pass information from right to left, so must reanalyze left element
        key_aux = analyze_expr(key_tree, traverse_aux(inher_aux, constraints_aux))
        content_aux = analyze_expr(content_tree, traverse_aux(inher_aux, constraints_aux))
        assert len(key_aux.expr_types) == 1
        key_type = key_aux.expr_types[0]
        assert len(content_aux.expr_types) == 1
        content_type = content_aux.expr_types[0]

        return crawler.Synth[SynthAux](
            tree = pas.DictionaryComp(key_tree, content_tree, constraints_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([key_aux, content_aux, constraints_aux])),
                expr_types = (DictType(
                    key_type = key_type,
                    value_type = content_type,
                ),)
            )
        )
    
    # synthesize: expr <-- GeneratorExp
    def synthesize_for_expr_GeneratorExp(self, 
        inher_aux : InherAux,
        content_tree : pas.expr, 
        _ : SynthAux,
        constraints_tree : pas.comprehension_constraints, 
        constraints_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        # analysis needs to pass information from right to left, so must reanalyze left element
        content_aux = analyze_expr(content_tree, traverse_aux(inher_aux, constraints_aux))
        assert len(content_aux.expr_types) == 1
        content_type = content_aux.expr_types[0]

        return crawler.Synth[SynthAux](
            tree = pas.GeneratorExp(content_tree, constraints_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([content_aux, constraints_aux])),
                expr_types = (GeneratorType(
                    yield_type = content_type,
                    return_type = NoneType()
                ),)
            )
        )

    
    # synthesize: expr <-- Await
    def synthesize_for_expr_Await(self, 
        inher_aux : InherAux,
        content_tree : pas.expr, 
        content_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        # TODO: inferred type
        # check that content_aux.inferred type is subtype of Awaitable[T]
        # async functions return instances of Coroutine <: Awaitable
        # inferred_type = T
        return crawler.Synth[SynthAux](
            tree = pas.Await(content_tree),
            aux = self.synthesize_auxes(tuple([content_aux])) 
        )
    
    # synthesize: expr <-- YieldNothing
    def synthesize_for_expr_YieldNothing(self, 
        inher_aux : InherAux
    ) -> crawler.Synth[SynthAux]:
        # TODO: inferred type
        # set yield_type to None in synth_aux
        # at function definition record return type as be a Generator <: Iterator <: Iterable 
        return crawler.Synth[SynthAux](
            tree = pas.YieldNothing(),
            aux = make_SynthAux(
                yield_types = (NoneType(),)
            )
        )
    
    # synthesize: expr <-- Yield
    def synthesize_for_expr_Yield(self, 
        inher_aux : InherAux,
        content_tree : pas.expr, 
        content_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        # at function definition record return type as be a Generator <: Iterator <: Iterable 
        assert len(content_aux.expr_types) == 1
        expr_type = content_aux.expr_types[0]
        return crawler.Synth[SynthAux](
            tree = pas.Yield(content_tree),
            aux = update_SynthAux(content_aux,
                yield_types = (expr_type,)
            )
        )
    
    # synthesize: expr <-- YieldFrom
    def synthesize_for_expr_YieldFrom(self, 
        inher_aux : InherAux,
        content_tree : pas.expr, 
        content_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert len(content_aux.expr_types) == 1
        expr_type = content_aux.expr_types[0]
        item_type = get_iterable_item_type(expr_type, inher_aux)
        return crawler.Synth[SynthAux](
            tree = pas.YieldFrom(content_tree),
            aux = update_SynthAux(content_aux,
                yield_types = (item_type,)
            )
        )

    # synthesize: CompareRight
    def synthesize_for_CompareRight(self, 
        inher_aux : InherAux,
        rator_tree : pas.cmp_rator, 
        rator_aux : SynthAux,
        rand_tree : pas.expr, 
        rand_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        method_name = pas.from_cmp_rator_to_method_name(rator_tree)
        return crawler.Synth[SynthAux](
            tree = crawler.CompareRight(rator_tree, rand_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([rator_aux, rand_aux])), 
                method_names = tuple([method_name])
            )
        )
    
    # synthesize: expr <-- Compare
    def synthesize_for_expr_Compare(self, 
        inher_aux : InherAux,
        left_tree : pas.expr, 
        left_aux : SynthAux,
        comps_tree : pas.comparisons, 
        comps_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:

        assert len(left_aux.expr_types) == 1
        left_type = left_aux.expr_types[0]

        assert len(comps_aux.expr_types) == len(comps_aux.method_names) 
        for i, method_name in enumerate(comps_aux.method_names):
            right_type = comps_aux.expr_types[i]
            method_type = field_type(left_type, method_name, inher_aux)
            if isinstance(method_type, FunctionType):
                assert args_params_compatible(
                    [right_type], {}, 
                    method_type, inher_aux
                )
            # update:
            left_type = right_type

        return crawler.Synth[SynthAux](
            tree = pas.Compare(left_tree, comps_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([left_aux, comps_aux])),
                expr_types= tuple([BoolType()]),
                method_names = () 
            )
        )
    
    # synthesize: expr <-- Call
    def synthesize_for_expr_Call(self, 
        inher_aux : InherAux,
        func_tree : pas.expr, 
        func_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:

        inferred_type : type
        assert len(func_aux.expr_types) == 1
        func_type = func_aux.expr_types[0]
        if isinstance(func_type, FunctionType):
            inferred_type = func_type.return_type
        elif isinstance(func_type, TypeType):
            inferred_type = func_type.content 
        elif isinstance(func_type, AnyType):
            inferred_type = AnyType() 
        else:
            assert False

        return crawler.Synth[SynthAux](
            tree = pas.Call(func_tree),
            aux = update_SynthAux(func_aux,
                expr_types = tuple([inferred_type])
            )
        )

    # synthesize: keyword <-- NamedKeyword
    def synthesize_for_keyword_NamedKeyword(self, 
        inher_aux : InherAux,
        name_tree : str, 
        name_aux : SynthAux,
        content_tree : pas.expr, 
        content_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:

        assert len(content_aux.expr_types) == 1
        content_type = content_aux.expr_types[0]

        return crawler.Synth[SynthAux](
            tree = crawler.NamedKeyword(name_tree, content_tree),
            aux = make_SynthAux(
                kw_types = pmap({name_tree : content_type})
            ) 
        )
    
    # synthesize: keyword <-- SplatKeyword
    def synthesize_for_keyword_SplatKeyword(self, 
        inher_aux : InherAux,
        content_tree : pas.expr, 
        content_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert len(content_aux.expr_types) == 1
        content_type = content_aux.expr_types[0]

        (key_type, value_type) = get_mapping_key_value_types(content_type, inher_aux)
        assert isinstance(key_type, StrType)

        return crawler.Synth[SynthAux](
            tree = pas.SplatKeyword(content_tree),
            aux = update_SynthAux(content_aux) 
        )
    
    # synthesize: expr <-- CallArgs
    def synthesize_for_expr_CallArgs(self, 
        inher_aux : InherAux,
        func_tree : pas.expr, 
        func_aux : SynthAux,
        args_tree : pas.arguments, 
        args_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:



        expr_type = None

        assert len(func_aux.expr_types) == 1
        func_type = func_aux.expr_types[0]
        if isinstance(func_type, FunctionType):
            assert args_params_compatible(
                args_aux.expr_types,
                args_aux.kw_types, 
                func_type, inher_aux
            )
            expr_type = func_type.return_type

        elif isinstance(func_type, TypeType):
            class_key = get_class_key(func_type.content)

            if class_key == "typing.TypeVar": 

                pos_arg_types = args_aux.expr_types
                kw_arg_types = args_aux.kw_types

                name = ""
                if len(pos_arg_types) > 0: 
                    name_type = pos_arg_types[0]
                    assert isinstance(name_type, StrLitType) 
                    name = name_type.literal 
                else:
                    name_type = kw_arg_types["name"]
                    assert isinstance(name_type, StrLitType) 
                    name = name_type.literal 


                variant = NoVariant()
                assert not (
                    isinstance(kw_arg_types.get("covariant"), TrueType) and
                    isinstance(kw_arg_types.get("contravariant"), TrueType)
                )

                if isinstance(kw_arg_types.get("covariant"), TrueType):
                    variant = CoVariant()
                elif isinstance(kw_arg_types.get("contravariant"), TrueType):
                    variant = ContraVariant()
            
                expr_type = TypeType(VarType(name = name, variant = variant))
            else:

                class_key = get_class_key(func_type.content)
                class_record = from_static_path_to_ClassRecord(inher_aux, class_key)

                if class_record:
                    init_type = static_field_type(class_record, "__init__", inher_aux)
                    assert isinstance(init_type, FunctionType)

                    assert args_params_compatible(
                        args_aux.expr_types,
                        args_aux.kw_types, 
                        init_type, inher_aux
                    )

                expr_type = func_type.content 
        else:
            expr_type = AnyType()


        assert expr_type
        return crawler.Synth[SynthAux](
            tree = pas.CallArgs(func_tree, args_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([func_aux, args_aux])),
                expr_types = tuple([expr_type])
            )
        )
    
    # synthesize: expr <-- Integer
    def synthesize_for_expr_Integer(self, 
        inher_aux : InherAux,
        content_tree : str, 
        content_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        return crawler.Synth[SynthAux](
            tree = pas.Integer(content_tree),
            aux = update_SynthAux(content_aux,
                expr_types = tuple([IntLitType(literal = content_tree)])
            )
        )
    
    # synthesize: expr <-- Float
    def synthesize_for_expr_Float(self, 
        inher_aux : InherAux,
        content_tree : str, 
        content_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        return crawler.Synth[SynthAux](
            tree = pas.Float(content_tree),
            aux = update_SynthAux(content_aux,
                expr_types = tuple([FloatLitType(literal = content_tree)])
            )
        )

    # synthesize: sequence_string <-- ConsStr
    def synthesize_for_sequence_string_ConsStr(self, 
        inher_aux : InherAux,
        head_tree : str, 
        head_aux : SynthAux,
        tail_tree : pas.sequence_string, 
        tail_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:

        expr_type = (
            StrLitType(literal = head_tree)
            if is_literal_string(head_tree) else
            StrType()
        )

        return crawler.Synth[SynthAux](
            tree = pas.ConsStr(head_tree, tail_tree),
            aux = make_SynthAux(
                expr_types = tuple([expr_type]) + tail_aux.expr_types
            )
        )
    
    # synthesize: sequence_string <-- SingleStr
    def synthesize_for_sequence_string_SingleStr(self, 
        inher_aux : InherAux,
        content_tree : str, 
        content_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:

        expr_type = (
            StrLitType(literal = content_tree)
            if is_literal_string(content_tree) else
            StrType()
        )
        return crawler.Synth[SynthAux](
            tree = pas.SingleStr(content_tree),
            aux = make_SynthAux(
                expr_types = tuple([expr_type])
            ) 
        )
    
    # synthesize: expr <-- ConcatString
    def synthesize_for_expr_ConcatString(self, 
        inher_aux : InherAux,
        content_tree : pas.sequence_string, 
        content_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:

        assert len(content_aux.expr_types) > 0
        index_0_type = content_aux.expr_types[0]

        expr_type = (
            content_aux.expr_types[0]
            if len(content_aux.expr_types) == 1 else 
            StrType()
        )

        return crawler.Synth[SynthAux](
            tree = pas.ConcatString(content_tree),
            aux = update_SynthAux(content_aux,
                expr_types = tuple([expr_type])
            )
        )
    
    # synthesize: expr <-- True_
    def synthesize_for_expr_True_(self, 
        inher_aux : InherAux
    ) -> crawler.Synth[SynthAux]:
        return crawler.Synth[SynthAux](
            tree = pas.True_(),
            aux = make_SynthAux(
                expr_types = tuple([TrueType()])
            )
        )
    
    # synthesize: expr <-- False_
    def synthesize_for_expr_False_(self, 
        inher_aux : InherAux
    ) -> crawler.Synth[SynthAux]:
        return crawler.Synth[SynthAux](
            tree = pas.False_(),
            aux = make_SynthAux(
                expr_types = tuple([FalseType()])
            )
        )
    
    # synthesize: expr <-- None_
    def synthesize_for_expr_None_(self, 
        inher_aux : InherAux
    ) -> crawler.Synth[SynthAux]:
        return crawler.Synth[SynthAux](
            tree = pas.None_(),
            aux = make_SynthAux(
                expr_types = tuple([NoneType()])
            )
        )

    # synthesize: expr <-- Ellip
    def synthesize_for_expr_Ellip(self, 
        inher_aux : InherAux
    ) -> crawler.Synth[SynthAux]:
        return crawler.Synth[SynthAux](
            tree = pas.Ellip(),
            aux = make_SynthAux(
                expr_types = tuple([AnyType()]),
            )
        )
    
    # synthesize: expr <-- Attribute
    def synthesize_for_expr_Attribute(self, 
        inher_aux : InherAux,
        content_tree : pas.expr, 
        content_aux : SynthAux,
        name_tree : str, 
        name_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert len(content_aux.expr_types) == 1
        content_type = content_aux.expr_types[0]
        

        expr_type = None
        if isinstance(content_type, ModuleType) and not content_type.key:
            if inher_aux.global_env.get(name_tree):
                if not inher_aux.internal_path:
                    expr_type = inher_aux.local_env[name_tree].type
                else:
                    expr_type = inher_aux.global_env[name_tree].type
            else:
                expr_type = AnyType()
        else: 
            expr_type = field_type(content_type, name_tree, inher_aux)


        if not expr_type:
            expr_type = AnyType()
        return crawler.Synth[SynthAux](
            tree = pas.Attribute(content_tree, name_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([content_aux, name_aux])),
                expr_types = tuple([expr_type])
            )
        )

    # synthesize: expr <-- Subscript
    def synthesize_for_expr_Subscript(self, 
        inher_aux : InherAux,
        content_tree : pas.expr, 
        content_aux : SynthAux,
        slice_tree : pas.expr, 
        slice_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:

        assert len(content_aux.expr_types) == 1
        content_type = content_aux.expr_types[0]

        assert len(slice_aux.expr_types) == 1
        slice_type = slice_aux.expr_types[0]

        var_types : tuple[VarType, ...]= ()
        expr_types = ()

        if isinstance(content_type, TypeType):
            class_key = get_class_key(content_type.content)
            if class_key == "typing.Generic":
                if isinstance(slice_type, FixedTupleType):
                    for anno_vt in slice_type.item_types:
                        assert isinstance(anno_vt, TypeType)
                        vt = anno_vt.content
                        assert isinstance(vt, VarType)
                        var_types += (vt,) 
                else:
                    anno_vt = slice_type
                    assert isinstance(anno_vt, TypeType)
                    vt = anno_vt.content
                    assert isinstance(vt, VarType)
                    var_types += (vt,) 
            else:
                expr_types = (TypeType(from_class_key_to_type(inher_aux, class_key, slice_type)),)

        elif isinstance(content_type, TypeType):
            expr_types = tuple([AnyType()])
        else:
            method_type = field_type(content_type, "__getitem__", inher_aux)
            if isinstance(method_type, FunctionType): 
                assert args_params_compatible(
                    [slice_type], {}, 
                    method_type, inher_aux
                )

                assert method_type.return_type
                expr_types = tuple([
                    method_type.return_type
                ])
            else:
                expr_types = (AnyType(),)

        return crawler.Synth[SynthAux](
            tree = pas.Subscript(content_tree, slice_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([content_aux, slice_aux])),
                expr_types = expr_types, 
                var_types = var_types, 
            )
        )

    # synthesize: expr <-- Slice
    def synthesize_for_expr_Slice(self, 
        inher_aux : InherAux,
        lower_tree : pas.option_expr, 
        lower_aux : SynthAux,
        upper_tree : pas.option_expr, 
        upper_aux : SynthAux,
        step_tree : pas.option_expr, 
        step_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:

        return crawler.Synth[SynthAux](
            tree = pas.Slice(lower_tree, upper_tree, step_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([lower_aux, upper_aux, step_aux])),
                expr_types = tuple([SliceType(
                    start = lower_aux.expr_types[0] if lower_aux.expr_types else NoneType(),
                    stop = upper_aux.expr_types[0] if upper_aux.expr_types else NoneType(),
                    step = step_aux.expr_types[0] if step_aux.expr_types else NoneType()
                )])
            )
        )
    
    
    # synthesize: expr <-- Name
    def synthesize_for_expr_Name(self, 
        inher_aux : InherAux,
        content_tree : str, 
        content_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:

        # TODO: update to apply decorators from environment when inferring type
        id = content_tree
        prov = lookup(inher_aux, id)
        expr_type = (
            prov.type
            if prov else
            AnyType()
        )

        return crawler.Synth[SynthAux](
            tree = pas.Name(content_tree),
            aux = make_SynthAux(
                expr_types = tuple([expr_type]),
            )
        )
    
    # synthesize: expr <-- List
    def synthesize_for_expr_List(self, 
        inher_aux : InherAux,
        content_tree : pas.comma_exprs, 
        content_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:

        assert len(content_aux.expr_types) > 0

        item_type = content_aux.expr_types[0] 
        for t in content_aux.expr_types[1:]:
            item_type = unionize_types(t, item_type)

        list_type = make_ListType(
            item_type = item_type
        )
        return crawler.Synth[SynthAux](
            tree = pas.List(content_tree),
            aux = update_SynthAux(content_aux,
                expr_types = tuple([list_type]),
            )
        )
    
    # synthesize: expr <-- EmptyList
    def synthesize_for_expr_EmptyList(self, 
        inher_aux : InherAux
    ) -> crawler.Synth[SynthAux]:
        return crawler.Synth[SynthAux](
            tree = pas.EmptyList(),
            aux = make_SynthAux(
                expr_types = tuple([ListType(
                    item_type=AnyType()
                )])
            )
        )

    # synthesize: expr <-- Tuple
    def synthesize_for_expr_Tuple(self, 
        inher_aux : InherAux,
        content_tree : pas.comma_exprs, 
        content_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:

        content_types = content_aux.expr_types
        assert len(content_types) > 0
        tuple_type = make_FixedTupleType(
            item_types = content_types 
        )
        return crawler.Synth[SynthAux](
            tree = pas.Tuple(content_tree),
            aux = update_SynthAux(content_aux,
                expr_types = tuple([tuple_type]),
            )
        )
    
    # synthesize: expr <-- EmptyTuple
    def synthesize_for_expr_EmptyTuple(self, 
        inher_aux : InherAux
    ) -> crawler.Synth[SynthAux]:
        return crawler.Synth[SynthAux](
            tree = pas.EmptyTuple(),
            aux = make_SynthAux(
                expr_types = tuple([FixedTupleType(
                    item_types=()
                )])
            )
        )
    
    # synthesize: expr <-- Starred
    def synthesize_for_expr_Starred(self, 
        inher_aux : InherAux,
        content_tree : pas.expr, 
        content_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:

        assert len(content_aux.expr_types) == 1
        content_type = content_aux.expr_types[0]
        item_type = get_iterable_item_type(content_type, inher_aux)
        return crawler.Synth[SynthAux](
            tree = pas.Starred(content_tree),
            aux = update_SynthAux(content_aux)
        )

    # synthesize: module <-- FutureMod
    def synthesize_for_module_FutureMod(self, 
        inher_aux : InherAux,
        names_tree : pas.sequence_import_name, 
        names_aux : SynthAux,
        body_tree : pas.statements, 
        body_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        return crawler.Synth[SynthAux](
            tree = pas.FutureMod(names_tree, body_tree),
            aux = body_aux 
        )


    # synthesize: decorators <-- ConsDec
    def synthesize_for_decorators_ConsDec(self, 
        inher_aux : InherAux,
        head_tree : pas.expr, 
        head_aux : SynthAux,
        tail_tree : pas.decorators, 
        tail_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert len(head_aux.expr_types) == 1
        head_type = head_aux.expr_types[0]
        synth_aux = make_SynthAux(
            expr_types = tuple([head_type]) + tail_aux.expr_types
        )
        return crawler.Synth[SynthAux](
            tree = pas.ConsDec(head_tree, tail_tree),
            aux = synth_aux 
        )
    
    # synthesize: stmt <-- DecClassDef
    def synthesize_for_stmt_DecClassDef(self, 
        inher_aux : InherAux,
        decs_tree : pas.decorators, 
        decs_aux : SynthAux,
        class_def_tree : pas.ClassDef, 
        class_def_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:

        env_additions = pmap({
            name : make_Provenance(
                initialized = prov.initialized, 
                type = prov.type,
                decorator_types = decs_aux.expr_types   
            )
            for name, prov in class_def_aux.env_additions.items()
        })  
        return crawler.Synth[SynthAux](
            tree = pas.DecClassDef(decs_tree, class_def_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([decs_aux, class_def_aux])),
                env_additions = env_additions
            ) 
        )

    # synthesize: stmt <-- ReturnSomething
    def synthesize_for_stmt_ReturnSomething(self, 
        inher_aux : InherAux,
        content_tree : pas.expr, 
        content_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert len(content_aux.expr_types) == 1
        expr_type = content_aux.expr_types[0]

        return crawler.Synth[SynthAux](
            tree = pas.ReturnSomething(content_tree),
            aux = make_SynthAux(
                return_types = tuple([expr_type])
            )
        )
    
    # synthesize: stmt <-- Return
    def synthesize_for_stmt_Return(self, 
        inher_aux : InherAux
    ) -> crawler.Synth[SynthAux]:
        return crawler.Synth[SynthAux](
            tree = pas.Return(),
            aux = make_SynthAux(
                return_types = tuple([NoneType()])
            )
        )
    
    # traverse: ClassDef
    def traverse_ClassDef_body(self,
        inher_aux : InherAux,
        name_tree : str, 
        name_aux : SynthAux,
        bs_tree : pas.bases, 
        bs_aux : SynthAux
    ) -> InherAux:
        return copy_env(inher_aux, name_tree)
    
    # synthesize: ClassDef
    def synthesize_for_ClassDef(self, 
        inher_aux : InherAux,
        name_tree : str, 
        name_aux : SynthAux,
        bs_tree : pas.bases, 
        bs_aux : SynthAux,
        body_tree : pas.statements, 
        body_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:

        # check semantics of body
        check_forward_references(inher_aux, body_aux, body_tree)

        type_params : tuple[VarType, ...] = bs_aux.var_types

        super_types : tuple[type, ...] = bs_aux.expr_types
        assert inher_aux.internal_path.endswith(name_tree)

        class_key = f"{inher_aux.external_path}.{inher_aux.internal_path}"

        def expose_static_method_type(name : str, p : Provenance) -> type:
            if not isinstance(p.type, FunctionType):
                return p.type

            for dt in p.decorator_types:
                if isinstance(dt, TypeType):
                    dt_class_key = get_class_key(dt.content)
                    if dt_class_key == "builtins.staticmethod":
                        return p.type
                    elif dt_class_key == "builtins.classmethod":
                        return update_FunctionType(p.type,
                            pos_kw_param_sigs=p.type.pos_kw_param_sigs[1:]
                        )


            if name == "__init__": 
                # first param is for newly constructed self
                assert len(p.type.pos_kw_param_sigs) > 0
                return update_FunctionType(p.type,
                    pos_kw_param_sigs=p.type.pos_kw_param_sigs[1:]
                )

            elif len(p.type.pos_kw_param_sigs) == 0:
                return p.type 
            else:

                # check if type has been partially resolved in previous iteration of analysis
                type_arg = (
                    TypeType(type_params[0])
                    if len(type_params) == 1 else 
                    FixedTupleType(tuple(TypeType(t) for t in type_params))
                    if len(type_params) > 1 else
                    None
                ) 
                self_instance_type = from_class_key_to_type(inher_aux, class_key, type_arg)

                self_instance_param_sig = update_ParamSig(p.type.pos_kw_param_sigs[0], type = self_instance_type)

                return update_FunctionType(p.type,
                    pos_kw_param_sigs=tuple([self_instance_param_sig]) + p.type.pos_kw_param_sigs[1:]
                )

        def expose_instance_method_type(p : Provenance) -> Optional[type]:
            if not isinstance(p.type, FunctionType):
                return None 

            for dt in p.decorator_types:
                if isinstance(dt, TypeType):
                    dt_class_key = get_class_key(dt.content)
                    if dt_class_key == "builtins.staticmethod":
                        return None 
                    elif dt_class_key == "builtins.classmethod":
                        return None

            if len(p.type.pos_kw_param_sigs) == 0:
                return None 
            else :
                return update_FunctionType(p.type,
                    pos_kw_param_sigs=p.type.pos_kw_param_sigs[1:]
                )


        static_fields : PMap[str, type] = pmap({
            name : expose_static_method_type(name, p)
            for name, p in body_aux.env_additions.items()
        })

        instance_fields : PMap[str, type] = pmap({
            k : t 
            for k, p in body_aux.env_additions.items()
            for t in [expose_instance_method_type(p)]
            if t 
        })


        # TODO: check that covariant type params are only used as outputs
        # TODO: check that contravariant type params are only used as inputs
        

        class_record = ClassRecord(
            key = class_key,
            type_params = type_params,
            super_types = super_types, # tuple[ClassType, ...]

            static_fields = static_fields, #, PMap[str, type]
            instance_fields = instance_fields # PMap[str, type]
        )

        instance_type = from_static_path_to_type(inher_aux, class_record.key)
        return crawler.Synth[SynthAux](
            tree = pas.ClassDef(name_tree, bs_tree, body_tree),
            aux = make_SynthAux(
                env_subtractions=s(),
                env_additions=pmap({
                    name_tree : make_Provenance(
                        initialized=True, 
                        type=TypeType(instance_type)
                    )
                }),
                class_additions=pmap({inher_aux.internal_path : class_record}) + body_aux.class_additions
            ) 
        )

    # synthesize: stmt <-- DecFunctionDef
    def synthesize_for_stmt_DecFunctionDef(self, 
        inher_aux : InherAux,
        decs_tree : pas.decorators, 
        decs_aux : SynthAux,
        fun_def_tree : pas.function_def, 
        fun_def_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:

        env_additions = pmap({
            name : make_Provenance(
                initialized = prov.initialized, 
                type = prov.type,
                decorator_types = decs_aux.expr_types   
            )
            for name, prov in fun_def_aux.env_additions.items()
        })  
        return crawler.Synth[SynthAux](
            tree = pas.DecFunctionDef(decs_tree, fun_def_tree),
            aux = make_SynthAux(
                env_additions = env_additions
            ) 
        )

    # traverse: function_def <-- FunctionDef
    def traverse_function_def_FunctionDef_body(self, 
        inher_aux : InherAux,
        name_tree : str, 
        name_aux : SynthAux,
        params_tree : pas.parameters, 
        params_aux : SynthAux,
        ret_anno_tree : pas.return_annotation, 
        ret_anno_aux : SynthAux
    ) -> InherAux:
        assert len(params_aux.env_subtractions) == 0
        inher_aux = shift_env(inher_aux, name_tree)
        return update_InherAux(inher_aux, local_env = inher_aux.local_env + params_aux.env_additions) 

    # traverse: function_def <-- AsyncFunctionDef
    def traverse_function_def_AsyncFunctionDef_body(self, 
        inher_aux : InherAux,
        name_tree : str, 
        name_aux : SynthAux,
        params_tree : pas.parameters, 
        params_aux : SynthAux,
        ret_anno_tree : pas.return_annotation, 
        ret_anno_aux : SynthAux
    ) -> InherAux:
        assert len(params_aux.env_subtractions) == 0
        inher_aux = shift_env(inher_aux, name_tree)
        return update_InherAux(inher_aux, local_env = inher_aux.local_env + params_aux.env_additions) 

    

    
    # synthesize: function_def <-- FunctionDef
    def synthesize_for_function_def_FunctionDef(self, 
        inher_aux : InherAux,
        name_tree : str, 
        name_aux : SynthAux,
        params_tree : pas.parameters, 
        params_aux : SynthAux,
        ret_anno_tree : pas.return_annotation, 
        ret_anno_aux : SynthAux,
        body_tree : pas.statements, 
        body_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:

        # check semantics of body
        check_forward_references(inher_aux, body_aux, body_tree)

        function_body_return_type = (
            GeneratorType(
                yield_type = unionize_all_types(body_aux.yield_types),
                return_type = (
                    unionize_all_types(body_aux.yield_types)
                    if len(body_aux.return_types) > 0 else
                    NoneType()
                )
            )
            if len(body_aux.yield_types) > 0 else
            unionize_all_types(body_aux.return_types)
            if len(body_aux.return_types) > 0 else
            NoneType()
        )

        if isinstance(ret_anno_tree, pas.SomeReturnAnno): 
            function_sig_return_type = (
                coerce_to_TypeType(ret_anno_aux.expr_types[0]).content
                if len(ret_anno_aux.expr_types) == 1 else
                AnyType()
            )
            assert subsumes(function_body_return_type, function_sig_return_type, inher_aux)
            function_return_type = function_sig_return_type
        else:
            function_return_type = function_body_return_type

        type = FunctionType(
            pos_param_types = params_aux.pos_param_types,
            pos_kw_param_sigs = params_aux.pos_kw_param_sigs,
            splat_pos_param_type = params_aux.splat_pos_param_type,
            kw_param_sigs = params_aux.kw_param_sigs,
            splat_kw_param_type = params_aux.splat_kw_param_type,
            return_type = function_return_type 
        )

        return crawler.Synth[SynthAux](
            tree = pas.FunctionDef(name_tree, params_tree, ret_anno_tree, body_tree),
            aux = make_SynthAux(
                env_subtractions = s(),
                env_additions = pmap({name_tree : make_Provenance(initialized = True, type = type)})
            )
        )

    # synthesize: function_def <-- AsyncFunctionDef
    def synthesize_for_function_def_AsyncFunctionDef(self, 
        inher_aux : InherAux,
        name_tree : str, 
        name_aux : SynthAux,
        params_tree : pas.parameters, 
        params_aux : SynthAux,
        ret_anno_tree : pas.return_annotation, 
        ret_anno_aux : SynthAux,
        body_tree : pas.statements, 
        body_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        # TODO: follow FunctionDef but return a CoroutineType 
        return crawler.Synth[SynthAux](
            tree = pas.AsyncFunctionDef(name_tree, params_tree, ret_anno_tree, body_tree),
            aux = make_SynthAux(
                env_subtractions = s(),
                env_additions = pmap({name_tree : make_Provenance(initialized=True)})
            ) 
        )

    # synthesize: Param 
    def synthesize_for_Param(self, 
        inher_aux : InherAux,
        name_tree : str, 
        name_aux : SynthAux,
        anno_tree : pas.param_annotation, 
        anno_aux : SynthAux,
        default_tree : pas.param_default, 
        default_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:

        sig_type = (
            coerce_to_TypeType(anno_aux.expr_types[0]).content
            if len(anno_aux.expr_types) == 1 else 
            AnyType()
        )
        if len(default_aux.expr_types) > 0:
            default_type = default_aux.expr_types[0]
            assert subsumes(default_type, sig_type, inher_aux)

        return crawler.Synth[SynthAux](
            tree = pas.Param(name_tree, anno_tree, default_tree),

            aux = make_SynthAux(
                env_additions = pmap({name_tree : make_Provenance(initialized=True, type=sig_type)}),

                param_sig = ParamSig(
                    key = name_tree, 
                    type = sig_type,
                    optional = isinstance(default_tree, SomeParamDefault)  
                )
            )
        )

    
    # synthesize: parameters_d <-- ConsKwParam
    def synthesize_for_parameters_d_ConsKwParam(self, 
        inher_aux : InherAux,
        head_tree : pas.Param, 
        head_aux : SynthAux,
        tail_tree : pas.parameters_d, 
        tail_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert head_aux.param_sig
        return crawler.Synth[SynthAux](
            tree = pas.ConsKwParam(head_tree, tail_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([head_aux, tail_aux])),
                kw_param_sigs = tuple([head_aux.param_sig]) + tail_aux.kw_param_sigs
            )
        )
    
    # synthesize: parameters_d <-- SingleKwParam
    def synthesize_for_parameters_d_SingleKwParam(self, 
        inher_aux : InherAux,
        content_tree : pas.Param, 
        content_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:

        assert content_aux.param_sig
        return crawler.Synth[SynthAux](
            tree = pas.SingleKwParam(content_tree),
            aux = update_SynthAux(content_aux,
                kw_param_sigs = tuple([content_aux.param_sig])
            )
        )
    
    # synthesize: parameters_d <-- DictionarySplatParam
    def synthesize_for_parameters_d_DictionarySplatParam(self, 
        inher_aux : InherAux,
        content_tree : pas.Param, 
        content_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert content_aux.param_sig
        return crawler.Synth[SynthAux](
            tree = pas.DictionarySplatParam(content_tree),
            aux = update_SynthAux(content_aux,
                splat_kw_param_type = content_aux.param_sig.type
            )
        )
    
    # synthesize: parameters_c <-- SingleListSplatParam
    def synthesize_for_parameters_c_SingleListSplatParam(self, 
        inher_aux : InherAux,
        content_tree : pas.Param, 
        content_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert content_aux.param_sig
        return crawler.Synth[SynthAux](
            tree = pas.SingleListSplatParam(content_tree),
            aux = update_SynthAux(content_aux,
                splat_pos_param_type = content_aux.param_sig.type
            ) 
        )
    
    # synthesize: parameters_c <-- TransListSplatParam
    def synthesize_for_parameters_c_TransListSplatParam(self, 
        inher_aux : InherAux,
        head_tree : pas.Param, 
        head_aux : SynthAux,
        tail_tree : pas.parameters_d, 
        tail_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert head_aux.param_sig
        return crawler.Synth[SynthAux](
            tree = pas.TransListSplatParam(head_tree, tail_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([head_aux, tail_aux])),
                splat_pos_param_type = head_aux.param_sig.type
            ) 
        )
    
    # synthesize: parameters_b <-- ConsPosKeyParam
    def synthesize_for_parameters_b_ConsPosKeyParam(self, 
        inher_aux : InherAux,
        head_tree : pas.Param, 
        head_aux : SynthAux,
        tail_tree : pas.parameters_b, 
        tail_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert head_aux.param_sig
        return crawler.Synth[SynthAux](
            tree = pas.ConsPosKeyParam(head_tree, tail_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([head_aux, tail_aux])),
                pos_kw_param_sigs = tuple([head_aux.param_sig]) + tail_aux.pos_kw_param_sigs
            )
        )
    
    # synthesize: parameters_b <-- SinglePosKeyParam
    def synthesize_for_parameters_b_SinglePosKeyParam(self, 
        inher_aux : InherAux,
        content_tree : pas.Param, 
        content_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert content_aux.param_sig
        return crawler.Synth[SynthAux](
            tree = pas.SinglePosKeyParam(content_tree),
            aux = update_SynthAux(content_aux,
                pos_kw_param_sigs = tuple([content_aux.param_sig])
            )
        )
    
    # synthesize: parameters_a <-- ConsPosParam
    def synthesize_for_parameters_a_ConsPosParam(self, 
        inher_aux : InherAux,
        head_tree : pas.Param, 
        head_aux : SynthAux,
        tail_tree : pas.parameters_a, 
        tail_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert head_aux.param_sig
        return crawler.Synth[SynthAux](
            tree = pas.ConsPosParam(head_tree, tail_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([head_aux, tail_aux])),
                pos_param_types = tuple([head_aux.param_sig.type]) + tail_aux.pos_param_types
            )
        )
    
    # synthesize: parameters_a <-- SinglePosParam
    def synthesize_for_parameters_a_SinglePosParam(self, 
        inher_aux : InherAux,
        content_tree : pas.Param, 
        content_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert content_aux.param_sig
        return crawler.Synth[SynthAux](
            tree = pas.SinglePosParam(content_tree),
            aux = update_SynthAux(content_aux,
                pos_param_types = tuple([content_aux.param_sig.type])
            )
        )
    
    # synthesize: parameters_a <-- TransPosParam
    def synthesize_for_parameters_a_TransPosParam(self, 
        inher_aux : InherAux,
        head_tree : pas.Param, 
        head_aux : SynthAux,
        tail_tree : pas.parameters_b, 
        tail_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert head_aux.param_sig
        return crawler.Synth[SynthAux](
            tree = pas.TransPosParam(head_tree, tail_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([head_aux, tail_aux])),
                pos_param_types = tuple([head_aux.param_sig.type]) + tail_aux.pos_param_types
            )
        )
    
    # stmt <-- Delete 
    def synthesize_for_stmt_Delete(self, 
        inher_aux : InherAux,
        targets_tree : pas.comma_exprs, 
        targets_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        return crawler.Synth[SynthAux](
            tree = pas.Delete(targets_tree),
            aux = make_SynthAux(
                env_subtractions = targets_aux.names
            ) 
        )
    # stmt <-- Assign
    def synthesize_for_stmt_Assign(self, 
        inher_aux : InherAux,
        targets_tree : pas.target_exprs, 
        targets_aux : SynthAux,
        content_tree : pas.expr, 
        content_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:

        # TODO: if source is of AnnoType(VarType), check that target symbol matches VarType's symbol

        # check name compatability between target and source expressions 
        for name in content_aux.names:

            assert (
                not (name in targets_aux.names) or (
                    name in inher_aux.local_env
                )
            )

        def patterns() -> Iterator[pas.expr]:
            tail = targets_tree
            while isinstance(tail, pas.ConsTargetExpr):
                yield tail.head
                tail = tail.tail

            assert isinstance(tail, pas.SingleTargetExpr)
            yield tail.content

        assert len(content_aux.expr_types) == 1
        content_type = content_aux.expr_types[0]
        env_types : PMap[str, type] = m()
        for pattern in patterns():
            next_env_types = unify(pattern, content_type, inher_aux)
            env_types += next_env_types 

        return crawler.Synth[SynthAux](
            tree = pas.Assign(targets_tree, content_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([targets_aux, content_aux])),
                env_additions = pmap({
                    k : make_Provenance(initialized=True, type=t)
                    for k, t in env_types.items()
                })
            ) 
        )
    
    # stmt <-- AugAssign
    def synthesize_for_stmt_AugAssign(self, 
        inher_aux : InherAux,
        target_tree : pas.expr, 
        target_aux : SynthAux,
        rator_tree : pas.bin_rator, 
        rator_aux : SynthAux,
        content_tree : pas.expr, 
        content_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert len(target_aux.expr_types) == 1
        target_type = target_aux.expr_types[0]
        assert len(content_aux.expr_types) == 1
        content_type = content_aux.expr_types[0]

        content_type = content_aux.expr_types[0]
        method_name = pas.from_bin_rator_to_aug_method_name(rator_tree)
        method_type = field_type(target_type, method_name, inher_aux)

        if isinstance(method_type, FunctionType):
            assert args_params_compatible(
                [content_type], {}, 
                method_type, inher_aux
            )

            assert subsumes(method_type, target_type, inher_aux)

        if isinstance(target_tree, pas.Name):
            symbol = target_tree.content
            assert symbol in inher_aux.local_env
        else:
            assert (
                isinstance(target_tree, pas.Subscript) or
                isinstance(target_tree, pas.Attribute) 
            )

        return crawler.Synth[SynthAux](
            tree = pas.AugAssign(target_tree, rator_tree, content_tree),
            aux = self.synthesize_auxes(tuple([target_aux, rator_aux, content_aux]))
        )


    # stmt <-- AnnoAssign
    def synthesize_for_stmt_AnnoAssign(self, 
        inher_aux : InherAux,
        target_tree : pas.expr, 
        target_aux : SynthAux,
        anno_tree : pas.expr, 
        anno_aux : SynthAux,
        content_tree : pas.expr, 
        content_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:

        assert len(content_aux.expr_types) == 1
        content_type = content_aux.expr_types[0]
        sig_type = coerce_to_TypeType(anno_aux.expr_types[0]).content
        assert isinstance(target_tree, pas.Name)
        symbol = target_tree.content

        subsumes(content_type, sig_type, inher_aux)

        return crawler.Synth[SynthAux](
            tree = pas.AnnoAssign(target_tree, anno_tree, content_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([target_aux, anno_aux, content_aux])),
                env_additions = pmap({
                    symbol : make_Provenance(initialized=True, type=sig_type)
                })
            ) 
        )

    # stmt <-- AnnoDeclar
    def synthesize_for_stmt_AnnoDeclar(self, 
        inher_aux : InherAux,
        target_tree : pas.expr, 
        target_aux : SynthAux,
        anno_tree : pas.expr, 
        anno_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert len(anno_aux.expr_types) > 0
        sig_type = coerce_to_TypeType( anno_aux.expr_types[0]).content
        assert isinstance(target_tree, pas.Name)
        symbol = target_tree.content

        return crawler.Synth[SynthAux](
            tree = pas.AnnoDeclar(target_tree, anno_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([target_aux, anno_aux])),
                env_additions = pmap({
                    symbol : make_Provenance(initialized=False, type=sig_type)
                })
            ) 
        )

    # traverse: stmt <-- For
    def traverse_stmt_For_body(self, 
        inher_aux : InherAux,
        target_tree : pas.expr, 
        target_aux : SynthAux,
        iter_tree : pas.expr, 
        iter_aux : SynthAux
    ) -> InherAux:
        assert len(iter_aux.expr_types) == 1
        iter_type = iter_aux.expr_types[0]
        return update_InherAux(inher_aux, local_env = (
            inher_aux.local_env + 
            iter_aux.env_additions +
            pmap({
                k : make_Provenance(initialized=True, type=t)
                for k, t in unify_iteration(inher_aux, target_tree, iter_type).items()
            })
        )) 

    

    # synthesize: stmt <-- For
    def synthesize_for_stmt_For(self, 
        inher_aux : InherAux,
        target_tree : pas.expr, 
        target_aux : SynthAux,
        iter_tree : pas.expr, 
        iter_aux : SynthAux,
        body_tree : pas.statements, 
        body_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:

        assert len(iter_aux.expr_types) == 1
        iter_type = iter_aux.expr_types[0]

        new_synth_aux = self.synthesize_auxes(tuple([iter_aux, body_aux]))
        return crawler.Synth[SynthAux](
            tree = pas.For(target_tree, iter_tree, body_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([target_aux, iter_aux])),
                env_subtractions = new_synth_aux.env_subtractions, 
                env_additions= (
                    new_synth_aux.env_additions +
                    pmap({
                        k : make_Provenance(initialized=True, type=t)
                        for k, t in unify_iteration(inher_aux, target_tree, iter_type).items()
                    })
                )
            )
        )

    # traverse: stmt <-- ForElse
    def traverse_stmt_ForElse_body(self, 
        inher_aux : InherAux,
        target_tree : pas.expr, 
        target_aux : SynthAux,
        iter_tree : pas.expr, 
        iter_aux : SynthAux
    ) -> InherAux:
        assert len(iter_aux.expr_types) == 1
        iter_type = iter_aux.expr_types[0]
        return update_InherAux(inher_aux, local_env = (
            inher_aux.local_env + 
            iter_aux.env_additions +
            pmap({
                k : make_Provenance(initialized=True, type=t)
                for k, t in unify_iteration(inher_aux, target_tree, iter_type).items()
            })
        )) 
    
    # synthesize: stmt <-- ForElse
    def synthesize_for_stmt_ForElse(self, 
        inher_aux : InherAux,
        target_tree : pas.expr, 
        target_aux : SynthAux,
        iter_tree : pas.expr, 
        iter_aux : SynthAux,
        body_tree : pas.statements, 
        body_aux : SynthAux,
        orelse_tree : pas.ElseBlock, 
        orelse_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert len(iter_aux.expr_types) == 1
        iter_type = iter_aux.expr_types[0]
        cross_joined_aux : SynthAux = cross_join_aux(body_aux, orelse_aux)

        new_synth_aux = self.synthesize_auxes(tuple([iter_aux, cross_joined_aux]))

        return crawler.Synth[SynthAux](
            tree = pas.ForElse(target_tree, iter_tree, body_tree, orelse_tree),
            aux = make_SynthAux(
                env_subtractions = new_synth_aux.env_subtractions, 
                env_additions = (
                    new_synth_aux.env_additions +
                    pmap({
                        k : make_Provenance(initialized=True, type=t)
                        for k, t in unify_iteration(inher_aux, target_tree, iter_type).items()
                    })
                )
            )
        )



    # traverse: stmt <-- AsyncFor
    def traverse_stmt_AsyncFor_body(self, 
        inher_aux : InherAux,
        target_tree : pas.expr, 
        target_aux : SynthAux,
        iter_tree : pas.expr, 
        iter_aux : SynthAux
    ) -> InherAux:
        return self.traverse_stmt_For_body(
            inher_aux,
            target_tree, 
            target_aux,
            iter_tree, 
            iter_aux
        ) 
    
    # synthesize: stmt <-- AsyncFor
    def synthesize_for_stmt_AsyncFor(self, 
        inher_aux : InherAux,
        target_tree : pas.expr, 
        target_aux : SynthAux,
        iter_tree : pas.expr, 
        iter_aux : SynthAux,
        body_tree : pas.statements, 
        body_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert len(iter_aux.expr_types) == 1
        iter_type = iter_aux.expr_types[0]
        new_synth_aux = self.synthesize_auxes(tuple([iter_aux, body_aux]))
        return crawler.Synth[SynthAux](
            tree = pas.AsyncFor(target_tree, iter_tree, body_tree),
            aux = make_SynthAux(
                env_subtractions = new_synth_aux.env_subtractions, 
                env_additions= (
                    new_synth_aux.env_additions +
                    pmap({
                        k : make_Provenance(initialized=True, type=t)
                        for k, t in unify_iteration(inher_aux, target_tree, iter_type).items()
                    })
                )
            )
        )

    # traverse: stmt <-- AsyncForElse
    def traverse_stmt_AsyncForElse_body(self, 
        inher_aux : InherAux,
        target_tree : pas.expr, 
        target_aux : SynthAux,
        iter_tree : pas.expr, 
        iter_aux : SynthAux
    ) -> InherAux:
        return self.traverse_stmt_ForElse_body(
            inher_aux, 
            target_tree, target_aux, 
            iter_tree, iter_aux
        )
    
    # synthesize: stmt <-- AsyncForElse
    def synthesize_for_stmt_AsyncForElse(self, 
        inher_aux : InherAux,
        target_tree : pas.expr, 
        target_aux : SynthAux,
        iter_tree : pas.expr, 
        iter_aux : SynthAux,
        body_tree : pas.statements, 
        body_aux : SynthAux,
        orelse_tree : pas.ElseBlock, 
        orelse_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert len(iter_aux.expr_types) == 1
        iter_type = iter_aux.expr_types[0]
        cross_joined_aux : SynthAux = cross_join_aux(body_aux, orelse_aux)
        new_synth_aux = self.synthesize_auxes(tuple([iter_aux, cross_joined_aux]))
        return crawler.Synth[SynthAux](
            tree = pas.AsyncForElse(target_tree, iter_tree, body_tree, orelse_tree),
            aux = make_SynthAux(
                env_subtractions = new_synth_aux.env_subtractions, 
                env_additions= (
                    new_synth_aux.env_additions +
                    pmap({
                        k : make_Provenance(initialized=True, type=t)
                        for k, t in unify_iteration(inher_aux, target_tree, iter_type).items()
                    })
                )
            )
        )

    # synthesize: import_name <-- ImportNameAlias
    def synthesize_for_import_name_ImportNameAlias(self, 
        inher_aux : InherAux,
        name_tree : str, 
        name_aux : SynthAux,
        alias_tree : str, 
        alias_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        return crawler.Synth[SynthAux](
            tree = pas.ImportNameAlias(name_tree, alias_tree),
            aux = make_SynthAux(
                import_names=pmap({alias_tree : name_tree})
            )
        )
    

    # synthesize: import_name <-- ImportNameOnly
    def synthesize_for_import_name_ImportNameOnly(self, 
        inher_aux : InherAux,
        name_tree : str, 
        name_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:

        return crawler.Synth[SynthAux](
            tree = pas.ImportNameOnly(name_tree),
            aux = make_SynthAux(
                import_names=pmap({name_tree : name_tree})
            )
        )


    # synthesize: stmt <-- Import
    def synthesize_for_stmt_Import(self, 
        inher_aux : InherAux,
        names_tree : pas.sequence_import_name, 
        names_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:

        env_additions : PMap[str, Provenance] = pmap({
            alias : make_Provenance(initialized=True, type=from_static_path_to_type(inher_aux, source_path))
            for alias, source_path in names_aux.import_names.items()
        })

        return crawler.Synth[SynthAux](
            tree = pas.Import(names_tree),
            aux = make_SynthAux(
                env_additions=env_additions
            ) 
        )

    # synthesize: stmt <-- ImportFrom 
    def synthesize_for_stmt_ImportFrom(self, 
        inher_aux : InherAux,
        module_tree : str, 
        module_aux : SynthAux,
        names_tree : pas.sequence_import_name, 
        names_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:

        env_additions : PMap[str, Provenance] = pmap({
            alias : make_Provenance(initialized=True, type=from_static_path_to_type(inher_aux, f'{module_tree}.{source_path}'))
            for alias, source_path in names_aux.import_names.items()
        })

        return crawler.Synth[SynthAux](
            tree = pas.ImportFrom(module_tree, names_tree),
            aux = make_SynthAux(
                env_additions=env_additions
            ) 
        )

    # synthesize: sequence_name <-- SingleId 
    def synthesize_for_sequence_name_SingleId(self, 
        inher_aux : InherAux,
        content_tree : str, 
        content_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        return crawler.Synth[SynthAux](
            tree = pas.SingleId(content_tree),
            aux = content_aux
        )
    

    # synthesize: stmt <-- Global 
    def synthesize_for_stmt_Global(self, 
        inher_aux : InherAux,
        names_tree : pas.sequence_name, 
        names_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        env_additions : PMap[str, Provenance] = m()
        for name in names_aux.names:
            # TODO: don't do assertion here. global name might be a forward reference. must wait until end of module to make assertion
            # Make the following assertion at the top module level to capture forward references: assert name in inher_aux.global_env
            env_additions = env_additions.set(name, inher_aux.global_env[name] if inher_aux.global_env.get(name) else make_Provenance(False))
        
        return crawler.Synth[SynthAux](
            tree = pas.Global(names_tree),
            aux = make_SynthAux(env_additions=env_additions)
        )

    # synthesize: stmt <-- Nonlocal 
    def synthesize_for_stmt_Nonlocal(self, 
        inher_aux : InherAux,
        names_tree : pas.sequence_name, 
        names_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        assert names_aux

        env_additions : PMap[str, Provenance] = m()
        for name in names_aux.names:
            env_additions = env_additions.set(name, inher_aux.nonlocal_env[name])
        
        return crawler.Synth[SynthAux](
            tree = pas.Nonlocal(names_tree),
            aux = make_SynthAux(env_additions=env_additions)
        )


    
    # synthesize: stmt <-- While
    def synthesize_for_stmt_While(self, 
        inher_aux : InherAux,
        test_tree : pas.expr, 
        test_aux : SynthAux,
        body_tree : pas.statements, 
        body_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        return crawler.Synth[SynthAux](
            tree = pas.While(test_tree, body_tree),
            aux = make_SynthAux(env_additions=test_aux.env_additions)
        )
    
    # traverse: stmt <-- WhileElse
    def traverse_stmt_WhileElse_orelse(self, 
        inher_aux : InherAux,
        test_tree : pas.expr, 
        test_aux : SynthAux,
        body_tree : pas.statements, 
        body_aux : SynthAux
    ) -> InherAux:
        return traverse_aux(inher_aux, test_aux) 
    

    # synthesize: stmt <-- WhileElse
    def synthesize_for_stmt_WhileElse(self, 
        inher_aux : InherAux,
        test_tree : pas.expr, 
        test_aux : SynthAux,
        body_tree : pas.statements, 
        body_aux : SynthAux,
        orelse_tree : pas.ElseBlock, 
        orelse_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        return crawler.Synth[SynthAux](
            tree = pas.WhileElse(test_tree, body_tree, orelse_tree),
            aux = make_SynthAux(env_additions = test_aux.env_additions)
        )

    # traverse: stmt <-- If
    def traverse_stmt_If_orelse(self, 
        inher_aux : InherAux,
        test_tree : pas.expr, 
        test_aux : SynthAux,
        body_tree : pas.statements, 
        body_aux : SynthAux
    ) -> InherAux:
        return traverse_aux(inher_aux, test_aux) 
    
    # synthesize: stmt <-- If 
    def synthesize_for_stmt_If(self, 
        inher_aux : InherAux,
        test_tree : pas.expr, 
        test_aux : SynthAux,
        body_tree : pas.statements, 
        body_aux : SynthAux,
        orelse_tree : pas.conditions, 
        orelse_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:

        joined_aux : SynthAux = cross_join_aux(body_aux, orelse_aux)
        new_synth_aux = self.synthesize_auxes(tuple([test_aux, joined_aux]))
        

        return crawler.Synth[SynthAux](
            tree = pas.If(test_tree, body_tree, orelse_tree),
            aux = update_SynthAux(new_synth_aux,
                return_types = body_aux.return_types + orelse_aux.return_types,
                yield_types = body_aux.yield_types + orelse_aux.yield_types
            )
        )

    # synthesize: conditions <-- ElifCond
    def synthesize_for_conditions_ElifCond(self, 
        inher_aux : InherAux,
        content_tree : pas.ElifBlock, 
        content_aux : SynthAux,
        tail_tree : pas.conditions, 
        tail_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        return crawler.Synth[SynthAux](
            tree = pas.ElifCond(content_tree, tail_tree),
            aux = update_SynthAux(cross_join_aux(content_aux, tail_aux),
                return_types = content_aux.return_types + tail_aux.return_types,
                yield_types = content_aux.yield_types + tail_aux.yield_types
            )
        )
    
    # synthesize: ElifBlock
    def synthesize_for_ElifBlock(self, 
        inher_aux : InherAux,
        test_tree : pas.expr, 
        test_aux : SynthAux,
        body_tree : pas.statements, 
        body_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        return crawler.Synth[SynthAux](
            tree = pas.ElifBlock(test_tree, body_tree), 
            aux = make_SynthAux(
                return_types = body_aux.return_types, 
                yield_types = body_aux.yield_types, 
            )
        )
    
    # synthesize: except_arg <-- SomeExceptArgName
    def synthesize_for_except_arg_SomeExceptArgName(self, 
        inher_aux : InherAux,
        content_tree : pas.expr, 
        content_aux : SynthAux,
        name_tree : str, 
        name_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:

        name_aux = make_SynthAux(env_additions = pmap({name_tree : make_Provenance(initialized=False)}))

        return crawler.Synth[SynthAux](
            tree = pas.SomeExceptArgName(content_tree, name_tree),
            aux = make_SynthAux(
                env_additions = (
                    content_aux.env_additions + 
                    name_aux.env_additions
                )
            )
        )
        
    
    # synthesize: with_item <-- WithItemAlias
    def synthesize_for_with_item_WithItemAlias(self, 
        inher_aux : InherAux,
        content_tree : pas.expr, 
        content_aux : SynthAux,
        alias_tree : pas.expr, 
        alias_aux : SynthAux
    ) -> crawler.Synth[SynthAux]:
        # check name compatability between target and source expressions 
        for name in content_aux.names:
            assert (
                not (name in alias_aux.names) or (
                    name in inher_aux.local_env
                )

            )

        assert len(content_aux.expr_types) == 1
        content_type = content_aux.expr_types[0]
        return crawler.Synth[SynthAux](
            tree = pas.WithItemAlias(content_tree, alias_tree),
            aux = make_SynthAux(
                env_additions = (
                    content_aux.env_additions +
                    pmap({
                        k : make_Provenance(initialized=True, type = t)
                        for k, t in unify(alias_tree, content_type, inher_aux).items() 
                    })
                )
                
            )
        )