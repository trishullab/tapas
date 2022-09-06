from __future__ import annotations

from dataclasses import dataclass
from re import I
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


def to_bases(base_nodes : list[GenericNode], kws : keywords | None, default_start : int, default_end : int) -> bases:

    only_comments = all(n.syntax_part == "comment" for n in base_nodes)
    if only_comments and not kws:
        comment = merge_comments(base_nodes) 
        return NoBases(comment, default_start, default_end)
    else:

        to_comment_triplets(base_nodes)

        start_node, end_node = (
            (base_nodes[0], kws)
            if bases and kws else
            (base_nodes[0], base_nodes[-1])
            if bases else
            (kws, kws)
        )

        start = (
            start_node.source_start
            if isinstance(start_node, GenericNode) else
            unguard_keywords(start_node).source_end
            if isinstance(start_node, keywords) else
            0
        )
        end = (
            end_node.source_start
            if isinstance(end_node, GenericNode) else
            unguard_keywords(end_node).source_end
            if isinstance(end_node, keywords) else
            0
        )


        return SomeBases(to_sequence_base(base_nodes, kws), start, end)


def to_sequence_base(base_nodes : list[GenericNode], keywords : keywords | None) -> bases_a | None:
    if  base_nodes or keywords:

        trips = to_comment_triplets(base_nodes)


        if keywords:

            result = KeywordBases(keywords, 
                unguard_keywords(keywords).source_start,
                unguard_keywords(keywords).source_end,
            )

        else:

            (pre, n, post) = trips[-1]
            b = from_generic_tree_to_expr(n) 

            result = SingleBase(pre, b, post,
                unguard_expr(b).source_start if b else 0,
                unguard_expr(b).source_end if b else 0,
            )
            trips = trips[:-1]


        for pre, n, post in reversed(trips):
            b = from_generic_tree_to_expr(n) 
            result = ConsBase(pre, b, post, result,
                unguard_expr(b).source_start if b else 0,
                unguard_expr(b).source_end if b else 0
            )

        return result
    else:
        return None



def to_parameters(
    pos_sections : list[list[GenericNode]], 
    pos_kw_sections : list[list[GenericNode]], 
    list_splat_section : list[GenericNode] | None, 
    kw_sections : list[list[GenericNode]], 
    dictionary_splat_section : list[GenericNode] | None,
    default_start : int,
    default_end : int,
) -> parameters:

    if not (
        pos_sections or pos_kw_sections or list_splat_section or kw_sections or dictionary_splat_section
    ):
        return NoParam(default_start, default_end)
    elif pos_sections:
        return ParamsA(to_parameters_a(
            pos_sections, pos_kw_sections, list_splat_section, kw_sections, dictionary_splat_section
        ), default_start, default_end)
    else:
        return ParamsB(to_parameters_b(
            pos_kw_sections, list_splat_section, kw_sections, dictionary_splat_section
        ), default_start, default_end)


def to_parameters_d(
    kw_sections : list[list[GenericNode]], 
    dictionary_splat_section : list[GenericNode] | None
) -> parameters_d:
    assert kw_sections

    kw_section = kw_sections[-1]
    (kw_pre, kw_node, kw_post) = to_comment_triple(kw_section)
    kw_param = from_generic_tree_to_Param(kw_node)

    if dictionary_splat_section:

        (dpre, dnode, dpost) = to_comment_triple(dictionary_splat_section)
        dparam = from_generic_tree_to_Param(dnode)

        result = TransKwParam(kw_pre, kw_param, kw_post, dpre, dparam, dpost,
            kw_param.source_start if kw_param else 0,
            dparam.source_start if dparam else 0
        )

        kw_sections = kw_sections[:-1]

    else:
        result = SingleKwParam(kw_pre, kw_param, kw_post,
            kw_param.source_start if kw_param else 0,
            kw_param.source_end if kw_param else 0,
        )
        kw_sections =  kw_sections[:-1]

    for section in reversed(kw_sections):
        (pre, n, post) = to_comment_triple(section)
        p = from_generic_tree_to_Param(n)
        result = ConsKwParam(pre, p, post, result,
            p.source_start if p else 0,
            result.source_end,
        )

    return result


def to_parameters_c(
    list_splat_section : list[GenericNode] | None, 
    kw_sections : list[list[GenericNode]], 
    dictionary_splat_section : list[GenericNode] | None,
) -> parameters_c:

    pre_sep, list_splat_node, post_sep = (
        to_comment_triple(list_splat_section)
        if list_splat_section else
        '', None, ''
    )

    if not list_splat_node or list_splat_node.syntax_part == "keyword_separator" :
        # just a separator; no bundling of element into list

        if not kw_sections and dictionary_splat_section:

            (pre, dictionary_splat_node, post) = to_comment_triple(dictionary_splat_section)
            source_start = dictionary_splat_node.source_start
            source_end = dictionary_splat_node.source_end
            dictionary_bundle_param = from_generic_tree_to_Param(dictionary_splat_node)

            return DictionaryBundleParam(
                pre, dictionary_bundle_param, post,
                source_start, source_end
            )
        else:
            #  not list_splat_param and kw_params:
            params_d = to_parameters_d(kw_sections, dictionary_splat_section)
            return ParamsD(params_d,
                unguard_parameters_d(params_d).source_start if params_d else 0, 
                unguard_parameters_d(params_d).source_end if params_d else 0
            )

    else:

        assert list_splat_node.syntax_part == "list_splat_pattern" 
        list_bundle_param = from_generic_tree_to_Param(list_splat_node)

        if kw_sections:
            source_start = list_splat_section.source_start
            source_end = (
                dictionary_splat_section.source_end 
                if dictionary_splat_section else
                kw_sections[-1].source_end 
                if kw_sections[-1] else 0
            )
            return TransTupleBundleParam(list_splat_section, 
                to_parameters_d(kw_sections, dictionary_splat_section),
                source_start, source_end
            )
        elif not kw_sections and not dictionary_splat_section:
            source_start = list_splat_section.source_start
            source_end = list_splat_section.source_end if list_splat_section else 0
            return SingleTupleBundleParam(list_splat_section, 
                source_start, source_end
            )
        elif not kw_sections and dictionary_splat_section:
            source_start = list_splat_section.source_start
            source_end =  dictionary_splat_section.source_end
            return DoubleBundleParam(list_splat_section, dictionary_splat_section,
                source_start, source_end
            )



def to_parameters_b(
    pos_kw_sections : list[list[GenericNode]], 
    list_splat_section : list[GenericNode] | None, 
    kw_sections : list[list[GenericNode]], 
    dictionary_splat_section : list[GenericNode] | None,
) -> parameters_b:

    pos_kw_trips = [to_comment_triple(section) for section in pos_kw_sections]

    if (list_splat_section or kw_sections or dictionary_splat_section):

        params_c = to_parameters_c(list_splat_section, kw_sections, dictionary_splat_section)
        result = ParamsC(params_c,
            unguard_parameters_c(params_c).source_start,
            unguard_parameters_c(params_c).source_end,
        ) 
    else:
        assert pos_kw_trips
        (pre, n, post) = pos_kw_trips[-1]
        p = from_generic_tree_to_Param(n)

        result = SinglePosKeyParam(pre, p, post,
            p.source_start if p else 0,
            p.source_end if p else 0,
        )

        pos_kw_trips = pos_kw_trips[:-1]

    for pre, n, post in reversed(pos_kw_trips):
        p = from_generic_tree_to_Param(n)
        result = ConsPosKeyParam(pre, p, post, result,
            p.source_start if p else 0,
            result.source_end if result else 0
        )

    return result


def to_parameters_a(
    pos_sections : list[list[GenericNode]], 
    pos_kw_sections : list[list[GenericNode]], 
    list_splat_section : list[GenericNode] | None, 
    kw_sections : list[list[GenericNode]], 
    dictionary_splat_section : list[GenericNode] | None
) -> parameters_a:
    assert len(pos_sections) >= 2

    pos_triples = [to_comment_triple(section) for section in pos_sections]
    (pre_sep, _, post_sep) = pos_triples[-1]
    (pre, pos_node, post) = pos_triples[-2]
    pos_param = from_generic_tree_to_Param(pos_node)
    

    result = (
        (
            params_b := to_parameters_b(pos_kw_sections, list_splat_section, kw_sections, dictionary_splat_section),
            TransPosParam(pre, pos_param, post, pre_sep, post_sep, params_b,
                pos_param.source_start if pos_param else 0,
                unguard_parameters_b(params_b).source_end
            )
        )[-1]
        if (pos_kw_sections or list_splat_section or kw_sections or dictionary_splat_section) else

        SinglePosParam(pre, pos_param, post, pre_sep, post_sep,
            pos_param.source_start if pos_param else 0,
            pos_param.source_end if pos_param else 0,
        )
    )

    for (pre, n, post) in reversed(pos_triples[:-2]):
        pp = from_generic_tree_to_Param(n)
        result = ConsPosParam(pre, pp, post, result,
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

def to_dictionary_item(node : GenericNode) -> dictionary_item:
    def is_pair(pair): 
        return pair.syntax_part == "pair"

    def assert_splat(dsplat): 
        assert dsplat.syntax_part == "dictionary_splat" and dsplat.children[0].syntax_part == "**" 

    colon_index = next(
        i
        for i, n in enumerate(node.children)
        if n.syntax_part == ":"
    )

    pre_comment = merge_comments(node.children[1:colon_index])
    post_comment = merge_comments(node.children[colon_index + 1:-1])

    return (
        make_Field(
            from_generic_tree_to_expr(node.children[0]), 
            pre_comment, post_comment,
            from_generic_tree_to_expr(node.children[-1]),
            node.children[0].source_start,
            node.children[-1].source_end,

        )
        if is_pair(node) else

        (assert_splat(node), 
        make_DictionarySplatFields(from_generic_tree_to_expr(node.children[1]),
            node.children[1].source_start,
            node.children[1].source_end,
        ))[-1]
    )

def to_dictionary_content(nodes : list[GenericNode]) -> dictionary_content:
    item_trips = [to_comment_triple(section) for section in to_sections(nodes)]
    assert item_trips

    pre, node, post = item_trips[-1]
    item = to_dictionary_item(node)
    result = SingleDictionaryItem(pre, item, post,
        unguard_dictionary_item(item).source_start,
        unguard_dictionary_item(item).source_end,
    )
    for pre, node, post in reversed(item_trips[:-1]):
        f = to_dictionary_item(node)
        result = ConsDictionaryItem(pre, f, post, result,
            unguard_dictionary_item(f).source_start,
            result.source_end
        )

    return result

def to_comprehension_constraints(constraint_nodes : list[GenericNode]) -> comprehension_constraints:
    cs = collapse_constraint_nodes(constraint_nodes)
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


def to_decorators(nodes : list[GenericNode], base_start : int, base_end : int) -> decorators:
    result = NoDec(base_start, base_end)
    for node in reversed(nodes):
        d = from_generic_tree_to_decorator(node)
        result = ConsDec(d, result,
            unguard_decorator(d).source_start if d else 0,
            result.source_end
        )

    return result 


def to_comment_triple(section : list[GenericNode]) -> tuple[str, GenericNode, str]:
    split_index = next(
        i for i, n in enumerate(section)
        if n.syntax_part != "comment"
    )
    n = section[split_index]
    pre = merge_comments(section[0:split_index])
    post = merge_comments(section[split_index + 1:])
    return (pre, n, post)

def to_sections(comma_sep_nodes : list[GenericNode]) -> list[list[GenericNode]]:
    if not comma_sep_nodes:
        return []

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

    return [ 
        section
        for start, end in zip(start_indices, end_indices) 
        for section in [comma_sep_nodes[start:end]]
    ]


def to_comma_exprs(comma_sep_nodes : list[GenericNode]) -> comma_exprs | None:
    es = [to_comment_triple(section) for section in to_sections(comma_sep_nodes)]
    if es :
        (pre_comment, n, post_comment) = es[-1]
        e = from_generic_tree_to_expr(n)
        result = SingleExpr(pre_comment, e, post_comment,
            unguard_expr(e).source_start if e else 0,
            unguard_expr(e).source_end if e else 0,
        )
        for (pre_comment, n, post_comment) in reversed(es[:-1]):
            e = from_generic_tree_to_expr(n)
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

def to_constraint_filters(nodes : list[GenericNode], base_start : int, base_end : int) -> constraint_filters:

    def assert_if_node(n):
        assert n.syntax_part == "if_clause"
        assert n.children[0].syntax_part == "if"

    start_indices = [
        i
        for i, n in enumerate(nodes)
        if n.syntax_part == "if_clause"
    ]

    end_indices = start_indices[1:] + [len(nodes)]

    trips = [
        (pre, cond, post)
        for start, end in zip(start_indices, end_indices)
        for if_node in [nodes[start]]
        for _ in [assert_if_node(if_node)]
        for pre in [merge_comments(if_node.children[1:-1])]
        for cond in [if_node.children[-1]]
        for post in [merge_comments(nodes[start+1:end])]
    ]

    (pre, n, post) = trips[-1]
    e = from_generic_tree_to_expr(n)

    (result, trips) = (
        (SingleFilter(pre, e, post,
            unguard_expr(e).source_start if e else 0,
            unguard_expr(e).source_end if e else 0,
        ), trips[:-1])
        if trips else

        (NoFilter(base_start, base_end), []) 
    )
    for (pre, n, post) in reversed(trips):
        e = from_generic_tree_to_expr(n)
        result = ConsFilter(pre, e, post, result,
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

def from_generic_tree_to_decorator(dec_node : GenericNode) -> decorator:
    if dec_node.syntax_part == "decorator":
        assert dec_node.children[0].syntax_part == "@"
        expr_node = dec_node.children[1] 
        comment_text = '' if len(dec_node.children) <= 2 else merge_comments(dec_node.children[2:])
        return ExprDec(from_generic_tree_to_expr(expr_node), comment_text, expr_node.source_start, expr_node.source_end)
    else:
        assert dec_node.syntax_part == "comment"
        return CmntDec(dec_node.text, dec_node.source_start, dec_node.source_end)


def from_list_to_keywords(ks : list[tuple[str, GenericNode, str]]) -> keywords:
    assert ks  

    (pre, n, post) = ks[-1]
    k = from_generic_tree_to_keyword(n)

    result = SingleKeyword(pre, k, post,
        unguard_keyword(k).source_start if k else 0,
        unguard_keyword(k).source_end if k else 0,
    )
    for pre, n, post in reversed(ks[:-1]):
        k = from_generic_tree_to_keyword(n)
        result = ConsKeyword(pre, k, post, result,
            unguard_keyword(k).source_start if k else 0,
            result.source_end
        )

    return result


def to_arguments(argument_nodes : list[GenericNode]) -> arguments:
    trips = [to_comment_triple(section) for section in to_sections(argument_nodes)]
    pos_trips = [
        (pre, n, post) 
        for pre, n, post in trips 
        if n.syntax_part != "keyword_argument" and n.syntax_part != "dictionary_splat"
    ]

    kw_trips = [
        (pre, n, post) 
        for pre, n, post in trips 
        if n.syntax_part == "keyword_argument" or n.syntax_part == "dictionary_splat"
    ]

    return from_list_to_arguments(pos_trips, (from_list_to_keywords(kw_trips) if kw_trips else None))


def from_list_to_arguments(ps : list[tuple[str, GenericNode, str]], kws : keywords | None) -> arguments:
    (pre, n, post) = ps[-1]
    p = from_generic_tree_to_expr(n)

    (result, ps) = (
        (KeywordsArg(kws,
            unguard_keywords(kws).source_start,
            unguard_keywords(kws).source_end,
        ), ps)
        if kws else

        (SingleArg(pre, p, post,
            unguard_expr(p).source_start if p else 0,
            unguard_expr(p).source_end if p else 0,
        ), ps[:-1])
    )

    for pre, n, post in reversed(ps):
        p = from_generic_tree_to_expr(n)
        result = ConsArg(pre, p, post, result,
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

import itertools

def split_rators_and_rands(
    nodes : list[GenericNode], 
    comments : list[str] = [], 
    rators : list[cmp_rator] = [], 
    rands : list[expr | None] = []
) -> tuple[list[str], list[cmp_rator], list[expr | None]]:


    if len(nodes) == 0:
        assert len(comments) == len(rators) == len(rands)
        return (comments, rators, rands)
    else:
        comment_nodes = list(itertools.takewhile(lambda n: n.syntax_part == "comment", nodes))
        comment = merge_comments(comment_nodes)
        head_index = len(comment_nodes)
        head_node = nodes[head_index]
        if head_node.syntax_part == '<':
            return split_rators_and_rands(nodes[head_index + 1:], comments + [comment], rators + [Lt(head_node.source_start, head_node.source_end)], rands)
        if head_node.syntax_part == '<=':
            return split_rators_and_rands(nodes[head_index + 1:], comments + [comment], rators + [LtE(head_node.source_start, head_node.source_end)], rands)
        if head_node.syntax_part == '==':
            return split_rators_and_rands(nodes[head_index + 1:], comments + [comment], rators + [Eq(head_node.source_start, head_node.source_end)], rands)
        if head_node.syntax_part == '!=':
            return split_rators_and_rands(nodes[head_index + 1:], comments + [comment], rators + [NotEq(head_node.source_start, head_node.source_end)], rands)
        if head_node.syntax_part == '>=':
            return split_rators_and_rands(nodes[head_index + 1:], comments + [comment], rators + [GtE(head_node.source_start, head_node.source_end)], rands)
        if head_node.syntax_part == '>':
            return split_rators_and_rands(nodes[head_index + 1:], comments + [comment], rators + [Gt(head_node.source_start, head_node.source_end)], rands)
        if head_node.syntax_part == '<>':
            return split_rators_and_rands(nodes[head_index + 1:], comments + [comment], rators + [NotEq(head_node.source_start, head_node.source_end)], rands)
        if head_node.syntax_part == 'in':
            return split_rators_and_rands(nodes[head_index + 1:], comments + [comment], rators + [In(head_node.source_start, head_node.source_end)], rands)
        if head_node.syntax_part == 'not':

            more_comment_nodes = list(itertools.takewhile(lambda n: n.syntax_part == "comment", nodes[head_index + 1:]))
            next_node_index = head_index + 1 + len(more_comment_nodes)
            next_head = nodes[next_node_index]
            if next_head.syntax_part == "in":
                comment = merge_comments(comment_nodes + more_comment_nodes)
                return split_rators_and_rands(nodes[next_node_index + 1:], comments + [comment], rators + [NotIn(head_node.source_start, next_head.source_end)], rands)
            else:
                raise Unsupported(next_head.syntax_part)
                # return split_rators_and_rands(nodes[1:], rators + [In()], rands)
        if head_node.syntax_part == 'is':
            more_comment_nodes = list(itertools.takewhile(lambda n: n.syntax_part == "comment", nodes[head_index + 1:]))
            next_node_index = head_index + 1 + len(more_comment_nodes)
            next_head = nodes[next_node_index]
            if next_head.syntax_part == "not":
                return split_rators_and_rands(nodes[next_node_index + 1:], comments + [comment], rators + [IsNot(head_node.source_start, next_head.source_end)], rands)
            else:
                return split_rators_and_rands(nodes[head_index + 1:], comments + [comment], rators + [Is(head_node.source_start, head_node.source_end)], rands)

        else:
            rand = from_generic_tree_to_expr(head_node)
            tail = nodes[head_index + 1:]
            return split_rators_and_rands(tail, comments, rators, rands + [rand])


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

    in_index = next(
        i
        for i, n in enumerate(for_children)
        if n.syntax_part == "in"
    )

    target_index = next(
        i + 1
        for i, n in enumerate(for_children[1:in_index])
        if n.syntax_part != "comment"
    )

    if_clause_index = next((
        i
        for i, n in enumerate(for_children)
        if n.syntax_part == "if_clause"
    ), None)

    iter_index = next(
        i + in_index + 1
        for i, n in enumerate(for_children[in_index + 1:(if_clause_index or len(for_children))])
        if n.syntax_part != "comment"
    )

    comment_a = merge_comments(for_children[1:target_index])

    target_expr = from_generic_tree_to_expr(for_children[target_index])

    comment_b = merge_comments(for_children[target_index + 1:in_index])
    comment_c = merge_comments(for_children[in_index + 1:iter_index])

    iter_expr = from_generic_tree_to_expr(for_children[iter_index])

    comment_d = merge_comments(for_children[iter_index + 1:if_clause_index])






    if_nodes = nodes[if_clause_index:]




    source_start = nodes[0].source_start
    source_end = nodes[-1].source_end
    if is_async:
        return AsyncConstraint(comment_a, target_expr, comment_b, comment_c, iter_expr, comment_d, to_constraint_filters(if_nodes, 
            unguard_expr(iter_expr).source_end if iter_expr else 0,
            source_end
        ), source_start, source_end)
    else:
        return Constraint(comment_a, target_expr, comment_b, comment_c, iter_expr, comment_d, to_constraint_filters(if_nodes,
            unguard_expr(iter_expr).source_end if iter_expr else 0,
            source_end
        ), source_start, source_end)


def collapse_constraint_nodes(nodes : list[GenericNode]) -> list[constraint] | None:
    start_indices = [
        i
        for i, n in enumerate(nodes)
        if n.syntax_part == "for_in_clause"
    ]
    end_indicies = start_indices[1:] + [len(nodes)] 

    return [
        from_nodes_to_constraint(slice)
        for start, end in zip(start_indices, end_indicies)
        for slice in [nodes[start:end]]
    ]


def comprehension_parts(node : GenericNode):
    assert (
        (node.syntax_part == "list_comprehension") or
        (node.syntax_part == "set_comprehension") or
        (node.syntax_part == "generator_expression")
    )
    children = node.children[1:-1]

    expr_index = next(
        i
        for i, n in enumerate(children)
        if n.syntax_part != "comment"
        if n.syntax_part != "for_in_clause"
        if n.syntax_part != "if_clause"
    )

    for_clause_index = next((
        i
        for i, n in enumerate(children)
        if n.syntax_part == "for_in_clause"
    ), None)

    pre_comment = merge_comments(children[1:expr_index])
    expr = from_generic_tree_to_expr(children[expr_index])
    post_comment = merge_comments(children[expr_index + 1:(for_clause_index or -1)])
    constraint_nodes = children[for_clause_index:] if for_clause_index else [] 

    return (
        pre_comment,
        expr, 
        post_comment,
        (
            to_comprehension_constraints(constraint_nodes)
            if constraint_nodes else
            None
        ),
        node.source_start, node.source_end
    )


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
        comment = merge_comments(children[1:-1])
        rand_node = children[-1]
        op = from_generic_tree_to_unaryop(op_node)
        rand = from_generic_tree_to_expr(rand_node)
        return UnaryOp(op, comment, rand, node.source_start, node.source_end)
    
    elif (node.syntax_part == "attribute"):
        children = node.children
        expr_node = children[0]
        expr = from_generic_tree_to_expr(expr_node)
        pre_comment_nodes = list(itertools.takewhile(lambda n: n.syntax_part == "comment", children[1:]))
        dot_index = len(pre_comment_nodes) + 1
        post_comment_nodes = list(itertools.takewhile(lambda n: n.syntax_part == "comment", children[dot_index + 1:]))
        id_node = children[-1]

        pre_comment = merge_comments(pre_comment_nodes)
        post_comment = merge_comments(post_comment_nodes)
        id = from_generic_tree_to_identifier(id_node)
        return Attribute(expr, pre_comment, post_comment, id, node.source_start, node.source_end)

    elif (node.syntax_part == "subscript"):
        children = node.children
        target_node = children[0]
        target = from_generic_tree_to_expr(target_node)
        comment_a_nodes = list(itertools.takewhile(lambda n: n.syntax_part == "comment", children[1:]))

        bracket_index = len(comment_a_nodes) + 1
        assert children[bracket_index].syntax_part == "["
        assert children[-1].syntax_part == "]"

        comment_a = merge_comments(comment_a_nodes)

        slice_index = next(( 
            i + bracket_index + 1 
            for i, n in enumerate(children[bracket_index + 1:-1])
            if n.syntax_part == "slice"
        ), None) 


        if slice_index:
            slice_node = children[slice_index]
            comment_b = merge_comments(children[bracket_index + 1:slice_index])
            slice = from_generic_tree_to_expr(slice_node)
            comment_c = merge_comments(children[slice_index + 1:-1])
            return Subscript(target, comment_a, comment_b, slice, comment_c, node.source_start, node.source_end)

        else:
            comma_sep_nodes = children[bracket_index + 1:-1]
            exprs = to_comma_exprs(comma_sep_nodes)

            slice = Tuple(exprs, children[1].source_start, children[-1].source_end)
            return Subscript(target, comment_a, '', slice, '', node.source_start, node.source_end)


    elif (node.syntax_part == "call"):
        children = node.children
        func_node = children[0]
        func = from_generic_tree_to_expr(func_node)

        comment_nodes = list(itertools.takewhile(lambda n: n.syntax_part == "comment", children[1:]))
        args_index = len(comment_nodes) + 1
        comment = merge_comments(comment_nodes)

        args_node = children[args_index]
        if args_node.syntax_part == "argument_list":
            argument_nodes = args_node.children[1:-1]
            if argument_nodes: 
                seq_arg = to_arguments(argument_nodes)
                return CallArgs(func, comment, seq_arg, node.source_start, node.source_end)
            else:
                return Call(func, comment, node.source_start, node.source_end)

        elif args_node.syntax_part == "generator_expression":
            return CallArgs(func, comment, from_list_to_arguments([('', args_node, '')], None), node.source_start, node.source_end)

        else:
            return node_error(args_node)

    elif (node.syntax_part == "list"):

        exprs = to_comma_exprs(node.children[1:-1])
        if exprs:
            return List(exprs, node.source_start, node.source_end)
        else:
            return EmptyList(node.source_start, node.source_end)

    elif (node.syntax_part == "list_comprehension"):
        (
            pre_comment,
            expr, 
            post_comment,
            constraints,
            source_start, source_end
        ) = comprehension_parts(node)

        return ListComp(
            pre_comment,
            expr, 
            post_comment,
            constraints,
            node.source_start, node.source_end
        )

    elif (node.syntax_part == "dictionary"):
        children = node.children[1:-1]
        if children:
            return Dictionary(to_dictionary_content(children), node.source_start, node.source_end)
        else:
            return EmptyDictionary(node.source_start, node.source_end)

    elif node.syntax_part == "dictionary_comprehension":
        # children = node.children[1:-1]
        # pair_node = children[0]
        # assert pair_node.syntax_part == "pair"
        # pair = pair_node.children
        # key = from_generic_tree_to_expr(pair[0])
        # assert pair[1].syntax_part == ":"
        # value = from_generic_tree_to_expr(pair[2])

        # constraint_nodes = children[1:]
        # constraints = collapse_constraint_nodes(constraint_nodes)
        ################################


        children = node.children[1:-1]

        pair_index = next(
            i
            for i, n in enumerate(children)
            if n.syntax_part == "pair"
        )

        pair = children[pair_index]

        pair_colon_index = next(
            i
            for i, n in enumerate(pair.children)
            if n.syntax_part == ":"
        )


        for_clause_index = next((
            i
            for i, n in enumerate(children)
            if n.syntax_part == "for_in_clause"
        ), None)


        comment_a = merge_comments(children[:pair_index])
        key = from_generic_tree_to_expr(pair.children[0])
        comment_b = merge_comments(pair.children[1:pair_colon_index])
        comment_c = merge_comments(pair.children[pair_colon_index + 1:-1])
        value = from_generic_tree_to_expr(pair.children[-1])
        comment_d = merge_comments(children[pair_index + 1:(for_clause_index or -1)])
        constraint_nodes = children[for_clause_index:] if for_clause_index else [] 

        return DictionaryComp(
            comment_a,
            key, 
            comment_b, comment_c, 
            value, 
            comment_d, (
                to_comprehension_constraints(constraint_nodes)
                if constraint_nodes else
                None
            ),
            node.source_start, node.source_end
        )

    elif (node.syntax_part == "set"):
        exprs = to_comma_exprs(node.children[1:-1])
        return Set(exprs, node.source_start, node.source_end)

    elif (node.syntax_part == "set_comprehension"):
        (
            pre_comment,
            expr, 
            post_comment,
            constraints,
            source_start, source_end
        ) = comprehension_parts(node)

        return SetComp(
            pre_comment,
            expr, 
            post_comment,
            constraints,
            source_start, source_end
        )


    elif (node.syntax_part == "generator_expression"):
        (
            pre_comment,
            expr, 
            post_comment,
            constraints,
            source_start, source_end
        ) = comprehension_parts(node)

        return GeneratorExp(
            pre_comment,
            expr, 
            post_comment,
            constraints,
            source_start, source_end
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

        from_index = next((
            i
            for i, n in enumerate(children)
            if n.syntax_part == "from"
        ), None)

        if from_index:
            comment_a = merge_comments(children[1:from_index])
            comment_b = merge_comments(children[from_index + 1: -1])
            expr = from_generic_tree_to_expr(children[-1])
            return YieldFrom(comment_a, comment_b, expr, node.source_start, node.source_end)
        else:

            if len(children) == 1:
                return YieldNothing(node.source_start, node.source_end)
            else:
                comment = merge_comments(children[1:-1])
                expr = from_generic_tree_to_expr(children[-1])
                return Yield(comment, expr, node.source_start, node.source_end)

    elif node.syntax_part == "comparison_operator":
        left = from_generic_tree_to_expr(node.children[0])
        (comments, rators, rands) = split_rators_and_rands(node.children[1:])
        assert len(rators) == len(rands)
        comp_rights = [
            CompareRight(comments[i], rators[i], rands[i], unguard_cmp_rator(rators[-1]).source_start, node.source_end)
            for i, _ in enumerate(rators)
        ]
        return Compare(left, to_comparisons(comp_rights), node.source_start, node.source_end)

    elif (node.syntax_part == "not_operator"):
        children = node.children
        assert children[0].syntax_part == "not"
        comment = merge_comments(children[1:-1])
        rand_node = children[-1]
        op = Not(node.source_start, node.source_end) 
        rand = from_generic_tree_to_expr(rand_node)
        return UnaryOp(op, comment, rand, node.source_start, node.source_end)

    elif node.syntax_part == "boolean_operator":
        children = node.children
        left_expr = from_generic_tree_to_expr(children[0])
        op_index = next(
            i + 1
            for i, n in enumerate(children[1:-1])
            if n.syntax_part != "comment"
        )
        pre_comment = merge_comments(children[1:op_index])
        op = from_generic_tree_to_boolop(children[op_index])
        post_comment = merge_comments(children[op_index + 1:-1])
        right_expr = from_generic_tree_to_expr(children[-1])

        return BoolOp(left_expr, pre_comment, op, post_comment, right_expr, node.source_start, node.source_end)

    elif node.syntax_part == "await":
        assert node.children[0].syntax_part == "await"
        comment = merge_comments(node.children[1:-1])
        expr = from_generic_tree_to_expr(node.children[-1])
        return Await(comment, expr, node.source_start, node.source_end)

    elif node.syntax_part == "lambda":
        assert node.children[0].syntax_part == "lambda"

        params_index = next((
            i + 1
            for i, n in enumerate(node.children[1:-1])
            if n.syntax_part == "lambda_parameters"
        ), None)

        colon_index = next(
            i + 1
            for i, n in enumerate(node.children[1:-1])
            if n.syntax_part == ":"
        )
        if not params_index:
            params = NoParam(node.source_start, node.source_end)
            comment_a = merge_comments(node.children[1:colon_index])
            comment_b = '' 
            comment_c = merge_comments(node.children[colon_index + 1:-1])
            body = from_generic_tree_to_expr(node.children[-1])
            return Lambda(comment_a, params, comment_b, comment_c, body, node.source_start, node.source_end)
        else:
            params = from_generic_tree_to_parameters(node.children[params_index])
            body = from_generic_tree_to_expr(node.children[-1])
            comment_a = merge_comments(node.children[1:params_index])
            comment_b = merge_comments(node.children[params_index + 1:colon_index])
            comment_c = merge_comments(node.children[colon_index + 1:-1])

            return Lambda(comment_a, params, comment_b, comment_c, body, node.source_start, node.source_end)

    elif node.syntax_part == "conditional_expression":
        children = node.children
        if_index = next(
            i for i, n in enumerate(children)
            if n.syntax_part == "if"
        )
        cond_index = next(
            i + if_index + 1
            for i, n in enumerate(children[if_index + 1:])
            if n.syntax_part != "comment"
        )
        else_index = next(
            i for i, n in enumerate(children)
            if n.syntax_part == "else"
        )

        true_expr = from_generic_tree_to_expr(children[0])
        comment_a = merge_comments(children[1:if_index])
        comment_b = merge_comments(children[if_index + 1:cond_index])
        cond_expr = from_generic_tree_to_expr(children[cond_index])
        comment_c = merge_comments(children[cond_index + 1:else_index])
        comment_d = merge_comments(children[else_index + 1:-1])
        false_expr = from_generic_tree_to_expr(children[-1])

        return IfExp(true_expr, comment_a, comment_b, cond_expr, comment_c, comment_d, false_expr, node.source_start, node.source_end)

    elif node.syntax_part == "named_expression":
        children = node.children
        target_expr = from_generic_tree_to_expr(children[0])
        assign_index = next(
            i + 1
            for i, n in enumerate(children[1:-1])
            if n.syntax_part == ":="
        )
        pre_comment = merge_comments(children[1:assign_index])
        post_comment = merge_comments(children[assign_index + 1:-1])
        value_expr = from_generic_tree_to_expr(children[-1])
        return AssignExpr(target_expr, pre_comment, post_comment, value_expr, node.source_start, node.source_end)

    elif node.syntax_part == "type":
        return from_generic_tree_to_expr(node.children[0])

    elif node.syntax_part == "slice":
        children = node.children


        comment_a_nodes = list(itertools.takewhile(lambda n: n.syntax_part == "comment", children[1:]))
        colon_a_index = len(comment_a_nodes) + 1

        colon_b_index = next((
            i + colon_a_index + 1
            for i, n in enumerate(children[colon_a_index + 1:])
            if n.syntax_part == ":"
        ), None)

        right_index = (
            next((
                i + colon_a_index + 1
                for i, n in enumerate(children[colon_a_index + 1:colon_b_index])
                if n.syntax_part != "comment"
            ), None)
            if colon_b_index else
            next((
                i + colon_a_index + 1
                for i, n in enumerate(children[colon_a_index + 1:])
                if n.syntax_part != "comment"
            ), None)
        )


        left_node = children[0] if colon_a_index != 0 else None
        right_node = children[right_index] if right_index else None
        step_node = children[-1] if colon_b_index and colon_b_index != len(children) - 1 else None

        comment_a = merge_comments(comment_a_nodes)
        comment_b = (
            merge_comments(children[colon_a_index + 1:right_index])
            if right_index else
            merge_comments(children[colon_a_index + 1:colon_b_index])
            if colon_b_index else
            ''
        )

        comment_c = (
            merge_comments(children[right_index + 1:colon_b_index])
            if right_index and colon_b_index else
            merge_comments(children[right_index + 1:])
            if right_index else
            ''
        )

        comment_d = (
            merge_comments(children[colon_b_index + 1:-1])
            if colon_b_index and step_node else
            merge_comments(children[colon_b_index + 1:])
            if colon_b_index else
            ''
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

        return Slice(left, comment_a, comment_b, right, comment_c, comment_d, step, node.source_start, node.source_end)

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
            '',
            id, 
            NoParamAnno(node.source_start, node.source_start), 
            NoParamDefault(node.source_start, node.source_start), 
            node.source_start, node.source_end
        )

    elif node.syntax_part == "typed_parameter":

        first_child = node.children[0]
        id_node = (
            first_child.children[1]
            if 
                first_child.syntax_part == "list_splat_pattern" and
                first_child.children[0].syntax_part == "*"
            else

            first_child.children[1]
            if 
                first_child.syntax_part == "dictionary_splat_pattern" and
                first_child.children[0].syntax_part == "**"
            else 
            
            first_child

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
        comment = merge_comments(node.children[1:-1]) 
        id_node = node.children[-1]
        id = from_generic_tree_to_identifier(id_node)
        return Param(
            comment,
            id, 
            NoParamAnno(id_node.source_end, id_node.source_end), 
            NoParamDefault(id_node.source_end, id_node.source_end),
            node.source_start, node.source_end
        )

    elif node.syntax_part == "dictionary_splat_pattern":
        assert node.children[0].syntax_part == "**"
        comment = merge_comments(node.children[1:-1]) 
        id_node = node.children[-1]
        id = from_generic_tree_to_identifier(id_node)
        return Param(
            comment,
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
        ]


        sections = to_sections(children)


        positional_separator_section_index = next(
            (
                i 
                for i, section in enumerate(sections)
                if any(n.syntax_part == "positional_separator" for n in section)
            ),
            -1 
        )



        list_splat_section_index = next(
            (
                i 
                for i, section in enumerate(sections)
                if any(
                    n.syntax_part == "list_splat_pattern" or 
                    (
                        n.syntax_part == "typed_parameter" and
                        n.children[0].syntax_part == "list_splat_pattern"
                    ) or
                    n.syntax_part == "keyword_separator"
                    for n in section
                )

            ),
            -1 
        )

        dictionary_splat_section_index = next(
            (
                i 
                for i, section in enumerate(sections)
                if any(
                    n.syntax_part == "dictionary_splat_pattern" or 
                    (
                        n.syntax_part == "typed_parameter" and
                        n.children[0].syntax_part == "dictionary_splat_pattern"
                    )
                    for n in section
                )
            ),
            -1 
        )

        pos_sections = (
            sections[0:positional_separator_section_index + 1] # include param sep section 
            if positional_separator_section_index > -1 else
            []
        )

        (pos_kw_sections, list_splat_section, kw_sections, dictionary_splat_section) = (

            (
                sections[positional_separator_section_index + 1:list_splat_section_index], 
                sections[list_splat_section_index], 
                sections[list_splat_section_index + 1: dictionary_splat_section_index], 
                sections[dictionary_splat_section_index]
            )
            if (list_splat_section_index >= 0 and dictionary_splat_section_index >= 0) else 
            
            (
                sections[positional_separator_section_index + 1:list_splat_section_index], 
                sections[list_splat_section_index], 
                sections[list_splat_section_index + 1:], 
                None
            )
            if list_splat_section_index >= 0 and dictionary_splat_section_index < 0 else 
            
            (
                sections[positional_separator_section_index + 1:-1], 
                None,
                [],
                sections[dictionary_splat_section_index]
            )
            if list_splat_section_index < 0 and dictionary_splat_section_index >= 0 else 

            (
                sections[positional_separator_section_index + 1:], 
                None,
                [],
                None
            )
        )

        return to_parameters(pos_sections, pos_kw_sections, list_splat_section, kw_sections, dictionary_splat_section, 
            node.source_start, node.source_end
        )

        # pos_params = [
        #     from_generic_tree_to_Param(n)
        #     for n in pos_param_nodes
        # ]

        # pos_kw_params = [
        #     from_generic_tree_to_Param(n)
        #     for n in pos_kw_param_nodes
        # ]


        # list_splat_param = (
        #     None
        #     if (
        #         not list_splat_node or 
        #         (
        #             list_splat_node.syntax_part == "list_splat_pattern" and 
        #             len(list_splat_node.children) == 0
        #         ) or 
        #         list_splat_node.syntax_part == "keyword_separator"
        #     ) else 

        #     from_generic_tree_to_Param(list_splat_node)
        # )

        # kw_params = [
        #     from_generic_tree_to_Param(n)
        #     for n in kw_nodes
        # ]

        # dictionary_splat_param = from_generic_tree_to_Param(dictionary_splat_node) if dictionary_splat_node else None

        # return to_parameters(pos_params, pos_kw_params, list_splat_param, kw_params, dictionary_splat_param, 
        #     node.source_start, node.source_end
        # )


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
        arg_keywords = None 

        chev_node = children[1]
        if chev_node.syntax_part == "chevron":
            arg_index = 2

            k = make_NamedKeyword("file", Name(
                "sys.stderr", 
                chev_node.source_start, chev_node.source_start
            ), node.source_start, node.source_start)
            
            arg_keywords = make_SingleKeyword('', k, '',
                unguard_keyword(k).source_start if k else 0,
                unguard_keyword(k).source_end if k else 0,
            )
        else:
            arg_index = 1

        arg_nodes = [to_comment_triple(section) for section in to_sections(children[arg_index:])]

        comment = ''

        return [Expr(
            CallArgs(
                Name("print",
                    children[0].source_start,
                    children[0].source_end,
                ), 
                comment,
                from_list_to_arguments(arg_nodes, arg_keywords),
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
        block_index = next( 
            i
            for i, n in enumerate(children)
            if n.syntax_part == "block"
        )
        comment = merge_comments(children[2:block_index])
        try_block = children[block_index]
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
                    comment,
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
                    comment,
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
                    comment,
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
                    comment,
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
                    comment,
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

        base_nodes = list(itertools.takewhile(lambda n: 
            n.syntax_part != "keyword_argument" and n.syntax_part != "dictionary_splat", 
            arguments_node.children[1:-1]
        )) if arguments_node else []


        kw_index = 1 + len(base_nodes) + 1

        if arguments_node:
            print(f"%%%arguments_node.children[kw_index:-1]: {arguments_node.children[kw_index:-1]}")

        kw_trips = []
        if (arguments_node != None):
            kw_trips = [to_comment_triple(section) for section in to_sections(arguments_node.children[kw_index:-1])] 

        kws = from_list_to_keywords(kw_trips) if kw_trips else None

        bases = to_bases(base_nodes, kws, name_node.source_end, block_node.children[0].source_start)

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

        def_node = children[-1]

        decs = to_decorators([
            dec_node
            for dec_node in dec_nodes
        ], def_node.source_start, def_node.source_start)

        return from_generic_tree_to_stmts(def_node, decorators = decs)

    elif (node.syntax_part == "comment"):
        return [Comment(node.text, node.source_start, node.source_end)]

    else:
        # exec_statement for Python 2
        # print_statement for Python 2
        return [node_error(node)]