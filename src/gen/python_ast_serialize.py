
from __future__ import annotations
from lib import production_instance as prod_inst 
from gen.python_ast import *
from gen.line_format import InLine, NewLine, IndentLine

import sys

sys.setrecursionlimit(10**6)



def serialize_Module(
    o : Module, depth : int = 0, relation : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:
    return (
        [prod_inst.make_Grammar(
            nonterminal = 'Module',
            sequence_id = 'Module',
            depth = depth,
            relation = relation,
            indent_width = indent_width,
            inline = inline
        )] +         serialize_statements(o.body, depth + 1, "body", 
            prod_inst.next_indent_width(indent_width, InLine()),
            True,
        )
    )


def serialize_CompareRight(
    o : CompareRight, depth : int = 0, relation : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:
    return (
        [prod_inst.make_Grammar(
            nonterminal = 'CompareRight',
            sequence_id = 'CompareRight',
            depth = depth,
            relation = relation,
            indent_width = indent_width,
            inline = inline
        )] +         serialize_cmpop(o.op, depth + 1, "op", 
            prod_inst.next_indent_width(indent_width, InLine()),
            True,
        ) +         serialize_expr(o.rand, depth + 1, "rand", 
            prod_inst.next_indent_width(indent_width, InLine()),
            True,
        )
    )


def serialize_ExceptHandler(
    o : ExceptHandler, depth : int = 0, relation : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:
    return (
        [prod_inst.make_Grammar(
            nonterminal = 'ExceptHandler',
            sequence_id = 'ExceptHandler',
            depth = depth,
            relation = relation,
            indent_width = indent_width,
            inline = inline
        )] +         serialize_except_arg(o.arg, depth + 1, "arg", 
            prod_inst.next_indent_width(indent_width, InLine()),
            True,
        ) +         serialize_statements(o.body, depth + 1, "body", 
            prod_inst.next_indent_width(indent_width, IndentLine()),
            False,
        )
    )


def serialize_Param(
    o : Param, depth : int = 0, relation : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:
    return (
        [prod_inst.make_Grammar(
            nonterminal = 'Param',
            sequence_id = 'Param',
            depth = depth,
            relation = relation,
            indent_width = indent_width,
            inline = inline
        )] +         [prod_inst.make_Vocab(
            choices_id = 'identifier',
            word = o.name,
            depth = depth + 1,
            relation = "name"
        )] +         serialize_param_type(o.type, depth + 1, "type", 
            prod_inst.next_indent_width(indent_width, InLine()),
            True,
        ) +         serialize_param_default(o.default, depth + 1, "default", 
            prod_inst.next_indent_width(indent_width, InLine()),
            True,
        )
    )


def serialize_Field(
    o : Field, depth : int = 0, relation : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:
    return (
        [prod_inst.make_Grammar(
            nonterminal = 'Field',
            sequence_id = 'Field',
            depth = depth,
            relation = relation,
            indent_width = indent_width,
            inline = inline
        )] +         serialize_expr(o.key, depth + 1, "key", 
            prod_inst.next_indent_width(indent_width, InLine()),
            True,
        ) +         serialize_expr(o.contents, depth + 1, "contents", 
            prod_inst.next_indent_width(indent_width, InLine()),
            True,
        )
    )


def serialize_ImportName(
    o : ImportName, depth : int = 0, relation : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:
    return (
        [prod_inst.make_Grammar(
            nonterminal = 'ImportName',
            sequence_id = 'ImportName',
            depth = depth,
            relation = relation,
            indent_width = indent_width,
            inline = inline
        )] +         [prod_inst.make_Vocab(
            choices_id = 'module_identifier',
            word = o.name,
            depth = depth + 1,
            relation = "name"
        )] +         serialize_alias(o.as_name, depth + 1, "as_name", 
            prod_inst.next_indent_width(indent_width, InLine()),
            True,
        )
    )


def serialize_Withitem(
    o : Withitem, depth : int = 0, relation : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:
    return (
        [prod_inst.make_Grammar(
            nonterminal = 'Withitem',
            sequence_id = 'Withitem',
            depth = depth,
            relation = relation,
            indent_width = indent_width,
            inline = inline
        )] +         serialize_expr(o.contet, depth + 1, "contet", 
            prod_inst.next_indent_width(indent_width, InLine()),
            True,
        ) +         serialize_alias_expr(o.target, depth + 1, "target", 
            prod_inst.next_indent_width(indent_width, InLine()),
            True,
        )
    )


def serialize_ClassDef(
    o : ClassDef, depth : int = 0, relation : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:
    return (
        [prod_inst.make_Grammar(
            nonterminal = 'ClassDef',
            sequence_id = 'ClassDef',
            depth = depth,
            relation = relation,
            indent_width = indent_width,
            inline = inline
        )] +         [prod_inst.make_Vocab(
            choices_id = 'identifier',
            word = o.name,
            depth = depth + 1,
            relation = "name"
        )] +         serialize_bases(o.bs, depth + 1, "bs", 
            prod_inst.next_indent_width(indent_width, InLine()),
            True,
        ) +         serialize_statements(o.body, depth + 1, "body", 
            prod_inst.next_indent_width(indent_width, IndentLine()),
            False,
        )
    )


def serialize_ElifBlock(
    o : ElifBlock, depth : int = 0, relation : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:
    return (
        [prod_inst.make_Grammar(
            nonterminal = 'ElifBlock',
            sequence_id = 'ElifBlock',
            depth = depth,
            relation = relation,
            indent_width = indent_width,
            inline = inline
        )] +         serialize_expr(o.test, depth + 1, "test", 
            prod_inst.next_indent_width(indent_width, InLine()),
            True,
        ) +         serialize_statements(o.body, depth + 1, "body", 
            prod_inst.next_indent_width(indent_width, IndentLine()),
            False,
        )
    )


def serialize_ElseBlock(
    o : ElseBlock, depth : int = 0, relation : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:
    return (
        [prod_inst.make_Grammar(
            nonterminal = 'ElseBlock',
            sequence_id = 'ElseBlock',
            depth = depth,
            relation = relation,
            indent_width = indent_width,
            inline = inline
        )] +         serialize_statements(o.body, depth + 1, "body", 
            prod_inst.next_indent_width(indent_width, IndentLine()),
            False,
        )
    )


def serialize_FinallyBlock(
    o : FinallyBlock, depth : int = 0, relation : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:
    return (
        [prod_inst.make_Grammar(
            nonterminal = 'FinallyBlock',
            sequence_id = 'FinallyBlock',
            depth = depth,
            relation = relation,
            indent_width = indent_width,
            inline = inline
        )] +         serialize_statements(o.body, depth + 1, "body", 
            prod_inst.next_indent_width(indent_width, IndentLine()),
            False,
        )
    )


def serialize_return_type(
    o : return_type, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_SomeReturnType(o : SomeReturnType): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'return_type',
                sequence_id = 'SomeReturnType',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_NoReturnType(o : NoReturnType): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'return_type',
                sequence_id = 'NoReturnType',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )


    return match_return_type(o, ReturnTypeHandlers(
        case_SomeReturnType = handle_SomeReturnType,  
        case_NoReturnType = handle_NoReturnType 
    ))



def serialize_module_id(
    o : module_id, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_SomeModuleId(o : SomeModuleId): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'module_id',
                sequence_id = 'SomeModuleId',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             [prod_inst.make_Vocab(
                choices_id = 'module_identifier',
                word = o.contents,
                depth = depth + 1,
                relation = "contents"
            )]        )

    def handle_NoModuleId(o : NoModuleId): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'module_id',
                sequence_id = 'NoModuleId',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )


    return match_module_id(o, ModuleIdHandlers(
        case_SomeModuleId = handle_SomeModuleId,  
        case_NoModuleId = handle_NoModuleId 
    ))



def serialize_except_arg(
    o : except_arg, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_SomeExceptArg(o : SomeExceptArg): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'except_arg',
                sequence_id = 'SomeExceptArg',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_SomeExceptArgName(o : SomeExceptArgName): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'except_arg',
                sequence_id = 'SomeExceptArgName',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            [prod_inst.make_Vocab(
                choices_id = 'identifier',
                word = o.name,
                depth = depth + 1,
                relation = "name"
            )]        )

    def handle_NoExceptArg(o : NoExceptArg): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'except_arg',
                sequence_id = 'NoExceptArg',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )


    return match_except_arg(o, ExceptArgHandlers(
        case_SomeExceptArg = handle_SomeExceptArg,  
        case_SomeExceptArgName = handle_SomeExceptArgName,  
        case_NoExceptArg = handle_NoExceptArg 
    ))



def serialize_param_type(
    o : param_type, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_SomeParamType(o : SomeParamType): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'param_type',
                sequence_id = 'SomeParamType',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_NoParamType(o : NoParamType): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'param_type',
                sequence_id = 'NoParamType',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )


    return match_param_type(o, ParamTypeHandlers(
        case_SomeParamType = handle_SomeParamType,  
        case_NoParamType = handle_NoParamType 
    ))



def serialize_param_default(
    o : param_default, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_SomeParamDefault(o : SomeParamDefault): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'param_default',
                sequence_id = 'SomeParamDefault',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_NoParamDefault(o : NoParamDefault): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'param_default',
                sequence_id = 'NoParamDefault',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )


    return match_param_default(o, ParamDefaultHandlers(
        case_SomeParamDefault = handle_SomeParamDefault,  
        case_NoParamDefault = handle_NoParamDefault 
    ))



def serialize_parameters_d(
    o : parameters_d, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_ConsKwParam(o : ConsKwParam): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'parameters_d',
                sequence_id = 'ConsKwParam',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_Param(o.head, depth + 1, "head", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_parameters_d(o.tail, depth + 1, "tail", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_SingleKwParam(o : SingleKwParam): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'parameters_d',
                sequence_id = 'SingleKwParam',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_Param(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_DictionarySplatParam(o : DictionarySplatParam): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'parameters_d',
                sequence_id = 'DictionarySplatParam',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_Param(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )


    return match_parameters_d(o, ParametersDHandlers(
        case_ConsKwParam = handle_ConsKwParam,  
        case_SingleKwParam = handle_SingleKwParam,  
        case_DictionarySplatParam = handle_DictionarySplatParam 
    ))



def serialize_parameters_c(
    o : parameters_c, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_SingleListSplatParam(o : SingleListSplatParam): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'parameters_c',
                sequence_id = 'SingleListSplatParam',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_Param(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_TransListSplatParam(o : TransListSplatParam): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'parameters_c',
                sequence_id = 'TransListSplatParam',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_Param(o.head, depth + 1, "head", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_parameters_d(o.tail, depth + 1, "tail", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_ParamsD(o : ParamsD): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'parameters_c',
                sequence_id = 'ParamsD',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_parameters_d(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )


    return match_parameters_c(o, ParametersCHandlers(
        case_SingleListSplatParam = handle_SingleListSplatParam,  
        case_TransListSplatParam = handle_TransListSplatParam,  
        case_ParamsD = handle_ParamsD 
    ))



def serialize_parameters_b(
    o : parameters_b, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_ConsParam(o : ConsParam): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'parameters_b',
                sequence_id = 'ConsParam',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_Param(o.head, depth + 1, "head", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_parameters_b(o.tail, depth + 1, "tail", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_SingleParam(o : SingleParam): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'parameters_b',
                sequence_id = 'SingleParam',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_Param(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_ParamsC(o : ParamsC): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'parameters_b',
                sequence_id = 'ParamsC',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_parameters_c(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )


    return match_parameters_b(o, ParametersBHandlers(
        case_ConsParam = handle_ConsParam,  
        case_SingleParam = handle_SingleParam,  
        case_ParamsC = handle_ParamsC 
    ))



def serialize_parameters(
    o : parameters, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_ParamsA(o : ParamsA): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'parameters',
                sequence_id = 'ParamsA',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_parameters_a(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_ParamsB(o : ParamsB): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'parameters',
                sequence_id = 'ParamsB',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_parameters_b(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_NoParam(o : NoParam): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'parameters',
                sequence_id = 'NoParam',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )


    return match_parameters(o, ParametersHandlers(
        case_ParamsA = handle_ParamsA,  
        case_ParamsB = handle_ParamsB,  
        case_NoParam = handle_NoParam 
    ))



def serialize_parameters_a(
    o : parameters_a, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_ConsPosParam(o : ConsPosParam): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'parameters_a',
                sequence_id = 'ConsPosParam',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_Param(o.head, depth + 1, "head", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_parameters_a(o.tail, depth + 1, "tail", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_SinglePosParam(o : SinglePosParam): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'parameters_a',
                sequence_id = 'SinglePosParam',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_Param(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_TransPosParam(o : TransPosParam): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'parameters_a',
                sequence_id = 'TransPosParam',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_Param(o.head, depth + 1, "head", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_parameters_b(o.tail, depth + 1, "tail", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )


    return match_parameters_a(o, ParametersAHandlers(
        case_ConsPosParam = handle_ConsPosParam,  
        case_SinglePosParam = handle_SinglePosParam,  
        case_TransPosParam = handle_TransPosParam 
    ))



def serialize_keyword(
    o : keyword, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_NamedKeyword(o : NamedKeyword): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'keyword',
                sequence_id = 'NamedKeyword',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             [prod_inst.make_Vocab(
                choices_id = 'identifier',
                word = o.name,
                depth = depth + 1,
                relation = "name"
            )] +             serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_SplatKeyword(o : SplatKeyword): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'keyword',
                sequence_id = 'SplatKeyword',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )


    return match_keyword(o, KeywordHandlers(
        case_NamedKeyword = handle_NamedKeyword,  
        case_SplatKeyword = handle_SplatKeyword 
    ))



def serialize_alias(
    o : alias, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_SomeAlias(o : SomeAlias): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'alias',
                sequence_id = 'SomeAlias',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             [prod_inst.make_Vocab(
                choices_id = 'identifier',
                word = o.contents,
                depth = depth + 1,
                relation = "contents"
            )]        )

    def handle_NoAlias(o : NoAlias): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'alias',
                sequence_id = 'NoAlias',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )


    return match_alias(o, AliasHandlers(
        case_SomeAlias = handle_SomeAlias,  
        case_NoAlias = handle_NoAlias 
    ))



def serialize_alias_expr(
    o : alias_expr, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_SomeAliasExpr(o : SomeAliasExpr): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'alias_expr',
                sequence_id = 'SomeAliasExpr',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_NoAliasExpr(o : NoAliasExpr): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'alias_expr',
                sequence_id = 'NoAliasExpr',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )


    return match_alias_expr(o, AliasExprHandlers(
        case_SomeAliasExpr = handle_SomeAliasExpr,  
        case_NoAliasExpr = handle_NoAliasExpr 
    ))



def serialize_bases(
    o : bases, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_SomeBases(o : SomeBases): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'bases',
                sequence_id = 'SomeBases',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_bases_a(o.bases, depth + 1, "bases", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_NoBases(o : NoBases): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'bases',
                sequence_id = 'NoBases',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )


    return match_bases(o, BasesHandlers(
        case_SomeBases = handle_SomeBases,  
        case_NoBases = handle_NoBases 
    ))



def serialize_bases_a(
    o : bases_a, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_ConsBase(o : ConsBase): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'bases_a',
                sequence_id = 'ConsBase',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.head, depth + 1, "head", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_bases_a(o.tail, depth + 1, "tail", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_SingleBase(o : SingleBase): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'bases_a',
                sequence_id = 'SingleBase',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_KeywordsBase(o : KeywordsBase): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'bases_a',
                sequence_id = 'KeywordsBase',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_keywords(o.kws, depth + 1, "kws", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )


    return match_bases_a(o, BasesAHandlers(
        case_ConsBase = handle_ConsBase,  
        case_SingleBase = handle_SingleBase,  
        case_KeywordsBase = handle_KeywordsBase 
    ))



def serialize_keywords(
    o : keywords, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_ConsKeyword(o : ConsKeyword): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'keywords',
                sequence_id = 'ConsKeyword',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_keyword(o.head, depth + 1, "head", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_keywords(o.tail, depth + 1, "tail", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_SingleKeyword(o : SingleKeyword): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'keywords',
                sequence_id = 'SingleKeyword',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_keyword(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )


    return match_keywords(o, KeywordsHandlers(
        case_ConsKeyword = handle_ConsKeyword,  
        case_SingleKeyword = handle_SingleKeyword 
    ))



def serialize_comparisons(
    o : comparisons, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_ConsCompareRight(o : ConsCompareRight): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'comparisons',
                sequence_id = 'ConsCompareRight',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_CompareRight(o.head, depth + 1, "head", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_comparisons(o.tail, depth + 1, "tail", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_SingleCompareRight(o : SingleCompareRight): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'comparisons',
                sequence_id = 'SingleCompareRight',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_CompareRight(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )


    return match_comparisons(o, ComparisonsHandlers(
        case_ConsCompareRight = handle_ConsCompareRight,  
        case_SingleCompareRight = handle_SingleCompareRight 
    ))



def serialize_option_expr(
    o : option_expr, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_SomeExpr(o : SomeExpr): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'option_expr',
                sequence_id = 'SomeExpr',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_NoExpr(o : NoExpr): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'option_expr',
                sequence_id = 'NoExpr',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )


    return match_option_expr(o, OptionExprHandlers(
        case_SomeExpr = handle_SomeExpr,  
        case_NoExpr = handle_NoExpr 
    ))



def serialize_comma_exprs(
    o : comma_exprs, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_ConsExpr(o : ConsExpr): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'comma_exprs',
                sequence_id = 'ConsExpr',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.head, depth + 1, "head", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_comma_exprs(o.tail, depth + 1, "tail", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_SingleExpr(o : SingleExpr): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'comma_exprs',
                sequence_id = 'SingleExpr',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )


    return match_comma_exprs(o, CommaExprsHandlers(
        case_ConsExpr = handle_ConsExpr,  
        case_SingleExpr = handle_SingleExpr 
    ))



def serialize_target_exprs(
    o : target_exprs, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_ConsTargetExpr(o : ConsTargetExpr): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'target_exprs',
                sequence_id = 'ConsTargetExpr',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.head, depth + 1, "head", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_target_exprs(o.tail, depth + 1, "tail", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_SingleTargetExpr(o : SingleTargetExpr): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'target_exprs',
                sequence_id = 'SingleTargetExpr',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )


    return match_target_exprs(o, TargetExprsHandlers(
        case_ConsTargetExpr = handle_ConsTargetExpr,  
        case_SingleTargetExpr = handle_SingleTargetExpr 
    ))



def serialize_decorators(
    o : decorators, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_ConsDec(o : ConsDec): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'decorators',
                sequence_id = 'ConsDec',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.head, depth + 1, "head", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_decorators(o.tail, depth + 1, "tail", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_NoDec(o : NoDec): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'decorators',
                sequence_id = 'NoDec',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )


    return match_decorators(o, DecoratorsHandlers(
        case_ConsDec = handle_ConsDec,  
        case_NoDec = handle_NoDec 
    ))



def serialize_constraint_filters(
    o : constraint_filters, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_ConsFilter(o : ConsFilter): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'constraint_filters',
                sequence_id = 'ConsFilter',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.head, depth + 1, "head", 
                prod_inst.next_indent_width(indent_width, NewLine()),
                False,
            ) +  
            serialize_constraint_filters(o.tail, depth + 1, "tail", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_SingleFilter(o : SingleFilter): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'constraint_filters',
                sequence_id = 'SingleFilter',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, NewLine()),
                False,
            ) 
        )

    def handle_NoFilter(o : NoFilter): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'constraint_filters',
                sequence_id = 'NoFilter',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )


    return match_constraint_filters(o, ConstraintFiltersHandlers(
        case_ConsFilter = handle_ConsFilter,  
        case_SingleFilter = handle_SingleFilter,  
        case_NoFilter = handle_NoFilter 
    ))



def serialize_sequence_string(
    o : sequence_string, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_ConsStr(o : ConsStr): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'sequence_string',
                sequence_id = 'ConsStr',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             [prod_inst.make_Vocab(
                choices_id = 'string',
                word = o.head,
                depth = depth + 1,
                relation = "head"
            )] +             serialize_sequence_string(o.tail, depth + 1, "tail", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_SingleStr(o : SingleStr): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'sequence_string',
                sequence_id = 'SingleStr',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             [prod_inst.make_Vocab(
                choices_id = 'string',
                word = o.contents,
                depth = depth + 1,
                relation = "contents"
            )]        )


    return match_sequence_string(o, SequenceStringHandlers(
        case_ConsStr = handle_ConsStr,  
        case_SingleStr = handle_SingleStr 
    ))



def serialize_arguments(
    o : arguments, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_ConsArg(o : ConsArg): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'arguments',
                sequence_id = 'ConsArg',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.head, depth + 1, "head", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_arguments(o.tail, depth + 1, "tail", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_SingleArg(o : SingleArg): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'arguments',
                sequence_id = 'SingleArg',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_KeywordsArg(o : KeywordsArg): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'arguments',
                sequence_id = 'KeywordsArg',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_keywords(o.kws, depth + 1, "kws", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )


    return match_arguments(o, ArgumentsHandlers(
        case_ConsArg = handle_ConsArg,  
        case_SingleArg = handle_SingleArg,  
        case_KeywordsArg = handle_KeywordsArg 
    ))



def serialize_dictionary_contents(
    o : dictionary_contents, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_ConsField(o : ConsField): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'dictionary_contents',
                sequence_id = 'ConsField',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_Field(o.head, depth + 1, "head", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_dictionary_contents(o.tail, depth + 1, "tail", 
                prod_inst.next_indent_width(indent_width, NewLine()),
                False,
            ) 
        )

    def handle_SingleField(o : SingleField): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'dictionary_contents',
                sequence_id = 'SingleField',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_Field(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )


    return match_dictionary_contents(o, DictionaryContentsHandlers(
        case_ConsField = handle_ConsField,  
        case_SingleField = handle_SingleField 
    ))



def serialize_sequence_var(
    o : sequence_var, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_ConsId(o : ConsId): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'sequence_var',
                sequence_id = 'ConsId',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             [prod_inst.make_Vocab(
                choices_id = 'identifier',
                word = o.head,
                depth = depth + 1,
                relation = "head"
            )] +             serialize_sequence_var(o.tail, depth + 1, "tail", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_SingleId(o : SingleId): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'sequence_var',
                sequence_id = 'SingleId',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             [prod_inst.make_Vocab(
                choices_id = 'identifier',
                word = o.contents,
                depth = depth + 1,
                relation = "contents"
            )]        )


    return match_sequence_var(o, SequenceVarHandlers(
        case_ConsId = handle_ConsId,  
        case_SingleId = handle_SingleId 
    ))



def serialize_sequence_ImportName(
    o : sequence_ImportName, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_ConsImportName(o : ConsImportName): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'sequence_ImportName',
                sequence_id = 'ConsImportName',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_ImportName(o.head, depth + 1, "head", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_sequence_ImportName(o.tail, depth + 1, "tail", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_SingleImportName(o : SingleImportName): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'sequence_ImportName',
                sequence_id = 'SingleImportName',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_ImportName(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )


    return match_sequence_ImportName(o, SequenceImportNameHandlers(
        case_ConsImportName = handle_ConsImportName,  
        case_SingleImportName = handle_SingleImportName 
    ))



def serialize_sequence_Withitem(
    o : sequence_Withitem, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_ConsWithitem(o : ConsWithitem): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'sequence_Withitem',
                sequence_id = 'ConsWithitem',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_Withitem(o.head, depth + 1, "head", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_sequence_Withitem(o.tail, depth + 1, "tail", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_SingleWithitem(o : SingleWithitem): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'sequence_Withitem',
                sequence_id = 'SingleWithitem',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_Withitem(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )


    return match_sequence_Withitem(o, SequenceWithitemHandlers(
        case_ConsWithitem = handle_ConsWithitem,  
        case_SingleWithitem = handle_SingleWithitem 
    ))



def serialize_statements(
    o : statements, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_ConsStmt(o : ConsStmt): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'statements',
                sequence_id = 'ConsStmt',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_stmt(o.head, depth + 1, "head", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_statements(o.tail, depth + 1, "tail", 
                prod_inst.next_indent_width(indent_width, NewLine()),
                False,
            ) 
        )

    def handle_SingleStmt(o : SingleStmt): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'statements',
                sequence_id = 'SingleStmt',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_stmt(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )


    return match_statements(o, StatementsHandlers(
        case_ConsStmt = handle_ConsStmt,  
        case_SingleStmt = handle_SingleStmt 
    ))



def serialize_comprehension_constraints(
    o : comprehension_constraints, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_ConsConstraint(o : ConsConstraint): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'comprehension_constraints',
                sequence_id = 'ConsConstraint',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_constraint(o.head, depth + 1, "head", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_comprehension_constraints(o.tail, depth + 1, "tail", 
                prod_inst.next_indent_width(indent_width, NewLine()),
                False,
            ) 
        )

    def handle_SingleConstraint(o : SingleConstraint): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'comprehension_constraints',
                sequence_id = 'SingleConstraint',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_constraint(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )


    return match_comprehension_constraints(o, ComprehensionConstraintsHandlers(
        case_ConsConstraint = handle_ConsConstraint,  
        case_SingleConstraint = handle_SingleConstraint 
    ))



def serialize_sequence_ExceptHandler(
    o : sequence_ExceptHandler, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_ConsExceptHandler(o : ConsExceptHandler): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'sequence_ExceptHandler',
                sequence_id = 'ConsExceptHandler',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_ExceptHandler(o.head, depth + 1, "head", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_sequence_ExceptHandler(o.tail, depth + 1, "tail", 
                prod_inst.next_indent_width(indent_width, NewLine()),
                False,
            ) 
        )

    def handle_SingleExceptHandler(o : SingleExceptHandler): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'sequence_ExceptHandler',
                sequence_id = 'SingleExceptHandler',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_ExceptHandler(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )


    return match_sequence_ExceptHandler(o, SequenceExceptHandlerHandlers(
        case_ConsExceptHandler = handle_ConsExceptHandler,  
        case_SingleExceptHandler = handle_SingleExceptHandler 
    ))



def serialize_conditions(
    o : conditions, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_ElifCond(o : ElifCond): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'conditions',
                sequence_id = 'ElifCond',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_ElifBlock(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, NewLine()),
                False,
            ) +  
            serialize_conditions(o.tail, depth + 1, "tail", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_ElseCond(o : ElseCond): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'conditions',
                sequence_id = 'ElseCond',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_ElseBlock(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, NewLine()),
                False,
            ) 
        )

    def handle_NoCond(o : NoCond): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'conditions',
                sequence_id = 'NoCond',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )


    return match_conditions(o, ConditionsHandlers(
        case_ElifCond = handle_ElifCond,  
        case_ElseCond = handle_ElseCond,  
        case_NoCond = handle_NoCond 
    ))



def serialize_function_def(
    o : function_def, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_FunctionDef(o : FunctionDef): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'function_def',
                sequence_id = 'FunctionDef',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             [prod_inst.make_Vocab(
                choices_id = 'identifier',
                word = o.name,
                depth = depth + 1,
                relation = "name"
            )] +             serialize_parameters(o.params, depth + 1, "params", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_return_type(o.ret_typ, depth + 1, "ret_typ", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_statements(o.body, depth + 1, "body", 
                prod_inst.next_indent_width(indent_width, IndentLine()),
                False,
            ) 
        )

    def handle_AsyncFunctionDef(o : AsyncFunctionDef): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'function_def',
                sequence_id = 'AsyncFunctionDef',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             [prod_inst.make_Vocab(
                choices_id = 'identifier',
                word = o.name,
                depth = depth + 1,
                relation = "name"
            )] +             serialize_parameters(o.params, depth + 1, "params", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_return_type(o.ret_typ, depth + 1, "ret_typ", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_statements(o.body, depth + 1, "body", 
                prod_inst.next_indent_width(indent_width, IndentLine()),
                False,
            ) 
        )


    return match_function_def(o, FunctionDefHandlers(
        case_FunctionDef = handle_FunctionDef,  
        case_AsyncFunctionDef = handle_AsyncFunctionDef 
    ))



def serialize_stmt(
    o : stmt, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_DecFunctionDef(o : DecFunctionDef): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'DecFunctionDef',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_decorators(o.decs, depth + 1, "decs", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_function_def(o.fun_def, depth + 1, "fun_def", 
                prod_inst.next_indent_width(indent_width, NewLine()),
                False,
            ) 
        )

    def handle_DecAsyncFunctionDef(o : DecAsyncFunctionDef): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'DecAsyncFunctionDef',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_decorators(o.decs, depth + 1, "decs", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_function_def(o.fun_def, depth + 1, "fun_def", 
                prod_inst.next_indent_width(indent_width, NewLine()),
                False,
            ) 
        )

    def handle_DecClassDef(o : DecClassDef): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'DecClassDef',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_decorators(o.decs, depth + 1, "decs", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_ClassDef(o.class_def, depth + 1, "class_def", 
                prod_inst.next_indent_width(indent_width, NewLine()),
                False,
            ) 
        )

    def handle_ReturnSomething(o : ReturnSomething): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'ReturnSomething',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_Return(o : Return): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'Return',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_Delete(o : Delete): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'Delete',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_comma_exprs(o.targets, depth + 1, "targets", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_Assign(o : Assign): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'Assign',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_target_exprs(o.targets, depth + 1, "targets", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_AugAssign(o : AugAssign): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'AugAssign',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.target, depth + 1, "target", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_operator(o.op, depth + 1, "op", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_TypedAssign(o : TypedAssign): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'TypedAssign',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.target, depth + 1, "target", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_expr(o.type, depth + 1, "type", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_TypedDeclare(o : TypedDeclare): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'TypedDeclare',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.target, depth + 1, "target", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_expr(o.type, depth + 1, "type", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_For(o : For): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'For',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.target, depth + 1, "target", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_expr(o.iter, depth + 1, "iter", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_statements(o.body, depth + 1, "body", 
                prod_inst.next_indent_width(indent_width, IndentLine()),
                False,
            ) 
        )

    def handle_ForElse(o : ForElse): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'ForElse',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.target, depth + 1, "target", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_expr(o.iter, depth + 1, "iter", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_statements(o.body, depth + 1, "body", 
                prod_inst.next_indent_width(indent_width, IndentLine()),
                False,
            ) +  
            serialize_ElseBlock(o.orelse, depth + 1, "orelse", 
                prod_inst.next_indent_width(indent_width, NewLine()),
                False,
            ) 
        )

    def handle_AsyncFor(o : AsyncFor): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'AsyncFor',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.target, depth + 1, "target", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_expr(o.iter, depth + 1, "iter", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_statements(o.body, depth + 1, "body", 
                prod_inst.next_indent_width(indent_width, IndentLine()),
                False,
            ) 
        )

    def handle_AsyncForElse(o : AsyncForElse): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'AsyncForElse',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.target, depth + 1, "target", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_expr(o.iter, depth + 1, "iter", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_statements(o.body, depth + 1, "body", 
                prod_inst.next_indent_width(indent_width, IndentLine()),
                False,
            ) +  
            serialize_ElseBlock(o.orelse, depth + 1, "orelse", 
                prod_inst.next_indent_width(indent_width, NewLine()),
                False,
            ) 
        )

    def handle_While(o : While): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'While',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.test, depth + 1, "test", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_statements(o.body, depth + 1, "body", 
                prod_inst.next_indent_width(indent_width, IndentLine()),
                False,
            ) 
        )

    def handle_WhileElse(o : WhileElse): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'WhileElse',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.test, depth + 1, "test", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_statements(o.body, depth + 1, "body", 
                prod_inst.next_indent_width(indent_width, IndentLine()),
                False,
            ) +  
            serialize_ElseBlock(o.orelse, depth + 1, "orelse", 
                prod_inst.next_indent_width(indent_width, NewLine()),
                False,
            ) 
        )

    def handle_If(o : If): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'If',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.test, depth + 1, "test", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_statements(o.body, depth + 1, "body", 
                prod_inst.next_indent_width(indent_width, IndentLine()),
                False,
            ) +  
            serialize_conditions(o.orelse, depth + 1, "orelse", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_With(o : With): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'With',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_sequence_Withitem(o.items, depth + 1, "items", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_statements(o.body, depth + 1, "body", 
                prod_inst.next_indent_width(indent_width, IndentLine()),
                False,
            ) 
        )

    def handle_AsyncWith(o : AsyncWith): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'AsyncWith',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_sequence_Withitem(o.items, depth + 1, "items", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_statements(o.body, depth + 1, "body", 
                prod_inst.next_indent_width(indent_width, IndentLine()),
                False,
            ) 
        )

    def handle_Raise(o : Raise): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'Raise',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_RaiseExc(o : RaiseExc): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'RaiseExc',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.exc, depth + 1, "exc", 
                prod_inst.next_indent_width(indent_width, IndentLine()),
                False,
            ) 
        )

    def handle_RaiseFrom(o : RaiseFrom): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'RaiseFrom',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.exc, depth + 1, "exc", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_expr(o.caus, depth + 1, "caus", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_Try(o : Try): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'Try',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_statements(o.body, depth + 1, "body", 
                prod_inst.next_indent_width(indent_width, IndentLine()),
                False,
            ) +  
            serialize_sequence_ExceptHandler(o.handlers, depth + 1, "handlers", 
                prod_inst.next_indent_width(indent_width, NewLine()),
                False,
            ) 
        )

    def handle_TryElse(o : TryElse): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'TryElse',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_statements(o.body, depth + 1, "body", 
                prod_inst.next_indent_width(indent_width, IndentLine()),
                False,
            ) +  
            serialize_sequence_ExceptHandler(o.handlers, depth + 1, "handlers", 
                prod_inst.next_indent_width(indent_width, NewLine()),
                False,
            ) +  
            serialize_ElseBlock(o.orelse, depth + 1, "orelse", 
                prod_inst.next_indent_width(indent_width, NewLine()),
                False,
            ) 
        )

    def handle_TryFin(o : TryFin): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'TryFin',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_statements(o.body, depth + 1, "body", 
                prod_inst.next_indent_width(indent_width, IndentLine()),
                False,
            ) +  
            serialize_sequence_ExceptHandler(o.handlers, depth + 1, "handlers", 
                prod_inst.next_indent_width(indent_width, NewLine()),
                False,
            ) +  
            serialize_FinallyBlock(o.fin, depth + 1, "fin", 
                prod_inst.next_indent_width(indent_width, NewLine()),
                False,
            ) 
        )

    def handle_TryElseFin(o : TryElseFin): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'TryElseFin',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_statements(o.body, depth + 1, "body", 
                prod_inst.next_indent_width(indent_width, IndentLine()),
                False,
            ) +  
            serialize_sequence_ExceptHandler(o.handlers, depth + 1, "handlers", 
                prod_inst.next_indent_width(indent_width, NewLine()),
                False,
            ) +  
            serialize_ElseBlock(o.orelse, depth + 1, "orelse", 
                prod_inst.next_indent_width(indent_width, NewLine()),
                False,
            ) +  
            serialize_FinallyBlock(o.fin, depth + 1, "fin", 
                prod_inst.next_indent_width(indent_width, NewLine()),
                False,
            ) 
        )

    def handle_Assert(o : Assert): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'Assert',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.test, depth + 1, "test", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_AssertMsg(o : AssertMsg): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'AssertMsg',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.test, depth + 1, "test", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_expr(o.msg, depth + 1, "msg", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_Import(o : Import): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'Import',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_sequence_ImportName(o.names, depth + 1, "names", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_ImportFrom(o : ImportFrom): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'ImportFrom',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_module_id(o.module, depth + 1, "module", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_sequence_ImportName(o.names, depth + 1, "names", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_ImportWildCard(o : ImportWildCard): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'ImportWildCard',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_module_id(o.module, depth + 1, "module", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_Global(o : Global): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'Global',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_sequence_var(o.names, depth + 1, "names", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_Nonlocal(o : Nonlocal): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'Nonlocal',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_sequence_var(o.names, depth + 1, "names", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_Expr(o : Expr): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'Expr',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_Pass(o : Pass): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'Pass',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_Break(o : Break): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'Break',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_Continue(o : Continue): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'stmt',
                sequence_id = 'Continue',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )


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



def serialize_expr(
    o : expr, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_BoolOp(o : BoolOp): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'BoolOp',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.left, depth + 1, "left", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_boolop(o.op, depth + 1, "op", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_expr(o.right, depth + 1, "right", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_NamedExpr(o : NamedExpr): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'NamedExpr',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.target, depth + 1, "target", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_BinOp(o : BinOp): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'BinOp',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.left, depth + 1, "left", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_operator(o.op, depth + 1, "op", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_expr(o.right, depth + 1, "right", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_UnaryOp(o : UnaryOp): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'UnaryOp',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_unaryop(o.op, depth + 1, "op", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_expr(o.right, depth + 1, "right", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_Lambda(o : Lambda): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'Lambda',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_parameters(o.params, depth + 1, "params", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_expr(o.body, depth + 1, "body", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_IfExp(o : IfExp): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'IfExp',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.body, depth + 1, "body", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_expr(o.test, depth + 1, "test", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_expr(o.orelse, depth + 1, "orelse", 
                prod_inst.next_indent_width(indent_width, NewLine()),
                False,
            ) 
        )

    def handle_Dictionary(o : Dictionary): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'Dictionary',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_dictionary_contents(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, IndentLine()),
                False,
            ) 
        )

    def handle_EmptyDictionary(o : EmptyDictionary): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'EmptyDictionary',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_Set(o : Set): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'Set',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_comma_exprs(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, IndentLine()),
                False,
            ) 
        )

    def handle_ListComp(o : ListComp): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'ListComp',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, IndentLine()),
                False,
            ) +  
            serialize_comprehension_constraints(o.constraints, depth + 1, "constraints", 
                prod_inst.next_indent_width(indent_width, IndentLine()),
                False,
            ) 
        )

    def handle_SetComp(o : SetComp): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'SetComp',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, IndentLine()),
                False,
            ) +  
            serialize_comprehension_constraints(o.constraints, depth + 1, "constraints", 
                prod_inst.next_indent_width(indent_width, IndentLine()),
                False,
            ) 
        )

    def handle_DictionaryComp(o : DictionaryComp): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'DictionaryComp',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.key, depth + 1, "key", 
                prod_inst.next_indent_width(indent_width, IndentLine()),
                False,
            ) +  
            serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_comprehension_constraints(o.constraints, depth + 1, "constraints", 
                prod_inst.next_indent_width(indent_width, IndentLine()),
                False,
            ) 
        )

    def handle_GeneratorExp(o : GeneratorExp): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'GeneratorExp',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, IndentLine()),
                False,
            ) +  
            serialize_comprehension_constraints(o.constraints, depth + 1, "constraints", 
                prod_inst.next_indent_width(indent_width, IndentLine()),
                False,
            ) 
        )

    def handle_Await(o : Await): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'Await',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_YieldNothing(o : YieldNothing): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'YieldNothing',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_Yield(o : Yield): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'Yield',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_YieldFrom(o : YieldFrom): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'YieldFrom',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_Compare(o : Compare): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'Compare',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.left, depth + 1, "left", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_comparisons(o.comps, depth + 1, "comps", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_Call(o : Call): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'Call',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.func, depth + 1, "func", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_CallArgs(o : CallArgs): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'CallArgs',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.func, depth + 1, "func", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_arguments(o.args, depth + 1, "args", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_Integer(o : Integer): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'Integer',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             [prod_inst.make_Vocab(
                choices_id = 'integer',
                word = o.contents,
                depth = depth + 1,
                relation = "contents"
            )]        )

    def handle_Float(o : Float): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'Float',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             [prod_inst.make_Vocab(
                choices_id = 'float',
                word = o.contents,
                depth = depth + 1,
                relation = "contents"
            )]        )

    def handle_ConcatString(o : ConcatString): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'ConcatString',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_sequence_string(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_True_(o : True_): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'True_',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_False_(o : False_): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'False_',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_None_(o : None_): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'None_',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_Ellip(o : Ellip): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'Ellip',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_Attribute(o : Attribute): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'Attribute',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            [prod_inst.make_Vocab(
                choices_id = 'identifier',
                word = o.name,
                depth = depth + 1,
                relation = "name"
            )]        )

    def handle_Subscript(o : Subscript): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'Subscript',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_expr(o.slice, depth + 1, "slice", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_Starred(o : Starred): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'Starred',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_Name(o : Name): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'Name',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             [prod_inst.make_Vocab(
                choices_id = 'identifier',
                word = o.contents,
                depth = depth + 1,
                relation = "contents"
            )]        )

    def handle_List(o : List): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'List',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_comma_exprs(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_EmptyList(o : EmptyList): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'EmptyList',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_Tuple(o : Tuple): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'Tuple',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_comma_exprs(o.contents, depth + 1, "contents", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_EmptyTuple(o : EmptyTuple): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'EmptyTuple',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_Slice(o : Slice): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'expr',
                sequence_id = 'Slice',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_option_expr(o.lower, depth + 1, "lower", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_option_expr(o.upper, depth + 1, "upper", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_option_expr(o.step, depth + 1, "step", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )


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



def serialize_boolop(
    o : boolop, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_And(o : And): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'boolop',
                sequence_id = 'And',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_Or(o : Or): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'boolop',
                sequence_id = 'Or',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )


    return match_boolop(o, BoolopHandlers(
        case_And = handle_And,  
        case_Or = handle_Or 
    ))



def serialize_operator(
    o : operator, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_Add(o : Add): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'operator',
                sequence_id = 'Add',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_Sub(o : Sub): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'operator',
                sequence_id = 'Sub',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_Mult(o : Mult): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'operator',
                sequence_id = 'Mult',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_MatMult(o : MatMult): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'operator',
                sequence_id = 'MatMult',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_Div(o : Div): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'operator',
                sequence_id = 'Div',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_Mod(o : Mod): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'operator',
                sequence_id = 'Mod',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_Pow(o : Pow): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'operator',
                sequence_id = 'Pow',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_LShift(o : LShift): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'operator',
                sequence_id = 'LShift',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_RShift(o : RShift): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'operator',
                sequence_id = 'RShift',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_BitOr(o : BitOr): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'operator',
                sequence_id = 'BitOr',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_BitXor(o : BitXor): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'operator',
                sequence_id = 'BitXor',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_BitAnd(o : BitAnd): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'operator',
                sequence_id = 'BitAnd',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_FloorDiv(o : FloorDiv): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'operator',
                sequence_id = 'FloorDiv',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )


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



def serialize_unaryop(
    o : unaryop, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_Invert(o : Invert): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'unaryop',
                sequence_id = 'Invert',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_Not(o : Not): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'unaryop',
                sequence_id = 'Not',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_UAdd(o : UAdd): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'unaryop',
                sequence_id = 'UAdd',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_USub(o : USub): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'unaryop',
                sequence_id = 'USub',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )


    return match_unaryop(o, UnaryopHandlers(
        case_Invert = handle_Invert,  
        case_Not = handle_Not,  
        case_UAdd = handle_UAdd,  
        case_USub = handle_USub 
    ))



def serialize_cmpop(
    o : cmpop, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_Eq(o : Eq): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'cmpop',
                sequence_id = 'Eq',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_NotEq(o : NotEq): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'cmpop',
                sequence_id = 'NotEq',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_Lt(o : Lt): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'cmpop',
                sequence_id = 'Lt',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_LtE(o : LtE): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'cmpop',
                sequence_id = 'LtE',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_Gt(o : Gt): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'cmpop',
                sequence_id = 'Gt',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_GtE(o : GtE): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'cmpop',
                sequence_id = 'GtE',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_Is(o : Is): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'cmpop',
                sequence_id = 'Is',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_IsNot(o : IsNot): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'cmpop',
                sequence_id = 'IsNot',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_In(o : In): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'cmpop',
                sequence_id = 'In',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )

    def handle_NotIn(o : NotIn): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'cmpop',
                sequence_id = 'NotIn',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )]        )


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



def serialize_constraint(
    o : constraint, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    def handle_AsyncConstraint(o : AsyncConstraint): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'constraint',
                sequence_id = 'AsyncConstraint',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.target, depth + 1, "target", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_expr(o.search_space, depth + 1, "search_space", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_constraint_filters(o.filts, depth + 1, "filts", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )

    def handle_Constraint(o : Constraint): 
        return (
            [prod_inst.make_Grammar(
                nonterminal = 'constraint',
                sequence_id = 'Constraint',
                depth = depth,
                relation = relation,
                indent_width = indent_width,
                inline = inline
            )] +             serialize_expr(o.target, depth + 1, "target", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_expr(o.search_space, depth + 1, "search_space", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) +  
            serialize_constraint_filters(o.filts, depth + 1, "filts", 
                prod_inst.next_indent_width(indent_width, InLine()),
                True,
            ) 
        )


    return match_constraint(o, ConstraintHandlers(
        case_AsyncConstraint = handle_AsyncConstraint,  
        case_Constraint = handle_Constraint 
    ))
