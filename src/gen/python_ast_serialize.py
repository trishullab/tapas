
from __future__ import annotations
from production import production, ProductionHandlers
import production as pro
from gen.python_ast import *
from gen.line_format import InLine, NewLine, IndentLine



def serialize_Module(
    o : Module, depth : int = 0, alias : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return (
        [pro.make_Node(
            lhs = 'Module',
            rhs = 'Module',
            depth = depth,
            alias = alias,
            indent_width = indent_width,
            inline = inline
        )] +
        serialize_statements(o.body, depth + 1, "body", 
            pro.next_indent_width(indent_width,  InLine()),
            True,
        ) +
        []
    )


def serialize_CompareRight(
    o : CompareRight, depth : int = 0, alias : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return (
        [pro.make_Node(
            lhs = 'CompareRight',
            rhs = 'CompareRight',
            depth = depth,
            alias = alias,
            indent_width = indent_width,
            inline = inline
        )] +
        serialize_cmpop(o.op, depth + 1, "op", 
            pro.next_indent_width(indent_width,  InLine()),
            True,
        ) +
        serialize_expr(o.rand, depth + 1, "rand", 
            pro.next_indent_width(indent_width,  InLine()),
            True,
        ) +
        []
    )


def serialize_ExceptHandler(
    o : ExceptHandler, depth : int = 0, alias : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return (
        [pro.make_Node(
            lhs = 'ExceptHandler',
            rhs = 'ExceptHandler',
            depth = depth,
            alias = alias,
            indent_width = indent_width,
            inline = inline
        )] +
        serialize_except_arg(o.arg, depth + 1, "arg", 
            pro.next_indent_width(indent_width,  InLine()),
            True,
        ) +
        serialize_statements(o.body, depth + 1, "body", 
            pro.next_indent_width(indent_width,  IndentLine()),
            False,
        ) +
        []
    )


def serialize_Param(
    o : Param, depth : int = 0, alias : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return (
        [pro.make_Node(
            lhs = 'Param',
            rhs = 'Param',
            depth = depth,
            alias = alias,
            indent_width = indent_width,
            inline = inline
        )] +
        serialize_Identifier(o.id, depth + 1, "id", 
            pro.next_indent_width(indent_width,  InLine()),
            True,
        ) +
        serialize_param_type(o.type, depth + 1, "type", 
            pro.next_indent_width(indent_width,  InLine()),
            True,
        ) +
        serialize_param_default(o.default, depth + 1, "default", 
            pro.next_indent_width(indent_width,  InLine()),
            True,
        ) +
        []
    )


def serialize_Field(
    o : Field, depth : int = 0, alias : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return (
        [pro.make_Node(
            lhs = 'Field',
            rhs = 'Field',
            depth = depth,
            alias = alias,
            indent_width = indent_width,
            inline = inline
        )] +
        serialize_expr(o.key, depth + 1, "key", 
            pro.next_indent_width(indent_width,  InLine()),
            True,
        ) +
        serialize_expr(o.content, depth + 1, "content", 
            pro.next_indent_width(indent_width,  InLine()),
            True,
        ) +
        []
    )


def serialize_ImportName(
    o : ImportName, depth : int = 0, alias : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return (
        [pro.make_Node(
            lhs = 'ImportName',
            rhs = 'ImportName',
            depth = depth,
            alias = alias,
            indent_width = indent_width,
            inline = inline
        )] +
        serialize_Identifier(o.name, depth + 1, "name", 
            pro.next_indent_width(indent_width,  InLine()),
            True,
        ) +
        serialize_alias(o.as_name, depth + 1, "as_name", 
            pro.next_indent_width(indent_width,  InLine()),
            True,
        ) +
        []
    )


def serialize_Identifier(
    o : Identifier, depth : int = 0, alias : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return (
        [pro.make_Node(
            lhs = 'Identifier',
            rhs = 'Identifier',
            depth = depth,
            alias = alias,
            indent_width = indent_width,
            inline = inline
        )] +
        [pro.make_Symbol(o.symbol, depth + 1, "symbol")] +
        []
    )


def serialize_Withitem(
    o : Withitem, depth : int = 0, alias : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return (
        [pro.make_Node(
            lhs = 'Withitem',
            rhs = 'Withitem',
            depth = depth,
            alias = alias,
            indent_width = indent_width,
            inline = inline
        )] +
        serialize_expr(o.contet, depth + 1, "contet", 
            pro.next_indent_width(indent_width,  InLine()),
            True,
        ) +
        serialize_alias_expr(o.target, depth + 1, "target", 
            pro.next_indent_width(indent_width,  InLine()),
            True,
        ) +
        []
    )


def serialize_ClassDef(
    o : ClassDef, depth : int = 0, alias : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return (
        [pro.make_Node(
            lhs = 'ClassDef',
            rhs = 'ClassDef',
            depth = depth,
            alias = alias,
            indent_width = indent_width,
            inline = inline
        )] +
        serialize_Identifier(o.name, depth + 1, "name", 
            pro.next_indent_width(indent_width,  InLine()),
            True,
        ) +
        serialize_bases(o.bs, depth + 1, "bs", 
            pro.next_indent_width(indent_width,  InLine()),
            True,
        ) +
        serialize_statements(o.body, depth + 1, "body", 
            pro.next_indent_width(indent_width,  IndentLine()),
            False,
        ) +
        []
    )


def serialize_return_type(
    o : return_type, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_return_type(o, ReturnTypeHandlers[list[production]](
        case_SomeReturnType = lambda o : (
            [pro.make_Node(
                lhs = 'return_type',
                rhs = 'SomeReturnType',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_NoReturnType = lambda o : (
            [pro.make_Node(
                lhs = 'return_type',
                rhs = 'NoReturnType',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        )
    ))


def serialize_module_id(
    o : module_id, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_module_id(o, ModuleIdHandlers[list[production]](
        case_SomeModuleId = lambda o : (
            [pro.make_Node(
                lhs = 'module_id',
                rhs = 'SomeModuleId',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_Identifier(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_NoModuleId = lambda o : (
            [pro.make_Node(
                lhs = 'module_id',
                rhs = 'NoModuleId',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        )
    ))


def serialize_except_arg(
    o : except_arg, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_except_arg(o, ExceptArgHandlers[list[production]](
        case_SomeExceptArg = lambda o : (
            [pro.make_Node(
                lhs = 'except_arg',
                rhs = 'SomeExceptArg',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_SomeExceptArgName = lambda o : (
            [pro.make_Node(
                lhs = 'except_arg',
                rhs = 'SomeExceptArgName',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_Identifier(o.name, depth + 1, "name", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_NoExceptArg = lambda o : (
            [pro.make_Node(
                lhs = 'except_arg',
                rhs = 'NoExceptArg',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        )
    ))


def serialize_param_type(
    o : param_type, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_param_type(o, ParamTypeHandlers[list[production]](
        case_SomeParamType = lambda o : (
            [pro.make_Node(
                lhs = 'param_type',
                rhs = 'SomeParamType',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_NoParamType = lambda o : (
            [pro.make_Node(
                lhs = 'param_type',
                rhs = 'NoParamType',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        )
    ))


def serialize_param_default(
    o : param_default, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_param_default(o, ParamDefaultHandlers[list[production]](
        case_SomeParamDefault = lambda o : (
            [pro.make_Node(
                lhs = 'param_default',
                rhs = 'SomeParamDefault',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_NoParamDefault = lambda o : (
            [pro.make_Node(
                lhs = 'param_default',
                rhs = 'NoParamDefault',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        )
    ))


def serialize_parameters_d(
    o : parameters_d, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_parameters_d(o, ParametersDHandlers[list[production]](
        case_ConsKwParam = lambda o : (
            [pro.make_Node(
                lhs = 'parameters_d',
                rhs = 'ConsKwParam',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_Param(o.head, depth + 1, "head", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_parameters_d(o.tail, depth + 1, "tail", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_SingleKwParam = lambda o : (
            [pro.make_Node(
                lhs = 'parameters_d',
                rhs = 'SingleKwParam',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_Param(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_DictionarySplatParam = lambda o : (
            [pro.make_Node(
                lhs = 'parameters_d',
                rhs = 'DictionarySplatParam',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_Param(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        )
    ))


def serialize_parameters_c(
    o : parameters_c, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_parameters_c(o, ParametersCHandlers[list[production]](
        case_SingleListSplatParam = lambda o : (
            [pro.make_Node(
                lhs = 'parameters_c',
                rhs = 'SingleListSplatParam',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_Param(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_TransListSplatParam = lambda o : (
            [pro.make_Node(
                lhs = 'parameters_c',
                rhs = 'TransListSplatParam',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_Param(o.head, depth + 1, "head", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_parameters_d(o.tail, depth + 1, "tail", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_ParamsD = lambda o : (
            [pro.make_Node(
                lhs = 'parameters_c',
                rhs = 'ParamsD',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_parameters_d(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        )
    ))


def serialize_parameters_b(
    o : parameters_b, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_parameters_b(o, ParametersBHandlers[list[production]](
        case_ConsParam = lambda o : (
            [pro.make_Node(
                lhs = 'parameters_b',
                rhs = 'ConsParam',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_Param(o.head, depth + 1, "head", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_parameters_b(o.tail, depth + 1, "tail", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_SingleParam = lambda o : (
            [pro.make_Node(
                lhs = 'parameters_b',
                rhs = 'SingleParam',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_Param(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_ParamsC = lambda o : (
            [pro.make_Node(
                lhs = 'parameters_b',
                rhs = 'ParamsC',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_parameters_c(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        )
    ))


def serialize_parameters(
    o : parameters, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_parameters(o, ParametersHandlers[list[production]](
        case_ParamsA = lambda o : (
            [pro.make_Node(
                lhs = 'parameters',
                rhs = 'ParamsA',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_parameters_a(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_ParamsB = lambda o : (
            [pro.make_Node(
                lhs = 'parameters',
                rhs = 'ParamsB',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_parameters_b(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_NoParam = lambda o : (
            [pro.make_Node(
                lhs = 'parameters',
                rhs = 'NoParam',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        )
    ))


def serialize_parameters_a(
    o : parameters_a, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_parameters_a(o, ParametersAHandlers[list[production]](
        case_ConsPosParam = lambda o : (
            [pro.make_Node(
                lhs = 'parameters_a',
                rhs = 'ConsPosParam',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_Param(o.head, depth + 1, "head", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_parameters_a(o.tail, depth + 1, "tail", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_SinglePosParam = lambda o : (
            [pro.make_Node(
                lhs = 'parameters_a',
                rhs = 'SinglePosParam',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_Param(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_TransPosParam = lambda o : (
            [pro.make_Node(
                lhs = 'parameters_a',
                rhs = 'TransPosParam',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_Param(o.head, depth + 1, "head", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_parameters_b(o.tail, depth + 1, "tail", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        )
    ))


def serialize_keyword(
    o : keyword, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_keyword(o, KeywordHandlers[list[production]](
        case_NamedKeyword = lambda o : (
            [pro.make_Node(
                lhs = 'keyword',
                rhs = 'NamedKeyword',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_Identifier(o.name, depth + 1, "name", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_SplatKeyword = lambda o : (
            [pro.make_Node(
                lhs = 'keyword',
                rhs = 'SplatKeyword',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        )
    ))


def serialize_alias(
    o : alias, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_alias(o, AliasHandlers[list[production]](
        case_SomeAlias = lambda o : (
            [pro.make_Node(
                lhs = 'alias',
                rhs = 'SomeAlias',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_Identifier(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_NoAlias = lambda o : (
            [pro.make_Node(
                lhs = 'alias',
                rhs = 'NoAlias',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        )
    ))


def serialize_alias_expr(
    o : alias_expr, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_alias_expr(o, AliasExprHandlers[list[production]](
        case_SomeAliasExpr = lambda o : (
            [pro.make_Node(
                lhs = 'alias_expr',
                rhs = 'SomeAliasExpr',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_NoAliasExpr = lambda o : (
            [pro.make_Node(
                lhs = 'alias_expr',
                rhs = 'NoAliasExpr',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        )
    ))


def serialize_bases(
    o : bases, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_bases(o, BasesHandlers[list[production]](
        case_SomeBases = lambda o : (
            [pro.make_Node(
                lhs = 'bases',
                rhs = 'SomeBases',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_bases_a(o.bases, depth + 1, "bases", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_NoBases = lambda o : (
            [pro.make_Node(
                lhs = 'bases',
                rhs = 'NoBases',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        )
    ))


def serialize_bases_a(
    o : bases_a, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_bases_a(o, BasesAHandlers[list[production]](
        case_ConsBase = lambda o : (
            [pro.make_Node(
                lhs = 'bases_a',
                rhs = 'ConsBase',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.head, depth + 1, "head", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_bases_a(o.tail, depth + 1, "tail", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_SingleBase = lambda o : (
            [pro.make_Node(
                lhs = 'bases_a',
                rhs = 'SingleBase',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_KeywordsBase = lambda o : (
            [pro.make_Node(
                lhs = 'bases_a',
                rhs = 'KeywordsBase',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_keywords(o.kws, depth + 1, "kws", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        )
    ))


def serialize_keywords(
    o : keywords, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_keywords(o, KeywordsHandlers[list[production]](
        case_ConsKeyword = lambda o : (
            [pro.make_Node(
                lhs = 'keywords',
                rhs = 'ConsKeyword',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_keyword(o.head, depth + 1, "head", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_keywords(o.tail, depth + 1, "tail", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_SingleKeyword = lambda o : (
            [pro.make_Node(
                lhs = 'keywords',
                rhs = 'SingleKeyword',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_keyword(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        )
    ))


def serialize_comparisons(
    o : comparisons, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_comparisons(o, ComparisonsHandlers[list[production]](
        case_ConsCompareRight = lambda o : (
            [pro.make_Node(
                lhs = 'comparisons',
                rhs = 'ConsCompareRight',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_CompareRight(o.head, depth + 1, "head", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_comparisons(o.tail, depth + 1, "tail", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_SingleCompareRight = lambda o : (
            [pro.make_Node(
                lhs = 'comparisons',
                rhs = 'SingleCompareRight',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_CompareRight(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        )
    ))


def serialize_option_expr(
    o : option_expr, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_option_expr(o, OptionExprHandlers[list[production]](
        case_SomeExpr = lambda o : (
            [pro.make_Node(
                lhs = 'option_expr',
                rhs = 'SomeExpr',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_NoExpr = lambda o : (
            [pro.make_Node(
                lhs = 'option_expr',
                rhs = 'NoExpr',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        )
    ))


def serialize_comma_exprs(
    o : comma_exprs, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_comma_exprs(o, CommaExprsHandlers[list[production]](
        case_ConsExpr = lambda o : (
            [pro.make_Node(
                lhs = 'comma_exprs',
                rhs = 'ConsExpr',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.head, depth + 1, "head", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_comma_exprs(o.tail, depth + 1, "tail", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_SingleExpr = lambda o : (
            [pro.make_Node(
                lhs = 'comma_exprs',
                rhs = 'SingleExpr',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        )
    ))


def serialize_decorators(
    o : decorators, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_decorators(o, DecoratorsHandlers[list[production]](
        case_ConsDec = lambda o : (
            [pro.make_Node(
                lhs = 'decorators',
                rhs = 'ConsDec',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.head, depth + 1, "head", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_decorators(o.tail, depth + 1, "tail", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_NoDec = lambda o : (
            [pro.make_Node(
                lhs = 'decorators',
                rhs = 'NoDec',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        )
    ))


def serialize_constraint_filters(
    o : constraint_filters, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_constraint_filters(o, ConstraintFiltersHandlers[list[production]](
        case_ConsFilter = lambda o : (
            [pro.make_Node(
                lhs = 'constraint_filters',
                rhs = 'ConsFilter',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.head, depth + 1, "head", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_constraint_filters(o.tail, depth + 1, "tail", 
                pro.next_indent_width(indent_width, NewLine()),
                False,
            ) + 
            []
        ),
        case_SingleFilter = lambda o : (
            [pro.make_Node(
                lhs = 'constraint_filters',
                rhs = 'SingleFilter',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        )
    ))


def serialize_sequence_str(
    o : sequence_str, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_sequence_str(o, SequenceStrHandlers[list[production]](
        case_ConsStr = lambda o : (
            [pro.make_Node(
                lhs = 'sequence_str',
                rhs = 'ConsStr',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            [pro.make_Symbol(o.head, depth + 1, "head")] +
            serialize_sequence_str(o.tail, depth + 1, "tail", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_SingleStr = lambda o : (
            [pro.make_Node(
                lhs = 'sequence_str',
                rhs = 'SingleStr',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            [pro.make_Symbol(o.content, depth + 1, "content")] +
            []
        )
    ))


def serialize_arguments(
    o : arguments, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_arguments(o, ArgumentsHandlers[list[production]](
        case_ConsArg = lambda o : (
            [pro.make_Node(
                lhs = 'arguments',
                rhs = 'ConsArg',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.head, depth + 1, "head", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_arguments(o.tail, depth + 1, "tail", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_SingleArg = lambda o : (
            [pro.make_Node(
                lhs = 'arguments',
                rhs = 'SingleArg',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_KeywordsArg = lambda o : (
            [pro.make_Node(
                lhs = 'arguments',
                rhs = 'KeywordsArg',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_keywords(o.kws, depth + 1, "kws", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        )
    ))


def serialize_dictionary_contents(
    o : dictionary_contents, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_dictionary_contents(o, DictionaryContentsHandlers[list[production]](
        case_ConsField = lambda o : (
            [pro.make_Node(
                lhs = 'dictionary_contents',
                rhs = 'ConsField',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_Field(o.head, depth + 1, "head", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_dictionary_contents(o.tail, depth + 1, "tail", 
                pro.next_indent_width(indent_width, NewLine()),
                False,
            ) + 
            []
        ),
        case_SingleField = lambda o : (
            [pro.make_Node(
                lhs = 'dictionary_contents',
                rhs = 'SingleField',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_Field(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        )
    ))


def serialize_sequence_Identifier(
    o : sequence_Identifier, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_sequence_Identifier(o, SequenceIdentifierHandlers[list[production]](
        case_ConsId = lambda o : (
            [pro.make_Node(
                lhs = 'sequence_Identifier',
                rhs = 'ConsId',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_Identifier(o.head, depth + 1, "head", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_sequence_Identifier(o.tail, depth + 1, "tail", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_SingleId = lambda o : (
            [pro.make_Node(
                lhs = 'sequence_Identifier',
                rhs = 'SingleId',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_Identifier(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        )
    ))


def serialize_sequence_ImportName(
    o : sequence_ImportName, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_sequence_ImportName(o, SequenceImportNameHandlers[list[production]](
        case_ConsImportName = lambda o : (
            [pro.make_Node(
                lhs = 'sequence_ImportName',
                rhs = 'ConsImportName',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_ImportName(o.head, depth + 1, "head", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_sequence_ImportName(o.tail, depth + 1, "tail", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_SingleImportName = lambda o : (
            [pro.make_Node(
                lhs = 'sequence_ImportName',
                rhs = 'SingleImportName',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_ImportName(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        )
    ))


def serialize_sequence_Withitem(
    o : sequence_Withitem, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_sequence_Withitem(o, SequenceWithitemHandlers[list[production]](
        case_ConsWithitem = lambda o : (
            [pro.make_Node(
                lhs = 'sequence_Withitem',
                rhs = 'ConsWithitem',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_Withitem(o.head, depth + 1, "head", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_sequence_Withitem(o.tail, depth + 1, "tail", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_SingleWithitem = lambda o : (
            [pro.make_Node(
                lhs = 'sequence_Withitem',
                rhs = 'SingleWithitem',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_Withitem(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        )
    ))


def serialize_statements(
    o : statements, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_statements(o, StatementsHandlers[list[production]](
        case_ConsStmt = lambda o : (
            [pro.make_Node(
                lhs = 'statements',
                rhs = 'ConsStmt',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_stmt(o.head, depth + 1, "head", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_statements(o.tail, depth + 1, "tail", 
                pro.next_indent_width(indent_width, NewLine()),
                False,
            ) + 
            []
        ),
        case_SingleStmt = lambda o : (
            [pro.make_Node(
                lhs = 'statements',
                rhs = 'SingleStmt',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_stmt(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        )
    ))


def serialize_comprehension_constraints(
    o : comprehension_constraints, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_comprehension_constraints(o, ComprehensionConstraintsHandlers[list[production]](
        case_ConsConstraint = lambda o : (
            [pro.make_Node(
                lhs = 'comprehension_constraints',
                rhs = 'ConsConstraint',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_constraint(o.head, depth + 1, "head", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_comprehension_constraints(o.tail, depth + 1, "tail", 
                pro.next_indent_width(indent_width, NewLine()),
                False,
            ) + 
            []
        ),
        case_SingleConstraint = lambda o : (
            [pro.make_Node(
                lhs = 'comprehension_constraints',
                rhs = 'SingleConstraint',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_constraint(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        )
    ))


def serialize_sequence_ExceptHandler(
    o : sequence_ExceptHandler, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_sequence_ExceptHandler(o, SequenceExceptHandlerHandlers[list[production]](
        case_ConsExceptHandler = lambda o : (
            [pro.make_Node(
                lhs = 'sequence_ExceptHandler',
                rhs = 'ConsExceptHandler',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_ExceptHandler(o.head, depth + 1, "head", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_sequence_ExceptHandler(o.tail, depth + 1, "tail", 
                pro.next_indent_width(indent_width, NewLine()),
                False,
            ) + 
            []
        ),
        case_SingleExceptHandler = lambda o : (
            [pro.make_Node(
                lhs = 'sequence_ExceptHandler',
                rhs = 'SingleExceptHandler',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_ExceptHandler(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        )
    ))


def serialize_conditions(
    o : conditions, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_conditions(o, ConditionsHandlers[list[production]](
        case_ElifCond = lambda o : (
            [pro.make_Node(
                lhs = 'conditions',
                rhs = 'ElifCond',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.test, depth + 1, "test", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_statements(o.body, depth + 1, "body", 
                pro.next_indent_width(indent_width, IndentLine()),
                False,
            ) + 
            serialize_conditions(o.tail, depth + 1, "tail", 
                pro.next_indent_width(indent_width, NewLine()),
                False,
            ) + 
            []
        ),
        case_ElseCond = lambda o : (
            [pro.make_Node(
                lhs = 'conditions',
                rhs = 'ElseCond',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_else_block(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, NewLine()),
                False,
            ) + 
            []
        )
    ))


def serialize_else_block(
    o : else_block, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_else_block(o, ElseBlockHandlers[list[production]](
        case_SomeElseBlock = lambda o : (
            [pro.make_Node(
                lhs = 'else_block',
                rhs = 'SomeElseBlock',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_statements(o.body, depth + 1, "body", 
                pro.next_indent_width(indent_width, IndentLine()),
                False,
            ) + 
            []
        ),
        case_NoElseBlock = lambda o : (
            [pro.make_Node(
                lhs = 'else_block',
                rhs = 'NoElseBlock',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        )
    ))


def serialize_final(
    o : final, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_final(o, FinalHandlers[list[production]](
        case_SomeFinal = lambda o : (
            [pro.make_Node(
                lhs = 'final',
                rhs = 'SomeFinal',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_statements(o.body, depth + 1, "body", 
                pro.next_indent_width(indent_width, IndentLine()),
                False,
            ) + 
            []
        ),
        case_NoFinal = lambda o : (
            [pro.make_Node(
                lhs = 'final',
                rhs = 'NoFinal',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        )
    ))


def serialize_function_def(
    o : function_def, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_function_def(o, FunctionDefHandlers[list[production]](
        case_FunctionDef = lambda o : (
            [pro.make_Node(
                lhs = 'function_def',
                rhs = 'FunctionDef',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_Identifier(o.name, depth + 1, "name", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_parameters(o.params, depth + 1, "params", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_return_type(o.ret_typ, depth + 1, "ret_typ", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_statements(o.body, depth + 1, "body", 
                pro.next_indent_width(indent_width, IndentLine()),
                False,
            ) + 
            []
        ),
        case_AsyncFunctionDef = lambda o : (
            [pro.make_Node(
                lhs = 'function_def',
                rhs = 'AsyncFunctionDef',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_Identifier(o.name, depth + 1, "name", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_parameters(o.params, depth + 1, "params", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_return_type(o.ret_typ, depth + 1, "ret_typ", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_statements(o.body, depth + 1, "body", 
                pro.next_indent_width(indent_width, IndentLine()),
                False,
            ) + 
            []
        )
    ))


def serialize_stmt(
    o : stmt, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_stmt(o, StmtHandlers[list[production]](
        case_DecFunctionDef = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'DecFunctionDef',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_decorators(o.decs, depth + 1, "decs", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_function_def(o.fun_def, depth + 1, "fun_def", 
                pro.next_indent_width(indent_width, NewLine()),
                False,
            ) + 
            []
        ),
        case_DecAsyncFunctionDef = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'DecAsyncFunctionDef',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_decorators(o.decs, depth + 1, "decs", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_function_def(o.fun_def, depth + 1, "fun_def", 
                pro.next_indent_width(indent_width, NewLine()),
                False,
            ) + 
            []
        ),
        case_DecClassDef = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'DecClassDef',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_decorators(o.decs, depth + 1, "decs", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_ClassDef(o.class_def, depth + 1, "class_def", 
                pro.next_indent_width(indent_width, NewLine()),
                False,
            ) + 
            []
        ),
        case_ReturnSomething = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'ReturnSomething',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_Return = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'Return',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_Delete = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'Delete',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_comma_exprs(o.targets, depth + 1, "targets", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_Assign = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'Assign',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_comma_exprs(o.targets, depth + 1, "targets", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_AugAssign = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'AugAssign',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.target, depth + 1, "target", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_operator(o.op, depth + 1, "op", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_TypedAssign = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'TypedAssign',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.target, depth + 1, "target", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_expr(o.type, depth + 1, "type", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_TypedDeclare = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'TypedDeclare',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.target, depth + 1, "target", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_expr(o.type, depth + 1, "type", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_For = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'For',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.target, depth + 1, "target", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_expr(o.iter, depth + 1, "iter", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_statements(o.body, depth + 1, "body", 
                pro.next_indent_width(indent_width, IndentLine()),
                False,
            ) + 
            serialize_else_block(o.orelse, depth + 1, "orelse", 
                pro.next_indent_width(indent_width, NewLine()),
                False,
            ) + 
            []
        ),
        case_AsyncFor = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'AsyncFor',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.target, depth + 1, "target", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_expr(o.iter, depth + 1, "iter", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_statements(o.body, depth + 1, "body", 
                pro.next_indent_width(indent_width, IndentLine()),
                False,
            ) + 
            serialize_else_block(o.orelse, depth + 1, "orelse", 
                pro.next_indent_width(indent_width, NewLine()),
                False,
            ) + 
            []
        ),
        case_While = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'While',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.test, depth + 1, "test", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_statements(o.body, depth + 1, "body", 
                pro.next_indent_width(indent_width, IndentLine()),
                False,
            ) + 
            serialize_else_block(o.orelse, depth + 1, "orelse", 
                pro.next_indent_width(indent_width, NewLine()),
                False,
            ) + 
            []
        ),
        case_If = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'If',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.test, depth + 1, "test", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_statements(o.body, depth + 1, "body", 
                pro.next_indent_width(indent_width, IndentLine()),
                False,
            ) + 
            serialize_conditions(o.orelse, depth + 1, "orelse", 
                pro.next_indent_width(indent_width, NewLine()),
                False,
            ) + 
            []
        ),
        case_With = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'With',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_sequence_Withitem(o.items, depth + 1, "items", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_statements(o.body, depth + 1, "body", 
                pro.next_indent_width(indent_width, IndentLine()),
                False,
            ) + 
            []
        ),
        case_AsyncWith = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'AsyncWith',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_sequence_Withitem(o.items, depth + 1, "items", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_statements(o.body, depth + 1, "body", 
                pro.next_indent_width(indent_width, IndentLine()),
                False,
            ) + 
            []
        ),
        case_Raise = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'Raise',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_RaiseExc = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'RaiseExc',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.exc, depth + 1, "exc", 
                pro.next_indent_width(indent_width, IndentLine()),
                False,
            ) + 
            []
        ),
        case_RaiseFrom = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'RaiseFrom',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.exc, depth + 1, "exc", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_expr(o.caus, depth + 1, "caus", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_Try = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'Try',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_statements(o.body, depth + 1, "body", 
                pro.next_indent_width(indent_width, IndentLine()),
                False,
            ) + 
            serialize_sequence_ExceptHandler(o.handlers, depth + 1, "handlers", 
                pro.next_indent_width(indent_width, NewLine()),
                False,
            ) + 
            serialize_else_block(o.orelse, depth + 1, "orelse", 
                pro.next_indent_width(indent_width, NewLine()),
                False,
            ) + 
            serialize_final(o.fin, depth + 1, "fin", 
                pro.next_indent_width(indent_width, NewLine()),
                False,
            ) + 
            []
        ),
        case_Assert = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'Assert',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.test, depth + 1, "test", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_AssertMsg = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'AssertMsg',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.test, depth + 1, "test", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_expr(o.msg, depth + 1, "msg", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_Import = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'Import',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_sequence_ImportName(o.names, depth + 1, "names", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_ImportFrom = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'ImportFrom',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_module_id(o.module, depth + 1, "module", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_sequence_ImportName(o.names, depth + 1, "names", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_ImportWildCard = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'ImportWildCard',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_module_id(o.module, depth + 1, "module", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_Global = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'Global',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_sequence_Identifier(o.names, depth + 1, "names", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_Nonlocal = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'Nonlocal',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_sequence_Identifier(o.names, depth + 1, "names", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_Expr = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'Expr',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_Pass = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'Pass',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_Break = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'Break',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_Continue = lambda o : (
            [pro.make_Node(
                lhs = 'stmt',
                rhs = 'Continue',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        )
    ))


def serialize_expr(
    o : expr, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_expr(o, ExprHandlers[list[production]](
        case_BoolOp = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'BoolOp',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.left, depth + 1, "left", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_boolop(o.op, depth + 1, "op", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_expr(o.right, depth + 1, "right", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_NamedExpr = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'NamedExpr',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.target, depth + 1, "target", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_BinOp = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'BinOp',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.left, depth + 1, "left", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_operator(o.op, depth + 1, "op", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_expr(o.right, depth + 1, "right", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_UnaryOp = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'UnaryOp',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_unaryop(o.op, depth + 1, "op", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_expr(o.right, depth + 1, "right", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_Lambda = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'Lambda',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_parameters(o.params, depth + 1, "params", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_expr(o.body, depth + 1, "body", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_IfExp = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'IfExp',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.body, depth + 1, "body", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_expr(o.test, depth + 1, "test", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_expr(o.orelse, depth + 1, "orelse", 
                pro.next_indent_width(indent_width, NewLine()),
                False,
            ) + 
            []
        ),
        case_Dictionary = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'Dictionary',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_dictionary_contents(o.contents, depth + 1, "contents", 
                pro.next_indent_width(indent_width, IndentLine()),
                False,
            ) + 
            []
        ),
        case_Set = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'Set',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_comma_exprs(o.contents, depth + 1, "contents", 
                pro.next_indent_width(indent_width, IndentLine()),
                False,
            ) + 
            []
        ),
        case_ListComp = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'ListComp',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, IndentLine()),
                False,
            ) + 
            serialize_comprehension_constraints(o.constraints, depth + 1, "constraints", 
                pro.next_indent_width(indent_width, IndentLine()),
                False,
            ) + 
            []
        ),
        case_SetComp = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'SetComp',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, IndentLine()),
                False,
            ) + 
            serialize_comprehension_constraints(o.constraints, depth + 1, "constraints", 
                pro.next_indent_width(indent_width, IndentLine()),
                False,
            ) + 
            []
        ),
        case_DictionaryComp = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'DictionaryComp',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.key, depth + 1, "key", 
                pro.next_indent_width(indent_width, IndentLine()),
                False,
            ) + 
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_comprehension_constraints(o.constraints, depth + 1, "constraints", 
                pro.next_indent_width(indent_width, IndentLine()),
                False,
            ) + 
            []
        ),
        case_GeneratorExp = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'GeneratorExp',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, IndentLine()),
                False,
            ) + 
            serialize_comprehension_constraints(o.constraints, depth + 1, "constraints", 
                pro.next_indent_width(indent_width, IndentLine()),
                False,
            ) + 
            []
        ),
        case_Await = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'Await',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_YieldNothing = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'YieldNothing',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_Yield = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'Yield',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_YieldFrom = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'YieldFrom',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_Compare = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'Compare',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.left, depth + 1, "left", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_comparisons(o.comps, depth + 1, "comps", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_Call = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'Call',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.func, depth + 1, "func", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_CallArgs = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'CallArgs',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.func, depth + 1, "func", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_arguments(o.args, depth + 1, "args", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_Integer = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'Integer',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            [pro.make_Symbol(o.content, depth + 1, "content")] +
            []
        ),
        case_Float = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'Float',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            [pro.make_Symbol(o.content, depth + 1, "content")] +
            []
        ),
        case_ConcatString = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'ConcatString',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_sequence_str(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_True_ = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'True_',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_False_ = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'False_',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_None_ = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'None_',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_Ellip = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'Ellip',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_Attribute = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'Attribute',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_Identifier(o.attr, depth + 1, "attr", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_Subscript = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'Subscript',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_expr(o.slice, depth + 1, "slice", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_Starred = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'Starred',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.content, depth + 1, "content", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_Name = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'Name',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_Identifier(o.id, depth + 1, "id", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_List = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'List',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_comma_exprs(o.contents, depth + 1, "contents", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_Tuple = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'Tuple',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_comma_exprs(o.contents, depth + 1, "contents", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        ),
        case_Slice = lambda o : (
            [pro.make_Node(
                lhs = 'expr',
                rhs = 'Slice',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_option_expr(o.lower, depth + 1, "lower", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_option_expr(o.upper, depth + 1, "upper", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_option_expr(o.step, depth + 1, "step", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            []
        )
    ))


def serialize_boolop(
    o : boolop, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_boolop(o, BoolopHandlers[list[production]](
        case_And = lambda o : (
            [pro.make_Node(
                lhs = 'boolop',
                rhs = 'And',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_Or = lambda o : (
            [pro.make_Node(
                lhs = 'boolop',
                rhs = 'Or',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        )
    ))


def serialize_operator(
    o : operator, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_operator(o, OperatorHandlers[list[production]](
        case_Add = lambda o : (
            [pro.make_Node(
                lhs = 'operator',
                rhs = 'Add',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_Sub = lambda o : (
            [pro.make_Node(
                lhs = 'operator',
                rhs = 'Sub',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_Mult = lambda o : (
            [pro.make_Node(
                lhs = 'operator',
                rhs = 'Mult',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_MatMult = lambda o : (
            [pro.make_Node(
                lhs = 'operator',
                rhs = 'MatMult',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_Div = lambda o : (
            [pro.make_Node(
                lhs = 'operator',
                rhs = 'Div',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_Mod = lambda o : (
            [pro.make_Node(
                lhs = 'operator',
                rhs = 'Mod',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_Pow = lambda o : (
            [pro.make_Node(
                lhs = 'operator',
                rhs = 'Pow',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_LShift = lambda o : (
            [pro.make_Node(
                lhs = 'operator',
                rhs = 'LShift',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_RShift = lambda o : (
            [pro.make_Node(
                lhs = 'operator',
                rhs = 'RShift',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_BitOr = lambda o : (
            [pro.make_Node(
                lhs = 'operator',
                rhs = 'BitOr',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_BitXor = lambda o : (
            [pro.make_Node(
                lhs = 'operator',
                rhs = 'BitXor',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_BitAnd = lambda o : (
            [pro.make_Node(
                lhs = 'operator',
                rhs = 'BitAnd',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_FloorDiv = lambda o : (
            [pro.make_Node(
                lhs = 'operator',
                rhs = 'FloorDiv',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        )
    ))


def serialize_unaryop(
    o : unaryop, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_unaryop(o, UnaryopHandlers[list[production]](
        case_Invert = lambda o : (
            [pro.make_Node(
                lhs = 'unaryop',
                rhs = 'Invert',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_Not = lambda o : (
            [pro.make_Node(
                lhs = 'unaryop',
                rhs = 'Not',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_UAdd = lambda o : (
            [pro.make_Node(
                lhs = 'unaryop',
                rhs = 'UAdd',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_USub = lambda o : (
            [pro.make_Node(
                lhs = 'unaryop',
                rhs = 'USub',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        )
    ))


def serialize_cmpop(
    o : cmpop, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_cmpop(o, CmpopHandlers[list[production]](
        case_Eq = lambda o : (
            [pro.make_Node(
                lhs = 'cmpop',
                rhs = 'Eq',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_NotEq = lambda o : (
            [pro.make_Node(
                lhs = 'cmpop',
                rhs = 'NotEq',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_Lt = lambda o : (
            [pro.make_Node(
                lhs = 'cmpop',
                rhs = 'Lt',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_LtE = lambda o : (
            [pro.make_Node(
                lhs = 'cmpop',
                rhs = 'LtE',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_Gt = lambda o : (
            [pro.make_Node(
                lhs = 'cmpop',
                rhs = 'Gt',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_GtE = lambda o : (
            [pro.make_Node(
                lhs = 'cmpop',
                rhs = 'GtE',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_Is = lambda o : (
            [pro.make_Node(
                lhs = 'cmpop',
                rhs = 'Is',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_IsNot = lambda o : (
            [pro.make_Node(
                lhs = 'cmpop',
                rhs = 'IsNot',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_In = lambda o : (
            [pro.make_Node(
                lhs = 'cmpop',
                rhs = 'In',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        ),
        case_NotIn = lambda o : (
            [pro.make_Node(
                lhs = 'cmpop',
                rhs = 'NotIn',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            []
        )
    ))


def serialize_constraint(
    o : constraint, depth : int = 0, alias : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[production]:
    return match_constraint(o, ConstraintHandlers[list[production]](
        case_AsyncConstraint = lambda o : (
            [pro.make_Node(
                lhs = 'constraint',
                rhs = 'AsyncConstraint',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.target, depth + 1, "target", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_expr(o.search_space, depth + 1, "search_space", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_constraint_filters(o.filts, depth + 1, "filts", 
                pro.next_indent_width(indent_width, NewLine()),
                False,
            ) + 
            []
        ),
        case_Constraint = lambda o : (
            [pro.make_Node(
                lhs = 'constraint',
                rhs = 'Constraint',
                depth = depth,
                alias = alias,
                indent_width = indent_width,
                inline = inline
            )] +
            serialize_expr(o.target, depth + 1, "target", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_expr(o.search_space, depth + 1, "search_space", 
                pro.next_indent_width(indent_width, InLine()),
                True,
            ) + 
            serialize_constraint_filters(o.filts, depth + 1, "filts", 
                pro.next_indent_width(indent_width, NewLine()),
                False,
            ) + 
            []
        )
    ))