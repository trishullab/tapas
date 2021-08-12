from type_def import header, to_shape_list, generate_type_union_def, generate_type_intersection_def
from file import write

# Rather than use the Python's ast module, we define our own custom constructors and types
# for type safety and better correspondence to the abstract grammar 
# https://docs.python.org/3/library/ast.html
# We use one class purely for static typing, which corresponds to LHS of the grammar
# We use the type's subclasses as constructors of the RHS of the grammar.
# For each static type, we define a pattern matching mechanism using the visitor design pattern,
# static types without their own constructors will be lowercase


code = "\n\n".join([
    generate_type_intersection_def(
        "Module", 
        [
            ("body", "list[stmt]")
        ]
    ),

    generate_type_union_def(
        "stmt",
        [
            ("FunctionDef", [
                ("name", "Identifier"),
                ("param_group", "ParamGroup"),
                ("body", "list[stmt]"),
                ("decorator_list", "list[expr]"),
                ("returns", "Optional[expr]")
            ]),

            ("AsyncFunctionDef", [
                ("name", "Identifier"),
                ("param_group", "ParamGroup"),
                ("body", "list[stmt]"),
                ("decorator_list", "list[expr]"),
                ("returns", "Optional[expr]")
            ]),

            ("ClassDef", [
                ("name", "Identifier"),
                ("bases", "list[expr]"),
                ("keywords", "list[Keyword]"),
                ("body", "list[stmt]"),
                ("decorator_list", "list[expr]")
            ]),

            ("Return", [
                ("value", "Optional[expr]")
            ]),

            ("Delete", [
                ("targets", "list[expr]")
            ]),

            ("Assign", [
                ("targets", "list[expr]"),
                ("value", "expr")
            ]),

            ("AugAssign", [
                ("target", "expr"),
                ("op", "operator"),
                ("value", "expr")
            ]),

            #'simple' indicates that we annotate simple name without parens
            ("AnnAssign", [
                ("target", "expr"),
                ("annotation", "expr"),
                ("value", "Optional[expr]")
            ]),

            ("AnnAssignSimple", [
                ("target", "expr"),
                ("annotation", "expr"),
                ("value", "Optional[expr]")
            ]),

            # use 'orelse' because else is a Keyword in target languages
            ("For", [
                ("target", "expr"),
                ("iter", "expr"),
                ("body", "list[stmt]"),
                ("orelse", "list[stmt]")
            ]),

            ("AsyncFor", [
                ("target", "expr"),
                ("iter", "expr"),
                ("body", "list[stmt]"),
                ("orelse", "list[stmt]")
            ]),

            ("While", [
                ("test", "expr"),
                ("body", "list[stmt]"),
                ("orelse", "list[stmt]")
            ]),

            ("If", [
                ("test", "expr"),
                ("body", "list[stmt]"),
                ("orelse", "list[stmt]")
            ]),

            ("With", [
                ("items", "list[Withitem]"),
                ("body", "list[stmt]")
            ]),

            ("AsyncWith", [
                ("items", "list[Withitem]"),
                ("body", "list[stmt]")
            ]),

            ("Raise", [
                ("exc", "Optional[expr]"),
                ("cause", "Optional[expr]")
            ]),

            ("Try", [
                ("body", "list[stmt]"),
                ("handlers", "list[ExceptHandler]"),
                ("orelse", "list[stmt]"),
                ("finalbody", "list[stmt]")
            ]),

            ("Assert", [
                ("test", "expr"),
                ("msg", "Optional[expr]")
            ]),

            ("Import", [
                ("names", "list[Alias]")
            ]),

            ("ImportFrom", [
                ("module", "Optional[Identifier]"),
                ("names", "list[Alias]"),
                ("level", "Optional[int]")
            ]),


            ("Global", [
                ("names", "list[Identifier]")
            ]),

            ("Nonlocal", [
                ("names", "list[Identifier]"),
            ]),

            ("Expr", [
                ("value", "expr")
            ]),

            ("Pass", []), 
            ("Break", []),
            ("Continue", [])


        ]
    ),

    generate_type_union_def(
        "expr",
        [
            ("BoolOp", [
                ("left", "expr"),
                ("op", "boolop"),
                ("right", "expr")
            ]),

            ("NamedExpr", [
                ("target", "expr"),
                ("value", "expr")
            ]),

            ("BinOp", [
                ("left", "expr"),
                ("op", "operator"),
                ("right", "expr")
            ]),

            ("UnaryOp", [
                ("op", "unaryop"),
                ("operand", "expr")
            ]),

            ("Lambda", [
                ("param_group", "ParamGroup"),
                ("body", "expr")
            ]),

            ("IfExp", [
                ("test", "expr"),
                ("body", "expr"),
                ("orelse", "expr")
            ]),

            ("Dict", [
                ("entries", "list[Entry]"),
            ]),

            ("Set", [
                ("elts", "list[expr]")
            ]),

            ("ListComp", [
                ("elt", "expr"),
                ("constraints", "list[constraint]")
            ]),

            ("SetComp", [
                ("elt", "expr"),
                ("constraints", "list[constraint]")
            ]),

            ("DictComp", [
                ("key", "expr"),
                ("value", "expr"),
                ("constraints", "list[constraint]")
            ]),

            ("GeneratorExp", [
                ("elt", "expr"),
                ("constraints", "list[constraint]")
            ]),

            # the grammar constrains where yield expressions can occur
            ("Await", [
                ("value", "expr")
            ]),

            ("Yield", [
                ("value", "Optional[expr]")
            ]),

            ("YieldFrom", [
                ("value", "expr")
            ]),

            # need sequences for compare to distinguish between
            # x < 4 < 3 and (x < 4) < 3
            ("Compare", [
                ("left", "expr"),
                ("ops", "list[cmpop]"),
                ("comparators", "list[expr]")
            ]),

            ("Call", [
                ("func", "expr"),
                ("args", "list[expr]"),
                ("keywords", "list[Keyword]")
            ]),

            ("Integer", [
                ("value", "str"),
            ]),

            ("Float", [
                ("value", "str"),
            ]),

            ("String", [
                ("value", "str"),
            ]),

            ("True_", []),

            ("False_", []),

            ("None_", []),

            ("Ellip", []),

            ("ConcatString", [
                ("values", "list[str]"),
            ]),


            # the following expression can appear in assignment context
            ("Attribute", [
                ("value", "expr"),
                ("attr", "Identifier")
            ]),

            ("Subscript", [
                ("value", "expr"),
                ("slice", "expr")
            ]),

            ("Starred", [
                ("value", "expr")
            ]),

            ("Name", [
                ("id", "Identifier")
            ]),

            ("List", [
                ("elts", "list[expr]")
            ]),

            ("Tuple", [
                ("elts", "list[expr]")
            ]),

            # can appear only in Subscript
            ("Slice", [
                ("lower", "Optional[expr]"),
                ("upper", "Optional[expr]"),
                ("step", "Optional[expr]")
            ])

        ]
    ),


    generate_type_union_def(
        "boolop",
        [
            ("And", []),
            ("Or", [])
        ]
    ),

    generate_type_union_def(
        "operator",
        [
            ("Add", []), 
            ("Sub", []), 
            ("Mult", []), 
            ("MatMult", []), 
            ("Div", []), 
            ("Mod", []), 
            ("Pow", []), 
            ("LShift", []),
            ("RShift", []), 
            ("BitOr", []), 
            ("BitXor", []), 
            ("BitAnd", []), 
            ("FloorDiv", [])
        ]
    ),

    generate_type_union_def(
        "unaryop",
        [
            ("Invert", []), 
            ("Not", []), 
            ("UAdd", []), 
            ("USub", [])
        ]
    ),

    generate_type_union_def(
        "cmpop", [
            ("Eq", []), 
            ("NotEq", []), 
            ("Lt", []), 
            ("LtE", []), 
            ("Gt", []), 
            ("GtE", []), 
            ("Is", []), 
            ("IsNot", []), 
            ("In", []), 
            ("NotIn", [])
        ] 
    ),

    generate_type_union_def(
        "constraint", [
            ("AsyncConstraint", [
                ("target", "expr"),
                ("iter", "expr"),
                ("ifs", "list[expr]")
            ]),
            ("Constraint", [
                ("target", "expr"),
                ("iter", "expr"),
                ("ifs", "list[expr]")
            ])
        ]
    ),

    generate_type_intersection_def(
        "ExceptHandler",
         [
            ("type", "Optional[expr]"),
            ("name", "Optional[Identifier]"),
            ("body", "list[stmt]")
         ]
    ),

    generate_type_intersection_def(
        "ParamGroup",
        [
            ("pos_params", "list[Param]"),
            ("params", "list[Param]"),
            ("list_splat", "Optional[Param]"),
            ("kw_params", "list[Param]"),
            ("dictionary_splat", "Optional[Param]")
        ]
    ),

    generate_type_intersection_def(
        "Param",
        [
            ("id", "Identifier"),
            ("annotation", "Optional[expr]"),
            ("default", "Optional[expr]")
        ]
    ),

    generate_type_intersection_def(
        "Keyword",
        [
            ("name", "Optional[Identifier]"),
            ("value", "expr")
        ]
    ),

    generate_type_intersection_def(
        "Entry",
        [
            ("key", "expr"),
            ("value", "expr")
        ]
    ),

    generate_type_intersection_def(
        "Alias",
        [
            ("name", "Identifier"),
            ("asname", "Optional[Identifier]")
        ]
    ),

    generate_type_intersection_def(
        "Withitem",
        [
            ("context_expr", "expr"),
            ("optional_vars", "Optional[expr]")
        ]
    ),

    generate_type_intersection_def(
        "Identifier",
        [ 
            ("symbol", "str")
        ]
    )


])


code = f"""
{header}

{code}

"""

write("python_ast", code)
