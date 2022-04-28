from __future__ import annotations

from lib import construct_def
from lib.construct_def import Constructor, Field


singles = [


    # TODO: add abstract methods 
    # related to universal type in PLT
    # concrete type if it has no abstract_methods and no type parameters 
    Constructor("ClassRecord", [], [
        # class type params are determined by use of Generic constructor
        Field("key", "str", ""),
        Field("type_params", "tuple[VarType, ...]", ""),
        Field("super_types", "tuple[type, ...]", ""),
        Field("static_fields", "PMap[str, type]", ""),
        Field("instance_fields", "PMap[str, type]", "")
    ]),

    Constructor("ModulePackage", [], [
        Field("module", "PMap[str, type]", "m()"),
        Field("class_env", "PMap[str, ClassRecord]", "m()"),
        Field("package", "PMap[str, ModulePackage]", "m()"),
    ]),

    Constructor("ParamSig", [], [
        Field("key", "str", ""),
        Field("type", "type", ""),
        Field("optional", "bool", "")
    ]),

    Constructor("VarLen", [], []),

    Constructor("Provenance", [], [
        Field("initialized", "bool", "False"),
        Field("type", "type", "AnyType()"),
        Field("decorator_types", "tuple[type, ...]", "()")
    ]),

    Constructor("InherAux", [], [
        Field("package", "PMap[str, ModulePackage]", "m()"),
        Field("external_path", "str", "''"),
        Field("internal_path", "str", "''"),
        Field("global_env", "PMap[str, Provenance]", "m()"),
        Field("nonlocal_env", "PMap[str, Provenance]", "m()"),
        Field("local_env", "PMap[str, Provenance]", "m()"),
        Field("class_env", "PMap[str, ClassRecord]", "m()"), # internal_path |-> ClassRecord
    ]),

    Constructor("SynthAux", [], [

        Field("class_additions", "PMap[str, ClassRecord]", "m()"),

        Field("env_subtractions", "PSet[str]", "s()"),
        Field("env_additions", "PMap[str, Provenance]", "m()"),
        Field("names", "PSet[str]", "s()"),


        Field("method_names", "tuple[str, ...]", "()"),

        Field("expr_types", "tuple[type, ...]", "()"),
        Field("kw_types", "PMap[str, type]", "m()"),

        Field("return_types", "tuple[type, ...]", "()"),
        Field("yield_types", "tuple[type, ...]", "()"),

        Field("var_types", "tuple[VarType, ...]", "()"),

        # param that is collected at a lower level
        # (key, type, optional)
        Field("param_sig", "Optional[ParamSig]", "None"),

        # params according to the context within which they occur 
        Field("pos_param_types", "tuple[type, ...]", "()"),
        Field("pos_kw_param_sigs", "tuple[ParamSig, ...]", "()"),
        Field("splat_pos_param_type", "Optional[type]", "None"),
        Field("kw_param_sigs", "tuple[ParamSig, ...]", "()"),
        Field("splat_kw_param_type", "Optional[type]", "None"),

        # import names { alias : module source }
        Field("import_names", "PMap[str, str]", "m()")



    ]),

]

choices = {

    "variant" : [
        Constructor("CoVariant", [], []),
        Constructor("ContraVariant", [], []),
        Constructor("NoVariant", [], []),
    ],

    "type" : [

        Constructor("TypeType", [], [
            Field("content", "type", ""),
        ]),

        # TODO: should TypeType and AnnoType be merged?
        Constructor("AnnoType", [], [
            Field("content", "type", "")
        ]),

        Constructor("VarType", [], [
            Field("name", "str", ""),
            Field("variant", "variant", "NoVariant()")
        ]),

        Constructor("EllipType", [], []),

        # this means something is untyped and cannot trigger a type error 
        Constructor("AnyType", [], []),

        # related to top in PLT
        Constructor("ObjectType", [], []),

        # related to bottom type in PLT
        Constructor("NoneType", [], []),

        # static product type
        Constructor("ModuleType", [], [
            Field("key", "str", "")
        ]),

        # universal type if it contains params 
        Constructor("FunctionType", [], [
            # args for these may only be associated with param by position 
            Field("pos_param_types", "tuple[type, ...]", "()"),

            # args for these may be associated with param by either position or key
            # once a key is used for one, then it's required for subsequent arguments
            # default value makes argument optional
            # (key, type, optional)
            Field("pos_kw_param_sigs", "tuple[ParamSig, ...]", "()"),

            Field("splat_pos_param_type", "Optional[type]", "None"),

            # args for these may only be associated with param by key
            # (key, type, optional)
            Field("kw_param_sigs", "tuple[ParamSig, ...]", "()"),
            Field("splat_kw_param_type", "Optional[type]", "None"),

            Field("return_type", "type", "AnyType()")
        ]),

        # related to sum type in PLT
        Constructor("UnionType", [], [
            Field("type_choices", "tuple[type, ...]", "")
        ]),

        # related to product type in PLT
        Constructor("InterType", [], [
            Field("type_components", "tuple[type, ...]", "")
        ]),

        # created from ClassType. Refers to the methods of the class
        # related to product type in PLT
        Constructor("RecordType", [], [
            Field("class_key", "str", ""),
            Field("class_uid", "int", "0"),
            Field("type_args", "tuple[type, ...]", "()"),
        ]),


        Constructor("FixedTupleType", [], [
            Field("item_types", "tuple[type, ...]", "()"),
        ]),

        Constructor("VariedTupleType", [], [
            Field("item_type", "type", "AnyType()"),
        ]),
            
        Constructor("MappingType", [], [
            Field("key_type", "type", "AnyType()"),
            Field("value_type", "type", "AnyType()"),
        ]),

        Constructor("DictType", [], [
            Field("key_type", "type", "AnyType()"),
            Field("value_type", "type", "AnyType()"),
        ]),

        Constructor("SetType", [], [
            Field("item_type", "type", "AnyType()"),
        ]),

        Constructor("IterableType", [], [
            Field("item_type", "type", "AnyType()"),
        ]),


        Constructor("DictKeysType", [], [
            Field("item_type", "type", "AnyType()"),
        ]),
        Constructor("DictValuesType", [], [
            Field("item_type", "type", "AnyType()"),
        ]),
        Constructor("DictItemsType", [], [
            Field("item_type", "type", "AnyType()"),
        ]),

        Constructor("SequenceType", [], [
            Field("item_type", "type", "AnyType()"),
        ]),

        Constructor("RangeType", [], [
            Field("item_type", "type", "AnyType()"),
        ]),

        Constructor("ListType", [], [
            Field("item_type", "type", "AnyType()"),
        ]),

        Constructor("ListLitType", [], [
            Field("item_types", "tuple[type, ...]", "()"),
        ]),

        Constructor("GeneratorType", [], [
            Field("yield_type", "type", "NoneType()"),
            Field("return_type", "type", "NoneType()"),
        ]),

        Constructor("BoolType", [], []),
        Constructor("TrueType", [], []),
        Constructor("FalseType", [], []),
        Constructor("IntType", [], []),
        Constructor("IntLitType", [], [
            Field("literal", "str", "''"),
        ]),
        Constructor("FloatType", [], []),
        Constructor("FloatLitType", [], [
            Field("literal", "str", "''"),
        ]),
        Constructor("StrType", [], []),
        Constructor("StrLitType", [], [
            Field("literal", "str", "''"),
        ]),
        Constructor("SliceType", [], [
            Field("start", "type", "AnyType()"),
            Field("stop", "type", "AnyType()"),
            Field("step", "type", "AnyType()")
        ]),

    ]

}



def generate_content():
    return construct_def.generate_content(f"""
from pyrsistent.typing import PMap, PSet
from pyrsistent import pmap, m, pset, s
from lib.abstract_token_system import abstract_token 
from lib.python_ast_construct_autogen import ast 
from lib import python_ast_system as ast_sys
    """, singles, choices)