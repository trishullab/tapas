from __future__ import annotations

from tapas_base import construct_def
from tapas_base.construct_def import Constructor, Field


singles = [

    # TODO: add abstract methods 
    # related to universal type in PLT
    # concrete type if it has no abstract_methods and no type parameters 
    Constructor("ClassRecord", [], [
        # class type params are determined by use of Generic constructor
        Field("key", "str", ""),
        Field("type_params", "tuple[VarType, ...]", ""),
        Field("super_types", "tuple[TypeType, ...]", ""),
        Field("static_fields", "InsertOrderMap[str, type]", ""),
        Field("instance_fields", "InsertOrderMap[str, type]", ""),
        Field("protocol", "bool", "False")
    ]),

    Constructor("ModulePackage", [], [
        # TODO: update module to contain declaration instead of merely the type. 
        # Need to know if constant/initialized.
        Field("module", "InsertOrderMap[str, Declaration]", "iom()"),
        Field("class_env", "InsertOrderMap[str, ClassRecord]", "iom()"),
        Field("package", "InsertOrderMap[str, ModulePackage]", "iom()"),
    ]),

    Constructor("ParamSig", [], [
        Field("key", "str", ""),
        Field("type", "type", ""),
        Field("optional", "bool", "")
    ]),

    Constructor("VarLen", [], []),

    Constructor("InherAux", [], [
        Field("package", "InsertOrderMap[str, ModulePackage]", "iom()"),
        Field("external_path", "str", "''"),
        Field("internal_path", "str", "''"),
        Field("method_kind", "Optional[method_kind]", "None"),
        Field("in_class", "bool", "False"),

        Field("global_env", "InsertOrderMap[str, Declaration]", "iom()"),
        Field("nonlocal_env", "InsertOrderMap[str, Declaration]", "iom()"),
        Field("local_env", "InsertOrderMap[str, Declaration]", "iom()"),
        Field("declared_globals", "PSet[str]", "s()"),
        Field("declared_nonlocals", "PSet[str]", "s()"),

        Field("usage_env", "PMap[str, Usage]", "m()"),
        Field("observed_types", "tuple[type, ...]", "()"),
        Field("class_env", "InsertOrderMap[str, ClassRecord]", "iom()"), # internal_path |-> ClassRecord

        Field("anchor_symbol", "str", "''")


    ]),

    Constructor("SynthAux", [], [


        Field("static_field_additions", "InsertOrderMap[str, type]", "iom()"),
        Field("instance_field_additions", "InsertOrderMap[str, type]", "iom()"),

        Field("class_additions", "InsertOrderMap[str, ClassRecord]", "iom()"),

        Field("decl_subtractions", "PSet[str]", "s()"),
        Field("decl_additions", "InsertOrderMap[str, Declaration]", "iom()"),
        Field("declared_globals", "PSet[str]", "s()"),
        Field("declared_nonlocals", "PSet[str]", "s()"),

        Field("usage_additions", "PMap[str, Usage]", "m()"), # TODO: add more info like type info - PMap[str, Usage]
        Field("nested_usages", "PMap[str, tuple[Usage, ...]]", "m()"),
        Field("cmp_names", "tuple[str, ...]", "()"),

        Field("observed_types", "tuple[type, ...]", "()"),
        Field("kw_types", "PMap[str, type]", "m()"),

        Field("return_types", "tuple[type, ...]", "()"),
        Field("yield_types", "tuple[type, ...]", "()"),

        Field("var_types", "tuple[VarType, ...]", "()"),

        Field("protocol", "bool", "False"),

        # param that is collected at a lower level
        # (key, type, optional)
        Field("param_sig", "Optional[ParamSig]", "None"),

        # params according to the context within which they occur 
        Field("pos_param_types", "tuple[type, ...]", "()"),
        Field("pos_kw_param_sigs", "tuple[ParamSig, ...]", "()"),
        Field("bundle_pos_param_type", "Optional[type]", "None"),
        Field("kw_param_sigs", "tuple[ParamSig, ...]", "()"),
        Field("bundle_kw_param_type", "Optional[type]", "None"),

        # import names { alias : module source }
        Field("import_names", "InsertOrderMap[str, str]", "iom()")

    ]),

    Constructor("Declaration", [], [
        Field("updatable", "Optional[type]", ""), # def/class are constant; assignment is not constant

        Field("initialized", "bool", "False"),
        Field("type", "type", "AnyType()"),
        Field("decorator_types", "tuple[type, ...]", "()"),
        Field("overloading", "bool", "False")
    ]),

    Constructor("Usage", [], [
        Field("backref", "bool", ""),
        Field("updated", "bool", "False"),
        # Field("type", "type", "AnyType()"), # expectation

        # if field_usages is not empty, then the function types should be empty
        # Field("field_usages", "PMap[str, Usage]", "m()"), # expectations

        # if the following are not empty, then the expected type should be a FunctionType/TypeType
        # and expected_field_types should be empty.
        # The observations/expectations of a function are reversed from that of a function definition.
        # Field("pos_types", "tuple[type, ...]", "()"), # observation
        # Field("kw_types", "PMap[str, type]", "m()"), # observation
        # Field("return_type", "type | None", "None"), # expectation
    ]),

]

choices = {

    "method_kind" : [
        Constructor("InstanceMethod", [], []),
        Constructor("StaticMethod", [], []),
        Constructor("ClassMethod", [], []),
    ],

    "variant" : [
        Constructor("CoVariant", [], []),
        Constructor("ContraVariant", [], []),
        Constructor("NoVariant", [], []),
    ],

    "type" : [

        Constructor("ProtocolType", [], []),
        Constructor("GenericType", [], []),

        # type for the @overload decorator
        Constructor("OverloadType", [], [ ]),

        Constructor("TypeType", [], [
            Field("content", "type", ""),
        ]),

        Constructor("VarType", [], [
            Field("name", "str", ""),
            Field("version", "int", "0"),
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
            Field("static_key", "str", "''"),
            # args for these may only be associated with param by position 
            Field("pos_param_types", "tuple[type, ...]", "()"),

            # args for these may be associated with param by either position or key
            # once a key is used for one, then it's required for subsequent arguments
            # default value makes argument optional
            # (key, type, optional)
            Field("pos_kw_param_sigs", "tuple[ParamSig, ...]", "()"),

            Field("bundle_pos_param_type", "Optional[type]", "None"),

            # args for these may only be associated with param by key
            # (key, type, optional)
            Field("kw_param_sigs", "tuple[ParamSig, ...]", "()"),
            Field("bundle_kw_param_type", "Optional[type]", "None"),

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
            Field("class_version", "int", "0"),
            Field("type_args", "tuple[type, ...]", "()"),
        ]),

        Constructor("TupleLitType", [], [
            Field("item_types", "tuple[type, ...]", "()"),
        ]),

        Constructor("VariedTupleType", [], [
            Field("item_type", "type", "AnyType()"),
        ]),

        Constructor("NamedTupleType", [], [
            Field("name", "str", "''"),
            Field("fields", "tuple[str, ...]", "()"),
        ]),
            
        Constructor("ListLitType", [], [
            Field("item_types", "tuple[type, ...]", "()"),
        ]),

        Constructor("DictLitType", [], [
            Field("pair_types", "tuple[tuple[type, type], ...]", "()"),
        ]),

        Constructor("TrueType", [], []),
        Constructor("FalseType", [], []),
        Constructor("IntLitType", [], [
            Field("literal", "str", "''"),
        ]),
        Constructor("FloatLitType", [], [
            Field("literal", "str", "''"),
        ]),
        Constructor("StrLitType", [], [
            Field("literal", "str", "''"),
        ]),

    ],
}


choices_type_base = {
    ('semantic_check', 'Exception') : [
        Constructor("LookupTypeCheck", [], []),
        Constructor("ApplyArgTypeCheck", [], []),
        Constructor("ApplyRatorTypeCheck", [], []),
        Constructor("SplatKeywordArgTypeCheck", [], []),
        Constructor("ReturnTypeCheck", [], []),
        Constructor("UnifyTypeCheck", [], []),
        Constructor("AssignTypeCheck", [], []),
        Constructor("IterateTypeCheck", [], []),
        Constructor("LookupDecCheck", [], []),
        Constructor("LookupInitCheck", [], []),
        Constructor("UpdateCheck", [], []),
        Constructor("DeclareCheck", [], []),
        Constructor("BranchDeclareCheck", [], []),
    ]
}



def generate_content():
    return construct_def.generate_content(f"""
from pyrsistent.typing import PMap, PSet
from pyrsistent import pmap, m, pset, s
from tapas_base.util_system import InsertOrderMap, iom 
from tapas_base.abstract_token_construct_autogen import abstract_token 
from tapas_lib.python_ast_construct_autogen import ast 
    """, singles, choices) + construct_def.generate_choices_type_base(choices_type_base)