
from __future__ import annotations
import lib.instance
from gen.instance import instance
from gen.python_ast import *
from gen.line_format import InLine, NewLine, IndentLine





def serialize_Module(
    o : Module
) -> list[instance]:

    return (
        [lib.instance.make_Grammar(
            options = 'Module',
            selection = 'Module'
        )] +

        serialize_statements(o.body)

    )
    




def serialize_CompareRight(
    o : CompareRight
) -> list[instance]:

    return (
        [lib.instance.make_Grammar(
            options = 'CompareRight',
            selection = 'CompareRight'
        )] +

        serialize_cmpop(o.op) +
        serialize_expr(o.rand)

    )
    




def serialize_ExceptHandler(
    o : ExceptHandler
) -> list[instance]:

    return (
        [lib.instance.make_Grammar(
            options = 'ExceptHandler',
            selection = 'ExceptHandler'
        )] +

        serialize_except_arg(o.arg) +
        serialize_statements(o.body)

    )
    




def serialize_Param(
    o : Param
) -> list[instance]:

    return (
        [lib.instance.make_Grammar(
            options = 'Param',
            selection = 'Param'
        )] +

        [lib.instance.make_Vocab(options = 'identifier', selection = o.name)] +
        serialize_param_type(o.type) +
        serialize_param_default(o.default)

    )
    




def serialize_ImportName(
    o : ImportName
) -> list[instance]:

    return (
        [lib.instance.make_Grammar(
            options = 'ImportName',
            selection = 'ImportName'
        )] +

        [lib.instance.make_Vocab(options = 'module_identifier', selection = o.name)] +
        serialize_alias(o.as_name)

    )
    




def serialize_Withitem(
    o : Withitem
) -> list[instance]:

    return (
        [lib.instance.make_Grammar(
            options = 'Withitem',
            selection = 'Withitem'
        )] +

        serialize_expr(o.contet) +
        serialize_alias_expr(o.target)

    )
    




def serialize_ClassDef(
    o : ClassDef
) -> list[instance]:

    return (
        [lib.instance.make_Grammar(
            options = 'ClassDef',
            selection = 'ClassDef'
        )] +

        [lib.instance.make_Vocab(options = 'identifier', selection = o.name)] +
        serialize_bases(o.bs) +
        serialize_statements(o.body)

    )
    




def serialize_ElifBlock(
    o : ElifBlock
) -> list[instance]:

    return (
        [lib.instance.make_Grammar(
            options = 'ElifBlock',
            selection = 'ElifBlock'
        )] +

        serialize_expr(o.test) +
        serialize_statements(o.body)

    )
    




def serialize_ElseBlock(
    o : ElseBlock
) -> list[instance]:

    return (
        [lib.instance.make_Grammar(
            options = 'ElseBlock',
            selection = 'ElseBlock'
        )] +

        serialize_statements(o.body)

    )
    




def serialize_FinallyBlock(
    o : FinallyBlock
) -> list[instance]:

    return (
        [lib.instance.make_Grammar(
            options = 'FinallyBlock',
            selection = 'FinallyBlock'
        )] +

        serialize_statements(o.body)

    )
    




def serialize_return_type(
    o : return_type
) -> list[instance]:

    result = []

    stack : list[Union[return_type, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, return_type):

            

            def handle_SomeReturnType(o : SomeReturnType): 
                nonlocal stack
                assert isinstance(o, return_type)

                
                stack.append(
                    serialize_expr(o.contents)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'return_type',
                        selection = 'SomeReturnType'
                    )]
                )
        


            def handle_NoReturnType(o : NoReturnType): 
                nonlocal stack
                assert isinstance(o, return_type)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'return_type',
                        selection = 'NoReturnType'
                    )]
                )
        


            match_return_type(stack_item, ReturnTypeHandlers(
                case_SomeReturnType = handle_SomeReturnType,
                case_NoReturnType = handle_NoReturnType
            ))

        else:
            result += stack_item 

    return result
    




def serialize_module_id(
    o : module_id
) -> list[instance]:

    result = []

    stack : list[Union[module_id, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, module_id):

            

            def handle_SomeModuleId(o : SomeModuleId): 
                nonlocal stack
                assert isinstance(o, module_id)

                
                stack.append(
                    [lib.instance.make_Vocab(
                        options = 'module_identifier',
                        selection = o.contents
                    )]
                )
            
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'module_id',
                        selection = 'SomeModuleId'
                    )]
                )
        


            def handle_NoModuleId(o : NoModuleId): 
                nonlocal stack
                assert isinstance(o, module_id)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'module_id',
                        selection = 'NoModuleId'
                    )]
                )
        


            match_module_id(stack_item, ModuleIdHandlers(
                case_SomeModuleId = handle_SomeModuleId,
                case_NoModuleId = handle_NoModuleId
            ))

        else:
            result += stack_item 

    return result
    




def serialize_except_arg(
    o : except_arg
) -> list[instance]:

    result = []

    stack : list[Union[except_arg, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, except_arg):

            

            def handle_SomeExceptArg(o : SomeExceptArg): 
                nonlocal stack
                assert isinstance(o, except_arg)

                
                stack.append(
                    serialize_expr(o.contents)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'except_arg',
                        selection = 'SomeExceptArg'
                    )]
                )
        


            def handle_SomeExceptArgName(o : SomeExceptArgName): 
                nonlocal stack
                assert isinstance(o, except_arg)

                
                stack.append(
                    [lib.instance.make_Vocab(
                        options = 'identifier',
                        selection = o.name
                    )]
                )
            


                stack.append(
                    serialize_expr(o.contents)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'except_arg',
                        selection = 'SomeExceptArgName'
                    )]
                )
        


            def handle_NoExceptArg(o : NoExceptArg): 
                nonlocal stack
                assert isinstance(o, except_arg)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'except_arg',
                        selection = 'NoExceptArg'
                    )]
                )
        


            match_except_arg(stack_item, ExceptArgHandlers(
                case_SomeExceptArg = handle_SomeExceptArg,
                case_SomeExceptArgName = handle_SomeExceptArgName,
                case_NoExceptArg = handle_NoExceptArg
            ))

        else:
            result += stack_item 

    return result
    




def serialize_param_type(
    o : param_type
) -> list[instance]:

    result = []

    stack : list[Union[param_type, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, param_type):

            

            def handle_SomeParamType(o : SomeParamType): 
                nonlocal stack
                assert isinstance(o, param_type)

                
                stack.append(
                    serialize_expr(o.contents)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'param_type',
                        selection = 'SomeParamType'
                    )]
                )
        


            def handle_NoParamType(o : NoParamType): 
                nonlocal stack
                assert isinstance(o, param_type)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'param_type',
                        selection = 'NoParamType'
                    )]
                )
        


            match_param_type(stack_item, ParamTypeHandlers(
                case_SomeParamType = handle_SomeParamType,
                case_NoParamType = handle_NoParamType
            ))

        else:
            result += stack_item 

    return result
    




def serialize_param_default(
    o : param_default
) -> list[instance]:

    result = []

    stack : list[Union[param_default, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, param_default):

            

            def handle_SomeParamDefault(o : SomeParamDefault): 
                nonlocal stack
                assert isinstance(o, param_default)

                
                stack.append(
                    serialize_expr(o.contents)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'param_default',
                        selection = 'SomeParamDefault'
                    )]
                )
        


            def handle_NoParamDefault(o : NoParamDefault): 
                nonlocal stack
                assert isinstance(o, param_default)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'param_default',
                        selection = 'NoParamDefault'
                    )]
                )
        


            match_param_default(stack_item, ParamDefaultHandlers(
                case_SomeParamDefault = handle_SomeParamDefault,
                case_NoParamDefault = handle_NoParamDefault
            ))

        else:
            result += stack_item 

    return result
    




def serialize_parameters_d(
    o : parameters_d
) -> list[instance]:

    result = []

    stack : list[Union[parameters_d, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, parameters_d):

            

            def handle_ConsKwParam(o : ConsKwParam): 
                nonlocal stack
                assert isinstance(o, parameters_d)

                
                stack.append(
                    o.tail
                )
                


                stack.append(
                    serialize_Param(o.head)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'parameters_d',
                        selection = 'ConsKwParam'
                    )]
                )
        


            def handle_SingleKwParam(o : SingleKwParam): 
                nonlocal stack
                assert isinstance(o, parameters_d)

                
                stack.append(
                    serialize_Param(o.contents)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'parameters_d',
                        selection = 'SingleKwParam'
                    )]
                )
        


            def handle_DictionarySplatParam(o : DictionarySplatParam): 
                nonlocal stack
                assert isinstance(o, parameters_d)

                
                stack.append(
                    serialize_Param(o.contents)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'parameters_d',
                        selection = 'DictionarySplatParam'
                    )]
                )
        


            match_parameters_d(stack_item, ParametersDHandlers(
                case_ConsKwParam = handle_ConsKwParam,
                case_SingleKwParam = handle_SingleKwParam,
                case_DictionarySplatParam = handle_DictionarySplatParam
            ))

        else:
            result += stack_item 

    return result
    




def serialize_parameters_c(
    o : parameters_c
) -> list[instance]:

    result = []

    stack : list[Union[parameters_c, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, parameters_c):

            

            def handle_SingleListSplatParam(o : SingleListSplatParam): 
                nonlocal stack
                assert isinstance(o, parameters_c)

                
                stack.append(
                    serialize_Param(o.contents)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'parameters_c',
                        selection = 'SingleListSplatParam'
                    )]
                )
        


            def handle_TransListSplatParam(o : TransListSplatParam): 
                nonlocal stack
                assert isinstance(o, parameters_c)

                
                stack.append(
                    serialize_parameters_d(o.tail)
                )
                


                stack.append(
                    serialize_Param(o.head)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'parameters_c',
                        selection = 'TransListSplatParam'
                    )]
                )
        


            def handle_ParamsD(o : ParamsD): 
                nonlocal stack
                assert isinstance(o, parameters_c)

                
                stack.append(
                    serialize_parameters_d(o.contents)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'parameters_c',
                        selection = 'ParamsD'
                    )]
                )
        


            match_parameters_c(stack_item, ParametersCHandlers(
                case_SingleListSplatParam = handle_SingleListSplatParam,
                case_TransListSplatParam = handle_TransListSplatParam,
                case_ParamsD = handle_ParamsD
            ))

        else:
            result += stack_item 

    return result
    




def serialize_parameters_b(
    o : parameters_b
) -> list[instance]:

    result = []

    stack : list[Union[parameters_b, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, parameters_b):

            

            def handle_ConsParam(o : ConsParam): 
                nonlocal stack
                assert isinstance(o, parameters_b)

                
                stack.append(
                    o.tail
                )
                


                stack.append(
                    serialize_Param(o.head)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'parameters_b',
                        selection = 'ConsParam'
                    )]
                )
        


            def handle_SingleParam(o : SingleParam): 
                nonlocal stack
                assert isinstance(o, parameters_b)

                
                stack.append(
                    serialize_Param(o.contents)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'parameters_b',
                        selection = 'SingleParam'
                    )]
                )
        


            def handle_ParamsC(o : ParamsC): 
                nonlocal stack
                assert isinstance(o, parameters_b)

                
                stack.append(
                    serialize_parameters_c(o.contents)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'parameters_b',
                        selection = 'ParamsC'
                    )]
                )
        


            match_parameters_b(stack_item, ParametersBHandlers(
                case_ConsParam = handle_ConsParam,
                case_SingleParam = handle_SingleParam,
                case_ParamsC = handle_ParamsC
            ))

        else:
            result += stack_item 

    return result
    




def serialize_parameters(
    o : parameters
) -> list[instance]:

    result = []

    stack : list[Union[parameters, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, parameters):

            

            def handle_ParamsA(o : ParamsA): 
                nonlocal stack
                assert isinstance(o, parameters)

                
                stack.append(
                    serialize_parameters_a(o.contents)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'parameters',
                        selection = 'ParamsA'
                    )]
                )
        


            def handle_ParamsB(o : ParamsB): 
                nonlocal stack
                assert isinstance(o, parameters)

                
                stack.append(
                    serialize_parameters_b(o.contents)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'parameters',
                        selection = 'ParamsB'
                    )]
                )
        


            def handle_NoParam(o : NoParam): 
                nonlocal stack
                assert isinstance(o, parameters)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'parameters',
                        selection = 'NoParam'
                    )]
                )
        


            match_parameters(stack_item, ParametersHandlers(
                case_ParamsA = handle_ParamsA,
                case_ParamsB = handle_ParamsB,
                case_NoParam = handle_NoParam
            ))

        else:
            result += stack_item 

    return result
    




def serialize_parameters_a(
    o : parameters_a
) -> list[instance]:

    result = []

    stack : list[Union[parameters_a, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, parameters_a):

            

            def handle_ConsPosParam(o : ConsPosParam): 
                nonlocal stack
                assert isinstance(o, parameters_a)

                
                stack.append(
                    o.tail
                )
                


                stack.append(
                    serialize_Param(o.head)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'parameters_a',
                        selection = 'ConsPosParam'
                    )]
                )
        


            def handle_SinglePosParam(o : SinglePosParam): 
                nonlocal stack
                assert isinstance(o, parameters_a)

                

                stack.append(
                    serialize_Param(o.contents)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'parameters_a',
                        selection = 'SinglePosParam'
                    )]
                )
        


            def handle_TransPosParam(o : TransPosParam): 
                nonlocal stack
                assert isinstance(o, parameters_a)

                
                stack.append(
                    serialize_parameters_b(o.tail)
                )
                


                stack.append(
                    serialize_Param(o.head)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'parameters_a',
                        selection = 'TransPosParam'
                    )]
                )
        


            match_parameters_a(stack_item, ParametersAHandlers(
                case_ConsPosParam = handle_ConsPosParam,
                case_SinglePosParam = handle_SinglePosParam,
                case_TransPosParam = handle_TransPosParam
            ))

        else:
            result += stack_item 

    return result
    




def serialize_keyword(
    o : keyword
) -> list[instance]:

    result = []

    stack : list[Union[keyword, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, keyword):

            

            def handle_NamedKeyword(o : NamedKeyword): 
                nonlocal stack
                assert isinstance(o, keyword)

                
                stack.append(
                    serialize_expr(o.contents)
                )
                


                stack.append(
                    [lib.instance.make_Vocab(
                        options = 'identifier',
                        selection = o.name
                    )]
                )
            
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'keyword',
                        selection = 'NamedKeyword'
                    )]
                )
        


            def handle_SplatKeyword(o : SplatKeyword): 
                nonlocal stack
                assert isinstance(o, keyword)

                
                stack.append(
                    serialize_expr(o.contents)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'keyword',
                        selection = 'SplatKeyword'
                    )]
                )
        


            match_keyword(stack_item, KeywordHandlers(
                case_NamedKeyword = handle_NamedKeyword,
                case_SplatKeyword = handle_SplatKeyword
            ))

        else:
            result += stack_item 

    return result
    




def serialize_alias(
    o : alias
) -> list[instance]:

    result = []

    stack : list[Union[alias, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, alias):

            

            def handle_SomeAlias(o : SomeAlias): 
                nonlocal stack
                assert isinstance(o, alias)

                
                stack.append(
                    [lib.instance.make_Vocab(
                        options = 'identifier',
                        selection = o.contents
                    )]
                )
            

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'alias',
                        selection = 'SomeAlias'
                    )]
                )
        


            def handle_NoAlias(o : NoAlias): 
                nonlocal stack
                assert isinstance(o, alias)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'alias',
                        selection = 'NoAlias'
                    )]
                )
        


            match_alias(stack_item, AliasHandlers(
                case_SomeAlias = handle_SomeAlias,
                case_NoAlias = handle_NoAlias
            ))

        else:
            result += stack_item 

    return result
    




def serialize_alias_expr(
    o : alias_expr
) -> list[instance]:

    result = []

    stack : list[Union[alias_expr, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, alias_expr):

            

            def handle_SomeAliasExpr(o : SomeAliasExpr): 
                nonlocal stack
                assert isinstance(o, alias_expr)

                
                stack.append(
                    serialize_expr(o.contents)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'alias_expr',
                        selection = 'SomeAliasExpr'
                    )]
                )
        


            def handle_NoAliasExpr(o : NoAliasExpr): 
                nonlocal stack
                assert isinstance(o, alias_expr)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'alias_expr',
                        selection = 'NoAliasExpr'
                    )]
                )
        


            match_alias_expr(stack_item, AliasExprHandlers(
                case_SomeAliasExpr = handle_SomeAliasExpr,
                case_NoAliasExpr = handle_NoAliasExpr
            ))

        else:
            result += stack_item 

    return result
    




def serialize_bases(
    o : bases
) -> list[instance]:

    result = []

    stack : list[Union[bases, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, bases):

            

            def handle_SomeBases(o : SomeBases): 
                nonlocal stack
                assert isinstance(o, bases)

                

                stack.append(
                    serialize_bases_a(o.bases)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'bases',
                        selection = 'SomeBases'
                    )]
                )
        


            def handle_NoBases(o : NoBases): 
                nonlocal stack
                assert isinstance(o, bases)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'bases',
                        selection = 'NoBases'
                    )]
                )
        


            match_bases(stack_item, BasesHandlers(
                case_SomeBases = handle_SomeBases,
                case_NoBases = handle_NoBases
            ))

        else:
            result += stack_item 

    return result
    




def serialize_bases_a(
    o : bases_a
) -> list[instance]:

    result = []

    stack : list[Union[bases_a, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, bases_a):

            

            def handle_ConsBase(o : ConsBase): 
                nonlocal stack
                assert isinstance(o, bases_a)

                
                stack.append(
                    o.tail
                )
                


                stack.append(
                    serialize_expr(o.head)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'bases_a',
                        selection = 'ConsBase'
                    )]
                )
        


            def handle_SingleBase(o : SingleBase): 
                nonlocal stack
                assert isinstance(o, bases_a)

                
                stack.append(
                    serialize_expr(o.contents)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'bases_a',
                        selection = 'SingleBase'
                    )]
                )
        


            def handle_KeywordsBase(o : KeywordsBase): 
                nonlocal stack
                assert isinstance(o, bases_a)

                
                stack.append(
                    serialize_keywords(o.kws)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'bases_a',
                        selection = 'KeywordsBase'
                    )]
                )
        


            match_bases_a(stack_item, BasesAHandlers(
                case_ConsBase = handle_ConsBase,
                case_SingleBase = handle_SingleBase,
                case_KeywordsBase = handle_KeywordsBase
            ))

        else:
            result += stack_item 

    return result
    




def serialize_keywords(
    o : keywords
) -> list[instance]:

    result = []

    stack : list[Union[keywords, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, keywords):

            

            def handle_ConsKeyword(o : ConsKeyword): 
                nonlocal stack
                assert isinstance(o, keywords)

                
                stack.append(
                    o.tail
                )
                


                stack.append(
                    serialize_keyword(o.head)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'keywords',
                        selection = 'ConsKeyword'
                    )]
                )
        


            def handle_SingleKeyword(o : SingleKeyword): 
                nonlocal stack
                assert isinstance(o, keywords)

                
                stack.append(
                    serialize_keyword(o.contents)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'keywords',
                        selection = 'SingleKeyword'
                    )]
                )
        


            match_keywords(stack_item, KeywordsHandlers(
                case_ConsKeyword = handle_ConsKeyword,
                case_SingleKeyword = handle_SingleKeyword
            ))

        else:
            result += stack_item 

    return result
    




def serialize_comparisons(
    o : comparisons
) -> list[instance]:

    result = []

    stack : list[Union[comparisons, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, comparisons):

            

            def handle_ConsCompareRight(o : ConsCompareRight): 
                nonlocal stack
                assert isinstance(o, comparisons)

                
                stack.append(
                    o.tail
                )
                


                stack.append(
                    serialize_CompareRight(o.head)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'comparisons',
                        selection = 'ConsCompareRight'
                    )]
                )
        


            def handle_SingleCompareRight(o : SingleCompareRight): 
                nonlocal stack
                assert isinstance(o, comparisons)

                
                stack.append(
                    serialize_CompareRight(o.contents)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'comparisons',
                        selection = 'SingleCompareRight'
                    )]
                )
        


            match_comparisons(stack_item, ComparisonsHandlers(
                case_ConsCompareRight = handle_ConsCompareRight,
                case_SingleCompareRight = handle_SingleCompareRight
            ))

        else:
            result += stack_item 

    return result
    




def serialize_option_expr(
    o : option_expr
) -> list[instance]:

    result = []

    stack : list[Union[option_expr, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, option_expr):

            

            def handle_SomeExpr(o : SomeExpr): 
                nonlocal stack
                assert isinstance(o, option_expr)

                
                stack.append(
                    serialize_expr(o.contents)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'option_expr',
                        selection = 'SomeExpr'
                    )]
                )
        


            def handle_NoExpr(o : NoExpr): 
                nonlocal stack
                assert isinstance(o, option_expr)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'option_expr',
                        selection = 'NoExpr'
                    )]
                )
        


            match_option_expr(stack_item, OptionExprHandlers(
                case_SomeExpr = handle_SomeExpr,
                case_NoExpr = handle_NoExpr
            ))

        else:
            result += stack_item 

    return result
    




def serialize_comma_exprs(
    o : comma_exprs
) -> list[instance]:

    result = []

    stack : list[Union[comma_exprs, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, comma_exprs):

            

            def handle_ConsExpr(o : ConsExpr): 
                nonlocal stack
                assert isinstance(o, comma_exprs)

                
                stack.append(
                    o.tail
                )
                


                stack.append(
                    serialize_expr(o.head)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'comma_exprs',
                        selection = 'ConsExpr'
                    )]
                )
        


            def handle_SingleExpr(o : SingleExpr): 
                nonlocal stack
                assert isinstance(o, comma_exprs)

                
                stack.append(
                    serialize_expr(o.contents)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'comma_exprs',
                        selection = 'SingleExpr'
                    )]
                )
        


            match_comma_exprs(stack_item, CommaExprsHandlers(
                case_ConsExpr = handle_ConsExpr,
                case_SingleExpr = handle_SingleExpr
            ))

        else:
            result += stack_item 

    return result
    




def serialize_target_exprs(
    o : target_exprs
) -> list[instance]:

    result = []

    stack : list[Union[target_exprs, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, target_exprs):

            

            def handle_ConsTargetExpr(o : ConsTargetExpr): 
                nonlocal stack
                assert isinstance(o, target_exprs)

                
                stack.append(
                    o.tail
                )
                


                stack.append(
                    serialize_expr(o.head)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'target_exprs',
                        selection = 'ConsTargetExpr'
                    )]
                )
        


            def handle_SingleTargetExpr(o : SingleTargetExpr): 
                nonlocal stack
                assert isinstance(o, target_exprs)

                
                stack.append(
                    serialize_expr(o.contents)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'target_exprs',
                        selection = 'SingleTargetExpr'
                    )]
                )
        


            match_target_exprs(stack_item, TargetExprsHandlers(
                case_ConsTargetExpr = handle_ConsTargetExpr,
                case_SingleTargetExpr = handle_SingleTargetExpr
            ))

        else:
            result += stack_item 

    return result
    




def serialize_decorators(
    o : decorators
) -> list[instance]:

    result = []

    stack : list[Union[decorators, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, decorators):

            

            def handle_ConsDec(o : ConsDec): 
                nonlocal stack
                assert isinstance(o, decorators)

                
                stack.append(
                    o.tail
                )
                

                stack.append(
                    serialize_expr(o.head)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'decorators',
                        selection = 'ConsDec'
                    )]
                )
        


            def handle_NoDec(o : NoDec): 
                nonlocal stack
                assert isinstance(o, decorators)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'decorators',
                        selection = 'NoDec'
                    )]
                )
        


            match_decorators(stack_item, DecoratorsHandlers(
                case_ConsDec = handle_ConsDec,
                case_NoDec = handle_NoDec
            ))

        else:
            result += stack_item 

    return result
    




def serialize_constraint_filters(
    o : constraint_filters
) -> list[instance]:

    result = []

    stack : list[Union[constraint_filters, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, constraint_filters):

            

            def handle_ConsFilter(o : ConsFilter): 
                nonlocal stack
                assert isinstance(o, constraint_filters)

                
                stack.append(
                    o.tail
                )
                

                stack.append(
                    serialize_expr(o.head)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'constraint_filters',
                        selection = 'ConsFilter'
                    )]
                )
        


            def handle_SingleFilter(o : SingleFilter): 
                nonlocal stack
                assert isinstance(o, constraint_filters)

                
                stack.append(
                    serialize_expr(o.contents)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'constraint_filters',
                        selection = 'SingleFilter'
                    )]
                )
        


            def handle_NoFilter(o : NoFilter): 
                nonlocal stack
                assert isinstance(o, constraint_filters)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'constraint_filters',
                        selection = 'NoFilter'
                    )]
                )
        


            match_constraint_filters(stack_item, ConstraintFiltersHandlers(
                case_ConsFilter = handle_ConsFilter,
                case_SingleFilter = handle_SingleFilter,
                case_NoFilter = handle_NoFilter
            ))

        else:
            result += stack_item 

    return result
    




def serialize_sequence_string(
    o : sequence_string
) -> list[instance]:

    result = []

    stack : list[Union[sequence_string, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, sequence_string):

            

            def handle_ConsStr(o : ConsStr): 
                nonlocal stack
                assert isinstance(o, sequence_string)

                
                stack.append(
                    o.tail
                )
                


                stack.append(
                    [lib.instance.make_Vocab(
                        options = 'string',
                        selection = o.head
                    )]
                )
            
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'sequence_string',
                        selection = 'ConsStr'
                    )]
                )
        


            def handle_SingleStr(o : SingleStr): 
                nonlocal stack
                assert isinstance(o, sequence_string)

                
                stack.append(
                    [lib.instance.make_Vocab(
                        options = 'string',
                        selection = o.contents
                    )]
                )
            
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'sequence_string',
                        selection = 'SingleStr'
                    )]
                )
        


            match_sequence_string(stack_item, SequenceStringHandlers(
                case_ConsStr = handle_ConsStr,
                case_SingleStr = handle_SingleStr
            ))

        else:
            result += stack_item 

    return result
    




def serialize_arguments(
    o : arguments
) -> list[instance]:

    result = []

    stack : list[Union[arguments, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, arguments):

            

            def handle_ConsArg(o : ConsArg): 
                nonlocal stack
                assert isinstance(o, arguments)

                
                stack.append(
                    o.tail
                )
                


                stack.append(
                    serialize_expr(o.head)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'arguments',
                        selection = 'ConsArg'
                    )]
                )
        


            def handle_SingleArg(o : SingleArg): 
                nonlocal stack
                assert isinstance(o, arguments)

                
                stack.append(
                    serialize_expr(o.contents)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'arguments',
                        selection = 'SingleArg'
                    )]
                )
        


            def handle_KeywordsArg(o : KeywordsArg): 
                nonlocal stack
                assert isinstance(o, arguments)

                
                stack.append(
                    serialize_keywords(o.kws)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'arguments',
                        selection = 'KeywordsArg'
                    )]
                )
        


            match_arguments(stack_item, ArgumentsHandlers(
                case_ConsArg = handle_ConsArg,
                case_SingleArg = handle_SingleArg,
                case_KeywordsArg = handle_KeywordsArg
            ))

        else:
            result += stack_item 

    return result
    




def serialize_dictionary_item(
    o : dictionary_item
) -> list[instance]:

    result = []

    stack : list[Union[dictionary_item, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, dictionary_item):

            

            def handle_Field(o : Field): 
                nonlocal stack
                assert isinstance(o, dictionary_item)

                
                stack.append(
                    serialize_expr(o.contents)
                )
                


                stack.append(
                    serialize_expr(o.key)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'dictionary_item',
                        selection = 'Field'
                    )]
                )
        


            def handle_DictionarySplatFields(o : DictionarySplatFields): 
                nonlocal stack
                assert isinstance(o, dictionary_item)

                
                stack.append(
                    serialize_expr(o.contents)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'dictionary_item',
                        selection = 'DictionarySplatFields'
                    )]
                )
        


            match_dictionary_item(stack_item, DictionaryItemHandlers(
                case_Field = handle_Field,
                case_DictionarySplatFields = handle_DictionarySplatFields
            ))

        else:
            result += stack_item 

    return result
    




def serialize_dictionary_contents(
    o : dictionary_contents
) -> list[instance]:

    result = []

    stack : list[Union[dictionary_contents, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, dictionary_contents):

            

            def handle_ConsDictionaryItem(o : ConsDictionaryItem): 
                nonlocal stack
                assert isinstance(o, dictionary_contents)

                
                stack.append(
                    o.tail
                )
                


                stack.append(
                    serialize_dictionary_item(o.head)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'dictionary_contents',
                        selection = 'ConsDictionaryItem'
                    )]
                )
        


            def handle_SingleDictionaryItem(o : SingleDictionaryItem): 
                nonlocal stack
                assert isinstance(o, dictionary_contents)

                
                stack.append(
                    serialize_dictionary_item(o.contents)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'dictionary_contents',
                        selection = 'SingleDictionaryItem'
                    )]
                )
        


            match_dictionary_contents(stack_item, DictionaryContentsHandlers(
                case_ConsDictionaryItem = handle_ConsDictionaryItem,
                case_SingleDictionaryItem = handle_SingleDictionaryItem
            ))

        else:
            result += stack_item 

    return result
    




def serialize_sequence_var(
    o : sequence_var
) -> list[instance]:

    result = []

    stack : list[Union[sequence_var, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, sequence_var):

            

            def handle_ConsId(o : ConsId): 
                nonlocal stack
                assert isinstance(o, sequence_var)

                
                stack.append(
                    o.tail
                )
                


                stack.append(
                    [lib.instance.make_Vocab(
                        options = 'identifier',
                        selection = o.head
                    )]
                )
            
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'sequence_var',
                        selection = 'ConsId'
                    )]
                )
        


            def handle_SingleId(o : SingleId): 
                nonlocal stack
                assert isinstance(o, sequence_var)

                
                stack.append(
                    [lib.instance.make_Vocab(
                        options = 'identifier',
                        selection = o.contents
                    )]
                )
            
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'sequence_var',
                        selection = 'SingleId'
                    )]
                )
        


            match_sequence_var(stack_item, SequenceVarHandlers(
                case_ConsId = handle_ConsId,
                case_SingleId = handle_SingleId
            ))

        else:
            result += stack_item 

    return result
    




def serialize_sequence_ImportName(
    o : sequence_ImportName
) -> list[instance]:

    result = []

    stack : list[Union[sequence_ImportName, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, sequence_ImportName):

            

            def handle_ConsImportName(o : ConsImportName): 
                nonlocal stack
                assert isinstance(o, sequence_ImportName)

                
                stack.append(
                    o.tail
                )
                


                stack.append(
                    serialize_ImportName(o.head)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'sequence_ImportName',
                        selection = 'ConsImportName'
                    )]
                )
        


            def handle_SingleImportName(o : SingleImportName): 
                nonlocal stack
                assert isinstance(o, sequence_ImportName)

                
                stack.append(
                    serialize_ImportName(o.contents)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'sequence_ImportName',
                        selection = 'SingleImportName'
                    )]
                )
        


            match_sequence_ImportName(stack_item, SequenceImportNameHandlers(
                case_ConsImportName = handle_ConsImportName,
                case_SingleImportName = handle_SingleImportName
            ))

        else:
            result += stack_item 

    return result
    




def serialize_sequence_Withitem(
    o : sequence_Withitem
) -> list[instance]:

    result = []

    stack : list[Union[sequence_Withitem, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, sequence_Withitem):

            

            def handle_ConsWithitem(o : ConsWithitem): 
                nonlocal stack
                assert isinstance(o, sequence_Withitem)

                
                stack.append(
                    o.tail
                )
                


                stack.append(
                    serialize_Withitem(o.head)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'sequence_Withitem',
                        selection = 'ConsWithitem'
                    )]
                )
        


            def handle_SingleWithitem(o : SingleWithitem): 
                nonlocal stack
                assert isinstance(o, sequence_Withitem)

                
                stack.append(
                    serialize_Withitem(o.contents)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'sequence_Withitem',
                        selection = 'SingleWithitem'
                    )]
                )
        


            match_sequence_Withitem(stack_item, SequenceWithitemHandlers(
                case_ConsWithitem = handle_ConsWithitem,
                case_SingleWithitem = handle_SingleWithitem
            ))

        else:
            result += stack_item 

    return result
    




def serialize_statements(
    o : statements
) -> list[instance]:

    result = []

    stack : list[Union[statements, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, statements):

            

            def handle_ConsStmt(o : ConsStmt): 
                nonlocal stack
                assert isinstance(o, statements)

                
                stack.append(
                    o.tail
                )
                

                stack.append(
                    serialize_stmt(o.head)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'statements',
                        selection = 'ConsStmt'
                    )]
                )
        


            def handle_SingleStmt(o : SingleStmt): 
                nonlocal stack
                assert isinstance(o, statements)

                
                stack.append(
                    serialize_stmt(o.contents)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'statements',
                        selection = 'SingleStmt'
                    )]
                )
        


            match_statements(stack_item, StatementsHandlers(
                case_ConsStmt = handle_ConsStmt,
                case_SingleStmt = handle_SingleStmt
            ))

        else:
            result += stack_item 

    return result
    




def serialize_comprehension_constraints(
    o : comprehension_constraints
) -> list[instance]:

    result = []

    stack : list[Union[comprehension_constraints, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, comprehension_constraints):

            

            def handle_ConsConstraint(o : ConsConstraint): 
                nonlocal stack
                assert isinstance(o, comprehension_constraints)

                
                stack.append(
                    o.tail
                )
                

                stack.append(
                    serialize_constraint(o.head)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'comprehension_constraints',
                        selection = 'ConsConstraint'
                    )]
                )
        


            def handle_SingleConstraint(o : SingleConstraint): 
                nonlocal stack
                assert isinstance(o, comprehension_constraints)

                
                stack.append(
                    serialize_constraint(o.contents)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'comprehension_constraints',
                        selection = 'SingleConstraint'
                    )]
                )
        


            match_comprehension_constraints(stack_item, ComprehensionConstraintsHandlers(
                case_ConsConstraint = handle_ConsConstraint,
                case_SingleConstraint = handle_SingleConstraint
            ))

        else:
            result += stack_item 

    return result
    




def serialize_sequence_ExceptHandler(
    o : sequence_ExceptHandler
) -> list[instance]:

    result = []

    stack : list[Union[sequence_ExceptHandler, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, sequence_ExceptHandler):

            

            def handle_ConsExceptHandler(o : ConsExceptHandler): 
                nonlocal stack
                assert isinstance(o, sequence_ExceptHandler)

                
                stack.append(
                    o.tail
                )
                

                stack.append(
                    serialize_ExceptHandler(o.head)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'sequence_ExceptHandler',
                        selection = 'ConsExceptHandler'
                    )]
                )
        


            def handle_SingleExceptHandler(o : SingleExceptHandler): 
                nonlocal stack
                assert isinstance(o, sequence_ExceptHandler)

                
                stack.append(
                    serialize_ExceptHandler(o.contents)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'sequence_ExceptHandler',
                        selection = 'SingleExceptHandler'
                    )]
                )
        


            match_sequence_ExceptHandler(stack_item, SequenceExceptHandlerHandlers(
                case_ConsExceptHandler = handle_ConsExceptHandler,
                case_SingleExceptHandler = handle_SingleExceptHandler
            ))

        else:
            result += stack_item 

    return result
    




def serialize_conditions(
    o : conditions
) -> list[instance]:

    result = []

    stack : list[Union[conditions, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, conditions):

            

            def handle_ElifCond(o : ElifCond): 
                nonlocal stack
                assert isinstance(o, conditions)

                
                stack.append(
                    o.tail
                )
                

                stack.append(
                    serialize_ElifBlock(o.contents)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'conditions',
                        selection = 'ElifCond'
                    )]
                )
        


            def handle_ElseCond(o : ElseCond): 
                nonlocal stack
                assert isinstance(o, conditions)

                
                stack.append(
                    serialize_ElseBlock(o.contents)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'conditions',
                        selection = 'ElseCond'
                    )]
                )
        


            def handle_NoCond(o : NoCond): 
                nonlocal stack
                assert isinstance(o, conditions)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'conditions',
                        selection = 'NoCond'
                    )]
                )
        


            match_conditions(stack_item, ConditionsHandlers(
                case_ElifCond = handle_ElifCond,
                case_ElseCond = handle_ElseCond,
                case_NoCond = handle_NoCond
            ))

        else:
            result += stack_item 

    return result
    




def serialize_function_def(
    o : function_def
) -> list[instance]:

    result = []

    stack : list[Union[function_def, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, function_def):

            

            def handle_FunctionDef(o : FunctionDef): 
                nonlocal stack
                assert isinstance(o, function_def)

                
                stack.append(
                    serialize_statements(o.body)
                )
                


                stack.append(
                    serialize_return_type(o.ret_typ)
                )
                


                stack.append(
                    serialize_parameters(o.params)
                )
                


                stack.append(
                    [lib.instance.make_Vocab(
                        options = 'identifier',
                        selection = o.name
                    )]
                )
            

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'function_def',
                        selection = 'FunctionDef'
                    )]
                )
        


            def handle_AsyncFunctionDef(o : AsyncFunctionDef): 
                nonlocal stack
                assert isinstance(o, function_def)

                
                stack.append(
                    serialize_statements(o.body)
                )
                


                stack.append(
                    serialize_return_type(o.ret_typ)
                )
                


                stack.append(
                    serialize_parameters(o.params)
                )
                


                stack.append(
                    [lib.instance.make_Vocab(
                        options = 'identifier',
                        selection = o.name
                    )]
                )
            

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'function_def',
                        selection = 'AsyncFunctionDef'
                    )]
                )
        


            match_function_def(stack_item, FunctionDefHandlers(
                case_FunctionDef = handle_FunctionDef,
                case_AsyncFunctionDef = handle_AsyncFunctionDef
            ))

        else:
            result += stack_item 

    return result
    




def serialize_stmt(
    o : stmt
) -> list[instance]:

    result = []

    stack : list[Union[stmt, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, stmt):

            

            def handle_DecFunctionDef(o : DecFunctionDef): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_function_def(o.fun_def)
                )
                

                stack.append(
                    serialize_decorators(o.decs)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'DecFunctionDef'
                    )]
                )
        


            def handle_DecAsyncFunctionDef(o : DecAsyncFunctionDef): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_function_def(o.fun_def)
                )
                

                stack.append(
                    serialize_decorators(o.decs)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'DecAsyncFunctionDef'
                    )]
                )
        


            def handle_DecClassDef(o : DecClassDef): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_ClassDef(o.class_def)
                )
                

                stack.append(
                    serialize_decorators(o.decs)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'DecClassDef'
                    )]
                )
        


            def handle_ReturnSomething(o : ReturnSomething): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_expr(o.contents)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'ReturnSomething'
                    )]
                )
        


            def handle_Return(o : Return): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'Return'
                    )]
                )
        


            def handle_Delete(o : Delete): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_comma_exprs(o.targets)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'Delete'
                    )]
                )
        


            def handle_Assign(o : Assign): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_expr(o.contents)
                )
                


                stack.append(
                    serialize_target_exprs(o.targets)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'Assign'
                    )]
                )
        


            def handle_AugAssign(o : AugAssign): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_expr(o.contents)
                )
                


                stack.append(
                    serialize_operator(o.op)
                )
                


                stack.append(
                    serialize_expr(o.target)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'AugAssign'
                    )]
                )
        


            def handle_TypedAssign(o : TypedAssign): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_expr(o.contents)
                )
                


                stack.append(
                    serialize_expr(o.type)
                )
                


                stack.append(
                    serialize_expr(o.target)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'TypedAssign'
                    )]
                )
        


            def handle_TypedDeclare(o : TypedDeclare): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_expr(o.type)
                )
                


                stack.append(
                    serialize_expr(o.target)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'TypedDeclare'
                    )]
                )
        


            def handle_For(o : For): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_statements(o.body)
                )
                


                stack.append(
                    serialize_expr(o.iter)
                )
                


                stack.append(
                    serialize_expr(o.target)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'For'
                    )]
                )
        


            def handle_ForElse(o : ForElse): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_ElseBlock(o.orelse)
                )
                

                stack.append(
                    serialize_statements(o.body)
                )
                


                stack.append(
                    serialize_expr(o.iter)
                )
                


                stack.append(
                    serialize_expr(o.target)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'ForElse'
                    )]
                )
        


            def handle_AsyncFor(o : AsyncFor): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_statements(o.body)
                )
                


                stack.append(
                    serialize_expr(o.iter)
                )
                


                stack.append(
                    serialize_expr(o.target)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'AsyncFor'
                    )]
                )
        


            def handle_AsyncForElse(o : AsyncForElse): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_ElseBlock(o.orelse)
                )
                

                stack.append(
                    serialize_statements(o.body)
                )
                


                stack.append(
                    serialize_expr(o.iter)
                )
                


                stack.append(
                    serialize_expr(o.target)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'AsyncForElse'
                    )]
                )
        


            def handle_While(o : While): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_statements(o.body)
                )
                


                stack.append(
                    serialize_expr(o.test)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'While'
                    )]
                )
        


            def handle_WhileElse(o : WhileElse): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_ElseBlock(o.orelse)
                )
                

                stack.append(
                    serialize_statements(o.body)
                )
                


                stack.append(
                    serialize_expr(o.test)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'WhileElse'
                    )]
                )
        


            def handle_If(o : If): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_conditions(o.orelse)
                )
                

                stack.append(
                    serialize_statements(o.body)
                )
                


                stack.append(
                    serialize_expr(o.test)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'If'
                    )]
                )
        


            def handle_With(o : With): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_statements(o.body)
                )
                


                stack.append(
                    serialize_sequence_Withitem(o.items)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'With'
                    )]
                )
        


            def handle_AsyncWith(o : AsyncWith): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_statements(o.body)
                )
                


                stack.append(
                    serialize_sequence_Withitem(o.items)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'AsyncWith'
                    )]
                )
        


            def handle_Raise(o : Raise): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'Raise'
                    )]
                )
        


            def handle_RaiseExc(o : RaiseExc): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_expr(o.exc)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'RaiseExc'
                    )]
                )
        


            def handle_RaiseFrom(o : RaiseFrom): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_expr(o.caus)
                )
                


                stack.append(
                    serialize_expr(o.exc)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'RaiseFrom'
                    )]
                )
        


            def handle_Try(o : Try): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_sequence_ExceptHandler(o.handlers)
                )
                

                stack.append(
                    serialize_statements(o.body)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'Try'
                    )]
                )
        


            def handle_TryElse(o : TryElse): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_ElseBlock(o.orelse)
                )
                

                stack.append(
                    serialize_sequence_ExceptHandler(o.handlers)
                )
                

                stack.append(
                    serialize_statements(o.body)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'TryElse'
                    )]
                )
        


            def handle_TryFin(o : TryFin): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_FinallyBlock(o.fin)
                )
                

                stack.append(
                    serialize_sequence_ExceptHandler(o.handlers)
                )
                

                stack.append(
                    serialize_statements(o.body)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'TryFin'
                    )]
                )
        


            def handle_TryElseFin(o : TryElseFin): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_FinallyBlock(o.fin)
                )
                

                stack.append(
                    serialize_ElseBlock(o.orelse)
                )
                

                stack.append(
                    serialize_sequence_ExceptHandler(o.handlers)
                )
                

                stack.append(
                    serialize_statements(o.body)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'TryElseFin'
                    )]
                )
        


            def handle_Assert(o : Assert): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_expr(o.test)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'Assert'
                    )]
                )
        


            def handle_AssertMsg(o : AssertMsg): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_expr(o.msg)
                )
                


                stack.append(
                    serialize_expr(o.test)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'AssertMsg'
                    )]
                )
        


            def handle_Import(o : Import): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_sequence_ImportName(o.names)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'Import'
                    )]
                )
        


            def handle_ImportFrom(o : ImportFrom): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_sequence_ImportName(o.names)
                )
                


                stack.append(
                    serialize_module_id(o.module)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'ImportFrom'
                    )]
                )
        


            def handle_ImportWildCard(o : ImportWildCard): 
                nonlocal stack
                assert isinstance(o, stmt)

                

                stack.append(
                    serialize_module_id(o.module)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'ImportWildCard'
                    )]
                )
        


            def handle_Global(o : Global): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_sequence_var(o.names)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'Global'
                    )]
                )
        


            def handle_Nonlocal(o : Nonlocal): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_sequence_var(o.names)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'Nonlocal'
                    )]
                )
        


            def handle_Expr(o : Expr): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    serialize_expr(o.contents)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'Expr'
                    )]
                )
        


            def handle_Pass(o : Pass): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'Pass'
                    )]
                )
        


            def handle_Break(o : Break): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'Break'
                    )]
                )
        


            def handle_Continue(o : Continue): 
                nonlocal stack
                assert isinstance(o, stmt)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'stmt',
                        selection = 'Continue'
                    )]
                )
        


            match_stmt(stack_item, StmtHandlers(
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

        else:
            result += stack_item 

    return result
    




def serialize_expr(
    o : expr
) -> list[instance]:

    result = []

    stack : list[Union[expr, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, expr):

            

            def handle_BoolOp(o : BoolOp): 
                nonlocal stack
                assert isinstance(o, expr)

                

                stack.append(
                    o.right
                )
                


                stack.append(
                    serialize_boolop(o.op)
                )
                


                stack.append(
                    o.left
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'BoolOp'
                    )]
                )
        


            def handle_NamedExpr(o : NamedExpr): 
                nonlocal stack
                assert isinstance(o, expr)

                
                stack.append(
                    o.contents
                )
                


                stack.append(
                    o.target
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'NamedExpr'
                    )]
                )
        


            def handle_BinOp(o : BinOp): 
                nonlocal stack
                assert isinstance(o, expr)

                

                stack.append(
                    o.right
                )
                


                stack.append(
                    serialize_operator(o.op)
                )
                


                stack.append(
                    o.left
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'BinOp'
                    )]
                )
        


            def handle_UnaryOp(o : UnaryOp): 
                nonlocal stack
                assert isinstance(o, expr)

                

                stack.append(
                    o.right
                )
                


                stack.append(
                    serialize_unaryop(o.op)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'UnaryOp'
                    )]
                )
        


            def handle_Lambda(o : Lambda): 
                nonlocal stack
                assert isinstance(o, expr)

                
                stack.append(
                    o.body
                )
                


                stack.append(
                    serialize_parameters(o.params)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'Lambda'
                    )]
                )
        


            def handle_IfExp(o : IfExp): 
                nonlocal stack
                assert isinstance(o, expr)

                
                stack.append(
                    o.orelse
                )
                


                stack.append(
                    o.test
                )
                


                stack.append(
                    o.body
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'IfExp'
                    )]
                )
        


            def handle_Dictionary(o : Dictionary): 
                nonlocal stack
                assert isinstance(o, expr)

                

                stack.append(
                    serialize_dictionary_contents(o.contents)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'Dictionary'
                    )]
                )
        


            def handle_EmptyDictionary(o : EmptyDictionary): 
                nonlocal stack
                assert isinstance(o, expr)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'EmptyDictionary'
                    )]
                )
        


            def handle_Set(o : Set): 
                nonlocal stack
                assert isinstance(o, expr)

                

                stack.append(
                    serialize_comma_exprs(o.contents)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'Set'
                    )]
                )
        


            def handle_ListComp(o : ListComp): 
                nonlocal stack
                assert isinstance(o, expr)

                

                stack.append(
                    serialize_comprehension_constraints(o.constraints)
                )
                

                stack.append(
                    o.contents
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'ListComp'
                    )]
                )
        


            def handle_SetComp(o : SetComp): 
                nonlocal stack
                assert isinstance(o, expr)

                

                stack.append(
                    serialize_comprehension_constraints(o.constraints)
                )
                

                stack.append(
                    o.contents
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'SetComp'
                    )]
                )
        


            def handle_DictionaryComp(o : DictionaryComp): 
                nonlocal stack
                assert isinstance(o, expr)

                

                stack.append(
                    serialize_comprehension_constraints(o.constraints)
                )
                

                stack.append(
                    o.contents
                )
                


                stack.append(
                    o.key
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'DictionaryComp'
                    )]
                )
        


            def handle_GeneratorExp(o : GeneratorExp): 
                nonlocal stack
                assert isinstance(o, expr)

                

                stack.append(
                    serialize_comprehension_constraints(o.constraints)
                )
                

                stack.append(
                    o.contents
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'GeneratorExp'
                    )]
                )
        


            def handle_Await(o : Await): 
                nonlocal stack
                assert isinstance(o, expr)

                
                stack.append(
                    o.contents
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'Await'
                    )]
                )
        


            def handle_YieldNothing(o : YieldNothing): 
                nonlocal stack
                assert isinstance(o, expr)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'YieldNothing'
                    )]
                )
        


            def handle_Yield(o : Yield): 
                nonlocal stack
                assert isinstance(o, expr)

                
                stack.append(
                    o.contents
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'Yield'
                    )]
                )
        


            def handle_YieldFrom(o : YieldFrom): 
                nonlocal stack
                assert isinstance(o, expr)

                
                stack.append(
                    o.contents
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'YieldFrom'
                    )]
                )
        


            def handle_Compare(o : Compare): 
                nonlocal stack
                assert isinstance(o, expr)

                
                stack.append(
                    serialize_comparisons(o.comps)
                )
                


                stack.append(
                    o.left
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'Compare'
                    )]
                )
        


            def handle_Call(o : Call): 
                nonlocal stack
                assert isinstance(o, expr)

                

                stack.append(
                    o.func
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'Call'
                    )]
                )
        


            def handle_CallArgs(o : CallArgs): 
                nonlocal stack
                assert isinstance(o, expr)

                

                stack.append(
                    serialize_arguments(o.args)
                )
                


                stack.append(
                    o.func
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'CallArgs'
                    )]
                )
        


            def handle_Integer(o : Integer): 
                nonlocal stack
                assert isinstance(o, expr)

                
                stack.append(
                    [lib.instance.make_Vocab(
                        options = 'integer',
                        selection = o.contents
                    )]
                )
            
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'Integer'
                    )]
                )
        


            def handle_Float(o : Float): 
                nonlocal stack
                assert isinstance(o, expr)

                
                stack.append(
                    [lib.instance.make_Vocab(
                        options = 'float',
                        selection = o.contents
                    )]
                )
            
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'Float'
                    )]
                )
        


            def handle_ConcatString(o : ConcatString): 
                nonlocal stack
                assert isinstance(o, expr)

                
                stack.append(
                    serialize_sequence_string(o.contents)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'ConcatString'
                    )]
                )
        


            def handle_True_(o : True_): 
                nonlocal stack
                assert isinstance(o, expr)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'True_'
                    )]
                )
        


            def handle_False_(o : False_): 
                nonlocal stack
                assert isinstance(o, expr)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'False_'
                    )]
                )
        


            def handle_None_(o : None_): 
                nonlocal stack
                assert isinstance(o, expr)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'None_'
                    )]
                )
        


            def handle_Ellip(o : Ellip): 
                nonlocal stack
                assert isinstance(o, expr)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'Ellip'
                    )]
                )
        


            def handle_Attribute(o : Attribute): 
                nonlocal stack
                assert isinstance(o, expr)

                
                stack.append(
                    [lib.instance.make_Vocab(
                        options = 'identifier',
                        selection = o.name
                    )]
                )
            


                stack.append(
                    o.contents
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'Attribute'
                    )]
                )
        


            def handle_Subscript(o : Subscript): 
                nonlocal stack
                assert isinstance(o, expr)

                

                stack.append(
                    o.slice
                )
                


                stack.append(
                    o.contents
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'Subscript'
                    )]
                )
        


            def handle_Starred(o : Starred): 
                nonlocal stack
                assert isinstance(o, expr)

                
                stack.append(
                    o.contents
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'Starred'
                    )]
                )
        


            def handle_Name(o : Name): 
                nonlocal stack
                assert isinstance(o, expr)

                
                stack.append(
                    [lib.instance.make_Vocab(
                        options = 'identifier',
                        selection = o.contents
                    )]
                )
            
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'Name'
                    )]
                )
        


            def handle_List(o : List): 
                nonlocal stack
                assert isinstance(o, expr)

                

                stack.append(
                    serialize_comma_exprs(o.contents)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'List'
                    )]
                )
        


            def handle_EmptyList(o : EmptyList): 
                nonlocal stack
                assert isinstance(o, expr)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'EmptyList'
                    )]
                )
        


            def handle_Tuple(o : Tuple): 
                nonlocal stack
                assert isinstance(o, expr)

                

                stack.append(
                    serialize_comma_exprs(o.contents)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'Tuple'
                    )]
                )
        


            def handle_EmptyTuple(o : EmptyTuple): 
                nonlocal stack
                assert isinstance(o, expr)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'EmptyTuple'
                    )]
                )
        


            def handle_Slice(o : Slice): 
                nonlocal stack
                assert isinstance(o, expr)

                
                stack.append(
                    serialize_option_expr(o.step)
                )
                


                stack.append(
                    serialize_option_expr(o.upper)
                )
                


                stack.append(
                    serialize_option_expr(o.lower)
                )
                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'expr',
                        selection = 'Slice'
                    )]
                )
        


            match_expr(stack_item, ExprHandlers(
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

        else:
            result += stack_item 

    return result
    




def serialize_boolop(
    o : boolop
) -> list[instance]:

    result = []

    stack : list[Union[boolop, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, boolop):

            

            def handle_And(o : And): 
                nonlocal stack
                assert isinstance(o, boolop)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'boolop',
                        selection = 'And'
                    )]
                )
        


            def handle_Or(o : Or): 
                nonlocal stack
                assert isinstance(o, boolop)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'boolop',
                        selection = 'Or'
                    )]
                )
        


            match_boolop(stack_item, BoolopHandlers(
                case_And = handle_And,
                case_Or = handle_Or
            ))

        else:
            result += stack_item 

    return result
    




def serialize_operator(
    o : operator
) -> list[instance]:

    result = []

    stack : list[Union[operator, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, operator):

            

            def handle_Add(o : Add): 
                nonlocal stack
                assert isinstance(o, operator)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'operator',
                        selection = 'Add'
                    )]
                )
        


            def handle_Sub(o : Sub): 
                nonlocal stack
                assert isinstance(o, operator)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'operator',
                        selection = 'Sub'
                    )]
                )
        


            def handle_Mult(o : Mult): 
                nonlocal stack
                assert isinstance(o, operator)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'operator',
                        selection = 'Mult'
                    )]
                )
        


            def handle_MatMult(o : MatMult): 
                nonlocal stack
                assert isinstance(o, operator)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'operator',
                        selection = 'MatMult'
                    )]
                )
        


            def handle_Div(o : Div): 
                nonlocal stack
                assert isinstance(o, operator)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'operator',
                        selection = 'Div'
                    )]
                )
        


            def handle_Mod(o : Mod): 
                nonlocal stack
                assert isinstance(o, operator)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'operator',
                        selection = 'Mod'
                    )]
                )
        


            def handle_Pow(o : Pow): 
                nonlocal stack
                assert isinstance(o, operator)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'operator',
                        selection = 'Pow'
                    )]
                )
        


            def handle_LShift(o : LShift): 
                nonlocal stack
                assert isinstance(o, operator)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'operator',
                        selection = 'LShift'
                    )]
                )
        


            def handle_RShift(o : RShift): 
                nonlocal stack
                assert isinstance(o, operator)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'operator',
                        selection = 'RShift'
                    )]
                )
        


            def handle_BitOr(o : BitOr): 
                nonlocal stack
                assert isinstance(o, operator)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'operator',
                        selection = 'BitOr'
                    )]
                )
        


            def handle_BitXor(o : BitXor): 
                nonlocal stack
                assert isinstance(o, operator)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'operator',
                        selection = 'BitXor'
                    )]
                )
        


            def handle_BitAnd(o : BitAnd): 
                nonlocal stack
                assert isinstance(o, operator)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'operator',
                        selection = 'BitAnd'
                    )]
                )
        


            def handle_FloorDiv(o : FloorDiv): 
                nonlocal stack
                assert isinstance(o, operator)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'operator',
                        selection = 'FloorDiv'
                    )]
                )
        


            match_operator(stack_item, OperatorHandlers(
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

        else:
            result += stack_item 

    return result
    




def serialize_unaryop(
    o : unaryop
) -> list[instance]:

    result = []

    stack : list[Union[unaryop, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, unaryop):

            

            def handle_Invert(o : Invert): 
                nonlocal stack
                assert isinstance(o, unaryop)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'unaryop',
                        selection = 'Invert'
                    )]
                )
        


            def handle_Not(o : Not): 
                nonlocal stack
                assert isinstance(o, unaryop)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'unaryop',
                        selection = 'Not'
                    )]
                )
        


            def handle_UAdd(o : UAdd): 
                nonlocal stack
                assert isinstance(o, unaryop)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'unaryop',
                        selection = 'UAdd'
                    )]
                )
        


            def handle_USub(o : USub): 
                nonlocal stack
                assert isinstance(o, unaryop)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'unaryop',
                        selection = 'USub'
                    )]
                )
        


            match_unaryop(stack_item, UnaryopHandlers(
                case_Invert = handle_Invert,
                case_Not = handle_Not,
                case_UAdd = handle_UAdd,
                case_USub = handle_USub
            ))

        else:
            result += stack_item 

    return result
    




def serialize_cmpop(
    o : cmpop
) -> list[instance]:

    result = []

    stack : list[Union[cmpop, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, cmpop):

            

            def handle_Eq(o : Eq): 
                nonlocal stack
                assert isinstance(o, cmpop)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'cmpop',
                        selection = 'Eq'
                    )]
                )
        


            def handle_NotEq(o : NotEq): 
                nonlocal stack
                assert isinstance(o, cmpop)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'cmpop',
                        selection = 'NotEq'
                    )]
                )
        


            def handle_Lt(o : Lt): 
                nonlocal stack
                assert isinstance(o, cmpop)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'cmpop',
                        selection = 'Lt'
                    )]
                )
        


            def handle_LtE(o : LtE): 
                nonlocal stack
                assert isinstance(o, cmpop)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'cmpop',
                        selection = 'LtE'
                    )]
                )
        


            def handle_Gt(o : Gt): 
                nonlocal stack
                assert isinstance(o, cmpop)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'cmpop',
                        selection = 'Gt'
                    )]
                )
        


            def handle_GtE(o : GtE): 
                nonlocal stack
                assert isinstance(o, cmpop)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'cmpop',
                        selection = 'GtE'
                    )]
                )
        


            def handle_Is(o : Is): 
                nonlocal stack
                assert isinstance(o, cmpop)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'cmpop',
                        selection = 'Is'
                    )]
                )
        


            def handle_IsNot(o : IsNot): 
                nonlocal stack
                assert isinstance(o, cmpop)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'cmpop',
                        selection = 'IsNot'
                    )]
                )
        


            def handle_In(o : In): 
                nonlocal stack
                assert isinstance(o, cmpop)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'cmpop',
                        selection = 'In'
                    )]
                )
        


            def handle_NotIn(o : NotIn): 
                nonlocal stack
                assert isinstance(o, cmpop)

                
                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'cmpop',
                        selection = 'NotIn'
                    )]
                )
        


            match_cmpop(stack_item, CmpopHandlers(
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

        else:
            result += stack_item 

    return result
    




def serialize_constraint(
    o : constraint
) -> list[instance]:

    result = []

    stack : list[Union[constraint, list[instance]]] = [o]
    while stack:
        stack_item = stack.pop()
        if isinstance(stack_item, constraint):

            

            def handle_AsyncConstraint(o : AsyncConstraint): 
                nonlocal stack
                assert isinstance(o, constraint)

                
                stack.append(
                    serialize_constraint_filters(o.filts)
                )
                

                stack.append(
                    serialize_expr(o.search_space)
                )
                


                stack.append(
                    serialize_expr(o.target)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'constraint',
                        selection = 'AsyncConstraint'
                    )]
                )
        


            def handle_Constraint(o : Constraint): 
                nonlocal stack
                assert isinstance(o, constraint)

                
                stack.append(
                    serialize_constraint_filters(o.filts)
                )
                

                stack.append(
                    serialize_expr(o.search_space)
                )
                


                stack.append(
                    serialize_expr(o.target)
                )
                

                stack.append(
                    [lib.instance.make_Grammar(
                        options = 'constraint',
                        selection = 'Constraint'
                    )]
                )
        


            match_constraint(stack_item, ConstraintHandlers(
                case_AsyncConstraint = handle_AsyncConstraint,
                case_Constraint = handle_Constraint
            ))

        else:
            result += stack_item 

    return result
    