from __future__ import annotations
from gen.schema import ChildHandlers

from lib.schema import Node, Vocab, Grammar
from lib import schema
from gen.line_format import NewLine, InLine, IndentLine


unions : dict[str, list[Node]] = {

    "return_type" : [

        Node(
            "SomeReturnType",
            " -> ",
            [
                Grammar("content", "expr", InLine(), "")
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
                Vocab("content", "module_name", "")
            ]
        ),

        Node(
            "NoModuleId",
            ".",
            []
        )
    ],

    "except_arg" : [
        Node(
            "SomeExceptArg",
            " ",
            [
                Grammar("content", "expr", InLine(), "")
            ]
        ),

        Node(
            "SomeExceptArgName",
            " ",
            [
                Grammar("content", "expr", InLine(), " as "),
                Vocab("name", "var", ""),
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
                Grammar("content", "expr", InLine(), ""),
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
                Grammar("content", "expr", InLine(), ""),
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
                Grammar("head", "Param", InLine(), ", "),
                Grammar("tail", "parameters_d", InLine(), ""),
            ]
        ),

        Node(
            "SingleKwParam",
            "",
            [
                Grammar("content", "Param", InLine(), ""),
            ]
        ),

        Node(
            "DictionarySplatParam",
            "**",
            [
                Grammar("content", "Param", InLine(), "")
            ]
        )

    ],

    "parameters_c" : [
        Node(
            "SingleListSplatParam",
            "*",
            [
                Grammar("content", "Param", InLine(), ""),
            ]
        ),

        Node(
            "TransListSplatParam",
            "*",
            [
                Grammar("head", "Param", InLine(), ", "),
                Grammar("tail", "parameters_d", InLine(), ""),
            ]
        ),

        Node(
            "ParamsD",
            "*, ",
            [
                Grammar("content", "parameters_d", InLine(), ""),
            ]
        ),
    ],

    "parameters_b" : [
        Node(
            "ConsParam",
            "",
            [
                Grammar("head", "Param", InLine(), ", "),
                Grammar("tail", "parameters_b", InLine(), ""),
            ]
        ),

        Node(
            "SingleParam",
            "",
            [
                Grammar("content", "Param", InLine(), ""),
            ]
        ),

        Node(
            "ParamsC",
            "",
            [
                Grammar("content", "parameters_c", InLine(), ""),
            ]
        ),

    ],

    "parameters" : [
        Node(
            "ParamsA",
            "",
            [
                Grammar("content", "parameters_a", InLine(), ""),
            ]
        ),


        Node(
            "ParamsB",
            "",
            [
                Grammar("content", "parameters_b", InLine(), "")
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
                Grammar("head", "Param", InLine(), ", "),
                Grammar("tail", "parameters_a", InLine(), ""),
            ]
        ),

        Node(
            "SinglePosParam",
            "",
            [
                Grammar("content", "Param", InLine(), ", /"),
            ]
        ),

        Node(
            "TransPosParam",
            "",
            [
                Grammar("head", "Param", InLine(), ", /, "),
                Grammar("tail", "parameters_b", InLine(), ""),
            ]
        )

    ],


    "keyword" : [

        Node(
            "NamedKeyword",
            "",
            [
                Vocab("name", "var", " = "),
                Grammar("content", "expr", InLine(), "")
            ]
        ),

        Node(
            "SplatKeyword",
            "**",
            [
                Grammar("content", "expr", InLine(), "")
            ]
        ),
    ],

    "alias" : [

        Node(
            "SomeAlias",
            " as ",
            [
                Vocab("content", "var", "")
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
                Grammar("content", "expr", InLine(), "")
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
                Grammar("bases", "bases_a", InLine(), ")")
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
                Grammar("head", "expr", InLine(), ", "),
                Grammar("tail", "bases_a", InLine(), ""),
            ]
        ),

        Node(
            "SingleBase",
            "",
            [
                Grammar("content", "expr", InLine(), ""),
            ]
        ),

        Node(
            "KeywordsBase",
            "",
            [
                Grammar("kws", "keywords", InLine(), "")
            ]
        ),

    ],

    "keywords" : [
        Node(
            "ConsKeyword",
            "",
            [
                Grammar("head", "keyword", InLine(), ", "),
                Grammar("tail", "keywords", InLine(), ""),
            ]
        ),

        Node(
            "SingleKeyword",
            "",
            [
                Grammar("content", "keyword", InLine(), ""),
            ]
        ),

    ],

    "comparisons" : [
        Node(
            "ConsCompareRight",
            "",
            [
                Grammar("head", "CompareRight", InLine(), " "),
                Grammar("tail", "comparisons", InLine(), ""),
            ]
        ),

        Node(
            "SingleCompareRight",
            "",
            [
                Grammar("content", "CompareRight", InLine(), ""),
            ]
        ),

    ],

    "option_expr" : [
        Node(
            "SomeExpr",
            "",
            [
                Grammar("content", "expr", InLine(), ""),
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
                Grammar("head", "expr", InLine(), ", "),
                Grammar("tail", "comma_exprs", InLine(), ""),
            ]
        ),

        Node(
            "SingleExpr",
            "",
            [
                Grammar("content", "expr", InLine(), ""),
            ]
        ),

    ],

    "target_exprs" : [
        Node(
            "ConsTargetExpr",
            "",
            [
                Grammar("head", "expr", InLine(), " = "),
                Grammar("tail", "target_exprs", InLine(), ""),
            ]
        ),

        Node(
            "SingleTargetExpr",
            "",
            [
                Grammar("content", "expr", InLine(), ""),
            ]
        ),

    ],

    "decorators" : [
        Node(
            "ConsDec",
            "@",
            [
                Grammar("head", "expr", InLine(), ""),
                Grammar("tail", "decorators", InLine(), ""),
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
                Grammar("head", "expr", NewLine(), ""),
                Grammar("tail", "constraint_filters", InLine(), ""),
            ]
        ),

        Node(
            "SingleFilter",
            "if ",
            [
                Grammar("content", "expr", NewLine(), ""),
            ]
        ),

        Node(
            "NoFilter",
            "",
            [
            ]
        ),

    ],

    "sequence_string" : [
        Node(
            "ConsStr",
            "",
            [
                Vocab("head", "string", " "),
                Grammar("tail", "sequence_string", InLine(), ""),
            ]
        ),

        Node(
            "SingleStr",
            "",
            [
                Vocab("content", "string", ""),
            ]
        ),

    ],

    "arguments" : [
        Node(
            "ConsArg",
            "",
            [
                Grammar("head", "expr", InLine(), ", "),
                Grammar("tail", "arguments", InLine(), ""),
            ]
        ),

        Node(
            "SingleArg",
            "",
            [
                Grammar("content", "expr", InLine(), ""),
            ]
        ),

        Node(
            "KeywordsArg",
            "",
            [
                Grammar("kws", "keywords", InLine(), ""),
            ]
        ),

    ],

    "dictionary_contents" : [
        Node(
            "ConsField",
            "",
            [
                Grammar("head", "Field", InLine(), ", "),
                Grammar("tail", "dictionary_contents", NewLine(), ""),
            ]
        ),

        Node(
            "SingleField",
            "",
            [
                Grammar("content", "Field", InLine(), ""),
            ]
        ),

    ],

    "sequence_var" : [
        Node(
            "ConsId",
            "",
            [
                Vocab("head", "var", ", "),
                Grammar("tail", "sequence_var", InLine(), ""),
            ]
        ),

        Node(
            "SingleId",
            "",
            [
                Vocab("content", "var", ""),
            ]
        ),

    ],


    "sequence_ImportName" : [
        Node(
            "ConsImportName",
            "",
            [
                Grammar("head", "ImportName", InLine(), ", "),
                Grammar("tail", "sequence_ImportName", InLine(), ""),
            ]
        ),

        Node(
            "SingleImportName",
            "",
            [
                Grammar("content", "ImportName", InLine(), ""),
            ]
        ),

    ],

    "sequence_Withitem" : [
        Node(
            "ConsWithitem",
            "",
            [
                Grammar("head", "Withitem", InLine(), ", "),
                Grammar("tail", "sequence_Withitem", InLine(), ""),
            ]
        ),

        Node(
            "SingleWithitem",
            "",
            [
                Grammar("content", "Withitem", InLine(), ""),
            ]
        ),

    ],


    "statements" : [
        Node(
            "ConsStmt",
            "",
            [
                Grammar("head", "stmt", InLine(), ""),
                Grammar("tail", "statements", NewLine(), ""),
            ]
        ),

        Node(
            "SingleStmt",
            "",
            [
                Grammar("content", "stmt", InLine(), ""),
            ]
        ),

    ],

    "comprehension_constraints" : [
        Node(
            "ConsConstraint",
            "",
            [
                Grammar("head", "constraint", InLine(), ""),
                Grammar("tail", "comprehension_constraints", NewLine(), ""),
            ]
        ),

        Node(
            "SingleConstraint",
            "",
            [
                Grammar("content", "constraint", InLine(), ""),
            ]
        ),

    ],

    "sequence_ExceptHandler" : [
        Node(
            "ConsExceptHandler",
            "",
            [
                Grammar("head", "ExceptHandler", InLine(), ""),
                Grammar("tail", "sequence_ExceptHandler", NewLine(), ""),
            ]
        ),

        Node(
            "SingleExceptHandler",
            "",
            [
                Grammar("content", "ExceptHandler", InLine(), ""),
            ]
        ),

    ],

    "conditions" : [

        Node(
            "ElifCond",
            "",
            [
                Grammar("content", "ElifBlock", NewLine(), ""),
                Grammar("tail", "conditions", InLine(), ""),
            ]
        ),

        Node(
            "ElseCond",
            "",
            [
                Grammar("content", "ElseBlock", NewLine(), ""),
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
                Vocab("name", "function_name", "("),
                Grammar("params", "parameters", InLine(), ")"),
                Grammar("ret_typ", "return_type", InLine(), ":"),
                Grammar("body", "statements", IndentLine(), "")
            ]
        ),

        Node(
            "AsyncFunctionDef",
            "def ",
            [
                Vocab("name", "function_name", "("),
                Grammar("params", "parameters", InLine(), ")"),
                Grammar("ret_typ", "return_type", InLine(), ":"),
                Grammar("body", "statements", IndentLine(), "")
            ]
        ),
    ],


    "stmt" : [
        Node(
            "DecFunctionDef",
            "",
            [ 
                Grammar("decs", "decorators", InLine(), ""),
                Grammar("fun_def", "function_def", NewLine(), ""),
            ]
        ),

        Node(
            "DecAsyncFunctionDef",
            "",
            [
                Grammar("decs", "decorators", InLine(), ""),
                Grammar("fun_def", "function_def", NewLine(), ""),
            ]
        ),

        Node(
            "DecClassDef",
            "",
            [
                Grammar("decs", "decorators", InLine(), ""),
                Grammar("class_def", "ClassDef", NewLine(), ""),
            ]
        ),


        Node(
            "ReturnSomething",
            "return ", 
            [
                Grammar("content", "expr", InLine(), ""),
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
                Grammar("targets", "comma_exprs", InLine(), "")
            ]
        ),

        Node(
            "Assign",
            "",
            [
                Grammar("targets", "target_exprs", InLine(), " = "),
                Grammar("content", "expr", InLine(), "")
            ]
        ),

        Node(
            "AugAssign",
            "",
            [
                Grammar("target", "expr", InLine(), " "),
                Grammar("op", "operator", InLine(), "= "),
                Grammar("content", "expr", InLine(), "")
            ]
        ),

        Node(
            "TypedAssign", 
            "",
            [
                Grammar("target", "expr", InLine(), " : "),
                Grammar("type", "expr", InLine(), " = "),
                Grammar("content", "expr", InLine(), "")
            ],
        ),

        Node(
            "TypedDeclare", 
            "",
            [
                Grammar("target", "expr", InLine(), " : "),
                Grammar("type", "expr", InLine(), "")
            ],
        ),

        Node(
            "For",
            "for ",
            [
                Grammar("target", "expr", InLine(), " in "),
                Grammar("iter", "expr", InLine(), " : "),
                Grammar("body", "statements", IndentLine(), ""),
            ]
        ),

        Node(
            "ForElse",
            "for ",
            [
                Grammar("target", "expr", InLine(), " in "),
                Grammar("iter", "expr", InLine(), " : "),
                Grammar("body", "statements", IndentLine(), ""),
                Grammar("orelse", "ElseBlock", NewLine(), "")
            ]
        ),

        Node(
            "AsyncFor",
            "async for ",
            [
                Grammar("target", "expr", InLine(), " in "),
                Grammar("iter", "expr", InLine(), " : "),
                Grammar("body", "statements", IndentLine(), ""),
            ]
        ),

        Node(
            "AsyncForElse",
            "async for ",
            [
                Grammar("target", "expr", InLine(), " in "),
                Grammar("iter", "expr", InLine(), " : "),
                Grammar("body", "statements", IndentLine(), ""),
                Grammar("orelse", "ElseBlock", NewLine(), "")
            ]
        ),

        Node(
            "While",
            "while ",
            [
                Grammar("test", "expr", InLine(), ": "),
                Grammar("body", "statements", IndentLine(), ""),
            ]
        ),

        Node(
            "WhileElse",
            "while ",
            [
                Grammar("test", "expr", InLine(), ": "),
                Grammar("body", "statements", IndentLine(), ""),
                Grammar("orelse", "ElseBlock", NewLine(), "")
            ]
        ),

        Node(
            "If",
            "if ",
            [
                Grammar("test", "expr", InLine(), ": "),
                Grammar("body", "statements", IndentLine(), ""),
                Grammar("orelse", "conditions", InLine(), "")
            ]
        ),

        Node(
            "With",
            "with ",
            [
                Grammar("items", "sequence_Withitem", InLine(), ":"),
                Grammar("body", "statements", IndentLine(), "")
            ]
        ),

        Node(
            "AsyncWith",
            "async with ",
            [
                Grammar("items", "sequence_Withitem", InLine(), ":"),
                Grammar("body", "statements", IndentLine(), "")
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
                Grammar("exc", "expr", IndentLine(), ""),
            ]
        ),

        Node(
            "RaiseFrom",
            "raise ",
            [
                Grammar("exc", "expr", InLine(), " from "),
                Grammar("caus", "expr", InLine(), "")
            ]
        ),


        Node(
            "Try",
            "try:",
            [
                Grammar("body", "statements", IndentLine(), ""),
                Grammar("handlers", "sequence_ExceptHandler", NewLine(), ""),
            ]
        ),

        Node(
            "TryElse",
            "try:",
            [
                Grammar("body", "statements", IndentLine(), ""),
                Grammar("handlers", "sequence_ExceptHandler", NewLine(), ""),
                Grammar("orelse", "ElseBlock", NewLine(), ""),
            ]
        ),

        Node(
            "TryFin",
            "try:",
            [
                Grammar("body", "statements", IndentLine(), ""),
                Grammar("handlers", "sequence_ExceptHandler", NewLine(), ""),
                Grammar("fin", "FinallyBlock", NewLine(), "")
            ]
        ),

        Node(
            "TryElseFin",
            "try:",
            [
                Grammar("body", "statements", IndentLine(), ""),
                Grammar("handlers", "sequence_ExceptHandler", NewLine(), ""),
                Grammar("orelse", "ElseBlock", NewLine(), ""),
                Grammar("fin", "FinallyBlock", NewLine(), "")
            ]
        ),


        Node(
            "Assert",
            "assert ",
            [
                Grammar("test", "expr", InLine(), ""),
            ]
        ),

        Node(
            "AssertMsg",
            "assert ",
            [
                Grammar("test", "expr", InLine(), ", "),
                Grammar("msg", "expr", InLine(), "")
            ]
        ),



        Node(
            "Import",
            "import ",
            [
                Grammar("names", "sequence_ImportName", InLine(), "")
            ]
        ),

        Node(
            "ImportFrom",
            "from ",
            [
                Grammar("module", "module_id", InLine(), " import "),
                Grammar("names", "sequence_ImportName", InLine(), "")
            ]
        ),

        Node(
            "ImportWildCard",
            "from ",
            [
                Grammar("module", "module_id", InLine(), " import *"),
            ]
        ),

        Node(
            "Global",
            "global ",
            [
                Grammar("names", "sequence_var", InLine(), "")
            ]
        ),

        Node(
            "Nonlocal",
            "nonlocal ",
            [
                Grammar("names", "sequence_var", InLine(), "")
            ]
        ),

        Node(
            "Expr",
            "",
            [
                Grammar("content", "expr", InLine(), "")
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
                Grammar("left", "expr", InLine(), " "),
                Grammar("op", "boolop", InLine(), " "),
                Grammar("right", "expr", InLine(), "")
            ]
        ),

        Node(
            "NamedExpr",
            "",
            [
                Grammar("target", "expr", InLine(), " := "),
                Grammar("content", "expr", InLine(), "")
            ]
        ),

        Node(
            "BinOp",
            "(",
            [
                Grammar("left", "expr", InLine(), " "),
                Grammar("op", "operator", InLine(), " "),
                Grammar("right", "expr", InLine(), ")")
            ]
        ),

        Node(
            "UnaryOp",
            "",
            [
                Grammar("op", "unaryop", InLine(), " "),
                Grammar("right", "expr", InLine(), "")
            ]
        ),

        Node(
            "Lambda",
            "lambda ",
            [
                Grammar("params", "parameters", InLine(), " :"),
                Grammar("body", "expr", InLine(), "")
            ]
        ),

        Node(
            "IfExp",
            "",
            [
                Grammar("body", "expr", InLine(), "if "),
                Grammar("test", "expr", InLine(), " else"),
                Grammar("orelse", "expr", NewLine(), "")
            ]
        ),

        Node(
            "Dictionary",
            "{",
            [
                Grammar("contents", "dictionary_contents", IndentLine(), "}")
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
                Grammar("contents", "comma_exprs", IndentLine(), "}")
            ]
        ),

        Node(
            "ListComp",
            "[",
            [
                Grammar("content", "expr", IndentLine(), ""),
                Grammar("constraints", "comprehension_constraints", IndentLine(), "]")
            ]
        ),

        Node(
            "SetComp",
            "{",
            [
                Grammar("content", "expr", IndentLine(), ""),
                Grammar("constraints", "comprehension_constraints", IndentLine(), "}")
            ]
        ),

        Node(
            "DictionaryComp",
            "{",
            [
                Grammar("key", "expr", IndentLine(), " : "),
                Grammar("content", "expr", InLine(), ""),
                Grammar("constraints", "comprehension_constraints", IndentLine(), "}")
            ]
        ),

        Node(
            "GeneratorExp",
            "(",
            [
                Grammar("content", "expr", IndentLine(), ""),
                Grammar("constraints", "comprehension_constraints", IndentLine(), ")")
            ]
        ),

        Node(
            "Await",
            "await ",
            [
                Grammar("content", "expr", InLine(), "")
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
                Grammar("content", "expr", InLine(), "")
            ]
        ),

        Node(
            "YieldFrom",
            "yield from ",
            [
                Grammar("content", "expr", InLine(), "")
            ]
        ),

        # need sequences for compare to distinguish between
        # x < 4 < 3 and (x < 4) < 3
        Node(
            "Compare",
            "",
            [
                Grammar("left", "expr", InLine(), " "),
                Grammar("comps", "comparisons", InLine(), "")
            ]
        ),

        Node(
            "Call",
            "",
            [
                Grammar("func", "expr", InLine(), "()"),
            ]
        ),

        Node(
            "CallArgs",
            "",
            [
                Grammar("func", "expr", InLine(), "("),
                Grammar("args", "arguments", InLine(), ")")
            ]
        ),

        Node(
            "Integer",
            "",
            [
                Vocab("content", "integer", "")
            ]
        ),

        Node(
            "Float",
            "",
            [
                Vocab("content", "float", "")
            ]
        ),

        Node(
            "ConcatString",
            "",
            [
                Grammar("content", "sequence_string", InLine(), "")
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
                Grammar("content", "expr", InLine(), "."),
                Vocab("attr", "attribute", "")
            ]
        ),

        Node(
            "Subscript",
            "",
            [
                Grammar("content", "expr", InLine(), "["),
                Grammar("slice", "expr", InLine(), "]")
            ]
        ),

        Node(
            "Starred",
            "*",
            [
                Grammar("content", "expr", InLine(), ""),
            ]
        ),

        Node(
            "Name",
            "",
            [
                Vocab("id", "var", ""),
            ]
        ),

        Node(
            "List",
            "[",
            [
                Grammar("contents", "comma_exprs", InLine(), "]"),
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
                Grammar("contents", "comma_exprs", InLine(), ")"),
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
                Grammar("lower", "option_expr", InLine(), ":"),
                Grammar("upper", "option_expr", InLine(), ":"),
                Grammar("step", "option_expr", InLine(), "")
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
                Grammar("target", "expr", InLine(), " in "),
                Grammar("search_space", "expr", InLine(), ""),
                Grammar("filts", "constraint_filters", InLine(), "")
            ] 
        ),

        Node(
            "Constraint",
            "for ",
            [
                Grammar("target", "expr", InLine(), " in "),
                Grammar("search_space", "expr", InLine(), ""),
                Grammar("filts", "constraint_filters", InLine(), "")
            ] 
        ),

    ]
}


intersections : list[Node] = [

    Node(
        "Module",
        "",
        [
            Grammar("body", "statements", InLine(), "")
        ]
    ),

    Node(
        "CompareRight",
        "",
        [
            Grammar("op", "cmpop", InLine(), " "),
            Grammar("rand", "expr", InLine(), "")
        ]
    ),

    Node(
        "ExceptHandler",
        "except ",
        [
            Grammar("arg", "except_arg", InLine(), ":"),
            Grammar("body", "statements", IndentLine(), "")
        ]
    ),

    Node(
        "Param",
        "",
        [
            Vocab("id", "param_name", ""),
            Grammar("type", "param_type", InLine(), ""),
            Grammar("default", "param_default", InLine(), "")
        ]
    ),

    Node(
        "Field",
        "",
        [
            Grammar("key", "expr", InLine(), " : "),
            Grammar("content", "expr", InLine(), "")
        ]
    ),

    Node(
        "ImportName",
        "",
        [
            Vocab("name", "module_identifier", ""),
            Grammar("as_name", "alias", InLine(), "")
        ]
    ),


    Node(
        "Withitem",
        "",
        [
            Grammar("contet", "expr", InLine(), ""),
            Grammar("target", "alias_expr", InLine(), "")
        ]
    ),

    Node(
        "ClassDef",
        "class ",
        [
            Vocab("name", "class_name", ""),
            Grammar("bs", "bases", InLine(), ":"), 
            Grammar("body", "statements", IndentLine(), "")
        ]
    ),

    Node(
        "ElifBlock",
        "elif ",
        [
            Grammar("test", "expr", InLine(), ":"),
            Grammar("body", "statements", IndentLine(), ""),
        ]
    ),

    Node(
        "ElseBlock",
        "else:",
        [
            Grammar("body", "statements", IndentLine(), ""),
        ]
    ),

    Node(
        "FinallyBlock",
        "finally:",
        [
            Grammar("body", "statements", IndentLine(), ""),
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

    def make_field_str(child : schema.child) -> str:
        return schema.match_child(child, ChildHandlers[str](
            case_Grammar=lambda o : (
                lf := line_format.to_string(o.format),
                fol := o.follower,
                "(grammar " + lf + ' : ' + o.relation + ' : ' + o.nonterminal + ") " + f"`{fol}`"
            )[-1],
            case_Vocab=lambda o : (
                "(vocab : " + o.relation + ' : ' + o.choices_id + ")" 
            )
        ))

    ### rule of sequence ###
    rule_of_sequence_unions = [
        k + " :: " + f"`{choice.leader}`" + " " + fields_str 
        for choices in unions.values()
        for choice in choices
        for k in [choice.name]
        for fields_str in [' '.join([
            make_field_str(child)
            for child in choice.children
        ])]
    ]

    rule_of_sequence_intersections = [
        k + " :: " + f"`{constructor.leader}`" + " " + fields_str 
        for constructor in intersections
        for k in [constructor.name]
        for fields_str in [' '.join([
            make_field_str(child)
            for child in constructor.children
        ])]
    ]

    rule_of_sequence_string = "---- RULE OF SEQUENCE ----\n\n" + (
        "\n".join(rule_of_sequence_unions) + 
        "\n" + 
        "\n".join(rule_of_sequence_intersections) + 
        "\n"
    )


    return rule_of_nonterm_str + "\n\n" + rule_of_sequence_string