from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from collections.abc import Callable

from abc import ABC, abstractmethod


from lib.generic_tree import GenericNode
from gen.python_ast import *

from lib.utils import fail
from lib import utils



def unsupported(node : GenericNode):
    fail(f"unsupported syntax for {node.syntax_part}")


def to_bases(bases : list[expr], keywords : list[keyword]) -> bases:
    if not bases and not keywords:
        return NoBases()
    else:
        return SomeBases(to_sequence_base(bases, keywords))


def to_sequence_base(bases : list[expr], keywords : list[keyword]):

    assert bases or keywords

    (result, bases) = (

        (KeywordsBase(to_keywords(keywords)), bases)
        if keywords else

        (SingleBase(bases[-1]), bases[:-1])

    )

    for b in reversed(bases):
        result = ConsBase(b, result)

    return result



def to_parameters(
    pos_params : list[Param], 
    params : list[Param], 
    list_splat_param : Optional[Param], 
    kw_params : list[Param], 
    dictionary_splat_param : Optional[Param]
) -> parameters:

    if not (
        pos_params or params or list_splat_param or kw_params or dictionary_splat_param
    ):
        return NoParam()
    elif pos_params:
        return ParamsA(to_parameters_a(
            pos_params, params, list_splat_param, kw_params, dictionary_splat_param
        ))
    else:
        return ParamsB(to_parameters_b(
            params, list_splat_param, kw_params, dictionary_splat_param
        ))


def to_parameters_d(
    kw_params : list[Param], 
    dictionary_splat_param : Optional[Param]
) -> parameters_d:
    assert kw_params or dictionary_splat_param
    (result, kw_params) = (
        (DictionarySplatParam(dictionary_splat_param), kw_params)
        if dictionary_splat_param else

        (SingleKwParam(kw_params[-1]), kw_params[:-1])
    )

    for p in reversed(kw_params):
        result = ConsKwParam(p, result)

    return result


def to_parameters_c(
    list_splat_param : Optional[Param], 
    kw_params : list[Param], 
    dictionary_splat_param : Optional[Param]
) -> parameters_c:
    if (list_splat_param and (kw_params or dictionary_splat_param)):
        return TransListSplatParam(list_splat_param, 
            to_parameters_d(kw_params, dictionary_splat_param)
        )
    elif (list_splat_param and not (kw_params or dictionary_splat_param)):
        return SingleListSplatParam(list_splat_param)
    else:
        return ParamsD(to_parameters_d(kw_params, dictionary_splat_param))


def to_parameters_b(
    params : list[Param], 
    list_splat_param : Optional[Param], 
    kw_params : list[Param], 
    dictionary_splat_param : Optional[Param]
) -> parameters_b:

    (result, params) = (
        (
            ParamsC( 
                to_parameters_c(list_splat_param, kw_params, dictionary_splat_param)
            ), 
            params
        )
        if (list_splat_param or kw_params or dictionary_splat_param) else

        (SingleParam(params[-1]), params[:-1])
    )

    for p in reversed(params):
        result = ConsParam(p, result)

    return result


def to_parameters_a(
    pos_params : list[Param], 
    params : list[Param], 
    list_splat_param : Optional[Param], 
    kw_params : list[Param], 
    dictionary_splat_param : Optional[Param]
) -> parameters_a:
    assert pos_params

    result = (

        TransPosParam(pos_params[-1], 
            to_parameters_b(params, list_splat_param, kw_params, dictionary_splat_param)
        )
        if (params or list_splat_param or kw_params or dictionary_splat_param) else

        SinglePosParam(pos_params[-1])
    )

    for pp in reversed(pos_params):
        result = ConsPosParam(pp, result)

    return result



def to_comparisons(crs : list[CompareRight]) -> comparisons:
    assert crs 

    result = SingleCompareRight(crs[-1])
    for cr in reversed(crs[:-1]):
        result = ConsCompareRight(cr, result)

    return result

def to_dictionary_contents(items : list[dictionary_item]) -> dictionary_contents:
    assert items 

    result = SingleDictionaryItem(items[-1])
    for f in reversed(items[:-1]):
        result = ConsDictionaryItem(f, result)

    return result

def to_comprehension_constraints(cs : list[constraint]) -> comprehension_constraints:
    assert cs 

    result = SingleConstraint(cs[-1])
    for c in reversed(cs[:-1]):
        result = ConsConstraint(c, result)

    return result

def to_statements(stmts : list[stmt]) -> statements:
    assert stmts

    result = SingleStmt(stmts[-1])
    for stmt in reversed(stmts[:-1]):
        result = ConsStmt(stmt, result)

    return result

def to_sequence_ImportName(ns : list[ImportName]) -> sequence_ImportName:
    assert ns 

    result = SingleImportName(ns[-1])
    for n in reversed(ns[:-1]):
        result = ConsImportName(n, result)

    return result

def to_sequence_var(ids : list[str]) -> sequence_var:
    assert ids 

    result = SingleId(ids[-1])
    for id in reversed(ids[:-1]):
        result = ConsId(id, result)

    return result

def to_sequence_ExceptHandler(es : list[ExceptHandler]) -> sequence_ExceptHandler:
    assert es 

    result = SingleExceptHandler(es[-1])
    for e in reversed(es[:-1]):
        result = ConsExceptHandler(e, result)

    return result


def to_sequence_Withitem(ws : list[Withitem]) -> sequence_Withitem:
    assert ws 

    result = SingleWithitem(ws[-1])
    for w in reversed(ws[:-1]):
        result = ConsWithitem(w, result)

    return result


def to_decorators(ds : list[expr]) -> decorators:

    result = NoDec()
    for d in reversed(ds):
        result = ConsDec(d, result)

    return result 


def to_comma_exprs(es : list[expr]) -> comma_exprs:
    assert es 

    result = SingleExpr(es[-1])
    for e in reversed(es[:-1]):
        result = ConsExpr(e, result)

    return result

def to_target_exprs(es : list[expr]) -> target_exprs:
    assert es 

    result = SingleTargetExpr(es[-1])
    for e in reversed(es[:-1]):
        result = ConsTargetExpr(e, result)

    return result

def to_constraint_filters(es : list[expr]) -> constraint_filters:


    (result, es) = (
        (SingleFilter(es[-1]), es[:-1])
        if es else

        (NoFilter(), es) 
    )
    for e in reversed(es):
        result = ConsFilter(e, result)

    return result

def to_sequence_string(ss : list[str]) -> sequence_string:
    assert ss  

    result = SingleStr(ss[-1])
    for s in reversed(ss[:-1]):
        result = ConsStr(s, result)

    return result

def to_keywords(ks : list[keyword]) -> keywords:
    assert ks  

    result = SingleKeyword(ks[-1])
    for k in reversed(ks[:-1]):
        result = ConsKeyword(k, result)

    return result

def to_arguments(ps : list[expr], ks : list[keyword]) -> arguments:

    (result, ps) = (
        (KeywordsArg(to_keywords(ks)), ps)
        if ks else

        (SingleArg(ps[-1]), ps[:-1])
    )

    for p in reversed(ps):
        result = ConsArg(p, result)

    return result

def from_generic_ast(node : GenericNode) -> Module: 
    children = node.children
    if (node.syntax_part == "module"):
        statements = [
            stmt
            for stmt_node in children  
            for stmt in from_generic_ast_to_stmts(stmt_node)
        ]
        return Module(to_statements(statements))
    else:
       unsupported(node) 



def from_generic_ast_to_identifier(node : GenericNode) -> str:
    if (node.syntax_part == "dotted_name"):
        children = node.children
        dotted_name = "".join([
            id.text
            for id in children
        ])
        return dotted_name
    elif (node.syntax_part == "identifier"):
        return node.text
    else:
       unsupported(node) 


def from_generic_ast_to_ImportName(node : GenericNode, alias : Optional[str] = None) -> ImportName:
    
    if (node.syntax_part == "dotted_name"):
        dotted_name = ".".join([
            child.text
            for child in node.children
            if child.syntax_part == "identifier"
        ])
        return ImportName(
            (dotted_name),
            (
                SomeAlias((alias)) 
                if alias else 
                NoAlias()
            )
        )
    elif (node.syntax_part == "identifier"):
        text = node.text
        return ImportName(
            (text),
            (
                SomeAlias((alias)) 
                if alias else 
                NoAlias()
            )
        )
    elif (node.syntax_part == "aliased_import"):
        children = node.children
        name_node = children[0]
        assert children[1].syntax_part == "as"
        asname_node = children[2]
        asname_text = asname_node.text
        return from_generic_ast_to_ImportName(name_node, asname_text)
    else:
        unsupported(node)

def from_generic_ast_to_unaryop(node):
    if (node.syntax_part == "~"):
       return Invert() 
    elif (node.syntax_part == "+"):
       return UAdd() 
    elif (node.syntax_part == "-"):
       return USub() 
    else:
        unsupported(node)

def from_generic_ast_to_boolop(node):
    if node.syntax_part == "and":
       return And() 
    elif node.syntax_part == "or":
       return Or() 
    else:
        unsupported(node)

def from_generic_ast_to_operator(node : GenericNode) -> operator: 

    if node.syntax_part in {"+=", "+"}:
       return Add() 

    elif node.syntax_part in {"-=", "-"}:
        return Sub()

    elif node.syntax_part in {"*=", "*"}:
        return Mult()

    elif node.syntax_part in {"/=", "/"}:
        return Div()

    elif node.syntax_part in {"@=", "@"}:
        return MatMult()

    elif node.syntax_part in {"//=", "//"}:
        return FloorDiv()

    elif node.syntax_part in {"%=", "%"}:
        return Mod()

    elif node.syntax_part in {"**=", "**"}:
        return Pow()

    elif node.syntax_part in {">>=", ">>"}:
        return RShift()

    elif node.syntax_part in {"<<=", "<<"}:
        return LShift()

    elif node.syntax_part in {"&=", "&"}:
        return BitAnd()

    elif node.syntax_part in {"^=", "^"}:
        return BitXor()

    elif node.syntax_part in {"|=", "|"}:
        return BitOr()

    else:
        unsupported(node)


def split_ops_and_rands(
    nodes : list[GenericNode], 
    ops : list[cmpop] = [], 
    rands : list[expr] = []
) -> tuple[list[cmpop], list[expr]]:

    if len(nodes) == 0:
        return (ops, rands)
    else:
        head = nodes[-1]
        if head.syntax_part == '<':
            return split_ops_and_rands(nodes[:-1], ops + [Lt()], rands)
        if head.syntax_part == '<=':
            return split_ops_and_rands(nodes[:-1], ops + [LtE()], rands)
        if head.syntax_part == '==':
            return split_ops_and_rands(nodes[:-1], ops + [Eq()], rands)
        if head.syntax_part == '!=':
            return split_ops_and_rands(nodes[:-1], ops + [NotEq()], rands)
        if head.syntax_part == '>=':
            return split_ops_and_rands(nodes[:-1], ops + [GtE()], rands)
        if head.syntax_part == '>':
            return split_ops_and_rands(nodes[:-1], ops + [Gt()], rands)
        if head.syntax_part == '<>':
            return split_ops_and_rands(nodes[:-1], ops + [NotEq()], rands)
        if head.syntax_part == 'in':
            return split_ops_and_rands(nodes[:-1], ops + [In()], rands)
        if head.syntax_part == 'not':
            next_head = nodes[-2]
            if next_head.syntax_part == "in":
                return split_ops_and_rands(nodes[:-2], ops + [NotIn()], rands)
            else:
                return split_ops_and_rands(nodes[:-1], ops + [In()], rands)
        if head.syntax_part == 'is':
            next_head = nodes[-2]
            if next_head.syntax_part == "not":
                return split_ops_and_rands(nodes[:-2], ops + [Is()], rands)
            else:
                return split_ops_and_rands(nodes[:-1], ops + [IsNot()], rands)

        else:
            rand = from_generic_ast_to_expr(head)
            tail = nodes[:-1]
            return split_ops_and_rands(tail, ops, rands + [rand])


def from_generic_ast_to_ExceptHandler(node) -> ExceptHandler:
    assert node.syntax_part == "except_clause"
    children = node.children
    assert children[0].syntax_part == "except"
    (expr_node, name_node, block_node) = (

        (None, None, children[2])
        if children[1].syntax_part == ":" else 
        
        (children[1], None, children[3])
        if children[2].syntax_part == ":" else 
        
        (children[1], children[3], children[5]) if (
            children[2].syntax_part == "as" and 
            children[4].syntax_part == ":" 
        ) else 
        
        (None, None, None)
    )

    assert block_node

    expr = utils.map_option(from_generic_ast_to_expr, expr_node)
    name = utils.map_option(from_generic_ast_to_identifier, name_node)
    stmts = [
        stmt
        for stmt_node in block_node.children
        for stmt in from_generic_ast_to_stmts(stmt_node)
    ]

    arg  = (
        SomeExceptArgName(expr, name)
        if expr and name else

        SomeExceptArg(expr)
        if expr else

        NoExceptArg()
    )

    return  ExceptHandler(arg, to_statements(stmts))


def from_generic_ast_to_Withitem(node) -> Withitem:
    assert node.syntax_part == "with_item"
    children = node.children
    context_node = children[0]
    pattern_node = (
        children[2]
        if (len(children) == 3 and children[1].syntax_part == "as") 
        
        else None
    )

    context_expr = from_generic_ast_to_expr(context_node)
    pattern_expr = utils.map_option(from_generic_ast_to_expr, pattern_node)

    target = (
        SomeAliasExpr(pattern_expr)
        if pattern_expr else

        NoAliasExpr()
    )
    return Withitem(context_expr, target)


def from_nodes_to_constraint(nodes : list[GenericNode]) -> constraint:

    for_node = nodes[0]
    assert for_node.syntax_part == "for_in_clause"

    (is_async, for_children) = (
        (True, for_node.children[1:])
        if for_node.children[0].syntax_part == "async"

        else (False, for_node.children)
    )

    assert for_children[0].syntax_part == "for"
    assert for_children[2].syntax_part == "in"


    target_expr = from_generic_ast_to_expr(for_children[1])
    iter_expr = from_generic_ast_to_expr(for_children[3])

    def assert_if_node(n):
        assert n.syntax_part == "if_clause"
        assert n.children[0].syntax_part == "if"




    if_nodes = nodes[1:]
    if_exprs = [
        from_generic_ast_to_expr(n.children[1])
        for n in if_nodes
        for _ in [assert_if_node(n)]
    ]



    if is_async:
        return AsyncConstraint(target_expr, iter_expr, to_constraint_filters(if_exprs))
    else:
        return Constraint(target_expr, iter_expr, to_constraint_filters(if_exprs))


def collapse_constraint_nodes(nodes : list[GenericNode]) -> list[constraint]:

    def collapse_constraint_nodes_r(
        nodes : list[GenericNode], 
        collected_group : list[GenericNode] = [], 
        collected_constraints : list[constraint] = []
    ) -> list[constraint]:

        if len(nodes) == 0:
            if len(collected_group) == 0:
                return collected_constraints 
            else:
                return collected_constraints + [from_nodes_to_constraint(collected_group)]
        else:
            node = nodes[-1]
            tail = nodes[0:-1]
            if node.syntax_part == "for_in_clause":
                if len(collected_group) == 0:
                    return collapse_constraint_nodes_r(tail, [node], collected_constraints)
                else:
                    constraint = from_nodes_to_constraint(collected_group)
                    return collapse_constraint_nodes_r(
                        tail, 
                        [node], 
                        collected_constraints + [constraint]
                    )

            if node.syntax_part == "if_clause":
                return collapse_constraint_nodes_r(
                    tail, 
                    collected_group + [node], 
                    collected_constraints
                )
            else:
                unsupported(node)

    return collapse_constraint_nodes_r([n for n in reversed(nodes)])


def from_generic_ast_to_expr(node : GenericNode) -> expr: 

    if node.syntax_part == "binary_operator" :
        children = node.children
        left_node = children[0]
        op_node = children[1]
        right_node = children[2]

        left_expr = from_generic_ast_to_expr(left_node)
        op = from_generic_ast_to_operator(op_node)
        right_expr = from_generic_ast_to_expr(right_node)

        return BinOp(left_expr, op, right_expr)

    elif node.syntax_part == "identifier":
        return Name(from_generic_ast_to_identifier(node))

    elif (node.syntax_part == "string"):
        return ConcatString(SingleStr(node.text))

    elif node.syntax_part == "concatenated_string":
        children = node.children
        str_values = [
            n.text
            for n in children
        ]

        return ConcatString(to_sequence_string(str_values))

    elif (node.syntax_part == "integer"):
        return Integer(node.text)

    elif (node.syntax_part == "float"):
        return Float(node.text)

    elif (node.syntax_part == "true"):
        return True_()

    elif (node.syntax_part == "false"):
        return False_()

    elif (node.syntax_part == "none"):
        return None_()

    elif (node.syntax_part == "unary_operator"):
        children = node.children
        op_node = children[0]
        rand_node = children[1]
        op = from_generic_ast_to_unaryop(op_node)
        rand = from_generic_ast_to_expr(rand_node)
        return UnaryOp(op, rand)
    
    elif (node.syntax_part == "attribute"):
        children = node.children
        expr_node = children[0]
        expr = from_generic_ast_to_expr(expr_node)
        assert children[1].syntax_part == "."
        id_node = children[2]
        id = from_generic_ast_to_identifier(id_node)
        return Attribute(expr, id)

    elif (node.syntax_part == "subscript"):
        children = node.children
        target_node = children[0]
        target = from_generic_ast_to_expr(target_node)
        assert children[1].syntax_part == "["
        assert children[-1].syntax_part == "]"
        if len(children[2:-1]) > 1:
            exprs = to_comma_exprs([
                from_generic_ast_to_expr(n)
                for n in children[2:-1]
                if n.syntax_part != ","
            ])
            slice = Tuple(exprs)
            return Subscript(target, slice)

        else:
            slice_node = children[2]
            slice = from_generic_ast_to_expr(slice_node)
            return Subscript(target, slice)

    elif (node.syntax_part == "call"):
        children = node.children
        func_node = children[0]
        func = from_generic_ast_to_expr(func_node)

        args_node = children[1]
        if args_node.syntax_part == "argument_list":
            argument_nodes = [
                child
                for child in args_node.children[1:-1]
                if child.syntax_part != ","
            ]

            pos_nodes = [n for n in argument_nodes if n.syntax_part != "keyword_argument" and n.syntax_part != "dictionary_splat"]
            kw_nodes = [n for n in argument_nodes if n.syntax_part == "keyword_argument" or n.syntax_part == "dictionary_splat"]

            pos_args = [
                from_generic_ast_to_expr(n)
                for n in pos_nodes
            ]

            keywords = [
                from_generic_ast_to_keyword(n)
                for n in kw_nodes
            ]

            if pos_args or keywords: 
                seq_arg = to_arguments(pos_args, keywords)
                return CallArgs(func, seq_arg)
            else:
                return Call(func)

        elif args_node.syntax_part == "generator_expression":
            return CallArgs(func, to_arguments([from_generic_ast_to_expr(args_node)], []))

        else:
            unsupported(args_node)

    elif (node.syntax_part == "list"):
        items = [
            from_generic_ast_to_expr(child)
            for child in node.children[1:-1]
            if child.syntax_part != ","
        ]
        if items:
            return List(to_comma_exprs(items))
        else:
            return EmptyList()

    elif (node.syntax_part == "list_comprehension"):
        children = node.children[1:-1]
        expr = from_generic_ast_to_expr(children[0])

        constraint_nodes = children[1:]

        constraints = collapse_constraint_nodes(constraint_nodes)

        return ListComp(expr, to_comprehension_constraints(constraints))

    elif (node.syntax_part == "dictionary"):
        children = [
            child
            for child in node.children[1:-1]
            if child.syntax_part != ","
        ]

        def is_pair(pair): 
            return pair.syntax_part == "pair" and pair.children[1].syntax_part == ":"

        def assert_splat(dsplat): 
            assert dsplat.syntax_part == "dictionary_splat" and dsplat.children[0].syntax_part == "**" 

        items = [
            (
                make_Field(
                    from_generic_ast_to_expr(child_node.children[0]), 
                    from_generic_ast_to_expr(child_node.children[2])
                )
                if is_pair(child_node) else

                (assert_splat(child_node), 
                make_DictionarySplatFields(from_generic_ast_to_expr(child_node.children[1])))[-1]

            )
            for child_node in children
        ]

        if items:
            return Dictionary(to_dictionary_contents(items))
        else:
            return EmptyDictionary()

    elif node.syntax_part == "dictionary_comprehension":
        children = node.children[1:-1]
        pair_node = children[0]
        assert pair_node.syntax_part == "pair"
        pair = pair_node.children
        key = from_generic_ast_to_expr(pair[0])
        assert pair[1].syntax_part == ":"
        value = from_generic_ast_to_expr(pair[2])

        constraint_nodes = children[1:]
        constraints = collapse_constraint_nodes(constraint_nodes)

        return DictionaryComp(key, value, to_comprehension_constraints(constraints))

    elif (node.syntax_part == "set"):
        
        items = [
            from_generic_ast_to_expr(n)
            for n in node.children[1:-1]
            if n.syntax_part != ","
        ]
        return Set(to_comma_exprs(items))

    elif (node.syntax_part == "set_comprehension"):
        children = node.children[1:-1]
        expr = from_generic_ast_to_expr(children[0])

        constraint_nodes = children[1:]
        constraints = collapse_constraint_nodes(constraint_nodes)
        return SetComp(expr, to_comprehension_constraints(constraints))


    elif (node.syntax_part == "generator_expression"):
        children = node.children[1:-1]
        expr = from_generic_ast_to_expr(children[0])

        constraint_nodes = children[1:]
        constraints = collapse_constraint_nodes(constraint_nodes)
        return GeneratorExp(expr, to_comprehension_constraints(constraints))

    elif (node.syntax_part == "tuple"):

        if (node.children[1:-1]):
            items = [
                from_generic_ast_to_expr(n)
                for n in node.children[1:-1]
                if n.syntax_part != ","
            ]
            return Tuple(to_comma_exprs(items))
        else:
            return EmptyTuple()

    elif (node.syntax_part == "expression_list"):
        items = [
            from_generic_ast_to_expr(n)
            for n in node.children
            if n.syntax_part != ","
        ]
        return Tuple(to_comma_exprs(items))

    
    elif (node.syntax_part == "parenthesized_expression"):
        expr_node = node.children[1:-1][0]
        return from_generic_ast_to_expr(expr_node)

    elif (node.syntax_part == "ellipsis"):
        return Ellip() 

    elif (node.syntax_part == "list_splat"):
        children = node.children
        assert children[0].syntax_part == "*"
        expr_node = children[1]
        expr = from_generic_ast_to_expr(expr_node)
        return Starred(expr)

    elif (node.syntax_part == "list_splat_pattern"):
        children = node.children
        assert children[0].syntax_part == "*"
        expr_node = children[1]
        expr = from_generic_ast_to_expr(expr_node)
        return Starred(expr)

    elif (node.syntax_part == "tuple_pattern"):
        items = [
            from_generic_ast_to_expr(n)
            for n in node.children[1:-1]
            if n.syntax_part != ","
        ]
        return Tuple(to_comma_exprs(items))

    elif (node.syntax_part == "list_pattern"):
        items = [
            from_generic_ast_to_expr(n)
            for n in node.children[1:-1]
            if n.syntax_part != ","
        ]
        return List(to_comma_exprs(items))

    elif (node.syntax_part == "pattern_list"):
        items = [
            from_generic_ast_to_expr(n)
            for n in node.children
            if n.syntax_part != ","
        ]
        return Tuple(to_comma_exprs(items))

    elif (node.syntax_part == "yield"):

        children = node.children

        assert children[0].syntax_part == "yield"
        is_yield_from = (
            len(children) > 1 and
            children[1].syntax_part == "from"
        )

        if is_yield_from:
            expr = from_generic_ast_to_expr(children[2])
            return YieldFrom(expr)
        else:
            expr = from_generic_ast_to_expr(children[1])
            return Yield(expr)

    elif node.syntax_part == "comparison_operator":
        left = from_generic_ast_to_expr(node.children[0])
        (ops, rands) = split_ops_and_rands([n for n in reversed(node.children[1:])])
        assert len(ops) == len(rands)
        comp_rights = [
            CompareRight(ops[i], rands[i])
            for i, _ in enumerate(ops)
        ]
        return Compare(left, to_comparisons(comp_rights))

    elif (node.syntax_part == "not_operator"):
        children = node.children
        assert children[0].syntax_part == "not"
        rand_node = children[1]
        op = Not() 
        rand = from_generic_ast_to_expr(rand_node)
        return UnaryOp(op, rand)

    elif node.syntax_part == "boolean_operator":
        children = node.children
        left_expr = from_generic_ast_to_expr(children[0])
        op = from_generic_ast_to_boolop(children[1])
        right_expr = from_generic_ast_to_expr(children[2])

        return BoolOp(left_expr, op, right_expr)
    elif node.syntax_part == "await":
        assert node.children[0].syntax_part == "await"
        expr = from_generic_ast_to_expr(node.children[1])
        return Await(expr)

    elif node.syntax_part == "lambda":
        assert node.children[0].syntax_part == "lambda"
        if len(node.children) == 3:
            params = NoParam()
            body = from_generic_ast_to_expr(node.children[2])
            return Lambda(params, body)
        else:
            params = from_generic_ast_to_parameters(node.children[1])
            assert node.children[2].syntax_part == ":"
            body = from_generic_ast_to_expr(node.children[3])
            return Lambda(params, body)

    elif node.syntax_part == "conditional_expression":
        children = node.children
        true_expr = from_generic_ast_to_expr(children[0])
        assert children[1].syntax_part == "if"
        cond_expr = from_generic_ast_to_expr(children[2])
        assert children[3].syntax_part == "else"
        false_expr = from_generic_ast_to_expr(children[4])
        return IfExp(true_expr, cond_expr, false_expr)

    elif node.syntax_part == "named_expression":
        children = node.children
        target_expr = from_generic_ast_to_expr(children[0])
        assert children[1].syntax_part == ":="
        value_expr = from_generic_ast_to_expr(children[2])
        return NamedExpr(target_expr, value_expr)

    elif node.syntax_part == "type":
        return from_generic_ast_to_expr(node.children[0])

    elif node.syntax_part == "slice":
        children = node.children

        (left_node, right_node, step_node) = (
            (children[0], children[2], children[4])
            if len(children) == 5 else


            (children[0], children[2], None)
            if len(children) == 4 and children[1].syntax_part == ":" and children[3].syntax_part == ":" else

            (None, children[1], children[3])
            if len(children) == 4 and children[0].syntax_part == ":" and children[2].syntax_part == ":" else

            (children[0], None, children[3])
            if len(children) == 4 and children[1].syntax_part == ":" and children[2].syntax_part == ":" else

            (children[0], None, None)
            if len(children) == 3 and children[1].syntax_part == ":" and children[2].syntax_part == ":" else

            (None, children[1], None)
            if len(children) == 3 and children[0].syntax_part == ":" and children[2].syntax_part == ":" else

            (None, None, children[2])
            if len(children) == 3 and children[0].syntax_part == ":" and children[1].syntax_part == ":" else

            (children[0], children[2], None)
            if len(children) == 3 and children[1].syntax_part == ":" and children[2].syntax_part != ":" else

            (None, children[1], None)
            if len(children) == 2 and children[0].syntax_part == ":" and children[1].syntax_part != ":" else

            (children[0], None, None)
            if len(children) == 2 and children[0].syntax_part != ":" and children[1].syntax_part == ":" else

            (None, None, None)
        )
        left = (
            SomeExpr(from_generic_ast_to_expr(left_node))
            if left_node else

            NoExpr()
        )

        right = (
            SomeExpr(from_generic_ast_to_expr(right_node))
            if right_node else

            NoExpr()
        )

        step = (
            SomeExpr(from_generic_ast_to_expr(step_node))
            if step_node else

            NoExpr()
        )

        return Slice(left, right, step)

    else:
        # keyword_identifier / not sure if this is actually ever used
        unsupported(node)



def from_generic_ast_to_keyword(node) -> keyword:
    children = node.children

    if (node.syntax_part == "keyword_argument"):
        key_node = children[0]
        assert children[1].syntax_part == "="
        value_node = children[2]

        key_id = from_generic_ast_to_identifier(key_node)
        value_expr = from_generic_ast_to_expr(value_node)
        return NamedKeyword(key_id, value_expr)

    elif (node.syntax_part == "dictionary_splat"):
        assert children[0].syntax_part == "**" 
        value_expr = from_generic_ast_to_expr(children[1])
        return SplatKeyword(value_expr)

    else:
        unsupported(node)



def from_generic_ast_to_Param(node : GenericNode) -> Param:

    if node.syntax_part == "identifier":
        id = from_generic_ast_to_identifier(node)
        return Param(id, NoParamType(), NoParamDefault())

    elif node.syntax_part == "typed_parameter":

        first_child = node.children[0]
        id_node = (
            first_child.children[1]
            if first_child.syntax_part == "list_splat_pattern" and
            first_child.children[0].syntax_part == "*"

            else
            first_child.children[1]
            if first_child.syntax_part == "dictionary_splat_pattern" and
            first_child.children[0].syntax_part == "**"

            else first_child

        ) 

        id = from_generic_ast_to_identifier(id_node)
        assert node.children[1].syntax_part == ":"
        type_anno = from_generic_ast_to_expr(node.children[2])
        return Param(id, SomeParamType(type_anno), NoParamDefault())

    elif node.syntax_part == "default_parameter":
        id = from_generic_ast_to_identifier(node.children[0])
        assert node.children[1].syntax_part == "="
        default_expr = from_generic_ast_to_expr(node.children[2])
        return Param(id, NoParamType(), SomeParamDefault(default_expr))

    elif node.syntax_part == "typed_default_parameter":
        id = from_generic_ast_to_identifier(node.children[0])
        assert node.children[1].syntax_part == ":"
        type_anno = from_generic_ast_to_expr(node.children[2])
        assert node.children[3].syntax_part == "="
        default_expr = from_generic_ast_to_expr(node.children[4])
        return Param(id, SomeParamType(type_anno), SomeParamDefault(default_expr))

    elif node.syntax_part == "list_splat_pattern":
        assert node.children[0].syntax_part == "*"
        id = from_generic_ast_to_identifier(node.children[1])
        return Param(id, NoParamType(), NoParamDefault())

    elif node.syntax_part == "dictionary_splat_pattern":
        assert node.children[0].syntax_part == "**"
        id = from_generic_ast_to_identifier(node.children[1])
        return Param(id, NoParamType(), NoParamDefault())

    else:
        unsupported(node)


def from_generic_ast_to_parameters(node : GenericNode) -> parameters:
    if node.syntax_part == "parameters" or node.syntax_part == "lambda_parameters":

        children = [
            child
            for child in (
                node.children
                if node.syntax_part == "lambda_parameters"

                else node.children[1:-1]
            )
            if child.syntax_part != ","
        ]

        # tree-sitter doesn't support position-only parameters
        pos_params = []

        def is_list_splat_node(n : GenericNode):
            return (
                n.syntax_part == "list_splat_pattern" or (
                    n.syntax_part == "typed_parameter" and
                    n.children[0].syntax_part == "list_splat_pattern"
                )
            )


        def is_dictionary_splat_node(n : GenericNode):
            return (
                n.syntax_part == "dictionary_splat_pattern" or (
                    n.syntax_part == "typed_parameter" and
                    n.children[0].syntax_part == "dictionary_splat_pattern"
                )
            )

        list_splat_index = next(
            (
                i 
                for i, n in enumerate(children)
                if is_list_splat_node(n) 
            ),
            None
        )


        dictionary_splat_index = next(
            (
                i 
                for i, n in enumerate(children)
                if is_dictionary_splat_node(n)
            ),
            None
        )

        (param_nodes, list_splat_node, kw_nodes, dictionary_splat_node) = (

            (
                children[0:list_splat_index], 
                children[list_splat_index], 
                children[list_splat_index + 1: dictionary_splat_index], 
                children[dictionary_splat_index]
            )
            if (list_splat_index and dictionary_splat_index)

            else (
                children[0:list_splat_index], 
                children[list_splat_index], 
                children[list_splat_index + 1: -1], 
                None
            )
            if list_splat_index and not dictionary_splat_index

            else (
                children[0:list_splat_index], 
                None,
                [],
                children[dictionary_splat_index]
            )
            if not list_splat_index and dictionary_splat_index

            else (
                children[0:list_splat_index], 
                None,
                [],
                None
            )
        )



        params = [
            from_generic_ast_to_Param(n)
            for n in param_nodes
        ]


        list_splat_param = (
            None
            if not list_splat_node or (
                list_splat_node.syntax_part == "list_splat_pattern" and 
                len(list_splat_node.children) == 0
            )

            else from_generic_ast_to_Param(list_splat_node)
        )

        kw_params = [
            from_generic_ast_to_Param(n)
            for n in kw_nodes
        ]

        dictionary_splat_param = utils.map_option(from_generic_ast_to_Param, dictionary_splat_node)


        return to_parameters(pos_params, params, list_splat_param, kw_params, dictionary_splat_param)


    else:
        unsupported(node)



def from_generic_ast_to_stmts(node : GenericNode, decorators : decorators = NoDec()) -> list[stmt]: 

    if (node.syntax_part == "import_statement"):
        children = node.children
        assert children[0].syntax_part == "import"
        return [Import(
            names = to_sequence_ImportName([
                from_generic_ast_to_ImportName(child)
                for child in children[1:]
                if child.syntax_part != ","
            ])
        )]

    elif (node.syntax_part == "import_from_statement"):
        children = node.children
        assert children[0].syntax_part == "from"
        assert_syntax = lambda node, label : node.syntax_part == label
        module = (
            (
                rel_import_node := children[1],
                prefix_node := rel_import_node.children[0],
                assert_syntax(prefix_node, "import_prefix"),
                prefix := len(prefix_node.children) * '.', 
                (
                    SomeModuleId(prefix + from_generic_ast_to_identifier(rel_import_node.children[1]))
                    if len(rel_import_node.children) == 2 else
                    SomeModuleId(prefix)
                )
            )[-1]
            if children[1].syntax_part == "relative_import" else

            SomeModuleId(from_generic_ast_to_identifier(children[1]))
        )

        assert children[2].syntax_part == "import"
        if len(children) == 4 and children[3].syntax_part == "wildcard_import":
            return [ImportWildCard(module)]

        else:

            import_list = (
                children[4:-1]
                if children[3].syntax_part == "(" else

                children[3:]
            )

            aliases = to_sequence_ImportName([
                from_generic_ast_to_ImportName(n) 
                for n in import_list
                if n.syntax_part != ","
            ])
            return [ImportFrom(module, aliases)]

    elif (node.syntax_part == "future_import_statement"):
        children = node.children
        assert children[0].syntax_part == "from"
        id = SomeModuleId(("__future__"))
        assert children[2].syntax_part == "import"

        import_list = (
            children[4:-1]
            if children[3].syntax_part == "(" else

            children[3:]
        )

        names = to_sequence_ImportName([
            from_generic_ast_to_ImportName(n) 
            for n in import_list 
            if n.syntax_part != ","
        ])
        return [ImportFrom(id, names)]

    elif (node.syntax_part == "assert_statement"):
        children = node.children
        assert children[0].syntax_part == "assert"
        test_expr = from_generic_ast_to_expr(children[1])

        if len(children) == 2:
            msg = from_generic_ast_to_expr(children[1])
            return [ AssertMsg(test_expr, msg) ]
        else:
            return [ Assert(test_expr) ]


    elif (node.syntax_part == "print_statement"):
        children = node.children
        assert children[0].syntax_part == "print"
        arg_nodes = [c for c in children[1:] if c.syntax_part != ","]
        arg_exprs = [
            from_generic_ast_to_expr(node)
            for node in arg_nodes
        ]

        return [ Expr(CallArgs(Name("print"), to_arguments(arg_exprs, []))) ]

    elif (node.syntax_part == "expression_statement"):
        children = node.children

        if (len(children) > 1):
            return [
                Expr(from_generic_ast_to_expr(expr_node))
                for expr_node in children
            ]
        else:
            estmt_node = children[0]
            if (estmt_node.syntax_part == "assignment"):
                estmt_children = estmt_node.children

                if estmt_children[2].syntax_part == "assignment":

                    def extract_targets_source(node, targets = []):
                        if node.syntax_part == "assignment":
                            target_node = node.children[0]
                            assert node.children[1].syntax_part == "="
                            remainder_node = node.children[2]
                            return extract_targets_source(remainder_node, targets + [from_generic_ast_to_expr(target_node)])
                        else:
                            return (targets, from_generic_ast_to_expr(node))

                    (targets, source) = extract_targets_source(estmt_node)

                    return [Assign(to_target_exprs(targets), source)]
                else:
                    (left, typ, right) = (

                        (estmt_children[0], estmt_children[2], None)
                        if len(estmt_children) == 3 and estmt_children[1].syntax_part == ":" else 
                        
                        (estmt_children[0], None, estmt_children[2])
                        if len(estmt_children) == 3 and estmt_children[1].syntax_part == "=" else 

                        (estmt_children[0], estmt_children[2], estmt_children[4])
                        if (
                            len(estmt_children) == 5 and 
                            estmt_children[1].syntax_part == ":" and
                            estmt_children[3].syntax_part == "="
                        ) else 
                        
                        (None, None, None)
                    )

                    assert left 

                    if typ:
                        left_expr = from_generic_ast_to_expr(left)
                        typ_expr = from_generic_ast_to_expr(typ)
                        right_expr = utils.map_option(from_generic_ast_to_expr, right)
                        if right_expr:
                            return [
                                TypedAssign(left_expr, typ_expr, right_expr)
                            ]
                        else:
                            return [
                                TypedDeclare(left_expr, typ_expr)
                            ]
                    elif right:
                        right_expr = from_generic_ast_to_expr(right)

                        left_exprs = SingleTargetExpr(from_generic_ast_to_expr(left))
                        return [
                            Assign(left_exprs, right_expr)
                        ] 

                    else:
                        unsupported(node) 


            elif (estmt_node.syntax_part == "augmented_assignment"):

                estmt_children = estmt_node.children

                left = estmt_children[0]
                op = estmt_children[1]
                right = estmt_children[2]

                left_expr = from_generic_ast_to_expr(left)
                oper = from_generic_ast_to_operator(op)
                right_expr = from_generic_ast_to_expr(right)
                return [
                    AugAssign(left_expr, oper, right_expr)
                ]

            else:
                return [Expr(from_generic_ast_to_expr(estmt_node))]
    elif (node.syntax_part == "return_statement"):
        children = node.children
        assert children[0].syntax_part == "return"
        if len(children) == 2:
            expr = from_generic_ast_to_expr(children[1])
            return [
                ReturnSomething(expr)
            ]
        else:
            return [Return()]




    elif (node.syntax_part == "delete_statement"):
        assert node.children[0].syntax_part == "del"
        child = node.children[1]
        if (child.syntax_part == "expression_list"):
            exprs = to_comma_exprs([
                from_generic_ast_to_expr(expr_node)
                for expr_node in child.children
                if expr_node.syntax_part != ","
            ])
            return [ Delete(exprs) ]
        else:
            exprs = SingleExpr(from_generic_ast_to_expr(child))
            return [ Delete(exprs) ]

    elif (node.syntax_part == "raise_statement"):
        children = node.children
        assert children[0].syntax_part == "raise"

        (exc, cause) = (
            (children[1], children[3]) 
            if len(children) == 4 
            
            else
            (children[1], None) 
            if len(children) == 2 
            
            else (None, None)
        )

        exc_expr = utils.map_option(from_generic_ast_to_expr, exc)
        cause_expr = utils.map_option(from_generic_ast_to_expr, cause)
        if (exc_expr and cause_expr):
            return [ RaiseFrom(exc_expr, cause_expr) ]
        elif (exc_expr):
            return [ RaiseExc(exc_expr) ]
        else:
            return [ Raise() ]


    elif (node.syntax_part == "pass_statement"):
        return [
            Pass()
        ]

    elif (node.syntax_part == "break_statement"):
        return [
            Break()
        ]

    elif (node.syntax_part == "continue_statement"):
        return [
            Continue()
        ]

    elif (node.syntax_part == "global_statement"):
        children = node.children
        assert children[0].syntax_part == "global"
        ids = to_sequence_var([
            from_generic_ast_to_identifier(id_node)
            for id_node in children[1:]
            if id_node.syntax_part != ","
        ])

        return [
            Global(ids)
        ]

    elif (node.syntax_part == "nonlocal_statement"):
        children = node.children
        assert children[0].syntax_part == "nonlocal"
        ids = to_sequence_var([
            from_generic_ast_to_identifier(id_node)
            for id_node in children[1:]
            if id_node.syntax_part != ","
        ])

        return [
            Nonlocal(ids)
        ]

    elif (node.syntax_part == "if_statement"):
        children = node.children
        assert children[0].syntax_part == "if"
        cond_node = children[1]
        assert children[2].syntax_part  == ":"
        block_node = children[3]


        def to_else_content(else_node : GenericNode) -> statements:
            assert else_node.syntax_part == "else_clause"

            else_children = else_node.children
            assert else_children[0].syntax_part == "else"
            assert else_children[1].syntax_part == ":"
            block_node_ = else_children[2]
            block_children = block_node_.children
            return to_statements([
                stmt 
                for stmt_node in block_children
                for stmt in from_generic_ast_to_stmts(stmt_node)
            ])

        import gen.python_ast
        def to_elif_content(elif_node : GenericNode) -> tuple[gen.python_ast.expr, statements]:
            assert (elif_node.syntax_part == "elif_clause")
            else_children = elif_node.children
            assert else_children[0].syntax_part == "elif"
            cond_node = else_children[1]
            assert else_children[2].syntax_part == ":"

            block_node_ = else_children[3]
            block_children = block_node_.children
            return (
                from_generic_ast_to_expr(cond_node),
                to_statements([
                    stmt 
                    for stmt_node in block_children
                    for stmt in from_generic_ast_to_stmts(stmt_node)
                ])
            )

        (else_block, else_nodes) = (

            (ElseCond(ElseBlock(to_else_content(children[-1]))), children[4:-1])
            if children[-1].syntax_part == "else_clause" else

            (NoCond(), children[4:])
        )

        for n in reversed(else_nodes):
            (e, sts) = to_elif_content(n)
            else_block = ElifCond(ElifBlock(e, sts), else_block)


        cond = from_generic_ast_to_expr(cond_node)
        block = to_statements([
            stmt
            for stmt_node in block_node.children
            for stmt in from_generic_ast_to_stmts(stmt_node)
        ])
        return [If(cond, block, else_block)]


    elif(node.syntax_part == "for_statement"):
        children = node.children

        (is_async, children) = (
          (True, children[1:])
          if (children[0].syntax_part == "async") else
          (False, children)
        ) 


        assert children[0].syntax_part == "for"
        target_expr = from_generic_ast_to_expr(children[1])
        assert children[2].syntax_part == "in"
        iter_expr = from_generic_ast_to_expr(children[3])
        assert children[4].syntax_part == ":"
        block_node = children[5]
        body_stmts = to_statements([
            stmt
            for stmt_node in block_node.children
            for stmt in from_generic_ast_to_stmts(stmt_node) 
        ])

        else_node = (
            children[6]
            if (len(children) == 7) 
            
            else None 
        )

        assert not else_node or else_node.syntax_part == "else_clause"

        assert not else_node or else_node.children[0].syntax_part == "else" 

        assert not else_node or else_node.children[1].syntax_part == ":" 

        else_block = else_node.children[2] if else_node else None 

        assert not else_block or else_block.syntax_part == "block"

        block_children = else_block.children if else_block else []


        if block_children:

            else_block = ElseBlock(to_statements([
                stmt
                for stmt_node in block_children
                for stmt in from_generic_ast_to_stmts(stmt_node) 
            ]))

            if is_async:
                return [
                    AsyncForElse(target_expr, iter_expr, body_stmts, else_block)
                ]

            else:
                return [
                    ForElse(target_expr, iter_expr, body_stmts, else_block)
                ]
        else:

            if is_async:
                return [
                    AsyncFor(target_expr, iter_expr, body_stmts)
                ]

            else:
                return [
                    For(target_expr, iter_expr, body_stmts)
                ]

    elif(node.syntax_part == "while_statement"):
        children = node.children
        assert children[0].syntax_part == "while"
        test_expr = from_generic_ast_to_expr(children[1])

        assert children[2].syntax_part == ":"
        block_node = children[3]
        assert block_node.syntax_part == "block"
        body_stmts = to_statements([
            stmt
            for stmt_node in block_node.children 
            for stmt in from_generic_ast_to_stmts(stmt_node) 
        ])

        else_node = (
            children[4]
            if (len(children) == 5) 
            
            else None 
        )


        assert not else_node or else_node.syntax_part == "else_clause"

        assert not else_node or else_node.children[0].syntax_part == "else" 

        assert not else_node or else_node.children[1].syntax_part == ":" 

        else_block = else_node.children[2] if else_node else None 

        assert not else_block or else_block.syntax_part == "block"

        block_children = else_block.children if else_block else []


        if else_block:
            else_stmts = ElseBlock(to_statements([
                stmt
                for stmt_node in block_children 
                for stmt in from_generic_ast_to_stmts(stmt_node) 
            ]))

            return [
                WhileElse(test_expr, body_stmts, else_stmts)
            ]
        else:
            return [
                While(test_expr, body_stmts)
            ]

    elif (node.syntax_part == "try_statement"):
        children = node.children
        assert children[0].syntax_part == "try"
        assert children[1].syntax_part == ":"
        try_block = children[2]
        assert try_block.syntax_part == "block"
        try_stmts = to_statements([
            stmt
            for stmt_node in try_block.children
            for stmt in from_generic_ast_to_stmts(stmt_node) 
        ])

        except_clause_nodes = [
            n
            for n in children
            if n.syntax_part == "except_clause"
        ]

        except_handlers = (
            to_sequence_ExceptHandler([
                from_generic_ast_to_ExceptHandler(ec_node)
                for ec_node in except_clause_nodes
            ])
            if except_clause_nodes else

            None
        )

        else_clause_nodes = [
            n
            for n in children
            if n.syntax_part == "else_clause"
        ] 

        def assert_else_clause(else_clause_node):
            assert else_clause_node.children[0].syntax_part == "else"
            assert else_clause_node.children[1].syntax_part == ":"
            assert else_clause_node.children[2].syntax_part == "block"

        else_stmts = (
            [] 
            if len(else_clause_nodes) == 0 else
            
            [
                stmt
                for else_clause_node in [else_clause_nodes[0]]
                for _ in [assert_else_clause(else_clause_node)]
                for else_block_node in [else_clause_node.children[2]]
                for stmt_node in else_block_node.children
                for stmt in from_generic_ast_to_stmts(stmt_node)
            ]
        )

        finally_clause_nodes = [
            n
            for n in children
            if n.syntax_part == "finally_clause"
        ]

        def assert_finally_clause(n):
            assert n.children[0].syntax_part == "finally"
            assert n.children[1].syntax_part == ":"
            assert n.children[2].syntax_part == "block"
        
        finally_stmts = (
            [] 
            if len(finally_clause_nodes) == 0 else

            [
                stmt
                for finally_clause_node in [finally_clause_nodes[0]] 
                for _ in [assert_finally_clause(finally_clause_node)]
                for block_node in [finally_clause_node.children[2]] 
                for stmt_node in block_node.children
                for stmt in from_generic_ast_to_stmts(stmt_node)
            ]
        )


        if except_handlers and else_stmts and finally_stmts:
            return [
                TryElseFin(try_stmts, except_handlers, ElseBlock(to_statements(else_stmts)), FinallyBlock(to_statements(finally_stmts)))
            ]

        elif except_handlers and else_stmts:
            return [
                TryElse(try_stmts, except_handlers, ElseBlock(to_statements(else_stmts)))
            ]

        elif except_handlers and finally_stmts:
            return [
                TryExceptFin(try_stmts, except_handlers, FinallyBlock(to_statements(finally_stmts)))
            ]

        elif finally_stmts:
            return [
                TryFin(try_stmts, FinallyBlock(to_statements(finally_stmts)))
            ]

        elif except_handlers:
            return [
                Try(try_stmts, except_handlers)
            ]
        else:
            assert False



    elif (node.syntax_part == "with_statement"):
        children = node.children
        (is_async, children) = (
          (True, children[1:])
          if (children[0].syntax_part == "async") else
          (False, children)
        ) 

        assert children[0].syntax_part == "with"

        with_clause_node = children[1]
        assert with_clause_node.syntax_part == "with_clause"

        with_items = to_sequence_Withitem([
            from_generic_ast_to_Withitem(item_node)
            for item_node in with_clause_node.children
        ])


        assert children[2].syntax_part == ":"
        block_node = children[3]
        assert block_node.syntax_part == "block"
        stmts = to_statements([
            stmt
            for stmt_node in block_node.children
            for stmt in from_generic_ast_to_stmts(stmt_node)
        ])

        if is_async:
            return [
                AsyncWith(with_items, stmts)
            ]

        else:
            return [
                With(with_items, stmts)
            ]

    elif (node.syntax_part == "function_definition"):
        children = node.children
        (is_async, children) = (
            (True, children[1:])
            if (children[0].syntax_part == "async") else
            (False, children)
        ) 

        assert children[0].syntax_part == "def"
        name_node = children[1]
        name = from_generic_ast_to_identifier(name_node)

        params_node = children[2]
        param_group = from_generic_ast_to_parameters(params_node)

        (return_type_node, block_node) = (
            (children[4], children[6])
            if children[3].syntax_part == "->" and children[5].syntax_part == ":"
            
            else (None, children[4])
            if children[3].syntax_part == ":"

            else (None, None)
        )

        assert block_node

        return_type = (
            SomeReturnType(from_generic_ast_to_expr(return_type_node))
            if return_type_node else

            NoReturnType()
        )

        body = to_statements([
            stmt
            for stmt_node in block_node.children
            for stmt in from_generic_ast_to_stmts(stmt_node)
        ])

        if is_async: 
            return [
                DecAsyncFunctionDef(
                    decorators,
                    AsyncFunctionDef(name, param_group, return_type, body)
                )
            ]

        else:
            return [
                DecFunctionDef(
                    decorators, 
                    FunctionDef(name, param_group, return_type, body)
                )
            ]


    elif (node.syntax_part == "class_definition"):
        children = node.children

        assert children[0].syntax_part == "class"

        name_node = children[1]
        name = from_generic_ast_to_identifier(name_node)

        (arguments_node, block_node) = (
            (None, children[3])
            if children[2].syntax_part == ":"

            else (children[2], children[4])

        )

        (argument_nodes) = (
            [
                n
                for n in arguments_node.children[1:-1]
                if n.syntax_part != ","
            ]
            if (arguments_node != None) else
            []
        )

        base_nodes = [n for n in argument_nodes if n.syntax_part != "keyword_argument" and n.syntax_part != "dictionary_splat"]
        kw_nodes = [n for n in argument_nodes if n.syntax_part == "keyword_argument" or n.syntax_part == "dictionary_splat"]

        base_exprs = [
            from_generic_ast_to_expr(n)
            for n in base_nodes
        ]

        keywords = [
            from_generic_ast_to_keyword(n)
            for n in kw_nodes
        ]

        bases = to_bases(base_exprs, keywords)

        body_stmts = to_statements([
            stmt
            for n in block_node.children
            for stmt in from_generic_ast_to_stmts(n)
        ])

        return [
            DecClassDef(
                decorators,
                ClassDef(name, bases, body_stmts)
            )
        ]

    elif (node.syntax_part == "decorated_definition"):
        children = node.children
        dec_nodes = children[0:-1]
        def assert_decorator(dec_node):
            assert dec_node.syntax_part == "decorator"
            assert dec_node.children[0].syntax_part == "@"

        dec_exprs = to_decorators([
            from_generic_ast_to_expr(dec_expr_node)
            for dec_node in dec_nodes
            for _ in [assert_decorator(dec_node)]
            for dec_expr_node in [dec_node.children[1]]
        ])

        def_node = children[-1]
        return from_generic_ast_to_stmts(def_node, decorators = dec_exprs)

    elif (node.syntax_part == "comment"):
        return []

    else:
        # exec_statement for Python 2
        # print_statement for Python 2
        print("syntax unsupported: " + node.syntax_part)
        unsupported(node)