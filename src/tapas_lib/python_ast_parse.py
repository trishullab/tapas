from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from collections.abc import Callable

from abc import ABC, abstractmethod


from tapas_base import util_system
from tapas_base.abstract_token_construct_autogen import Vocab
from tapas_lib.generic_tree_system import GenericNode
from tapas_lib.python_ast_construct_autogen import *
from tapas_lib import python_ast_construct_autogen as past 


class Obsolete(Exception):
    pass

class Unsupported(Exception):
    pass

class ConcreteParsingError(Exception):
    pass

class TreeSitterError(Exception):
    pass

def obsolete(node : GenericNode):
    raise Obsolete(node.syntax_part)

def node_error(node : GenericNode) -> None:
    if (node.syntax_part == "ERROR"):
        raise ConcreteParsingError()
    else:
        raise Unsupported(node.syntax_part)



def is_comment(cm_node):
    print(f"cm_node ~> {cm_node}")
    assert cm_node.syntax_part == "comment"
    return cm_node.syntax_part == "comment"

def merge_comments(comment_nodes : list[GenericNode]) -> str:
    return "\n".join([cm.text for cm in comment_nodes if is_comment(cm)])


def to_bases(bases : list[expr | None], keywords : list[keyword | None], default_start : int, default_end : int) -> bases:
    if not bases and not keywords:
        return NoBases(default_start, default_end)
    else:

        start_node, end_node = (
            (bases[0], keywords[-1])
            if bases and keywords else
            (bases[0], bases[-1])
            if bases else
            (keywords[0], keywords[-1])
        )

        start = (
            unguard_expr(start_node).source_start
            if isinstance(start_node, expr) else
            unguard_keyword(start_node).source_end
            if isinstance(start_node, keyword) else
            0
        )
        end = (
            unguard_expr(end_node).source_start
            if isinstance(end_node, expr) else
            unguard_keyword(end_node).source_end
            if isinstance(end_node, keyword) else
            0
        )


        return SomeBases(to_sequence_base(bases, keywords), start, end)


def to_sequence_base(bases : list[expr | None], keywords : list[keyword | None]) -> bases_a | None:
    if  bases or keywords:

        (result, bases) = (

            (KeywordBases(to_keywords(keywords), 
                unguard_keyword(keywords[0]).source_start if keywords[0] else 0,
                unguard_keyword(keywords[-1]).source_end if keywords[-1] else 0,
            ), bases)
            if keywords else

            (SingleBase(bases[-1],
                unguard_expr(bases[-1]).source_start if bases[-1] else 0,
                unguard_expr(bases[-1]).source_end if bases[-1] else 0,
            ), bases[:-1])

        )

        for b in reversed(bases):
            result = ConsBase(b, result,
                unguard_expr(b).source_start if b else 0,
                unguard_expr(b).source_end if b else 0,
            )

        return result
    else:
        return None



def to_parameters(
    pos_params : list[Param | None], 
    params : list[Param | None], 
    list_splat_param : Param | None, 
    kw_params : list[Param | None], 
    dictionary_splat_param : Param | None,
    default_start : int,
    default_end : int,
) -> parameters:

    if not (
        pos_params or params or list_splat_param or kw_params or dictionary_splat_param
    ):
        return NoParam(default_start, default_end)
    elif pos_params:
        return ParamsA(to_parameters_a(
            pos_params, params, list_splat_param, kw_params, dictionary_splat_param
        ), default_start, default_end)
    else:
        return ParamsB(to_parameters_b(
            params, list_splat_param, kw_params, dictionary_splat_param
        ), default_start, default_end)


def to_parameters_d(
    kw_params : list[Param | None], 
    dictionary_splat_param : Param | None
) -> parameters_d:
    assert kw_params
    (result, kw_params) = (
        (TransKwParam(kw_params[-1], dictionary_splat_param,
            kw_params[-1].source_start if kw_params[-1] else 0,
            dictionary_splat_param.source_start if dictionary_splat_param else 0
        ), kw_params[:-1])
        if dictionary_splat_param else

        (SingleKwParam( kw_params[-1],
            kw_params[-1].source_start if kw_params[-1] else 0,
            kw_params[-1].source_end if kw_params[-1] else 0,
        ), kw_params[:-1])
    )

    for p in reversed(kw_params):
        result = ConsKwParam(p, result,
            p.source_start if p else 0,
            result.source_end,
        )

    return result


def to_parameters_c(
    list_splat_param : Param | None, 
    kw_params : list[Param | None], 
    dictionary_splat_param : Param | None,
) -> parameters_c:
    if list_splat_param and kw_params:
        source_start = list_splat_param.source_start
        source_end = (
            dictionary_splat_param.source_end 
            if dictionary_splat_param else
            kw_params[-1].source_end 
            if kw_params[-1] else 0
        )
        return TransTupleBundleParam(list_splat_param, 
            to_parameters_d(kw_params, dictionary_splat_param),
            source_start, source_end
        )
    elif list_splat_param and not kw_params and not dictionary_splat_param:
        source_start = list_splat_param.source_start
        source_end = list_splat_param.source_end if list_splat_param else 0
        return SingleTupleBundleParam(list_splat_param, 
            source_start, source_end
        )
    elif list_splat_param and not kw_params and dictionary_splat_param:
        source_start = list_splat_param.source_start
        source_end =  dictionary_splat_param.source_end
        return DoubleBundleParam(list_splat_param, dictionary_splat_param,
            source_start, source_end
        )
    elif not list_splat_param and not kw_params and dictionary_splat_param:
        source_start = dictionary_splat_param.source_start
        source_end = dictionary_splat_param.source_end
        return DictionaryBundleParam(dictionary_splat_param,
            source_start, source_end
        )
    else:
        #  not list_splat_param and kw_params:
        params_d = to_parameters_d(kw_params, dictionary_splat_param)
        return ParamsD(params_d,
            unguard_parameters_d(params_d).source_start if params_d else 0, 
            unguard_parameters_d(params_d).source_end if params_d else 0
        )


def to_parameters_b(
    params : list[Param | None], 
    list_splat_param : Param | None, 
    kw_params : list[Param | None], 
    dictionary_splat_param : Param | None,
) -> parameters_b:

    (result, params) = (
        (
            params_c := to_parameters_c(list_splat_param, kw_params, dictionary_splat_param),
            (
            ParamsC(params_c,
                unguard_parameters_c(params_c).source_start,
                unguard_parameters_c(params_c).source_end,
            ), 
            params
            )
        )[-1]
        if (list_splat_param or kw_params or dictionary_splat_param) else

        (SinglePosKeyParam( params[-1],
            params[-1].source_start if params[-1] else 0,
            params[-1].source_end if params[-1] else 0,
        ), params[:-1])
    )

    for p in reversed(params):
        result = ConsPosKeyParam(p, result,
            p.source_start if p else 0,
            result.source_end if result else 0
        )

    return result


def to_parameters_a(
    pos_params : list[Param | None], 
    params : list[Param | None], 
    list_splat_param : Param | None, 
    kw_params : list[Param | None], 
    dictionary_splat_param : Param | None
) -> parameters_a:
    assert pos_params

    result = (
        (
            params_b := to_parameters_b(params, list_splat_param, kw_params, dictionary_splat_param),
            TransPosParam(pos_params[-1], params_b,
                pos_params[-1].source_start if pos_params[-1] else 0,
                unguard_parameters_b(params_b).source_end
            )
        )[-1]
        if (params or list_splat_param or kw_params or dictionary_splat_param) else

        SinglePosParam(pos_params[-1],
            pos_params[-1].source_start if pos_params[-1] else 0,
            pos_params[-1].source_end if pos_params[-1] else 0,
        )
    )

    for pp in reversed(pos_params[:-1]):
        result = ConsPosParam(pp, result,
            pp.source_start if pp else 0,
            result.source_end
        )

    return result



def to_comparisons(crs : list[CompareRight]) -> comparisons:
    assert crs 

    result = SingleCompareRight(crs[-1],
        crs[-1].source_start,
        crs[-1].source_end,
    )
    for cr in reversed(crs[:-1]):
        result = ConsCompareRight(cr, result,
            cr.source_start,
            result.source_end
        )

    return result

def to_dictionary_content(items : list[dictionary_item]) -> dictionary_content:
    assert items 

    result = SingleDictionaryItem(items[-1],
        unguard_dictionary_item(items[-1]).source_start,
        unguard_dictionary_item(items[-1]).source_end,
    )
    for f in reversed(items[:-1]):
        result = ConsDictionaryItem(f, result,
            unguard_dictionary_item(f).source_start,
            result.source_end
        )

    return result

def to_comprehension_constraints(cs : list[constraint]) -> comprehension_constraints:
    assert cs 

    result = SingleConstraint(cs[-1],
        unguard_constraint(cs[-1]).source_start,
        unguard_constraint(cs[-1]).source_end,
    )
    for c in reversed(cs[:-1]):
        result = ConsConstraint(c, result,
            unguard_constraint(c).source_start,
            result.source_end
        )

    return result

def to_statements(stmts : list[stmt | None]) -> statements | None:
    if stmts:

        result = SingleStmt(stmts[-1],
            unguard_stmt(stmts[-1]).source_start if stmts[-1] else 0,
            unguard_stmt(stmts[-1]).source_end if stmts[-1] else 0,
        )
        for stmt in reversed(stmts[:-1]):
            result = ConsStmt(stmt, result,
                unguard_stmt(stmt).source_start if stmt else 0,
                result.source_end
            )

        return result
    else:
        return None

def to_sequence_import_name(ns : list[import_name | None]) -> sequence_import_name:
    assert ns 

    result = SingleImportName(ns[-1],
            unguard_import_name(ns[-1]).source_start if ns[-1] else 0,
            unguard_import_name(ns[-1]).source_end if ns[-1] else 0,
    )
    for n in reversed(ns[:-1]):
        result = ConsImportName(n, result,
            unguard_import_name(n).source_start if n else 0,
            result.source_end
        )

    return result

def to_sequence_var(ids : list[tuple[str, int, int]]) -> sequence_name:
    assert ids 

    result = SingleId(ids[-1][0], ids[-1][1], ids[-1][2])
    for id in reversed(ids[:-1]):
        result = ConsId(id[0], result,
            id[1],
            result.source_end
        )

    return result

def to_sequence_ExceptHandler(es : list[ExceptHandler]) -> sequence_ExceptHandler:
    assert es 

    result = SingleExceptHandler(es[-1],
        es[-1].source_start,
        es[-1].source_end,
    )
    for e in reversed(es[:-1]):
        result = ConsExceptHandler(e, result,
            e.source_start,
            result.source_end,
        )

    return result


def to_sequence_with_item(ws : list[with_item]) -> sequence_with_item:
    assert ws 

    result = SingleWithItem(ws[-1],
        unguard_with_item(ws[-1]).source_start,
        unguard_with_item(ws[-1]).source_end,
    )
    for w in reversed(ws[:-1]):
        result = ConsWithItem(w, result,
            unguard_with_item(w).source_start,
            result.source_end
        )

    return result


def to_decorators(ds : list[decorator | None], base_start : int, base_end : int) -> decorators:

    result = NoDec(base_start, base_end)
    for d in reversed(ds):
        result = ConsDec(d, result,
            unguard_decorator(d).source_start if d else 0,
            result.source_end
        )

    return result 



def to_comma_exprs(comma_sep_nodes : list[GenericNode]) -> comma_exprs | None:

    end_indices = [ 
        i
        for i, n in enumerate(comma_sep_nodes)
        if n.syntax_part == ","
    ] + [len(comma_sep_nodes)]

    start_indices = [0] + [ 
        i + 1 
        for i, n in enumerate(comma_sep_nodes)
        if n.syntax_part == ","
    ]

    assert len(end_indices) == len(start_indices)


    exprs = from_list_to_comma_exprs([ 
        (pre, from_generic_tree_to_expr(n), post)
        for start, end in zip(start_indices, end_indices) 
        for section in [comma_sep_nodes[start:end]]
        for split_index in [next(
            i for i, n in enumerate(section)
            if n.syntax_part != "comment"
        )]
        for n in [section[split_index]]
        for pre in [merge_comments(section[0:split_index])]
        for post in [merge_comments(section[split_index + 1:])]
    ])

    return exprs


def from_list_to_comma_exprs(es : list[tuple[str, expr | None, str]]) -> comma_exprs | None:
    if es :
        (pre_comment, e, post_comment) = es[-1]
        result = SingleExpr(pre_comment, e, post_comment,
            unguard_expr(e).source_start if e else 0,
            unguard_expr(e).source_end if e else 0,
        )
        for (pre_comment, e, post_comment) in reversed(es[:-1]):
            result = ConsExpr(pre_comment, e, post_comment, result,
                unguard_expr(e).source_start if e else 0,
                result.source_end
            )

        return result
    else:
        return None

def to_target_exprs(es : list[expr]) -> target_exprs:
    assert es 

    result = SingleTargetExpr(es[-1],
        unguard_expr(es[-1]).source_start if es[-1] else 0,
        unguard_expr(es[-1]).source_end if es[-1] else 0,
    )
    for e in reversed(es[:-1]):
        result = ConsTargetExpr(e, result,
            unguard_expr(e).source_start if e else 0,
            result.source_end
        )

    return result

def to_constraint_filters(es : list[expr | None], base_start : int, base_end : int) -> constraint_filters:

    (result, es) = (
        (SingleFilter(es[-1],
            unguard_expr(es[-1]).source_start if es[-1] else 0,
            unguard_expr(es[-1]).source_end if es[-1] else 0,
        ), es[:-1])
        if es else

        (NoFilter(base_start, base_end), es) 
    )
    for e in reversed(es):
        result = ConsFilter(e, result,
            unguard_expr(e).source_start if e else 0,
            result.source_end
        )

    return result

def to_sequence_string(ss : list[tuple[str, int, int]]) -> sequence_string:
    assert ss  

    result = SingleStr(ss[-1][0], ss[-1][1], ss[-1][2])
    for s in reversed(ss[:-1]):
        result = ConsStr(s[0], result,
            s[1],
            result.source_end
        )

    return result

def to_keywords(ks : list[keyword | None]) -> keywords:
    assert ks  

    result = SingleKeyword(ks[-1],
        unguard_keyword(ks[-1]).source_start if ks[-1] else 0,
        unguard_keyword(ks[-1]).source_end if ks[-1] else 0,
    )
    for k in reversed(ks[:-1]):
        result = ConsKeyword(k, result,
            unguard_keyword(k).source_start if k else 0,
            result.source_end
        )

    return result

def to_arguments(ps : list[expr | None], ks : list[keyword | None]) -> arguments:

    (result, ps) = (
        (
            kws := to_keywords(ks),
            (KeywordsArg(kws,
                unguard_keywords(kws).source_start,
                unguard_keywords(kws).source_end,
            ), ps)
        )[-1]
        if ks else

        (SingleArg(ps[-1],
            unguard_expr(ps[-1]).source_start if ps[-1] else 0,
            unguard_expr(ps[-1]).source_end if ps[-1] else 0,
        ), ps[:-1])
    )

    for p in reversed(ps):
        result = ConsArg(p, result,
            unguard_expr(p).source_start if p else 0,
            result.source_end
        )

    return result


def from_generic_tree(node : GenericNode) -> module: 
    if (node.syntax_part == "module"):
        children = node.children

        first = children[0]
        rest = children[1:]

        if (first.syntax_part == "future_import_statement"):
            children = first.children
            assert children[0].syntax_part == "from"
            id = ("__future__")
            assert children[2].syntax_part == "import"

            import_list = (
                children[4:-1]
                if children[3].syntax_part == "(" else

                children[3:]
            )

            names = to_sequence_import_name([
                from_generic_tree_to_import_name(n) 
                for n in import_list 
                if n.syntax_part != ","
            ])

            statements = [
                stmt
                for stmt_node in rest  
                for stmt in from_generic_tree_to_stmts(stmt_node)
            ]
            
            return FutureMod(names, to_statements(statements), node.source_start, node.source_end)
        else:
            statements = [
                stmt
                for stmt_node in children  
                for stmt in from_generic_tree_to_stmts(stmt_node)
            ]
            
            return SimpleMod(to_statements(statements), node.source_start, node.source_end)
    else:
       node_error(node) 
       raise ConcreteParsingError()





def from_generic_tree_to_identifier(node : GenericNode) -> str:
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
       return "" 


def from_generic_tree_to_import_name(node : GenericNode, alias : Optional[str] = None) -> import_name | None:
    
    if (node.syntax_part == "dotted_name"):
        dotted_name = ".".join([
            child.text
            for child in node.children
            if child.syntax_part == "identifier"
        ])
        return (
            ImportNameAlias(dotted_name, alias, node.source_start, node.source_end) 
            if alias else 
            ImportNameOnly(dotted_name, node.source_start, node.source_end)
        )

    elif (node.syntax_part == "identifier"):
        text = node.text
        return (
            ImportNameAlias(text, alias, node.source_start, node.source_end) 
            if alias else 
            ImportNameOnly(text, node.source_start, node.source_end)
        )

    elif (node.syntax_part == "aliased_import"):
        children = node.children
        name_node = children[0]
        assert children[1].syntax_part == "as"
        asname_node = children[2]
        asname_text = asname_node.text
        return from_generic_tree_to_import_name(name_node, asname_text)
    else:
        return node_error(node)

def from_generic_tree_to_unaryop(node):
    if (node.syntax_part == "~"):
       return Invert(node.source_start, node.source_end) 
    elif (node.syntax_part == "+"):
       return UAdd(node.source_start, node.source_end) 
    elif (node.syntax_part == "-"):
       return USub(node.source_start, node.source_end) 
    else:
        return node_error(node)

def from_generic_tree_to_boolop(node):
    if node.syntax_part == "and":
       return And(node.source_start, node.source_end) 
    elif node.syntax_part == "or":
       return Or(node.source_start, node.source_end) 
    else:
        return node_error(node)

def from_generic_tree_to_bin_rator(node : GenericNode) -> bin_rator | None: 

    if node.syntax_part in {"+=", "+"}:
       return Add(node.source_start, node.source_end) 

    elif node.syntax_part in {"-=", "-"}:
        return Sub(node.source_start, node.source_end)

    elif node.syntax_part in {"*=", "*"}:
        return Mult(node.source_start, node.source_end)

    elif node.syntax_part in {"/=", "/"}:
        return Div(node.source_start, node.source_end)

    elif node.syntax_part in {"@=", "@"}:
        return MatMult(node.source_start, node.source_end)

    elif node.syntax_part in {"//=", "//"}:
        return FloorDiv(node.source_start, node.source_end)

    elif node.syntax_part in {"%=", "%"}:
        return Mod(node.source_start, node.source_end)

    elif node.syntax_part in {"**=", "**"}:
        return Pow(node.source_start, node.source_end)

    elif node.syntax_part in {">>=", ">>"}:
        return RShift(node.source_start, node.source_end)

    elif node.syntax_part in {"<<=", "<<"}:
        return LShift(node.source_start, node.source_end)

    elif node.syntax_part in {"&=", "&"}:
        return BitAnd(node.source_start, node.source_end)

    elif node.syntax_part in {"^=", "^"}:
        return BitXor(node.source_start, node.source_end)

    elif node.syntax_part in {"|=", "|"}:
        return BitOr(node.source_start, node.source_end)

    else:
        return node_error(node)


def split_rators_and_rands(
    nodes : list[GenericNode], 
    rators : list[cmp_rator] = [], 
    rands : list[expr | None] = []
) -> tuple[list[cmp_rator], list[expr | None]]:

    if len(nodes) == 0:
        return (rators, rands)
    else:
        head = nodes[-1]
        if head.syntax_part == '<':
            return split_rators_and_rands(nodes[:-1], rators + [Lt(head.source_start, head.source_end)], rands)
        if head.syntax_part == '<=':
            return split_rators_and_rands(nodes[:-1], rators + [LtE(head.source_start, head.source_end)], rands)
        if head.syntax_part == '==':
            return split_rators_and_rands(nodes[:-1], rators + [Eq(head.source_start, head.source_end)], rands)
        if head.syntax_part == '!=':
            return split_rators_and_rands(nodes[:-1], rators + [NotEq(head.source_start, head.source_end)], rands)
        if head.syntax_part == '>=':
            return split_rators_and_rands(nodes[:-1], rators + [GtE(head.source_start, head.source_end)], rands)
        if head.syntax_part == '>':
            return split_rators_and_rands(nodes[:-1], rators + [Gt(head.source_start, head.source_end)], rands)
        if head.syntax_part == '<>':
            return split_rators_and_rands(nodes[:-1], rators + [NotEq(head.source_start, head.source_end)], rands)
        if head.syntax_part == 'in':
            return split_rators_and_rands(nodes[:-1], rators + [In(head.source_start, head.source_end)], rands)
        if head.syntax_part == 'not':
            next_head = nodes[-2]
            if next_head.syntax_part == "in":
                return split_rators_and_rands(nodes[:-2], rators + [NotIn(head.source_start, next_head.source_end)], rands)
            else:
                raise Unsupported(next_head.syntax_part)
                # return split_rators_and_rands(nodes[:-1], rators + [In()], rands)
        if head.syntax_part == 'is':
            next_head = nodes[-2]
            if next_head.syntax_part == "not":
                return split_rators_and_rands(nodes[:-2], rators + [IsNot(head.source_start, next_head.source_end)], rands)
            else:
                return split_rators_and_rands(nodes[:-1], rators + [Is(head.source_start, head.source_end)], rands)

        else:
            rand = from_generic_tree_to_expr(head)
            tail = nodes[:-1]
            return split_rators_and_rands(tail, rators, rands + [rand])


def from_generic_tree_to_ExceptHandler(node : GenericNode) -> ExceptHandler:
    assert node.syntax_part == "except_clause"
    children = node.children
    assert children[0].syntax_part == "except"
    (expr_node, name_node, comment_text, block_node) = (

        (None, None, merge_comments(children[2:-1]), children[-1])
        if children[1].syntax_part == ":" else 
        
        (children[1], None, merge_comments(children[3:-1]), children[-1])
        if children[2].syntax_part == ":" else 
        
        (children[1], children[3], merge_comments(children[5:-1]), children[-1]) if (
            children[2].syntax_part == "as" and 
            children[4].syntax_part == ":" 
        ) else 

        (children[1], children[3], merge_comments(children[5:-1]), children[-1]) if (
            children[2].syntax_part == "," and 
            children[4].syntax_part == ":" 
        ) else 
        
        (None, None, '', None)
    )

    assert block_node

    expr = from_generic_tree_to_expr(expr_node) if expr_node else None
    name = from_generic_tree_to_identifier(name_node) if name_node else None
    stmts = [
        stmt
        for stmt_node in block_node.children
        for stmt in from_generic_tree_to_stmts(stmt_node)
    ]

    arg  = (
        SomeExceptArgName(expr, name, expr_node.source_start, name_node.source_end)
        if expr and expr_node and name and name_node else

        SomeExceptArg(expr, expr_node.source_start, expr_node.source_end)
        if expr and expr_node else

        NoExceptArg(node.source_start, node.source_end)
    )

    return  ExceptHandler(arg, comment_text, to_statements(stmts), node.source_start, node.source_end)


def from_generic_tree_to_with_item(node : GenericNode) -> with_item:
    assert node.syntax_part == "with_item"
    children = node.children

    if children[0].syntax_part == "as_pattern":
        as_pattern_node = children[0]
        assert (
            len(as_pattern_node.children) == 3 and 
            as_pattern_node.children[1].syntax_part == "as"
        ) 

        content_node = as_pattern_node.children[0]
        content_expr = from_generic_tree_to_expr(content_node)


        as_pattern_target_node = as_pattern_node.children[2]
        assert as_pattern_target_node.syntax_part == "as_pattern_target"
        pattern_node = as_pattern_target_node.children[0]
        pattern_expr = from_generic_tree_to_expr(pattern_node) if pattern_node else None

        return WithItemAlias(content_expr, pattern_expr, node.source_start, node.source_end)

    else:
        content_node = children[0]
        content_expr = from_generic_tree_to_expr(content_node)

        return WithItemOnly(content_expr, node.source_start, node.source_end) 


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


    target_expr = from_generic_tree_to_expr(for_children[1])
    iter_expr = from_generic_tree_to_expr(for_children[3])

    def assert_if_node(n):
        assert n.syntax_part == "if_clause"
        assert n.children[0].syntax_part == "if"




    if_nodes = nodes[1:]
    if_exprs = [
        from_generic_tree_to_expr(n.children[1])
        for n in if_nodes
        for _ in [assert_if_node(n)]
    ]


    source_start = nodes[0].source_start
    source_end = nodes[-1].source_end
    if is_async:
        return AsyncConstraint(target_expr, iter_expr, to_constraint_filters(if_exprs, 
            unguard_expr(iter_expr).source_end if iter_expr else 0,
            source_end
        ), source_start, source_end)
    else:
        return Constraint(target_expr, iter_expr, to_constraint_filters(if_exprs,
            unguard_expr(iter_expr).source_end if iter_expr else 0,
            source_end
        ), source_start, source_end)


def collapse_constraint_nodes(nodes : list[GenericNode]) -> list[constraint] | None:

    def collapse_constraint_nodes_r(
        nodes : list[GenericNode], 
        collected_group : list[GenericNode] = [], 
        collected_constraints : list[constraint] = []
    ) -> list[constraint] | None:

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
                return node_error(node)

    return collapse_constraint_nodes_r([n for n in reversed(nodes)])


def from_generic_tree_to_expr(node : GenericNode) -> expr | None: 

    if node.syntax_part == "binary_operator" :
        children = node.children
        left_node = children[0]
        split_index = next(
            i + 1 for i, n in enumerate(children[1:-1])
            if n.syntax_part != "comment"
        )
        op_node = children[split_index]
        print(f"op_node :: {op_node}")
        pre_comment = merge_comments(children[1:split_index])
        post_comment = merge_comments(children[split_index + 1: -1])
        right_node = children[-1]

        left_expr = from_generic_tree_to_expr(left_node)
        op = from_generic_tree_to_bin_rator(op_node)
        right_expr = from_generic_tree_to_expr(right_node)

        return BinOp(left_expr, pre_comment, op, post_comment, right_expr, left_node.source_start, right_node.source_end)

    elif node.syntax_part == "identifier":
        return Name(from_generic_tree_to_identifier(node), node.source_start, node.source_end)

    elif (node.syntax_part == "string"):
        return ConcatString(SingleStr(node.text, node.source_start, node.source_end), node.source_start, node.source_end)

    elif node.syntax_part == "concatenated_string":
        children = node.children
        str_values = [
            (n.text, n.source_start, n.source_end)
            for n in children
        ]

        return ConcatString(to_sequence_string(str_values), node.source_start, node.source_end)

    elif (node.syntax_part == "integer"):
        return Integer(node.text, node.source_start, node.source_end)

    elif (node.syntax_part == "float"):
        return Float(node.text, node.source_start, node.source_end)

    elif (node.syntax_part == "true"):
        return True_(node.source_start, node.source_end)

    elif (node.syntax_part == "false"):
        return False_(node.source_start, node.source_end)

    elif (node.syntax_part == "none"):
        return None_(node.source_start, node.source_end)

    elif (node.syntax_part == "unary_operator"):
        children = node.children
        op_node = children[0]
        rand_node = children[1]
        op = from_generic_tree_to_unaryop(op_node)
        rand = from_generic_tree_to_expr(rand_node)
        return UnaryOp(op, rand, node.source_start, node.source_end)
    
    elif (node.syntax_part == "attribute"):
        children = node.children
        expr_node = children[0]
        expr = from_generic_tree_to_expr(expr_node)
        assert children[1].syntax_part == "."
        id_node = children[2]
        id = from_generic_tree_to_identifier(id_node)
        return Attribute(expr, id, node.source_start, node.source_end)

    elif (node.syntax_part == "subscript"):
        children = node.children
        target_node = children[0]
        target = from_generic_tree_to_expr(target_node)
        assert children[1].syntax_part == "["
        assert children[-1].syntax_part == "]"
        if len(children[2:-1]) > 1:

            comma_sep_nodes = children[2:-1]
            exprs = to_comma_exprs(comma_sep_nodes)

            slice = Tuple(exprs, children[1].source_start, children[-1].source_end)
            return Subscript(target, slice, node.source_start, node.source_end)

        else:
            slice_node = children[2]
            slice = from_generic_tree_to_expr(slice_node)
            return Subscript(target, slice, node.source_start, node.source_end)

    elif (node.syntax_part == "call"):
        children = node.children
        func_node = children[0]
        func = from_generic_tree_to_expr(func_node)

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
                from_generic_tree_to_expr(n)
                for n in pos_nodes
            ]

            keywords : list[keyword | None] = [
                from_generic_tree_to_keyword(n)
                for n in kw_nodes
            ]

            if pos_args or keywords: 
                seq_arg = to_arguments(pos_args, keywords)
                return CallArgs(func, seq_arg, node.source_start, node.source_end)
            else:
                return Call(func, node.source_start, node.source_end)

        elif args_node.syntax_part == "generator_expression":
            return CallArgs(func, to_arguments([from_generic_tree_to_expr(args_node)], []), node.source_start, node.source_end)

        else:
            return node_error(args_node)

    elif (node.syntax_part == "list"):

        exprs = to_comma_exprs(node.children[1:-1])
        if exprs:
            return List(exprs, node.source_start, node.source_end)
        else:
            return EmptyList(node.source_start, node.source_end)

    elif (node.syntax_part == "list_comprehension"):
        children = node.children[1:-1]
        expr = from_generic_tree_to_expr(children[0])

        constraint_nodes = children[1:]

        constraints = collapse_constraint_nodes(constraint_nodes)

        return ListComp(
            expr, 
            (
                to_comprehension_constraints(constraints)
                if constraints else
                None
            ),
            node.source_start, node.source_end
        )

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
                    from_generic_tree_to_expr(child_node.children[0]), 
                    from_generic_tree_to_expr(child_node.children[2]),
                    child_node.children[0].source_start,
                    child_node.children[2].source_end,

                )
                if is_pair(child_node) else

                (assert_splat(child_node), 
                make_DictionarySplatFields(from_generic_tree_to_expr(child_node.children[1]),
                    child_node.children[1].source_start,
                    child_node.children[1].source_end,
                ))[-1]

            )
            for child_node in children
        ]

        if items:
            return Dictionary(to_dictionary_content(items), node.source_start, node.source_end)
        else:
            return EmptyDictionary(node.source_start, node.source_end)

    elif node.syntax_part == "dictionary_comprehension":
        children = node.children[1:-1]
        pair_node = children[0]
        assert pair_node.syntax_part == "pair"
        pair = pair_node.children
        key = from_generic_tree_to_expr(pair[0])
        assert pair[1].syntax_part == ":"
        value = from_generic_tree_to_expr(pair[2])

        constraint_nodes = children[1:]
        constraints = collapse_constraint_nodes(constraint_nodes)

        return DictionaryComp(
            key, value, (
                to_comprehension_constraints(constraints)
                if constraints else
                None
            ),
            node.source_start, node.source_end
        )

    elif (node.syntax_part == "set"):
        exprs = to_comma_exprs(node.children[1:-1])
        return Set(exprs, node.source_start, node.source_end)

    elif (node.syntax_part == "set_comprehension"):
        children = node.children[1:-1]
        expr = from_generic_tree_to_expr(children[0])

        constraint_nodes = children[1:]
        constraints = collapse_constraint_nodes(constraint_nodes)
        return SetComp(expr, 
            to_comprehension_constraints(constraints)
            if constraints else
            None, node.source_start, node.source_end
        )


    elif (node.syntax_part == "generator_expression"):
        children = node.children[1:-1]
        expr = from_generic_tree_to_expr(children[0])

        constraint_nodes = children[1:]
        constraints = collapse_constraint_nodes(constraint_nodes)
        return GeneratorExp(expr, 
            to_comprehension_constraints(constraints)
            if constraints else
            None, node.source_start, node.source_end
        )

    elif (node.syntax_part == "tuple"):

        if (node.children[1:-1]):
            exprs = to_comma_exprs(node.children[1:-1])
            return Tuple(exprs, node.source_start, node.source_end)
        else:
            return EmptyTuple(node.source_start, node.source_end)

    elif (node.syntax_part == "expression_list"):
        exprs = to_comma_exprs(node.children[1:-1])
        return Tuple(exprs, node.source_start, node.source_end)

    
    elif (node.syntax_part == "parenthesized_expression"):
        children = node.children[1:-1]
        split_index = next(
            i for i, n in enumerate(children)
            if n.syntax_part != "comment"
        ) 
        pre_comment = merge_comments(children[0:split_index])
        post_comment = merge_comments(children[split_index + 1:])
        expr_node = children[split_index] 

        return ParenExpr(pre_comment, from_generic_tree_to_expr(expr_node), post_comment, node.source_start, node.source_end)

    elif (node.syntax_part == "ellipsis"):
        return Ellip(node.source_start, node.source_end) 

    elif (node.syntax_part == "list_splat"):
        children = node.children
        assert children[0].syntax_part == "*"
        expr_node = children[1]
        expr = from_generic_tree_to_expr(expr_node)
        return Starred(expr, node.source_start, node.source_end)

    elif (node.syntax_part == "list_splat_pattern"):
        children = node.children
        assert children[0].syntax_part == "*"
        expr_node = children[1]
        expr = from_generic_tree_to_expr(expr_node)
        return Starred(expr, node.source_start, node.source_end)

    elif (node.syntax_part == "tuple_pattern"):
        exprs = to_comma_exprs(node.children[1:-1])
        return Tuple(exprs, node.source_start, node.source_end)

    elif (node.syntax_part == "list_pattern"):
        exprs = to_comma_exprs(node.children[1:-1])
        return List(exprs, node.source_start, node.source_end)

    elif (node.syntax_part == "pattern_list"):
        exprs = to_comma_exprs(node.children[1:-1])
        return Tuple(exprs, node.source_start, node.source_end)

    elif (node.syntax_part == "yield"):

        children = node.children

        assert children[0].syntax_part == "yield"
        is_yield_from = (
            len(children) > 1 and
            children[1].syntax_part == "from"
        )

        if is_yield_from:
            expr = from_generic_tree_to_expr(children[2])
            return YieldFrom(expr, node.source_start, node.source_end)
        else:
            expr = from_generic_tree_to_expr(children[1])
            return Yield(expr, node.source_start, node.source_end)

    elif node.syntax_part == "comparison_operator":
        left = from_generic_tree_to_expr(node.children[0])
        (rators, rands) = split_rators_and_rands([n for n in reversed(node.children[1:])])
        assert len(rators) == len(rands)
        comp_rights = [
            CompareRight(rators[i], rands[i], unguard_cmp_rator(rators[-1]).source_start, node.source_end)
            for i, _ in enumerate(rators)
        ]
        return Compare(left, to_comparisons(comp_rights), node.source_start, node.source_end)

    elif (node.syntax_part == "not_operator"):
        children = node.children
        assert children[0].syntax_part == "not"
        rand_node = children[1]
        op = Not(node.source_start, node.source_end) 
        rand = from_generic_tree_to_expr(rand_node)
        return UnaryOp(op, rand, node.source_start, node.source_end)

    elif node.syntax_part == "boolean_operator":
        children = node.children
        left_expr = from_generic_tree_to_expr(children[0])
        op = from_generic_tree_to_boolop(children[1])
        right_expr = from_generic_tree_to_expr(children[2])

        return BoolOp(left_expr, op, right_expr, node.source_start, node.source_end)
    elif node.syntax_part == "await":
        assert node.children[0].syntax_part == "await"
        expr = from_generic_tree_to_expr(node.children[1])
        return Await(expr, node.source_start, node.source_end)

    elif node.syntax_part == "lambda":
        assert node.children[0].syntax_part == "lambda"
        if len(node.children) == 3:
            params = NoParam(node.source_start, node.source_end)
            body = from_generic_tree_to_expr(node.children[2])
            return Lambda(params, body, node.source_start, node.source_end)
        else:
            params = from_generic_tree_to_parameters(node.children[1])
            assert node.children[2].syntax_part == ":"
            body = from_generic_tree_to_expr(node.children[3])
            return Lambda(params, body, node.source_start, node.source_end)

    elif node.syntax_part == "conditional_expression":
        children = node.children
        true_expr = from_generic_tree_to_expr(children[0])
        assert children[1].syntax_part == "if"
        cond_expr = from_generic_tree_to_expr(children[2])
        assert children[3].syntax_part == "else"
        false_expr = from_generic_tree_to_expr(children[4])
        return IfExp(true_expr, cond_expr, false_expr, node.source_start, node.source_end)

    elif node.syntax_part == "named_expression":
        children = node.children
        target_expr = from_generic_tree_to_expr(children[0])
        assert children[1].syntax_part == ":="
        value_expr = from_generic_tree_to_expr(children[2])
        return AssignExpr(target_expr, value_expr, node.source_start, node.source_end)

    elif node.syntax_part == "type":
        return from_generic_tree_to_expr(node.children[0])

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
            SomeExpr(from_generic_tree_to_expr(left_node), left_node.source_start, left_node.source_end)
            if left_node else

            NoExpr(node.source_start, node.source_start)
        )

        right = (
            SomeExpr(from_generic_tree_to_expr(right_node), right_node.source_start, right_node.source_end)
            if right_node else
            NoExpr(left_node.source_end, left_node.source_end)
            if left_node else
            NoExpr(node.source_start, node.source_start)
        )

        step = (
            SomeExpr(from_generic_tree_to_expr(step_node), step_node.source_start, step_node.source_end)
            if step_node else
            NoExpr(right_node.source_end, right_node.source_end)
            if right_node else
            NoExpr(left_node.source_end, left_node.source_end)
            if left_node else
            NoExpr(node.source_start, node.source_start)
        )

        return Slice(left, right, step, node.source_start, node.source_end)

    else:
        # keyword_identifier / not sure if this is actually ever used
        return node_error(node)



def from_generic_tree_to_keyword(node) -> keyword | None:
    children = node.children

    if (node.syntax_part == "keyword_argument"):
        key_node = children[0]
        assert children[1].syntax_part == "="
        value_node = children[2]

        key_id = from_generic_tree_to_identifier(key_node)
        value_expr = from_generic_tree_to_expr(value_node)
        return NamedKeyword(key_id, value_expr, node.source_start, node.source_end)

    elif (node.syntax_part == "dictionary_splat"):
        assert children[0].syntax_part == "**" 
        value_expr = from_generic_tree_to_expr(children[1])
        return SplatKeyword(value_expr, node.source_start, node.source_end)

    else:
        return node_error(node)



def from_generic_tree_to_Param(node : GenericNode) -> Param | None:

    if node.syntax_part == "identifier":
        id = from_generic_tree_to_identifier(node)
        return Param(
            id, 
            NoParamAnno(node.source_start, node.source_start), 
            NoParamDefault(node.source_start, node.source_start), 
            node.source_start, node.source_end
        )

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

        id = from_generic_tree_to_identifier(id_node)
        assert node.children[1].syntax_part == ":"
        type_anno_node = node.children[2]
        type_anno = from_generic_tree_to_expr(type_anno_node)
        return Param(id, 
            SomeParamAnno(type_anno, type_anno_node.source_start, type_anno_node.source_end), 
            NoParamDefault(type_anno_node.source_end, type_anno_node.source_end), 
            node.source_start, node.source_end
        )

    elif node.syntax_part == "default_parameter":
        id = from_generic_tree_to_identifier(node.children[0])
        assert node.children[1].syntax_part == "="
        default_expr_node = node.children[2]
        default_expr = from_generic_tree_to_expr(default_expr_node)
        return Param(id, 
            NoParamAnno(node.source_start, node.source_start), 
            SomeParamDefault(default_expr, default_expr_node.source_start, default_expr_node.source_start), 
            node.source_start, node.source_end
        )

    elif node.syntax_part == "typed_default_parameter":
        id = from_generic_tree_to_identifier(node.children[0])
        assert node.children[1].syntax_part == ":"
        type_anno_node = node.children[2]
        type_anno = from_generic_tree_to_expr(node.children[2])
        assert node.children[3].syntax_part == "="
        default_expr_node = node.children[4]
        default_expr = from_generic_tree_to_expr(default_expr_node)
        return Param(
            id, 
            SomeParamAnno(type_anno, type_anno_node.source_start, type_anno_node.source_end), 
            SomeParamDefault(default_expr, default_expr_node.source_start, default_expr_node.source_start), 
            node.source_start, node.source_end
        )

    elif node.syntax_part == "list_splat_pattern":
        assert node.children[0].syntax_part == "*"
        id_node = node.children[1]
        id = from_generic_tree_to_identifier(id_node)
        return Param(
            id, 
            NoParamAnno(id_node.source_end, id_node.source_end), 
            NoParamDefault(id_node.source_end, id_node.source_end),
            node.source_start, node.source_end
        )

    elif node.syntax_part == "dictionary_splat_pattern":
        assert node.children[0].syntax_part == "**"
        id_node = node.children[1]
        id = from_generic_tree_to_identifier(id_node)
        return Param(
            id, 
            NoParamAnno(id_node.source_end, id_node.source_end), 
            NoParamDefault(id_node.source_end, id_node.source_end),
            node.source_start, node.source_end
        )

    elif node.syntax_part == "tuple_pattern":
        obsolete(node)
    else:
        return node_error(node)


def from_generic_tree_to_parameters(node : GenericNode) -> parameters | None:

    if node.syntax_part == "lambda_parameters":
        lambda_params = [
            from_generic_tree_to_Param(param_node)
            for param_node in node.children
            if param_node.syntax_part != ","
        ]

        return to_parameters([], lambda_params, None, [], None, node.source_start, node.source_end)

    elif node.syntax_part == "parameters":

        children = [
            child
            for child in (
                node.children
                if node.syntax_part == "lambda_parameters"

                else node.children[1:-1]
            )
            if child.syntax_part != ","
        ]



        positional_separator_index = next(
            (
                i 
                for i, n in enumerate(children)
                if n.syntax_part == "positional_separator"
            ),
            -1 
        )

        list_splat_index = next(
            (
                i 
                for i, n in enumerate(children)
                if (
                    n.syntax_part == "list_splat_pattern" or 
                    (
                        n.syntax_part == "typed_parameter" and
                        n.children[0].syntax_part == "list_splat_pattern"
                    ) or
                    n.syntax_part == "keyword_separator"
                )

            ),
            -1 
        )

        dictionary_splat_index = next(
            (
                i 
                for i, n in enumerate(children)
                if (
                    n.syntax_part == "dictionary_splat_pattern" or 
                    (
                        n.syntax_part == "typed_parameter" and
                        n.children[0].syntax_part == "dictionary_splat_pattern"
                    )
                )
            ),
            -1 
        )

        pos_param_nodes = (
            children[0:positional_separator_index]
            if positional_separator_index > -1 else
            []
        )

        (pos_kw_param_nodes, list_splat_node, kw_nodes, dictionary_splat_node) = (

            (
                children[positional_separator_index + 1:list_splat_index], 
                children[list_splat_index], 
                children[list_splat_index + 1: dictionary_splat_index], 
                children[dictionary_splat_index]
            )
            if (list_splat_index >= 0 and dictionary_splat_index >= 0) else 
            
            (
                children[positional_separator_index + 1:list_splat_index], 
                children[list_splat_index], 
                children[list_splat_index + 1:], 
                None
            )
            if list_splat_index >= 0 and dictionary_splat_index < 0 else 
            
            (
                children[positional_separator_index + 1:-1], 
                None,
                [],
                children[dictionary_splat_index]
            )
            if list_splat_index < 0 and dictionary_splat_index >= 0 else 

            (
                children[positional_separator_index + 1:], 
                None,
                [],
                None
            )
        )

        pos_params = [
            from_generic_tree_to_Param(n)
            for n in pos_param_nodes
        ]

        pos_kw_params = [
            from_generic_tree_to_Param(n)
            for n in pos_kw_param_nodes
        ]


        list_splat_param = (
            None
            if (
                not list_splat_node or 
                (
                    list_splat_node.syntax_part == "list_splat_pattern" and 
                    len(list_splat_node.children) == 0
                ) or 
                list_splat_node.syntax_part == "keyword_separator"
            ) else 

            from_generic_tree_to_Param(list_splat_node)
        )

        kw_params = [
            from_generic_tree_to_Param(n)
            for n in kw_nodes
        ]

        dictionary_splat_param = from_generic_tree_to_Param(dictionary_splat_node) if dictionary_splat_node else None

        return to_parameters(pos_params, pos_kw_params, list_splat_param, kw_params, dictionary_splat_param, 
            node.source_start, node.source_end
        )


    else:
        return node_error(node)



def from_generic_tree_to_stmts(node : GenericNode, decorators : decorators | None = None) -> list[stmt | None]: 

    if not decorators:
        decorators = NoDec(node.source_start, node.source_start)

    decorators_start, decorators_end = match_decorators(decorators, past.DecoratorsHandlers(
        case_ConsDec = lambda d : (d.source_start, d.source_end),
        case_NoDec = lambda d : (d.source_start, d.source_end),
    ))

    if (node.syntax_part == "import_statement"):
        children = node.children
        assert children[0].syntax_part == "import"
        return [Import(
            to_sequence_import_name([
                from_generic_tree_to_import_name(child)
                for child in children[1:]
                if child.syntax_part != ","
            ]),
            node.source_start, node.source_start
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
                    (prefix + from_generic_tree_to_identifier(rel_import_node.children[1]))
                    if len(rel_import_node.children) == 2 else
                    (prefix)
                )
            )[-1]
            if children[1].syntax_part == "relative_import" else

            (from_generic_tree_to_identifier(children[1]))
        )

        assert children[2].syntax_part == "import"
        if len(children) == 4 and children[3].syntax_part == "wildcard_import":
            return [ImportWildCard(module, node.source_start, node.source_start)]

        else:

            import_list = (
                children[4:-1]
                if children[3].syntax_part == "(" else

                children[3:]
            )

            aliases = to_sequence_import_name([
                from_generic_tree_to_import_name(n) 
                for n in import_list
                if n.syntax_part != ","
            ])
            return [ImportFrom(module, aliases, node.source_start, node.source_start)]

    elif (node.syntax_part == "future_import_statement"):
        children = node.children
        assert children[0].syntax_part == "from"
        id = ("__future__")
        assert children[2].syntax_part == "import"

        import_list = (
            children[4:-1]
            if children[3].syntax_part == "(" else

            children[3:]
        )

        names = to_sequence_import_name([
            from_generic_tree_to_import_name(n) 
            for n in import_list 
            if n.syntax_part != ","
        ])
        return [ImportFrom(id, names, node.source_start, node.source_start)]

    elif (node.syntax_part == "assert_statement"):
        children = node.children
        assert children[0].syntax_part == "assert"
        test_expr = from_generic_tree_to_expr(children[1])

        if len(children) == 2:
            msg = from_generic_tree_to_expr(children[1])
            return [ AssertMsg(test_expr, msg, node.source_start, node.source_start) ]
        else:
            return [ Assert(test_expr, node.source_start, node.source_start) ]


    elif (node.syntax_part == "print_statement"):
        children = node.children
        assert children[0].syntax_part == "print"

        arg_index = 1
        arg_keywords : list[keyword | None] = []

        chev_node = children[1]
        if chev_node.syntax_part == "chevron":
            arg_index = 2
            arg_keywords = [make_NamedKeyword("file", Name(
                "sys.stderr", 
                chev_node.source_start, chev_node.source_start
            ), node.source_start, node.source_start)]
        else:
            arg_index = 1

        arg_nodes = [c for c in children[arg_index:] if c.syntax_part != ","]
        arg_exprs = [
            from_generic_tree_to_expr(node)
            for node in arg_nodes
        ]

        return [Expr(
            CallArgs(
                Name("print",
                    children[0].source_start,
                    children[0].source_end,
                ), 
                to_arguments(arg_exprs, arg_keywords),
                node.source_start, node.source_start
            ), 
            node.source_start, node.source_start
        )]

    elif (node.syntax_part == "expression_statement"):
        children = node.children

        if (len(children) > 1):
            return [
                Expr(from_generic_tree_to_expr(expr_node), expr_node.source_start, expr_node.source_start)
                for expr_node in children
                if expr_node.syntax_part != ","
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
                            return extract_targets_source(remainder_node, targets + [from_generic_tree_to_expr(target_node)])
                        else:
                            return (targets, from_generic_tree_to_expr(node))

                    (targets, source) = extract_targets_source(estmt_node)

                    return [Assign(to_target_exprs(targets), source, estmt_node.source_start, estmt_node.source_end)]

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
                        left_expr = from_generic_tree_to_expr(left)
                        typ_expr = from_generic_tree_to_expr(typ)
                        right_expr = from_generic_tree_to_expr(right) if right else None
                        if right_expr:
                            return [
                                AnnoAssign(
                                    left_expr, typ_expr, right_expr,
                                    estmt_node.source_start, estmt_node.source_end
                                )
                            ]
                        else:
                            return [
                                AnnoDeclar(left_expr, typ_expr, estmt_node.source_start, estmt_node.source_end)
                            ]
                    elif right:
                        right_expr = from_generic_tree_to_expr(right)

                        left_exprs = SingleTargetExpr(
                            from_generic_tree_to_expr(left), 
                            left.source_start, 
                            left.source_end
                        )
                        return [
                            Assign(left_exprs, right_expr, estmt_node.source_start, estmt_node.source_end)
                        ] 

                    else:
                        return [node_error(node)]


            elif (estmt_node.syntax_part == "augmented_assignment"):

                estmt_children = estmt_node.children

                left = estmt_children[0]
                op = estmt_children[1]
                right = estmt_children[2]

                left_expr = from_generic_tree_to_expr(left)
                oper = from_generic_tree_to_bin_rator(op)
                right_expr = from_generic_tree_to_expr(right)
                return [
                    AugAssign(left_expr, oper, right_expr, estmt_node.source_start, estmt_node.source_end)
                ]

            else:
                return [Expr(from_generic_tree_to_expr(estmt_node), estmt_node.source_start, estmt_node.source_end)]
    elif (node.syntax_part == "return_statement"):
        children = node.children
        assert children[0].syntax_part == "return"
        if len(children) == 2:
            expr = from_generic_tree_to_expr(children[1])
            return [
                ReturnSomething(expr, node.source_start, node.source_end)
            ]
        else:
            return [Return(node.source_start, node.source_end)]




    elif (node.syntax_part == "delete_statement"):
        assert node.children[0].syntax_part == "del"
        child = node.children[1]
        if (child.syntax_part == "expression_list"):

            exprs = to_comma_exprs(child.children)
            return [ Delete(exprs, node.source_start, node.source_end) ]
        else:
            exprs = SingleExpr('', from_generic_tree_to_expr(child), '', child.source_start, child.source_end)
            return [ Delete(exprs, node.source_start, node.source_end) ]

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

        exc_expr = from_generic_tree_to_expr(exc) if exc else None
        cause_expr = from_generic_tree_to_expr(cause) if cause else None
        if (exc_expr and cause_expr):
            return [ RaiseFrom(exc_expr, cause_expr, node.source_start, node.source_end) ]
        elif (exc_expr):
            return [ RaiseExc(exc_expr, node.source_start, node.source_end) ]
        else:
            return [ Raise(node.source_start, node.source_end) ]


    elif (node.syntax_part == "pass_statement"):
        return [
            Pass(node.source_start, node.source_end)
        ]

    elif (node.syntax_part == "break_statement"):
        return [
            Break(node.source_start, node.source_end)
        ]

    elif (node.syntax_part == "continue_statement"):
        return [
            Continue(node.source_start, node.source_end)
        ]

    elif (node.syntax_part == "global_statement"):
        children = node.children
        assert children[0].syntax_part == "global"
        ids = to_sequence_var([
            (from_generic_tree_to_identifier(id_node), id_node.source_start, id_node.source_end)
            for id_node in children[1:]
            if id_node.syntax_part != ","
        ])

        return [
            Global(ids, node.source_start, node.source_end)
        ]

    elif (node.syntax_part == "nonlocal_statement"):
        children = node.children
        assert children[0].syntax_part == "nonlocal"
        ids = to_sequence_var([
            (from_generic_tree_to_identifier(id_node), id_node.source_start, id_node.source_end)
            for id_node in children[1:]
            if id_node.syntax_part != ","
        ])

        return [
            Nonlocal(ids, node.source_start, node.source_end)
        ]

    elif (node.syntax_part == "if_statement"):
        children = node.children
        assert children[0].syntax_part == "if"
        cond_node = children[1]
        assert children[2].syntax_part  == ":"

        comment_nodes = [
            child
            for child in children[3:]
            if child.syntax_part == "comment"
        ]
        comment_text = merge_comments(comment_nodes)
        block_node = children[3 + len(comment_nodes)]


        def to_else_content(else_node : GenericNode) -> tuple[str, statements | None]:
            assert else_node.syntax_part == "else_clause"

            else_children = else_node.children
            assert else_children[0].syntax_part == "else"
            assert else_children[1].syntax_part == ":"
            comment_text = merge_comments(else_children[2:-1])
            block_node_ = else_children[-1]
            block_children = block_node_.children
            return comment_text, to_statements([
                stmt 
                for stmt_node in block_children
                for stmt in from_generic_tree_to_stmts(stmt_node)
            ])

        def to_elif_content(elif_node : GenericNode) -> tuple[expr | None, str, statements | None]:
            assert (elif_node.syntax_part == "elif_clause")
            else_children = elif_node.children
            assert else_children[0].syntax_part == "elif"
            cond_node = else_children[1]
            assert else_children[2].syntax_part == ":"

            (comment_text, block_node_) = (merge_comments(else_children[3:-1]), else_children[-1])

            block_children = block_node_.children
            return (
                from_generic_tree_to_expr(cond_node),
                comment_text,
                to_statements([
                    stmt 
                    for stmt_node in block_children
                    for stmt in from_generic_tree_to_stmts(stmt_node)
                ])
            )


        else_index = 3 + len(comment_nodes) + 1

        (else_block, else_nodes) = (

            (ElseCond(
                ElseBlock(*(to_else_content(children[-1])),
                    children[-1].source_start,
                    children[-1].source_end,
                ),
                node.source_start, node.source_end
            ), children[else_index:-1])
            if children[-1].syntax_part == "else_clause" else

            (NoCond(block_node.source_end, block_node.source_end), children[else_index:])
        )

        for n in reversed(else_nodes):
            (e, comment_text, sts) = to_elif_content(n)
            else_block = ElifCond(
                ElifBlock(e, comment_text, sts, n.source_start, n.source_end), 
                else_block,
                node.source_start, node.source_end
            )


        cond = from_generic_tree_to_expr(cond_node)
        block = to_statements([
            stmt
            for stmt_node in block_node.children
            for stmt in from_generic_tree_to_stmts(stmt_node)
        ])
        return [If(cond, comment_text, block, else_block, node.source_start, node.source_end)]
                


    elif(node.syntax_part == "for_statement"):
        children = node.children

        (is_async, children) = (
          (True, children[1:])
          if (children[0].syntax_part == "async") else
          (False, children)
        ) 


        assert children[0].syntax_part == "for"
        target_expr = from_generic_tree_to_expr(children[1])
        assert children[2].syntax_part == "in"
        iter_expr = from_generic_tree_to_expr(children[3])
        assert children[4].syntax_part == ":"
        comment_nodes = [
            child
            for child in children[5:]
            if child.syntax_part == "comment"
        ]
        comment_text = merge_comments(comment_nodes)
        block_node = children[5 + len(comment_nodes)]
        body_stmts = to_statements([
            stmt
            for stmt_node in block_node.children
            for stmt in from_generic_tree_to_stmts(stmt_node) 
        ])

        else_index = 5 + len(comment_nodes) + 1
        else_node = (
            children[else_index]
            if (len(children) == else_index + 1) 
            
            else None 
        )

        assert not else_node or else_node.syntax_part == "else_clause"

        assert not else_node or else_node.children[0].syntax_part == "else" 

        assert not else_node or else_node.children[1].syntax_part == ":" 

        else_comment_text = merge_comments(else_node.children[2:-1]) if else_node else '' 
        else_block_node = else_node.children[-1] if else_node else None 

        assert not else_block_node or else_block_node.syntax_part == "block"

        block_children = else_block_node.children if else_block_node else []


        if block_children:

            else_block = ElseBlock(
                else_comment_text,
                to_statements([
                    stmt
                    for stmt_node in block_children
                    for stmt in from_generic_tree_to_stmts(stmt_node) 
                ]), 
                else_block_node.source_start if else_block_node else node.source_start, 
                else_block_node.source_end if else_block_node else node.source_start
            )

            if is_async:
                return [
                    AsyncForElse(target_expr, iter_expr, comment_text, body_stmts, else_block, node.source_start, node.source_end)
                ]

            else:
                return [
                    ForElse(target_expr, iter_expr, comment_text, body_stmts, else_block, node.source_start, node.source_end)
                ]
        else:

            if is_async:
                return [
                    AsyncFor(target_expr, iter_expr, comment_text, body_stmts, node.source_start, node.source_end)
                ]

            else:
                return [
                    For(target_expr, iter_expr, comment_text, body_stmts, node.source_start, node.source_end)
                ]

    elif(node.syntax_part == "while_statement"):
        children = node.children
        assert children[0].syntax_part == "while"
        test_expr = from_generic_tree_to_expr(children[1])

        assert children[2].syntax_part == ":"
        comment_nodes = [
            child
            for child in children[5:]
            if child.syntax_part == "comment"
        ]
        comment_text = merge_comments(comment_nodes)
        block_node = children[3 + len(comment_nodes)]
        assert block_node.syntax_part == "block"
        body_stmts = to_statements([
            stmt
            for stmt_node in block_node.children 
            for stmt in from_generic_tree_to_stmts(stmt_node) 
        ])

        else_index = 3 + len(comment_nodes) + 1
        else_node = (
            children[else_index]
            if (len(children) == else_index + 1) 
            
            else None 
        )


        assert not else_node or else_node.syntax_part == "else_clause"

        assert not else_node or else_node.children[0].syntax_part == "else" 

        assert not else_node or else_node.children[1].syntax_part == ":" 

        else_comment_text = merge_comments(else_node.children[2:-1]) if else_node else '' 

        else_block_node = else_node.children[-1] if else_node else None 

        assert not else_block_node or else_block_node.syntax_part == "block"

        block_children = else_block_node.children if else_block_node else []


        if else_block_node:
            else_stmts = ElseBlock(
                else_comment_text,
                to_statements([
                    stmt
                    for stmt_node in block_children 
                    for stmt in from_generic_tree_to_stmts(stmt_node) 
                ]),
                else_block_node.source_start,
                else_block_node.source_end
            )

            return [
                WhileElse(test_expr, comment_text, body_stmts, else_stmts, node.source_start, node.source_end)
            ]
        else:
            return [
                While(test_expr, comment_text, body_stmts, node.source_start, node.source_end)
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
            for stmt in from_generic_tree_to_stmts(stmt_node) 
        ])

        except_clause_nodes = [
            n
            for n in children
            if n.syntax_part == "except_clause"
        ]

        except_handlers = (
            to_sequence_ExceptHandler([
                from_generic_tree_to_ExceptHandler(ec_node)
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
            assert else_clause_node.children[-1].syntax_part == "block"

        else_comment_text = merge_comments(else_clause_nodes[0].children[2:-1])

        else_stmts = (
            [] 
            if len(else_clause_nodes) == 0 else
            
            [
                stmt
                for else_clause_node in [else_clause_nodes[0]]
                for _ in [assert_else_clause(else_clause_node)]
                for else_block_node in [else_clause_node.children[-1]]
                for stmt_node in else_block_node.children
                for stmt in from_generic_tree_to_stmts(stmt_node)
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
            assert n.children[-1].syntax_part == "block"

        finally_comment_text = merge_comments(else_clause_nodes[0].children[2:-1])
        
        finally_stmts = (
            [] 
            if len(finally_clause_nodes) == 0 else

            [
                stmt
                for finally_clause_node in [finally_clause_nodes[0]] 
                for _ in [assert_finally_clause(finally_clause_node)]
                for block_node in [finally_clause_node.children[-1]] 
                for stmt_node in block_node.children
                for stmt in from_generic_tree_to_stmts(stmt_node)
            ]
        )


        if except_handlers and else_stmts and finally_stmts:
            else_clause_node = else_clause_nodes[0]
            finally_clause_node = finally_clause_nodes[0]
            return [
                TryElseFin(
                    try_stmts, 
                    except_handlers, 
                    ElseBlock(else_comment_text, to_statements(else_stmts),
                        else_clause_node.source_start,
                        else_clause_node.source_end,
                    ), 
                    FinallyBlock(finally_comment_text, to_statements(finally_stmts),
                        finally_clause_node.source_start,
                        finally_clause_node.source_end,
                    ),
                    node.source_start, node.source_end
                )
            ]

        elif except_handlers and else_stmts:
            else_clause_node = else_clause_nodes[0]
            return [
                TryElse(
                    try_stmts, except_handlers, 
                    ElseBlock(else_comment_text, to_statements(else_stmts),
                        else_clause_node.source_start,
                        else_clause_node.source_end,
                    ),
                    node.source_start, node.source_end
                )
            ]

        elif except_handlers and finally_stmts:
            finally_clause_node = finally_clause_nodes[0]
            return [
                TryExceptFin(
                    try_stmts, except_handlers, FinallyBlock(
                        finally_comment_text, 
                        to_statements(finally_stmts),
                        finally_clause_node.source_start,
                        finally_clause_node.source_end,
                    ),
                    node.source_start, node.source_end
                )
            ]

        elif finally_stmts:
            finally_clause_node = finally_clause_nodes[0]
            return [
                TryFin(
                    try_stmts, FinallyBlock(
                        finally_comment_text, 
                        to_statements(finally_stmts),
                        finally_clause_node.source_start,
                        finally_clause_node.source_end,
                    ),
                    node.source_start, node.source_end
                )
            ]

        elif except_handlers:
            return [
                Try(
                    try_stmts, except_handlers,
                    node.source_start, node.source_end
                )
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

        with_items = to_sequence_with_item([
            from_generic_tree_to_with_item(item_node)
            for item_node in with_clause_node.children
        ])


        assert children[2].syntax_part == ":"
        comment_text = merge_comments(children[3:-1])
        block_node = children[-1]
        assert block_node.syntax_part == "block"
        stmts = to_statements([
            stmt
            for stmt_node in block_node.children
            for stmt in from_generic_tree_to_stmts(stmt_node)
        ])

        if is_async:
            return [
                AsyncWith(
                    with_items, comment_text, stmts,
                    node.source_start, node.source_end
                )
            ]

        else:
            return [
                With(
                    with_items, comment_text, stmts,
                    node.source_start, node.source_end
                )
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
        name = from_generic_tree_to_identifier(name_node)

        params_node = children[2]
        param_group = from_generic_tree_to_parameters(params_node)

        (return_anno_node, comment_text, block_node) = (
            (children[4], merge_comments(children[6:-1]), children[-1])
            if children[3].syntax_part == "->" and children[5].syntax_part == ":" else

            (None, merge_comments(children[4:-1]), children[-1])
            if children[3].syntax_part == ":" else

            (None, '', None)
        )

        comment_text = (
            children[-1].text
            if children[-1].syntax_part == "comment" else
            ''
        )

        assert block_node

        return_anno = (
            SomeReturnAnno(from_generic_tree_to_expr(return_anno_node), node.source_start, node.source_end)
            if return_anno_node else

            NoReturnAnno(children[3].source_start, children[3].source_start)
        )

        body = to_statements([
            stmt
            for stmt_node in block_node.children
            for stmt in from_generic_tree_to_stmts(stmt_node)
        ])

        if is_async: 

            return [
                DecFunctionDef(
                    decorators,
                    AsyncFunctionDef(name, param_group, return_anno, comment_text, body,
                        node.source_start, node.source_end
                    ),
                    decorators_start, decorators_end
                )
            ]

        else:
            return [
                DecFunctionDef(
                    decorators, 
                    FunctionDef(name, param_group, return_anno, comment_text, body,
                        node.source_start, node.source_end
                    ),
                    decorators_start, decorators_end
                )
            ]


    elif (node.syntax_part == "class_definition"):
        children = node.children

        assert children[0].syntax_part == "class"

        name_node = children[1]
        name = from_generic_tree_to_identifier(name_node)

        (arguments_node, comment_text, block_node) = (
            (None, merge_comments(children[3:-1]), children[-1])
            if children[2].syntax_part == ":" else 
            (children[2], merge_comments(children[4:-1]), children[-1])
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
            from_generic_tree_to_expr(n)
            for n in base_nodes
        ]

        keywords = [
            from_generic_tree_to_keyword(n)
            for n in kw_nodes
        ]

        bases = to_bases(base_exprs, keywords, name_node.source_end, block_node.children[0].source_start)

        body_stmts = to_statements([
            stmt
            for n in block_node.children
            for stmt in from_generic_tree_to_stmts(n)
        ])

        return [
            DecClassDef(
                decorators,
                ClassDef(name, bases, comment_text, body_stmts,
                    node.source_start, node.source_end
                ),
                decorators_start, decorators_end
            )
        ]

    elif (node.syntax_part == "decorated_definition"):
        children = node.children
        dec_nodes = children[0:-1]

        def from_generic_tree_to_decorator(dec_node : GenericNode) -> decorator:
            if dec_node.syntax_part == "decorator":
                assert dec_node.children[0].syntax_part == "@"
                expr_node = dec_node.children[1] 
                return ExprDec(from_generic_tree_to_expr(expr_node), expr_node.source_start, expr_node.source_end)
            else:
                assert dec_node.syntax_part == "comment"
                return CmntDec(dec_node.text, dec_node.source_start, dec_node.source_end)

        def_node = children[-1]

        decs = to_decorators([
            from_generic_tree_to_decorator(dec_node)
            for dec_node in dec_nodes
        ], def_node.source_start, def_node.source_start)

        return from_generic_tree_to_stmts(def_node, decorators = decs)

    elif (node.syntax_part == "comment"):
        return [Comment(node.text, node.source_start, node.source_end)]

    else:
        # exec_statement for Python 2
        # print_statement for Python 2
        return [node_error(node)]