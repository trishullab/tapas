
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



def rename_Field(
    o : Field, 
    global_map : dict[str, str],
    nonlocal_map : dict[str, str],
    local_map : dict[str, str]
) -> Field:

    return Field(
        rename_expr(
            o.key,
            global_map,
            nonlocal_map,
            local_map
        ),         rename_expr(
            o.contents,
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

        def handle_SomeReturnType(o : SomeReturnType): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_NoReturnType(o : NoReturnType): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_return_type(o, ReturnTypeHandlers(
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

        def handle_SomeModuleId(o : SomeModuleId): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_NoModuleId(o : NoModuleId): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_module_id(o, ModuleIdHandlers(
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

        def handle_SomeExceptArg(o : SomeExceptArg): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_SomeExceptArgName(o : SomeExceptArgName): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_NoExceptArg(o : NoExceptArg): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_except_arg(o, ExceptArgHandlers(
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

        def handle_SomeParamType(o : SomeParamType): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_NoParamType(o : NoParamType): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_param_type(o, ParamTypeHandlers(
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

        def handle_SomeParamDefault(o : SomeParamDefault): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_NoParamDefault(o : NoParamDefault): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_param_default(o, ParamDefaultHandlers(
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

        def handle_ConsKwParam(o : ConsKwParam): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "tail"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "tail":
                    stack.append((ConsKwParam(
                        o.head,                         result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "tail":
                    stack.append((o.tail, recursion_site + 1))
 


        def handle_SingleKwParam(o : SingleKwParam): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_DictionarySplatParam(o : DictionarySplatParam): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_parameters_d(o, ParametersDHandlers(
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

        def handle_SingleListSplatParam(o : SingleListSplatParam): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_TransListSplatParam(o : TransListSplatParam): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_ParamsD(o : ParamsD): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_parameters_c(o, ParametersCHandlers(
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

        def handle_ConsParam(o : ConsParam): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "tail"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "tail":
                    stack.append((ConsParam(
                        o.head,                         result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "tail":
                    stack.append((o.tail, recursion_site + 1))
 


        def handle_SingleParam(o : SingleParam): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_ParamsC(o : ParamsC): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_parameters_b(o, ParametersBHandlers(
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

        def handle_ParamsA(o : ParamsA): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_ParamsB(o : ParamsB): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_NoParam(o : NoParam): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_parameters(o, ParametersHandlers(
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

        def handle_ConsPosParam(o : ConsPosParam): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "tail"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "tail":
                    stack.append((ConsPosParam(
                        o.head,                         result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "tail":
                    stack.append((o.tail, recursion_site + 1))
 


        def handle_SinglePosParam(o : SinglePosParam): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_TransPosParam(o : TransPosParam): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_parameters_a(o, ParametersAHandlers(
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

        def handle_NamedKeyword(o : NamedKeyword): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_SplatKeyword(o : SplatKeyword): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_keyword(o, KeywordHandlers(
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

        def handle_SomeAlias(o : SomeAlias): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_NoAlias(o : NoAlias): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_alias(o, AliasHandlers(
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

        def handle_SomeAliasExpr(o : SomeAliasExpr): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_NoAliasExpr(o : NoAliasExpr): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_alias_expr(o, AliasExprHandlers(
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

        def handle_SomeBases(o : SomeBases): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_NoBases(o : NoBases): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_bases(o, BasesHandlers(
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

        def handle_ConsBase(o : ConsBase): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "tail"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "tail":
                    stack.append((ConsBase(
                        o.head,                         result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "tail":
                    stack.append((o.tail, recursion_site + 1))
 


        def handle_SingleBase(o : SingleBase): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_KeywordsBase(o : KeywordsBase): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_bases_a(o, BasesAHandlers(
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

        def handle_ConsKeyword(o : ConsKeyword): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "tail"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "tail":
                    stack.append((ConsKeyword(
                        o.head,                         result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "tail":
                    stack.append((o.tail, recursion_site + 1))
 


        def handle_SingleKeyword(o : SingleKeyword): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_keywords(o, KeywordsHandlers(
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

        def handle_ConsCompareRight(o : ConsCompareRight): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "tail"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "tail":
                    stack.append((ConsCompareRight(
                        o.head,                         result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "tail":
                    stack.append((o.tail, recursion_site + 1))
 


        def handle_SingleCompareRight(o : SingleCompareRight): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_comparisons(o, ComparisonsHandlers(
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

        def handle_SomeExpr(o : SomeExpr): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_NoExpr(o : NoExpr): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_option_expr(o, OptionExprHandlers(
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

        def handle_ConsExpr(o : ConsExpr): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "tail"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "tail":
                    stack.append((ConsExpr(
                        o.head,                         result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "tail":
                    stack.append((o.tail, recursion_site + 1))
 


        def handle_SingleExpr(o : SingleExpr): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_comma_exprs(o, CommaExprsHandlers(
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

        def handle_ConsTargetExpr(o : ConsTargetExpr): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "tail"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "tail":
                    stack.append((ConsTargetExpr(
                        o.head,                         result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "tail":
                    stack.append((o.tail, recursion_site + 1))
 


        def handle_SingleTargetExpr(o : SingleTargetExpr): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_target_exprs(o, TargetExprsHandlers(
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

        def handle_ConsDec(o : ConsDec): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "tail"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "tail":
                    stack.append((ConsDec(
                        o.head,                         result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "tail":
                    stack.append((o.tail, recursion_site + 1))
 


        def handle_NoDec(o : NoDec): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_decorators(o, DecoratorsHandlers(
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

        def handle_ConsFilter(o : ConsFilter): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "tail"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "tail":
                    stack.append((ConsFilter(
                        o.head,                         result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "tail":
                    stack.append((o.tail, recursion_site + 1))
 


        def handle_SingleFilter(o : SingleFilter): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_NoFilter(o : NoFilter): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_constraint_filters(o, ConstraintFiltersHandlers(
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

        def handle_ConsStr(o : ConsStr): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "tail"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "tail":
                    stack.append((ConsStr(
                        o.head,                         result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "tail":
                    stack.append((o.tail, recursion_site + 1))
 


        def handle_SingleStr(o : SingleStr): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_sequence_string(o, SequenceStringHandlers(
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

        def handle_ConsArg(o : ConsArg): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "tail"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "tail":
                    stack.append((ConsArg(
                        o.head,                         result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "tail":
                    stack.append((o.tail, recursion_site + 1))
 


        def handle_SingleArg(o : SingleArg): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_KeywordsArg(o : KeywordsArg): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_arguments(o, ArgumentsHandlers(
            case_ConsArg = handle_ConsArg,  
            case_SingleArg = handle_SingleArg,  
            case_KeywordsArg = handle_KeywordsArg 
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

        def handle_ConsField(o : ConsField): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "tail"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "tail":
                    stack.append((ConsField(
                        o.head,                         result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "tail":
                    stack.append((o.tail, recursion_site + 1))
 


        def handle_SingleField(o : SingleField): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_dictionary_contents(o, DictionaryContentsHandlers(
            case_ConsField = handle_ConsField,  
            case_SingleField = handle_SingleField 
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

        def handle_ConsId(o : ConsId): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "tail"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "tail":
                    stack.append((ConsId(
                        o.head,                         result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "tail":
                    stack.append((o.tail, recursion_site + 1))
 


        def handle_SingleId(o : SingleId): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_sequence_var(o, SequenceVarHandlers(
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

        def handle_ConsImportName(o : ConsImportName): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "tail"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "tail":
                    stack.append((ConsImportName(
                        o.head,                         result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "tail":
                    stack.append((o.tail, recursion_site + 1))
 


        def handle_SingleImportName(o : SingleImportName): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_sequence_ImportName(o, SequenceImportNameHandlers(
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

        def handle_ConsWithitem(o : ConsWithitem): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "tail"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "tail":
                    stack.append((ConsWithitem(
                        o.head,                         result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "tail":
                    stack.append((o.tail, recursion_site + 1))
 


        def handle_SingleWithitem(o : SingleWithitem): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_sequence_Withitem(o, SequenceWithitemHandlers(
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

        def handle_ConsStmt(o : ConsStmt): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "tail"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "tail":
                    stack.append((ConsStmt(
                        o.head,                         result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "tail":
                    stack.append((o.tail, recursion_site + 1))
 


        def handle_SingleStmt(o : SingleStmt): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_statements(o, StatementsHandlers(
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

        def handle_ConsConstraint(o : ConsConstraint): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "tail"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "tail":
                    stack.append((ConsConstraint(
                        o.head,                         result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "tail":
                    stack.append((o.tail, recursion_site + 1))
 


        def handle_SingleConstraint(o : SingleConstraint): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_comprehension_constraints(o, ComprehensionConstraintsHandlers(
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

        def handle_ConsExceptHandler(o : ConsExceptHandler): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "tail"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "tail":
                    stack.append((ConsExceptHandler(
                        o.head,                         result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "tail":
                    stack.append((o.tail, recursion_site + 1))
 


        def handle_SingleExceptHandler(o : SingleExceptHandler): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_sequence_ExceptHandler(o, SequenceExceptHandlerHandlers(
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

        def handle_ElifCond(o : ElifCond): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "tail"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "tail":
                    stack.append((ElifCond(
                        o.contents,                         result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "tail":
                    stack.append((o.tail, recursion_site + 1))
 


        def handle_ElseCond(o : ElseCond): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_NoCond(o : NoCond): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_conditions(o, ConditionsHandlers(
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

        def handle_FunctionDef(o : FunctionDef): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_AsyncFunctionDef(o : AsyncFunctionDef): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_function_def(o, FunctionDefHandlers(
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

        def handle_DecFunctionDef(o : DecFunctionDef): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_DecAsyncFunctionDef(o : DecAsyncFunctionDef): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_DecClassDef(o : DecClassDef): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_ReturnSomething(o : ReturnSomething): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Return(o : Return): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Delete(o : Delete): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Assign(o : Assign): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_AugAssign(o : AugAssign): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_TypedAssign(o : TypedAssign): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_TypedDeclare(o : TypedDeclare): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_For(o : For): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_ForElse(o : ForElse): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_AsyncFor(o : AsyncFor): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_AsyncForElse(o : AsyncForElse): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_While(o : While): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_WhileElse(o : WhileElse): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_If(o : If): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_With(o : With): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_AsyncWith(o : AsyncWith): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Raise(o : Raise): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_RaiseExc(o : RaiseExc): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_RaiseFrom(o : RaiseFrom): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Try(o : Try): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_TryElse(o : TryElse): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_TryFin(o : TryFin): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_TryElseFin(o : TryElseFin): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Assert(o : Assert): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_AssertMsg(o : AssertMsg): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Import(o : Import): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_ImportFrom(o : ImportFrom): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_ImportWildCard(o : ImportWildCard): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Global(o : Global): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Nonlocal(o : Nonlocal): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Expr(o : Expr): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Pass(o : Pass): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Break(o : Break): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Continue(o : Continue): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_stmt(o, StmtHandlers(
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

        def handle_BoolOp(o : BoolOp): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "left",

                "right"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "left":
                    stack.append((BoolOp(
                        result,                         o.op,                         o.right                    ), recursion_site + 1))
                elif recursion_sites[recursion_site] == "right":
                    stack.append((BoolOp(
                        o.left,                         o.op,                         result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "left":
                    stack.append((o.left, recursion_site + 1))
                elif recursion_sites[recursion_site + 1] == "right":
                    stack.append((o.right, recursion_site + 1))
 


        def handle_NamedExpr(o : NamedExpr): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "target",

                "contents"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "target":
                    stack.append((NamedExpr(
                        result,                         o.contents                    ), recursion_site + 1))
                elif recursion_sites[recursion_site] == "contents":
                    stack.append((NamedExpr(
                        o.target,                         result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "target":
                    stack.append((o.target, recursion_site + 1))
                elif recursion_sites[recursion_site + 1] == "contents":
                    stack.append((o.contents, recursion_site + 1))
 


        def handle_BinOp(o : BinOp): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "left",

                "right"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "left":
                    stack.append((BinOp(
                        result,                         o.op,                         o.right                    ), recursion_site + 1))
                elif recursion_sites[recursion_site] == "right":
                    stack.append((BinOp(
                        o.left,                         o.op,                         result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "left":
                    stack.append((o.left, recursion_site + 1))
                elif recursion_sites[recursion_site + 1] == "right":
                    stack.append((o.right, recursion_site + 1))
 


        def handle_UnaryOp(o : UnaryOp): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "right"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "right":
                    stack.append((UnaryOp(
                        o.op,                         result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "right":
                    stack.append((o.right, recursion_site + 1))
 


        def handle_Lambda(o : Lambda): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "body"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "body":
                    stack.append((Lambda(
                        o.params,                         result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "body":
                    stack.append((o.body, recursion_site + 1))
 


        def handle_IfExp(o : IfExp): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "body",

                "test",

                "orelse"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "body":
                    stack.append((IfExp(
                        result,                         o.test,                         o.orelse                    ), recursion_site + 1))
                elif recursion_sites[recursion_site] == "test":
                    stack.append((IfExp(
                        o.body,                         result,                         o.orelse                    ), recursion_site + 1))
                elif recursion_sites[recursion_site] == "orelse":
                    stack.append((IfExp(
                        o.body,                         o.test,                         result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "body":
                    stack.append((o.body, recursion_site + 1))
                elif recursion_sites[recursion_site + 1] == "test":
                    stack.append((o.test, recursion_site + 1))
                elif recursion_sites[recursion_site + 1] == "orelse":
                    stack.append((o.orelse, recursion_site + 1))
 


        def handle_Dictionary(o : Dictionary): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_EmptyDictionary(o : EmptyDictionary): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Set(o : Set): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_ListComp(o : ListComp): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "contents"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "contents":
                    stack.append((ListComp(
                        result,                         o.constraints                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "contents":
                    stack.append((o.contents, recursion_site + 1))
 


        def handle_SetComp(o : SetComp): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "contents"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "contents":
                    stack.append((SetComp(
                        result,                         o.constraints                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "contents":
                    stack.append((o.contents, recursion_site + 1))
 


        def handle_DictionaryComp(o : DictionaryComp): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "key",

                "contents"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "key":
                    stack.append((DictionaryComp(
                        result,                         o.contents,                         o.constraints                    ), recursion_site + 1))
                elif recursion_sites[recursion_site] == "contents":
                    stack.append((DictionaryComp(
                        o.key,                         result,                         o.constraints                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "key":
                    stack.append((o.key, recursion_site + 1))
                elif recursion_sites[recursion_site + 1] == "contents":
                    stack.append((o.contents, recursion_site + 1))
 


        def handle_GeneratorExp(o : GeneratorExp): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "contents"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "contents":
                    stack.append((GeneratorExp(
                        result,                         o.constraints                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "contents":
                    stack.append((o.contents, recursion_site + 1))
 


        def handle_Await(o : Await): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "contents"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "contents":
                    stack.append((Await(
                        result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "contents":
                    stack.append((o.contents, recursion_site + 1))
 


        def handle_YieldNothing(o : YieldNothing): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Yield(o : Yield): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "contents"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "contents":
                    stack.append((Yield(
                        result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "contents":
                    stack.append((o.contents, recursion_site + 1))
 


        def handle_YieldFrom(o : YieldFrom): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "contents"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "contents":
                    stack.append((YieldFrom(
                        result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "contents":
                    stack.append((o.contents, recursion_site + 1))
 


        def handle_Compare(o : Compare): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "left"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "left":
                    stack.append((Compare(
                        result,                         o.comps                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "left":
                    stack.append((o.left, recursion_site + 1))
 


        def handle_Call(o : Call): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "func"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "func":
                    stack.append((Call(
                        result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "func":
                    stack.append((o.func, recursion_site + 1))
 


        def handle_CallArgs(o : CallArgs): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "func"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "func":
                    stack.append((CallArgs(
                        result,                         o.args                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "func":
                    stack.append((o.func, recursion_site + 1))
 


        def handle_Integer(o : Integer): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Float(o : Float): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_ConcatString(o : ConcatString): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_True_(o : True_): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_False_(o : False_): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_None_(o : None_): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Ellip(o : Ellip): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Attribute(o : Attribute): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "contents"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "contents":
                    stack.append((Attribute(
                        result,                         o.name                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "contents":
                    stack.append((o.contents, recursion_site + 1))
 


        def handle_Subscript(o : Subscript): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "contents",

                "slice"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "contents":
                    stack.append((Subscript(
                        result,                         o.slice                    ), recursion_site + 1))
                elif recursion_sites[recursion_site] == "slice":
                    stack.append((Subscript(
                        o.contents,                         result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "contents":
                    stack.append((o.contents, recursion_site + 1))
                elif recursion_sites[recursion_site + 1] == "slice":
                    stack.append((o.slice, recursion_site + 1))
 


        def handle_Starred(o : Starred): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
                "contents"
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False
                elif recursion_sites[recursion_site] == "contents":
                    stack.append((Starred(
                        result                    ), recursion_site + 1))



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
                elif recursion_sites[recursion_site + 1] == "contents":
                    stack.append((o.contents, recursion_site + 1))
 


        def handle_Name(o : Name): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_List(o : List): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_EmptyList(o : EmptyList): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Tuple(o : Tuple): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_EmptyTuple(o : EmptyTuple): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Slice(o : Slice): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_expr(o, ExprHandlers(
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

        def handle_And(o : And): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Or(o : Or): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_boolop(o, BoolopHandlers(
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

        def handle_Add(o : Add): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Sub(o : Sub): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Mult(o : Mult): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_MatMult(o : MatMult): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Div(o : Div): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Mod(o : Mod): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Pow(o : Pow): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_LShift(o : LShift): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_RShift(o : RShift): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_BitOr(o : BitOr): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_BitXor(o : BitXor): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_BitAnd(o : BitAnd): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_FloorDiv(o : FloorDiv): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_operator(o, OperatorHandlers(
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

        def handle_Invert(o : Invert): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Not(o : Not): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_UAdd(o : UAdd): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_USub(o : USub): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_unaryop(o, UnaryopHandlers(
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

        def handle_Eq(o : Eq): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_NotEq(o : NotEq): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Lt(o : Lt): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_LtE(o : LtE): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Gt(o : Gt): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_GtE(o : GtE): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Is(o : Is): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_IsNot(o : IsNot): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_In(o : In): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_NotIn(o : NotIn): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_cmpop(o, CmpopHandlers(
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

        def handle_AsyncConstraint(o : AsyncConstraint): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 


        def handle_Constraint(o : Constraint): 
            nonlocal stack
            nonlocal partial_result
            nonlocal recursion_site
            nonlocal result

            recursion_sites = [
            ]

            if recursion_site >= 0:

                # update the stack with the result at the recursion_site
                if False:
                    assert False



                # update the stack with the node at the next recursion_site 
                # if the current recursion site is not the last
                if recursion_site + 1 >= len(recursion_sites):
                    result = partial_result
 

 

        match_constraint(o, ConstraintHandlers(
            case_AsyncConstraint = handle_AsyncConstraint,  
            case_Constraint = handle_Constraint 
         ))
    return result

