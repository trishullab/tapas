from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from collections.abc import Callable

from abc import ABC, abstractmethod


from generic_tree import GenericNode

from gen.python_ast import *
from python_ast_serialize import serialize_constraint

from utils import fail
import utils



def unsupported(node : GenericNode):
        fail(f"unsupported syntax for {node.syntax_part}")

def from_generic_ast(node : GenericNode) -> Module: 
    children = node.children
    if (node.syntax_part == "module"):
        statements = [
            stmt
            for stmt_node in children  
            for stmt in from_generic_ast_to_stmts(stmt_node)
        ]
        return Module(statements)
    else:
       unsupported(node) 



def from_generic_ast_to_Identifier(node : GenericNode) -> Identifier:
    node.syntax_part
    if (node.syntax_part == "dotted_name"):
        children = node.children
        dotted_name = ".".join([
            id.text
            for id in children
        ])
        return Identifier(dotted_name)
    elif (node.syntax_part == "identifier"):
        return Identifier(node.text)
    else:
       unsupported(node) 


def from_generic_ast_to_Alias(node : GenericNode, alias : Optional[str] = None) -> Alias:
    
    if (node.syntax_part == "dotted_name"):
        dotted_name = ".".join([
            child.text
            for child in node.children
            if child.syntax_part == "identifier"
        ])
        return Alias(
            Identifier(dotted_name),
            utils.map_option(Identifier, alias) 
        )
    elif (node.syntax_part == "identifier"):
        text = node.text
        return Alias(
            Identifier(text),
            utils.map_option(Identifier, alias) 
        )
    elif (node.syntax_part == "aliased_import"):
        children = node.children
        name_node = children[0]
        assert children[1].syntax_part == "as"
        asname_node = children[2]
        asname_text = asname_node.text
        return from_generic_ast_to_Alias(name_node, asname_text)
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
        if children[1].syntax_part == ":" 
        
        else  (children[1], None, children[3])
        if children[2].syntax_part == ":" 
        
        else (children[1], children[3], children[5])
        if (
            children[2].syntax_part == "as" and 
            children[4].syntax_part == ":" 
        ) 
        
        else (None, None, None)
    )

    assert block_node

    expr = utils.map_option(from_generic_ast_to_expr, expr_node)
    name = utils.map_option(from_generic_ast_to_Identifier, name_node)
    stmts = [
        stmt
        for stmt_node in block_node.children
        for stmt in from_generic_ast_to_stmts(stmt_node)
    ]

    return  ExceptHandler(expr, name, stmts)


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
    return Withitem(context_expr, pattern_expr)


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
        return AsyncConstraint(target_expr, iter_expr, if_exprs)
    else:
        return Constraint(target_expr, iter_expr, if_exprs)


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
        return Name(from_generic_ast_to_Identifier(node))

    elif (node.syntax_part == "string"):
        return String(node.text)

    elif node.syntax_part == "concatenated_string":
        children = node.children
        str_values = [
            n.text
            for n in children
        ]

        return ConcatString(str_values)

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
        id = from_generic_ast_to_Identifier(id_node)
        return Attribute(expr, id)

    elif (node.syntax_part == "subscript"):
        children = node.children
        target_node = children[0]
        target = from_generic_ast_to_expr(target_node)
        assert children[1].syntax_part == "["
        assert children[3].syntax_part == "]"
        slice_node = children[2]
        slice = from_generic_ast_to_expr(slice_node)
        return Subscript(target, slice)

    elif (node.syntax_part == "call"):
        children = node.children
        func_node = children[0]
        func = from_generic_ast_to_expr(func_node)

        arg_list_node = children[1]
        assert arg_list_node.syntax_part == "argument_list"

        argument_nodes = [
            child
            for child in arg_list_node.children[1:-1]
            if child.syntax_part != ","
        ]

        pos_nodes = [n for n in argument_nodes if n.syntax_part != "keyword_argument"]
        kw_nodes = [n for n in argument_nodes if n.syntax_part == "keyword_argument"]

        pos_args = [
            from_generic_ast_to_expr(n)
            for n in pos_nodes
        ]

        keywords = [
            from_generic_ast_to_Keyword(n)
            for n in kw_nodes
        ]

        return Call(func, pos_args, keywords)

    elif (node.syntax_part == "list"):
        items = [
            from_generic_ast_to_expr(child)
            for child in node.children[1:-1]
            if child.syntax_part != ","
        ]
        return List(items)

    elif (node.syntax_part == "list_comprehension"):
        children = node.children[1:-1]
        expr = from_generic_ast_to_expr(children[0])

        constraint_nodes = children[1:]

        print(f"nodes length: {len(constraint_nodes)}")


        constraints = collapse_constraint_nodes(constraint_nodes)
        print(f"constraints length: {len(constraints)}")

        return ListComp(expr, constraints)

    elif (node.syntax_part == "dictionary"):
        children = [
            child
            for child in node.children[1:-1]
            if child.syntax_part != ","
        ]

        def assert_colon(pair): 
            assert pair[1].syntax_part == ":"

        entries = [
            Entry(k, v)
            for pair_node in children
            for pair in [pair_node.children]
            for k in [from_generic_ast_to_expr(pair[0])]
            for _ in [assert_colon(pair)]
            for v in [from_generic_ast_to_expr(pair[2])]
        ]

        return Dict(entries)

    elif node.syntax_part == "dictionary_comprehension":
        children = node.children[1:-1]
        pair_node = children[0]
        pair = pair_node.children
        key = from_generic_ast_to_expr(pair[0])
        value = from_generic_ast_to_expr(pair[1])

        constraint_nodes = children[1:]
        constraints = collapse_constraint_nodes(constraint_nodes)

        return DictComp(key, value, constraints)

    elif (node.syntax_part == "set"):
        
        items = [
            from_generic_ast_to_expr(n)
            for n in node.children[1:-1]
            if n.syntax_part != ","
        ]
        return Set(items)

    elif (node.syntax_part == "set_comprehension"):
        children = node.children[1:-1]
        expr = from_generic_ast_to_expr(children[0])

        constraint_nodes = children[1:]
        constraints = collapse_constraint_nodes(constraint_nodes)
        return SetComp(expr, constraints)

    elif (node.syntax_part == "generator_expression"):
        children = node.children[1:-1]
        expr = from_generic_ast_to_expr(children[0])

        constraint_nodes = children[1:]
        constraints = collapse_constraint_nodes(constraint_nodes)
        return GeneratorExp(expr, constraints)

    elif (node.syntax_part == "tuple"):
        items = [
            from_generic_ast_to_expr(n)
            for n in node.children[1:-1]
            if n.syntax_part != ","
        ]
        return Tuple(items)

    elif (node.syntax_part == "expression_list"):
        items = [
            from_generic_ast_to_expr(n)
            for n in node.children
            if n.syntax_part != ","
        ]
        return Tuple(items)

    
    elif (node.syntax_part == "parenthesized_expression"):
        expr_node = node.children[1:-1][0]
        return from_generic_ast_to_expr(expr_node)

    elif (node.syntax_part == "ellipsis"):
        return Ellip() 

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
        return Tuple(items)

    elif (node.syntax_part == "list_pattern"):
        items = [
            from_generic_ast_to_expr(n)
            for n in node.children[1:-1]
            if n.syntax_part != ","
        ]
        return List(items)

    elif (node.syntax_part == "pattern_list"):
        items = [
            from_generic_ast_to_expr(n)
            for n in node.children
            if n.syntax_part != ","
        ]
        return Tuple(items)

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
        return Compare(left, ops, rands)

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
        param_group = from_generic_ast_to_ParamGroup(node.children[1])
        assert node.children[2].syntax_part == ":"
        body = from_generic_ast_to_expr(node.children[3])
        return Lambda(param_group, body)

    elif node.syntax_part == "conditional_expression":
        children = node.children
        true_expr = from_generic_ast_to_expr(children[0])
        assert children[1].syntax_part == "if"
        cond_expr = from_generic_ast_to_expr(children[1])
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
            if len(children) == 5

            else
            (None, children[1], children[3])
            if len(children) == 4 and children[0].syntax_part == ":"

            else
            (children[0], children[2], None)
            if len(children) == 4 and children[0].syntax_part != ":"

            else
            (None, children[1], None)
            if len(children) == 3 and children[0].syntax_part == ":"

            else
            (children[0], None, None)
            if len(children) == 3 and children[1].syntax_part == ":" and
            children[2].syntax_part == ":" 

            else
            (children[0], None, children[1])
            if len(children) == 3 and children[1].syntax_part == ":" and
            children[2].syntax_part != ":" 

            else
            (None, children[1], None)
            if len(children) == 2 and children[0].syntax_part == ":" 

            else
            (children[0], None, None)
            if len(children) == 2 and children[1].syntax_part == ":"

            else
            (None, None, None)

        )
        left = utils.map_option(from_generic_ast_to_expr, left_node)
        right = utils.map_option(from_generic_ast_to_expr, right_node)
        step = utils.map_option(from_generic_ast_to_expr, step_node)

        return Slice(left, right, step)

    else:
        # keyword_identifier / not sure if this is actually ever used
        unsupported(node)



def from_generic_ast_to_Keyword(node) -> Keyword:
    assert node.syntax_part == "keyword_argument"
    children = node.children
    key_node = children[0]
    assert children[1].syntax_part == "="
    value_node = children[2]

    key_id = utils.map_option(from_generic_ast_to_Identifier, key_node)
    value_expr = from_generic_ast_to_expr(value_node)

    return Keyword(key_id, value_expr)



def from_generic_ast_to_Param(node : GenericNode) -> Param:

    if node.syntax_part == "identifier":
        id = from_generic_ast_to_Identifier(node)
        return Param(id, None, None)

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

        id = from_generic_ast_to_Identifier(id_node)
        assert node.children[1].syntax_part == ":"
        type_anno = from_generic_ast_to_expr(node.children[2])
        return Param(id, type_anno, None)

    elif node.syntax_part == "default_parameter":
        id = from_generic_ast_to_Identifier(node.children[0])
        assert node.children[1].syntax_part == "="
        default_expr = from_generic_ast_to_expr(node.children[2])
        return Param(id, None, default_expr)

    elif node.syntax_part == "typed_default_parameter":
        id = from_generic_ast_to_Identifier(node.children[0])
        assert node.children[1].syntax_part == ":"
        type_anno = from_generic_ast_to_expr(node.children[2])
        assert node.children[3].syntax_part == "="
        default_expr = from_generic_ast_to_expr(node.children[4])
        return Param(id, type_anno, default_expr)

    elif node.syntax_part == "list_splat_pattern":
        assert node.children[0].syntax_part == "*"
        id = from_generic_ast_to_Identifier(node.children[1])
        return Param(id, None, None)

    elif node.syntax_part == "dictionary_splat_pattern":
        assert node.children[0].syntax_part == "**"
        id = from_generic_ast_to_Identifier(node.children[1])
        return Param(id, None, None)

    else:
        unsupported(node)


def from_generic_ast_to_ParamGroup(node : GenericNode) -> ParamGroup:
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
                    n.children[0] == "list_splat_pattern"
                )
            )


        def is_dictionary_splat_node(n : GenericNode):
            return (
                n.syntax_part == "dictionary_splat_pattern" or (
                    n.syntax_part == "typed_parameter" and
                    n.children[0] == "dictionary_splat_pattern"
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


        return ParamGroup(pos_params, params, list_splat_param, kw_params, dictionary_splat_param)

    else:
        unsupported(node)



def from_generic_ast_to_stmts(node : GenericNode, decorators : list[expr] = []) -> list[stmt]: 

    if (node.syntax_part == "import_statement"):
        children = node.children
        assert children[0].syntax_part == "import"
        return [Import(
            names = [
                from_generic_ast_to_Alias(child)
                for child in children[1:]
                if child.syntax_part != ","
            ]
        )]

    elif (node.syntax_part == "import_from_statement"):
        children = node.children
        assert children[0].syntax_part == "from"
        module = from_generic_ast_to_Identifier(children[1])
        assert children[2].syntax_part == "import"
        aliases = (
            []
            if len(children) == 4 and
            children[3].syntax_part == "wildcard_import"

            else
            [
                from_generic_ast_to_Alias(n) 
                for n in children[3:]
                if n.syntax_part != ","
            ]
        )
        return [ImportFrom(module, aliases, None)]

    elif (node.syntax_part == "future_import_statement"):
        children = node.children
        assert children[0].syntax_part == "from"
        id = Identifier("__future__") 
        assert children[2].syntax_part == "import"
        aliases = [
            from_generic_ast_to_Alias(n) 
            for n in children[3:]
            if n.syntax_part != ","
        ]
        return [ImportFrom(id, aliases, None)]

    elif (node.syntax_part == "assert_statement"):
        children = node.children
        assert children[0].syntax_part == "assert"
        test_expr = from_generic_ast_to_expr(children[1])
        msg_expr = (from_generic_ast_to_expr(children[2])
            if len(children) == 2 else None)

        return [
            Assert(test_expr, msg_expr)
        ]

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

                (left, typ, right) = (

                    (estmt_children[0], estmt_children[2], None)
                    if len(estmt_children) == 3 and estmt_children[1].syntax_part == ":" 
                    
                    else (estmt_children[0], None, estmt_children[2])
                    if len(estmt_children) == 3 and estmt_children[1].syntax_part == "=" 

                    else 
                    (estmt_children[0], estmt_children[2], estmt_children[4])
                    if (
                        len(estmt_children) == 5 and 
                        estmt_children[1].syntax_part == ":" and
                        estmt_children[3].syntax_part == "="
                    )

                    else (None, None, None)
                )

                assert left 

                if typ:
                    left_expr = from_generic_ast_to_expr(left)
                    typ_expr = from_generic_ast_to_expr(typ)
                    right_expr = utils.map_option(from_generic_ast_to_expr, right)
                    return [
                        AnnAssign(left_expr, typ_expr, right_expr)
                    ]
                elif right:
                    right_expr = from_generic_ast_to_expr(right)

                    if (left.syntax_part == "pattern_list"):
                        left_exprs = [
                            from_generic_ast_to_expr(left_child) 
                            for left_child in left.children
                            if left_child.syntax_part != ","
                        ]
                        return [
                            Assign(left_exprs, right_expr)
                        ] 

                    else:
                        left_exprs = [from_generic_ast_to_expr(left)]
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
        expr = (from_generic_ast_to_expr(children[1]) if len(children) == 2 else None)

        return [
            Return(expr)
        ]

    elif (node.syntax_part == "delete_statement"):
        assert node.children[0] == "del"
        child = node.children[1]
        if (child.syntax_part == "expression_list"):
            exprs = [
                from_generic_ast_to_expr(expr_node)
                for expr_node in child.children
                if expr_node.syntax_part != ","
            ]
            return [
                Delete(exprs)
            ]
        else:
            expr = from_generic_ast_to_expr(child)
            return [
                Delete([expr])
            ]

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
        return [
            Raise(exc_expr, cause_expr)
        ]

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
        assert children[0] == "global"
        ids = [
            from_generic_ast_to_Identifier(id_node)
            for id_node in children
            if id_node.syntax_part != ","
        ]

        return [
            Global(ids)
        ]

    elif (node.syntax_part == "nonlocal_statement"):
        children = node.children
        assert children[0] == "nonlocal"
        ids = [
            from_generic_ast_to_Identifier(id_node)
            for id_node in children
            if id_node.syntax_part != ","
        ]

        return [
            Nonlocal(ids)
        ]

    elif (node.syntax_part == "if_statement"):
        children = node.children
        assert children[0] == "if"
        cond_node = children[1]
        assert children[2] == ":"
        block_node = children[3]

        def nest_elifs(cond_node, block_node, remainder):
            def nest_elifs_(cond_node, block_node, remainder):
                assert block_node.syntax_part == "block"
                block_children = block_node.children
                cond_expr = from_generic_ast_to_expr(cond_node)
                block_stmts = [
                    stmt 
                    for stmt_node in block_children
                    for stmt in from_generic_ast_to_stmts(stmt_node)
                ]

                if len(remainder) > 0:
                    else_node = remainder[-1]
                    if (else_node == "elif_clause"):
                        else_children = else_node.children
                        assert else_children[0].syntax_part == "elif"
                        cond_node_ = else_children[1]
                        assert else_children[2].syntax_part == ":"
                        block_node_ = else_children[3]
                        else_stmts = nest_elifs_(cond_node_, block_node_, remainder[:-1])
                        return If(cond_expr, block_stmts, else_stmts)

                    elif (else_node == "else_clause"):
                        else_children = else_node.children
                        assert else_children[0].syntax_part == "else"
                        assert else_children[1].syntax_part == ":"
                        block_node_ = else_children[2]
                        block_children = block_node_.children
                        else_stmts = [
                            stmt 
                            for stmt_node in block_children
                            for stmt in from_generic_ast_to_stmts(stmt_node)
                        ]
                        return If(cond_expr, block_stmts, else_stmts)
                    else:
                        unsupported(else_node)
                else:
                    return If(cond_expr, block_stmts, [])

            return nest_elifs_(cond_node, block_node, [r for r in reversed(remainder)])

        return [nest_elifs(cond_node, block_node, children[2:])]

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
        body_stmts = [
            stmt
            for stmt_node in block_node.children
            for stmt in from_generic_ast_to_stmts(stmt_node) 
        ]

        else_node = (
            children[6]
            if (len(children) == 7) 
            
            else None 
        )

        assert not else_node or else_node.syntax_part == "else_clause"

        assert not else_node or else_node.children[0] == "else" 

        assert not else_node or else_node.children[1] == ":" 

        else_block = else_node.children[2] if else_node else None 

        assert not else_block or else_block.syntax_part == "block"

        block_children = else_block.children if else_block else []

        else_stmts = [
            stmt
            for stmt_node in block_children
            for stmt in from_generic_ast_to_stmts(stmt_node) 
        ]

        if is_async:
            return [
                AsyncFor(target_expr, iter_expr, body_stmts, else_stmts)
            ]

        else:
            return [
                For(target_expr, iter_expr, body_stmts, else_stmts)
            ]

    elif(node.syntax_part == "while_statement"):
        children = node.children
        assert children[0].syntax_part == "while"
        test_expr = from_generic_ast_to_expr(children[1])

        assert children[2].syntax_part == ":"
        block_node = children[3]
        assert block_node.syntax_part == "block"
        body_stmts = [
            stmt
            for stmt_node in block_node.children 
            for stmt in from_generic_ast_to_stmts(stmt_node) 
        ]

        else_node = (
            children[4]
            if (len(children) == 5) 
            
            else None 
        )


        assert not else_node or else_node.syntax_part == "else_clause"

        assert not else_node or else_node.children[0] == "else" 

        assert not else_node or else_node.children[1] == ":" 

        else_block = else_node.children[2] if else_node else None 

        assert not else_block or else_block.syntax_part == "block"

        block_children = else_block.children if else_block else []

        else_stmts = [
            stmt
            for stmt_node in block_children 
            for stmt in from_generic_ast_to_stmts(stmt_node) 
        ]

        return [
            While(test_expr, body_stmts, else_stmts)
        ]
    elif (node.syntax_part == "try_statement"):
        children = node.children
        assert children[0] == "try"
        assert children[1] == ":"
        try_block = children[2]
        assert try_block.syntax_part == "block"
        try_stmts = [
            stmt
            for stmt_node in try_block.children
            for stmt in from_generic_ast_to_stmts(stmt_node) 
        ]

        except_clause_nodes = [
            n
            for n in children
            if n.syntax_part == "except_clause"
        ]

        except_handlers = [
            from_generic_ast_to_ExceptHandler(ec_node)
            for ec_node in except_clause_nodes
        ]

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
            if len(else_clause_nodes) == 0 
            
            else
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
            if len(finally_clause_nodes) == 0 
            
            else
            [
                stmt
                for finally_clause_node in [finally_clause_nodes[0]] 
                for _ in [assert_finally_clause(finally_clause_node)]
                for block_node in [finally_clause_node.children[2]] 
                for stmt_node in block_node.children
                for stmt in from_generic_ast_to_stmts(stmt_node)
            ]
        )

        return [
            Try(try_stmts, except_handlers, else_stmts, finally_stmts)
        ]



    elif (node.syntax_part == "with_statement"):
        children = node.children
        (is_async, children) = (
          (True, children[1:])
          if (children[0].syntax_part == "async") else
          (False, children)
        ) 

        assert children[0].syntax_part == "with"
        with_clause_node = children[1]
        with_items = [
            from_generic_ast_to_Withitem(item_node)
            for item_node in with_clause_node.children
        ]

        block_node = children[1]
        stmts = [
            stmt
            for stmt_node in block_node.children
            for stmt in from_generic_ast_to_stmts(stmt_node)
        ]

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
        name = from_generic_ast_to_Identifier(name_node)

        params_node = children[2]
        param_group = from_generic_ast_to_ParamGroup(params_node)

        (return_type_node, block_node) = (
            (children[4], children[6])
            if children[3].syntax_part == "->" and children[5].syntax_part == ":"
            
            else (None, children[4])
            if children[3].syntax_part == ":"

            else (None, None)
        )

        assert block_node

        return_type = utils.map_option(
            lambda n : from_generic_ast_to_expr(n), 
            return_type_node 
        )

        body = [
            stmt
            for stmt_node in block_node.children
            for stmt in from_generic_ast_to_stmts(stmt_node)
        ]



        if is_async: 
            return [
                AsyncFunctionDef(name, param_group, body, decorators, return_type)
            ]

        else:
            return [
                FunctionDef(name, param_group, body, decorators, return_type)
            ]


    elif (node.syntax_part == "class_definition"):
        children = node.children

        assert children[0].syntax_part == "class"

        name_node = children[1]
        name = from_generic_ast_to_Identifier(name_node)

        (arguments_node, block_node) = (
            (None, children[3])
            if children[2].syntax_part == ":"

            else (children[1], children[2])

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

        base_nodes = [n for n in argument_nodes if n.syntax_part != "keyword_argument"]
        kw_nodes = [n for n in argument_nodes if n.syntax_part == "keyword_argument"]

        base_exprs = [
            from_generic_ast_to_expr(n)
            for n in base_nodes
        ]

        keywords = [
            from_generic_ast_to_Keyword(n)
            for n in kw_nodes
        ]

        body_stmts = [
            stmt
            for n in block_node.children
            for stmt in from_generic_ast_to_stmts(n)
        ]

        return [
            ClassDef(name, base_exprs, keywords, body_stmts, decorators)
        ]

    elif (node.syntax_part == "decorated_definition"):
        children = node.children
        dec_nodes = children[0:-1]
        def assert_decorator(dec_node):
            assert dec_node.syntax_part == "decorator"
            assert dec_node.children[0].syntax_part == "@"

        dec_exprs = [
            from_generic_ast_to_expr(dec_expr_node)
            for dec_node in dec_nodes
            for _ in [assert_decorator(dec_node)]
            for dec_expr_node in [dec_node.children[1]]
        ] 

        def_node = children[-1]
        return from_generic_ast_to_stmts(def_node, decorators = dec_exprs)

    else:
        # exec_statement for Python 2
        # print_statement for Python 2
        unsupported(node)