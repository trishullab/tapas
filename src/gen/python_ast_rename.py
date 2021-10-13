
from __future__ import annotations
from lib import production_instance as prod_inst 
from gen.python_ast import *
from gen.line_format import InLine, NewLine, IndentLine
import sys

sys.setrecursionlimit(10**6)



def rename_Module(
    o : Module, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> Module:

    return Module (

        rename_statements(
            o.body,
            global_map,
            nonlocal_map,
            local_map
        )    )



def rename_CompareRight(
    o : CompareRight, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> CompareRight:

    return CompareRight (

        rename_cmpop(
            o.op,
            global_map,
            nonlocal_map,
            local_map
        ),         rename_expr(
            o.rand,
            global_map,
            nonlocal_map,
            local_map
        )    )



def rename_ExceptHandler(
    o : ExceptHandler, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> ExceptHandler:

    return ExceptHandler (

        rename_except_arg(
            o.arg,
            global_map,
            nonlocal_map,
            local_map
        ),         rename_statements(
            o.body,
            global_map,
            nonlocal_map,
            local_map
        )    )



def rename_Param(
    o : Param, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> Param:

    return Param (

        o.id,         rename_param_type(
            o.type,
            global_map,
            nonlocal_map,
            local_map
        ),         rename_param_default(
            o.default,
            global_map,
            nonlocal_map,
            local_map
        )    )



def rename_Field(
    o : Field, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> Field:

    return Field (

        rename_expr(
            o.key,
            global_map,
            nonlocal_map,
            local_map
        ),         rename_expr(
            o.content,
            global_map,
            nonlocal_map,
            local_map
        )    )



def rename_ImportName(
    o : ImportName, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> ImportName:

    return ImportName (

        o.name,         rename_alias(
            o.as_name,
            global_map,
            nonlocal_map,
            local_map
        )    )



def rename_Withitem(
    o : Withitem, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> Withitem:

    return Withitem (

        rename_expr(
            o.contet,
            global_map,
            nonlocal_map,
            local_map
        ),         rename_alias_expr(
            o.target,
            global_map,
            nonlocal_map,
            local_map
        )    )



def rename_ClassDef(
    o : ClassDef, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> ClassDef:

    return ClassDef (

        o.name,         rename_bases(
            o.bs,
            global_map,
            nonlocal_map,
            local_map
        ),         rename_statements(
            o.body,
            global_map,
            nonlocal_map,
            local_map
        )    )



def rename_ElifBlock(
    o : ElifBlock, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> ElifBlock:

    return ElifBlock (

        rename_expr(
            o.test,
            global_map,
            nonlocal_map,
            local_map
        ),         rename_statements(
            o.body,
            global_map,
            nonlocal_map,
            local_map
        )    )



def rename_ElseBlock(
    o : ElseBlock, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> ElseBlock:

    return ElseBlock (

        rename_statements(
            o.body,
            global_map,
            nonlocal_map,
            local_map
        )    )



def rename_FinallyBlock(
    o : FinallyBlock, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> FinallyBlock:

    return FinallyBlock (

        rename_statements(
            o.body,
            global_map,
            nonlocal_map,
            local_map
        )    )



def rename_return_type(
    o : return_type, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> return_type:

    def handle_SomeReturnType(o : SomeReturnType): 

        return SomeReturnType(
            rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_NoReturnType(o : NoReturnType): 

        return NoReturnType(
        )


    return match_return_type(o, ReturnTypeHandlers(
        case_SomeReturnType = handle_SomeReturnType,  
        case_NoReturnType = handle_NoReturnType 
    ))



def rename_module_id(
    o : module_id, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> module_id:

    def handle_SomeModuleId(o : SomeModuleId): 

        return SomeModuleId(
            o.content        )

    def handle_NoModuleId(o : NoModuleId): 

        return NoModuleId(
        )


    return match_module_id(o, ModuleIdHandlers(
        case_SomeModuleId = handle_SomeModuleId,  
        case_NoModuleId = handle_NoModuleId 
    ))



def rename_except_arg(
    o : except_arg, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> except_arg:

    def handle_SomeExceptArg(o : SomeExceptArg): 

        return SomeExceptArg(
            rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_SomeExceptArgName(o : SomeExceptArgName): 

        return SomeExceptArgName(
            rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            ),             o.name        )

    def handle_NoExceptArg(o : NoExceptArg): 

        return NoExceptArg(
        )


    return match_except_arg(o, ExceptArgHandlers(
        case_SomeExceptArg = handle_SomeExceptArg,  
        case_SomeExceptArgName = handle_SomeExceptArgName,  
        case_NoExceptArg = handle_NoExceptArg 
    ))



def rename_param_type(
    o : param_type, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> param_type:

    def handle_SomeParamType(o : SomeParamType): 

        return SomeParamType(
            rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_NoParamType(o : NoParamType): 

        return NoParamType(
        )


    return match_param_type(o, ParamTypeHandlers(
        case_SomeParamType = handle_SomeParamType,  
        case_NoParamType = handle_NoParamType 
    ))



def rename_param_default(
    o : param_default, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> param_default:

    def handle_SomeParamDefault(o : SomeParamDefault): 

        return SomeParamDefault(
            rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_NoParamDefault(o : NoParamDefault): 

        return NoParamDefault(
        )


    return match_param_default(o, ParamDefaultHandlers(
        case_SomeParamDefault = handle_SomeParamDefault,  
        case_NoParamDefault = handle_NoParamDefault 
    ))



def rename_parameters_d(
    o : parameters_d, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> parameters_d:

    def handle_ConsKwParam(o : ConsKwParam): 

        return ConsKwParam(
            rename_Param(
                o.head,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_parameters_d(
                o.tail,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_SingleKwParam(o : SingleKwParam): 

        return SingleKwParam(
            rename_Param(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_DictionarySplatParam(o : DictionarySplatParam): 

        return DictionarySplatParam(
            rename_Param(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )


    return match_parameters_d(o, ParametersDHandlers(
        case_ConsKwParam = handle_ConsKwParam,  
        case_SingleKwParam = handle_SingleKwParam,  
        case_DictionarySplatParam = handle_DictionarySplatParam 
    ))



def rename_parameters_c(
    o : parameters_c, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> parameters_c:

    def handle_SingleListSplatParam(o : SingleListSplatParam): 

        return SingleListSplatParam(
            rename_Param(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_TransListSplatParam(o : TransListSplatParam): 

        return TransListSplatParam(
            rename_Param(
                o.head,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_parameters_d(
                o.tail,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_ParamsD(o : ParamsD): 

        return ParamsD(
            rename_parameters_d(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )


    return match_parameters_c(o, ParametersCHandlers(
        case_SingleListSplatParam = handle_SingleListSplatParam,  
        case_TransListSplatParam = handle_TransListSplatParam,  
        case_ParamsD = handle_ParamsD 
    ))



def rename_parameters_b(
    o : parameters_b, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> parameters_b:

    def handle_ConsParam(o : ConsParam): 

        return ConsParam(
            rename_Param(
                o.head,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_parameters_b(
                o.tail,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_SingleParam(o : SingleParam): 

        return SingleParam(
            rename_Param(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_ParamsC(o : ParamsC): 

        return ParamsC(
            rename_parameters_c(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )


    return match_parameters_b(o, ParametersBHandlers(
        case_ConsParam = handle_ConsParam,  
        case_SingleParam = handle_SingleParam,  
        case_ParamsC = handle_ParamsC 
    ))



def rename_parameters(
    o : parameters, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> parameters:

    def handle_ParamsA(o : ParamsA): 

        return ParamsA(
            rename_parameters_a(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_ParamsB(o : ParamsB): 

        return ParamsB(
            rename_parameters_b(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_NoParam(o : NoParam): 

        return NoParam(
        )


    return match_parameters(o, ParametersHandlers(
        case_ParamsA = handle_ParamsA,  
        case_ParamsB = handle_ParamsB,  
        case_NoParam = handle_NoParam 
    ))



def rename_parameters_a(
    o : parameters_a, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> parameters_a:

    def handle_ConsPosParam(o : ConsPosParam): 

        return ConsPosParam(
            rename_Param(
                o.head,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_parameters_a(
                o.tail,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_SinglePosParam(o : SinglePosParam): 

        return SinglePosParam(
            rename_Param(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_TransPosParam(o : TransPosParam): 

        return TransPosParam(
            rename_Param(
                o.head,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_parameters_b(
                o.tail,
                global_map,
                nonlocal_map,
                local_map
            )        )


    return match_parameters_a(o, ParametersAHandlers(
        case_ConsPosParam = handle_ConsPosParam,  
        case_SinglePosParam = handle_SinglePosParam,  
        case_TransPosParam = handle_TransPosParam 
    ))



def rename_keyword(
    o : keyword, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> keyword:

    def handle_NamedKeyword(o : NamedKeyword): 

        return NamedKeyword(
            o.name,             rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_SplatKeyword(o : SplatKeyword): 

        return SplatKeyword(
            rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )


    return match_keyword(o, KeywordHandlers(
        case_NamedKeyword = handle_NamedKeyword,  
        case_SplatKeyword = handle_SplatKeyword 
    ))



def rename_alias(
    o : alias, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> alias:

    def handle_SomeAlias(o : SomeAlias): 

        return SomeAlias(
            o.content        )

    def handle_NoAlias(o : NoAlias): 

        return NoAlias(
        )


    return match_alias(o, AliasHandlers(
        case_SomeAlias = handle_SomeAlias,  
        case_NoAlias = handle_NoAlias 
    ))



def rename_alias_expr(
    o : alias_expr, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> alias_expr:

    def handle_SomeAliasExpr(o : SomeAliasExpr): 

        return SomeAliasExpr(
            rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_NoAliasExpr(o : NoAliasExpr): 

        return NoAliasExpr(
        )


    return match_alias_expr(o, AliasExprHandlers(
        case_SomeAliasExpr = handle_SomeAliasExpr,  
        case_NoAliasExpr = handle_NoAliasExpr 
    ))



def rename_bases(
    o : bases, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> bases:

    def handle_SomeBases(o : SomeBases): 

        return SomeBases(
            rename_bases_a(
                o.bases,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_NoBases(o : NoBases): 

        return NoBases(
        )


    return match_bases(o, BasesHandlers(
        case_SomeBases = handle_SomeBases,  
        case_NoBases = handle_NoBases 
    ))



def rename_bases_a(
    o : bases_a, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> bases_a:

    def handle_ConsBase(o : ConsBase): 

        return ConsBase(
            rename_expr(
                o.head,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_bases_a(
                o.tail,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_SingleBase(o : SingleBase): 

        return SingleBase(
            rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_KeywordsBase(o : KeywordsBase): 

        return KeywordsBase(
            rename_keywords(
                o.kws,
                global_map,
                nonlocal_map,
                local_map
            )        )


    return match_bases_a(o, BasesAHandlers(
        case_ConsBase = handle_ConsBase,  
        case_SingleBase = handle_SingleBase,  
        case_KeywordsBase = handle_KeywordsBase 
    ))



def rename_keywords(
    o : keywords, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> keywords:

    def handle_ConsKeyword(o : ConsKeyword): 

        return ConsKeyword(
            rename_keyword(
                o.head,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_keywords(
                o.tail,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_SingleKeyword(o : SingleKeyword): 

        return SingleKeyword(
            rename_keyword(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )


    return match_keywords(o, KeywordsHandlers(
        case_ConsKeyword = handle_ConsKeyword,  
        case_SingleKeyword = handle_SingleKeyword 
    ))



def rename_comparisons(
    o : comparisons, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> comparisons:

    def handle_ConsCompareRight(o : ConsCompareRight): 

        return ConsCompareRight(
            rename_CompareRight(
                o.head,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_comparisons(
                o.tail,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_SingleCompareRight(o : SingleCompareRight): 

        return SingleCompareRight(
            rename_CompareRight(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )


    return match_comparisons(o, ComparisonsHandlers(
        case_ConsCompareRight = handle_ConsCompareRight,  
        case_SingleCompareRight = handle_SingleCompareRight 
    ))



def rename_option_expr(
    o : option_expr, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> option_expr:

    def handle_SomeExpr(o : SomeExpr): 

        return SomeExpr(
            rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_NoExpr(o : NoExpr): 

        return NoExpr(
        )


    return match_option_expr(o, OptionExprHandlers(
        case_SomeExpr = handle_SomeExpr,  
        case_NoExpr = handle_NoExpr 
    ))



def rename_comma_exprs(
    o : comma_exprs, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> comma_exprs:

    def handle_ConsExpr(o : ConsExpr): 

        return ConsExpr(
            rename_expr(
                o.head,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_comma_exprs(
                o.tail,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_SingleExpr(o : SingleExpr): 

        return SingleExpr(
            rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )


    return match_comma_exprs(o, CommaExprsHandlers(
        case_ConsExpr = handle_ConsExpr,  
        case_SingleExpr = handle_SingleExpr 
    ))



def rename_target_exprs(
    o : target_exprs, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> target_exprs:

    def handle_ConsTargetExpr(o : ConsTargetExpr): 

        return ConsTargetExpr(
            rename_expr(
                o.head,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_target_exprs(
                o.tail,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_SingleTargetExpr(o : SingleTargetExpr): 

        return SingleTargetExpr(
            rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )


    return match_target_exprs(o, TargetExprsHandlers(
        case_ConsTargetExpr = handle_ConsTargetExpr,  
        case_SingleTargetExpr = handle_SingleTargetExpr 
    ))



def rename_decorators(
    o : decorators, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> decorators:

    def handle_ConsDec(o : ConsDec): 

        return ConsDec(
            rename_expr(
                o.head,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_decorators(
                o.tail,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_NoDec(o : NoDec): 

        return NoDec(
        )


    return match_decorators(o, DecoratorsHandlers(
        case_ConsDec = handle_ConsDec,  
        case_NoDec = handle_NoDec 
    ))



def rename_constraint_filters(
    o : constraint_filters, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> constraint_filters:

    def handle_ConsFilter(o : ConsFilter): 

        return ConsFilter(
            rename_expr(
                o.head,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_constraint_filters(
                o.tail,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_SingleFilter(o : SingleFilter): 

        return SingleFilter(
            rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_NoFilter(o : NoFilter): 

        return NoFilter(
        )


    return match_constraint_filters(o, ConstraintFiltersHandlers(
        case_ConsFilter = handle_ConsFilter,  
        case_SingleFilter = handle_SingleFilter,  
        case_NoFilter = handle_NoFilter 
    ))



def rename_sequence_string(
    o : sequence_string, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> sequence_string:

    def handle_ConsStr(o : ConsStr): 

        return ConsStr(
            o.head,             rename_sequence_string(
                o.tail,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_SingleStr(o : SingleStr): 

        return SingleStr(
            o.content        )


    return match_sequence_string(o, SequenceStringHandlers(
        case_ConsStr = handle_ConsStr,  
        case_SingleStr = handle_SingleStr 
    ))



def rename_arguments(
    o : arguments, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> arguments:

    def handle_ConsArg(o : ConsArg): 

        return ConsArg(
            rename_expr(
                o.head,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_arguments(
                o.tail,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_SingleArg(o : SingleArg): 

        return SingleArg(
            rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_KeywordsArg(o : KeywordsArg): 

        return KeywordsArg(
            rename_keywords(
                o.kws,
                global_map,
                nonlocal_map,
                local_map
            )        )


    return match_arguments(o, ArgumentsHandlers(
        case_ConsArg = handle_ConsArg,  
        case_SingleArg = handle_SingleArg,  
        case_KeywordsArg = handle_KeywordsArg 
    ))



def rename_dictionary_contents(
    o : dictionary_contents, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> dictionary_contents:

    def handle_ConsField(o : ConsField): 

        return ConsField(
            rename_Field(
                o.head,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_dictionary_contents(
                o.tail,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_SingleField(o : SingleField): 

        return SingleField(
            rename_Field(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )


    return match_dictionary_contents(o, DictionaryContentsHandlers(
        case_ConsField = handle_ConsField,  
        case_SingleField = handle_SingleField 
    ))



def rename_sequence_var(
    o : sequence_var, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> sequence_var:

    def handle_ConsId(o : ConsId): 

        return ConsId(
            o.head,             rename_sequence_var(
                o.tail,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_SingleId(o : SingleId): 

        return SingleId(
            o.content        )


    return match_sequence_var(o, SequenceVarHandlers(
        case_ConsId = handle_ConsId,  
        case_SingleId = handle_SingleId 
    ))



def rename_sequence_ImportName(
    o : sequence_ImportName, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> sequence_ImportName:

    def handle_ConsImportName(o : ConsImportName): 

        return ConsImportName(
            rename_ImportName(
                o.head,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_sequence_ImportName(
                o.tail,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_SingleImportName(o : SingleImportName): 

        return SingleImportName(
            rename_ImportName(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )


    return match_sequence_ImportName(o, SequenceImportNameHandlers(
        case_ConsImportName = handle_ConsImportName,  
        case_SingleImportName = handle_SingleImportName 
    ))



def rename_sequence_Withitem(
    o : sequence_Withitem, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> sequence_Withitem:

    def handle_ConsWithitem(o : ConsWithitem): 

        return ConsWithitem(
            rename_Withitem(
                o.head,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_sequence_Withitem(
                o.tail,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_SingleWithitem(o : SingleWithitem): 

        return SingleWithitem(
            rename_Withitem(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )


    return match_sequence_Withitem(o, SequenceWithitemHandlers(
        case_ConsWithitem = handle_ConsWithitem,  
        case_SingleWithitem = handle_SingleWithitem 
    ))



def rename_statements(
    o : statements, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> statements:

    def handle_ConsStmt(o : ConsStmt): 

        return ConsStmt(
            rename_stmt(
                o.head,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_statements(
                o.tail,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_SingleStmt(o : SingleStmt): 

        return SingleStmt(
            rename_stmt(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )


    return match_statements(o, StatementsHandlers(
        case_ConsStmt = handle_ConsStmt,  
        case_SingleStmt = handle_SingleStmt 
    ))



def rename_comprehension_constraints(
    o : comprehension_constraints, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> comprehension_constraints:

    def handle_ConsConstraint(o : ConsConstraint): 

        return ConsConstraint(
            rename_constraint(
                o.head,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_comprehension_constraints(
                o.tail,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_SingleConstraint(o : SingleConstraint): 

        return SingleConstraint(
            rename_constraint(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )


    return match_comprehension_constraints(o, ComprehensionConstraintsHandlers(
        case_ConsConstraint = handle_ConsConstraint,  
        case_SingleConstraint = handle_SingleConstraint 
    ))



def rename_sequence_ExceptHandler(
    o : sequence_ExceptHandler, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> sequence_ExceptHandler:

    def handle_ConsExceptHandler(o : ConsExceptHandler): 

        return ConsExceptHandler(
            rename_ExceptHandler(
                o.head,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_sequence_ExceptHandler(
                o.tail,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_SingleExceptHandler(o : SingleExceptHandler): 

        return SingleExceptHandler(
            rename_ExceptHandler(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )


    return match_sequence_ExceptHandler(o, SequenceExceptHandlerHandlers(
        case_ConsExceptHandler = handle_ConsExceptHandler,  
        case_SingleExceptHandler = handle_SingleExceptHandler 
    ))



def rename_conditions(
    o : conditions, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> conditions:

    def handle_ElifCond(o : ElifCond): 

        return ElifCond(
            rename_ElifBlock(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_conditions(
                o.tail,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_ElseCond(o : ElseCond): 

        return ElseCond(
            rename_ElseBlock(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_NoCond(o : NoCond): 

        return NoCond(
        )


    return match_conditions(o, ConditionsHandlers(
        case_ElifCond = handle_ElifCond,  
        case_ElseCond = handle_ElseCond,  
        case_NoCond = handle_NoCond 
    ))



def rename_function_def(
    o : function_def, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> function_def:

    def handle_FunctionDef(o : FunctionDef): 

        return FunctionDef(
            o.name,             rename_parameters(
                o.params,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_return_type(
                o.ret_typ,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_statements(
                o.body,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_AsyncFunctionDef(o : AsyncFunctionDef): 

        return AsyncFunctionDef(
            o.name,             rename_parameters(
                o.params,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_return_type(
                o.ret_typ,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_statements(
                o.body,
                global_map,
                nonlocal_map,
                local_map
            )        )


    return match_function_def(o, FunctionDefHandlers(
        case_FunctionDef = handle_FunctionDef,  
        case_AsyncFunctionDef = handle_AsyncFunctionDef 
    ))



def rename_stmt(
    o : stmt, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> stmt:

    def handle_DecFunctionDef(o : DecFunctionDef): 

        return DecFunctionDef(
            rename_decorators(
                o.decs,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_function_def(
                o.fun_def,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_DecAsyncFunctionDef(o : DecAsyncFunctionDef): 

        return DecAsyncFunctionDef(
            rename_decorators(
                o.decs,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_function_def(
                o.fun_def,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_DecClassDef(o : DecClassDef): 

        return DecClassDef(
            rename_decorators(
                o.decs,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_ClassDef(
                o.class_def,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_ReturnSomething(o : ReturnSomething): 

        return ReturnSomething(
            rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_Return(o : Return): 

        return Return(
        )

    def handle_Delete(o : Delete): 

        return Delete(
            rename_comma_exprs(
                o.targets,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_Assign(o : Assign): 

        return Assign(
            rename_target_exprs(
                o.targets,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_AugAssign(o : AugAssign): 

        return AugAssign(
            rename_expr(
                o.target,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_operator(
                o.op,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_TypedAssign(o : TypedAssign): 

        return TypedAssign(
            rename_expr(
                o.target,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_expr(
                o.type,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_TypedDeclare(o : TypedDeclare): 

        return TypedDeclare(
            rename_expr(
                o.target,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_expr(
                o.type,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_For(o : For): 

        return For(
            rename_expr(
                o.target,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_expr(
                o.iter,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_statements(
                o.body,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_ForElse(o : ForElse): 

        return ForElse(
            rename_expr(
                o.target,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_expr(
                o.iter,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_statements(
                o.body,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_ElseBlock(
                o.orelse,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_AsyncFor(o : AsyncFor): 

        return AsyncFor(
            rename_expr(
                o.target,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_expr(
                o.iter,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_statements(
                o.body,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_AsyncForElse(o : AsyncForElse): 

        return AsyncForElse(
            rename_expr(
                o.target,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_expr(
                o.iter,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_statements(
                o.body,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_ElseBlock(
                o.orelse,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_While(o : While): 

        return While(
            rename_expr(
                o.test,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_statements(
                o.body,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_WhileElse(o : WhileElse): 

        return WhileElse(
            rename_expr(
                o.test,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_statements(
                o.body,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_ElseBlock(
                o.orelse,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_If(o : If): 

        return If(
            rename_expr(
                o.test,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_statements(
                o.body,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_conditions(
                o.orelse,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_With(o : With): 

        return With(
            rename_sequence_Withitem(
                o.items,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_statements(
                o.body,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_AsyncWith(o : AsyncWith): 

        return AsyncWith(
            rename_sequence_Withitem(
                o.items,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_statements(
                o.body,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_Raise(o : Raise): 

        return Raise(
        )

    def handle_RaiseExc(o : RaiseExc): 

        return RaiseExc(
            rename_expr(
                o.exc,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_RaiseFrom(o : RaiseFrom): 

        return RaiseFrom(
            rename_expr(
                o.exc,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_expr(
                o.caus,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_Try(o : Try): 

        return Try(
            rename_statements(
                o.body,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_sequence_ExceptHandler(
                o.handlers,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_TryElse(o : TryElse): 

        return TryElse(
            rename_statements(
                o.body,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_sequence_ExceptHandler(
                o.handlers,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_ElseBlock(
                o.orelse,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_TryFin(o : TryFin): 

        return TryFin(
            rename_statements(
                o.body,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_sequence_ExceptHandler(
                o.handlers,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_FinallyBlock(
                o.fin,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_TryElseFin(o : TryElseFin): 

        return TryElseFin(
            rename_statements(
                o.body,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_sequence_ExceptHandler(
                o.handlers,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_ElseBlock(
                o.orelse,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_FinallyBlock(
                o.fin,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_Assert(o : Assert): 

        return Assert(
            rename_expr(
                o.test,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_AssertMsg(o : AssertMsg): 

        return AssertMsg(
            rename_expr(
                o.test,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_expr(
                o.msg,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_Import(o : Import): 

        return Import(
            rename_sequence_ImportName(
                o.names,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_ImportFrom(o : ImportFrom): 

        return ImportFrom(
            rename_module_id(
                o.module,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_sequence_ImportName(
                o.names,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_ImportWildCard(o : ImportWildCard): 

        return ImportWildCard(
            rename_module_id(
                o.module,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_Global(o : Global): 

        return Global(
            rename_sequence_var(
                o.names,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_Nonlocal(o : Nonlocal): 

        return Nonlocal(
            rename_sequence_var(
                o.names,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_Expr(o : Expr): 

        return Expr(
            rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_Pass(o : Pass): 

        return Pass(
        )

    def handle_Break(o : Break): 

        return Break(
        )

    def handle_Continue(o : Continue): 

        return Continue(
        )


    return match_stmt(o, StmtHandlers(
        case_DecFunctionDef = handle_DecFunctionDef,  
        case_DecAsyncFunctionDef = handle_DecAsyncFunctionDef,  
        case_DecClassDef = handle_DecClassDef,  
        case_ReturnSomething = handle_ReturnSomething,  
        case_Return = handle_Return,  
        case_Delete = handle_Delete,  
        case_Assign = handle_Assign,  
        case_AugAssign = handle_AugAssign,  
        case_TypedAssign = handle_TypedAssign,  
        case_TypedDeclare = handle_TypedDeclare,  
        case_For = handle_For,  
        case_ForElse = handle_ForElse,  
        case_AsyncFor = handle_AsyncFor,  
        case_AsyncForElse = handle_AsyncForElse,  
        case_While = handle_While,  
        case_WhileElse = handle_WhileElse,  
        case_If = handle_If,  
        case_With = handle_With,  
        case_AsyncWith = handle_AsyncWith,  
        case_Raise = handle_Raise,  
        case_RaiseExc = handle_RaiseExc,  
        case_RaiseFrom = handle_RaiseFrom,  
        case_Try = handle_Try,  
        case_TryElse = handle_TryElse,  
        case_TryFin = handle_TryFin,  
        case_TryElseFin = handle_TryElseFin,  
        case_Assert = handle_Assert,  
        case_AssertMsg = handle_AssertMsg,  
        case_Import = handle_Import,  
        case_ImportFrom = handle_ImportFrom,  
        case_ImportWildCard = handle_ImportWildCard,  
        case_Global = handle_Global,  
        case_Nonlocal = handle_Nonlocal,  
        case_Expr = handle_Expr,  
        case_Pass = handle_Pass,  
        case_Break = handle_Break,  
        case_Continue = handle_Continue 
    ))



def rename_expr(
    o : expr, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> expr:

    def handle_BoolOp(o : BoolOp): 

        return BoolOp(
            rename_expr(
                o.left,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_boolop(
                o.op,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_expr(
                o.right,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_NamedExpr(o : NamedExpr): 

        return NamedExpr(
            rename_expr(
                o.target,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_BinOp(o : BinOp): 

        return BinOp(
            rename_expr(
                o.left,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_operator(
                o.op,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_expr(
                o.right,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_UnaryOp(o : UnaryOp): 

        return UnaryOp(
            rename_unaryop(
                o.op,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_expr(
                o.right,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_Lambda(o : Lambda): 

        return Lambda(
            rename_parameters(
                o.params,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_expr(
                o.body,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_IfExp(o : IfExp): 

        return IfExp(
            rename_expr(
                o.body,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_expr(
                o.test,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_expr(
                o.orelse,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_Dictionary(o : Dictionary): 

        return Dictionary(
            rename_dictionary_contents(
                o.contents,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_EmptyDictionary(o : EmptyDictionary): 

        return EmptyDictionary(
        )

    def handle_Set(o : Set): 

        return Set(
            rename_comma_exprs(
                o.contents,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_ListComp(o : ListComp): 

        return ListComp(
            rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_comprehension_constraints(
                o.constraints,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_SetComp(o : SetComp): 

        return SetComp(
            rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_comprehension_constraints(
                o.constraints,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_DictionaryComp(o : DictionaryComp): 

        return DictionaryComp(
            rename_expr(
                o.key,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_comprehension_constraints(
                o.constraints,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_GeneratorExp(o : GeneratorExp): 

        return GeneratorExp(
            rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_comprehension_constraints(
                o.constraints,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_Await(o : Await): 

        return Await(
            rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_YieldNothing(o : YieldNothing): 

        return YieldNothing(
        )

    def handle_Yield(o : Yield): 

        return Yield(
            rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_YieldFrom(o : YieldFrom): 

        return YieldFrom(
            rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_Compare(o : Compare): 

        return Compare(
            rename_expr(
                o.left,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_comparisons(
                o.comps,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_Call(o : Call): 

        return Call(
            rename_expr(
                o.func,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_CallArgs(o : CallArgs): 

        return CallArgs(
            rename_expr(
                o.func,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_arguments(
                o.args,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_Integer(o : Integer): 

        return Integer(
            o.content        )

    def handle_Float(o : Float): 

        return Float(
            o.content        )

    def handle_ConcatString(o : ConcatString): 

        return ConcatString(
            rename_sequence_string(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_True_(o : True_): 

        return True_(
        )

    def handle_False_(o : False_): 

        return False_(
        )

    def handle_None_(o : None_): 

        return None_(
        )

    def handle_Ellip(o : Ellip): 

        return Ellip(
        )

    def handle_Attribute(o : Attribute): 

        return Attribute(
            rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            ),             o.attr        )

    def handle_Subscript(o : Subscript): 

        return Subscript(
            rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_expr(
                o.slice,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_Starred(o : Starred): 

        return Starred(
            rename_expr(
                o.content,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_Name(o : Name): 

        return Name(
            o.id        )

    def handle_List(o : List): 

        return List(
            rename_comma_exprs(
                o.contents,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_EmptyList(o : EmptyList): 

        return EmptyList(
        )

    def handle_Tuple(o : Tuple): 

        return Tuple(
            rename_comma_exprs(
                o.contents,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_EmptyTuple(o : EmptyTuple): 

        return EmptyTuple(
        )

    def handle_Slice(o : Slice): 

        return Slice(
            rename_option_expr(
                o.lower,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_option_expr(
                o.upper,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_option_expr(
                o.step,
                global_map,
                nonlocal_map,
                local_map
            )        )


    return match_expr(o, ExprHandlers(
        case_BoolOp = handle_BoolOp,  
        case_NamedExpr = handle_NamedExpr,  
        case_BinOp = handle_BinOp,  
        case_UnaryOp = handle_UnaryOp,  
        case_Lambda = handle_Lambda,  
        case_IfExp = handle_IfExp,  
        case_Dictionary = handle_Dictionary,  
        case_EmptyDictionary = handle_EmptyDictionary,  
        case_Set = handle_Set,  
        case_ListComp = handle_ListComp,  
        case_SetComp = handle_SetComp,  
        case_DictionaryComp = handle_DictionaryComp,  
        case_GeneratorExp = handle_GeneratorExp,  
        case_Await = handle_Await,  
        case_YieldNothing = handle_YieldNothing,  
        case_Yield = handle_Yield,  
        case_YieldFrom = handle_YieldFrom,  
        case_Compare = handle_Compare,  
        case_Call = handle_Call,  
        case_CallArgs = handle_CallArgs,  
        case_Integer = handle_Integer,  
        case_Float = handle_Float,  
        case_ConcatString = handle_ConcatString,  
        case_True_ = handle_True_,  
        case_False_ = handle_False_,  
        case_None_ = handle_None_,  
        case_Ellip = handle_Ellip,  
        case_Attribute = handle_Attribute,  
        case_Subscript = handle_Subscript,  
        case_Starred = handle_Starred,  
        case_Name = handle_Name,  
        case_List = handle_List,  
        case_EmptyList = handle_EmptyList,  
        case_Tuple = handle_Tuple,  
        case_EmptyTuple = handle_EmptyTuple,  
        case_Slice = handle_Slice 
    ))



def rename_boolop(
    o : boolop, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> boolop:

    def handle_And(o : And): 

        return And(
        )

    def handle_Or(o : Or): 

        return Or(
        )


    return match_boolop(o, BoolopHandlers(
        case_And = handle_And,  
        case_Or = handle_Or 
    ))



def rename_operator(
    o : operator, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> operator:

    def handle_Add(o : Add): 

        return Add(
        )

    def handle_Sub(o : Sub): 

        return Sub(
        )

    def handle_Mult(o : Mult): 

        return Mult(
        )

    def handle_MatMult(o : MatMult): 

        return MatMult(
        )

    def handle_Div(o : Div): 

        return Div(
        )

    def handle_Mod(o : Mod): 

        return Mod(
        )

    def handle_Pow(o : Pow): 

        return Pow(
        )

    def handle_LShift(o : LShift): 

        return LShift(
        )

    def handle_RShift(o : RShift): 

        return RShift(
        )

    def handle_BitOr(o : BitOr): 

        return BitOr(
        )

    def handle_BitXor(o : BitXor): 

        return BitXor(
        )

    def handle_BitAnd(o : BitAnd): 

        return BitAnd(
        )

    def handle_FloorDiv(o : FloorDiv): 

        return FloorDiv(
        )


    return match_operator(o, OperatorHandlers(
        case_Add = handle_Add,  
        case_Sub = handle_Sub,  
        case_Mult = handle_Mult,  
        case_MatMult = handle_MatMult,  
        case_Div = handle_Div,  
        case_Mod = handle_Mod,  
        case_Pow = handle_Pow,  
        case_LShift = handle_LShift,  
        case_RShift = handle_RShift,  
        case_BitOr = handle_BitOr,  
        case_BitXor = handle_BitXor,  
        case_BitAnd = handle_BitAnd,  
        case_FloorDiv = handle_FloorDiv 
    ))



def rename_unaryop(
    o : unaryop, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> unaryop:

    def handle_Invert(o : Invert): 

        return Invert(
        )

    def handle_Not(o : Not): 

        return Not(
        )

    def handle_UAdd(o : UAdd): 

        return UAdd(
        )

    def handle_USub(o : USub): 

        return USub(
        )


    return match_unaryop(o, UnaryopHandlers(
        case_Invert = handle_Invert,  
        case_Not = handle_Not,  
        case_UAdd = handle_UAdd,  
        case_USub = handle_USub 
    ))



def rename_cmpop(
    o : cmpop, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> cmpop:

    def handle_Eq(o : Eq): 

        return Eq(
        )

    def handle_NotEq(o : NotEq): 

        return NotEq(
        )

    def handle_Lt(o : Lt): 

        return Lt(
        )

    def handle_LtE(o : LtE): 

        return LtE(
        )

    def handle_Gt(o : Gt): 

        return Gt(
        )

    def handle_GtE(o : GtE): 

        return GtE(
        )

    def handle_Is(o : Is): 

        return Is(
        )

    def handle_IsNot(o : IsNot): 

        return IsNot(
        )

    def handle_In(o : In): 

        return In(
        )

    def handle_NotIn(o : NotIn): 

        return NotIn(
        )


    return match_cmpop(o, CmpopHandlers(
        case_Eq = handle_Eq,  
        case_NotEq = handle_NotEq,  
        case_Lt = handle_Lt,  
        case_LtE = handle_LtE,  
        case_Gt = handle_Gt,  
        case_GtE = handle_GtE,  
        case_Is = handle_Is,  
        case_IsNot = handle_IsNot,  
        case_In = handle_In,  
        case_NotIn = handle_NotIn 
    ))



def rename_constraint(
    o : constraint, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> constraint:

    def handle_AsyncConstraint(o : AsyncConstraint): 

        return AsyncConstraint(
            rename_expr(
                o.target,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_expr(
                o.search_space,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_constraint_filters(
                o.filts,
                global_map,
                nonlocal_map,
                local_map
            )        )

    def handle_Constraint(o : Constraint): 

        return Constraint(
            rename_expr(
                o.target,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_expr(
                o.search_space,
                global_map,
                nonlocal_map,
                local_map
            ),             rename_constraint_filters(
                o.filts,
                global_map,
                nonlocal_map,
                local_map
            )        )


    return match_constraint(o, ConstraintHandlers(
        case_AsyncConstraint = handle_AsyncConstraint,  
        case_Constraint = handle_Constraint 
    ))
