from __future__ import annotations

from lib.schema import Node, Child
from lib import schema
from gen.line_format import NewLine, InLine, IndentLine

unions : dict[str, list[Node]] = {

    "return_type" : [

        Node(
            "SomeReturnType",
            " -> ",
            [
                Child("content", "expr", InLine(), "")
            ]
        ),

        Node(
            "NoReturnType",
            "",
            []
        )
    ],

    "module_id" : [

        Node(
            "SomeModuleId",
            "",
            [
                Child("content", "Identifier", InLine(), "")
            ]
        ),

        Node(
            "NoModuleId",
            ". ",
            []
        )
    ],

    "except_arg" : [
        Node(
            "SomeExceptArg",
            " ",
            [
                Child("content", "expr", InLine(), "")
            ]
        ),

        Node(
            "SomeExceptArgName",
            " ",
            [
                Child("content", "expr", InLine(), " as "),
                Child("name", "Identifier", InLine(), ""),
            ]
        ),

        Node(
            "NoExceptArg",
            "",
            []
        )
    ],

    "param_type" : [
        Node(
            "SomeParamType",
            " : ",
            [
                Child("content", "expr", InLine(), ""),
            ]
        ),

        Node(
            "NoParamType",
            "",
            []
        ),
    ],

    "param_default" : [
        Node(
            "SomeParamDefault",
            " = ",
            [
                Child("content", "expr", InLine(), ""),
            ]
        ),

        Node(
            "NoParamDefault",
            "",
            []
        ),
    ],

    "parameters_d" : [
        Node(
            "ConsKwParam",
            "",
            [
                Child("head", "Param", InLine(), ", "),
                Child("tail", "parameters_d", InLine(), ""),
            ]
        ),

        Node(
            "SingleKwParam",
            "",
            [
                Child("content", "Param", InLine(), ""),
            ]
        ),

        Node(
            "DictionarySplatParam",
            "**",
            [
                Child("content", "Param", InLine(), "")
            ]
        )

    ],

    "parameters_c" : [
        Node(
            "SingleListSplatParam",
            "*",
            [
                Child("content", "Param", InLine(), ""),
            ]
        ),

        Node(
            "TransListSplatParam",
            "*",
            [
                Child("head", "Param", InLine(), ", "),
                Child("tail", "parameters_d", InLine(), ""),
            ]
        ),

        Node(
            "ParamsD",
            "*, ",
            [
                Child("content", "parameters_d", InLine(), ""),
            ]
        ),
    ],

    "parameters_b" : [
        Node(
            "ConsParam",
            "",
            [
                Child("head", "Param", InLine(), ", "),
                Child("tail", "parameters_b", InLine(), ""),
            ]
        ),

        Node(
            "SingleParam",
            "",
            [
                Child("content", "Param", InLine(), ""),
            ]
        ),

        Node(
            "ParamsC",
            "",
            [
                Child("content", "parameters_c", InLine(), ""),
            ]
        ),

    ],

    "parameters" : [
        Node(
            "ParamsA",
            "",
            [
                Child("content", "parameters_a", InLine(), ""),
            ]
        ),


        Node(
            "ParamsB",
            "",
            [
                Child("content", "parameters_b", InLine(), "")
            ]
        ),

        Node(
            "NoParam",
            "",
            []
        )
    ],


    "parameters_a" : [
        Node(
            "ConsPosParam",
            "",
            [
                Child("head", "Param", InLine(), ", "),
                Child("tail", "parameters_a", InLine(), ""),
            ]
        ),

        Node(
            "SinglePosParam",
            "",
            [
                Child("content", "Param", InLine(), ", /"),
            ]
        ),

        Node(
            "TransPosParam",
            "",
            [
                Child("head", "Param", InLine(), ", /, "),
                Child("tail", "parameters_b", InLine(), ""),
            ]
        )

    ],


    "keyword" : [

        Node(
            "NamedKeyword",
            "",
            [
                Child("name", "Identifier", InLine(), " = "),
                Child("content", "expr", InLine(), "")
            ]
        ),

        Node(
            "SplatKeyword",
            "**",
            [
                Child("content", "expr", InLine(), "")
            ]
        ),
    ],

    "alias" : [

        Node(
            "SomeAlias",
            " as ",
            [
                Child("content", "Identifier", InLine(), "")
            ]
        ),

        Node(
            "NoAlias",
            "",
            []
        ),

    ],

    "alias_expr" : [

        Node(
            "SomeAliasExpr",
            " as ",
            [
                Child("content", "expr", InLine(), "")
            ]
        ),

        Node(
            "NoAliasExpr",
            "",
            []
        ),

    ],

    "bases" : [
        Node(
            "SomeBases",
            "(",
            [
                Child("bases", "bases_a", InLine(), ")")
            ]
        ),

        Node(
            "NoBases",
            "",
            []
        )
    ],

    "bases_a" : [
        Node(
            "ConsBase",
            "",
            [
                Child("head", "expr", InLine(), ", "),
                Child("tail", "bases_a", InLine(), ""),
            ]
        ),

        Node(
            "SingleBase",
            "",
            [
                Child("content", "expr", InLine(), ""),
            ]
        ),

        Node(
            "KeywordsBase",
            "",
            [
                Child("kws", "keywords", InLine(), "")
            ]
        ),

    ],

    "keywords" : [
        Node(
            "ConsKeyword",
            "",
            [
                Child("head", "keyword", InLine(), ", "),
                Child("tail", "keywords", InLine(), ""),
            ]
        ),

        Node(
            "SingleKeyword",
            "",
            [
                Child("content", "keyword", InLine(), ""),
            ]
        ),

    ],

    "comparisons" : [
        Node(
            "ConsCompareRight",
            "",
            [
                Child("head", "CompareRight", InLine(), " "),
                Child("tail", "comparisons", InLine(), ""),
            ]
        ),

        Node(
            "SingleCompareRight",
            "",
            [
                Child("content", "CompareRight", InLine(), ""),
            ]
        ),

    ],

    "option_expr" : [
        Node(
            "SomeExpr",
            "",
            [
                Child("content", "expr", InLine(), ""),
            ]
        ),

        Node(
            "NoExpr",
            "",
            []
        )
    ],


    "comma_exprs" : [
        Node(
            "ConsExpr",
            "",
            [
                Child("head", "expr", InLine(), ", "),
                Child("tail", "comma_exprs", InLine(), ""),
            ]
        ),

        Node(
            "SingleExpr",
            "",
            [
                Child("content", "expr", InLine(), ""),
            ]
        ),

    ],

    "target_exprs" : [
        Node(
            "ConsTargetExpr",
            "",
            [
                Child("head", "expr", InLine(), " = "),
                Child("tail", "target_exprs", InLine(), ""),
            ]
        ),

        Node(
            "SingleTargetExpr",
            "",
            [
                Child("content", "expr", InLine(), ""),
            ]
        ),

    ],

    "decorators" : [
        Node(
            "ConsDec",
            "@",
            [
                Child("head", "expr", InLine(), ""),
                Child("tail", "decorators", InLine(), ""),
            ]
        ),

        Node(
            "NoDec",
            "",
            []
        ),

    ],

    "constraint_filters" : [
        Node(
            "ConsFilter",
            "if ",
            [
                Child("head", "expr", NewLine(), ""),
                Child("tail", "constraint_filters", InLine(), ""),
            ]
        ),

        Node(
            "SingleFilter",
            "if ",
            [
                Child("content", "expr", NewLine(), ""),
            ]
        ),

        Node(
            "NoFilter",
            "",
            [
            ]
        ),

    ],

    "sequence_str" : [
        Node(
            "ConsStr",
            "",
            [
                Child("head", "str", InLine(), " "),
                Child("tail", "sequence_str", InLine(), ""),
            ]
        ),

        Node(
            "SingleStr",
            "",
            [
                Child("content", "str", InLine(), ""),
            ]
        ),

    ],

    "arguments" : [
        Node(
            "ConsArg",
            "",
            [
                Child("head", "expr", InLine(), ", "),
                Child("tail", "arguments", InLine(), ""),
            ]
        ),

        Node(
            "SingleArg",
            "",
            [
                Child("content", "expr", InLine(), ""),
            ]
        ),

        Node(
            "KeywordsArg",
            "",
            [
                Child("kws", "keywords", InLine(), ""),
            ]
        ),

    ],

    "dictionary_contents" : [
        Node(
            "ConsField",
            "",
            [
                Child("head", "Field", InLine(), ", "),
                Child("tail", "dictionary_contents", NewLine(), ""),
            ]
        ),

        Node(
            "SingleField",
            "",
            [
                Child("content", "Field", InLine(), ""),
            ]
        ),

    ],

    "sequence_Identifier" : [
        Node(
            "ConsId",
            "",
            [
                Child("head", "Identifier", InLine(), ", "),
                Child("tail", "sequence_Identifier", InLine(), ""),
            ]
        ),

        Node(
            "SingleId",
            "",
            [
                Child("content", "Identifier", InLine(), ""),
            ]
        ),

    ],


    "sequence_ImportName" : [
        Node(
            "ConsImportName",
            "",
            [
                Child("head", "ImportName", InLine(), ", "),
                Child("tail", "sequence_ImportName", InLine(), ""),
            ]
        ),

        Node(
            "SingleImportName",
            "",
            [
                Child("content", "ImportName", InLine(), ""),
            ]
        ),

    ],

    "sequence_Withitem" : [
        Node(
            "ConsWithitem",
            "",
            [
                Child("head", "Withitem", InLine(), ", "),
                Child("tail", "sequence_Withitem", InLine(), ""),
            ]
        ),

        Node(
            "SingleWithitem",
            "",
            [
                Child("content", "Withitem", InLine(), ""),
            ]
        ),

    ],


    "statements" : [
        Node(
            "ConsStmt",
            "",
            [
                Child("head", "stmt", InLine(), ""),
                Child("tail", "statements", NewLine(), ""),
            ]
        ),

        Node(
            "SingleStmt",
            "",
            [
                Child("content", "stmt", InLine(), ""),
            ]
        ),

    ],

    "comprehension_constraints" : [
        Node(
            "ConsConstraint",
            "",
            [
                Child("head", "constraint", InLine(), ""),
                Child("tail", "comprehension_constraints", NewLine(), ""),
            ]
        ),

        Node(
            "SingleConstraint",
            "",
            [
                Child("content", "constraint", InLine(), ""),
            ]
        ),

    ],

    "sequence_ExceptHandler" : [
        Node(
            "ConsExceptHandler",
            "",
            [
                Child("head", "ExceptHandler", InLine(), ""),
                Child("tail", "sequence_ExceptHandler", NewLine(), ""),
            ]
        ),

        Node(
            "SingleExceptHandler",
            "",
            [
                Child("content", "ExceptHandler", InLine(), ""),
            ]
        ),

    ],

    "conditions" : [

        Node(
            "ElifCond",
            "",
            [
                Child("content", "ElifBlock", NewLine(), ""),
                Child("tail", "conditions", InLine(), ""),
            ]
        ),

        Node(
            "ElseCond",
            "",
            [
                Child("content", "ElseBlock", NewLine(), ""),
            ]
        ),

        Node(
            "NoCond",
            "",
            []
        )

    ],

    "function_def" : [
        Node(
            "FunctionDef",
            "def ",
            [ 
                Child("name", "Identifier", InLine(), "("),
                Child("params", "parameters", InLine(), ")"),
                Child("ret_typ", "return_type", InLine(), ":"),
                Child("body", "statements", IndentLine(), "")
            ]
        ),

        Node(
            "AsyncFunctionDef",
            "def ",
            [
                Child("name", "Identifier", InLine(), "("),
                Child("params", "parameters", InLine(), ")"),
                Child("ret_typ", "return_type", InLine(), ":"),
                Child("body", "statements", IndentLine(), "")
            ]
        ),
    ],


    "stmt" : [
        Node(
            "DecFunctionDef",
            "",
            [ 
                Child("decs", "decorators", InLine(), ""),
                Child("fun_def", "function_def", NewLine(), ""),
            ]
        ),

        Node(
            "DecAsyncFunctionDef",
            "",
            [
                Child("decs", "decorators", InLine(), ""),
                Child("fun_def", "function_def", NewLine(), ""),
            ]
        ),

        Node(
            "DecClassDef",
            "",
            [
                Child("decs", "decorators", InLine(), ""),
                Child("class_def", "ClassDef", NewLine(), ""),
            ]
        ),


        Node(
            "ReturnSomething",
            "return ", 
            [
                Child("content", "expr", InLine(), ""),
            ]
        ),

        Node(
            "Return",
            "return", 
            []
        ),

        Node(
            "Delete",
            "del",
            [
                Child("targets", "comma_exprs", InLine(), "")
            ]
        ),

        Node(
            "Assign",
            "",
            [
                Child("targets", "target_exprs", InLine(), " = "),
                Child("content", "expr", InLine(), "")
            ]
        ),

        Node(
            "AugAssign",
            "",
            [
                Child("target", "expr", InLine(), " "),
                Child("op", "operator", InLine(), "= "),
                Child("content", "expr", InLine(), "")
            ]
        ),

        Node(
            "TypedAssign", 
            "",
            [
                Child("target", "expr", InLine(), " : "),
                Child("type", "expr", InLine(), " = "),
                Child("content", "expr", InLine(), "")
            ],
        ),

        Node(
            "TypedDeclare", 
            "",
            [
                Child("target", "expr", InLine(), " : "),
                Child("type", "expr", InLine(), "")
            ],
        ),

        Node(
            "For",
            "for ",
            [
                Child("target", "expr", InLine(), " in "),
                Child("iter", "expr", InLine(), " : "),
                Child("body", "statements", IndentLine(), ""),
            ]
        ),

        Node(
            "ForElse",
            "for ",
            [
                Child("target", "expr", InLine(), " in "),
                Child("iter", "expr", InLine(), " : "),
                Child("body", "statements", IndentLine(), ""),
                Child("orelse", "ElseBlock", NewLine(), "")
            ]
        ),

        Node(
            "AsyncFor",
            "async for ",
            [
                Child("target", "expr", InLine(), " in "),
                Child("iter", "expr", InLine(), " : "),
                Child("body", "statements", IndentLine(), ""),
            ]
        ),

        Node(
            "AsyncForElse",
            "async for ",
            [
                Child("target", "expr", InLine(), " in "),
                Child("iter", "expr", InLine(), " : "),
                Child("body", "statements", IndentLine(), ""),
                Child("orelse", "ElseBlock", NewLine(), "")
            ]
        ),

        Node(
            "While",
            "while ",
            [
                Child("test", "expr", InLine(), ": "),
                Child("body", "statements", IndentLine(), ""),
            ]
        ),

        Node(
            "WhileElse",
            "while ",
            [
                Child("test", "expr", InLine(), ": "),
                Child("body", "statements", IndentLine(), ""),
                Child("orelse", "ElseBlock", NewLine(), "")
            ]
        ),

        Node(
            "If",
            "if ",
            [
                Child("test", "expr", InLine(), ": "),
                Child("body", "statements", IndentLine(), ""),
                Child("orelse", "conditions", InLine(), "")
            ]
        ),

        Node(
            "With",
            "with ",
            [
                Child("items", "sequence_Withitem", InLine(), ":"),
                Child("body", "statements", IndentLine(), "")
            ]
        ),

        Node(
            "AsyncWith",
            "async with ",
            [
                Child("items", "sequence_Withitem", InLine(), ":"),
                Child("body", "statements", IndentLine(), "")
            ]
        ),

        Node(
            "Raise",
            "raise",
            []
        ),

        Node(
            "RaiseExc",
            "raise ",
            [
                Child("exc", "expr", IndentLine(), ""),
            ]
        ),

        Node(
            "RaiseFrom",
            "raise ",
            [
                Child("exc", "expr", InLine(), " from "),
                Child("caus", "expr", InLine(), "")
            ]
        ),


        Node(
            "Try",
            "try:",
            [
                Child("body", "statements", IndentLine(), ""),
                Child("handlers", "sequence_ExceptHandler", NewLine(), ""),
            ]
        ),

        Node(
            "TryElse",
            "try:",
            [
                Child("body", "statements", IndentLine(), ""),
                Child("handlers", "sequence_ExceptHandler", NewLine(), ""),
                Child("orelse", "ElseBlock", NewLine(), ""),
            ]
        ),

        Node(
            "TryFin",
            "try:",
            [
                Child("body", "statements", IndentLine(), ""),
                Child("handlers", "sequence_ExceptHandler", NewLine(), ""),
                Child("fin", "FinallyBlock", NewLine(), "")
            ]
        ),

        Node(
            "TryElseFin",
            "try:",
            [
                Child("body", "statements", IndentLine(), ""),
                Child("handlers", "sequence_ExceptHandler", NewLine(), ""),
                Child("orelse", "ElseBlock", NewLine(), ""),
                Child("fin", "FinallyBlock", NewLine(), "")
            ]
        ),


        Node(
            "Assert",
            "assert ",
            [
                Child("test", "expr", InLine(), ""),
            ]
        ),

        Node(
            "AssertMsg",
            "assert ",
            [
                Child("test", "expr", InLine(), ", "),
                Child("msg", "expr", InLine(), "")
            ]
        ),



        Node(
            "Import",
            "import ",
            [
                Child("names", "sequence_ImportName", InLine(), "")
            ]
        ),

        Node(
            "ImportFrom",
            "from ",
            [
                Child("module", "module_id", InLine(), " import "),
                Child("names", "sequence_ImportName", InLine(), "")
            ]
        ),

        Node(
            "ImportWildCard",
            "from ",
            [
                Child("module", "module_id", InLine(), " import *"),
            ]
        ),

        Node(
            "Global",
            "global ",
            [
                Child("names", "sequence_Identifier", InLine(), "")
            ]
        ),

        Node(
            "Nonlocal",
            "nonlocal ",
            [
                Child("names", "sequence_Identifier", InLine(), "")
            ]
        ),

        Node(
            "Expr",
            "",
            [
                Child("content", "expr", InLine(), "")
            ]
        ),

        Node(
            "Pass",
            "pass",
            []
        ),

        Node(
            "Break",
            "break",
            []
        ),

        Node(
            "Continue",
            "continue",
            []
        ),

    ],

    "expr" : [

        Node(
            "BoolOp",
            "",
            [
                Child("left", "expr", InLine(), ""),
                Child("op", "boolop", InLine(), ""),
                Child("right", "expr", InLine(), "")
            ]
        ),

        Node(
            "NamedExpr",
            "",
            [
                Child("target", "expr", InLine(), " := "),
                Child("content", "expr", InLine(), "")
            ]
        ),

        Node(
            "BinOp",
            "(",
            [
                Child("left", "expr", InLine(), " "),
                Child("op", "operator", InLine(), " "),
                Child("right", "expr", InLine(), ")")
            ]
        ),

        Node(
            "UnaryOp",
            "",
            [
                Child("op", "unaryop", InLine(), " "),
                Child("right", "expr", InLine(), "")
            ]
        ),

        Node(
            "Lambda",
            "lambda ",
            [
                Child("params", "parameters", InLine(), " :"),
                Child("body", "expr", InLine(), "")
            ]
        ),

        Node(
            "IfExp",
            "",
            [
                Child("body", "expr", InLine(), "if "),
                Child("test", "expr", InLine(), " else"),
                Child("orelse", "expr", NewLine(), "")
            ]
        ),

        Node(
            "Dictionary",
            "{",
            [
                Child("contents", "dictionary_contents", IndentLine(), "}")
            ]
        ),

        Node(
            "EmptyDictionary",
            "{}",
            []
        ),

        Node(
            "Set",
            "{",
            [
                Child("contents", "comma_exprs", IndentLine(), "}")
            ]
        ),

        Node(
            "ListComp",
            "[",
            [
                Child("content", "expr", IndentLine(), ""),
                Child("constraints", "comprehension_constraints", IndentLine(), "]")
            ]
        ),

        Node(
            "SetComp",
            "{",
            [
                Child("content", "expr", IndentLine(), ""),
                Child("constraints", "comprehension_constraints", IndentLine(), "}")
            ]
        ),

        Node(
            "DictionaryComp",
            "{",
            [
                Child("key", "expr", IndentLine(), " : "),
                Child("content", "expr", InLine(), ""),
                Child("constraints", "comprehension_constraints", IndentLine(), "}")
            ]
        ),

        Node(
            "GeneratorExp",
            "(",
            [
                Child("content", "expr", IndentLine(), ""),
                Child("constraints", "comprehension_constraints", IndentLine(), ")")
            ]
        ),

        Node(
            "Await",
            "await ",
            [
                Child("content", "expr", InLine(), "")
            ]
        ),

        Node(
            "YieldNothing",
            "yield",
            []
        ),

        Node(
            "Yield",
            "yield ",
            [
                Child("content", "expr", InLine(), "")
            ]
        ),

        Node(
            "YieldFrom",
            "yield from ",
            [
                Child("content", "expr", InLine(), "")
            ]
        ),

        # need sequences for compare to distinguish between
        # x < 4 < 3 and (x < 4) < 3
        Node(
            "Compare",
            "",
            [
                Child("left", "expr", InLine(), " "),
                Child("comps", "comparisons", InLine(), "")
            ]
        ),

        Node(
            "Call",
            "",
            [
                Child("func", "expr", InLine(), "()"),
            ]
        ),

        Node(
            "CallArgs",
            "",
            [
                Child("func", "expr", InLine(), "("),
                Child("args", "arguments", InLine(), ")")
            ]
        ),

        Node(
            "Integer",
            "",
            [
                Child("content", "str", InLine(), "")
            ]
        ),

        Node(
            "Float",
            "",
            [
                Child("content", "str", InLine(), "")
            ]
        ),

        Node(
            "ConcatString",
            "",
            [
                Child("content", "sequence_str", InLine(), "")
            ]
        ),

        Node(
            "True_",
            "True",
            []
        ),

        Node(
            "False_",
            "False",
            []
        ),


        Node(
            "None_",
            "None",
            []
        ),

        Node(
            "Ellip",
            "...",
            []
        ),

        Node(
            "Attribute",
            "",
            [
                Child("content", "expr", InLine(), "."),
                Child("attr", "Identifier", InLine(), "")
            ]
        ),

        Node(
            "Subscript",
            "",
            [
                Child("content", "expr", InLine(), "["),
                Child("slice", "expr", InLine(), "]")
            ]
        ),

        Node(
            "Starred",
            "*",
            [
                Child("content", "expr", InLine(), ""),
            ]
        ),

        Node(
            "Name",
            "",
            [
                Child("id", "Identifier", InLine(), ""),
            ]
        ),

        Node(
            "List",
            "[",
            [
                Child("contents", "comma_exprs", InLine(), "]"),
            ]
        ),

        Node(
            "EmptyList",
            "[]",
            []
        ),

        Node(
            "Tuple",
            "(",
            [
                Child("contents", "comma_exprs", InLine(), ")"),
            ]
        ),

        Node(
            "EmptyTuple",
            "()",
            []
        ),

        Node(
            "Slice",
            "",
            [
                Child("lower", "option_expr", InLine(), ":"),
                Child("upper", "option_expr", InLine(), ":"),
                Child("step", "option_expr", InLine(), "")
            ]
        ),

    ],

    "boolop" : [
        Node(
            "And",
            "and",
            [] 
        ),

        Node(
            "Or",
            "or",
            [] 
        )
    ], 

    "operator" : [
        Node(
            "Add",
            "+",
            [] 
        ),

        Node(
            "Sub",
            "-",
            [] 
        ),

        Node(
            "Mult",
            "*",
            [] 
        ),

        Node(
            "MatMult",
            "@",
            [] 
        ),

        Node(
            "Div",
            "/",
            [] 
        ),

        Node(
            "Mod",
            "%",
            [] 
        ),

        Node(
            "Pow",
            "**",
            [] 
        ),

        Node(
            "LShift",
            "<<",
            [] 
        ),

        Node(
            "RShift",
            ">>",
            [] 
        ),

        Node(
            "BitOr",
            "|",
            [] 
        ),

        Node(
            "BitXor",
            "^",
            [] 
        ),

        Node(
            "BitAnd",
            "&",
            [] 
        ),

        Node(
            "FloorDiv",
            "//",
            [] 
        ),
    ],

    "unaryop" : [
        Node(
            "Invert",
            "~",
            [] 
        ),

        Node(
            "Not",
            "not",
            [] 
        ),

        Node(
            "UAdd",
            "+",
            [] 
        ),

        Node(
            "USub",
            "-",
            [] 
        ),
    ],

    "cmpop" : [
        Node(
            "Eq",
            "==",
            [] 
        ),

        Node(
            "NotEq",
            "!=",
            [] 
        ),

        Node(
            "Lt",
            "<",
            [] 
        ),

        Node(
            "LtE",
            "<=",
            [] 
        ),

        Node(
            "Gt",
            ">",
            [] 
        ),

        Node(
            "GtE",
            ">=",
            [] 
        ),

        Node(
            "Is",
            "is",
            [] 
        ),

        Node(
            "IsNot",
            "is not",
            [] 
        ),

        Node(
            "In",
            "in",
            [] 
        ),

        Node(
            "NotIn",
            "not in",
            [] 
        ),
    ],

    "constraint" : [

        Node(
            "AsyncConstraint",
            "async for ",
            [
                Child("target", "expr", InLine(), " in "),
                Child("search_space", "expr", InLine(), ""),
                Child("filts", "constraint_filters", InLine(), "")
            ] 
        ),

        Node(
            "Constraint",
            "for ",
            [
                Child("target", "expr", InLine(), " in "),
                Child("search_space", "expr", InLine(), ""),
                Child("filts", "constraint_filters", InLine(), "")
            ] 
        ),

    ]
}


intersections : list[Node] = [

    Node(
        "Module",
        "",
        [
            Child("body", "statements", InLine(), "")
        ]
    ),

    Node(
        "CompareRight",
        "",
        [
            Child("op", "cmpop", InLine(), " "),
            Child("rand", "expr", InLine(), "")
        ]
    ),

    Node(
        "ExceptHandler",
        "except ",
        [
            Child("arg", "except_arg", InLine(), ":"),
            Child("body", "statements", IndentLine(), "")
        ]
    ),

    Node(
        "Param",
        "",
        [
            Child("id", "Identifier", InLine(), ""),
            Child("type", "param_type", InLine(), ""),
            Child("default", "param_default", InLine(), "")
        ]
    ),

    Node(
        "Field",
        "",
        [
            Child("key", "expr", InLine(), " : "),
            Child("content", "expr", InLine(), "")
        ]
    ),

    Node(
        "ImportName",
        "",
        [
            Child("name", "Identifier", InLine(), ""),
            Child("as_name", "alias", InLine(), "")
        ]
    ),


    Node(
        "Identifier",
        "",
        [
            Child("symbol", "str", InLine(), "")
        ]
    ),

    Node(
        "Withitem",
        "",
        [
            Child("contet", "expr", InLine(), " as "),
            Child("target", "alias_expr", InLine(), "")
        ]
    ),

    Node(
        "ClassDef",
        "class ",
        [
            Child("name", "Identifier", InLine(), ""),
            Child("bs", "bases", InLine(), ":"), 
            Child("body", "statements", IndentLine(), "")
        ]
    ),

    Node(
        "ElifBlock",
        "elif ",
        [
            Child("test", "expr", InLine(), ":"),
            Child("body", "statements", IndentLine(), ""),
        ]
    ),

    Node(
        "ElseBlock",
        "else:",
        [
            Child("body", "statements", IndentLine(), ""),
        ]
    ),

    Node(
        "FinallyBlock",
        "finally:",
        [
            Child("body", "statements", IndentLine(), ""),
        ]
    )


]

node_map = {
    node.name : node 
    for node in intersections
} | {
    node.name : node 
    for nodes in unions.values()
    for node in nodes 
}

grammar_dictionary = {
    node.name : [schema.to_dictionary(node)]
    for node in intersections
} | {
    name : [schema.to_dictionary(node) for node in nodes]
    for name, nodes in unions.items()
}


def format() -> str:

    ### rule of non-terminal ###

    rule_of_nonterm_unions = [
        k + " : " + choices_str 
        for k, choices in unions.items()
        for choices_str in [ ' | '.join([
            ck.name
            for ck in choices
        ])]
    ]

    import inflection
    rule_of_nonterm_intersections = [
        node.name + " : " + node.name
        for node in intersections
    ]


    rule_of_nonterm_str = "---- RULE OF NON-TERMINAL ----\n\n" + (
        "\n".join(rule_of_nonterm_unions) + 
        "\n" + 
        "\n".join(rule_of_nonterm_intersections) + 
        "\n" 
    )

    from lib import line_format

    ### rule of sequence ###
    rule_of_sequence_unions = [
        k + " :: " + f"`{choice.leader}`" + " " + fields_str 
        for choices in unions.values()
        for choice in choices
        for k in [choice.name]
        for fields_str in [' '.join([
            "(" + lf + ' : ' + name + ' : ' + ('symbol' if typ == 'str' else typ) + ") " + f"`{fol}`"
            for child in choice.children
            for name, typ in [(child.attr, child.typ)]
            for lf in [line_format.to_string(child.line_form)]
            for fol in [child.follower]
        ])]
    ]

    rule_of_sequence_intersections = [
        k + " :: " + f"`{constructor.leader}`" + " " + fields_str 
        for constructor in intersections
        for k in [constructor.name]
        for fields_str in [' '.join([
            "(" + lf + ' : ' + name + ' : ' + ('symbol' if typ == 'str' else typ) + ") " + f"`{fol}`"
            for child in constructor.children
            for name, typ in [(child.attr, child.typ)]
            for lf in [line_format.to_string(child.line_form)]
            for fol in [child.follower]
        ])]
    ]

    rule_of_sequence_str = "---- RULE OF SEQUENCE ----\n\n" + (
        "\n".join(rule_of_sequence_unions) + 
        "\n" + 
        "\n".join(rule_of_sequence_intersections) + 
        "\n"
    )


    return rule_of_nonterm_str + "\n\n" + rule_of_sequence_str