from __future__ import annotations

from typing import Optional

from abc import ABC, abstractmethod

from production import Production
import production as pro

from utils import fail
import utils

from gen.python_ast import *


def serialize(module : Module, depth : int = 0) -> list[Production]:
    return (
        [
            Production(
                lhs = 'mod',
                rhs = 'Module',
                depth = depth 
            )
        ] +
        pro.map_list(serialize_stmt, module.body, depth + 1, alias = 'body')
    )


def serialize_operator(
    operator : operator, depth : int = 0, 
    alias : Optional[str] = None
) -> list[Production]:

    production = lambda rhs : (
        Production(
            lhs = 'operator',
            rhs = rhs, 
            depth = depth,
            alias = alias
        )
    )

    return match_operator(operator, OperatorHandlers[list[Production]](
        case_Add = lambda o : [production("Add")],
        case_Sub = lambda o : [production("Sub")],
        case_Mult = lambda o : [production("Mult")],
        case_MatMult = lambda o : [production("MatMult")],
        case_Div = lambda o : [production("Div")],
        case_Mod = lambda o : [production("Mod")],
        case_Pow = lambda o : [production("Pow")],
        case_LShift = lambda o : [production("LShift")],
        case_RShift = lambda o : [production("RShift")],
        case_BitOr = lambda o : [production("BitOr")],
        case_BitXor = lambda o : [production("BitXor")],
        case_BitAnd = lambda o : [production("BitAnd")],
        case_FloorDiv = lambda o : [production("FloorDiv")]
    ))

def serialize_unaryop(
    op : unaryop, depth : int = 0, 
    alias : Optional[str] = None
) -> list[Production]:

    production = lambda rhs : (
        Production(
            lhs = 'unaryop',
            rhs = rhs, 
            depth = depth,
            alias = alias
        )
    )

    return match_unaryop(op, UnaryopHandlers[list[Production]](
        case_Invert = lambda o : [production("Invert")],
        case_Not = lambda o : [production("Not")],
        case_UAdd = lambda o : [production("UAdd")],
        case_USub = lambda o : [production("USub")]
    ))

def serialize_boolop(
    operator : boolop, depth : int = 0, 
    alias : Optional[str] = None
) -> list[Production]:

    production = lambda rhs : (
        Production(
            lhs = 'boolop',
            rhs = rhs, 
            depth = depth,
            alias = alias
        )
    )

    return match_boolop(operator, BoolopHandlers[list[Production]](
        case_And = lambda o : [production("And")],
        case_Or = lambda o : [production("Or")],
    ))

def serialize_cmpop(
    operator : cmpop, depth : int = 0, 
    alias : Optional[str] = None
) -> list[Production]:

    production = lambda rhs : (
        Production(
            lhs = 'cmpop',
            rhs = rhs, 
            depth = depth,
            alias = alias
        )
    )

    return match_cmpop(operator, CmpopHandlers[list[Production]](
        case_Eq = lambda _ : [production("Eq")],
        case_NotEq = lambda _ : [production("NotEq")],
        case_Lt = lambda _ : [production("Lt")],
        case_LtE = lambda _ : [production("LtE")],
        case_Gt = lambda _ : [production("Gt")],
        case_GtE = lambda _ : [production("GtE")],
        case_Is = lambda _ : [production("Is")],
        case_IsNot = lambda _ : [production("IsNot")],
        case_In = lambda _ : [production("In")],
        case_NotIn = lambda _ : [production("NotIn")]
    ))



def serialize_expr(
    expr : expr, depth : int = 0, 
    alias : Optional[str] = None
) -> list[Production] :

    production = lambda rhs, symbol = None : (
        Production(
            lhs = 'expr',
            rhs = rhs,
            depth = depth,
            alias = alias,
            symbol = symbol
        )
    )

    return match_expr(expr, ExprHandlers(
        case_BoolOp = lambda o : (
            [production("BoolOp")] +
            serialize_expr(o.left, depth + 1, 'left') +
            serialize_boolop(o.op, depth + 1, 'op') +
            serialize_expr(o.right, depth + 1, 'right')
        ),
        case_NamedExpr = lambda o : (
            [production("NamedExpr")] +
            serialize_expr(o.target, depth + 1, 'target') +
            serialize_expr(o.value, depth + 1, 'value')
        ),
        case_BinOp = lambda o : (
            [production("BinOp")] +
            serialize_expr(o.left, depth + 1, 'left') +
            serialize_operator(o.op, depth + 1, 'op') +
            serialize_expr(o.right, depth + 1, 'right')
        ),
        case_UnaryOp = lambda o : (
            [production("UnaryOp")] +
            serialize_unaryop(o.op, depth + 1, 'op') +
            serialize_expr(o.operand, depth + 1, 'operand')
        ),
        case_Lambda = lambda o : (
            [production("Lambda")] +
            serialize_ParamGroup(o.param_group, depth + 1, 'args') +
            serialize_expr(o.body, depth + 1, 'body')
        ),
        case_IfExp = lambda o : (
            [production("IfExp")] +
            serialize_expr(o.test, depth + 1, 'test') +
            serialize_expr(o.body, depth + 1, 'body') +
            serialize_expr(o.orelse, depth + 1, 'orelse')
        ),
        case_Dict = lambda o : (
            [production("Dict")] +
            pro.map_list(serialize_Entry, o.entries, depth + 1, 'entries')
        ),
        case_Set = lambda o : (
            [production("Set")] +
            pro.map_list(serialize_expr, o.elts, depth + 1, 'elts')
        ),
        case_ListComp = lambda o : (
            [production("ListComp")] +
            serialize_expr(o.elt, depth + 1, 'elt') +
            pro.map_list(serialize_constraint, o.constraints, depth + 1, 'generators')
        ),
        case_SetComp = lambda o : (
            [production("SetComp")] +
            serialize_expr(o.elt, depth + 1, 'elt') +
            pro.map_list(serialize_constraint, o.constraints, depth + 1, 'generators')
        ),
        case_DictComp = lambda o : (
            [production("DictComp")] +
            serialize_expr(o.key, depth + 1, 'key') +
            serialize_expr(o.value, depth + 1, 'value') +
            pro.map_list(serialize_constraint, o.constraints, depth + 1, 'generators')
        ),
        case_GeneratorExp = lambda o : (
            [production("GeneratorExp")] +
            serialize_expr(o.elt, depth + 1, 'elt') +
            pro.map_list(serialize_constraint, o.constraints, depth + 1, 'generators')
        ),
        case_Await = lambda o : (
            [production("Await")] +
            serialize_expr(o.value, depth + 1, 'value')
        ),
        case_Yield = lambda o : (
            [production("Yield")] +
            pro.map_option(serialize_expr, o.value, depth + 1, 'value')
        ),
        case_YieldFrom = lambda o : (
            [production("YieldFrom")] +
            serialize_expr(o.value, depth + 1, 'value')
        ),
        case_Compare = lambda o : (
            [production("Compare")] +
            serialize_expr(o.left, depth + 1, 'left') +
            pro.map_list(serialize_cmpop, o.ops, depth + 1, 'ops') +
            pro.map_list(serialize_expr, o.comparators, depth + 1, 'comparators')
        ),
        case_Call = lambda o : (
            [production("Call")] +
            serialize_expr(o.func, depth + 1, 'func') +
            pro.map_list(serialize_expr, o.args, depth + 1, 'args') +
            pro.map_list(serialize_Keyword, o.keywords, depth + 1, 'keywords')
        ),

        case_Integer = lambda o : (
            [production("Integer", symbol = o.value)]
        ),

        case_Float = lambda o : (
            [production("Float", symbol = o.value)]
        ),

        case_String = lambda o : (
            [production("String", symbol = o.value)]
        ),

        case_True_ = lambda _ : (
            [production("True_")]
        ),

        case_False_ = lambda _ : (
            [production("False_")]
        ),

        case_None_ = lambda _ : (
            [production("None_")]
        ),

        case_Ellip = lambda _ : (
            [production("Ellip")]
        ),

        case_ConcatString = lambda o : (
            [production("ConcatString")] +
            [
                production("ConstantString", symbol = str)
                for str in o.values
            ]
        ),

        case_Attribute = lambda o : (
            [production("Attribute")] +
            serialize_expr(o.value, depth + 1, 'value') +
            serialize_Identifier(o.attr, depth + 1, 'attr')
        ),

        case_Subscript = lambda o : (
            [production("Subscript")] +
            serialize_expr(o.value, depth + 1, 'value') +
            serialize_expr(o.slice, depth + 1, 'slice')
        ),

        case_Starred = lambda o : (
            [production("Starred")] +
            serialize_expr(o.value, depth + 1, 'value')
        ),

        case_Name = lambda o : (
            [production("Name")] +
            serialize_Identifier(o.id, depth + 1, 'id')
        ),

        case_List = lambda o : (
            [production("List")] +
            pro.map_list(serialize_expr, o.elts, depth + 1, 'elts')
        ),

        case_Tuple = lambda o : (
            [production("Tuple")] +
            pro.map_list(serialize_expr, o.elts, depth + 1, 'elts')
        ),

        case_Slice = lambda o : (
            [production("Slice")] +
            pro.map_option(serialize_expr, o.lower, depth + 1, 'lower') +
            pro.map_option(serialize_expr, o.upper, depth + 1, 'upper') +
            pro.map_option(serialize_expr, o.step, depth + 1, 'step')
        )
    ))


def serialize_constraint(
    o : constraint, depth : int = 0, 
    alias : Optional[str] = None
) -> list[Production]:
    production = lambda rhs : (
        Production(
            lhs = 'constraint',
            rhs = rhs,
            depth = depth,
            alias = alias
        )
    )

    return match_constraint(o, ConstraintHandlers(
        case_Constraint = lambda o : (
            [production("Constraint")] +
            serialize_expr(o.target, depth + 1, 'target') + 
            serialize_expr(o.iter, depth + 1, 'iter') + 
            pro.map_list(serialize_expr, o.ifs, depth + 1, 'ifs')
        ),

        case_AsyncConstraint = lambda o : (
            [production("AsyncConstraint")] +
            serialize_expr(o.target, depth + 1, 'target') + 
            serialize_expr(o.iter, depth + 1, 'iter') + 
            pro.map_list(serialize_expr, o.ifs, depth + 1, 'ifs')
        )

    ))
        

def serialize_Alias(
    o : Alias, depth : int = 0, 
    alias : Optional[str] = None
) -> list[Production]:
    return (
        [Production(
            lhs = 'alias',
            rhs = 'Alias',
            depth = depth,
            alias = alias
        )] + 
        serialize_Identifier(o.name, depth + 1, 'name') + 
        pro.map_option(serialize_Identifier, o.asname, depth + 1, 'asname')
    )

def serialize_Identifier(
    id : Identifier, depth : int = 0, 
    alias : Optional[str] = None
) -> list[Production]:
    return [Production(
        lhs = 'id',
        rhs = 'Identifier',
        depth = depth,
        alias = alias,
        symbol = id.symbol
    )]

def serialize_Param(
    param : Param, depth : int = 0, 
    alias : Optional[str] = None
) -> list[Production]:

    return (
        [Production(
            lhs = 'param',
            rhs = 'Param',
            depth = depth,
            alias = alias
        )]  +
        serialize_Identifier(param.id, depth + 1, alias = 'id') +
        pro.map_option(serialize_expr, param.annotation, depth + 1, alias = 'annotation') +
        pro.map_option(serialize_expr, param.default, depth + 1, alias = 'default')
    )

def serialize_ParamGroup(
    param_group : ParamGroup, depth : int = 0, 
    alias : Optional[str] = None
) -> list[Production]:
    return (
        [Production(
            lhs = 'param_group',
            rhs = 'ParamGroup',
            depth = depth,
            alias = alias
        )]  +
        pro.map_list(serialize_Param, param_group.pos_params, depth + 1, alias = 'pos_params') +
        pro.map_list(serialize_Param, param_group.params, depth + 1, alias = 'params') +
        pro.map_option(serialize_Param, param_group.list_splat, depth + 1, alias = 'list_splat') +
        pro.map_list(serialize_Param, param_group.kw_params, depth + 1, alias = 'kw_params') +
        pro.map_option(serialize_Param, param_group.dictionary_splat, depth + 1, alias = 'dictionary_splat')

    )


def serialize_Entry(
    o : Entry, depth : int = 0, 
    alias : Optional[str] = None
) -> list[Production]:
    return (
        [Production(
            lhs = 'entry',
            rhs = 'Entry',
            depth = depth,
            alias = alias
        )] +
        serialize_expr(o.key, depth + 1, 'key') +
        serialize_expr(o.value, depth + 1, 'value')
    )

def serialize_Keyword(
    kw : Keyword, depth : int = 0, 
    alias : Optional[str] = None
) -> list[Production]:
    return (
        [Production(
            lhs = 'keyword',
            rhs = 'Keyword',
            depth = depth,
            alias = alias
        )] +
        pro.map_option(serialize_Identifier, kw.name, depth + 1, 'arg') +
        serialize_expr(kw.value, depth + 1, 'value')
    )


def serialize_Withitem(
    wi : Withitem, depth : int = 0, 
    alias : Optional[str] = None
) -> list[Production]:
    return (
        [Production(
            lhs = 'withitem',
            rhs = 'Withitem',
            depth = depth,
            alias = alias
        )] +
        serialize_expr(wi.context_expr, depth + 1, 'context_expr') +
        pro.map_option(serialize_expr, wi.optional_vars, depth + 1, 'optional_vars')
    )



def serialize_ExceptHandler(
    eh : ExceptHandler, depth : int = 0, 
    alias : Optional[str] = None
) -> list[Production]:
    return (
        [Production(
            lhs = 'except_handler',
            rhs = 'ExceptHandler',
            depth = depth,
            alias = alias
        )] +
        pro.map_option(serialize_expr, eh.type, depth + 1, 'type') +
        pro.map_option(serialize_Identifier, eh.name, depth + 1, 'name') +
        pro.map_list(serialize_stmt, eh.body, depth + 1, alias = 'body')
    )

def serialize_stmt(
    stmt : stmt, depth : int = 0, 
    alias : Optional[str] = None
) -> list :

    production = lambda rhs = None : (
        Production(
            lhs = "stmt",
            rhs = rhs, 
            depth = depth,
            alias = alias
        )
    )

    return match_stmt(stmt, StmtHandlers[list](

        case_FunctionDef = lambda o : (
            [production("FunctionDef")] + 
            serialize_Identifier(o.name, depth + 1, 'name')  + 
            serialize_ParamGroup(o.param_group, depth + 1, 'args') +
            pro.map_list(serialize_stmt, o.body, depth + 1, 'body') +
            pro.map_list(serialize_expr, o.decorator_list, depth + 1, 'decorator_list') +
            pro.map_option(serialize_expr, o.returns, depth + 1, 'returns')
        ),

        case_AsyncFunctionDef = lambda o : (
            [production("AsyncFunctionDef")] +
            serialize_Identifier(o.name, depth + 1, 'name')  + 
            serialize_ParamGroup(o.param_group, depth + 1, 'args') +
            pro.map_list(serialize_stmt, o.body, depth + 1, 'body') +
            pro.map_list(serialize_expr, o.decorator_list, depth + 1, 'decorator_list') +
            pro.map_option(serialize_expr, o.returns, depth + 1, 'returns')
        ),

        case_ClassDef = lambda o : (
            [production("ClassDef")] +
            serialize_Identifier(o.name, depth + 1, 'name')  + 
            pro.map_list(serialize_expr, o.bases, depth + 1, 'bases') +
            pro.map_list(serialize_Keyword, o.keywords, depth + 1, 'keywords') +
            pro.map_list(serialize_stmt, o.body, depth + 1, 'body') +
            pro.map_list(serialize_expr, o.decorator_list, depth + 1, 'decorator_list')
        ),

        case_Return = lambda o : (
            [production("Return")] +
            pro.map_option(serialize_expr, o.value, depth + 1, 'value')
        ),

        case_Delete = lambda o : (
            [production("Delete")] +
            pro.map_list(serialize_expr, o.targets, depth + 1, 'targets')
        ),


        case_Assign = lambda o : (
            [production("Assign")] +
            pro.map_list(serialize_expr, o.targets, depth + 1, 'targets') +
            serialize_expr(o.value, depth + 1, 'value')
        ),

        case_AugAssign = lambda o : (
            [production("AugAssign")] +
            serialize_expr(o.target, depth + 1, 'target') +
            serialize_operator(o.op, depth + 1, 'op') +
            serialize_expr(o.value, depth + 1, 'value')
        ),

        case_AnnAssign = lambda o : (
            [production("AnnAssign")] +
            serialize_expr(o.target, depth + 1, 'target') +
            serialize_expr(o.annotation, depth + 1, 'annotation') +
            pro.map_option(serialize_expr, o.value, depth + 1, 'value')
        ),

        case_AnnAssignSimple = lambda o : (
            [production("AnnAssignSimple")] +
            serialize_expr(o.target, depth + 1, 'target') +
            serialize_expr(o.annotation, depth + 1, 'annotation') +
            pro.map_option(serialize_expr, o.value, depth + 1, 'value')
        ),

        case_For = lambda o : (
            [production("For")] +
            serialize_expr(o.target, depth + 1, 'target') +
            serialize_expr(o.iter, depth + 1, 'iter') +
            pro.map_list(serialize_stmt, o.body, depth + 1, 'body') +
            pro.map_list(serialize_stmt, o.orelse, depth + 1, 'orelse')
        ),

        case_AsyncFor = lambda o : (
            [production("AsyncFor")] +
            serialize_expr(o.target, depth + 1, 'target') +
            serialize_expr(o.iter, depth + 1, 'iter') +
            pro.map_list(serialize_stmt, o.body, depth + 1, 'body') +
            pro.map_list(serialize_stmt, o.orelse, depth + 1, 'orelse')
        ),

        case_While = lambda o : (
            [production("While")] +
            serialize_expr(o.test, depth + 1, 'test') +
            pro.map_list(serialize_stmt, o.body, depth + 1, 'body') +
            pro.map_list(serialize_stmt, o.orelse, depth + 1, 'orelse')
        ),

        case_If = lambda o : (
            [production("If")] +
            serialize_expr(o.test, depth + 1, 'test') +
            pro.map_list(serialize_stmt, o.body, depth + 1, 'body') +
            pro.map_list(serialize_stmt, o.orelse, depth + 1, 'orelse')
        ),

        case_With = lambda o : (
            [production("With")] +
            pro.map_list(serialize_Withitem, o.items, depth + 1, 'items') +
            pro.map_list(serialize_stmt, o.body, depth + 1, 'body')
        ),

        case_AsyncWith = lambda o : (
            [production("AsyncWith")] +
            pro.map_list(serialize_Withitem, o.items, depth + 1, 'items') +
            pro.map_list(serialize_stmt, o.body, depth + 1, 'body')
        ),

        case_Raise = lambda o : (
            [production("Raise")] +
            pro.map_option(serialize_expr, o.exc, depth + 1, 'exc') +
            pro.map_option(serialize_expr, o.cause, depth + 1, 'cause')
        ),

        case_Try = lambda o : (
            [production("Try")] +
            pro.map_list(serialize_stmt, o.body, depth + 1, 'body') +
            pro.map_list(serialize_ExceptHandler, o.handlers, depth + 1, 'handlers') +
            pro.map_list(serialize_stmt, o.orelse, depth + 1, 'orelse') +
            pro.map_list(serialize_stmt, o.finalbody, depth + 1, 'finalbody')
        ),

        case_Assert = lambda o : (
            [production("Assert")] +
            serialize_expr(o.test, depth + 1, 'test') +
            pro.map_option(serialize_expr, o.msg, depth + 1, 'msg')
        ),

        case_Import = lambda o : (
            [production("Import")] +
            pro.map_list(serialize_Alias, o.names, depth + 1, 'names')
        ),

        case_ImportFrom = lambda o : (
            [production("ImportFrom")] +
            pro.map_option(serialize_Identifier, o.module, depth + 1, 'module') +
            pro.map_list(serialize_Alias, o.names, depth + 1, 'names')
        ),

        case_Global = lambda o : (
            [production("Global")] +
            pro.map_list(serialize_Identifier, o.names, depth + 1, 'names')
        ),

        case_Nonlocal = lambda o : (
            [production("Nonlocal")] +
            pro.map_list(serialize_Identifier, o.names, depth + 1, 'names')
        ),

        case_Expr = lambda o : (
            [production("Expr")] +
            serialize_expr(o.value, depth + 1, 'value')
        ),

        case_Pass = lambda _ : (
            [production("Pass")]
        ),

        case_Break = lambda _ : (
            [production("Break")]
        ),

        case_Continue = lambda _ : (
            [production("Continue")]
        )

    ))