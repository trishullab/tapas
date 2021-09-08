from __future__ import annotations

unions = {

    "stmt" : {
        "FunctionDef" : {
            "name" : "Identifier",
            "param_group" : "ParamGroup",
            "body" : "list[stmt]",
            "decorator_list" : "list[expr]",
            "returns" : "Optional[expr]"
        },

        "AsyncFunctionDef" : {
            "name" : "Identifier",
            "param_group" : "ParamGroup",
            "body" : "list[stmt]",
            "decorator_list" : "list[expr]",
            "returns" : "Optional[expr]"
        },

        "ClassDef" : {
            "name" : "Identifier",
            "bases" : "list[expr]",
            "keywords" : "list[Keyword]",
            "body" : "list[stmt]",
            "decorator_list" : "list[expr]"
        },

        "Return" : {
            "value" : "Optional[expr]"
        },

        "Delete" : {
            "targets" : "list[expr]"
        },

        "Assign" : {
            "targets" : "list[expr]",
            "value" : "expr"
        },

        "AugAssign" : {
            "target" : "expr",
            "op" : "operator",
            "value" : "expr"
        },

        #'simple' indicates that we annotate simple name without parens
        "AnnAssign" : {
            "target" : "expr",
            "annotation" : "expr",
            "value" : "Optional[expr]"
        },

        "AnnAssignSimple" : {
            "target" : "expr",
            "annotation" : "expr",
            "value" : "Optional[expr]"
        },

        # use 'orelse' because else is a Keyword in target languages
        "For" : {
            "target" : "expr",
            "iter" : "expr",
            "body" : "list[stmt]",
            "orelse" : "list[stmt]"
        },

        "AsyncFor" : {
            "target" : "expr",
            "iter" : "expr",
            "body" : "list[stmt]",
            "orelse" : "list[stmt]"
        },

        "While" : {
            "test" : "expr",
            "body" : "list[stmt]",
            "orelse" : "list[stmt]"
        },

        "If" : {
            "test" : "expr",
            "body" : "list[stmt]",
            "orelse" : "list[stmt]"
        },

        "With" : {
            "items" : "list[Withitem]",
            "body" : "list[stmt]"
        },

        "AsyncWith" : {
            "items" : "list[Withitem]",
            "body" : "list[stmt]"
        },

        "Raise" : {
            "exc" : "Optional[expr]",
            "cause" : "Optional[expr]"
        },

        "Try" : {
            "body" : "list[stmt]",
            "handlers" : "list[ExceptHandler]",
            "orelse" : "list[stmt]",
            "finalbody" : "list[stmt]"
        },

        "Assert" : {
            "test" : "expr",
            "msg" : "Optional[expr]"
        },

        "Import" : {
            "names" : "list[Alias]"
        },

        "ImportFrom" : {
            "module" : "Optional[Identifier]",
            "names" : "list[Alias]",
            "level" : "Optional[int]"
        },


        "Global" : {
            "names" : "list[Identifier]"
        },

        "Nonlocal" : {
            "names" : "list[Identifier]",
        },

        "Expr" : {
            "value" : "expr"
        },

        "Pass" : {}, 
        "Break" : {},
        "Continue" : {}

    },

    "expr" : {
        "BoolOp" : {
            "left" : "expr",
            "op" : "boolop",
            "right" : "expr"
        },

        "NamedExpr" : {
            "target" : "expr",
            "value" : "expr"
        },

        "BinOp" : {
            "left" : "expr",
            "op" : "operator",
            "right" : "expr"
        },

        "UnaryOp" : {
            "op" : "unaryop",
            "operand" : "expr"
        },

        "Lambda" : {
            "param_group" : "ParamGroup",
            "body" : "expr"
        },

        "IfExp" : {
            "test" : "expr",
            "body" : "expr",
            "orelse" : "expr"
        },

        "Dict" : {
            "entries" : "list[Entry]",
        },

        "Set" : {
            "elts" : "list[expr]"
        },

        "ListComp" : {
            "elt" : "expr",
            "constraints" : "list[constraint]"
        },

        "SetComp" : {
            "elt" : "expr",
            "constraints" : "list[constraint]"
        },

        "DictComp" : {
            "key" : "expr",
            "value" : "expr",
            "constraints" : "list[constraint]"
        },

        "GeneratorExp" : {
            "elt" : "expr",
            "constraints" : "list[constraint]"
        },

        # the grammar constrains where yield expressions can occur
        "Await" : {
            "value" : "expr"
        },

        "Yield" : {
            "value" : "Optional[expr]"
        },

        "YieldFrom" : {
            "value" : "expr"
        },

        # need sequences for compare to distinguish between
        # x < 4 < 3 and (x < 4) < 3
        "Compare" : {
            "left" : "expr",
            "ops" : "list[cmpop]",
            "comparators" : "list[expr]"
        },

        "Call" : {
            "func" : "expr",
            "args" : "list[expr]",
            "keywords" : "list[Keyword]"
        },

        "Integer" : {
            "value" : "str",
        },

        "Float" : {
            "value" : "str",
        },

        "String" : {
            "value" : "str",
        },

        "True_" : {},

        "False_" : {},

        "None_" : {},

        "Ellip" : {},

        "ConcatString" : {
            "values" : "list[str]",
        },


        # the following expression can appear in assignment context
        "Attribute" : {
            "value" : "expr",
            "attr" : "Identifier"
        },

        "Subscript" : {
            "value" : "expr",
            "slice" : "expr"
        },

        "Starred" : {
            "value" : "expr"
        },

        "Name" : {
            "id" : "Identifier"
        },

        "List" : {
            "elts" : "list[expr]"
        },

        "Tuple" : {
            "elts" : "list[expr]"
        },

        # can appear only in Subscript
        "Slice" : {
            "lower" : "Optional[expr]",
            "upper" : "Optional[expr]",
            "step" : "Optional[expr]"
        }

    },

    "boolop" : {
        "And" : {},
        "Or" : {}
    },

    "operator" : {
        "Add" : {}, 
        "Sub" : {}, 
        "Mult" : {}, 
        "MatMult" : {}, 
        "Div" : {}, 
        "Mod" : {}, 
        "Pow" : {}, 
        "LShift" : {},
        "RShift" : {}, 
        "BitOr" : {}, 
        "BitXor" : {}, 
        "BitAnd" : {}, 
        "FloorDiv" : {}
    },

    "unaryop" : {
        "Invert" : {}, 
        "Not" : {}, 
        "UAdd" : {}, 
        "USub" : {}
    },

    "cmpop" : {
        "Eq" : {}, 
        "NotEq" : {}, 
        "Lt" : {}, 
        "LtE" : {}, 
        "Gt" : {}, 
        "GtE" : {}, 
        "Is" : {}, 
        "IsNot" : {}, 
        "In" : {}, 
        "NotIn" : {}
    },

    "constraint" : {
        "AsyncConstraint" : {
            "target" : "expr",
            "iter" : "expr",
            "ifs" : "list[expr]"
        },
        "Constraint" : {
            "target" : "expr",
            "iter" : "expr",
            "ifs" : "list[expr]"
        }
    }

}


intersections = {

    "Module" : {
        "body" : "list[stmt]"
    },

    "ExceptHandler" : {
        "type" : "Optional[expr]",
        "name" : "Optional[Identifier]",
        "body" : "list[stmt]"
    },

    "ParamGroup": {
        "pos_params" : "list[Param]",
        "params" : "list[Param]",
        "list_splat" : "Optional[Param]",
        "kw_params" : "list[Param]",
        "dictionary_splat" : "Optional[Param]"
    },

    "Param" : {
        "id" : "Identifier",
        "annotation" : "Optional[expr]",
        "default" : "Optional[expr]"
    },

    "Keyword" : {
        "name" : "Optional[Identifier]",
        "value" : "expr"
    },

    "Entry" : {
        "key" : "expr",
        "value" : "expr"
    },

    "Alias" : {
        "name" : "Identifier",
        "asname" : "Optional[Identifier]"
    },

    "Withitem" : {
        "context_expr" : "expr",
        "optional_vars" : "Optional[expr]"
    },

    "Identifier" : { 
        "symbol" : "str"
    }

}


def format() -> str:


    ### rule of sequence ###

    rule_of_nonterm_unions = [
        k + " : " + choices_str 
        for k, choices in unions.items()
        for choices_str in [ ' | '.join([
            c[0]
            for c in choices
        ])]
    ]

    import inflection
    rule_of_nonterm_intersections = [
        k + " : " + k 
        for k in intersections.keys()
    ]

    rule_of_nonterm_list = "list[T] : {T]"

    rule_of_nonterm_str = "---- RULE OF NON-TERMINAL ----\n\n" + (
        "\n".join(rule_of_nonterm_unions) + 
        "\n" + 
        "\n".join(rule_of_nonterm_intersections) + 
        "\n" + 
        rule_of_nonterm_list
    )



    ### rule of sequence ###
    rule_of_sequence_unions = [
        k + " : { " + fields_str + " } "
        for choices in unions.values()
        for k, fields in choices
        for fields_str in [', '.join([
            name + ' : ' + typ
            for (name, typ) in fields
        ])]
    ]

    rule_of_sequence_intersections = [
        k + " : { " + fields_str + " } "
        for k, fields in intersections.items()
        for fields_str in [', '.join([
            name + ' : ' + typ
            for (name, typ) in fields
        ])]
    ]

    rule_of_sequence_list = "[T] : { _.. : T.. }"

    rule_of_sequence_str = "---- RULE OF SEQUENCE ----\n\n" + (
        "\n".join(rule_of_sequence_unions) + 
        "\n" + 
        "\n".join(rule_of_sequence_intersections) + 
        "\n" + 
        rule_of_sequence_list
    )


    return rule_of_nonterm_str + "\n\n" + rule_of_sequence_str