
from __future__ import annotations
from lib import production_instance as prod_inst 
from gen.python_ast import *
from gen.line_format import InLine, NewLine, IndentLine



def rename_Module(
    o : Module, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> Module:

    return Module(
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

    return CompareRight(
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

    return ExceptHandler(
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

    return Param(
        o.name,         rename_param_type(
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



def rename_ImportName(
    o : ImportName, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> ImportName:

    return ImportName(
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

    return Withitem(
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

    return ClassDef(
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

    return ElifBlock(
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

    return ElseBlock(
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

    return FinallyBlock(
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

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[return_type, int]] = [(o, -1)]
    result : return_type = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_SomeReturnType(partial_result : SomeReturnType): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_NoReturnType(partial_result : NoReturnType): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_return_type(partial_result, ReturnTypeHandlers(
            case_SomeReturnType = handle_SomeReturnType,  
            case_NoReturnType = handle_NoReturnType 
         ))
    return result




def rename_module_id(
    o : module_id, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> module_id:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[module_id, int]] = [(o, -1)]
    result : module_id = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_SomeModuleId(partial_result : SomeModuleId): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_NoModuleId(partial_result : NoModuleId): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_module_id(partial_result, ModuleIdHandlers(
            case_SomeModuleId = handle_SomeModuleId,  
            case_NoModuleId = handle_NoModuleId 
         ))
    return result




def rename_except_arg(
    o : except_arg, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> except_arg:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[except_arg, int]] = [(o, -1)]
    result : except_arg = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_SomeExceptArg(partial_result : SomeExceptArg): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_SomeExceptArgName(partial_result : SomeExceptArgName): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_NoExceptArg(partial_result : NoExceptArg): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_except_arg(partial_result, ExceptArgHandlers(
            case_SomeExceptArg = handle_SomeExceptArg,  
            case_SomeExceptArgName = handle_SomeExceptArgName,  
            case_NoExceptArg = handle_NoExceptArg 
         ))
    return result




def rename_param_type(
    o : param_type, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> param_type:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[param_type, int]] = [(o, -1)]
    result : param_type = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_SomeParamType(partial_result : SomeParamType): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_NoParamType(partial_result : NoParamType): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_param_type(partial_result, ParamTypeHandlers(
            case_SomeParamType = handle_SomeParamType,  
            case_NoParamType = handle_NoParamType 
         ))
    return result




def rename_param_default(
    o : param_default, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> param_default:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[param_default, int]] = [(o, -1)]
    result : param_default = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_SomeParamDefault(partial_result : SomeParamDefault): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_NoParamDefault(partial_result : NoParamDefault): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_param_default(partial_result, ParamDefaultHandlers(
            case_SomeParamDefault = handle_SomeParamDefault,  
            case_NoParamDefault = handle_NoParamDefault 
         ))
    return result




def rename_parameters_d(
    o : parameters_d, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> parameters_d:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[parameters_d, int]] = [(o, -1)]
    result : parameters_d = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_ConsKwParam(partial_result : ConsKwParam): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = ConsKwParam(
                    partial_result.head,
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.tail, -1))
 

        def handle_SingleKwParam(partial_result : SingleKwParam): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_DictionarySplatParam(partial_result : DictionarySplatParam): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_parameters_d(partial_result, ParametersDHandlers(
            case_ConsKwParam = handle_ConsKwParam,  
            case_SingleKwParam = handle_SingleKwParam,  
            case_DictionarySplatParam = handle_DictionarySplatParam 
         ))
    return result




def rename_parameters_c(
    o : parameters_c, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> parameters_c:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[parameters_c, int]] = [(o, -1)]
    result : parameters_c = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_SingleListSplatParam(partial_result : SingleListSplatParam): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_TransListSplatParam(partial_result : TransListSplatParam): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_ParamsD(partial_result : ParamsD): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_parameters_c(partial_result, ParametersCHandlers(
            case_SingleListSplatParam = handle_SingleListSplatParam,  
            case_TransListSplatParam = handle_TransListSplatParam,  
            case_ParamsD = handle_ParamsD 
         ))
    return result




def rename_parameters_b(
    o : parameters_b, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> parameters_b:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[parameters_b, int]] = [(o, -1)]
    result : parameters_b = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_ConsParam(partial_result : ConsParam): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = ConsParam(
                    partial_result.head,
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.tail, -1))
 

        def handle_SingleParam(partial_result : SingleParam): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_ParamsC(partial_result : ParamsC): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_parameters_b(partial_result, ParametersBHandlers(
            case_ConsParam = handle_ConsParam,  
            case_SingleParam = handle_SingleParam,  
            case_ParamsC = handle_ParamsC 
         ))
    return result




def rename_parameters(
    o : parameters, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> parameters:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[parameters, int]] = [(o, -1)]
    result : parameters = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_ParamsA(partial_result : ParamsA): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_ParamsB(partial_result : ParamsB): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_NoParam(partial_result : NoParam): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_parameters(partial_result, ParametersHandlers(
            case_ParamsA = handle_ParamsA,  
            case_ParamsB = handle_ParamsB,  
            case_NoParam = handle_NoParam 
         ))
    return result




def rename_parameters_a(
    o : parameters_a, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> parameters_a:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[parameters_a, int]] = [(o, -1)]
    result : parameters_a = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_ConsPosParam(partial_result : ConsPosParam): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = ConsPosParam(
                    partial_result.head,
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.tail, -1))
 

        def handle_SinglePosParam(partial_result : SinglePosParam): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_TransPosParam(partial_result : TransPosParam): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_parameters_a(partial_result, ParametersAHandlers(
            case_ConsPosParam = handle_ConsPosParam,  
            case_SinglePosParam = handle_SinglePosParam,  
            case_TransPosParam = handle_TransPosParam 
         ))
    return result




def rename_keyword(
    o : keyword, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> keyword:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[keyword, int]] = [(o, -1)]
    result : keyword = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_NamedKeyword(partial_result : NamedKeyword): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_SplatKeyword(partial_result : SplatKeyword): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_keyword(partial_result, KeywordHandlers(
            case_NamedKeyword = handle_NamedKeyword,  
            case_SplatKeyword = handle_SplatKeyword 
         ))
    return result




def rename_alias(
    o : alias, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> alias:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[alias, int]] = [(o, -1)]
    result : alias = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_SomeAlias(partial_result : SomeAlias): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_NoAlias(partial_result : NoAlias): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_alias(partial_result, AliasHandlers(
            case_SomeAlias = handle_SomeAlias,  
            case_NoAlias = handle_NoAlias 
         ))
    return result




def rename_alias_expr(
    o : alias_expr, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> alias_expr:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[alias_expr, int]] = [(o, -1)]
    result : alias_expr = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_SomeAliasExpr(partial_result : SomeAliasExpr): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_NoAliasExpr(partial_result : NoAliasExpr): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_alias_expr(partial_result, AliasExprHandlers(
            case_SomeAliasExpr = handle_SomeAliasExpr,  
            case_NoAliasExpr = handle_NoAliasExpr 
         ))
    return result




def rename_bases(
    o : bases, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> bases:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[bases, int]] = [(o, -1)]
    result : bases = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_SomeBases(partial_result : SomeBases): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_NoBases(partial_result : NoBases): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_bases(partial_result, BasesHandlers(
            case_SomeBases = handle_SomeBases,  
            case_NoBases = handle_NoBases 
         ))
    return result




def rename_bases_a(
    o : bases_a, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> bases_a:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[bases_a, int]] = [(o, -1)]
    result : bases_a = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_ConsBase(partial_result : ConsBase): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = ConsBase(
                    partial_result.head,
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.tail, -1))
 

        def handle_SingleBase(partial_result : SingleBase): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_KeywordsBase(partial_result : KeywordsBase): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_bases_a(partial_result, BasesAHandlers(
            case_ConsBase = handle_ConsBase,  
            case_SingleBase = handle_SingleBase,  
            case_KeywordsBase = handle_KeywordsBase 
         ))
    return result




def rename_keywords(
    o : keywords, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> keywords:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[keywords, int]] = [(o, -1)]
    result : keywords = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_ConsKeyword(partial_result : ConsKeyword): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = ConsKeyword(
                    partial_result.head,
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.tail, -1))
 

        def handle_SingleKeyword(partial_result : SingleKeyword): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_keywords(partial_result, KeywordsHandlers(
            case_ConsKeyword = handle_ConsKeyword,  
            case_SingleKeyword = handle_SingleKeyword 
         ))
    return result




def rename_comparisons(
    o : comparisons, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> comparisons:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[comparisons, int]] = [(o, -1)]
    result : comparisons = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_ConsCompareRight(partial_result : ConsCompareRight): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = ConsCompareRight(
                    partial_result.head,
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.tail, -1))
 

        def handle_SingleCompareRight(partial_result : SingleCompareRight): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_comparisons(partial_result, ComparisonsHandlers(
            case_ConsCompareRight = handle_ConsCompareRight,  
            case_SingleCompareRight = handle_SingleCompareRight 
         ))
    return result




def rename_option_expr(
    o : option_expr, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> option_expr:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[option_expr, int]] = [(o, -1)]
    result : option_expr = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_SomeExpr(partial_result : SomeExpr): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_NoExpr(partial_result : NoExpr): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_option_expr(partial_result, OptionExprHandlers(
            case_SomeExpr = handle_SomeExpr,  
            case_NoExpr = handle_NoExpr 
         ))
    return result




def rename_comma_exprs(
    o : comma_exprs, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> comma_exprs:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[comma_exprs, int]] = [(o, -1)]
    result : comma_exprs = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_ConsExpr(partial_result : ConsExpr): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = ConsExpr(
                    partial_result.head,
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.tail, -1))
 

        def handle_SingleExpr(partial_result : SingleExpr): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_comma_exprs(partial_result, CommaExprsHandlers(
            case_ConsExpr = handle_ConsExpr,  
            case_SingleExpr = handle_SingleExpr 
         ))
    return result




def rename_target_exprs(
    o : target_exprs, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> target_exprs:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[target_exprs, int]] = [(o, -1)]
    result : target_exprs = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_ConsTargetExpr(partial_result : ConsTargetExpr): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = ConsTargetExpr(
                    partial_result.head,
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.tail, -1))
 

        def handle_SingleTargetExpr(partial_result : SingleTargetExpr): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_target_exprs(partial_result, TargetExprsHandlers(
            case_ConsTargetExpr = handle_ConsTargetExpr,  
            case_SingleTargetExpr = handle_SingleTargetExpr 
         ))
    return result




def rename_decorators(
    o : decorators, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> decorators:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[decorators, int]] = [(o, -1)]
    result : decorators = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_ConsDec(partial_result : ConsDec): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = ConsDec(
                    partial_result.head,
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.tail, -1))
 

        def handle_NoDec(partial_result : NoDec): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_decorators(partial_result, DecoratorsHandlers(
            case_ConsDec = handle_ConsDec,  
            case_NoDec = handle_NoDec 
         ))
    return result




def rename_constraint_filters(
    o : constraint_filters, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> constraint_filters:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[constraint_filters, int]] = [(o, -1)]
    result : constraint_filters = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_ConsFilter(partial_result : ConsFilter): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = ConsFilter(
                    partial_result.head,
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.tail, -1))
 

        def handle_SingleFilter(partial_result : SingleFilter): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_NoFilter(partial_result : NoFilter): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_constraint_filters(partial_result, ConstraintFiltersHandlers(
            case_ConsFilter = handle_ConsFilter,  
            case_SingleFilter = handle_SingleFilter,  
            case_NoFilter = handle_NoFilter 
         ))
    return result




def rename_sequence_string(
    o : sequence_string, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> sequence_string:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[sequence_string, int]] = [(o, -1)]
    result : sequence_string = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_ConsStr(partial_result : ConsStr): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = ConsStr(
                    partial_result.head,
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.tail, -1))
 

        def handle_SingleStr(partial_result : SingleStr): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_sequence_string(partial_result, SequenceStringHandlers(
            case_ConsStr = handle_ConsStr,  
            case_SingleStr = handle_SingleStr 
         ))
    return result




def rename_arguments(
    o : arguments, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> arguments:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[arguments, int]] = [(o, -1)]
    result : arguments = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_ConsArg(partial_result : ConsArg): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = ConsArg(
                    partial_result.head,
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.tail, -1))
 

        def handle_SingleArg(partial_result : SingleArg): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_KeywordsArg(partial_result : KeywordsArg): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_arguments(partial_result, ArgumentsHandlers(
            case_ConsArg = handle_ConsArg,  
            case_SingleArg = handle_SingleArg,  
            case_KeywordsArg = handle_KeywordsArg 
         ))
    return result




def rename_dictionary_item(
    o : dictionary_item, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> dictionary_item:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[dictionary_item, int]] = [(o, -1)]
    result : dictionary_item = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_Field(partial_result : Field): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_DictionarySplatFields(partial_result : DictionarySplatFields): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_dictionary_item(partial_result, DictionaryItemHandlers(
            case_Field = handle_Field,  
            case_DictionarySplatFields = handle_DictionarySplatFields 
         ))
    return result




def rename_dictionary_contents(
    o : dictionary_contents, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> dictionary_contents:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[dictionary_contents, int]] = [(o, -1)]
    result : dictionary_contents = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_ConsDictionaryItem(partial_result : ConsDictionaryItem): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = ConsDictionaryItem(
                    partial_result.head,
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.tail, -1))
 

        def handle_SingleDictionaryItem(partial_result : SingleDictionaryItem): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_dictionary_contents(partial_result, DictionaryContentsHandlers(
            case_ConsDictionaryItem = handle_ConsDictionaryItem,  
            case_SingleDictionaryItem = handle_SingleDictionaryItem 
         ))
    return result




def rename_sequence_var(
    o : sequence_var, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> sequence_var:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[sequence_var, int]] = [(o, -1)]
    result : sequence_var = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_ConsId(partial_result : ConsId): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = ConsId(
                    partial_result.head,
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.tail, -1))
 

        def handle_SingleId(partial_result : SingleId): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_sequence_var(partial_result, SequenceVarHandlers(
            case_ConsId = handle_ConsId,  
            case_SingleId = handle_SingleId 
         ))
    return result




def rename_sequence_ImportName(
    o : sequence_ImportName, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> sequence_ImportName:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[sequence_ImportName, int]] = [(o, -1)]
    result : sequence_ImportName = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_ConsImportName(partial_result : ConsImportName): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = ConsImportName(
                    partial_result.head,
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.tail, -1))
 

        def handle_SingleImportName(partial_result : SingleImportName): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_sequence_ImportName(partial_result, SequenceImportNameHandlers(
            case_ConsImportName = handle_ConsImportName,  
            case_SingleImportName = handle_SingleImportName 
         ))
    return result




def rename_sequence_Withitem(
    o : sequence_Withitem, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> sequence_Withitem:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[sequence_Withitem, int]] = [(o, -1)]
    result : sequence_Withitem = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_ConsWithitem(partial_result : ConsWithitem): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = ConsWithitem(
                    partial_result.head,
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.tail, -1))
 

        def handle_SingleWithitem(partial_result : SingleWithitem): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_sequence_Withitem(partial_result, SequenceWithitemHandlers(
            case_ConsWithitem = handle_ConsWithitem,  
            case_SingleWithitem = handle_SingleWithitem 
         ))
    return result




def rename_statements(
    o : statements, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> statements:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[statements, int]] = [(o, -1)]
    result : statements = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_ConsStmt(partial_result : ConsStmt): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = ConsStmt(
                    partial_result.head,
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.tail, -1))
 

        def handle_SingleStmt(partial_result : SingleStmt): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_statements(partial_result, StatementsHandlers(
            case_ConsStmt = handle_ConsStmt,  
            case_SingleStmt = handle_SingleStmt 
         ))
    return result




def rename_comprehension_constraints(
    o : comprehension_constraints, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> comprehension_constraints:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[comprehension_constraints, int]] = [(o, -1)]
    result : comprehension_constraints = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_ConsConstraint(partial_result : ConsConstraint): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = ConsConstraint(
                    partial_result.head,
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.tail, -1))
 

        def handle_SingleConstraint(partial_result : SingleConstraint): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_comprehension_constraints(partial_result, ComprehensionConstraintsHandlers(
            case_ConsConstraint = handle_ConsConstraint,  
            case_SingleConstraint = handle_SingleConstraint 
         ))
    return result




def rename_sequence_ExceptHandler(
    o : sequence_ExceptHandler, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> sequence_ExceptHandler:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[sequence_ExceptHandler, int]] = [(o, -1)]
    result : sequence_ExceptHandler = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_ConsExceptHandler(partial_result : ConsExceptHandler): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = ConsExceptHandler(
                    partial_result.head,
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.tail, -1))
 

        def handle_SingleExceptHandler(partial_result : SingleExceptHandler): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_sequence_ExceptHandler(partial_result, SequenceExceptHandlerHandlers(
            case_ConsExceptHandler = handle_ConsExceptHandler,  
            case_SingleExceptHandler = handle_SingleExceptHandler 
         ))
    return result




def rename_conditions(
    o : conditions, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> conditions:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[conditions, int]] = [(o, -1)]
    result : conditions = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_ElifCond(partial_result : ElifCond): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = ElifCond(
                    partial_result.contents,
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.tail, -1))
 

        def handle_ElseCond(partial_result : ElseCond): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_NoCond(partial_result : NoCond): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_conditions(partial_result, ConditionsHandlers(
            case_ElifCond = handle_ElifCond,  
            case_ElseCond = handle_ElseCond,  
            case_NoCond = handle_NoCond 
         ))
    return result




def rename_function_def(
    o : function_def, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> function_def:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[function_def, int]] = [(o, -1)]
    result : function_def = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_FunctionDef(partial_result : FunctionDef): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_AsyncFunctionDef(partial_result : AsyncFunctionDef): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_function_def(partial_result, FunctionDefHandlers(
            case_FunctionDef = handle_FunctionDef,  
            case_AsyncFunctionDef = handle_AsyncFunctionDef 
         ))
    return result




def rename_stmt(
    o : stmt, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> stmt:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[stmt, int]] = [(o, -1)]
    result : stmt = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_DecFunctionDef(partial_result : DecFunctionDef): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_DecAsyncFunctionDef(partial_result : DecAsyncFunctionDef): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_DecClassDef(partial_result : DecClassDef): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_ReturnSomething(partial_result : ReturnSomething): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Return(partial_result : Return): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Delete(partial_result : Delete): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Assign(partial_result : Assign): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_AugAssign(partial_result : AugAssign): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_TypedAssign(partial_result : TypedAssign): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_TypedDeclare(partial_result : TypedDeclare): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_For(partial_result : For): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_ForElse(partial_result : ForElse): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_AsyncFor(partial_result : AsyncFor): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_AsyncForElse(partial_result : AsyncForElse): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_While(partial_result : While): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_WhileElse(partial_result : WhileElse): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_If(partial_result : If): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_With(partial_result : With): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_AsyncWith(partial_result : AsyncWith): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Raise(partial_result : Raise): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_RaiseExc(partial_result : RaiseExc): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_RaiseFrom(partial_result : RaiseFrom): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Try(partial_result : Try): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_TryElse(partial_result : TryElse): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_TryFin(partial_result : TryFin): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_TryElseFin(partial_result : TryElseFin): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Assert(partial_result : Assert): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_AssertMsg(partial_result : AssertMsg): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Import(partial_result : Import): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_ImportFrom(partial_result : ImportFrom): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_ImportWildCard(partial_result : ImportWildCard): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Global(partial_result : Global): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Nonlocal(partial_result : Nonlocal): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Expr(partial_result : Expr): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Pass(partial_result : Pass): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Break(partial_result : Break): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Continue(partial_result : Continue): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_stmt(partial_result, StmtHandlers(
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
    return result




def rename_expr(
    o : expr, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> expr:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[expr, int]] = [(o, -1)]
    result : expr = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_BoolOp(partial_result : BoolOp): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = BoolOp(
                    result,
                    partial_result.op,
                    partial_result.right
                )
            elif recursion_site == 1:
                next_partial_result = BoolOp(
                    partial_result.left,
                    partial_result.op,
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 2:
                result = next_partial_result
            elif recursion_site + 1 == 1:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.right, -1))
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.left, -1))
 

        def handle_NamedExpr(partial_result : NamedExpr): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = NamedExpr(
                    result,
                    partial_result.contents
                )
            elif recursion_site == 1:
                next_partial_result = NamedExpr(
                    partial_result.target,
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 2:
                result = next_partial_result
            elif recursion_site + 1 == 1:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.contents, -1))
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.target, -1))
 

        def handle_BinOp(partial_result : BinOp): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = BinOp(
                    result,
                    partial_result.op,
                    partial_result.right
                )
            elif recursion_site == 1:
                next_partial_result = BinOp(
                    partial_result.left,
                    partial_result.op,
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 2:
                result = next_partial_result
            elif recursion_site + 1 == 1:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.right, -1))
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.left, -1))
 

        def handle_UnaryOp(partial_result : UnaryOp): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = UnaryOp(
                    partial_result.op,
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.right, -1))
 

        def handle_Lambda(partial_result : Lambda): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = Lambda(
                    partial_result.params,
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.body, -1))
 

        def handle_IfExp(partial_result : IfExp): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = IfExp(
                    result,
                    partial_result.test,
                    partial_result.orelse
                )
            elif recursion_site == 1:
                next_partial_result = IfExp(
                    partial_result.body,
                    result,
                    partial_result.orelse
                )
            elif recursion_site == 2:
                next_partial_result = IfExp(
                    partial_result.body,
                    partial_result.test,
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 3:
                result = next_partial_result
            elif recursion_site + 1 == 2:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.orelse, -1))
            elif recursion_site + 1 == 1:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.test, -1))
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.body, -1))
 

        def handle_Dictionary(partial_result : Dictionary): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_EmptyDictionary(partial_result : EmptyDictionary): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Set(partial_result : Set): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_ListComp(partial_result : ListComp): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = ListComp(
                    result,
                    partial_result.constraints
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.contents, -1))
 

        def handle_SetComp(partial_result : SetComp): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = SetComp(
                    result,
                    partial_result.constraints
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.contents, -1))
 

        def handle_DictionaryComp(partial_result : DictionaryComp): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = DictionaryComp(
                    result,
                    partial_result.contents,
                    partial_result.constraints
                )
            elif recursion_site == 1:
                next_partial_result = DictionaryComp(
                    partial_result.key,
                    result,
                    partial_result.constraints
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 2:
                result = next_partial_result
            elif recursion_site + 1 == 1:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.contents, -1))
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.key, -1))
 

        def handle_GeneratorExp(partial_result : GeneratorExp): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = GeneratorExp(
                    result,
                    partial_result.constraints
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.contents, -1))
 

        def handle_Await(partial_result : Await): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = Await(
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.contents, -1))
 

        def handle_YieldNothing(partial_result : YieldNothing): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Yield(partial_result : Yield): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = Yield(
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.contents, -1))
 

        def handle_YieldFrom(partial_result : YieldFrom): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = YieldFrom(
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.contents, -1))
 

        def handle_Compare(partial_result : Compare): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = Compare(
                    result,
                    partial_result.comps
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.left, -1))
 

        def handle_Call(partial_result : Call): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = Call(
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.func, -1))
 

        def handle_CallArgs(partial_result : CallArgs): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = CallArgs(
                    result,
                    partial_result.args
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.func, -1))
 

        def handle_Integer(partial_result : Integer): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Float(partial_result : Float): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_ConcatString(partial_result : ConcatString): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_True_(partial_result : True_): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_False_(partial_result : False_): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_None_(partial_result : None_): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Ellip(partial_result : Ellip): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Attribute(partial_result : Attribute): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = Attribute(
                    result,
                    partial_result.name
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.contents, -1))
 

        def handle_Subscript(partial_result : Subscript): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = Subscript(
                    result,
                    partial_result.slice
                )
            elif recursion_site == 1:
                next_partial_result = Subscript(
                    partial_result.contents,
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 2:
                result = next_partial_result
            elif recursion_site + 1 == 1:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.slice, -1))
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.contents, -1))
 

        def handle_Starred(partial_result : Starred): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result
            elif recursion_site == 0:
                next_partial_result = Starred(
                    result
                )

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 1:
                result = next_partial_result
            elif recursion_site + 1 == 0:
                stack.append((next_partial_result, recursion_site + 1))
                stack.append((next_partial_result.contents, -1))
 

        def handle_Name(partial_result : Name): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_List(partial_result : List): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_EmptyList(partial_result : EmptyList): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Tuple(partial_result : Tuple): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_EmptyTuple(partial_result : EmptyTuple): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Slice(partial_result : Slice): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_expr(partial_result, ExprHandlers(
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
    return result




def rename_boolop(
    o : boolop, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> boolop:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[boolop, int]] = [(o, -1)]
    result : boolop = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_And(partial_result : And): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Or(partial_result : Or): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_boolop(partial_result, BoolopHandlers(
            case_And = handle_And,  
            case_Or = handle_Or 
         ))
    return result




def rename_operator(
    o : operator, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> operator:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[operator, int]] = [(o, -1)]
    result : operator = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_Add(partial_result : Add): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Sub(partial_result : Sub): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Mult(partial_result : Mult): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_MatMult(partial_result : MatMult): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Div(partial_result : Div): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Mod(partial_result : Mod): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Pow(partial_result : Pow): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_LShift(partial_result : LShift): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_RShift(partial_result : RShift): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_BitOr(partial_result : BitOr): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_BitXor(partial_result : BitXor): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_BitAnd(partial_result : BitAnd): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_FloorDiv(partial_result : FloorDiv): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_operator(partial_result, OperatorHandlers(
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
    return result




def rename_unaryop(
    o : unaryop, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> unaryop:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[unaryop, int]] = [(o, -1)]
    result : unaryop = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_Invert(partial_result : Invert): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Not(partial_result : Not): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_UAdd(partial_result : UAdd): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_USub(partial_result : USub): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_unaryop(partial_result, UnaryopHandlers(
            case_Invert = handle_Invert,  
            case_Not = handle_Not,  
            case_UAdd = handle_UAdd,  
            case_USub = handle_USub 
         ))
    return result




def rename_cmpop(
    o : cmpop, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> cmpop:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[cmpop, int]] = [(o, -1)]
    result : cmpop = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_Eq(partial_result : Eq): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_NotEq(partial_result : NotEq): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Lt(partial_result : Lt): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_LtE(partial_result : LtE): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Gt(partial_result : Gt): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_GtE(partial_result : GtE): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Is(partial_result : Is): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_IsNot(partial_result : IsNot): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_In(partial_result : In): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_NotIn(partial_result : NotIn): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_cmpop(partial_result, CmpopHandlers(
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
    return result




def rename_constraint(
    o : constraint, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> constraint:

    # int (starting at 0 zero) represents which recursion site is in progress
    stack : list[tuple[constraint, int]] = [(o, -1)]
    result : constraint = o

    while stack:
        (partial_result, recursion_site) = stack.pop() 

        def handle_AsyncConstraint(partial_result : AsyncConstraint): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

        def handle_Constraint(partial_result : Constraint): 
            nonlocal stack
            nonlocal result
            nonlocal recursion_site


            # update the partial result with the result at the recursion_site
            next_partial_result = partial_result 
            if recursion_site == -1:
                next_partial_result = partial_result

            # update the stack with the node at the next recursion_site 
            # if the current recursion site is not the last
            if recursion_site + 1 >= 0:
                result = next_partial_result
 

 

        match_constraint(partial_result, ConstraintHandlers(
            case_AsyncConstraint = handle_AsyncConstraint,  
            case_Constraint = handle_Constraint 
         ))
    return result

