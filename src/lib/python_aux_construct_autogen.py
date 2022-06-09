# THIS FILE IS AUTOGENERATED
# CHANGES MAY BE LOST



from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, TypeVar, Any, Generic, Union, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod

T = TypeVar('T')


@dataclass(frozen=True, eq=True)
class SourceFlag: 
    pass



from pyrsistent.typing import PMap, PSet
from pyrsistent import pmap, m, pset, s
from base.abstract_token_construct_autogen import abstract_token 
from lib.python_ast_construct_autogen import ast 
    


# type variant
@dataclass(frozen=True, eq=True)
class variant(ABC):
    # @abstractmethod
    def match(self, handlers : VariantHandlers[T]) -> T:
        raise Exception()


# constructors for type variant

@dataclass(frozen=True, eq=True)
class CoVariant(variant):


    def match(self, handlers : VariantHandlers[T]) -> T:
        return handlers.case_CoVariant(self)

def make_CoVariant(
) -> variant:
    return CoVariant(
    )

def update_CoVariant(source_CoVariant : CoVariant
) -> CoVariant:
    return CoVariant(
    )

        

@dataclass(frozen=True, eq=True)
class ContraVariant(variant):


    def match(self, handlers : VariantHandlers[T]) -> T:
        return handlers.case_ContraVariant(self)

def make_ContraVariant(
) -> variant:
    return ContraVariant(
    )

def update_ContraVariant(source_ContraVariant : ContraVariant
) -> ContraVariant:
    return ContraVariant(
    )

        

@dataclass(frozen=True, eq=True)
class NoVariant(variant):


    def match(self, handlers : VariantHandlers[T]) -> T:
        return handlers.case_NoVariant(self)

def make_NoVariant(
) -> variant:
    return NoVariant(
    )

def update_NoVariant(source_NoVariant : NoVariant
) -> NoVariant:
    return NoVariant(
    )

        

# case handlers for type variant
@dataclass(frozen=True, eq=True)
class VariantHandlers(Generic[T]):
    case_CoVariant : Callable[[CoVariant], T]
    case_ContraVariant : Callable[[ContraVariant], T]
    case_NoVariant : Callable[[NoVariant], T]


# matching for type variant
def match_variant(o : variant, handlers : VariantHandlers[T]) -> T :
    return o.match(handlers)
    

# type type
@dataclass(frozen=True, eq=True)
class type(ABC):
    # @abstractmethod
    def match(self, handlers : TypeHandlers[T]) -> T:
        raise Exception()


# constructors for type type

@dataclass(frozen=True, eq=True)
class ProtocolType(type):


    def match(self, handlers : TypeHandlers[T]) -> T:
        return handlers.case_ProtocolType(self)

def make_ProtocolType(
) -> type:
    return ProtocolType(
    )

def update_ProtocolType(source_ProtocolType : ProtocolType
) -> ProtocolType:
    return ProtocolType(
    )

        

@dataclass(frozen=True, eq=True)
class GenericType(type):


    def match(self, handlers : TypeHandlers[T]) -> T:
        return handlers.case_GenericType(self)

def make_GenericType(
) -> type:
    return GenericType(
    )

def update_GenericType(source_GenericType : GenericType
) -> GenericType:
    return GenericType(
    )

        

@dataclass(frozen=True, eq=True)
class OverloadType(type):


    def match(self, handlers : TypeHandlers[T]) -> T:
        return handlers.case_OverloadType(self)

def make_OverloadType(
) -> type:
    return OverloadType(
    )

def update_OverloadType(source_OverloadType : OverloadType
) -> OverloadType:
    return OverloadType(
    )

        

@dataclass(frozen=True, eq=True)
class TypeType(type):
    class_key : str
    content : type

    def match(self, handlers : TypeHandlers[T]) -> T:
        return handlers.case_TypeType(self)

def make_TypeType(
    class_key : str, 
    content : type
) -> type:
    return TypeType(
        class_key,
        content
    )

def update_TypeType(source_TypeType : TypeType,
    class_key : Union[str, SourceFlag] = SourceFlag(),
    content : Union[type, SourceFlag] = SourceFlag()
) -> TypeType:
    return TypeType(
        source_TypeType.class_key if isinstance(class_key, SourceFlag) else class_key,
        source_TypeType.content if isinstance(content, SourceFlag) else content
    )

        

@dataclass(frozen=True, eq=True)
class VarType(type):
    name : str
    variant : variant

    def match(self, handlers : TypeHandlers[T]) -> T:
        return handlers.case_VarType(self)

def make_VarType(
    name : str, 
    variant : variant = NoVariant()
) -> type:
    return VarType(
        name,
        variant
    )

def update_VarType(source_VarType : VarType,
    name : Union[str, SourceFlag] = SourceFlag(),
    variant : Union[variant, SourceFlag] = SourceFlag()
) -> VarType:
    return VarType(
        source_VarType.name if isinstance(name, SourceFlag) else name,
        source_VarType.variant if isinstance(variant, SourceFlag) else variant
    )

        

@dataclass(frozen=True, eq=True)
class EllipType(type):


    def match(self, handlers : TypeHandlers[T]) -> T:
        return handlers.case_EllipType(self)

def make_EllipType(
) -> type:
    return EllipType(
    )

def update_EllipType(source_EllipType : EllipType
) -> EllipType:
    return EllipType(
    )

        

@dataclass(frozen=True, eq=True)
class AnyType(type):


    def match(self, handlers : TypeHandlers[T]) -> T:
        return handlers.case_AnyType(self)

def make_AnyType(
) -> type:
    return AnyType(
    )

def update_AnyType(source_AnyType : AnyType
) -> AnyType:
    return AnyType(
    )

        

@dataclass(frozen=True, eq=True)
class ObjectType(type):


    def match(self, handlers : TypeHandlers[T]) -> T:
        return handlers.case_ObjectType(self)

def make_ObjectType(
) -> type:
    return ObjectType(
    )

def update_ObjectType(source_ObjectType : ObjectType
) -> ObjectType:
    return ObjectType(
    )

        

@dataclass(frozen=True, eq=True)
class NoneType(type):


    def match(self, handlers : TypeHandlers[T]) -> T:
        return handlers.case_NoneType(self)

def make_NoneType(
) -> type:
    return NoneType(
    )

def update_NoneType(source_NoneType : NoneType
) -> NoneType:
    return NoneType(
    )

        

@dataclass(frozen=True, eq=True)
class ModuleType(type):
    key : str

    def match(self, handlers : TypeHandlers[T]) -> T:
        return handlers.case_ModuleType(self)

def make_ModuleType(
    key : str
) -> type:
    return ModuleType(
        key
    )

def update_ModuleType(source_ModuleType : ModuleType,
    key : Union[str, SourceFlag] = SourceFlag()
) -> ModuleType:
    return ModuleType(
        source_ModuleType.key if isinstance(key, SourceFlag) else key
    )

        

@dataclass(frozen=True, eq=True)
class FunctionType(type):
    pos_param_types : tuple[type, ...]
    pos_kw_param_sigs : tuple[ParamSig, ...]
    splat_pos_param_type : Optional[type]
    kw_param_sigs : tuple[ParamSig, ...]
    splat_kw_param_type : Optional[type]
    return_type : type

    def match(self, handlers : TypeHandlers[T]) -> T:
        return handlers.case_FunctionType(self)

def make_FunctionType(
    pos_param_types : tuple[type, ...] = (), 
    pos_kw_param_sigs : tuple[ParamSig, ...] = (), 
    splat_pos_param_type : Optional[type] = None, 
    kw_param_sigs : tuple[ParamSig, ...] = (), 
    splat_kw_param_type : Optional[type] = None, 
    return_type : type = AnyType()
) -> type:
    return FunctionType(
        pos_param_types,
        pos_kw_param_sigs,
        splat_pos_param_type,
        kw_param_sigs,
        splat_kw_param_type,
        return_type
    )

def update_FunctionType(source_FunctionType : FunctionType,
    pos_param_types : Union[tuple[type, ...], SourceFlag] = SourceFlag(),
    pos_kw_param_sigs : Union[tuple[ParamSig, ...], SourceFlag] = SourceFlag(),
    splat_pos_param_type : Union[Optional[type], SourceFlag] = SourceFlag(),
    kw_param_sigs : Union[tuple[ParamSig, ...], SourceFlag] = SourceFlag(),
    splat_kw_param_type : Union[Optional[type], SourceFlag] = SourceFlag(),
    return_type : Union[type, SourceFlag] = SourceFlag()
) -> FunctionType:
    return FunctionType(
        source_FunctionType.pos_param_types if isinstance(pos_param_types, SourceFlag) else pos_param_types,
        source_FunctionType.pos_kw_param_sigs if isinstance(pos_kw_param_sigs, SourceFlag) else pos_kw_param_sigs,
        source_FunctionType.splat_pos_param_type if isinstance(splat_pos_param_type, SourceFlag) else splat_pos_param_type,
        source_FunctionType.kw_param_sigs if isinstance(kw_param_sigs, SourceFlag) else kw_param_sigs,
        source_FunctionType.splat_kw_param_type if isinstance(splat_kw_param_type, SourceFlag) else splat_kw_param_type,
        source_FunctionType.return_type if isinstance(return_type, SourceFlag) else return_type
    )

        

@dataclass(frozen=True, eq=True)
class UnionType(type):
    type_choices : tuple[type, ...]

    def match(self, handlers : TypeHandlers[T]) -> T:
        return handlers.case_UnionType(self)

def make_UnionType(
    type_choices : tuple[type, ...]
) -> type:
    return UnionType(
        type_choices
    )

def update_UnionType(source_UnionType : UnionType,
    type_choices : Union[tuple[type, ...], SourceFlag] = SourceFlag()
) -> UnionType:
    return UnionType(
        source_UnionType.type_choices if isinstance(type_choices, SourceFlag) else type_choices
    )

        

@dataclass(frozen=True, eq=True)
class InterType(type):
    type_components : tuple[type, ...]

    def match(self, handlers : TypeHandlers[T]) -> T:
        return handlers.case_InterType(self)

def make_InterType(
    type_components : tuple[type, ...]
) -> type:
    return InterType(
        type_components
    )

def update_InterType(source_InterType : InterType,
    type_components : Union[tuple[type, ...], SourceFlag] = SourceFlag()
) -> InterType:
    return InterType(
        source_InterType.type_components if isinstance(type_components, SourceFlag) else type_components
    )

        

@dataclass(frozen=True, eq=True)
class RecordType(type):
    class_key : str
    class_uid : int
    type_args : tuple[type, ...]
    protocol : bool

    def match(self, handlers : TypeHandlers[T]) -> T:
        return handlers.case_RecordType(self)

def make_RecordType(
    class_key : str, 
    class_uid : int = 0, 
    type_args : tuple[type, ...] = (), 
    protocol : bool = False
) -> type:
    return RecordType(
        class_key,
        class_uid,
        type_args,
        protocol
    )

def update_RecordType(source_RecordType : RecordType,
    class_key : Union[str, SourceFlag] = SourceFlag(),
    class_uid : Union[int, SourceFlag] = SourceFlag(),
    type_args : Union[tuple[type, ...], SourceFlag] = SourceFlag(),
    protocol : Union[bool, SourceFlag] = SourceFlag()
) -> RecordType:
    return RecordType(
        source_RecordType.class_key if isinstance(class_key, SourceFlag) else class_key,
        source_RecordType.class_uid if isinstance(class_uid, SourceFlag) else class_uid,
        source_RecordType.type_args if isinstance(type_args, SourceFlag) else type_args,
        source_RecordType.protocol if isinstance(protocol, SourceFlag) else protocol
    )

        

@dataclass(frozen=True, eq=True)
class TupleLitType(type):
    item_types : tuple[type, ...]

    def match(self, handlers : TypeHandlers[T]) -> T:
        return handlers.case_TupleLitType(self)

def make_TupleLitType(
    item_types : tuple[type, ...] = ()
) -> type:
    return TupleLitType(
        item_types
    )

def update_TupleLitType(source_TupleLitType : TupleLitType,
    item_types : Union[tuple[type, ...], SourceFlag] = SourceFlag()
) -> TupleLitType:
    return TupleLitType(
        source_TupleLitType.item_types if isinstance(item_types, SourceFlag) else item_types
    )

        

@dataclass(frozen=True, eq=True)
class VariedTupleType(type):
    item_type : type

    def match(self, handlers : TypeHandlers[T]) -> T:
        return handlers.case_VariedTupleType(self)

def make_VariedTupleType(
    item_type : type = AnyType()
) -> type:
    return VariedTupleType(
        item_type
    )

def update_VariedTupleType(source_VariedTupleType : VariedTupleType,
    item_type : Union[type, SourceFlag] = SourceFlag()
) -> VariedTupleType:
    return VariedTupleType(
        source_VariedTupleType.item_type if isinstance(item_type, SourceFlag) else item_type
    )

        

@dataclass(frozen=True, eq=True)
class ListLitType(type):
    item_types : tuple[type, ...]

    def match(self, handlers : TypeHandlers[T]) -> T:
        return handlers.case_ListLitType(self)

def make_ListLitType(
    item_types : tuple[type, ...] = ()
) -> type:
    return ListLitType(
        item_types
    )

def update_ListLitType(source_ListLitType : ListLitType,
    item_types : Union[tuple[type, ...], SourceFlag] = SourceFlag()
) -> ListLitType:
    return ListLitType(
        source_ListLitType.item_types if isinstance(item_types, SourceFlag) else item_types
    )

        

@dataclass(frozen=True, eq=True)
class TrueType(type):


    def match(self, handlers : TypeHandlers[T]) -> T:
        return handlers.case_TrueType(self)

def make_TrueType(
) -> type:
    return TrueType(
    )

def update_TrueType(source_TrueType : TrueType
) -> TrueType:
    return TrueType(
    )

        

@dataclass(frozen=True, eq=True)
class FalseType(type):


    def match(self, handlers : TypeHandlers[T]) -> T:
        return handlers.case_FalseType(self)

def make_FalseType(
) -> type:
    return FalseType(
    )

def update_FalseType(source_FalseType : FalseType
) -> FalseType:
    return FalseType(
    )

        

@dataclass(frozen=True, eq=True)
class IntLitType(type):
    literal : str

    def match(self, handlers : TypeHandlers[T]) -> T:
        return handlers.case_IntLitType(self)

def make_IntLitType(
    literal : str = ''
) -> type:
    return IntLitType(
        literal
    )

def update_IntLitType(source_IntLitType : IntLitType,
    literal : Union[str, SourceFlag] = SourceFlag()
) -> IntLitType:
    return IntLitType(
        source_IntLitType.literal if isinstance(literal, SourceFlag) else literal
    )

        

@dataclass(frozen=True, eq=True)
class FloatLitType(type):
    literal : str

    def match(self, handlers : TypeHandlers[T]) -> T:
        return handlers.case_FloatLitType(self)

def make_FloatLitType(
    literal : str = ''
) -> type:
    return FloatLitType(
        literal
    )

def update_FloatLitType(source_FloatLitType : FloatLitType,
    literal : Union[str, SourceFlag] = SourceFlag()
) -> FloatLitType:
    return FloatLitType(
        source_FloatLitType.literal if isinstance(literal, SourceFlag) else literal
    )

        

@dataclass(frozen=True, eq=True)
class StrLitType(type):
    literal : str

    def match(self, handlers : TypeHandlers[T]) -> T:
        return handlers.case_StrLitType(self)

def make_StrLitType(
    literal : str = ''
) -> type:
    return StrLitType(
        literal
    )

def update_StrLitType(source_StrLitType : StrLitType,
    literal : Union[str, SourceFlag] = SourceFlag()
) -> StrLitType:
    return StrLitType(
        source_StrLitType.literal if isinstance(literal, SourceFlag) else literal
    )

        

# case handlers for type type
@dataclass(frozen=True, eq=True)
class TypeHandlers(Generic[T]):
    case_ProtocolType : Callable[[ProtocolType], T]
    case_GenericType : Callable[[GenericType], T]
    case_OverloadType : Callable[[OverloadType], T]
    case_TypeType : Callable[[TypeType], T]
    case_VarType : Callable[[VarType], T]
    case_EllipType : Callable[[EllipType], T]
    case_AnyType : Callable[[AnyType], T]
    case_ObjectType : Callable[[ObjectType], T]
    case_NoneType : Callable[[NoneType], T]
    case_ModuleType : Callable[[ModuleType], T]
    case_FunctionType : Callable[[FunctionType], T]
    case_UnionType : Callable[[UnionType], T]
    case_InterType : Callable[[InterType], T]
    case_RecordType : Callable[[RecordType], T]
    case_TupleLitType : Callable[[TupleLitType], T]
    case_VariedTupleType : Callable[[VariedTupleType], T]
    case_ListLitType : Callable[[ListLitType], T]
    case_TrueType : Callable[[TrueType], T]
    case_FalseType : Callable[[FalseType], T]
    case_IntLitType : Callable[[IntLitType], T]
    case_FloatLitType : Callable[[FloatLitType], T]
    case_StrLitType : Callable[[StrLitType], T]


# matching for type type
def match_type(o : type, handlers : TypeHandlers[T]) -> T :
    return o.match(handlers)
     


# type and constructor ClassRecord
@dataclass(frozen=True, eq=True)
class ClassRecord:
    key : str
    type_params : tuple[VarType, ...]
    super_types : tuple[TypeType, ...]
    static_fields : PMap[str, type]
    instance_fields : PMap[str, type]


def make_ClassRecord(
    key : str,
    type_params : tuple[VarType, ...],
    super_types : tuple[TypeType, ...],
    static_fields : PMap[str, type],
    instance_fields : PMap[str, type]
) -> ClassRecord:
    return ClassRecord(
        key,
        type_params,
        super_types,
        static_fields,
        instance_fields)

def update_ClassRecord(source_ClassRecord : ClassRecord,
    key : Union[str, SourceFlag] = SourceFlag(),
    type_params : Union[tuple[VarType, ...], SourceFlag] = SourceFlag(),
    super_types : Union[tuple[TypeType, ...], SourceFlag] = SourceFlag(),
    static_fields : Union[PMap[str, type], SourceFlag] = SourceFlag(),
    instance_fields : Union[PMap[str, type], SourceFlag] = SourceFlag()
) -> ClassRecord:
    return ClassRecord(
        source_ClassRecord.key if isinstance(key, SourceFlag) else key, 
        source_ClassRecord.type_params if isinstance(type_params, SourceFlag) else type_params, 
        source_ClassRecord.super_types if isinstance(super_types, SourceFlag) else super_types, 
        source_ClassRecord.static_fields if isinstance(static_fields, SourceFlag) else static_fields, 
        source_ClassRecord.instance_fields if isinstance(instance_fields, SourceFlag) else instance_fields)

    

# type and constructor ModulePackage
@dataclass(frozen=True, eq=True)
class ModulePackage:
    module : PMap[str, Declaration]
    class_env : PMap[str, ClassRecord]
    package : PMap[str, ModulePackage]


def make_ModulePackage(
    module : PMap[str, Declaration] = m(),
    class_env : PMap[str, ClassRecord] = m(),
    package : PMap[str, ModulePackage] = m()
) -> ModulePackage:
    return ModulePackage(
        module,
        class_env,
        package)

def update_ModulePackage(source_ModulePackage : ModulePackage,
    module : Union[PMap[str, Declaration], SourceFlag] = SourceFlag(),
    class_env : Union[PMap[str, ClassRecord], SourceFlag] = SourceFlag(),
    package : Union[PMap[str, ModulePackage], SourceFlag] = SourceFlag()
) -> ModulePackage:
    return ModulePackage(
        source_ModulePackage.module if isinstance(module, SourceFlag) else module, 
        source_ModulePackage.class_env if isinstance(class_env, SourceFlag) else class_env, 
        source_ModulePackage.package if isinstance(package, SourceFlag) else package)

    

# type and constructor ParamSig
@dataclass(frozen=True, eq=True)
class ParamSig:
    key : str
    type : type
    optional : bool


def make_ParamSig(
    key : str,
    type : type,
    optional : bool
) -> ParamSig:
    return ParamSig(
        key,
        type,
        optional)

def update_ParamSig(source_ParamSig : ParamSig,
    key : Union[str, SourceFlag] = SourceFlag(),
    type : Union[type, SourceFlag] = SourceFlag(),
    optional : Union[bool, SourceFlag] = SourceFlag()
) -> ParamSig:
    return ParamSig(
        source_ParamSig.key if isinstance(key, SourceFlag) else key, 
        source_ParamSig.type if isinstance(type, SourceFlag) else type, 
        source_ParamSig.optional if isinstance(optional, SourceFlag) else optional)

    

# type and constructor VarLen
@dataclass(frozen=True, eq=True)
class VarLen:
    pass


def make_VarLen(
) -> VarLen:
    return VarLen()

def update_VarLen(source_VarLen : VarLen
) -> VarLen:
    return VarLen()

    

# type and constructor InherAux
@dataclass(frozen=True, eq=True)
class InherAux:
    package : PMap[str, ModulePackage]
    external_path : str
    internal_path : str
    in_class : bool
    global_env : PMap[str, Declaration]
    nonlocal_env : PMap[str, Declaration]
    local_env : PMap[str, Declaration]
    declared_globals : PSet[str]
    declared_nonlocals : PSet[str]
    usage_env : PMap[str, Usage]
    observed_types : tuple[type, ...]
    class_env : PMap[str, ClassRecord]


def make_InherAux(
    package : PMap[str, ModulePackage] = m(),
    external_path : str = '',
    internal_path : str = '',
    in_class : bool = False,
    global_env : PMap[str, Declaration] = m(),
    nonlocal_env : PMap[str, Declaration] = m(),
    local_env : PMap[str, Declaration] = m(),
    declared_globals : PSet[str] = s(),
    declared_nonlocals : PSet[str] = s(),
    usage_env : PMap[str, Usage] = m(),
    observed_types : tuple[type, ...] = (),
    class_env : PMap[str, ClassRecord] = m()
) -> InherAux:
    return InherAux(
        package,
        external_path,
        internal_path,
        in_class,
        global_env,
        nonlocal_env,
        local_env,
        declared_globals,
        declared_nonlocals,
        usage_env,
        observed_types,
        class_env)

def update_InherAux(source_InherAux : InherAux,
    package : Union[PMap[str, ModulePackage], SourceFlag] = SourceFlag(),
    external_path : Union[str, SourceFlag] = SourceFlag(),
    internal_path : Union[str, SourceFlag] = SourceFlag(),
    in_class : Union[bool, SourceFlag] = SourceFlag(),
    global_env : Union[PMap[str, Declaration], SourceFlag] = SourceFlag(),
    nonlocal_env : Union[PMap[str, Declaration], SourceFlag] = SourceFlag(),
    local_env : Union[PMap[str, Declaration], SourceFlag] = SourceFlag(),
    declared_globals : Union[PSet[str], SourceFlag] = SourceFlag(),
    declared_nonlocals : Union[PSet[str], SourceFlag] = SourceFlag(),
    usage_env : Union[PMap[str, Usage], SourceFlag] = SourceFlag(),
    observed_types : Union[tuple[type, ...], SourceFlag] = SourceFlag(),
    class_env : Union[PMap[str, ClassRecord], SourceFlag] = SourceFlag()
) -> InherAux:
    return InherAux(
        source_InherAux.package if isinstance(package, SourceFlag) else package, 
        source_InherAux.external_path if isinstance(external_path, SourceFlag) else external_path, 
        source_InherAux.internal_path if isinstance(internal_path, SourceFlag) else internal_path, 
        source_InherAux.in_class if isinstance(in_class, SourceFlag) else in_class, 
        source_InherAux.global_env if isinstance(global_env, SourceFlag) else global_env, 
        source_InherAux.nonlocal_env if isinstance(nonlocal_env, SourceFlag) else nonlocal_env, 
        source_InherAux.local_env if isinstance(local_env, SourceFlag) else local_env, 
        source_InherAux.declared_globals if isinstance(declared_globals, SourceFlag) else declared_globals, 
        source_InherAux.declared_nonlocals if isinstance(declared_nonlocals, SourceFlag) else declared_nonlocals, 
        source_InherAux.usage_env if isinstance(usage_env, SourceFlag) else usage_env, 
        source_InherAux.observed_types if isinstance(observed_types, SourceFlag) else observed_types, 
        source_InherAux.class_env if isinstance(class_env, SourceFlag) else class_env)

    

# type and constructor SynthAux
@dataclass(frozen=True, eq=True)
class SynthAux:
    class_additions : PMap[str, ClassRecord]
    decl_subtractions : PSet[str]
    decl_additions : PMap[str, Declaration]
    declared_globals : PSet[str]
    declared_nonlocals : PSet[str]
    usage_additions : PMap[str, Usage]
    cmp_names : tuple[str, ...]
    observed_types : tuple[type, ...]
    kw_types : PMap[str, type]
    return_types : tuple[type, ...]
    yield_types : tuple[type, ...]
    var_types : tuple[VarType, ...]
    protocol : bool
    param_sig : Optional[ParamSig]
    pos_param_types : tuple[type, ...]
    pos_kw_param_sigs : tuple[ParamSig, ...]
    splat_pos_param_type : Optional[type]
    kw_param_sigs : tuple[ParamSig, ...]
    splat_kw_param_type : Optional[type]
    import_names : PMap[str, str]


def make_SynthAux(
    class_additions : PMap[str, ClassRecord] = m(),
    decl_subtractions : PSet[str] = s(),
    decl_additions : PMap[str, Declaration] = m(),
    declared_globals : PSet[str] = s(),
    declared_nonlocals : PSet[str] = s(),
    usage_additions : PMap[str, Usage] = m(),
    cmp_names : tuple[str, ...] = (),
    observed_types : tuple[type, ...] = (),
    kw_types : PMap[str, type] = m(),
    return_types : tuple[type, ...] = (),
    yield_types : tuple[type, ...] = (),
    var_types : tuple[VarType, ...] = (),
    protocol : bool = False,
    param_sig : Optional[ParamSig] = None,
    pos_param_types : tuple[type, ...] = (),
    pos_kw_param_sigs : tuple[ParamSig, ...] = (),
    splat_pos_param_type : Optional[type] = None,
    kw_param_sigs : tuple[ParamSig, ...] = (),
    splat_kw_param_type : Optional[type] = None,
    import_names : PMap[str, str] = m()
) -> SynthAux:
    return SynthAux(
        class_additions,
        decl_subtractions,
        decl_additions,
        declared_globals,
        declared_nonlocals,
        usage_additions,
        cmp_names,
        observed_types,
        kw_types,
        return_types,
        yield_types,
        var_types,
        protocol,
        param_sig,
        pos_param_types,
        pos_kw_param_sigs,
        splat_pos_param_type,
        kw_param_sigs,
        splat_kw_param_type,
        import_names)

def update_SynthAux(source_SynthAux : SynthAux,
    class_additions : Union[PMap[str, ClassRecord], SourceFlag] = SourceFlag(),
    decl_subtractions : Union[PSet[str], SourceFlag] = SourceFlag(),
    decl_additions : Union[PMap[str, Declaration], SourceFlag] = SourceFlag(),
    declared_globals : Union[PSet[str], SourceFlag] = SourceFlag(),
    declared_nonlocals : Union[PSet[str], SourceFlag] = SourceFlag(),
    usage_additions : Union[PMap[str, Usage], SourceFlag] = SourceFlag(),
    cmp_names : Union[tuple[str, ...], SourceFlag] = SourceFlag(),
    observed_types : Union[tuple[type, ...], SourceFlag] = SourceFlag(),
    kw_types : Union[PMap[str, type], SourceFlag] = SourceFlag(),
    return_types : Union[tuple[type, ...], SourceFlag] = SourceFlag(),
    yield_types : Union[tuple[type, ...], SourceFlag] = SourceFlag(),
    var_types : Union[tuple[VarType, ...], SourceFlag] = SourceFlag(),
    protocol : Union[bool, SourceFlag] = SourceFlag(),
    param_sig : Union[Optional[ParamSig], SourceFlag] = SourceFlag(),
    pos_param_types : Union[tuple[type, ...], SourceFlag] = SourceFlag(),
    pos_kw_param_sigs : Union[tuple[ParamSig, ...], SourceFlag] = SourceFlag(),
    splat_pos_param_type : Union[Optional[type], SourceFlag] = SourceFlag(),
    kw_param_sigs : Union[tuple[ParamSig, ...], SourceFlag] = SourceFlag(),
    splat_kw_param_type : Union[Optional[type], SourceFlag] = SourceFlag(),
    import_names : Union[PMap[str, str], SourceFlag] = SourceFlag()
) -> SynthAux:
    return SynthAux(
        source_SynthAux.class_additions if isinstance(class_additions, SourceFlag) else class_additions, 
        source_SynthAux.decl_subtractions if isinstance(decl_subtractions, SourceFlag) else decl_subtractions, 
        source_SynthAux.decl_additions if isinstance(decl_additions, SourceFlag) else decl_additions, 
        source_SynthAux.declared_globals if isinstance(declared_globals, SourceFlag) else declared_globals, 
        source_SynthAux.declared_nonlocals if isinstance(declared_nonlocals, SourceFlag) else declared_nonlocals, 
        source_SynthAux.usage_additions if isinstance(usage_additions, SourceFlag) else usage_additions, 
        source_SynthAux.cmp_names if isinstance(cmp_names, SourceFlag) else cmp_names, 
        source_SynthAux.observed_types if isinstance(observed_types, SourceFlag) else observed_types, 
        source_SynthAux.kw_types if isinstance(kw_types, SourceFlag) else kw_types, 
        source_SynthAux.return_types if isinstance(return_types, SourceFlag) else return_types, 
        source_SynthAux.yield_types if isinstance(yield_types, SourceFlag) else yield_types, 
        source_SynthAux.var_types if isinstance(var_types, SourceFlag) else var_types, 
        source_SynthAux.protocol if isinstance(protocol, SourceFlag) else protocol, 
        source_SynthAux.param_sig if isinstance(param_sig, SourceFlag) else param_sig, 
        source_SynthAux.pos_param_types if isinstance(pos_param_types, SourceFlag) else pos_param_types, 
        source_SynthAux.pos_kw_param_sigs if isinstance(pos_kw_param_sigs, SourceFlag) else pos_kw_param_sigs, 
        source_SynthAux.splat_pos_param_type if isinstance(splat_pos_param_type, SourceFlag) else splat_pos_param_type, 
        source_SynthAux.kw_param_sigs if isinstance(kw_param_sigs, SourceFlag) else kw_param_sigs, 
        source_SynthAux.splat_kw_param_type if isinstance(splat_kw_param_type, SourceFlag) else splat_kw_param_type, 
        source_SynthAux.import_names if isinstance(import_names, SourceFlag) else import_names)

    

# type and constructor Declaration
@dataclass(frozen=True, eq=True)
class Declaration:
    annotated : bool
    constant : bool
    initialized : bool
    type : type
    decorator_types : tuple[type, ...]


def make_Declaration(
    annotated : bool,
    constant : bool,
    initialized : bool = False,
    type : type = AnyType(),
    decorator_types : tuple[type, ...] = ()
) -> Declaration:
    return Declaration(
        annotated,
        constant,
        initialized,
        type,
        decorator_types)

def update_Declaration(source_Declaration : Declaration,
    annotated : Union[bool, SourceFlag] = SourceFlag(),
    constant : Union[bool, SourceFlag] = SourceFlag(),
    initialized : Union[bool, SourceFlag] = SourceFlag(),
    type : Union[type, SourceFlag] = SourceFlag(),
    decorator_types : Union[tuple[type, ...], SourceFlag] = SourceFlag()
) -> Declaration:
    return Declaration(
        source_Declaration.annotated if isinstance(annotated, SourceFlag) else annotated, 
        source_Declaration.constant if isinstance(constant, SourceFlag) else constant, 
        source_Declaration.initialized if isinstance(initialized, SourceFlag) else initialized, 
        source_Declaration.type if isinstance(type, SourceFlag) else type, 
        source_Declaration.decorator_types if isinstance(decorator_types, SourceFlag) else decorator_types)

    

# type and constructor Usage
@dataclass(frozen=True, eq=True)
class Usage:
    updated : bool


def make_Usage(
    updated : bool = False
) -> Usage:
    return Usage(
        updated)

def update_Usage(source_Usage : Usage,
    updated : Union[bool, SourceFlag] = SourceFlag()
) -> Usage:
    return Usage(
        source_Usage.updated if isinstance(updated, SourceFlag) else updated)

     
    

# type semantic_check
@dataclass(frozen=True, eq=True)
class semantic_check(Exception, ABC):
    # @abstractmethod
    def match(self, handlers : SemanticCheckHandlers[T]) -> T:
        raise Exception()


# constructors for type semantic_check

@dataclass(frozen=True, eq=True)
class LookupTypeCheck(semantic_check):


    def match(self, handlers : SemanticCheckHandlers[T]) -> T:
        return handlers.case_LookupTypeCheck(self)

def make_LookupTypeCheck(
) -> semantic_check:
    return LookupTypeCheck(
    )

def update_LookupTypeCheck(source_LookupTypeCheck : LookupTypeCheck
) -> LookupTypeCheck:
    return LookupTypeCheck(
    )

        

@dataclass(frozen=True, eq=True)
class ApplyArgTypeCheck(semantic_check):


    def match(self, handlers : SemanticCheckHandlers[T]) -> T:
        return handlers.case_ApplyArgTypeCheck(self)

def make_ApplyArgTypeCheck(
) -> semantic_check:
    return ApplyArgTypeCheck(
    )

def update_ApplyArgTypeCheck(source_ApplyArgTypeCheck : ApplyArgTypeCheck
) -> ApplyArgTypeCheck:
    return ApplyArgTypeCheck(
    )

        

@dataclass(frozen=True, eq=True)
class ApplyRatorTypeCheck(semantic_check):


    def match(self, handlers : SemanticCheckHandlers[T]) -> T:
        return handlers.case_ApplyRatorTypeCheck(self)

def make_ApplyRatorTypeCheck(
) -> semantic_check:
    return ApplyRatorTypeCheck(
    )

def update_ApplyRatorTypeCheck(source_ApplyRatorTypeCheck : ApplyRatorTypeCheck
) -> ApplyRatorTypeCheck:
    return ApplyRatorTypeCheck(
    )

        

@dataclass(frozen=True, eq=True)
class SplatKeywordTypeCheck(semantic_check):


    def match(self, handlers : SemanticCheckHandlers[T]) -> T:
        return handlers.case_SplatKeywordTypeCheck(self)

def make_SplatKeywordTypeCheck(
) -> semantic_check:
    return SplatKeywordTypeCheck(
    )

def update_SplatKeywordTypeCheck(source_SplatKeywordTypeCheck : SplatKeywordTypeCheck
) -> SplatKeywordTypeCheck:
    return SplatKeywordTypeCheck(
    )

        

@dataclass(frozen=True, eq=True)
class ReturnTypeCheck(semantic_check):


    def match(self, handlers : SemanticCheckHandlers[T]) -> T:
        return handlers.case_ReturnTypeCheck(self)

def make_ReturnTypeCheck(
) -> semantic_check:
    return ReturnTypeCheck(
    )

def update_ReturnTypeCheck(source_ReturnTypeCheck : ReturnTypeCheck
) -> ReturnTypeCheck:
    return ReturnTypeCheck(
    )

        

@dataclass(frozen=True, eq=True)
class UnifyTypeCheck(semantic_check):


    def match(self, handlers : SemanticCheckHandlers[T]) -> T:
        return handlers.case_UnifyTypeCheck(self)

def make_UnifyTypeCheck(
) -> semantic_check:
    return UnifyTypeCheck(
    )

def update_UnifyTypeCheck(source_UnifyTypeCheck : UnifyTypeCheck
) -> UnifyTypeCheck:
    return UnifyTypeCheck(
    )

        

@dataclass(frozen=True, eq=True)
class AssignTypeCheck(semantic_check):


    def match(self, handlers : SemanticCheckHandlers[T]) -> T:
        return handlers.case_AssignTypeCheck(self)

def make_AssignTypeCheck(
) -> semantic_check:
    return AssignTypeCheck(
    )

def update_AssignTypeCheck(source_AssignTypeCheck : AssignTypeCheck
) -> AssignTypeCheck:
    return AssignTypeCheck(
    )

        

@dataclass(frozen=True, eq=True)
class IterateTypeCheck(semantic_check):


    def match(self, handlers : SemanticCheckHandlers[T]) -> T:
        return handlers.case_IterateTypeCheck(self)

def make_IterateTypeCheck(
) -> semantic_check:
    return IterateTypeCheck(
    )

def update_IterateTypeCheck(source_IterateTypeCheck : IterateTypeCheck
) -> IterateTypeCheck:
    return IterateTypeCheck(
    )

        

@dataclass(frozen=True, eq=True)
class LookupDecCheck(semantic_check):


    def match(self, handlers : SemanticCheckHandlers[T]) -> T:
        return handlers.case_LookupDecCheck(self)

def make_LookupDecCheck(
) -> semantic_check:
    return LookupDecCheck(
    )

def update_LookupDecCheck(source_LookupDecCheck : LookupDecCheck
) -> LookupDecCheck:
    return LookupDecCheck(
    )

        

@dataclass(frozen=True, eq=True)
class LookupInitCheck(semantic_check):


    def match(self, handlers : SemanticCheckHandlers[T]) -> T:
        return handlers.case_LookupInitCheck(self)

def make_LookupInitCheck(
) -> semantic_check:
    return LookupInitCheck(
    )

def update_LookupInitCheck(source_LookupInitCheck : LookupInitCheck
) -> LookupInitCheck:
    return LookupInitCheck(
    )

        

@dataclass(frozen=True, eq=True)
class UpdateCheck(semantic_check):


    def match(self, handlers : SemanticCheckHandlers[T]) -> T:
        return handlers.case_UpdateCheck(self)

def make_UpdateCheck(
) -> semantic_check:
    return UpdateCheck(
    )

def update_UpdateCheck(source_UpdateCheck : UpdateCheck
) -> UpdateCheck:
    return UpdateCheck(
    )

        

@dataclass(frozen=True, eq=True)
class DeclareCheck(semantic_check):


    def match(self, handlers : SemanticCheckHandlers[T]) -> T:
        return handlers.case_DeclareCheck(self)

def make_DeclareCheck(
) -> semantic_check:
    return DeclareCheck(
    )

def update_DeclareCheck(source_DeclareCheck : DeclareCheck
) -> DeclareCheck:
    return DeclareCheck(
    )

        

# case handlers for type semantic_check
@dataclass(frozen=True, eq=True)
class SemanticCheckHandlers(Generic[T]):
    case_LookupTypeCheck : Callable[[LookupTypeCheck], T]
    case_ApplyArgTypeCheck : Callable[[ApplyArgTypeCheck], T]
    case_ApplyRatorTypeCheck : Callable[[ApplyRatorTypeCheck], T]
    case_SplatKeywordTypeCheck : Callable[[SplatKeywordTypeCheck], T]
    case_ReturnTypeCheck : Callable[[ReturnTypeCheck], T]
    case_UnifyTypeCheck : Callable[[UnifyTypeCheck], T]
    case_AssignTypeCheck : Callable[[AssignTypeCheck], T]
    case_IterateTypeCheck : Callable[[IterateTypeCheck], T]
    case_LookupDecCheck : Callable[[LookupDecCheck], T]
    case_LookupInitCheck : Callable[[LookupInitCheck], T]
    case_UpdateCheck : Callable[[UpdateCheck], T]
    case_DeclareCheck : Callable[[DeclareCheck], T]


# matching for type semantic_check
def match_semantic_check(o : semantic_check, handlers : SemanticCheckHandlers[T]) -> T :
    return o.match(handlers)
     
    