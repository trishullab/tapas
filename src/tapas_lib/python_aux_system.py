from __future__ import annotations
from asyncio import constants

from typing import Sequence
from dataclasses import dataclass
from ftplib import all_errors
from typing import Callable, Iterator, Iterable, Mapping
from pkg_resources import compatible_platforms

from ast import literal_eval 

from pyrsistent import pmap, m, pset, s, PMap, PSet

from queue import Queue
import os
import pickle

from importlib import resources

from regex import P

from tapas_base.line_format_construct_autogen import InLine, NewLine, IndentLine
from tapas_base.abstract_token_construct_autogen import abstract_token, Vocab, Grammar
from tapas_base import abstract_token_system as ats
from tapas_base import util_system as us
from tapas_base.util_system import iom 

from tapas_lib import python_generic_tree_system as pgs 
from tapas_lib import python_ast_system as pas
from tapas_lib import python_abstract_token_system as pats 

from tapas_lib import python_aux_crawl_stream_autogen as paa
from tapas_lib.python_ast_construct_autogen import ParametersHandlers, match_parameters
from tapas_lib.python_aux_construct_autogen import *

from tapas_lib import python_ast_parse as pap
from tapas_lib import python_aux_construct_def as paux_def

from tapas_lib.python_aux_construct_autogen import type

T = TypeVar('T')



aux_vocab : PSet[str] = pset({
    c.name
    for _, cs in paux_def.choices.items()
    for c in cs
})


all_checks : PSet[semantic_check] = pset({
    LookupTypeCheck(),
    ApplyArgTypeCheck(),
    ApplyRatorTypeCheck(),
    SplatKeywordArgTypeCheck(),
    ReturnTypeCheck(),
    UnifyTypeCheck(),
    AssignTypeCheck(),
    IterateTypeCheck(),
    LookupDecCheck(),
    LookupInitCheck(),
    UpdateCheck(),
    DeclareCheck(),
    BranchDeclareCheck(),
})


class InspectSymbolException(Exception): pass

def spawn_inspect_code(module_name, code : str, package : InsertOrderMap[str, ModulePackage], checks) -> tuple[Callable[[str], tuple[str, InherAux]], Callable[[], None]]:
    gnode = pgs.parse(code)
    # print(pgs.dump(gnode))
    # raise Exception()

    mod = pas.parse_from_generic_tree(gnode)
    abstract_tokens = pas.serialize(mod)
    # print(pas.dump(mod))
    # raise Exception()

    partial_tokens = [] 
    client : Client = spawn_analysis(package, module_name, checks)
    partial_code = ""
    inher_aux : InherAux = client.init
    max_len = len(abstract_tokens)

    def kill():
        class TestKill(Exception): pass
        client.kill(TestKill())


    def inspect_next_symbol(sym : str) -> tuple[str, InherAux]:
        nonlocal partial_code
        nonlocal inher_aux
        i : int = len(partial_tokens) 
        while i < max_len:
            token = abstract_tokens[i]
            inher_aux = client.next(token)
            partial_tokens.append(token)
            partial_code = pats.concretize(tuple(partial_tokens))
            if inher_aux.local_env.get(sym):
                # print('----')
                # print((partial_code))
                # print(pats.dump(tuple(partial_tokens)))
                # print('----')
                return (partial_code, inher_aux)
            i += 1
        
        if not sym:
            # print('----')
            # print(pats.dump(tuple(partial_tokens)))
            # print('----')
            return (partial_code, inher_aux)
        else:
            raise InspectSymbolException()

    return (inspect_next_symbol, kill)



def get_first_param(params : pas.parameters) -> str:
    if isinstance(params, pas.ParamsA):
        params_a = params.content
        if isinstance(params_a, pas.ConsPosParam):
            p = params_a.head
            if p: return p.name
        elif isinstance(params_a, pas.SinglePosParam): 
            p = params_a.content
            if p: return p.name
    elif isinstance(params, pas.ParamsB):
        params_b = params.content
        if isinstance(params_b, pas.ConsPosKeyParam):
            p = params_b.head
            if p: return p.name
        elif isinstance(params_b, pas.SinglePosKeyParam): 
            p = params_b.content
            if p: return p.name
    return "" 

            
        


def method_kind_from_decorators(decorator_types : Sequence[type]) -> method_kind:
    for dt in decorator_types:
        if isinstance(dt, TypeType):
            dt_class_key = get_class_key(dt.content)
            if dt_class_key == "builtins.staticmethod":
                return StaticMethod() 
            elif dt_class_key == "builtins.classmethod":
                return ClassMethod() 

    return InstanceMethod()

def declared_and_initialized(inher_aux : InherAux, name : str) -> bool:
    return (
        name in inher_aux.declared_globals or
        name in inher_aux.declared_nonlocals or
        (
            name in inher_aux.local_env and
            inher_aux.local_env[name].initialized
        ) 
    )


def get_self_param(params_tree : pas.parameters) -> pas.Param | None:
    if isinstance(params_tree, pas.ParamsA):
        ps = params_tree.content 
        if ps:
            return pas.match_parameters_a(ps, pas.ParametersAHandlers(
                case_ConsPosParam = lambda x : x.head,
                case_SinglePosParam = lambda x : x.content,
                case_TransPosParam = lambda x : x.head
            ))
        else:
            return None
    elif isinstance(params_tree, pas.ParamsB):
        ps = params_tree.content 
        if ps:
            return pas.match_parameters_b(ps, pas.ParametersBHandlers(
                case_ConsPosKeyParam = lambda x : x.head, 
                case_SinglePosKeyParam = lambda x : x.content, 
                case_ParamsC = lambda _ : None 
            ))
        else:
            return None
    else:
        return None



def is_a_stub_body(tree : pas.ast) -> bool:
    if isinstance(tree, pas.SingleStmt):
        content = tree.content
        if isinstance(content, pas.Expr):
            return isinstance(content.content, pas.Ellip)
    return False

def is_a_stub_default(tree : pas.param_default) -> bool:
    if isinstance(tree, pas.SomeParamDefault):
        return isinstance(tree.content, pas.Ellip)
    else:
        return False

def filter_usage_additions(usage_additions : PMap[str, Usage], *excludes : Iterable[str]) -> PMap[str, Usage]:
    for exc in excludes:
        for k in exc:
            if k in usage_additions:
                usage_additions = usage_additions.remove(k)
    return usage_additions


def merge_usages(a : Usage, b : Usage) -> Usage:
    return Usage(
        backref = a.backref and b.backref,
        updated = a.updated or b.updated
    )

def merge_nested_usages(xs : PMap[str, tuple[Usage, ...]], ys : PMap[str, tuple[Usage, ...]]) -> PMap[str, tuple[Usage, ...]]:
    overlaps = pmap({
        yk : x + y 
        for yk, y in ys.items()
        for xk, x in xs.items()
        if yk == xk
    })
    
    return xs + ys + overlaps 


def merge_usage_additions(xs : PMap[str, Usage], ys : PMap[str, Usage]) -> PMap[str, Usage]:

    overlaps = pmap({
        yk : merge_usages(y, x)
        for yk, y in ys.items()
        for xk, x in xs.items()
        if yk == xk
    })

    return xs + ys + overlaps 

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
    if a == b:
        return a
    elif isinstance(a, UnionType) and isinstance(b, UnionType):
        return UnionType(
            type_choices = tuple(set(a.type_choices + b.type_choices))
        )
    elif isinstance(a, UnionType):
        return UnionType(
            type_choices = tuple(set(a.type_choices + (b,)))
        )
    elif isinstance(b, UnionType):
        return UnionType(
            type_choices = tuple(set((a,) + b.type_choices))
        )
    else:
        return UnionType(
            type_choices = (a, b)
        )

def get_type_args(t : type) -> tuple[type, ...]:

    return match_type(t, TypeHandlers(
        case_ProtocolType = lambda t : (),
        case_GenericType = lambda t : (),
        case_OverloadType = lambda t : (),
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
        case_TupleLitType = lambda t : t.item_types,
        case_VariedTupleType = lambda t : (t.item_type,),
        case_NamedTupleType = lambda t : (
            tuple(AnyType() for _ in t.fields)
        ),
        case_ListLitType = lambda t : (unionize_all_types(t.item_types),),
        case_DictLitType = lambda t : (
            unionize_all_types(kt for kt, _ in t.pair_types),
            unionize_all_types(vt for _, vt in t.pair_types)
        ),
        case_TrueType = lambda t : (),
        case_FalseType = lambda t : (),
        case_IntLitType = lambda t : (),
        case_FloatLitType = lambda t : (),
        case_StrLitType = lambda t : (),
    ))


def get_class_key(t : type) -> str:
    return match_type(t, TypeHandlers(
        case_ProtocolType = lambda t : "",
        case_GenericType = lambda t : "",
        case_OverloadType = lambda t : "",
        case_TypeType = lambda t : "builtins.type",
        case_VarType = lambda t : "",
        case_EllipType = lambda t : "builtins.ellipsis",
        case_AnyType = lambda t : "",
        case_ObjectType = lambda t : "builtins.object",
        case_NoneType = lambda t : "", 
        case_ModuleType = lambda t : "",
        case_FunctionType = lambda t : "typing.Callable",
        case_UnionType = lambda t : "typing.Union",
        case_InterType = lambda t : "",
        case_RecordType = lambda t : t.class_key,
        case_TupleLitType = lambda t : "builtins.tuple",
        case_VariedTupleType = lambda t : "builtins.tuple",
        case_NamedTupleType = lambda t : "builtins.tuple", 
        case_ListLitType = lambda t : "builtins.list",
        case_DictLitType = lambda t : "builtins.dict",
        case_TrueType = lambda t : "builtins.bool",
        case_FalseType = lambda t : "builtins.bool",
        case_IntLitType = lambda t : "builtins.int",
        case_FloatLitType = lambda t : "builtins.float",
        case_StrLitType = lambda t : "builtins.str",
    ))

def coerce_to_type(t) -> type:
    assert isinstance(t, type)
    return t


def lookup_path_type(path : str, inher_aux : InherAux) -> type:
    parts = path.split(".")
    assert len(parts) > 0
    root = parts[0]
    rest = parts[1:] 
    decl = lookup_declaration(inher_aux, root)
    if decl:
        t = decl.type
        for part in rest:
            t = lookup_field_type(t, part, inher_aux)
            if not t:
                return AnyType()
        return t
    else:
        return AnyType()

def coerce_to_TypeType(t : type, inher_aux : InherAux) -> TypeType:
    if isinstance(t, AnyType):
        return TypeType(content = AnyType())
    elif isinstance(t, EllipType):
        return TypeType(content = AnyType())
    elif isinstance(t, NoneType):
        return TypeType(content = NoneType())
    elif isinstance(t, StrLitType):
        annotation : str = literal_eval(t.literal)

        type_arg_start_index = annotation.find('[')
        type_arg_end_index = annotation.find(']')

        type_arg = (TupleLitType(tuple(
            lookup_path_type(type_str.strip(), inher_aux)
            for type_str in annotation[type_arg_start_index + 1:type_arg_end_index].split(",")
        )) if type_arg_start_index > -1 else
        None)


        base_annotation = annotation[:type_arg_start_index] if type_arg_start_index > 0 else annotation
        base_type = lookup_path_type(base_annotation, inher_aux)

        if isinstance(t, AnyType):
            return TypeType(content = AnyType())
        else:
            assert isinstance(base_type, TypeType)
            class_key = get_class_key(base_type.content)
            return from_class_key_to_typetype(inher_aux, class_key, type_arg)
    else:
        assert isinstance(t, TypeType)
        return t

def coerce_to_TupleLitType(t : type) -> TupleLitType:
    assert isinstance(t, TupleLitType)
    return t

def coerce_to_ListLitType(t : type) -> ListLitType:
    assert isinstance(t, ListLitType)
    return t

def from_anno_seq_to_instance_types(ts : Iterable[type], inher_aux : InherAux) -> tuple[type, ...]:
    return tuple(
        coerce_to_TypeType(t, inher_aux).content
        for t in ts 
    ) 

def from_anno_option_to_instance_type(t : type | None, inher_aux : InherAux) -> type:
    if t:
        return coerce_to_TypeType(t, inher_aux).content
    else:
        return AnyType()

def from_anno_pair_option_to_instance_type(t : type | None, inher_aux : InherAux) -> tuple[type, type]: 
    if t:
        ftt = coerce_to_TupleLitType(t)
        ts = from_anno_seq_to_instance_types(ftt.item_types, inher_aux)
        assert len(ts) == 2
        return (ts[0], ts[1])
    else:
        return (AnyType(), AnyType()) 

def from_class_key_to_typetype(inher_aux : InherAux, class_key : str, type_arg : Optional[type] = None) -> TypeType:

    content_type = AnyType() 

    if class_key == "":
        content_type = AnyType()
    elif class_key == "builtins.ellipsis":
        assert not type_arg
        content_type = EllipType()
    elif class_key == "typing.Callable":
        assert isinstance(type_arg, TupleLitType)
        type_args = coerce_to_TupleLitType(type_arg).item_types
        assert len(type_args) == 2
        param_type_args = coerce_to_ListLitType(type_args[0]).item_types
        pos_param_types = from_anno_seq_to_instance_types(param_type_args, inher_aux)
        return_type = coerce_to_TypeType(type_arg.item_types[1], inher_aux).content
        content_type = make_FunctionType(
            pos_param_types=pos_param_types,
            return_type=return_type
        )
    elif class_key == "typing.Union":
        assert type_arg

        if isinstance(type_arg, TupleLitType):
            ts = from_anno_seq_to_instance_types(coerce_to_TupleLitType(type_arg).item_types, inher_aux)
            content_type = make_UnionType(type_choices=ts)
        else:
            t = coerce_to_TypeType(type_arg, inher_aux).content
            content_type = make_UnionType(type_choices=(t,))


    elif class_key == "builtins.tuple":
        if (
            isinstance(type_arg, TupleLitType) and
            len(type_arg.item_types) == 2 and
            isinstance(type_arg.item_types[1], EllipType)
        ):
            content_type = VariedTupleType(item_type = coerce_to_TypeType(type_arg.item_types[0], inher_aux).content)

        elif isinstance(type_arg, TupleLitType):
            item_types = from_anno_seq_to_instance_types(type_arg.item_types, inher_aux)
            content_type = TupleLitType(item_types=item_types)

        elif type_arg:
            item_types = (coerce_to_TypeType(type_arg, inher_aux).content,)
            content_type = TupleLitType(item_types=item_types)

        else:
            content_type = TupleLitType(item_types=())

    elif (
        class_key == "builtins.type" and isinstance(type_arg, TypeType)
    ):
        content_type = type_arg

    else:
        type_args : tuple[type, ...] = (
            from_anno_seq_to_instance_types(type_arg.item_types, inher_aux)  
            if isinstance(type_arg, TupleLitType) else
            (coerce_to_TypeType(type_arg, inher_aux).content,)
            if type_arg else
            tuple()
        )

        content_type = make_RecordType(
            class_key=class_key,
            type_args=type_args
        )

    return TypeType(content = content_type)


def generalize_type(inher_aux : InherAux, spec_type : type) -> type:

    t = match_type(spec_type, TypeHandlers(
        case_ProtocolType = lambda t : t,
        case_GenericType = lambda t : t,
        case_OverloadType = lambda t : t,
        case_TypeType = lambda t : t,
        case_VarType = lambda t : t,
        case_EllipType = lambda t : t,
        case_AnyType = lambda t : t,
        case_ObjectType = lambda t : t,
        case_NoneType = lambda t : t, 
        case_ModuleType = lambda t : t,
        case_FunctionType = lambda t : t,
        case_UnionType = lambda t : t,
        case_InterType = lambda t : t,
        case_RecordType = lambda t : t,
        case_TupleLitType = lambda t : t,
        case_VariedTupleType = lambda t : t,
        case_NamedTupleType = lambda t : t, 
        case_ListLitType = lambda t : (
            class_record := from_static_path_to_ClassRecord(inher_aux, "builtins.list"),
            content_type := unionize_all_types(
                generalize_type(inher_aux, it)
                for it in t.item_types
            ),
            content_type := (
                unionize_types(content_type, class_record.type_params[0])
                if class_record else
                content_type
            ),
            make_RecordType(
                class_key="builtins.list", 
                type_args=(content_type,)        
            )
        )[-1],
        case_DictLitType = lambda t : make_RecordType(
            class_key="builtins.dict", 
            type_args=(
                unionize_all_types(generalize_type(inher_aux, kt) for kt, _ in t.pair_types),
                unionize_all_types(generalize_type(inher_aux, vt) for _, vt in t.pair_types),
            )        
        ),
        case_TrueType = lambda t : make_RecordType(class_key="builtins.bool"),
        case_FalseType = lambda t : make_RecordType(class_key="builtins.bool"),
        case_IntLitType = lambda t : make_RecordType(class_key="builtins.int"),
        case_FloatLitType = lambda t : make_RecordType(class_key="builtins.float"),
        case_StrLitType = lambda t : make_RecordType(class_key="builtins.str"),
    ))
    return t


def coerce_to_VarType(t : type) -> VarType:
    assert isinstance(t, VarType)
    return t


def types_match_subsumed(sub_type : type, super_type : type, inher_aux : InherAux, fuel : int) -> bool:

    if sub_type == super_type:
        return True

    if isinstance(sub_type, TypeType) and isinstance(super_type, TypeType):
        return types_match_subsumed(sub_type.content, super_type.content, inher_aux, fuel - 1)

    if isinstance(sub_type, TypeType) and not isinstance(super_type, TypeType):
        return False

    if not isinstance(sub_type, TypeType) and isinstance(super_type, TypeType):
        return False

    if get_class_key(sub_type) != get_class_key(super_type):
        return False
    
    if isinstance(sub_type, FunctionType):
        assert isinstance(super_type, FunctionType)
        param_subsumptions = [ 
            subsumed(super_type.pos_param_types[i], t, inher_aux, fuel - 1)
            for i, t in enumerate(sub_type.pos_param_types)
        ] + [ 
            subsumed(super_type.pos_kw_param_sigs[i].type, s.type, inher_aux, fuel - 1)
            for i, s in enumerate(sub_type.pos_kw_param_sigs)
        ] + [
            subsumed(super_type.bundle_pos_param_type, sub_type.bundle_pos_param_type, inher_aux, fuel - 1)
        ] if sub_type.bundle_pos_param_type and super_type.bundle_pos_param_type else [] + [
            subsumed(super_type.kw_param_sigs[i].type, s.type, inher_aux, fuel - 1)
            for i, s in enumerate(sub_type.kw_param_sigs)
        ] + [
            subsumed(super_type.bundle_kw_param_type, sub_type.bundle_kw_param_type, inher_aux, fuel - 1)
        ] if sub_type.bundle_kw_param_type and super_type.bundle_kw_param_type else [] 

        return_subsumption = subsumed(sub_type.return_type, super_type.return_type, inher_aux, fuel - 1)
        return_subsumption = True 


        return us.every(param_subsumptions, lambda x : x) and return_subsumption

    elif isinstance(sub_type, RecordType):
        assert isinstance(super_type, RecordType)
        if sub_type.class_key != super_type.class_key:
            return False

        class_record = from_static_path_to_ClassRecord(inher_aux, sub_type.class_key)
        if class_record:
            type_params = class_record.type_params

            assert len(sub_type.type_args) <= len(type_params)
            assert len(super_type.type_args) <= len(type_params)

            def get_type_arg(t : RecordType, i : int) -> type:
                return t.type_args[i] if i < len(t.type_args) else AnyType()

            subsumptions = [
                (
                    subsumed(get_type_arg(super_type, i), get_type_arg(sub_type, i), inher_aux, fuel - 1)
                    if isinstance(tp.variant, ContraVariant) else
                    subsumed(get_type_arg(sub_type, i), get_type_arg(super_type, i), inher_aux, fuel - 1)
                    # by default type_params should be treated as covariant
                    # if isinstance(tp.variant, CoVariant) else
                    # sub_type.type_args[i] == super_type.type_args[i]
                )
                for i, tp in enumerate(type_params)
            ]

            return us.every(subsumptions, lambda x : x)
        else:
            return True

    else:
        assert get_class_key(sub_type) == get_class_key(super_type)
        sub_type_args = get_type_args(sub_type)
        super_type_args = get_type_args(super_type)
        
        m = min(len(sub_type_args), len(super_type_args))
        subsumptions = [
            subsumed(sub_type_args[i], super_type_args[i], inher_aux, fuel - 1)
            for i in range(m)
        ]

        return us.every(subsumptions, lambda x : x)
    

def field_exists_subsumed(sub_type : type, field_name : str, field_type : type, inher_aux : InherAux, fuel : int) -> bool:

    sub_field_type = lookup_field_type(sub_type, field_name, inher_aux)
    if sub_field_type:
        return subsumed(sub_field_type, field_type, inher_aux, fuel - 1)
    else:
        return False

def subsumed(sub_type : type, super_type : type, inher_aux : InherAux, fuel : int = 20) -> bool:
    if fuel <= 0 : return False

    super_type = generalize_type(inher_aux, super_type)

    return (
        not isinstance(sub_type, ModuleType) and
        (

            isinstance(sub_type, AnyType) or 
            isinstance(super_type, AnyType) or 

            # VarType behaves like AnyType if it hasn't been substituted
            isinstance(sub_type, VarType) or
            isinstance(super_type, VarType) or

            isinstance(super_type, RecordType) and super_type.class_key == "builtins.object" or

            types_match_subsumed(sub_type, super_type, inher_aux, fuel - 1) or 

            (
                # TODO: figure out more general way to handle int <: float
                isinstance(super_type, RecordType) and
                super_type.class_key == "builtins.float" and
                isinstance(sub_type, RecordType) and
                sub_type.class_key == "builtins.int"
            ) or

            ( 
                isinstance(sub_type, TypeType) and
                isinstance(super_type, TypeType) and
                subsumed(sub_type.content, super_type.content, inher_aux, fuel - 1)
            ) or 

            (isinstance(super_type, RecordType) and
                super_type.class_key == "builtins.slice"
            ) or

            # break down super type of intersection into conjunctions before sub type into disjunctions 
            (isinstance(super_type, InterType) and 
                all(subsumed(sub_type, tc, inher_aux, fuel - 1) for tc in super_type.type_components)) or

            # break down sub type of union into conjunctions before super type into disjunctions 
            (isinstance(sub_type, UnionType) and 
                all(subsumed(tc, super_type, inher_aux, fuel - 1) for tc in sub_type.type_choices)) or

            (isinstance(sub_type, InterType) and 
                any(subsumed(tc, super_type, inher_aux, fuel - 1) for tc in sub_type.type_components)) or 

            (isinstance(super_type, UnionType) and 
                any(subsumed(sub_type, tc, inher_aux, fuel - 1) for tc in super_type.type_choices)) or


            (parent_type := get_parent_type(sub_type, inher_aux),
                parent_type != None and subsumed(parent_type, super_type, inher_aux, fuel - 1))[-1] or

            (
                isinstance(super_type, RecordType) and
                (
                    cr := infer_class_record(super_type, inher_aux),
                    cr and cr.protocol and us.every(cr.instance_fields.items(), lambda p : (
                        fe := field_exists_subsumed(sub_type, p[0], p[1], inher_aux, fuel - 1),
                        fe
                    )[-1])
                )[-1]
            ) or

            
            False 


        )
    )


def instance_parent_type(t : RecordType, inher_aux : InherAux) -> type:
    class_record = from_static_path_to_ClassRecord(inher_aux, t.class_key) 
    if not class_record:   
        return ObjectType()

    assert len(t.type_args) <= len(class_record.type_params)
    subst_map : PMap[str, type] = pmap({
        var_type.name : t.type_args[i] if i < len(t.type_args) else make_AnyType()
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
        case_ProtocolType = lambda t : None,
        case_GenericType = lambda t : None,
        case_OverloadType = lambda t : None,
        case_TypeType = lambda t : ObjectType(),
        # case_TypeType = lambda t : make_RecordType(class_key="builtins.type"),
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
        case_TupleLitType = lambda t : VariedTupleType(unionize_all_types(t.item_types)),
        case_VariedTupleType = lambda t : make_RecordType(class_key = "typing.Sequence", type_args=(t.item_type,)),
        case_NamedTupleType = lambda t : (
            (TupleLitType(tuple(AnyType() for _ in t.fields)))
            if len(t.fields) > 0 else
            (VariedTupleType(AnyType()))
        ), 
        case_ListLitType = lambda t : generalize_type(inher_aux, t),
        case_DictLitType = lambda t : generalize_type(inher_aux, t),
        case_TrueType = lambda t : make_RecordType(class_key="builtins.bool"),
        case_FalseType = lambda t : make_RecordType(class_key="builtins.bool"),
        case_IntLitType = lambda t : make_RecordType(class_key="builtins.int"),
        case_FloatLitType = lambda t : make_RecordType(class_key="builtins.float"),
        case_StrLitType = lambda t : make_RecordType(class_key="builtins.str"),
    )) 

def infer_class_record(t : type, inher_aux : InherAux) -> ClassRecord | None:
    t = generalize_type(inher_aux, t)
    class_key = get_class_key(t)

    class_record = from_static_path_to_ClassRecord(inher_aux, class_key) 
    if class_record:
        type_args : tuple[type, ...] = get_type_args(t)
        subst_map = pmap({
            tp.name : (type_args[i] if i < len(type_args) else make_AnyType())
            for i, tp in enumerate(class_record.type_params) 
        })

        return update_ClassRecord(class_record,
            static_fields = iom(*(
                (k, substitute_type_args(t, subst_map)) 
                for k, t in class_record.static_fields.items()
            )), 
            instance_fields = iom(*(
                (k, substitute_type_args(t, subst_map))
                for k, t in class_record.instance_fields.items()
            ))
        )
    else:
        return None


def lookup_constructor_type(class_record : ClassRecord, inher_aux : InherAux) -> Optional[type]:
    fields = class_record.static_fields 
    constructor = fields.get('__init__') or fields.get('__new__')
    if constructor:
        return constructor
    else:
        super_class_type_unresolved = False
        for st in class_record.super_types:
            super_class_type = infer_class_record(st, inher_aux)
            if super_class_type:
                result = lookup_constructor_type(super_class_type, inher_aux)
                if result:
                    return result
            else:
                super_class_type_unresolved = True
        if super_class_type_unresolved:
            return AnyType()
        else:
            return None

def lookup_static_field_type(class_record : ClassRecord, field_name : str, inher_aux : InherAux) -> Optional[type]:
    fields = class_record.static_fields 
    result = fields.get(field_name)
    if result:
        return result
    else:
        super_class_type_unresolved = False
        for st in class_record.super_types:
            super_class_type = infer_class_record(st, inher_aux)
            if super_class_type:
                result = lookup_static_field_type(super_class_type, field_name, inher_aux)
                if result:
                    return result
            else:
                super_class_type_unresolved = True
        if super_class_type_unresolved:
            return AnyType()
        else:
            return None

            
def lookup_field_type(anchor_type : type, field_name : str, inher_aux : InherAux) -> type | None:
    if isinstance(anchor_type, AnyType):
        return AnyType()
    elif isinstance(anchor_type, VarType):
        # TODO: figure out how to handle "_typeshed.SupportsRichComparisonT"
        return AnyType()

    elif isinstance(anchor_type, ModuleType):
        assert anchor_type.key
        path = f"{anchor_type.key}.{field_name}" 
        dec = from_static_path_to_declaration(inher_aux, path)
        return dec.type

    elif isinstance(anchor_type, TypeType):
        content_class_record = infer_class_record(anchor_type.content, inher_aux)
        if content_class_record:
            return lookup_static_field_type(content_class_record, field_name, inher_aux)
        else:
            return None 

    else:
        class_record = infer_class_record(anchor_type, inher_aux)

        if class_record:

            fields = class_record.instance_fields
            result = fields.get(field_name)

            if result:
                return result 
            else:
                for super_type in class_record.super_types:
                    result = lookup_field_type(super_type.content, field_name, inher_aux)
                    if result:
                        return result
        else:
            return None




def substitute_function_type_args(t : FunctionType, subst_map : PMap[str, type]) -> FunctionType:
    return FunctionType(
        static_key=t.static_key,
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
        bundle_pos_param_type = (
            substitute_type_args(t.bundle_pos_param_type, subst_map)
            if t.bundle_pos_param_type else
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
        bundle_kw_param_type = (
            substitute_type_args(t.bundle_kw_param_type, subst_map)
            if t.bundle_kw_param_type else
            None
        ), # Optional[type]
        return_type = substitute_type_args(t.return_type, subst_map) # type
    )

def substitute_type_args(t : type, subst_map : PMap[str, type]) -> type:
    return match_type(t, TypeHandlers(
        case_ProtocolType = lambda t : t,
        case_GenericType = lambda t : t,
        case_OverloadType = lambda t : t,
        case_TypeType = lambda t : update_TypeType(t, content = substitute_type_args(t.content, subst_map)),
        # case_TypeType = lambda t : substitute_type_args(t.content, subst_map),
        case_VarType = lambda t : subst_map[t.name] if subst_map.get(t.name) else t,
        case_EllipType = lambda t : t,
        case_AnyType = lambda t : t,
        case_ObjectType = lambda t : t,
        case_NoneType = lambda t : t, 
        case_ModuleType = lambda t : t,
        case_FunctionType = lambda t : (
            substitute_function_type_args(t, subst_map)
        ),
        case_UnionType = lambda t : (

            unionize_all_types(
                substitute_type_args(type_choice, subst_map)
                for type_choice in t.type_choices
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
        case_TupleLitType = lambda t : (
            update_TupleLitType(t,
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

        case_NamedTupleType = lambda t : t,

        case_ListLitType = lambda t :( 
            ListLitType(
                item_types = tuple(
                    substitute_type_args(item_type, subst_map)
                    for item_type in t.item_types
                )
            )
        ),
        case_DictLitType = lambda t : ( 
            DictLitType(
                pair_types = tuple(
                    (substitute_type_args(kt, subst_map), substitute_type_args(vt, subst_map))
                    for kt, vt in t.pair_types
                )
            )
        ),
        case_TrueType = lambda t : t,
        case_FalseType = lambda t : t,
        case_IntLitType = lambda t : t,
        case_FloatLitType = lambda t : t,
        case_StrLitType = lambda t : t,
    ))


def from_static_path_to_ClassRecord(inher_aux : InherAux, path : str) -> ClassRecord | None:
    if path.startswith(inher_aux.external_path + "."):
        class_record = inher_aux.class_env.get(path[len(inher_aux.external_path + "."):])
        return class_record 

    sep = "."
    levels = path.split(sep)
    l = len(levels)
    package : InsertOrderMap[str, ModulePackage] = inher_aux.package

    for i, level in enumerate(levels):
        if package.get(level):

            mod_pack = package[level]

            class_env = mod_pack.class_env
            package = mod_pack.package
            if i + 1 < l: 
                remaining_path = ".".join(levels[i + 1:])
                class_record = class_env.get(remaining_path)
                if class_record: 
                    return class_record

    return None

def from_static_path_to_declaration(inher_aux : InherAux, path : str) -> Declaration:

    if path == inher_aux.external_path:
         
        return make_Declaration(
            updatable=None, initialized = True, 
            type = ModuleType(inher_aux.external_path)
        )

    elif path.startswith(inher_aux.external_path + "."):
        name = path[len(inher_aux.external_path + "."):]
        internal_decl = (
            inher_aux.local_env.get(name)
            if not inher_aux.internal_path else
            inher_aux.global_env.get(name)
        )

        if internal_decl and not isinstance(internal_decl.type, AnyType):
            return internal_decl

    sep = "."
    levels = path.split(sep)
    l = len(levels)
    package : InsertOrderMap[str, ModulePackage] = inher_aux.package

    for i, level in enumerate(levels):
        if package.get(level):

            mod_pack = package[level]

            module = mod_pack.module
            package = mod_pack.package
            if i + 2 == l and module.get(levels[i + 1]):
                module_level = levels[i + 1]
                decl = module[module_level]
                if not isinstance(decl.type, AnyType):
                    return decl
        else:
            return make_Declaration(updatable = None, initialized = True, type = AnyType())

    return make_Declaration(
        updatable = None, initialized = True,
        type = ModuleType(key = path)
    )

def lookup_declaration(inher_aux : InherAux, key : str, builtins = True) -> Declaration | None:

    if inher_aux.local_env.get(key):
        t = inher_aux.local_env[key]
        return t
    elif inher_aux.nonlocal_env.get(key):
        return inher_aux.nonlocal_env[key]
    elif inher_aux.global_env.get(key):
        return inher_aux.global_env[key]
    elif key == "Ellipsis": # don't expose the type of builtins.Ellipsis
        return make_Declaration(updatable=None, initialized = True)
    elif builtins:
        return from_static_path_to_declaration(inher_aux, f"builtins.{key}")
    else:
        return None 





def infer_subst_map(
    inher_aux : InherAux, subst_map : PMap[str, type], 
    vt : type, t : type
) -> PMap[str, type]:

    # TODO: fill out the rest of substitution cases
    # TODO: this should be merged with subsumed
    # -- into a single constraint solving/unification procedure

    def flatten_maps(maps : Sequence[PMap]):
        result = m()
        for map in maps:
            result = result.update(map) 
        return result

    return match_type(vt, TypeHandlers(
        case_ProtocolType = lambda vt : subst_map, 
        case_GenericType = lambda vt : subst_map,
        case_OverloadType = lambda vt : subst_map,
        case_TypeType = lambda vt : subst_map,
        case_VarType = lambda vt : (
            (sub := subst_map.get(vt.name), (
                subst_map.update(pmap({vt.name:t}))
                if not sub or subsumed(sub, t, inher_aux) else
                subst_map
            ))[-1]
            if isinstance(vt, VarType) else
            subst_map
        ),
        case_EllipType = lambda vt : subst_map,
        case_AnyType = lambda vt : subst_map,
        case_ObjectType = lambda vt : subst_map,
        case_NoneType = lambda vt : subst_map,
        case_ModuleType = lambda vt : subst_map,
        case_FunctionType = lambda vt : subst_map,
        case_UnionType = lambda vt : (
            subst_maps := [
                infer_subst_map(inher_aux, subst_map, tc, t) 
                for tc in vt.type_choices 
            ], 
            flatten_maps([subst_map] + subst_maps)
        )[-1],
        case_InterType = lambda vt : subst_map,
        case_RecordType = lambda vt : subst_map,
        case_TupleLitType = lambda vt : subst_map,
        case_VariedTupleType = lambda vt : subst_map,
        case_NamedTupleType = lambda t : subst_map,
        case_ListLitType = lambda vt : subst_map,
        case_DictLitType = lambda vt : subst_map,
        case_TrueType = lambda vt : subst_map,
        case_FalseType = lambda vt : subst_map,
        case_IntLitType = lambda vt : subst_map,
        case_FloatLitType = lambda vt : subst_map,
        case_StrLitType = lambda vt : subst_map,
    ))


import random
import string
def make_gen_fresh_var() -> Callable[[], str]:
    count = 0
    rando = (''.join(random.choices(string.ascii_lowercase, k=3)))
    def gen_fresh_var() -> str:
        nonlocal count
        count += 1
        return f"Alpha_T_{rando}_{count}"
    return gen_fresh_var

gen_fresh_var = make_gen_fresh_var()


def check_application_args(
    pos_arg_types : Sequence[type],
    kw_arg_types : Mapping[str, type], 
    function_type : FunctionType,
    inher_aux : InherAux 
) -> tuple[FunctionType | None, PMap[str, type]]:

    subst_map : PMap[str, type] = pmap({}) # VarType |-> arg_type

    pos_overflow = len(pos_arg_types) - len(function_type.pos_param_types)
    if pos_overflow < 0:
        return (None, subst_map)

    if (
        not function_type.bundle_pos_param_type and  
        pos_overflow > len(function_type.pos_kw_param_sigs)
    ):
        return (None, subst_map)

    if (
        not function_type.bundle_pos_param_type and 
        not function_type.bundle_kw_param_type and 
        (pos_overflow + len(kw_arg_types) > (
            len(function_type.pos_kw_param_sigs) +
            len(function_type.kw_param_sigs)
        ))
    ):

        return (None, subst_map)

    if (
        function_type.bundle_pos_param_type and
        pos_overflow > len(function_type.pos_kw_param_sigs) and
        not function_type.bundle_kw_param_type and
        len(kw_arg_types) > len(function_type.kw_param_sigs)
    ):
        return (None, subst_map)

    if (
        function_type.bundle_pos_param_type and 
        pos_overflow <= len(function_type.pos_kw_param_sigs) and
        not function_type.bundle_kw_param_type and 
        (pos_overflow + len(kw_arg_types) > (
            len(function_type.pos_kw_param_sigs) +
            len(function_type.kw_param_sigs)
        ))
    ):
        return (None, subst_map)

    checks : Iterable[bool] = [
        (
            subst_map := infer_subst_map(
                inher_aux, subst_map, param_type, 
                generalize_type(inher_aux, pos_arg_types[i])
            ),
            ss := subsumed(pos_arg_types[i], param_type, inher_aux),
            ss
        )[-1]
        for i, param_type in enumerate(function_type.pos_param_types) 
    ] + [
        (
            subst_map := infer_subst_map(
                inher_aux, subst_map, 
                param_sig.type, 
                generalize_type(inher_aux, pos_arg_types[j])
            ),
            ss := subsumed(pos_arg_types[j], param_sig.type, inher_aux),
            ss
        )[-1]
        for i, param_sig in enumerate(function_type.pos_kw_param_sigs) 
        if i < pos_overflow 
        for j in [i + len(function_type.pos_param_types)]
    ] + (
        [
            (
                subst_map := infer_subst_map(
                    inher_aux, subst_map, 
                    function_type.bundle_pos_param_type, 
                    generalize_type(inher_aux, pos_type_arg)
                ),
                ss := subsumed(pos_type_arg, function_type.bundle_pos_param_type, inher_aux),
                ss
            )[-1]
            for pos_type_arg in pos_arg_types[len(function_type.pos_param_types) + len(function_type.pos_kw_param_sigs):]
        ]
        if (function_type.bundle_pos_param_type != None and
            len(pos_arg_types) > len(function_type.pos_param_types) + len(function_type.pos_kw_param_sigs)
        ) else
        [
            param_sig.optional or
            (
                kw_arg_types.get(param_sig.key) != None and
                (
                    subst_map := infer_subst_map(
                        inher_aux, subst_map, 
                        param_sig.type, 
                        generalize_type(inher_aux, kw_arg_types[param_sig.key])
                    ),
                    ss := subsumed(kw_arg_types[param_sig.key], param_sig.type, inher_aux),
                    ss
                )[-1]
            ) 
            for i, param_sig in enumerate(function_type.pos_kw_param_sigs) 
            if i >= pos_overflow 
        ] 
    ) + [
        param_sig.optional or
        (
            kw_arg_types.get(param_sig.key) != None and
            (
                subst_map := infer_subst_map(
                    inher_aux, subst_map, param_sig.type, 
                    generalize_type(inher_aux, kw_arg_types[param_sig.key])
                ),
                ss := subsumed(kw_arg_types[param_sig.key], param_sig.type, inher_aux),
                ss
            )[-1]
        ) 
        for param_sig in function_type.kw_param_sigs 
    ] + [
        (
            subst_map := infer_subst_map(
                inher_aux, subst_map, 
                function_type.bundle_kw_param_type, 
                generalize_type(inher_aux, kw_arg_type)
            ),
            ss := subsumed(kw_arg_type, function_type.bundle_kw_param_type, inher_aux),
            ss
        )[-1]
        for kw, kw_arg_type in kw_arg_types.items()
        if function_type.bundle_kw_param_type != None
        if (
            not kw in {sig.key for sig in function_type.pos_kw_param_sigs} and
            not kw in {sig.key for sig in function_type.kw_param_sigs}
        )
    ]

    # union with fresh variable
    unionized_subst_map = pmap({
        k:unionize_types(t, make_VarType(gen_fresh_var()))
        for k, t in subst_map.items()
    })

    if us.every(checks, lambda c : c):
        return (substitute_function_type_args(function_type, subst_map), unionized_subst_map)
    else:
        return (None, unionized_subst_map)


def is_literal_string(content : str) -> bool:
    try:
        result = literal_eval(content)
        return isinstance(result, str)
    except:
        return False

def from_inher_aux_to_primitive(inher_aux : InherAux):
    return ['A', 
        [from_type_to_primitive(t) for t in inher_aux.observed_types], 
        from_env_to_primitive(inher_aux.local_env), 
        from_env_to_primitive(inher_aux.nonlocal_env), 
        from_env_to_primitive(inher_aux.global_env),
        # from_class_env_to_primitive(inher_aux.class_env), 
    ]


def from_variant_to_primitive(v : variant) -> str:
    return match_variant(v, VariantHandlers(
        case_ContraVariant= lambda _ : "ContraVariant",
        case_CoVariant= lambda _ : "CoVariant",
        case_NoVariant= lambda _ : "NoVariant"
    ))


def from_declaration_to_primitive(dec : Declaration) -> list: 
    return [
        dec.updatable,
        dec.initialized,
        from_type_to_primitive(dec.type)
    ]


def from_module_to_primitive(module : InsertOrderMap[str, Declaration]) -> dict[str, list]:
    return {
        k : from_declaration_to_primitive(dec) 
        for k, dec in module.items()
    }

def from_package_to_primitive(package : InsertOrderMap[str, ModulePackage]) -> dict[str, list]:
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
        case_ProtocolType = lambda t : ["ProtocolType"],
        case_GenericType = lambda t : ["GenericType"],
        case_OverloadType = lambda t : ["OverloadType"],
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
            [from_type_to_primitive(t.bundle_pos_param_type)] if t.bundle_pos_param_type else [],
            [from_ParamSig_to_primitive(p) for p in t.kw_param_sigs],
            [from_type_to_primitive(t.bundle_kw_param_type)] if t.bundle_kw_param_type else [],
            from_type_to_primitive(t.return_type)
        ],
        case_UnionType = lambda t : ["UnionType", [from_type_to_primitive(tc) for tc in t.type_choices]],
        case_InterType = lambda t : ["InterType", [from_type_to_primitive(tc) for tc in t.type_components]],
        case_RecordType = lambda t : ["RecordType", t.class_key, t.class_version, [
            from_type_to_primitive(ta)
            for ta in t.type_args
        ]],
        case_TupleLitType = lambda t : ["TupleLitType", [from_type_to_primitive(it) for it in t.item_types]],
        case_VariedTupleType = lambda t : ["VariedTupleType", from_type_to_primitive(t.item_type)],
        case_NamedTupleType = lambda t : ["NamedTupleType", t.name, [fd for fd in t.fields]],
        case_ListLitType = lambda t : ["ListLitType", [from_type_to_primitive(it) for it in t.item_types]],
        case_DictLitType = lambda t : ["DictLitType", [
            (from_type_to_primitive(kt), from_type_to_primitive(vt)) 
            for kt, vt in t.pair_types
        ]],
        case_TrueType = lambda t : ["TrueType"],
        case_FalseType = lambda t : ["FalseType"],
        case_IntLitType = lambda t : ["IntLitType", t.literal],
        case_FloatLitType = lambda t : ["FloatLitType", t.literal],
        case_StrLitType = lambda t : ["StrLitType", t.literal],
    ))


from os import path
def analyze_modules_once(
    root_dir : str, 
    file_paths : Sequence[str], 
    package : InsertOrderMap[str, ModulePackage],
) -> InsertOrderMap[str, ModulePackage]:

    root_dir = path.abspath(root_dir)
    package_start = len(root_dir) + 1 

    file_paths = sorted(list(file_paths))
    success_count = 0
    for i, file_path in enumerate(file_paths):

        file_path_split = file_path.split(".") 
        if file_path_split[-1] != "pyi": continue 
        module_segments = file_path[:-4][package_start:].split("/")
        module_path = (
            ".".join(module_segments[:-1])
            if module_segments[-1] == "__init__" else
            ".".join(module_segments)
        )

        assert path.isfile(file_path)

        checks = pset() 
        # (
        #     all_checks
        #     .remove(LookupInitCheck())
        #     .remove(LookupDecCheck())
        #     .remove(DeclareCheck())
        #     .remove(AssignTypeCheck())
        #     .remove(BranchDeclareCheck())
        # )

        try:
            with open(file_path) as f:

                code = f.read().strip()
                if code:
                    package = analyze_code(package, module_path, code, checks=checks)
                else:
                    package = insert_module_class_env_dotpath(package, module_path, iom(), iom())
                success_count += 1
        except Exception as ex:
            # raise ex
            continue
            # return package 
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
    package : InsertOrderMap[str, ModulePackage],
    max_iter : int = 10 
) -> InsertOrderMap[str, ModulePackage]:

    print(f"fixpoint iteration count: {0}")
    in_package = package 
    in_package_prim = from_package_to_primitive(package)
    out_package = analyze_modules_once(root_dir, module_paths, in_package) 
    out_package_prim = from_package_to_primitive(out_package)

    count = 1
    print(f"fixpoint iteration count: {count}")
    while count < max_iter and out_package_prim != in_package_prim:
        in_package = out_package
        in_package_prim = out_package_prim 
        out_package = analyze_modules_once(root_dir, module_paths, in_package) 
        out_package_prim = from_package_to_primitive(out_package)
        count += 1
        print(f"fixpoint iteration count: {count}")

    return out_package


def with_cache(cache_path : str, f : Callable[[], T], cache_loadable : bool = True) -> T:
    return (
        us.load_object(cache_path)
        if cache_loadable and os.path.exists(us.project_path(cache_path)) else
        us.save_object(f(), cache_path)
    )

def analyze_typeshed_cache(cache_loadable : bool = True):
    return with_cache('tapas_res/cache/typeshed_cache', analyze_typeshed, cache_loadable)


def analyze_typeshed(max_iter : int = 2) -> InsertOrderMap[str, ModulePackage]:
    stdlib_dirpath = us.project_path("tapas_res/typeshed/stdlib")
    stdlib_module_paths = collect_module_paths(stdlib_dirpath)

    package : InsertOrderMap[str, ModulePackage] = iom()
    package = analyze_modules_fixpoint(stdlib_dirpath, stdlib_module_paths, package, max_iter) 

    # other_libs_dirpath = us.project_path(f"../typeshed/stubs")
    # other_module_paths = collect_module_paths(other_libs_dirpath)
    # package = analyze_modules_fixpoint(other_libs_dirpath, other_module_paths, package, limit) 
    return package 

def analyze_numpy_stubs(package : InsertOrderMap[str, ModulePackage], max_iter : int = 5) -> InsertOrderMap[str, ModulePackage]: 
    stdlib_dirpath = us.project_path("tapas_res/numpyshed")
    stdlib_module_paths = collect_module_paths(stdlib_dirpath)
    package = analyze_modules_fixpoint(stdlib_dirpath, stdlib_module_paths, package, max_iter) 
    return package

def analyze_pandas_stubs(package : InsertOrderMap[str, ModulePackage], max_iter : int = 6) -> InsertOrderMap[str, ModulePackage]: 
    stdlib_dirpath = us.project_path("tapas_res/pandas-stubs")
    stdlib_module_paths = collect_module_paths(stdlib_dirpath)
    package = analyze_modules_fixpoint(stdlib_dirpath, stdlib_module_paths, package, max_iter) 
    return package

def analyze_stubs() -> InsertOrderMap[str, ModulePackage]:
    package = analyze_typeshed()
    package = analyze_numpy_stubs(package)
    return package

def analyze_code(
    package : InsertOrderMap[str, ModulePackage], 
    module_name, 
    code : str,
    checks = all_checks
) -> InsertOrderMap[str, ModulePackage]:

    gnode = pgs.parse(code)
    mod = pas.parse_from_generic_tree(gnode)
    abstract_tokens = pas.serialize(mod)

    client : Client = spawn_analysis(package, module_name, checks)

    last_inher_aux : InherAux = client.init
    a_keys_len = len(last_inher_aux.package.keys())
    for token in abstract_tokens:
        last_inher_aux = client.next(token)

    b_keys_len = len(last_inher_aux.package.keys())
    assert b_keys_len >= a_keys_len

    return last_inher_aux.package

def from_semantic_check_to_string(sc : semantic_check) -> str:
    return match_semantic_check(sc, SemanticCheckHandlers(
        case_LookupTypeCheck = lambda _ : "lookup_type_check", 
        case_ApplyArgTypeCheck = lambda _ : "apply_arg_type_check", 
        case_ApplyRatorTypeCheck = lambda _ : "apply_rator_type_check", 
        case_SplatKeywordArgTypeCheck = lambda _ : "splat_keyword_arg_type_check", 
        case_ReturnTypeCheck = lambda _ : "return_type_check", 
        case_UnifyTypeCheck = lambda _ : "unify_type_check", 
        case_AssignTypeCheck = lambda _ : "assign_type_check", 
        case_IterateTypeCheck = lambda _ : "iterate_type_check", 
        case_LookupDecCheck = lambda _ :  "lookup_dec_check",
        case_LookupInitCheck = lambda _ : "lookup_init_check", 
        case_UpdateCheck = lambda _ : "update_check", 
        case_DeclareCheck = lambda _ : "declare_check",
        case_BranchDeclareCheck = lambda _ : "branch_declare_check",
    ))

def analyze_summary(
    package : InsertOrderMap[str, ModulePackage], 
    module_name, 
    code : str,
    checks = all_checks
) -> str:

    try:
        analyze_code(package, module_name, code, checks)
    except Exception as ex:
        if isinstance(ex, semantic_check):
            return from_semantic_check_to_string(ex)
        elif isinstance(ex, pap.Obsolete):
            return "parsing_obsolete"
        elif isinstance(ex, pap.Unsupported):
            return "parsing_unsupported"
        elif isinstance(ex, pap.ConcreteParsingError):
            return "parsing_concrete"
        elif isinstance(ex, pap.TreeSitterError):
            return "parsing_tree_sitter"
        else:
            import builtins
            return builtins.type(ex).__name__

    return "ok"


def from_class_env_to_primitive(env : PMap[str, ClassRecord]) -> dict:

    return {
        symbol : [p.key, 
            [from_type_to_primitive(t) for t in p.type_params],
            [from_type_to_primitive(t) for t in p.super_types],
            [[k, from_type_to_primitive(t)] for k, t in (p.static_fields.items())],
            [[k, from_type_to_primitive(t)] for k, t in (p.instance_fields.items())]
        ]

        for symbol, p in (env.items())
    }


def from_env_to_primitive(env : InsertOrderMap[str, Declaration]) -> dict:
    return {
        key : [p.initialized, from_type_to_primitive(p.type)]
        for key, p in env.items()
    }

def from_env_to_primitive_verbose(env : InsertOrderMap[str, Declaration]) -> dict:
    return {
        symbol : [f'initialized={p.initialized}', f'updatable={p.updatable}', from_type_to_primitive(p.type)]
        for symbol, p in (env.items())
    }

def traverse_function_body(inher_aux : InherAux, path_extension : str, anchor_symbol : str) -> InherAux:

    if not inher_aux.internal_path:
        return update_InherAux(inher_aux,
            # move local_decl into global_decl
            global_env = inher_aux.local_env,
            # reset local_decl
            local_env = iom(), 
            internal_path = path_extension,
            in_class = False,
            anchor_symbol = anchor_symbol if inher_aux.method_kind else ''
        )
    else:
        return update_InherAux(inher_aux,
            # move local_decl into nonlocal_decl 
            nonlocal_env = inher_aux.nonlocal_env + inher_aux.local_env, 
            # reset local_decl
            local_env = iom(), 
            internal_path = f"{inher_aux.internal_path}.{path_extension}",
            in_class = False,
            anchor_symbol = anchor_symbol if inher_aux.method_kind else ''
        )


def traverse_aux(inher_aux : InherAux, synth_aux : SynthAux) -> InherAux:
    local_env = inher_aux.local_env 
    for sub in synth_aux.decl_subtractions:
        local_env.remove(sub)

    # clear the anchor symbol if it has been overwritten
    anchor_symbol = (
        ""
        if synth_aux.decl_additions.get(inher_aux.anchor_symbol) else
        inher_aux.anchor_symbol
    )

    return update_InherAux(inher_aux, 
        local_env = local_env + synth_aux.decl_additions,
        declared_globals = inher_aux.declared_globals.update(synth_aux.declared_globals),
        declared_nonlocals = inher_aux.declared_nonlocals.update(synth_aux.declared_nonlocals),
        class_env = inher_aux.class_env + synth_aux.class_additions,
        observed_types = synth_aux.observed_types,
        anchor_symbol=anchor_symbol
    )

@dataclass(frozen=True, eq=True)
class Change(Generic[T]):
    subtractions: PSet[str]
    additions: InsertOrderMap[str, T] 

def to_change_decl(body_aux : SynthAux) -> Change[Declaration]:
    return Change(
        subtractions=body_aux.decl_subtractions,
        additions=body_aux.decl_additions
    )


import threading
from queue import Queue

@dataclass
class Client: 
    init : InherAux
    init_prim : list 
    next : Callable[[abstract_token], InherAux]
    next_prim : Callable[[list], list | None]
    kill : Callable[[Exception], None]


def insert_module_class_env_dotpath(
    package : InsertOrderMap[str, ModulePackage], dotpath : str,
    module : InsertOrderMap[str, Declaration], 
    class_env : InsertOrderMap[str, ClassRecord]
) -> InsertOrderMap[str, ModulePackage]:
    rpath = [s for s in reversed(dotpath.split("."))]
    return insert_module_class_env_rpath(package, rpath, module, class_env) 

def insert_module_class_env_rpath(
    package : InsertOrderMap[str, ModulePackage], 
    rpath : Sequence[str], 
    module : InsertOrderMap[str, Declaration], 
    class_env : InsertOrderMap[str, ClassRecord]
) -> InsertOrderMap[str, ModulePackage]:

    assert len(rpath) > 0 
    hd = rpath[-1]
    tl = rpath[:-1]

    if not tl:
        new_module_package = (
            update_ModulePackage(package[hd], module = module, class_env = class_env) 
            if package.get(hd) else
            make_ModulePackage(module = module, class_env = class_env)
        )

        return package + iom((hd, new_module_package))
    else:
        empty_package : InsertOrderMap[str, ModulePackage] = iom()

        hd_module_package = (
            update_ModulePackage(package[hd],
                package = insert_module_class_env_rpath(package[hd].package, tl, module, class_env)
            )
            if package.get(hd) else
            make_ModulePackage(
                package = insert_module_class_env_rpath(empty_package, tl, module, class_env)
            )
        )

        return package + iom((hd, hd_module_package))
        
        


def from_package_get_ModulePackage(package : InsertOrderMap[str, ModulePackage], external_path : str) -> ModulePackage | None:
    assert external_path
    levels = external_path.split(".")
    result : ModulePackage | None = package.get(levels[0])

    for level in levels[1:]:

        if result:
            result = result.package.get(level)
        else:
            return None


    return result

class AnalysisComplete(Exception): pass

def spawn_analysis(
    package : InsertOrderMap[str, ModulePackage], 
    module_name : str, 
    checks : PSet[semantic_check] = all_checks
) -> Client:

    in_stream : Queue[abstract_token | Exception] = Queue()
    out_stream : Queue[InherAux | Exception] = Queue()

    server : Server = Server(in_stream, out_stream, checks)

    mp = from_package_get_ModulePackage(package, module_name)

    inher_aux = (
        make_InherAux(
            external_path = module_name, 
            package = package,
            local_env = iom(*(
                (sym, update_Declaration(dec, initialized=False, overloading=False)) 
                for sym, dec in mp.module.items()
            )),
            class_env = mp.class_env
        )
        if mp else
        make_InherAux(external_path = module_name, package = package)
    )

    def run():
        try:
            nonlocal module_name
            nonlocal inher_aux
            token = in_stream.get()

            if isinstance(token, Exception):
                raise token

            synth = server.crawl_module(token, inher_aux)

            module : InsertOrderMap[str, Declaration] = iom(*(
                (k, dec)
                for k, dec in synth.aux.decl_additions.items()
            ))


            class_env : InsertOrderMap[str, ClassRecord] = iom(*(
                (k, cr) 
                for k, cr in synth.aux.class_additions.items()
            ))

            final_inher_aux = update_InherAux(inher_aux,
                external_path = "",
                global_env = iom(),
                nonlocal_env = iom(),
                local_env = iom(),
                class_env = iom(), 
                package = insert_module_class_env_dotpath(inher_aux.package, inher_aux.external_path, module, class_env)
            )
            out_stream.put(final_inher_aux)
            out_stream.put(AnalysisComplete())

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
        next_prim = next_prim,
        kill = lambda ex: in_stream.put(ex)
    ) 





def analyze_statements(
    statements_ast : pas.statements, 
    inher_aux : InherAux, 
) -> SynthAux:

    in_stream : Queue[abstract_token | Exception] = Queue()
    out_stream : Queue[InherAux | Exception] = Queue()

    return_stream : Queue[SynthAux] = Queue()

    server : Server = Server(in_stream, out_stream)

    def run():
        tok = in_stream.get()
        if isinstance(tok, Exception):
            raise tok
        synth = server.crawl_statements(tok, inher_aux)
        out_stream.put(inher_aux)
        return_stream.put(synth.aux)

    import threading
    thread = threading.Thread(target = run)
    thread.start()

    from tapas_lib.python_ast_serialize_autogen import from_statements as serialize_statements
    tokens : tuple[abstract_token, ...] = serialize_statements(statements_ast)
    for tok in tokens:
        in_stream.put(tok)
        out_stream.get()

    return return_stream.get() 


def analyze_expr(
    expr_ast : pas.expr, 
    inher_aux : InherAux, 
) -> SynthAux:

    in_stream : Queue[abstract_token | Exception] = Queue()
    out_stream : Queue[Union[InherAux, Exception]] = Queue()

    return_stream : Queue[SynthAux] = Queue()

    server : Server = Server(in_stream, out_stream)

    def run():
        tok = in_stream.get()
        if isinstance(tok, Exception):
            raise tok
        synth = server.crawl_expr(tok, inher_aux)
        out_stream.put(inher_aux)
        return_stream.put(synth.aux)

    import threading
    thread = threading.Thread(target = run)
    thread.start()

    from tapas_lib.python_ast_serialize_autogen import from_expr as serialize_expr
    tokens : tuple[abstract_token, ...] = serialize_expr(expr_ast)
    for tok in tokens:
        in_stream.put(tok)
        out_stream.get()

    return return_stream.get()

class Server(paa.Server[InherAux, SynthAux]):

    def __init__(self, 
        in_stream : Queue[abstract_token | Exception], 
        out_stream : Queue[InherAux | Exception],
        checks : PSet[semantic_check] = all_checks
    ):  
        super().__init__(in_stream, out_stream)
        self.checks = checks

    def get_mapping_key_value_types(self, t : type, inher_aux : InherAux) -> tuple[type, type]:
        if isinstance(t, RecordType):

            if t.class_key == "typing.Mapping":
                assert len(t.type_args) == 2
                key_type = t.type_args[0] 
                val_type = t.type_args[1] 
                return (key_type, val_type)

            class_record = from_static_path_to_ClassRecord(inher_aux, t.class_key)
            if class_record:
                substitution_map : PMap[str, type] = pmap({
                    class_record.type_params[i].name : type_arg
                    for i, type_arg in enumerate(t.type_args) 
                })

                for super_type in class_record.super_types:
                    super_type = substitute_type_args(super_type, substitution_map)
                    result = self.get_mapping_key_value_types(super_type, inher_aux)
                    return result

                self.check(IterateTypeCheck(), lambda:True)
                return (AnyType(), AnyType())
            else:
                return (AnyType(), AnyType())

        elif isinstance(t, AnyType):
            return (AnyType(), AnyType())

        else:
            self.check(IterateTypeCheck(), lambda:True)
            return (AnyType(), AnyType())


    def get_iterable_item_type_from_RecordType(self, t : RecordType, inher_aux : InherAux) -> type | None:

        if t.class_key == "typing.Iterable": 
            assert len(t.type_args) == 1
            item_type = t.type_args[0]
            return item_type
        
        class_record = from_static_path_to_ClassRecord(inher_aux, t.class_key)
        if class_record:
            substitution_map : PMap[str, type] = pmap({
                class_record.type_params[i].name : type_arg
                for i, type_arg in enumerate(t.type_args) 
            })

            for super_type in class_record.super_types:
                super_type_content = substitute_type_args(super_type.content, substitution_map)

                result = self.get_iterable_item_type(super_type_content, inher_aux)
                if result:
                    return result

            return None
        else:
            return AnyType()

    def get_iterable_item_type_from_UnionType(self, t : UnionType, inher_aux : InherAux) -> type | None:
        assert len(t.type_choices) > 0

        item = t.type_choices[0]
        for tc in t.type_choices[1:]:
            tc_item = self.get_iterable_item_type(tc, inher_aux)
            if tc_item:
                item = unionize_types(item, tc_item)
            else:
                return None
        return item

    def get_iterable_item_type(self, iter_type : type, inher_aux : InherAux) -> Optional[type]:

        return match_type(iter_type, TypeHandlers(
            case_ProtocolType = lambda t : None,
            case_GenericType = lambda t : None,
            case_OverloadType = lambda t : None,
            case_TypeType = lambda t : None,
            case_VarType = lambda t : 
                # treat VarType like AnyType if it hasn't been substituted
                AnyType(), 
            case_EllipType = lambda t : None,
            case_AnyType = lambda t : AnyType(),
            case_ObjectType = lambda t : None,
            case_NoneType = lambda t : None, 
            case_ModuleType = lambda t : None,
            case_FunctionType = lambda t : None,
            case_UnionType = lambda t : self.get_iterable_item_type_from_UnionType(t, inher_aux),
            case_InterType = lambda t : None,
            case_RecordType = lambda t : self.get_iterable_item_type_from_RecordType(t, inher_aux),
            case_TupleLitType = lambda t : unionize_all_types(t.item_types),
            case_VariedTupleType = lambda t : t.item_type,
            case_NamedTupleType = lambda t : AnyType(),
            case_ListLitType = lambda t : unionize_all_types(t.item_types),
            case_DictLitType = lambda t : self.get_iterable_item_type(generalize_type(inher_aux, t), inher_aux),
            case_TrueType = lambda t : None,
            case_FalseType = lambda t : None,
            case_IntLitType = lambda t : None,
            case_FloatLitType = lambda t : None,
            case_StrLitType = lambda t : make_RecordType(class_key="builtins.str"),
        ))



    def unionize_envs(self, envs : list[InsertOrderMap[str, type]]) -> InsertOrderMap[str, type]:
        env_result : InsertOrderMap[str, type] = iom()

        for env in envs: 
            for k, new_type in env.items():
                old_type =  env_result.get(k)
                if old_type:
                    env_result += iom((k, unionize_types(old_type, new_type)))
                else:
                    env_result += iom((k,  new_type))
            

        return env_result 

    def unify(
        self,
        pattern : pas.expr, type : type, 
        inher_aux : InherAux
    ) -> tuple[InsertOrderMap[str, type], InsertOrderMap[str, type]]: 
        anchor_symbol : str = inher_aux.anchor_symbol

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
            return (iom((pattern.content, type)), iom())
        ######################## 
        ## OLD CODE commented out: ##
        # elif isinstance(pattern, pas.List):
        #     type_env : InsertOrderMap[str, type] = iom()
        #     anchor_env : InsertOrderMap[str, type] = iom()
        #     assert pattern.content
        #     for p in generate_items(pattern.content):
        #         item_type = self.get_iterable_item_type(type, inher_aux)
        #         if item_type:
        #             new_type_env, new_anchor_env = self.unify(p, item_type, inher_aux)
        #             type_env += new_type_env
        #             anchor_env += new_anchor_env
        #         else:
        #             self.check(UnifyTypeCheck(), lambda:True)

        #     return (type_env, anchor_env)
        # elif isinstance(pattern, pas.Tuple):
        ########################
        elif isinstance(pattern, pas.List) or isinstance(pattern, pas.Tuple):
            if isinstance(type, TupleLitType):
                type_env : InsertOrderMap[str, type] = iom()
                anchor_env : InsertOrderMap[str, type] = iom()
                assert pattern.content
                for i, p in enumerate(generate_items(pattern.content)):
                    new_type_env, new_anchor_env = self.unify(p, type.item_types[i], inher_aux)
                    type_env += new_type_env 
                    anchor_env += new_anchor_env

                return (type_env, anchor_env)
            elif isinstance(type, UnionType):
                type_envs : list[InsertOrderMap[str, type]] = []
                anchor_envs : list[InsertOrderMap[str, type]] = []
                assert pattern.content
                for choice_type in type.type_choices:
                    (type_env, anchor_env) = self.unify(pattern, choice_type, inher_aux)
                    type_envs.append(type_env)
                    anchor_envs.append(anchor_env)
                return (self.unionize_envs(type_envs), self.unionize_envs(anchor_envs))
            else:
                type_env : InsertOrderMap[str, type] = iom()
                anchor_env : InsertOrderMap[str, type] = iom()
                assert pattern.content
                for p in generate_items(pattern.content):
                    item_type = self.get_iterable_item_type(type, inher_aux)
                    if item_type:
                        new_type_env, new_anchor_env = self.unify(p, item_type, inher_aux)
                        type_env += new_type_env
                        anchor_env += new_anchor_env
                    else:
                        self.check(UnifyTypeCheck(), lambda:True)
                        return (iom(), iom())

                return (type_env, anchor_env)
        elif isinstance(pattern, pas.Attribute):
            content = pattern.content
            if isinstance(content, pas.Name) and content.content == anchor_symbol:
                return (iom(), iom((pattern.name, type)))
            else:
                return (iom(), iom())
        elif isinstance(pattern, pas.Subscript):
            return (iom(), iom())
        else:
            self.check(UnifyTypeCheck(), lambda:True)
            return (iom(), iom())


    def unify_iteration(self, inher_aux : InherAux, pattern : pas.expr, iter_type : type) -> InsertOrderMap[str, type]:
        if isinstance(iter_type, AnyType):
            return self.unify(pattern, AnyType(), inher_aux)[0]
        else:
            item_type = self.get_iterable_item_type(iter_type, inher_aux)

            if item_type:
                target_types = self.unify(pattern, item_type, inher_aux)[0]
                for k, t in target_types.items():
                    dec = lookup_declaration(inher_aux, k)
                    if dec and not subsumed(t, dec.type, inher_aux):
                        self.check(UnifyTypeCheck(), lambda:True)

                return target_types
            else:
                self.check(IterateTypeCheck(), lambda:True)
                return iom()





    def cross_join_aux_decls(self, inher_aux : InherAux, true_body_aux : Change[Declaration], false_body_aux : Change[Declaration]) -> Change[Declaration]:

        subtractions : PSet[str] = s()
        for sub in true_body_aux.subtractions:
            if sub in false_body_aux.subtractions:
                subtractions = subtractions.add(sub)

        body_additions : InsertOrderMap[str, Declaration] = iom()
        for target, true_body_dec in true_body_aux.additions.items():
            if target in false_body_aux.additions:
                false_body_dec = false_body_aux.additions[target]   

                self.check(BranchDeclareCheck(), lambda: (
                    bool(true_body_dec.decorator_types == false_body_dec.decorator_types) and
                    bool(
                        (not (true_body_dec.updatable) and not false_body_dec.updatable) or 
                        (
                            true_body_dec.updatable and false_body_dec.updatable and 
                            subsumed(true_body_dec.updatable, false_body_dec.updatable, inher_aux) and 
                            subsumed(true_body_dec.type, false_body_dec.updatable, inher_aux) and 
                            subsumed(false_body_dec.updatable, true_body_dec.updatable, inher_aux) and
                            subsumed(false_body_dec.type, true_body_dec.updatable, inher_aux) 
                        )
                    )
                ))

                updatable = true_body_dec.updatable and false_body_dec.updatable and (
                    unionize_types(true_body_dec.updatable, false_body_dec.updatable)
                )
                initialized = true_body_dec.initialized and false_body_dec.initialized
                type = (
                    unionize_types(true_body_dec.type, false_body_dec.type)
                    if BranchDeclareCheck() in self.checks else
                    true_body_dec.type
                )
                decorator_types = true_body_dec.decorator_types

                new_declaration = make_Declaration(
                    updatable=updatable,
                    initialized=initialized,
                    type = type,
                    decorator_types=decorator_types
                ) 
                body_additions = body_additions + iom((target, new_declaration))


        return Change(
            subtractions = subtractions,
            additions = body_additions
        )


    def match_function_type(self, inher_aux : InherAux, 
        pos_arg_types : Sequence[type],
        kw_arg_types : Mapping[str, type], 
        it : InterType
    ) -> tuple[FunctionType | None, PMap[str, type]]:
        chosen_func_type = None
        for ft in it.type_components:
            self.check(ApplyRatorTypeCheck(), lambda:
                isinstance(ft, FunctionType)
            )
            if isinstance(ft, FunctionType):
                chosen_func_type, subst_map = check_application_args(pos_arg_types, kw_arg_types, ft, inher_aux)
                if chosen_func_type:
                    return chosen_func_type, subst_map
            else:
                return chosen_func_type, pmap({})
        return chosen_func_type, pmap({})

 


    def check(self, sc : semantic_check, f : Callable[[], bool]): 
        if sc in self.checks:
            if not f():
                raise sc

    def update_nested_usages(self, 
        decls: InsertOrderMap[str, Declaration], 
        usage_additions : PMap[str, Usage], 
        nested_usages : PMap[str, tuple[Usage, ...]]
    ):
        # potential future declarations
        # past declarations are subsumed filtered out via backref 
        # e.g. no need to include parameters (which are always past declarations)

        for symbol, dec in decls.items(): 
            symbol_usages = nested_usages.get(symbol) or () 
            if symbol_usages:
                nested_usages = nested_usages.remove(symbol)
                self.check(UpdateCheck(), lambda: 
                    us.every(symbol_usages, lambda symbol_usage:
                        not symbol_usage.updated or bool(dec.updatable)
                    )
                )


            local_usage = usage_additions.get(symbol)
            self.check(LookupDecCheck(), lambda:
                not local_usage or local_usage.backref
            )

            self.check(LookupInitCheck(), lambda: 
                not local_usage or not local_usage.backref or dec.initialized 
            )

        nested_usages = merge_nested_usages(
            pmap({
                k : (usg,)
                for k, usg in usage_additions.items() 
                if not usg.backref
            }),
            nested_usages
        )
        return nested_usages


    def check_decl_usage(self, dec_env : PMap[str, Declaration], usage_env : PMap[str, Usage]):
        self.check(DeclareCheck(), lambda:
            us.every(dec_env.keys(), lambda k :
                k in usage_env
            )  
        )

    # override parent class method
    def traverse_auxes(self, inher_aux : InherAux, synth_auxes : tuple[tuple[str, SynthAux], ...], parent_syntax_type, target_syntax_type) -> InherAux:
        if (
            target_syntax_type in ['expr', 'stmt', 'statements', 'str'] and
            True
        ):
            for source_syntax_type, synth_aux in synth_auxes:
                if source_syntax_type != "Param":
                    inher_aux = traverse_aux(inher_aux, synth_aux)
            return inher_aux
        else:
            return inher_aux

    # override parent class method
    def synthesize_auxes(self, auxes : tuple[SynthAux, ...]) -> SynthAux:

        static_field_additions : InsertOrderMap[str, type] = iom() 
        instance_field_additions : InsertOrderMap[str, type] = iom() 

        class_additions : InsertOrderMap[str, ClassRecord] = iom()
        decl_subtractions : PSet[str] = s()
        decl_additions : InsertOrderMap[str, Declaration] = iom()
        declared_globals : PSet[str] = s()
        declared_nonlocals : PSet[str] = s()
        usage_additions : PMap[str, Usage] = m()
        nested_usages : PMap[str, tuple[Usage, ...]] = m()

        method_names : tuple[str, ...] = ()
        observed_types : tuple[type, ...] = ()

        kw_types : PMap[str, type] = m()

        return_types : tuple[type, ...] = ()
        yield_types : tuple[type, ...] = ()

        var_types : tuple[VarType, ...] = ()

        protocol : bool = False

        param_sig : Optional[ParamSig] = None 
        pos_param_types : tuple[type, ...] = ()
        pos_kw_param_sigs : tuple[ParamSig, ...] = ()
        list_splat_param_type : Optional[type] = None
        kw_param_sigs : tuple[ParamSig, ...] = ()
        dict_splat_param_type : Optional[type] = None

        import_names  : InsertOrderMap[str, str] = iom()


        for aux in auxes:

            static_field_additions = static_field_additions + aux.static_field_additions
            instance_field_additions = instance_field_additions + aux.instance_field_additions

            class_additions = class_additions + aux.class_additions

            for sub in aux.decl_subtractions:
                if decl_additions.get(sub):
                    decl_additions = decl_additions.remove(sub)

            decl_subtractions = decl_subtractions.update(aux.decl_subtractions)
            decl_additions = decl_additions + aux.decl_additions
            declared_globals = declared_globals.update(aux.declared_globals)
            declared_nonlocals = declared_nonlocals.update(aux.declared_nonlocals)
            usage_additions = merge_usage_additions(usage_additions, aux.usage_additions)
            nested_usages = merge_nested_usages(nested_usages, aux.nested_usages)

            method_names = method_names + aux.cmp_names

            observed_types = observed_types + aux.observed_types

            kw_types = kw_types + aux.kw_types

            return_types = return_types + aux.return_types
            yield_types = yield_types + aux.yield_types

            var_types = var_types + aux.var_types
            protocol = protocol or aux.protocol

            param_sig = param_sig if param_sig else aux.param_sig

            pos_param_types = pos_param_types + aux.pos_param_types
            pos_kw_param_sigs = pos_kw_param_sigs + aux.pos_kw_param_sigs
            list_splat_param_type = list_splat_param_type if list_splat_param_type else aux.bundle_pos_param_type
            kw_param_sigs = kw_param_sigs + aux.kw_param_sigs 
            dict_splat_param_type = dict_splat_param_type if dict_splat_param_type else aux.bundle_kw_param_type 

            import_names = import_names + aux.import_names

        return SynthAux(
            static_field_additions,
            instance_field_additions,

            class_additions,
            decl_subtractions, decl_additions, 
            declared_globals, declared_nonlocals, 
            usage_additions, 
            nested_usages, 
            method_names,
            observed_types, 
            kw_types,
            return_types,
            yield_types,
            var_types,
            protocol,
            param_sig, 
            pos_param_types, pos_kw_param_sigs, list_splat_param_type, kw_param_sigs, dict_splat_param_type,
            import_names
        )


    # synthesize: expr <-- BoolOp
    def synthesize_for_expr_BoolOp(self, 
        inher_aux : InherAux,
        left_tree : pas.expr, 
        left_aux : SynthAux,
        pre_comment_tree : str, 
        pre_comment_aux : SynthAux,
        rator_tree : pas.bool_rator, 
        rator_aux : SynthAux,
        post_comment_tree : str, 
        post_comment_aux : SynthAux,
        right_tree : pas.expr, 
        right_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        assert len(left_aux.observed_types) == 1
        left_type = left_aux.observed_types[0]
        assert len(right_aux.observed_types) == 1
        right_type = right_aux.observed_types[0]

        expr_type = AnyType()

        # TODO: use some sort of subsumption check to determine __and__ vs _rand__ etc
        # infix operators should use the method on the higher type
        if subsumed(left_type, right_type, inher_aux):
            left_type = right_type

        method_name = pas.from_bool_rator_to_method_name(rator_tree)
        method_type = lookup_field_type(left_type, method_name, inher_aux)

        if isinstance(method_type, FunctionType):

            precise_method_type, subst_map = check_application_args(
                [right_type], {}, 
                method_type, inher_aux
            )
            self.check(ApplyArgTypeCheck(), lambda: precise_method_type != None)
            if precise_method_type: 
                expr_type = precise_method_type.return_type

        elif isinstance(method_type, InterType):
            chosen_method_type, _ = self.match_function_type(
                inher_aux,
                [right_type], {}, 
                method_type
            ) 
            self.check(ApplyArgTypeCheck(), lambda: chosen_method_type != None)
            if chosen_method_type:
                expr_type = chosen_method_type.return_type

        return paa.Result[SynthAux](
            tree = pas.make_BoolOp(left_tree, pre_comment_tree, rator_tree, post_comment_tree, right_tree),
            aux = update_SynthAux(self.synthesize_auxes((left_aux, rator_aux, right_aux)),
                observed_types = (expr_type,)
            )
        )
    

    # synthesize: expr <-- AssignExpr
    def synthesize_for_expr_AssignExpr(self, 
        inher_aux : InherAux,
        target_tree : pas.expr, 
        target_aux : SynthAux,
        pre_comment_tree : str, 
        pre_comment_aux : SynthAux,
        post_comment_tree : str, 
        post_comment_aux : SynthAux,
        content_tree : pas.expr, 
        content_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        # TODO: if source is of TypeType(VarType), check that target symbol matches VarType's symbol

        # check name compatability between target and source expressions 
        self.check(UpdateCheck(), lambda: 
            us.every(content_aux.usage_additions, lambda name : 
                name not in target_aux.usage_additions or 
                name in inher_aux.declared_globals or 
                name in inher_aux.declared_nonlocals or 
                name in inher_aux.local_env
            )
        )

        updated_usage_additions : PMap[str, Usage] = m()
        for name, usage in target_aux.usage_additions.items():
            if declared_and_initialized(inher_aux, name):
                updated_usage_additions = updated_usage_additions + pmap({name : update_Usage(usage, updated = True)})

        assert len(content_aux.observed_types) == 1
        content_type = content_aux.observed_types[0]


        unified_env, unified_anchor_env = self.unify(target_tree, content_type, inher_aux)

        return paa.Result[SynthAux](
            tree = pas.make_AssignExpr(target_tree, pre_comment_tree, post_comment_tree, content_tree),
            aux = update_SynthAux(content_aux,
                decl_additions = (
                    content_aux.decl_additions +
                    iom(*(
                        (k, make_Declaration(updatable = AnyType(), initialized=True, type = t))
                        for k, t in unified_env.items() 
                    ))
                ),
                usage_additions = merge_usage_additions(updated_usage_additions, content_aux.usage_additions),
                static_field_additions=(
                    unified_anchor_env
                    if isinstance(inher_aux.method_kind, ClassMethod) else
                    iom()
                ),
                instance_field_additions=(
                    unified_anchor_env
                    if isinstance(inher_aux.method_kind, InstanceMethod) else
                    iom()
                ),
                
            )
        )

    
    # synthesize: expr <-- BinOp
    def synthesize_for_expr_BinOp(self, 
        inher_aux : InherAux,
        left_tree : pas.expr, 
        left_aux : SynthAux,
        pre_comment_tree : str, 
        pre_comment_aux : SynthAux,
        rator_tree : pas.bin_rator, 
        rator_aux : SynthAux,
        post_comment_tree : str, 
        post_comment_aux : SynthAux,
        right_tree : pas.expr, 
        right_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        assert len(left_aux.observed_types) == 1
        left_type = left_aux.observed_types[0]
        assert len(right_aux.observed_types) == 1
        right_type = right_aux.observed_types[0]

        expr_type = AnyType()
        if (
            (isinstance(left_type, TypeType) or isinstance(right_type, TypeType)) and
            isinstance(rator_tree, pas.BitOr)
        ):
            left_instance_type = coerce_to_TypeType(left_type, inher_aux).content
            right_instance_type = coerce_to_TypeType(right_type, inher_aux).content
            union_type = unionize_types(left_instance_type, right_instance_type)
            expr_type = TypeType(content = union_type)
        else:


            # infix operators should use the method on the higher type
            if subsumed(left_type, right_type, inher_aux):
                left_type = right_type

            method_name = pas.from_bin_rator_to_method_name(rator_tree)
            method_type = lookup_field_type(left_type, method_name, inher_aux)

            if isinstance(method_type, FunctionType):

                precise_method_type, subst_map = check_application_args(
                    [right_type], {}, 
                    method_type, inher_aux
                )
                self.check(ApplyArgTypeCheck(), lambda: 
                    precise_method_type != None
                )
                if precise_method_type: 
                    expr_type = precise_method_type.return_type

            elif isinstance(method_type, InterType):

                chosen_method_type, _ = self.match_function_type(
                    inher_aux,
                    [right_type], {}, 
                    method_type
                ) 
                self.check(ApplyArgTypeCheck(), lambda: chosen_method_type != None)
                if chosen_method_type:
                    expr_type = chosen_method_type.return_type

        return paa.Result[SynthAux](
            tree = pas.make_BinOp(left_tree, pre_comment_tree, rator_tree, post_comment_tree, right_tree),
            aux = update_SynthAux(self.synthesize_auxes((left_aux, right_aux)),
                observed_types = (expr_type,)
            )
        )
    

    # synthesize: expr <-- UnaryOp 
    def synthesize_for_expr_UnaryOp(self, 
        inher_aux : InherAux,
        rator_tree : pas.unary_rator, 
        rator_aux : SynthAux,
        comment_tree, 
        comment_aux,
        rand_tree : pas.expr, 
        rand_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        assert len(rand_aux.observed_types) == 1
        rand_type = rand_aux.observed_types[0]
        method_name = pas.from_unary_rator_to_method_name(rator_tree)
        method_type = lookup_field_type(rand_type, method_name, inher_aux)
        return_type = AnyType()
        if isinstance(method_type, FunctionType):

            precise_method_type, subst_map = check_application_args(
                [], {}, 
                method_type, inher_aux
            )
            self.check(ApplyArgTypeCheck(), lambda: 
                precise_method_type != None
            )
            if precise_method_type:
                return_type = precise_method_type.return_type

        elif isinstance(method_type, InterType):

            chosen_method_type, _ = self.match_function_type(
                inher_aux,
                [], {}, 
                method_type
            )
            self.check(ApplyArgTypeCheck(), lambda: 
                chosen_method_type != None
            )
            if chosen_method_type: 
                return_type = chosen_method_type.return_type
        else:
            return_type = AnyType() 

        return paa.Result[SynthAux](
            tree = pas.make_UnaryOp(rator_tree, comment_tree, rand_tree),
            aux = update_SynthAux(rand_aux, 
                observed_types = (return_type,)
            )
        )


    # synthesize: expr <-- Lambda
    def synthesize_for_expr_Lambda(self, 
        inher_aux : InherAux,
        comment_a_tree : str, 
        comment_a_aux : SynthAux,
        params_tree : pas.parameters, 
        params_aux : SynthAux,
        comment_b_tree : str, 
        comment_b_aux : SynthAux,
        comment_c_tree : str, 
        comment_c_aux : SynthAux,
        body_tree : pas.expr, 
        body_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        assert len(body_aux.observed_types) == 1
        inferred_type = make_FunctionType(
            pos_kw_param_sigs = params_aux.pos_kw_param_sigs,
            return_type = body_aux.observed_types[0]
        )

        return paa.Result[SynthAux](
            tree = pas.make_Lambda(comment_a_tree, params_tree, comment_b_tree, comment_c_tree, body_tree),
            aux = update_SynthAux(self.synthesize_auxes((params_aux, body_aux)),
                observed_types = (inferred_type,)
            )  
        )
    
    # synthesize: expr <-- IfExp 
    def synthesize_for_expr_IfExp(self, 
        inher_aux : InherAux,
        body_tree : pas.expr, 
        body_aux : SynthAux,
        comment_a_tree : str, 
        comment_a_aux : SynthAux,
        comment_b_tree : str, 
        comment_b_aux : SynthAux,
        test_tree : pas.expr, 
        test_aux : SynthAux,
        comment_c_tree : str, 
        comment_c_aux : SynthAux,
        comment_d_tree : str, 
        comment_d_aux : SynthAux,
        orelse_tree : pas.expr, 
        orelse_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        assert len(body_aux.observed_types) == 1
        body_type = body_aux.observed_types[0]
        assert len(orelse_aux.observed_types) == 1
        orelse_type = orelse_aux.observed_types[0]
        return paa.Result[SynthAux](
            tree = pas.make_IfExp(
                body_tree, comment_a_tree, comment_b_tree, 
                test_tree, comment_c_tree, comment_d_tree, orelse_tree),
            aux = update_SynthAux(test_aux,
                observed_types=(unionize_types(body_type, orelse_type),)
            )
        )


    # synthesize: dictionary_item <-- Field
    def synthesize_for_dictionary_item_Field(self, 
        inher_aux : InherAux,
        key_tree : pas.expr, 
        key_aux : SynthAux,
        pre_comment_tree : str, 
        pre_comment_aux : SynthAux,
        post_comment_tree : str, 
        post_comment_aux : SynthAux,
        content_tree : pas.expr, 
        content_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        assert len(key_aux.observed_types) == 1
        key_type = key_aux.observed_types[0]
        assert len(content_aux.observed_types) == 1
        content_type = content_aux.observed_types[0]
        return paa.Result[SynthAux](
            tree = pas.make_Field(key_tree, pre_comment_tree, post_comment_tree, content_tree),
            aux = update_SynthAux(self.synthesize_auxes((key_aux, content_aux)),
                observed_types = (key_type, content_type)
            ) 
        )

    # synthesize: expr <-- Dictionary
    def synthesize_for_expr_Dictionary(self, 
        inher_aux : InherAux,
        content_tree : pas.dictionary_content, 
        content_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        dict_type = make_DictLitType(
            pair_types = tuple(
                (content_aux.observed_types[i], content_aux.observed_types[i + 1])
                for i in range(0, int(len(content_aux.observed_types)), 2)
            )
        )

        return paa.Result[SynthAux](
            tree = pas.make_Dictionary(content_tree),
            aux = update_SynthAux(content_aux,
                observed_types = (dict_type,)
            )
        )
    
    # synthesize: expr <-- EmptyDictionary
    def synthesize_for_expr_EmptyDictionary(self, 
        inher_aux : InherAux
    ) -> paa.Result[SynthAux]:

        dict_type = make_RecordType(
            class_key = "builtins.dict",
            type_args = (AnyType(), AnyType())
        )

        return paa.Result[SynthAux](
            tree = pas.make_EmptyDictionary(),
            aux = make_SynthAux(
                observed_types = (dict_type,) 
            )
        )


    # synthesize: expr <-- Set
    def synthesize_for_expr_Set(self, 
        inher_aux : InherAux,
        content_tree : pas.comma_exprs, 
        content_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        assert len(content_aux.observed_types) > 0

        item_type = content_aux.observed_types[0] 
        for t in content_aux.observed_types[1:]:
            item_type = unionize_types(item_type, t)

        set_type = make_RecordType(
            class_key = "builtins.set",
            type_args = (item_type,)
        )

        return paa.Result[SynthAux](
            tree = pas.make_Set(content_tree),
            aux = update_SynthAux(content_aux,
                observed_types = (set_type,)
            )
        )

    # synthesize: constraint <-- AsyncConstraint
    def synthesize_for_constraint_AsyncConstraint(self, 
        inher_aux : InherAux,
        comment_a_tree : str, 
        comment_a_aux : SynthAux,
        target_tree : pas.expr, 
        target_aux : SynthAux,
        comment_b_tree : str, 
        comment_b_aux : SynthAux,
        comment_c_tree : str, 
        comment_c_aux : SynthAux,
        search_space_tree : pas.expr, 
        search_space_aux : SynthAux,
        comment_d_tree : str, 
        comment_d_aux : SynthAux,
        filts_tree : pas.constraint_filters, 
        filts_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        assert len(search_space_aux.observed_types) == 1
        search_space_type = search_space_aux.observed_types[0]

        item_env = self.unify_iteration(inher_aux, target_tree, search_space_type)
        return paa.Result[SynthAux](
            tree = pas.make_AsyncConstraint(
                comment_a_tree, 
                target_tree, 
                comment_b_tree, 
                comment_c_tree, 
                search_space_tree, 
                comment_d_tree, 
                filts_tree),
            aux = update_SynthAux(self.synthesize_auxes((target_aux, search_space_aux, filts_aux)),
                decl_additions = iom(*(
                    (k, make_Declaration(updatable=None, initialized=True, type=t))
                    for k, t in item_env.items()
                ))
            )
        )
    
    # synthesize: constraint <-- Constraint
    def synthesize_for_constraint_Constraint(self, 
        inher_aux : InherAux,
        comment_a_tree : str, 
        comment_a_aux : SynthAux,
        target_tree : pas.expr, 
        target_aux : SynthAux,
        comment_b_tree : str, 
        comment_b_aux : SynthAux,
        comment_c_tree : str, 
        comment_c_aux : SynthAux,
        search_space_tree : pas.expr, 
        search_space_aux : SynthAux,
        comment_d_tree : str, 
        comment_d_aux : SynthAux,
        filts_tree : pas.constraint_filters, 
        filts_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        assert len(search_space_aux.observed_types) == 1
        search_space_type = search_space_aux.observed_types[0]
        item_env = self.unify_iteration(inher_aux, target_tree, search_space_type)
        return paa.Result[SynthAux](
            tree = pas.make_Constraint(
                comment_a_tree, 
                target_tree, 
                comment_b_tree, 
                comment_c_tree, 
                search_space_tree, 
                comment_d_tree, 
                filts_tree),
            aux = update_SynthAux(self.synthesize_auxes((target_aux, search_space_aux, filts_aux)),
                decl_additions = iom(*(
                    (k, make_Declaration(updatable=None, initialized=True, type=t))
                    for k, t in item_env.items()
                ))
            )
        )


    # synthesize: expr <-- ListComp
    def synthesize_for_expr_ListComp(self, 
        inher_aux : InherAux,
        pre_comment_tree : str, 
        pre_comment_aux : SynthAux,
        content_tree : pas.expr, 
        content_aux : SynthAux,
        post_comment_tree : str, 
        post_comment_aux : SynthAux,
        constraints_tree : pas.comprehension_constraints, 
        constraints_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        # analysis needs to pass information from right to left, so must reanalyze left element
        # content_aux = analyze_expr(content_tree, traverse_aux(inher_aux, constraints_aux))
        assert len(content_aux.observed_types) == 1
        content_type = content_aux.observed_types[0]

        return paa.Result[SynthAux](
            tree = pas.make_ListComp(pre_comment_tree, content_tree, post_comment_tree, constraints_tree),
            aux = update_SynthAux(self.synthesize_auxes((content_aux, constraints_aux)),
                observed_types = (make_RecordType(
                    class_key = "builtins.list",
                    type_args = (content_type,)
                ),)
            )
        )
    
    # synthesize: expr <-- SetComp
    def synthesize_for_expr_SetComp(self, 
        inher_aux : InherAux,
        pre_comment_tree : str, 
        pre_comment_aux : SynthAux,
        content_tree : pas.expr, 
        content_aux : SynthAux,
        post_comment_tree : str, 
        post_comment_aux : SynthAux,
        constraints_tree : pas.comprehension_constraints, 
        constraints_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        # analysis needs to pass information from right to left, so must reanalyze left element
        # TODO: replace this second pass with propagating expectations from left to right
        # content_aux = analyze_expr(content_tree, traverse_aux(inher_aux, constraints_aux))
        assert len(content_aux.observed_types) == 1
        content_type = content_aux.observed_types[0]

        return paa.Result[SynthAux](
            tree = pas.make_SetComp(pre_comment_tree, content_tree, post_comment_tree, constraints_tree),
            aux = update_SynthAux(self.synthesize_auxes((content_aux, constraints_aux)),
                observed_types = (make_RecordType(
                    class_key = "builtins.set",
                    type_args = (content_type,)
                ),)
            )
        )
    
    # synthesize: expr <-- DictionaryComp
    def synthesize_for_expr_DictionaryComp(self, 
        inher_aux : InherAux,
        comment_a_tree : str, 
        comment_a_aux : SynthAux,
        key_tree : pas.expr, 
        key_aux : SynthAux,
        comment_b_tree : str, 
        comment_b_aux : SynthAux,
        comment_c_tree : str, 
        comment_c_aux : SynthAux,
        content_tree : pas.expr, 
        content_aux : SynthAux,
        comment_d_tree : str, 
        comment_d_aux : SynthAux,
        constraints_tree : pas.comprehension_constraints, 
        constraints_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        # analysis needs to pass information from right to left, so must reanalyze left element

        # TODO: replace this second pass with propagating expectations from left to right
        # key_aux = analyze_expr(key_tree, traverse_aux(inher_aux, constraints_aux))
        # content_aux = analyze_expr(content_tree, traverse_aux(inher_aux, constraints_aux))
        assert len(key_aux.observed_types) == 1
        key_type = key_aux.observed_types[0]
        assert len(content_aux.observed_types) == 1
        content_type = content_aux.observed_types[0]

        return paa.Result[SynthAux](
            tree = pas.make_DictionaryComp(
                comment_a_tree, 
                key_tree, 
                comment_b_tree, 
                comment_c_tree, 
                content_tree, 
                comment_d_tree, 
                constraints_tree
            ),
            aux = update_SynthAux(self.synthesize_auxes((key_aux, content_aux, constraints_aux)),
                observed_types = (make_RecordType(
                    class_key = "builtins.dict",
                    type_args = (key_type, content_type)
                ),)
            )
        )
    
    # synthesize: expr <-- GeneratorExp
    def synthesize_for_expr_GeneratorExp(self, 
        inher_aux : InherAux,
        pre_comment_tree : str, 
        pre_comment_aux : SynthAux,
        content_tree : pas.expr, 
        content_aux : SynthAux,
        post_comment_tree : str, 
        post_comment_aux : SynthAux,
        constraints_tree : pas.comprehension_constraints, 
        constraints_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        # analysis needs to pass information from right to left, so must reanalyze left element
        # content_aux = analyze_expr(content_tree, traverse_aux(inher_aux, constraints_aux))
        assert len(content_aux.observed_types) == 1
        content_type = content_aux.observed_types[0]

        return paa.Result[SynthAux](
            tree = pas.make_GeneratorExp(pre_comment_tree, content_tree, post_comment_tree, constraints_tree),
            aux = update_SynthAux(self.synthesize_auxes((content_aux, constraints_aux)),
                observed_types = (make_RecordType(
                    class_key = "typing.Generator",
                    type_args = (content_type, NoneType(), NoneType())
                ),)
            )
        )

    
    # synthesize: expr <-- Await
    def synthesize_for_expr_Await(self, 
        inher_aux : InherAux,
        comment_tree : str, 
        comment_aux : SynthAux,
        content_tree : pas.expr, 
        content_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        # TODO: inferred type
        # check that content_aux.inferred type is subtype of Awaitable[T]
        # async functions return instances of Coroutine <: Awaitable
        # inferred_type = T
        return paa.Result[SynthAux](
            tree = pas.make_Await(comment_tree, content_tree),
            aux = self.synthesize_auxes((content_aux,)) 
        )
    
    # synthesize: expr <-- YieldNothing
    def synthesize_for_expr_YieldNothing(self, 
        inher_aux : InherAux
    ) -> paa.Result[SynthAux]:
        # TODO: inferred type
        # set yield_type to None in synth_aux
        # at function definition record return type as be a Generator <: Iterator <: Iterable 
        return paa.Result[SynthAux](
            tree = pas.make_YieldNothing(),
            aux = make_SynthAux(
                yield_types = (NoneType(),)
            )
        )
    
    # synthesize: expr <-- Yield
    def synthesize_for_expr_Yield(self, 
        inher_aux : InherAux,
        comment_tree : str, 
        comment_aux : SynthAux,
        content_tree : pas.expr, 
        content_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        # at function definition record return type as be a Generator <: Iterator <: Iterable 
        assert len(content_aux.observed_types) == 1
        expr_type = content_aux.observed_types[0]
        return paa.Result[SynthAux](
            tree = pas.make_Yield(comment_tree, content_tree),
            aux = update_SynthAux(content_aux,
                yield_types = (expr_type,)
            )
        )
    
    # synthesize: expr <-- YieldFrom
    def synthesize_for_expr_YieldFrom(self, 
        inher_aux : InherAux,
        comment_a_tree : str, 
        comment_a_aux : SynthAux,
        comment_b_tree : str, 
        comment_b_aux : SynthAux,
        content_tree : pas.expr, 
        content_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        assert len(content_aux.observed_types) == 1
        expr_type = content_aux.observed_types[0]
        item_type = self.get_iterable_item_type(expr_type, inher_aux)

        self.check(IterateTypeCheck(), lambda: item_type != None)

        return paa.Result[SynthAux](
            tree = pas.make_YieldFrom(comment_a_tree, comment_b_tree, content_tree),
            aux = update_SynthAux(content_aux,
                yield_types = (item_type or AnyType(),)
            )
        )

    # synthesize: CompareRight
    def synthesize_for_CompareRight(self, 
        inher_aux : InherAux,
        comment_tree : str, 
        comment_aux : SynthAux,
        rator_tree : pas.cmp_rator, 
        rator_aux : SynthAux,
        rand_tree : pas.expr, 
        rand_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        cmp_name = pas.from_cmp_rator_to_method_name(rator_tree)
        return paa.Result[SynthAux](
            tree = pas.make_CompareRight(comment_tree, rator_tree, rand_tree),
            aux = update_SynthAux(self.synthesize_auxes((rator_aux, rand_aux)), 
                cmp_names = (cmp_name,)
            )
        )
    
    # synthesize: expr <-- Compare
    def synthesize_for_expr_Compare(self, 
        inher_aux : InherAux,
        left_tree : pas.expr, 
        left_aux : SynthAux,
        comps_tree : pas.comparisons, 
        comps_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        assert len(left_aux.observed_types) == 1
        left_type = left_aux.observed_types[0]

        return_type = AnyType()
        assert len(comps_aux.observed_types) == len(comps_aux.cmp_names) 
        for i, method_name in enumerate(comps_aux.cmp_names):
            right_type = comps_aux.observed_types[i]
            method_type = lookup_field_type(left_type, method_name, inher_aux)

            if isinstance(method_type, FunctionType):
                precise_method_type, subst_map = check_application_args(
                    [right_type], {}, 
                    method_type, inher_aux
                )

                self.check(ApplyArgTypeCheck(), lambda: precise_method_type != None)
                if precise_method_type:
                    return_type = precise_method_type.return_type

            elif isinstance(method_type, InterType):
                chosen_method_type, _ = self.match_function_type(
                    inher_aux,
                    [right_type], {}, 
                    method_type
                ) 
                self.check(ApplyArgTypeCheck(), lambda: 
                    chosen_method_type != None
                )
                if chosen_method_type:
                    return_type = chosen_method_type.return_type

            # update:
            left_type = right_type

        return paa.Result[SynthAux](
            tree = pas.make_Compare(left_tree, comps_tree),
            aux = update_SynthAux(self.synthesize_auxes((left_aux, comps_aux)),
                observed_types= (return_type,),
                cmp_names = () 
            )
        )
    
    # synthesize: expr <-- Call
    def synthesize_for_expr_Call(self, 
        inher_aux : InherAux,
        func_tree : pas.expr, 
        func_aux : SynthAux,
        comment_tree : str, 
        comment_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        assert len(func_aux.observed_types) == 1
        func_type = func_aux.observed_types[0]
        inferred_type = AnyType() 
        if isinstance(func_type, FunctionType):
            precise_func_type, subst_map = check_application_args((), {}, func_type, inher_aux)
            self.check(ApplyArgTypeCheck(), lambda: precise_func_type != None)
            if precise_func_type:
                inferred_type = precise_func_type.return_type
        elif isinstance(func_type, InterType):
            chosen_func_type, _ = self.match_function_type(inher_aux, (), {}, func_type) 
            self.check(ApplyArgTypeCheck(), lambda: chosen_func_type != None)
            if chosen_func_type:
                inferred_type = chosen_func_type.return_type
        elif isinstance(func_type, TypeType):
            inferred_type = func_type.content 
            self.check(ApplyRatorTypeCheck(), lambda:
                not isinstance(inferred_type, TypeType) and ( 
                    # if ... then ... <-> not ... or ...
                    not isinstance(inferred_type, RecordType) or
                    (
                        cr := infer_class_record(inferred_type, inher_aux),
                        not cr or not cr.protocol
                    )[-1]
                )
            )

        elif isinstance(func_type, AnyType):
            inferred_type = AnyType() 
        else:
            self.check(ApplyRatorTypeCheck(), lambda: False)
            inferred_type = AnyType() 

        decl_additions = func_aux.decl_additions
        if isinstance(func_tree, pas.Attribute):
            content_tree = func_tree.content
            if isinstance(content_tree, pas.Name):
                prev_decl = lookup_declaration(inher_aux, content_tree.content)
                if prev_decl:
                    generlized_content_type = generalize_type(inher_aux, prev_decl.type)
                    decl_additions += iom((content_tree.content, update_Declaration(prev_decl, type = generlized_content_type)))

        return paa.Result[SynthAux](
            tree = pas.make_Call(func_tree, comment_tree),
            aux = update_SynthAux(func_aux,
                observed_types = (inferred_type,)
            )
        )

    # synthesize: keyword <-- NamedKeyword
    def synthesize_for_keyword_NamedKeyword(self, 
        inher_aux : InherAux,
        name_tree : str, 
        name_aux : SynthAux,
        pre_comment_tree : str, 
        pre_comment_aux : SynthAux,
        post_comment_tree : str, 
        post_comment_aux : SynthAux,
        content_tree : pas.expr, 
        content_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        assert len(content_aux.observed_types) == 1
        content_type = content_aux.observed_types[0]

        return paa.Result[SynthAux](
            tree = pas.make_NamedKeyword(name_tree, pre_comment_tree, post_comment_tree, content_tree),
            aux = make_SynthAux(
                kw_types = pmap({name_tree : content_type})
            ) 
        )
    
    # synthesize: keyword <-- SplatKeyword
    def synthesize_for_keyword_SplatKeyword(self, 
        inher_aux : InherAux,
        comment_tree : str, 
        comment_aux : SynthAux,
        content_tree : pas.expr, 
        content_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        assert len(content_aux.observed_types) == 1
        content_type = content_aux.observed_types[0]

        kw_types = pmap({})
        if isinstance(content_type, DictLitType):
            for kt, vt in content_type.pair_types:
                if isinstance(kt, StrLitType):
                    kw_types += pmap({literal_eval(kt.literal) : vt})
                else:
                    self.check(SplatKeywordArgTypeCheck(), lambda: 
                        subsumed(kt, make_RecordType("builtins.str"), inher_aux)
                    )
        else:
            (key_type, _) = self.get_mapping_key_value_types(content_type, inher_aux)

            self.check(SplatKeywordArgTypeCheck(), lambda: 
                subsumed(key_type, make_RecordType("builtins.str"), inher_aux)
            )

        return paa.Result[SynthAux](
            tree = pas.make_SplatKeyword(comment_tree, content_tree),
            aux = make_SynthAux(
                kw_types = kw_types
            ) 
        )
    
    # synthesize: expr <-- CallArgs
    def synthesize_for_expr_CallArgs(self, 
        inher_aux : InherAux,
        func_tree : pas.expr, 
        func_aux : SynthAux,
        comment_tree : str, 
        comment_aux : SynthAux,
        args_tree : pas.arguments, 
        args_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        expr_type = AnyType() 
        subst_map = m()
        assert len(func_aux.observed_types) == 1
        func_type = func_aux.observed_types[0]
        if isinstance(func_type, FunctionType):

            precise_func_type, subst_map = check_application_args(
                args_aux.observed_types,
                args_aux.kw_types, 
                func_type, inher_aux
            )

            self.check(ApplyArgTypeCheck(), lambda: 
                precise_func_type != None
            )

            if precise_func_type:
                if func_type.static_key == "collections.namedtuple":
                    name_type = args_aux.observed_types[0]
                    fields_type = args_aux.observed_types[1]

                    name = (
                        literal_eval(name_type.literal)
                        if isinstance(name_type, StrLitType) else
                        ''
                    )

                    fields = (
                        (literal_eval(fields_type.literal),)
                        if isinstance(fields_type, StrLitType) else
                        tuple(
                            (
                                literal_eval(fd.literal)
                                if isinstance(fd, StrLitType) else
                                ''
                            )
                            for fd in fields_type.item_types
                        )
                        if isinstance(fields_type, TupleLitType) else
                        tuple(
                            (
                                literal_eval(fd.literal)
                                if isinstance(fd, StrLitType) else
                                ''
                            )
                            for fd in fields_type.item_types
                        )
                        if isinstance(fields_type, ListLitType) else
                        ('',)
                    )

                    expr_type = TypeType(NamedTupleType(name, fields))
                else:
                    expr_type = precise_func_type.return_type

        elif isinstance(func_type, InterType):

            chosen_func_type, subst_map = self.match_function_type(inher_aux,
                args_aux.observed_types,
                args_aux.kw_types, 
                func_type
            ) 
            self.check(ApplyArgTypeCheck(), lambda: chosen_func_type != None)
            if chosen_func_type:
                expr_type = chosen_func_type.return_type

        elif isinstance(func_type, TypeType):
            content_type = func_type.content

            self.check(ApplyRatorTypeCheck(), lambda: 
                # if ... then ...
                not isinstance(content_type, RecordType) or
                (
                    cr := infer_class_record(content_type, inher_aux),
                    not cr or not cr.protocol
                )[-1]
            )

            class_key = get_class_key(content_type)

            if isinstance(content_type, NamedTupleType): 
                expr_type = content_type 
                required_len = len(content_type.fields)

                pos_len = len(args_aux.observed_types)
                keys = set(args_aux.kw_types.keys())
                self.check(ApplyArgTypeCheck(), lambda: 
                    (not pos_len > 0 or (len(keys) == 0 and required_len == pos_len)) and
                    (not len(keys) > 0 or (pos_len == 0 and required_len == len(keys)))
                )

            elif class_key == "builtins.type": 
                expr_type = TypeType(args_aux.observed_types[0])

            elif class_key == "typing.TypeVar": 

                pos_arg_types = args_aux.observed_types
                kw_arg_types = args_aux.kw_types

                local_name = ""
                if len(pos_arg_types) > 0: 
                    name_type = pos_arg_types[0]
                    assert isinstance(name_type, StrLitType) 
                    local_name = literal_eval(name_type.literal)
                else:
                    name_type = kw_arg_types["name"]
                    assert isinstance(name_type, StrLitType) 
                    local_name = literal_eval(name_type.literal)


                variant = NoVariant()
                assert not (
                    isinstance(kw_arg_types.get("covariant"), TrueType) and
                    isinstance(kw_arg_types.get("contravariant"), TrueType)
                )

                if isinstance(kw_arg_types.get("covariant"), TrueType):
                    variant = CoVariant()
                elif isinstance(kw_arg_types.get("contravariant"), TrueType):
                    variant = ContraVariant()


                full_name = (
                    f"{inher_aux.external_path}.{inher_aux.internal_path}.{local_name}"
                    if inher_aux.internal_path else
                    f"{inher_aux.external_path}.{local_name}"
                )
            
                expr_type = TypeType(content = make_VarType(name = full_name, variant = variant))
            else:

                class_key = get_class_key(func_type.content)
                class_record = from_static_path_to_ClassRecord(inher_aux, class_key)

                expr_type = func_type.content 
                if class_record:

                    constructor_type = lookup_constructor_type(class_record, inher_aux)

                    if isinstance(constructor_type, FunctionType):
                        precise_init_type, subst_map = check_application_args(
                            args_aux.observed_types,
                            args_aux.kw_types, 
                            constructor_type, inher_aux
                        )

                        self.check(ApplyArgTypeCheck(), lambda: 
                            precise_init_type != None
                        )

                        expr_type = substitute_type_args(func_type.content, subst_map)

                    elif isinstance(constructor_type, InterType):
                        chosen_func_type, subst_map = self.match_function_type(
                            inher_aux, 
                            args_aux.observed_types,
                            args_aux.kw_types, 
                            constructor_type
                        ) 
                        self.check(ApplyArgTypeCheck(), lambda: chosen_func_type != None)
                        expr_type = substitute_type_args(func_type.content, subst_map)

                    else:
                        assert isinstance(constructor_type, AnyType) or constructor_type == None

        else:
            self.check(ApplyRatorTypeCheck(), lambda:isinstance(func_type,AnyType))
            expr_type = AnyType()


        synth_aux = self.synthesize_auxes((func_aux, args_aux))

        decl_additions = synth_aux.decl_additions

        if isinstance(func_tree, pas.Attribute):
            content_tree = func_tree.content
            if isinstance(content_tree, pas.Name):
                prev_decl = lookup_declaration(inher_aux, content_tree.content)
                if prev_decl:
                    generlized_content_type = substitute_type_args(generalize_type(inher_aux, prev_decl.type), subst_map)
                    decl_additions += iom((content_tree.content, update_Declaration(prev_decl, type = generlized_content_type)))

        return paa.Result[SynthAux](
            tree = pas.make_CallArgs(func_tree, comment_tree, args_tree),
            aux = update_SynthAux(synth_aux,
                observed_types = (expr_type,),
                decl_additions = decl_additions
            )
        )
    
    # synthesize: expr <-- Integer
    def synthesize_for_expr_Integer(self, 
        inher_aux : InherAux,
        content_tree : str, 
        content_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        return paa.Result[SynthAux](
            tree = pas.make_Integer(content_tree),
            aux = update_SynthAux(content_aux,
                observed_types = (IntLitType(literal = content_tree),)
            )
        )
    
    # synthesize: expr <-- Float
    def synthesize_for_expr_Float(self, 
        inher_aux : InherAux,
        content_tree : str, 
        content_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        return paa.Result[SynthAux](
            tree = pas.make_Float(content_tree),
            aux = update_SynthAux(content_aux,
                observed_types = (FloatLitType(literal = content_tree),)
            )
        )

    # synthesize: sequence_string <-- ConsStr
    def synthesize_for_sequence_string_ConsStr(self, 
        inher_aux : InherAux,
        head_tree : str, 
        head_aux : SynthAux,
        tail_tree : pas.sequence_string, 
        tail_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        expr_type = (
            StrLitType(literal = head_tree)
            if is_literal_string(head_tree) else
            make_RecordType("builtins.str")
        )

        return paa.Result[SynthAux](
            tree = pas.make_ConsStr(head_tree, tail_tree),
            aux = make_SynthAux(
                observed_types = (expr_type,) + tail_aux.observed_types
            )
        )
    
    # synthesize: sequence_string <-- SingleStr
    def synthesize_for_sequence_string_SingleStr(self, 
        inher_aux : InherAux,
        content_tree : str, 
        content_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        expr_type = (
            StrLitType(literal = content_tree)
            if is_literal_string(content_tree) else
            make_RecordType("builtins.str")
        )
        return paa.Result[SynthAux](
            tree = pas.make_SingleStr(content_tree),
            aux = make_SynthAux(
                observed_types = (expr_type,)
            ) 
        )
    
    # synthesize: expr <-- ConcatString
    def synthesize_for_expr_ConcatString(self, 
        inher_aux : InherAux,
        content_tree : pas.sequence_string, 
        content_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        assert len(content_aux.observed_types) > 0

        expr_type = (
            content_aux.observed_types[0]
            if len(content_aux.observed_types) == 1 else 
            make_RecordType("builtins.str")
        )

        return paa.Result[SynthAux](
            tree = pas.make_ConcatString(content_tree),
            aux = update_SynthAux(content_aux,
                observed_types = (expr_type,)
            )
        )
    
    # synthesize: expr <-- True_
    def synthesize_for_expr_True_(self, 
        inher_aux : InherAux
    ) -> paa.Result[SynthAux]:
        return paa.Result[SynthAux](
            tree = pas.make_True_(),
            aux = make_SynthAux(
                observed_types = (TrueType(),)
            )
        )
    
    # synthesize: expr <-- False_
    def synthesize_for_expr_False_(self, 
        inher_aux : InherAux
    ) -> paa.Result[SynthAux]:
        return paa.Result[SynthAux](
            tree = pas.make_False_(),
            aux = make_SynthAux(
                observed_types = (FalseType(),)
            )
        )
    
    # synthesize: expr <-- None_
    def synthesize_for_expr_None_(self, 
        inher_aux : InherAux
    ) -> paa.Result[SynthAux]:
        return paa.Result[SynthAux](
            tree = pas.make_None_(),
            aux = make_SynthAux(
                observed_types = (NoneType(),)
            )
        )

    # synthesize: expr <-- Ellip
    def synthesize_for_expr_Ellip(self, 
        inher_aux : InherAux
    ) -> paa.Result[SynthAux]:
        return paa.Result[SynthAux](
            tree = pas.make_Ellip(),
            aux = make_SynthAux(
                observed_types = (EllipType(),)
            )
        )
    
    # synthesize: expr <-- Attribute
    def synthesize_for_expr_Attribute(self, 
        inher_aux : InherAux,
        content_tree : pas.expr, 
        content_aux : SynthAux,
        pre_comment_tree : str, 
        pre_comment_aux : SynthAux,
        post_comment_tree : str, 
        post_comment_aux : SynthAux,
        name_tree : str, 
        name_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        assert len(content_aux.observed_types) == 1
        content_type = content_aux.observed_types[0]


        if isinstance(content_type, AnyType):
            expr_type = AnyType()
        else:
            expr_type = lookup_field_type(content_type, name_tree, inher_aux)
            self.check(LookupTypeCheck(), lambda: 
                expr_type != None
            )
            if not expr_type:
                expr_type = AnyType()
        
        return paa.Result[SynthAux](
            tree = pas.make_Attribute(content_tree, pre_comment_tree, post_comment_tree, name_tree),
            aux = update_SynthAux(self.synthesize_auxes((content_aux, name_aux)),
                observed_types = (expr_type,)
            )
        )

    # synthesize: expr <-- Subscript
    def synthesize_for_expr_Subscript(self, 
        inher_aux : InherAux,
        content_tree : pas.expr, 
        content_aux : SynthAux,
        comment_a_tree : str, 
        comment_a_aux : SynthAux,
        comment_b_tree : str, 
        comment_b_aux : SynthAux,
        slice_tree : pas.expr, 
        slice_aux : SynthAux,
        comment_c_tree : str, 
        comment_c_aux : SynthAux,
    ) -> paa.Result[SynthAux]:

        assert len(content_aux.observed_types) == 1
        content_type = content_aux.observed_types[0]

        assert len(slice_aux.observed_types) == 1
        slice_type = slice_aux.observed_types[0]

        var_types : tuple[VarType, ...] = ()
        expr_types = ()
        protocol : bool = False

        if isinstance(content_type, TypeType):
            core_type = content_type.content
            if isinstance(core_type, ProtocolType):
                protocol = True
            if isinstance(core_type, GenericType) or isinstance(core_type, ProtocolType):
                if isinstance(slice_type, TupleLitType):
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
                class_key = get_class_key(content_type.content)
                expr_types = (from_class_key_to_typetype(inher_aux, class_key, slice_type),)

        else:
            method_type = lookup_field_type(content_type, "__getitem__", inher_aux)
            self.check(LookupTypeCheck(), lambda: 
                method_type != None
            )
            if isinstance(method_type, FunctionType): 

                precise_method_type, subst_map = check_application_args(
                    [slice_type], {}, 
                    method_type, inher_aux
                )

                self.check(ApplyArgTypeCheck(), lambda: 
                    precise_method_type != None
                )

                if precise_method_type and precise_method_type.return_type:
                    expr_types = (precise_method_type.return_type,)

            elif isinstance(method_type, InterType):
                chosen_method_type, _ = self.match_function_type(
                    inher_aux, 
                    [slice_type], {}, 
                    method_type
                ) 
                self.check(ApplyArgTypeCheck(), lambda: chosen_method_type != None)
                if chosen_method_type:
                    expr_types = (chosen_method_type.return_type,)

            else:
                expr_types = (AnyType(),)

        return paa.Result[SynthAux](
            tree = pas.make_Subscript(content_tree, comment_a_tree, comment_b_tree, slice_tree, comment_c_tree),
            aux = update_SynthAux(self.synthesize_auxes((content_aux, slice_aux)),
                observed_types = expr_types, 
                var_types = var_types, 
                protocol = protocol
            )
        )

    # synthesize: expr <-- Slice
    def synthesize_for_expr_Slice(self, 
        inher_aux : InherAux,
        lower_tree : pas.option_expr, 
        lower_aux : SynthAux,
        comment_a_tree : str, 
        comment_a_aux : SynthAux,
        comment_b_tree : str, 
        comment_b_aux : SynthAux,
        upper_tree : pas.option_expr, 
        upper_aux : SynthAux,
        comment_c_tree : str, 
        comment_c_aux : SynthAux,
        comment_d_tree : str, 
        comment_d_aux : SynthAux,
        step_tree : pas.option_expr, 
        step_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        return paa.Result[SynthAux](
            tree = pas.make_Slice(lower_tree, comment_a_tree, comment_b_tree, upper_tree, comment_c_tree, comment_d_tree, step_tree),
            aux = update_SynthAux(self.synthesize_auxes((lower_aux, upper_aux, step_aux)),
                observed_types = (make_RecordType("builtins.slice"),)
            )
        )
    
    
    # synthesize: expr <-- Name
    def synthesize_for_expr_Name(self, 
        inher_aux : InherAux,
        content_tree : str, 
        content_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        # TODO: update to apply decorators from environment when inferring type
        id = content_tree

        expr_dec = lookup_declaration(inher_aux, id)
        assert expr_dec

        protocol = False
        types = ()


        expr_type = expr_dec.type
        if isinstance(expr_type, TypeType):
            content_type =  expr_type.content
            if isinstance(content_type, ProtocolType):
                protocol = True

        types = (expr_type,)

        backref = (
            id in inher_aux.local_env or
            id in inher_aux.nonlocal_env or
            id in inher_aux.global_env
        )

        return paa.Result[SynthAux](
            tree = pas.make_Name(content_tree),
            aux = make_SynthAux(
                observed_types = types,
                protocol = protocol,
                usage_additions = pmap({content_tree : make_Usage(backref)})
            )
        )
    
    # synthesize: expr <-- List
    def synthesize_for_expr_List(self, 
        inher_aux : InherAux,
        content_tree : pas.comma_exprs, 
        content_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        assert len(content_aux.observed_types) > 0

        list_type = ListLitType(content_aux.observed_types)
        return paa.Result[SynthAux](
            tree = pas.make_List(content_tree),
            aux = update_SynthAux(content_aux,
                observed_types = (list_type,),
            )
        )
    
    # synthesize: expr <-- EmptyList
    def synthesize_for_expr_EmptyList(self, 
        inher_aux : InherAux
    ) -> paa.Result[SynthAux]:
        return paa.Result[SynthAux](
            tree = pas.make_EmptyList(),
            aux = make_SynthAux(
                observed_types = (make_RecordType(
                    class_key = "builtins.list",
                    type_args=(AnyType(),)
                ),)
            )
        )

    # synthesize: expr <-- Tuple
    def synthesize_for_expr_Tuple(self, 
        inher_aux : InherAux,
        content_tree : pas.comma_exprs, 
        content_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        content_types = content_aux.observed_types
        assert len(content_types) > 0
        tuple_type = make_TupleLitType(
            item_types = content_types 
        )
        return paa.Result[SynthAux](
            tree = pas.make_Tuple(content_tree),
            aux = update_SynthAux(content_aux,
                observed_types = (tuple_type,),
            )
        )
    
    # synthesize: expr <-- EmptyTuple
    def synthesize_for_expr_EmptyTuple(self, 
        inher_aux : InherAux
    ) -> paa.Result[SynthAux]:
        return paa.Result[SynthAux](
            tree = pas.make_EmptyTuple(),
            aux = make_SynthAux(
                observed_types = (TupleLitType(
                    item_types=()
                ),)
            )
        )

    # synthesize: expr <-- Starred
    def synthesize_for_expr_Starred(self, 
        inher_aux : InherAux,
        content_tree : pas.expr, 
        content_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        # splat the observed type

        observed_type = content_aux.observed_types[0]
        if isinstance(observed_type, ListLitType):
            splatted_types = observed_type.item_types
        elif isinstance(observed_type, TupleLitType):
            splatted_types = observed_type.item_types
        else:
            # cannot statically splat
            splatted_types = (observed_type,)

        return paa.Result[SynthAux](
            tree = pas.make_Starred(content_tree),
            aux = update_SynthAux(content_aux,
                observed_types=splatted_types
            )
        )

    # synthesize: module <-- FutureMod
    def synthesize_for_module_FutureMod(self, 
        inher_aux : InherAux,
        names_tree : pas.sequence_import_name, 
        names_aux : SynthAux,
        body_tree : pas.statements, 
        body_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        self.check(LookupDecCheck(), lambda: (
            nested_usages := self.update_nested_usages(
                body_aux.decl_additions, 
                body_aux.usage_additions, 
                body_aux.nested_usages
            ),
            us.every(nested_usages, lambda sym : 
                not isinstance(
                    from_static_path_to_declaration(inher_aux, f"builtins.{sym}"), 
                    AnyType
                )
            )
        )[-1])

        return paa.Result[SynthAux](
            tree = pas.make_FutureMod(names_tree, body_tree),
            aux = body_aux 
        )
        

    # synthesize: module <-- SimpleMod
    def synthesize_for_module_SimpleMod(self, 
        inher_aux : InherAux,
        body_tree : pas.statements, 
        body_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        nested_usages = self.update_nested_usages(
            body_aux.decl_additions, 
            body_aux.usage_additions, 
            body_aux.nested_usages
        )


        self.check(LookupDecCheck(), lambda:
            # any unmatched usages should be matched with definitions in standard lib
            all(
                not isinstance(dec.type, AnyType)
                for sym in nested_usages
                for dec in [from_static_path_to_declaration(inher_aux, f"builtins.{sym}")]
            )
        )

        return paa.Result[SynthAux](
            tree = pas.make_SimpleMod(body_tree),
            aux = body_aux 
        )


    # synthesize: decorators <-- ConsDec
    def synthesize_for_decorators_ConsDec(self, 
        inher_aux : InherAux,
        head_tree : pas.decorator, 
        head_aux : SynthAux,
        tail_tree : pas.decorators, 
        tail_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        synth_aux = make_SynthAux(
            observed_types = head_aux.observed_types + tail_aux.observed_types
        )
        return paa.Result[SynthAux](
            tree = pas.make_ConsDec(head_tree, tail_tree),
            aux = synth_aux 
        )
    
    # synthesize: stmt <-- DecClassDef
    def synthesize_for_stmt_DecClassDef(self, 
        inher_aux : InherAux,
        decs_tree : pas.decorators, 
        decs_aux : SynthAux,
        class_def_tree : pas.ClassDef, 
        class_def_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        env_additions = iom(*(
            (name, make_Declaration(
                updatable = dec.updatable,
                initialized = dec.initialized, 
                type = dec.type,
                decorator_types = decs_aux.observed_types   
            ))
            for name, dec in class_def_aux.decl_additions.items()
        ))  
        return paa.Result[SynthAux](
            tree = pas.make_DecClassDef(decs_tree, class_def_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([decs_aux, class_def_aux])),
                decl_additions = env_additions
            ) 
        )

    # synthesize: stmt <-- ReturnSomething
    def synthesize_for_stmt_ReturnSomething(self, 
        inher_aux : InherAux,
        content_tree : pas.expr, 
        content_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        assert len(content_aux.observed_types) == 1
        expr_type = content_aux.observed_types[0]

        return paa.Result[SynthAux](
            tree = pas.make_ReturnSomething(content_tree),
            aux = update_SynthAux(content_aux,
                return_types = tuple([expr_type])
            )
        )
    
    # synthesize: stmt <-- Return
    def synthesize_for_stmt_Return(self, 
        inher_aux : InherAux
    ) -> paa.Result[SynthAux]:
        return paa.Result[SynthAux](
            tree = pas.make_Return(),
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
        bs_aux : SynthAux,
        comment_tree : str, 
        comment_aux : SynthAux
    ) -> InherAux:
        if not inher_aux.internal_path:
            return update_InherAux(inher_aux,
                # copy local_decl into global_decl
                global_env = inher_aux.local_env,
                internal_path = name_tree,
                in_class = True
            )
        else:
            return update_InherAux(inher_aux,
                # copy local_decl into nonlocal_decl
                nonlocal_env = inher_aux.nonlocal_env + inher_aux.local_env, 
                internal_path = f"{inher_aux.internal_path}.{name_tree}",
                in_class = True
            )
    
    # synthesize: ClassDef
    def synthesize_for_ClassDef(self, 
        inher_aux : InherAux,
        name_tree : str, 
        name_aux : SynthAux,
        bs_tree : pas.bases, 
        bs_aux : SynthAux,
        comment_tree : str, 
        comment_aux : SynthAux,
        body_tree : pas.statements, 
        body_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        type_params : tuple[VarType, ...] = bs_aux.var_types

        super_types : tuple[TypeType, ...] = tuple(
            coerce_to_TypeType(t, inher_aux)
            for t in bs_aux.observed_types
        )

        internal_class_key = (
            f"{inher_aux.internal_path}.{name_tree}"
            if inher_aux.internal_path else
            name_tree
        )
        class_key = f"{inher_aux.external_path}.{internal_class_key}"

        def expose_static_method_type(name : str, decl : Declaration) -> type:
            decl_type = decl.type
            if isinstance(decl_type, InterType):
                return InterType(type_components=tuple(
                    expose_static_method_type(name, update_Declaration(decl,
                        type = ft
                    ))
                    for ft in decl_type.type_components

                ))
            elif not isinstance(decl.type, FunctionType):
                return decl.type

            for dt in decl.decorator_types:
                if isinstance(dt, TypeType):
                    dt_class_key = get_class_key(dt.content)
                    if dt_class_key == "builtins.staticmethod":
                        return decl.type
                    elif dt_class_key == "builtins.classmethod":
                        return update_FunctionType(decl.type,
                            pos_kw_param_sigs=decl.type.pos_kw_param_sigs[1:]
                        )

            if name == "__init__" or name == "__new__": 

                if len(decl.type.pos_kw_param_sigs) > 0:
                    # first param is for newly constructed self or static cls
                    return update_FunctionType(decl.type,
                        pos_kw_param_sigs=decl.type.pos_kw_param_sigs[1:]
                    )
                else:
                    return decl.type

            elif len(decl.type.pos_kw_param_sigs) == 0:
                return decl.type 
            else:

                # check if type has been partially resolved in previous iteration of analysis
                type_arg = (
                    TypeType(type_params[0])
                    if len(type_params) == 1 else 
                    TupleLitType(tuple(TypeType(t) for t in type_params))
                    if len(type_params) > 1 else
                    None
                ) 
                self_instance_type = from_class_key_to_typetype(inher_aux, class_key, type_arg).content
                self_instance_param_sig = update_ParamSig(decl.type.pos_kw_param_sigs[0], type = self_instance_type)

                return update_FunctionType(decl.type,
                    pos_kw_param_sigs=tuple([self_instance_param_sig]) + decl.type.pos_kw_param_sigs[1:]
                )

        def expose_instance_method_type(p : Declaration) -> Optional[type]:

            p_type = p.type
            if isinstance(p_type, InterType):

                fts = tuple(
                    expose_instance_method_type(update_Declaration(p, type = ft))
                    for ft in p_type.type_components
                )
                if us.exists(fts, lambda ft: ft == None):
                    return None
                fts = tuple(ft for ft in fts if ft != None) 

                return InterType(type_components=fts)

            elif not isinstance(p.type, FunctionType):
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


        static_fields : InsertOrderMap[str, type] = iom(*(
            (name, expose_static_method_type(name, p))
            for name, p in body_aux.decl_additions.items()
        )) + body_aux.static_field_additions

        instance_fields : InsertOrderMap[str, type] = iom(*(
            (k, t)
            for k, p in body_aux.decl_additions.items()
            for t in [expose_instance_method_type(p)]
            if t 
        )) + body_aux.static_field_additions + body_aux.instance_field_additions 

        # TODO: check that covariant type params are only used as outputs
        # TODO: check that contravariant type params are only used as inputs
        class_record = ClassRecord(
            key = class_key,
            type_params = type_params,
            super_types = super_types, # tuple[TypeType, ...]

            static_fields = static_fields, #, PMap[str, type]
            instance_fields = instance_fields, # PMap[str, type]
            protocol = bs_aux.protocol
        )

        type_arg = (
            TupleLitType(item_types=tuple(
                TypeType(content=tp)
                for tp in type_params
            ))
            if bool(type_params) else
            None
        ) 

        typetype = from_class_key_to_typetype(inher_aux, class_record.key, type_arg)

        return paa.Result[SynthAux](
            tree = pas.make_ClassDef(name_tree, bs_tree, comment_tree, body_tree),
            aux = update_SynthAux(body_aux,
                decl_subtractions=s(),
                decl_additions=iom(
                    (name_tree, make_Declaration(
                        updatable=None,
                        initialized=True, 
                        type=typetype
                    ))
                ),
                class_additions=iom((internal_class_key, class_record)) + body_aux.class_additions
            ) 
        )

    # traverse stmt <-- DecFunctionDef"
    def traverse_stmt_DecFunctionDef_fun_def(self, 
        inher_aux : InherAux,
        decs_tree : pas.decorators, 
        decs_aux : SynthAux
    ) -> InherAux:
        method_kind = method_kind_from_decorators([ 
            d.type
            for d in decs_aux.decl_additions.values()
        ])

        return update_InherAux(inher_aux,
            local_env = (
                iom() 
                if inher_aux.in_class else
                inher_aux.local_env
            ),
            method_kind = (
                method_kind
                if inher_aux.in_class else
                None
            )
        )

    # synthesize: stmt <-- DecFunctionDef
    def synthesize_for_stmt_DecFunctionDef(self, 
        inher_aux : InherAux,
        decs_tree : pas.decorators, 
        decs_aux : SynthAux,
        fun_def_tree : pas.function_def, 
        fun_def_aux : SynthAux
    ) -> paa.Result[SynthAux]:


        fun_decls = fun_def_aux.decl_additions.items()
        assert len(fun_def_aux.decl_additions.keys()) == 1

        (name, decl) = next(p for p in fun_decls)
        assert not decl.updatable

        ####### update overloaded type 
        prev_decl = inher_aux.local_env.get(name)
        assert not prev_decl or not prev_decl.overloading or isinstance(prev_decl.type, InterType)

        if us.exists(decs_aux.observed_types, lambda dt :
            isinstance(dt, OverloadType)
        ):

            overloaded_types = (
                prev_decl.type.type_components + (decl.type,)
                if prev_decl and prev_decl.overloading and isinstance(prev_decl.type, InterType) else 
                (decl.type,)
            ) 

            decl = update_Declaration(decl,
                updatable=None,
                # type = AnyType(), 
                type = InterType(type_components=overloaded_types), 
                decorator_types = (prev_decl and prev_decl.decorator_types or ()) + decs_aux.observed_types,
                overloading = True
            )

        else:
            if prev_decl and prev_decl.overloading:
                # TODO: check that prev_decl.types' params and return types subsume decl.type's params and return types
                decl = update_Declaration(decl,
                    # type = AnyType(), 
                    type = prev_decl.type,
                    updatable=None,
                    decorator_types = decs_aux.observed_types,
                    overloading = False
                )
            else:
                decl = update_Declaration(decl,
                    decorator_types = decs_aux.observed_types,
                    overloading = False
                )
        #######





        return paa.Result[SynthAux](
            tree = pas.make_DecFunctionDef(decs_tree, fun_def_tree),
            aux = update_SynthAux(fun_def_aux,
                decl_additions = iom((name, decl))
            ) 
        )

    # traverse function_def <-- FunctionDef"
    def traverse_function_def_FunctionDef_ret_anno(self, 
        inher_aux : InherAux,
        name_tree : str, 
        name_aux : SynthAux,
        params_tree : pas.parameters, 
        params_aux : SynthAux
    ) -> InherAux:
        return inher_aux 

    # traverse: function_def <-- FunctionDef
    def traverse_function_def_FunctionDef_body(self, 
        inher_aux : InherAux,
        name_tree : str, 
        name_aux : SynthAux,
        params_tree : pas.parameters, 
        params_aux : SynthAux,
        ret_anno_tree : pas.return_annotation, 
        ret_anno_aux : SynthAux,
        comment_tree : str, 
        comment_aux : SynthAux
    ) -> InherAux:
        assert len(params_aux.decl_subtractions) == 0
        inher_aux = traverse_function_body(inher_aux, name_tree, get_first_param(params_tree))
        return update_InherAux(inher_aux, local_env = inher_aux.local_env + params_aux.decl_additions) 

    # traverse function_def <-- AsyncFunctionDef"
    def traverse_function_def_AsyncFunctionDef_ret_anno(self, 
        inher_aux : InherAux,
        name_tree : str, 
        name_aux : SynthAux,
        params_tree : pas.parameters, 
        params_aux : SynthAux
    ) -> InherAux:
        return inher_aux 

    # traverse: function_def <-- AsyncFunctionDef
    def traverse_function_def_AsyncFunctionDef_body(self, 
        inher_aux : InherAux,
        name_tree : str, 
        name_aux : SynthAux,
        params_tree : pas.parameters, 
        params_aux : SynthAux,
        ret_anno_tree : pas.return_annotation, 
        ret_anno_aux : SynthAux,
        comment_tree : str, 
        comment_aux : SynthAux
    ) -> InherAux:
        assert len(params_aux.decl_subtractions) == 0
        inher_aux = traverse_function_body(inher_aux, name_tree, get_first_param(params_tree))
        return update_InherAux(inher_aux, local_env = inher_aux.local_env + params_aux.decl_additions) 

    

    
    # synthesize: function_def <-- FunctionDef
    def synthesize_for_function_def_FunctionDef(self, 
        inher_aux : InherAux,
        name_tree : str, 
        name_aux : SynthAux,
        params_tree : pas.parameters, 
        params_aux : SynthAux,
        ret_anno_tree : pas.return_annotation, 
        ret_anno_aux : SynthAux,
        comment_tree : str, 
        comment_aux : SynthAux,
        body_tree : pas.statements, 
        body_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        function_body_return_type = (
            make_RecordType(
                class_key = "typing.Generator",
                type_args = (
                    unionize_all_types(body_aux.yield_types),
                    NoneType(),
                    (
                        unionize_all_types(body_aux.yield_types)
                        if len(body_aux.return_types) > 0 else
                        NoneType()
                    )
                )
            )
            if len(body_aux.yield_types) > 0 else
            unionize_all_types(body_aux.return_types)
            if len(body_aux.return_types) > 0 else
            NoneType()
        )

        if isinstance(ret_anno_tree, pas.SomeReturnAnno): 
            assert len(ret_anno_aux.observed_types) == 1
            function_sig_return_type = coerce_to_TypeType(ret_anno_aux.observed_types[0], inher_aux).content

            self.check(ReturnTypeCheck(), lambda: 
                is_a_stub_body(body_tree) or
                subsumed(function_body_return_type, function_sig_return_type, inher_aux)
            )

            function_return_type = function_sig_return_type
        else:
            function_return_type = function_body_return_type

        type = FunctionType(
            static_key = (
                f"{inher_aux.external_path}.{inher_aux.internal_path}.{name_tree}"
                if inher_aux.internal_path else
                f"{inher_aux.external_path}.{name_tree}"
            ),
            pos_param_types = params_aux.pos_param_types,
            pos_kw_param_sigs = params_aux.pos_kw_param_sigs,
            bundle_pos_param_type = params_aux.bundle_pos_param_type,
            kw_param_sigs = params_aux.kw_param_sigs,
            bundle_kw_param_type = params_aux.bundle_kw_param_type,
            return_type = function_return_type 
        )

        nested_usages = self.update_nested_usages(body_aux.decl_additions, body_aux.usage_additions, body_aux.nested_usages)

        if (
            inher_aux.external_path == "typing" and
            name_tree == 'overload'
        ):
            type = OverloadType()

        return paa.Result[SynthAux](
            tree = pas.make_FunctionDef(name_tree, params_tree, ret_anno_tree, comment_tree, body_tree),
            aux = make_SynthAux(
                decl_subtractions = s(),
                decl_additions = iom((name_tree, make_Declaration(
                    updatable=None, initialized = True, type = type)
                )),
                usage_additions=m(),
                nested_usages=nested_usages
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
        comment_tree : str, 
        comment_aux : SynthAux,
        body_tree : pas.statements, 
        body_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        # TODO: follow FunctionDef but return a CoroutineType 

        nested_usages = self.update_nested_usages(body_aux.decl_additions, body_aux.usage_additions, body_aux.nested_usages)

        return paa.Result[SynthAux](
            tree = pas.make_AsyncFunctionDef(name_tree, params_tree, ret_anno_tree, comment_tree, body_tree),
            aux = make_SynthAux(
                decl_subtractions = s(),
                decl_additions = iom((name_tree, make_Declaration(
                    updatable=None,
                    initialized=True
                ))),
                usage_additions=m(),
                nested_usages=nested_usages
            ) 
        )

    # synthesize: Param 
    def synthesize_for_Param(self, 
        inher_aux : InherAux,
        comment_tree : str, 
        comment_aux : SynthAux,
        name_tree : str, 
        name_aux : SynthAux,
        anno_tree : pas.param_annotation, 
        anno_aux : SynthAux,
        default_tree : pas.param_default, 
        default_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        sig_type = (
            coerce_to_TypeType(anno_aux.observed_types[0], inher_aux).content
            if len(anno_aux.observed_types) == 1 else 
            default_aux.observed_types[0]
            if len(default_aux.observed_types) == 1 else 
            AnyType()
        )

        if len(default_aux.observed_types) > 0:
            default_type = default_aux.observed_types[0]
            self.check(AssignTypeCheck(), lambda: 
                subsumed(default_type, sig_type, inher_aux)
            )

        return paa.Result[SynthAux](
            tree = pas.make_Param(comment_tree, name_tree, anno_tree, default_tree),

            aux = make_SynthAux(
                decl_additions = iom((name_tree, make_Declaration(
                    updatable = sig_type,
                    initialized=True, 
                    type=sig_type
                ))),

                param_sig = ParamSig(
                    key = name_tree, 
                    type = sig_type,
                    optional = isinstance(default_tree, pas.SomeParamDefault)  
                )
            )
        )

    
    # synthesize: parameters_d <-- ConsKwParam
    def synthesize_for_parameters_d_ConsKwParam(self, 
        inher_aux : InherAux,
        pre_comment_tree : str, 
        pre_comment_aux : SynthAux,
        head_tree : pas.Param, 
        head_aux : SynthAux,
        post_comment_tree : str, 
        post_comment_aux : SynthAux,
        tail_tree : pas.parameters_d, 
        tail_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        assert head_aux.param_sig
        return paa.Result[SynthAux](
            tree = pas.make_ConsKwParam(pre_comment_tree, head_tree, post_comment_tree, tail_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([head_aux, tail_aux])),
                kw_param_sigs = (head_aux.param_sig,) + tail_aux.kw_param_sigs
            )
        )
    
    # synthesize: parameters_d <-- SingleKwParam
    def synthesize_for_parameters_d_SingleKwParam(self, 
        inher_aux : InherAux,
        pre_comment_tree : str, 
        pre_comment_aux : SynthAux,
        content_tree : pas.Param, 
        content_aux : SynthAux,
        post_comment_tree : str, 
        post_comment_aux : SynthAux,
    ) -> paa.Result[SynthAux]:

        assert content_aux.param_sig
        return paa.Result[SynthAux](
            tree = pas.make_SingleKwParam(pre_comment_tree, content_tree, post_comment_tree),
            aux = update_SynthAux(content_aux,
                kw_param_sigs = (content_aux.param_sig,)
            )
        )

    # synthesize: parameters_d <-- TransKwParam
    def synthesize_for_parameters_d_TransKwParam(self, 
        inher_aux : InherAux,
        comment_a_tree : str, 
        comment_a_aux : SynthAux,
        head_tree : pas.Param, 
        head_aux : SynthAux,
        comment_b_tree : str, 
        comment_b_aux : SynthAux,
        comment_c_tree : str, 
        comment_c_aux : SynthAux,
        tail_tree : pas.Param, 
        tail_aux : SynthAux,
        comment_d_tree : str, 
        comment_d_aux : SynthAux,
    ) -> paa.Result[SynthAux]:
        assert head_aux.param_sig
        assert tail_aux.param_sig
        return paa.Result[SynthAux](
            tree = pas.make_TransKwParam(
                comment_a_tree,
                head_tree, 
                comment_b_tree,
                comment_c_tree,
                tail_tree,
                comment_d_tree,
            ),
            aux = update_SynthAux(self.synthesize_auxes(tuple([head_aux, tail_aux])),
                kw_param_sigs = (head_aux.param_sig,) + tail_aux.kw_param_sigs,
                bundle_kw_param_type = tail_aux.param_sig.type,
                decl_additions=head_aux.decl_additions + iom(
                    (tail_aux.param_sig.key, make_Declaration(
                        updatable=make_RecordType(
                            class_key = "builtins.dict",
                            type_args=(
                                make_RecordType(class_key="builtins.str"),
                                tail_aux.param_sig.type,
                            )
                        ),
                        initialized = True,
                        type = make_RecordType(
                            class_key = "builtins.dict",
                            type_args=(
                                make_RecordType(class_key="builtins.str"),
                                tail_aux.param_sig.type,
                            )
                        )
                    ))
                )
            )
        )

    # synthesize: parameters_c <-- DoubleBundleParam
    def synthesize_for_parameters_c_DoubleBundleParam(self, 
        inher_aux : InherAux,
        comment_a_tree : str, 
        comment_a_aux : SynthAux,
        tuple_param_tree : pas.Param, 
        tuple_param_aux : SynthAux,
        comment_b_tree : str, 
        comment_b_aux : SynthAux,
        comment_c_tree : str, 
        comment_c_aux : SynthAux,
        dict_param_tree : pas.Param, 
        dict_param_aux : SynthAux,
        comment_d_tree : str, 
        comment_d_aux : SynthAux,
    ) -> paa.Result[SynthAux]:
        assert tuple_param_aux.param_sig
        assert dict_param_aux.param_sig
        return paa.Result[SynthAux](
            tree = pas.make_DoubleBundleParam(
                comment_a_tree, 
                tuple_param_tree, 
                comment_b_tree, 
                comment_c_tree, 
                dict_param_tree,
                comment_d_tree, 
            ),
            aux = update_SynthAux(self.synthesize_auxes(tuple([tuple_param_aux, dict_param_aux])),
                bundle_pos_param_type = tuple_param_aux.param_sig.type,
                bundle_kw_param_type = dict_param_aux.param_sig.type,
                decl_additions=iom(
                    (tuple_param_aux.param_sig.key, make_Declaration(
                        updatable = make_VariedTupleType(
                            item_type=tuple_param_aux.param_sig.type
                        ),
                        initialized = True,
                        type = make_VariedTupleType(
                            item_type=tuple_param_aux.param_sig.type
                        )
                    )),
                    (dict_param_aux.param_sig.key, make_Declaration(
                        updatable = make_RecordType(
                            class_key = "builtins.dict",
                            type_args=(
                                make_RecordType(class_key="builtins.str"),
                                dict_param_aux.param_sig.type,
                            )
                        ),
                        initialized = True,
                        type = make_RecordType(
                            class_key = "builtins.dict",
                            type_args=(
                                make_RecordType(class_key="builtins.str"),
                                dict_param_aux.param_sig.type,
                            )
                        )
                    ))
                )
            )
        )



    # synthesize: parameters_c <-- DictionaryBundleParam
    def synthesize_for_parameters_c_DictionaryBundleParam(self, 
        inher_aux : InherAux,
        pre_comment_tree : str, 
        pre_comment_aux : SynthAux,
        content_tree : pas.Param, 
        content_aux : SynthAux,
        post_comment_tree : str, 
        post_comment_aux : SynthAux,
    ) -> paa.Result[SynthAux]:
        assert content_aux.param_sig
        return paa.Result[SynthAux](
            tree = pas.make_DictionaryBundleParam(pre_comment_tree, content_tree, post_comment_tree),
            aux = update_SynthAux(content_aux,
                bundle_kw_param_type = content_aux.param_sig.type,
                decl_additions=iom(
                    (content_aux.param_sig.key, make_Declaration(
                        updatable = make_RecordType(
                            class_key = "builtins.dict",
                            type_args=(
                                make_RecordType(class_key="builtins.str"),
                                content_aux.param_sig.type,
                            )
                        ),
                        initialized = True,
                        type = make_RecordType(
                            class_key = "builtins.dict",
                            type_args=(
                                make_RecordType(class_key="builtins.str"),
                                content_aux.param_sig.type,
                            )
                        )
                    ))
                )
            )
        )
    
    # synthesize: parameters_c <-- SingleTupleBundleParam
    def synthesize_for_parameters_c_SingleTupleBundleParam(self, 
        inher_aux : InherAux,
        pre_comment_tree : str, 
        pre_comment_aux : SynthAux,
        content_tree : pas.Param, 
        content_aux : SynthAux,
        post_comment_tree : str, 
        post_comment_aux : SynthAux,
    ) -> paa.Result[SynthAux]:
        assert content_aux.param_sig
        return paa.Result[SynthAux](
            tree = pas.make_SingleTupleBundleParam(pre_comment_tree, content_tree, post_comment_tree),
            aux = update_SynthAux(content_aux,
                bundle_pos_param_type = content_aux.param_sig.type,
                decl_additions=iom(
                    (content_aux.param_sig.key, make_Declaration(
                        updatable = make_VariedTupleType(
                            item_type=content_aux.param_sig.type
                        ),
                        initialized = True,
                        type = make_VariedTupleType(
                            item_type=content_aux.param_sig.type
                        )
                    ))
                )
            ) 
        )
    
    # synthesize: parameters_c <-- TransTupleBundleParam
    def synthesize_for_parameters_c_TransTupleBundleParam(self, 
        inher_aux : InherAux,
        pre_comment_tree : str, 
        pre_comment_aux : SynthAux,
        head_tree : pas.Param, 
        head_aux : SynthAux,
        post_comment_tree : str, 
        post_comment_aux : SynthAux,
        tail_tree : pas.parameters_d, 
        tail_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        assert head_aux.param_sig
        return paa.Result[SynthAux](
            tree = pas.make_TransTupleBundleParam(pre_comment_tree, head_tree, post_comment_tree, tail_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([head_aux, tail_aux])),
                bundle_pos_param_type = head_aux.param_sig.type,
                decl_additions=iom(
                    (head_aux.param_sig.key, make_Declaration(
                        updatable = make_VariedTupleType(
                            item_type=head_aux.param_sig.type
                        ),
                        initialized = True,
                        type = make_VariedTupleType(
                            item_type=head_aux.param_sig.type
                        )
                    ))
                ) + tail_aux.decl_additions
            ) 
        )
    
    # synthesize: parameters_b <-- ConsPosKeyParam
    def synthesize_for_parameters_b_ConsPosKeyParam(self, 
        inher_aux : InherAux,
        pre_comment_tree : str, 
        pre_comment_aux : SynthAux,
        head_tree : pas.Param, 
        head_aux : SynthAux,
        post_comment_tree : str, 
        post_comment_aux : SynthAux,
        tail_tree : pas.parameters_b, 
        tail_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        assert head_aux.param_sig


        return paa.Result[SynthAux](
            tree = pas.make_ConsPosKeyParam(pre_comment_tree, head_tree, post_comment_tree, tail_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([head_aux, tail_aux])),
                pos_kw_param_sigs = (head_aux.param_sig,) + tail_aux.pos_kw_param_sigs
            )
        )
    
    # synthesize: parameters_b <-- SinglePosKeyParam
    def synthesize_for_parameters_b_SinglePosKeyParam(self, 
        inher_aux : InherAux,
        pre_comment_tree : str, 
        pre_comment_aux : SynthAux,
        content_tree : pas.Param, 
        content_aux : SynthAux,
        post_comment_tree : str, 
        post_comment_aux : SynthAux,
    ) -> paa.Result[SynthAux]:
        assert content_aux.param_sig

        return paa.Result[SynthAux](
            tree = pas.make_SinglePosKeyParam(pre_comment_tree, content_tree, post_comment_tree),
            aux = update_SynthAux(content_aux,
                pos_kw_param_sigs = (content_aux.param_sig,)
            )
        )
    
    # synthesize: parameters_a <-- ConsPosParam
    def synthesize_for_parameters_a_ConsPosParam(self, 
        inher_aux : InherAux,
        pre_comment_tree : str, 
        pre_comment_aux : SynthAux,
        head_tree : pas.Param, 
        head_aux : SynthAux,
        post_comment_tree : str, 
        post_comment_aux : SynthAux,
        tail_tree : pas.parameters_a, 
        tail_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        assert head_aux.param_sig
        return paa.Result[SynthAux](
            tree = pas.make_ConsPosParam(pre_comment_tree, head_tree, post_comment_tree, tail_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([head_aux, tail_aux])),
                pos_param_types = tuple([head_aux.param_sig.type]) + tail_aux.pos_param_types
            )
        )
    
    # synthesize: parameters_a <-- SinglePosParam
    def synthesize_for_parameters_a_SinglePosParam(self, 
        inher_aux : InherAux,
        pre_comment_tree : str, 
        pre_comment_aux : SynthAux,
        content_tree : pas.Param, 
        content_aux : SynthAux,
        post_comment_tree : str, 
        post_comment_aux : SynthAux,
        pre_sep_comment_tree : str, 
        pre_sep_comment_aux : SynthAux,
        post_sep_comment_tree : str, 
        post_sep_comment_aux : SynthAux,
    ) -> paa.Result[SynthAux]:
        assert content_aux.param_sig
        return paa.Result[SynthAux](
            tree = pas.make_SinglePosParam(
                pre_comment_tree, 
                content_tree,
                post_comment_tree, 
                pre_sep_comment_tree, 
                post_sep_comment_tree, 
            ),
            aux = update_SynthAux(content_aux,
                pos_param_types = tuple([content_aux.param_sig.type])
            )
        )
    
    # synthesize: parameters_a <-- TransPosParam
    def synthesize_for_parameters_a_TransPosParam(self, 
        inher_aux : InherAux,
        pre_comment_tree : str, 
        pre_comment_aux : SynthAux,
        head_tree : pas.Param, 
        head_aux : SynthAux,
        post_comment_tree : str, 
        post_comment_aux : SynthAux,
        pre_sep_comment_tree : str, 
        pre_sep_comment_aux : SynthAux,
        post_sep_comment_tree : str, 
        post_sep_comment_aux : SynthAux,
        tail_tree : pas.parameters_b, 
        tail_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        assert head_aux.param_sig
        return paa.Result[SynthAux](
            tree = pas.make_TransPosParam(
                pre_comment_tree, 
                head_tree, 
                post_comment_tree, 
                pre_sep_comment_tree,
                post_sep_comment_tree,
                tail_tree
            ),
            aux = update_SynthAux(self.synthesize_auxes(tuple([head_aux, tail_aux])),
                pos_param_types = tuple([head_aux.param_sig.type]) + tail_aux.pos_param_types
            )
        )
    
    # stmt <-- Delete 
    def synthesize_for_stmt_Delete(self, 
        inher_aux : InherAux,
        targets_tree : pas.comma_exprs, 
        targets_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        return paa.Result[SynthAux](
            tree = pas.make_Delete(targets_tree),
            aux = make_SynthAux(
                decl_subtractions = pset(targets_aux.usage_additions.keys())
            ) 
        )
    # stmt <-- Assign
    def synthesize_for_stmt_Assign(self, 
        inher_aux : InherAux,
        targets_tree : pas.target_exprs, 
        targets_aux : SynthAux,
        content_tree : pas.expr, 
        content_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        # TODO: if source is of TypeType(VarType), check that target symbol matches VarType's symbol

        # check name compatability between target and source expressions 
        self.check(UpdateCheck(), lambda: 
            us.every(content_aux.usage_additions, lambda name : 
                name not in targets_aux.usage_additions or 
                name in inher_aux.declared_globals or 
                name in inher_aux.declared_nonlocals or 
                name in inher_aux.local_env
            )
        )



        updated_usage_additions : PMap[str, Usage] = m()
        for name, usage in targets_aux.usage_additions.items():
            if declared_and_initialized(inher_aux, name):
                updated_usage_additions = updated_usage_additions + pmap({name : update_Usage(usage, updated = True)})


        def patterns() -> Iterator[pas.expr | None]:
            tail = targets_tree
            while isinstance(tail, pas.ConsTargetExpr):
                yield tail.head
                tail = tail.tail

            assert isinstance(tail, pas.SingleTargetExpr)
            yield tail.content

        assert len(content_aux.observed_types) == 1
        content_type = content_aux.observed_types[0]
        env_types : InsertOrderMap[str, type] = iom()
        anchor_env : InsertOrderMap[str, type] = iom() 
        for pattern in patterns():
            if pattern:
                next_env_types, next_anchor_env = self.unify(pattern, content_type, inher_aux)
                env_types += next_env_types 
                anchor_env += next_anchor_env

        # check observed type with declared type
        self.check(AssignTypeCheck(), lambda: 
            us.every(env_types.items(), lambda entry : (
                sym := entry[0],
                observed_type := entry[1],
                dec := lookup_declaration(inher_aux, sym, builtins = False),
                not dec or not dec.updatable or subsumed(observed_type, dec.updatable, inher_aux)
            )[-1])
        )



        decl_additions : InsertOrderMap[str, Declaration] = iom() 
        decl_additions = iom(*(
            (k, make_Declaration(updatable=AnyType(), initialized=True, type=t))
            for k, t in env_types.items()
        ))

        # special consideration for declaration of Any used for type annotation
        if (
            inher_aux.external_path == "typing" and
            len(env_types) == 1 and
            'Any' in env_types
        ):
            original_type = env_types['Any']

            if (
                isinstance(original_type, RecordType) and
                original_type.class_key == "builtins.object"
            ):
                decl_additions = iom(
                    ('Any', make_Declaration(updatable=None, initialized=True, type=TypeType(AnyType())))
                )

        elif (len(env_types) == 1):
            (symbol, original_type) = next((k, env_types[k]) for k in env_types)
            if (
                isinstance(original_type, RecordType) and
                original_type.class_key == "typing.NewType"
            ):
                t = TypeType(AnyType())
                decl_additions = iom((symbol, make_Declaration(updatable=None, initialized=True, type=t)))


        return paa.Result[SynthAux](
            tree = pas.make_Assign(targets_tree, content_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([targets_aux, content_aux])),
                usage_additions = merge_usage_additions(updated_usage_additions, content_aux.usage_additions),
                decl_additions = decl_additions,
                static_field_additions=(
                    anchor_env
                    if isinstance(inher_aux.method_kind, ClassMethod) else
                    iom()
                ),
                instance_field_additions=(
                    anchor_env
                    if isinstance(inher_aux.method_kind, InstanceMethod) else
                    iom()
                ),
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
    ) -> paa.Result[SynthAux]:
        assert len(target_aux.observed_types) == 1
        target_type = target_aux.observed_types[0]
        assert len(content_aux.observed_types) == 1
        content_type = content_aux.observed_types[0]

        content_type = content_aux.observed_types[0]
        method_name = pas.from_bin_rator_to_aug_method_name(rator_tree)

        method_type = lookup_field_type(target_type, method_name, inher_aux)

        if isinstance(method_type, FunctionType):


            precise_method_type, subst_map = check_application_args(
                [content_type], {}, 
                method_type, inher_aux
            )
            self.check(ApplyArgTypeCheck(), lambda: 
                precise_method_type != None
            )

            self.check(AssignTypeCheck(), lambda: 
                precise_method_type != None and
                subsumed(precise_method_type.return_type, target_type, inher_aux)
            )

        elif isinstance(method_type, InterType):
            chosen_method_type = self.match_function_type(
                inher_aux,
                [content_type], {}, 
                method_type
            ) 
            self.check(ApplyArgTypeCheck(), lambda: chosen_method_type != None)


        if isinstance(target_tree, pas.Name):
            symbol = target_tree.content

            self.check(UpdateCheck(), lambda: 
                symbol in inher_aux.declared_globals or 
                symbol in inher_aux.declared_nonlocals or 
                symbol in inher_aux.local_env
            )

        else:
            self.check(UpdateCheck(), lambda: 
                isinstance(target_tree, pas.Subscript) or 
                isinstance(target_tree, pas.Attribute) 
            )

        updated_usage_additions : PMap[str, Usage] = m()
        for name, usage in target_aux.usage_additions.items():
            if declared_and_initialized(inher_aux, name):
                updated_usage_additions = updated_usage_additions + pmap({name : update_Usage(usage, updated = True)})



        return paa.Result[SynthAux](
            tree = pas.make_AugAssign(target_tree, rator_tree, content_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([target_aux, rator_aux, content_aux])),
                usage_additions = merge_usage_additions(updated_usage_additions, content_aux.usage_additions)
            )
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
    ) -> paa.Result[SynthAux]:

        assert len(content_aux.observed_types) == 1
        content_type = content_aux.observed_types[0]
        sig_type = coerce_to_TypeType(anno_aux.observed_types[0], inher_aux).content

        decl_additions: InsertOrderMap[str, Declaration] = iom() 
        anchor_env : InsertOrderMap[str, type] = iom() 
        if isinstance(target_tree, pas.Name):
            symbol = target_tree.content

            self.check(AssignTypeCheck(), lambda: 
                subsumed(content_type, sig_type, inher_aux)
            )

            # special consideration for declaration of special_form types
            if (
                inher_aux.external_path == "typing" and
                isinstance(sig_type, RecordType) and
                sig_type.class_key == "typing._SpecialForm" and
                symbol == "Generic"
            ):
                t = TypeType(GenericType())
                decl_additions = iom(
                    (symbol, make_Declaration(updatable=None, initialized=True, type=t))
                )
            elif (
                inher_aux.external_path == "typing" and
                isinstance(sig_type, RecordType) and
                sig_type.class_key == "typing._SpecialForm" and
                symbol == "Union"
            ):
                t = TypeType(UnionType(()))
                decl_additions = iom(
                    (symbol, make_Declaration(updatable=None, initialized=True, type=t))
                )
            elif (
                inher_aux.external_path == "typing" and
                isinstance(sig_type, RecordType) and
                sig_type.class_key == "typing._SpecialForm" and 
                symbol == "Protocol"
            ):
                t = TypeType(ProtocolType())
                decl_additions = iom(
                    (symbol, make_Declaration(updatable=None, initialized=True, type=t))
                )
            elif (
                inher_aux.external_path == "typing_extensions" and
                isinstance(sig_type, RecordType) and
                sig_type.class_key == "typing_extensions._SpecialForm" and 
                symbol == "Protocol"
            ):
                t = TypeType(ProtocolType())
                decl_additions = iom(
                    (symbol, make_Declaration(updatable=None, initialized=True, type=t))
                )
            elif (
                (inher_aux.external_path == "typing" and
                isinstance(sig_type, RecordType) and
                sig_type.class_key == "typing._SpecialForm") or
                (inher_aux.external_path == "typing_extensions" and
                isinstance(sig_type, RecordType) and
                sig_type.class_key == "typing_extensions._SpecialForm")
            ):
                t = TypeType(AnyType())
                decl_additions = iom(
                    (symbol, make_Declaration(updatable=None, initialized=True, type=t))
                )
            elif (
                inher_aux.external_path == "typing" and
                isinstance(sig_type, RecordType) and
                sig_type.class_key == "typing.NewType"
            ):
                t = TypeType(AnyType())
                decl_additions = iom(
                    (symbol, make_Declaration(updatable=None, initialized=True, type=t))
                )
            else:
                decl_additions = iom(
                    (symbol, make_Declaration(updatable=None, initialized=True, type=sig_type))
                )

        else: 
            assert isinstance(target_tree, pas.Attribute)
            content = target_tree.content
            if isinstance(content, pas.Name) and content.content == inher_aux.anchor_symbol:
                anchor_env += iom((target_tree.name, sig_type))


        return paa.Result[SynthAux](
            tree = pas.make_AnnoAssign(target_tree, anno_tree, content_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([target_aux, anno_aux, content_aux])),
                usage_additions = content_aux.usage_additions,
                decl_additions = decl_additions,
                static_field_additions=(
                    anchor_env
                    if isinstance(inher_aux.method_kind, ClassMethod) else
                    iom()
                ),
                instance_field_additions=(
                    anchor_env
                    if isinstance(inher_aux.method_kind, InstanceMethod) else
                    iom()
                ),
            ) 
        )

    # synthesize: stmt <-- AnnoDeclar
    def synthesize_for_stmt_AnnoDeclar(self, 
        inher_aux : InherAux,
        target_tree : pas.expr, 
        target_aux : SynthAux,
        anno_tree : pas.expr, 
        anno_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        assert len(anno_aux.observed_types) > 0
        sig_type = coerce_to_TypeType(anno_aux.observed_types[0], inher_aux).content

        decl_additions: InsertOrderMap[str, Declaration] = iom() 
        anchor_env : InsertOrderMap[str, type] = iom() 

        if isinstance(target_tree, pas.Name):
            symbol = target_tree.content

            decl_additions: InsertOrderMap[str, Declaration] = iom() 
            # special consideration for declaration of special_form types
            if (
                (inher_aux.external_path == "typing" and
                isinstance(sig_type, RecordType) and
                sig_type.class_key == "typing._SpecialForm") or
                (inher_aux.external_path == "typing_extensions" and
                isinstance(sig_type, RecordType) and
                sig_type.class_key == "typing_extensions._SpecialForm")
            ):
                t = TypeType(AnyType())
                decl_additions = iom(
                    (symbol, make_Declaration(updatable=None, initialized=True, type=t))
                )
            elif (
                inher_aux.external_path == "typing" and
                isinstance(sig_type, RecordType) and
                sig_type.class_key == "typing.NewType"
            ):
                t = TypeType(AnyType())
                decl_additions = iom(
                    (symbol, make_Declaration(updatable=None, initialized=True, type=t))
                )
            elif (
                inher_aux.external_path == "builtins" and
                isinstance(sig_type, RecordType) and
                sig_type.class_key == "builtins._NotImplementedType" and
                symbol == "NotImplemented"
            ):
                t = TypeType(AnyType())
                decl_additions = iom(
                    (symbol, make_Declaration(updatable=None, initialized=True, type=t))
                )
            elif (
                inher_aux.external_path == "typing_extensions" and
                isinstance(sig_type, RecordType) and
                sig_type.class_key == "builtins.object" and
                symbol == "TypedDict"
            ):
                t = TypeType(AnyType())
                decl_additions = iom(
                    (symbol, make_Declaration(updatable=None, initialized=True, type=t))
                )
            else:
                decl_additions = iom(
                    (symbol, make_Declaration(updatable=sig_type, initialized=False, type=sig_type))
                )
        else:
            assert isinstance(target_tree, pas.Attribute)
            content = target_tree.content
            if isinstance(content, pas.Name) and content.content == inher_aux.anchor_symbol:
                anchor_env += iom((target_tree.name, sig_type))


        return paa.Result[SynthAux](
            tree = pas.make_AnnoDeclar(target_tree, anno_tree),
            aux = make_SynthAux(
                decl_additions = decl_additions,
                static_field_additions=(
                    anchor_env
                    if isinstance(inher_aux.method_kind, ClassMethod) else
                    iom()
                ),
                instance_field_additions=(
                    anchor_env
                    if isinstance(inher_aux.method_kind, InstanceMethod) else
                    iom()
                ),
            ) 
        )

    # traverse: stmt <-- For
    def traverse_stmt_For_body(self, 
        inher_aux : InherAux,
        target_tree : pas.expr, 
        target_aux : SynthAux,
        iter_tree : pas.expr, 
        iter_aux : SynthAux,
        comment_tree : str, 
        comment_aux : SynthAux
    ) -> InherAux:
        assert len(iter_aux.observed_types) == 1
        iter_type = iter_aux.observed_types[0]
        return update_InherAux(inher_aux, local_env = (
            inher_aux.local_env + 
            iter_aux.decl_additions +
            iom(*(
                (k, make_Declaration(updatable=AnyType(), initialized=True, type=t))
                for k, t in self.unify_iteration(inher_aux, target_tree, iter_type).items()
            ))
        )) 


    # synthesize: stmt <-- For
    def synthesize_for_stmt_For(self, 
        inher_aux : InherAux,
        target_tree : pas.expr, 
        target_aux : SynthAux,
        iter_tree : pas.expr, 
        iter_aux : SynthAux,
        comment_tree : str, 
        comment_aux : SynthAux,
        body_tree : pas.statements, 
        body_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        usage_additions = filter_usage_additions(body_aux.usage_additions, target_aux.usage_additions, body_aux.decl_additions)

        return paa.Result[SynthAux](
            tree = pas.make_For(target_tree, iter_tree, comment_tree, body_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([target_aux, iter_aux, comment_aux, body_aux])),
                decl_subtractions = iter_aux.decl_subtractions, 
                decl_additions = iter_aux.decl_additions,
                usage_additions = usage_additions
            )
        )

    # traverse: stmt <-- ForElse
    def traverse_stmt_ForElse_body(self, 
        inher_aux : InherAux,
        target_tree : pas.expr, 
        target_aux : SynthAux,
        iter_tree : pas.expr, 
        iter_aux : SynthAux,
        comment_tree : str, 
        comment_aux : SynthAux
    ) -> InherAux:

        assert len(iter_aux.observed_types) == 1
        iter_type = iter_aux.observed_types[0]
        return update_InherAux(inher_aux, local_env = (
            inher_aux.local_env + 
            iter_aux.decl_additions +
            iom(*(
                (k, make_Declaration(updatable=AnyType(), initialized=True, type=t))
                for k, t in self.unify_iteration(inher_aux, target_tree, iter_type).items()
            ))
        )) 
    
    # synthesize: stmt <-- ForElse
    def synthesize_for_stmt_ForElse(self, 
        inher_aux : InherAux,
        target_tree : pas.expr, 
        target_aux : SynthAux,
        iter_tree : pas.expr, 
        iter_aux : SynthAux,
        comment_tree : str, 
        comment_aux : SynthAux,
        body_tree : pas.statements, 
        body_aux : SynthAux,
        orelse_tree : pas.ElseBlock, 
        orelse_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        usage_additions = filter_usage_additions(body_aux.usage_additions, 
            target_aux.usage_additions,
            body_aux.decl_additions,
            orelse_aux.decl_additions,
        )

        change_decl : Change[Declaration] = self.cross_join_aux_decls(inher_aux,
            to_change_decl(body_aux), 
            to_change_decl(orelse_aux)
        )
        return paa.Result[SynthAux](
            tree = pas.make_ForElse(target_tree, iter_tree, comment_tree, body_tree, orelse_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([target_aux, iter_aux, comment_aux, body_aux, orelse_aux])),
                decl_subtractions = iter_aux.decl_subtractions.update(change_decl.subtractions), 
                decl_additions = iter_aux.decl_additions + change_decl.additions,
                usage_additions = usage_additions
            )
        )



    # traverse: stmt <-- AsyncFor
    def traverse_stmt_AsyncFor_body(self, 
        inher_aux : InherAux,
        target_tree : pas.expr, 
        target_aux : SynthAux,
        iter_tree : pas.expr, 
        iter_aux : SynthAux,
        comment_tree : str, 
        comment_aux : SynthAux
    ) -> InherAux:
        return self.traverse_stmt_For_body(
            inher_aux,
            target_tree, 
            target_aux,
            iter_tree, 
            iter_aux,
            comment_tree,
            comment_aux
        ) 
    
    # synthesize: stmt <-- AsyncFor
    def synthesize_for_stmt_AsyncFor(self, 
        inher_aux : InherAux,
        target_tree : pas.expr, 
        target_aux : SynthAux,
        iter_tree : pas.expr, 
        iter_aux : SynthAux,
        comment_tree : str, 
        comment_aux : SynthAux,
        body_tree : pas.statements, 
        body_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        usage_additions = filter_usage_additions(body_aux.usage_additions, 
            target_aux.usage_additions,
            body_aux.decl_additions,
        )

        assert len(iter_aux.observed_types) == 1
        iter_type = iter_aux.observed_types[0]
        new_synth_aux = self.synthesize_auxes((iter_aux, comment_aux, body_aux))
        return paa.Result[SynthAux](
            tree = pas.make_AsyncFor(target_tree, iter_tree, comment_tree, body_tree),
            aux = make_SynthAux(
                decl_subtractions = new_synth_aux.decl_subtractions, 
                decl_additions= (
                    new_synth_aux.decl_additions +
                    iom(*(
                        (k, make_Declaration(updatable=AnyType(), initialized=True, type=t))
                        for k, t in self.unify_iteration(inher_aux, target_tree, iter_type).items()
                    ))
                ),
                usage_additions=usage_additions
            )
        )

    # traverse: stmt <-- AsyncForElse
    def traverse_stmt_AsyncForElse_body(self, 
        inher_aux : InherAux,
        target_tree : pas.expr, 
        target_aux : SynthAux,
        iter_tree : pas.expr, 
        iter_aux : SynthAux,
        comment_tree : str, 
        comment_aux : SynthAux
    ) -> InherAux:
        return self.traverse_stmt_ForElse_body(
            inher_aux, 
            target_tree, target_aux, 
            iter_tree, iter_aux,
            comment_tree, comment_aux
        )
    
    # synthesize: stmt <-- AsyncForElse
    def synthesize_for_stmt_AsyncForElse(self, 
        inher_aux : InherAux,
        target_tree : pas.expr, 
        target_aux : SynthAux,
        iter_tree : pas.expr, 
        iter_aux : SynthAux,
        comment_tree : str, 
        comment_aux : SynthAux,
        body_tree : pas.statements, 
        body_aux : SynthAux,
        orelse_tree : pas.ElseBlock, 
        orelse_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        usage_additions = filter_usage_additions(body_aux.usage_additions, 
            target_aux.usage_additions,
            body_aux.decl_additions,
            orelse_aux.decl_additions
        )

        assert len(iter_aux.observed_types) == 1
        iter_type = iter_aux.observed_types[0]
        change_decl : Change[Declaration] = self.cross_join_aux_decls(inher_aux,
            to_change_decl(body_aux), 
            to_change_decl(orelse_aux)
        )
        return paa.Result[SynthAux](
            tree = pas.make_AsyncForElse(target_tree, iter_tree, comment_tree, body_tree, orelse_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([target_aux, iter_aux, comment_aux, body_aux, orelse_aux])),
                decl_subtractions = iter_aux.decl_subtractions.update(change_decl.subtractions), 
                decl_additions= (
                    iter_aux.decl_additions + change_decl.additions +
                    iom(*(
                        (k, make_Declaration(updatable=AnyType(), initialized=True, type=t))
                        for k, t in self.unify_iteration(inher_aux, target_tree, iter_type).items()
                    ))
                ),
                usage_additions=usage_additions
            )
        )

    # synthesize: import_name <-- ImportNameAlias
    def synthesize_for_import_name_ImportNameAlias(self, 
        inher_aux : InherAux,
        name_tree : str, 
        name_aux : SynthAux,
        pre_comment_tree : str, 
        pre_comment_aux : SynthAux,
        post_comment_tree : str, 
        post_comment_aux : SynthAux,
        alias_tree : str, 
        alias_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        return paa.Result[SynthAux](
            tree = pas.make_ImportNameAlias(name_tree, pre_comment_tree, post_comment_tree, alias_tree),
            aux = make_SynthAux(
                import_names=iom((alias_tree, name_tree))
            )
        )
    

    # synthesize: import_name <-- ImportNameOnly
    def synthesize_for_import_name_ImportNameOnly(self, 
        inher_aux : InherAux,
        name_tree : str, 
        name_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        return paa.Result[SynthAux](
            tree = pas.make_ImportNameOnly(name_tree),
            aux = make_SynthAux(
                import_names=iom((name_tree, name_tree))
            )
        )


    # synthesize: stmt <-- Import
    def synthesize_for_stmt_Import(self, 
        inher_aux : InherAux,
        names_tree : pas.sequence_import_name, 
        names_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        env_additions : InsertOrderMap[str, Declaration] = iom(*(
            (alias, from_static_path_to_declaration(inher_aux, source_path))
            for alias, source_path in names_aux.import_names.items()
        ))

        return paa.Result[SynthAux](
            tree = pas.make_Import(names_tree),
            aux = make_SynthAux(
                decl_additions=env_additions
            ) 
        )

    # synthesize: stmt <-- ImportFrom 
    def synthesize_for_stmt_ImportFrom(self, 
        inher_aux : InherAux,
        module_tree : str, 
        module_aux : SynthAux,
        names_tree : pas.sequence_import_name, 
        names_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        dot_num = next((
            i
            for i, c in enumerate(module_tree)
            if c != "."
        ), len(module_tree))

        external_levels = inher_aux.external_path.split(".")
        assert len(external_levels) >= dot_num

        if dot_num > 0:
            back_track = dot_num - 1
            end = len(external_levels) - back_track
            prefix = ".".join(external_levels[:end])

            suffix = module_tree[dot_num:]
            module_tree = prefix + ("." + suffix if suffix else '') 


        env_additions : InsertOrderMap[str, Declaration] = iom(*(
            (alias, from_static_path_to_declaration(inher_aux, f'{module_tree}.{source_path}'))
            for alias, source_path in names_aux.import_names.items()
        ))


        return paa.Result[SynthAux](
            tree = pas.make_ImportFrom(module_tree, names_tree),
            aux = make_SynthAux(
                decl_additions=env_additions
            ) 
        )

    # synthesize: sequence_name <-- SingleId 
    def synthesize_for_sequence_name_SingleId(self, 
        inher_aux : InherAux,
        content_tree : str, 
        content_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        return paa.Result[SynthAux](
            tree = pas.make_SingleId(content_tree),
            aux = content_aux
        )
    

    # synthesize: stmt <-- Global 
    def synthesize_for_stmt_Global(self, 
        inher_aux : InherAux,
        names_tree : pas.sequence_name, 
        names_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        return paa.Result[SynthAux](
            tree = pas.make_Global(names_tree),
            aux = make_SynthAux(
                declared_globals = pset(names_aux.usage_additions.keys())
            )
        )

    # synthesize: stmt <-- Nonlocal 
    def synthesize_for_stmt_Nonlocal(self, 
        inher_aux : InherAux,
        names_tree : pas.sequence_name, 
        names_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        return paa.Result[SynthAux](
            tree = pas.make_Nonlocal(names_tree),
            aux = make_SynthAux(
                declared_nonlocals = pset(names_aux.usage_additions.keys())
            )
        )

    
    # traverse: stmt <-- WhileElse
    def traverse_stmt_WhileElse_orelse(self, 
        inher_aux : InherAux,
        test_tree : pas.expr, 
        test_aux : SynthAux,
        comment_tree : str, 
        comment_aux : SynthAux,
        body_tree : pas.statements, 
        body_aux : SynthAux
    ) -> InherAux:
        return traverse_aux(inher_aux, test_aux) 
    

    # synthesize: stmt <-- While
    def synthesize_for_stmt_While(self, 
        inher_aux : InherAux,
        test_tree : pas.expr, 
        test_aux : SynthAux,
        comment_tree : str, 
        comment_aux : SynthAux,
        body_tree : pas.statements, 
        body_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        return paa.Result[SynthAux](
            tree = pas.make_While(test_tree, comment_tree, body_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([test_aux, comment_aux, body_aux])),
                decl_subtractions = test_aux.decl_subtractions,
                decl_additions = test_aux.decl_additions,
            ) 
        )

    # synthesize: stmt <-- WhileElse
    def synthesize_for_stmt_WhileElse(self, 
        inher_aux : InherAux,
        test_tree : pas.expr, 
        test_aux : SynthAux,
        comment_tree : str, 
        comment_aux : SynthAux,
        body_tree : pas.statements, 
        body_aux : SynthAux,
        orelse_tree : pas.ElseBlock, 
        orelse_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        change_decl : Change[Declaration] = self.cross_join_aux_decls(inher_aux,
            to_change_decl(body_aux), 
            to_change_decl(orelse_aux)
        )

        return paa.Result[SynthAux](
            tree = pas.make_WhileElse(test_tree, comment_tree, body_tree, orelse_tree),
            aux = update_SynthAux(self.synthesize_auxes((test_aux, comment_aux, body_aux, orelse_aux)),
                decl_subtractions = test_aux.decl_subtractions.update(change_decl.subtractions),
                decl_additions = test_aux.decl_additions + change_decl.additions,
            ) 
        )


    # traverse: stmt <-- If
    def traverse_stmt_If_orelse(self, 
        inher_aux : InherAux,
        test_tree : pas.expr, 
        test_aux : SynthAux,
        comment_tree : str, 
        comment_aux : SynthAux,
        body_tree : pas.statements, 
        body_aux : SynthAux
    ) -> InherAux:
        return traverse_aux(inher_aux, test_aux) 
    
    # synthesize: stmt <-- If 
    def synthesize_for_stmt_If(self, 
        inher_aux : InherAux,
        test_tree : pas.expr, 
        test_aux : SynthAux,
        comment_tree : str, 
        comment_aux : SynthAux,
        body_tree : pas.statements, 
        body_aux : SynthAux,
        orelse_tree : pas.conditions, 
        orelse_aux : SynthAux
    ) -> paa.Result[SynthAux]:

        change_decl : Change[Declaration] = self.cross_join_aux_decls(inher_aux,
            to_change_decl(body_aux), 
            to_change_decl(orelse_aux)
        )

        return paa.Result[SynthAux](
            tree = pas.make_If(test_tree, comment_tree, body_tree, orelse_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([test_aux, comment_aux, body_aux, orelse_aux])),
                decl_subtractions = test_aux.decl_subtractions.update(change_decl.subtractions), 
                decl_additions = test_aux.decl_additions + change_decl.additions,
                return_types = body_aux.return_types + orelse_aux.return_types,
                yield_types = body_aux.yield_types + orelse_aux.yield_types
            )
        )

    # traverse conditions <-- ElifCond
    def traverse_conditions_ElifCond_tail(self, 
        inher_aux : InherAux,
        content_tree : pas.ElifBlock, 
        content_aux : SynthAux
    ) -> InherAux:
        return inher_aux

    # synthesize: conditions <-- ElifCond
    def synthesize_for_conditions_ElifCond(self, 
        inher_aux : InherAux,
        content_tree : pas.ElifBlock, 
        content_aux : SynthAux,
        tail_tree : pas.conditions, 
        tail_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        change_decl = self.cross_join_aux_decls(inher_aux,
            
            to_change_decl(content_aux), 
            to_change_decl(tail_aux)
        )
            
        return paa.Result[SynthAux](
            tree = pas.make_ElifCond(content_tree, tail_tree),
            aux = update_SynthAux(self.synthesize_auxes(tuple([content_aux, tail_aux])),
                decl_subtractions = change_decl.subtractions, 
                decl_additions = change_decl.additions,
                return_types = content_aux.return_types + tail_aux.return_types,
                yield_types = content_aux.yield_types + tail_aux.yield_types
            )
        )
    
    # synthesize: ElifBlock
    def synthesize_for_ElifBlock(self, 
        inher_aux : InherAux,
        pre_comment_tree : str, 
        pre_comment_aux : SynthAux,
        test_tree : pas.expr, 
        test_aux : SynthAux,
        comment_tree : str, 
        comment_aux : SynthAux,
        body_tree : pas.statements, 
        body_aux : SynthAux
    ) -> paa.Result[SynthAux]:
        return paa.Result[SynthAux](
            tree = pas.make_ElifBlock(pre_comment_tree, test_tree, comment_tree, body_tree), 
            aux = update_SynthAux(body_aux,
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
    ) -> paa.Result[SynthAux]:


        assert len(content_aux.observed_types) == 1
        type_type = coerce_to_TypeType(content_aux.observed_types[0], inher_aux)
        t = type_type.content

        name_aux = make_SynthAux(decl_additions = iom(
            (name_tree, make_Declaration(updatable=t, initialized=False, type=t))
       ))

        return paa.Result[SynthAux](
            tree = pas.make_SomeExceptArgName(content_tree, name_tree),
            aux = make_SynthAux(
                decl_additions = (
                    content_aux.decl_additions + 
                    name_aux.decl_additions
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
    ) -> paa.Result[SynthAux]:

        self.check(UpdateCheck(), lambda: 
            us.every(content_aux.usage_additions, lambda name : 
                name not in alias_aux.usage_additions or 
                name in inher_aux.declared_globals or 
                name in inher_aux.declared_nonlocals or 
                name in inher_aux.local_env
            )
        )

        assert len(content_aux.observed_types) == 1
        content_type = content_aux.observed_types[0]
        env_additions, anchor_env_additions = self.unify(alias_tree, content_type, inher_aux)
        return paa.Result[SynthAux](
            tree = pas.make_WithItemAlias(content_tree, alias_tree),
            aux = make_SynthAux(
                decl_additions = (
                    content_aux.decl_additions +
                    iom(*(
                        (k, make_Declaration(updatable=AnyType(), initialized=True, type = t))
                        for k, t in env_additions.items() 
                    ))
                ),
                static_field_additions=(
                    anchor_env_additions
                    if isinstance(inher_aux.method_kind, ClassMethod) else
                    iom()
                ),
                instance_field_additions=(
                    anchor_env_additions
                    if isinstance(inher_aux.method_kind, InstanceMethod) else
                    iom()
                ),
            )
        )