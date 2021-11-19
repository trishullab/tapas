from __future__ import annotations
from gen.schema import ChildHandlers

from lib.schema import Node, Vocab, Terminal, Nonterm 
from lib import schema
from gen.line_format import NewLine, InLine, IndentLine


choices : dict[str, list[Node]] = {

    "return_type" : [

        Node(
            "SomeReturnType",
            [
                Terminal(" -> "),
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Node(
            "NoReturnType",
            []
        )
    ],

    "module_id" : [

        Node(
            "SomeModuleId",
            [
                Vocab("contents", "module_identifier")
            ]
        ),

        Node(
            "NoModuleId",
            [
                Terminal(".")
            ]
        )
    ],

    "except_arg" : [
        Node(
            "SomeExceptArg",
            [
                Terminal(" "),
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Node(
            "SomeExceptArgName",
            [
                Terminal(" "),
                Nonterm("contents", "expr", InLine()),
                Terminal(" as "),
                Vocab("name", "identifier"),
            ]
        ),

        Node(
            "NoExceptArg",
            []
        )
    ],

    "param_type" : [
        Node(
            "SomeParamType",
            [
                Terminal(" : "),
                Nonterm("contents", "expr", InLine()),
            ]
        ),

        Node(
            "NoParamType",
            []
        ),
    ],

    "param_default" : [
        Node(
            "SomeParamDefault",
            [
                Terminal(" = "),
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Node(
            "NoParamDefault",
            []
        ),
    ],

    "parameters_d" : [
        Node(
            "ConsKwParam",
            [
                Nonterm("head", "Param", InLine()),
                Terminal(", "),
                Nonterm("tail", "parameters_d", InLine())
            ]
        ),

        Node(
            "SingleKwParam",
            [
                Nonterm("contents", "Param", InLine())
            ]
        ),

        Node(
            "DictionarySplatParam",
            [
                Terminal("**"),
                Nonterm("contents", "Param", InLine())
            ]
        )

    ],

    "parameters_c" : [
        Node(
            "SingleListSplatParam",
            [
                Terminal("*"),
                Nonterm("contents", "Param", InLine())
            ]
        ),

        Node(
            "TransListSplatParam",
            [
                Terminal("*"),
                Nonterm("head", "Param", InLine()),
                Terminal(", "),
                Nonterm("tail", "parameters_d", InLine())
            ]
        ),

        Node(
            "ParamsD",
            [
                Terminal("*, "),
                Nonterm("contents", "parameters_d", InLine())
            ]
        ),
    ],

    "parameters_b" : [
        Node(
            "ConsParam",
            [
                Nonterm("head", "Param", InLine()),
                Terminal(", "),
                Nonterm("tail", "parameters_b", InLine())
            ]
        ),

        Node(
            "SingleParam",
            [
                Nonterm("contents", "Param", InLine())
            ]
        ),

        Node(
            "ParamsC",
            [
                Nonterm("contents", "parameters_c", InLine())
            ]
        ),

    ],

    "parameters" : [
        Node(
            "ParamsA",
            [
                Nonterm("contents", "parameters_a", InLine())
            ]
        ),


        Node(
            "ParamsB",
            [
                Nonterm("contents", "parameters_b", InLine())
            ]
        ),

        Node(
            "NoParam",
            []
        )
    ],


    "parameters_a" : [
        Node(
            "ConsPosParam",
            [
                Nonterm("head", "Param", InLine()),
                Terminal(", "),
                Nonterm("tail", "parameters_a", InLine())
            ]
        ),

        Node(
            "SinglePosParam",
            [
                Nonterm("contents", "Param", InLine()),
                Terminal(", /")
            ]
        ),

        Node(
            "TransPosParam",
            [
                Nonterm("head", "Param", InLine()),
                Terminal(", /, "),
                Nonterm("tail", "parameters_b", InLine()),
            ]
        )

    ],


    "keyword" : [

        Node(
            "NamedKeyword",
            [
                Vocab("name", "identifier"),
                Terminal(" = "),
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Node(
            "SplatKeyword",
            [
                Terminal("**"),
                Nonterm("contents", "expr", InLine())
            ]
        ),
    ],

    "alias" : [

        Node(
            "SomeAlias",
            [
                Terminal(" as "),
                Vocab("contents", "identifier")
            ]
        ),

        Node(
            "NoAlias",
            []
        ),

    ],

    "alias_expr" : [

        Node(
            "SomeAliasExpr",
            [
                Terminal(" as "),
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Node(
            "NoAliasExpr",
            []
        ),

    ],

    "bases" : [
        Node(
            "SomeBases",
            [
                Terminal("("),
                Nonterm("bases", "bases_a", InLine()),
                Terminal(")")
            ]
        ),

        Node(
            "NoBases",
            []
        )
    ],

    "bases_a" : [
        Node(
            "ConsBase",
            [
                Nonterm("head", "expr", InLine()),
                Terminal(", "),
                Nonterm("tail", "bases_a", InLine()),
            ]
        ),

        Node(
            "SingleBase",
            [
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Node(
            "KeywordsBase",
            [
                Nonterm("kws", "keywords", InLine())
            ]
        ),

    ],

    "keywords" : [
        Node(
            "ConsKeyword",
            [
                Nonterm("head", "keyword", InLine()),
                Terminal(", "),
                Nonterm("tail", "keywords", InLine()),
            ]
        ),

        Node(
            "SingleKeyword",
            [
                Nonterm("contents", "keyword", InLine()),
            ]
        ),

    ],

    "comparisons" : [
        Node(
            "ConsCompareRight",
            [
                Nonterm("head", "CompareRight", InLine()),
                Terminal(" "),
                Nonterm("tail", "comparisons", InLine()),
            ]
        ),

        Node(
            "SingleCompareRight",
            [
                Nonterm("contents", "CompareRight", InLine())
            ]
        ),

    ],

    "option_expr" : [
        Node(
            "SomeExpr",
            [
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Node(
            "NoExpr",
            []
        )
    ],


    "comma_exprs" : [
        Node(
            "ConsExpr",
            [
                Nonterm("head", "expr", InLine()),
                Terminal(", "),
                Nonterm("tail", "comma_exprs", InLine())
            ]
        ),

        Node(
            "SingleExpr",
            [
                Nonterm("contents", "expr", InLine())
            ]
        ),

    ],

    "target_exprs" : [
        Node(
            "ConsTargetExpr",
            [
                Nonterm("head", "expr", InLine()),
                Terminal(" = "),
                Nonterm("tail", "target_exprs", InLine()),
            ]
        ),

        Node(
            "SingleTargetExpr",
            [
                Nonterm("contents", "expr", InLine())
            ]
        ),

    ],

    "decorators" : [
        Node(
            "ConsDec",
            [
                Terminal("@"),
                Nonterm("head", "expr", InLine()),
                Nonterm("tail", "decorators", InLine())
            ]
        ),

        Node(
            "NoDec",
            []
        ),

    ],

    "constraint_filters" : [
        Node(
            "ConsFilter",
            [
                Terminal("if "),
                Nonterm("head", "expr", InLine()),
                Nonterm("tail", "constraint_filters", NewLine())
            ]
        ),

        Node(
            "SingleFilter",
            [
                Terminal("if "),
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Node(
            "NoFilter",
            []
        ),

    ],

    "sequence_string" : [
        Node(
            "ConsStr",
            [
                Vocab("head", "string"),
                Terminal(" "),
                Nonterm("tail", "sequence_string", InLine()),
            ]
        ),

        Node(
            "SingleStr",
            [
                Vocab("contents", "string"),
            ]
        ),

    ],

    "arguments" : [
        Node(
            "ConsArg",
            [
                Nonterm("head", "expr", InLine()),
                Terminal(", "),
                Nonterm("tail", "arguments", InLine()),
            ]
        ),

        Node(
            "SingleArg",
            [
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Node(
            "KeywordsArg",
            [
                Nonterm("kws", "keywords", InLine())
            ]
        ),

    ],

    "dictionary_item" : [

        Node(
            "Field",
            [
                Nonterm("key", "expr", InLine()),
                Terminal(" : "),
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Node(
            "DictionarySplatFields",
            [
                Terminal("**"),
                Nonterm("contents", "expr", InLine())
            ]
        )

    ],

    "dictionary_contents" : [
        Node(
            "ConsDictionaryItem",
            [
                Nonterm("head", "dictionary_item", InLine()),
                Terminal(", "),
                Nonterm("tail", "dictionary_contents", NewLine())
            ]
        ),

        Node(
            "SingleDictionaryItem",
            [
                Nonterm("contents", "dictionary_item", InLine())
            ]
        ),

    ],

    "sequence_var" : [
        Node(
            "ConsId",
            [
                Vocab("head", "identifier"),
                Terminal(", "),
                Nonterm("tail", "sequence_var", InLine())
            ]
        ),

        Node(
            "SingleId",
            [
                Vocab("contents", "identifier")
            ]
        ),

    ],


    "sequence_ImportName" : [
        Node(
            "ConsImportName",
            [
                Nonterm("head", "ImportName", InLine()),
                Terminal(", "),
                Nonterm("tail", "sequence_ImportName", InLine()),
            ]
        ),

        Node(
            "SingleImportName",
            [
                Nonterm("contents", "ImportName", InLine())
            ]
        ),

    ],

    "sequence_Withitem" : [
        Node(
            "ConsWithitem",
            [
                Nonterm("head", "Withitem", InLine()),
                Terminal(", "),
                Nonterm("tail", "sequence_Withitem", InLine())
            ]
        ),

        Node(
            "SingleWithitem",
            [
                Nonterm("contents", "Withitem", InLine())
            ]
        ),

    ],


    "statements" : [
        Node(
            "ConsStmt",
            [
                Nonterm("head", "stmt", InLine()),
                Nonterm("tail", "statements", NewLine())
            ]
        ),

        Node(
            "SingleStmt",
            [
                Nonterm("contents", "stmt", InLine())
            ]
        ),

    ],

    "comprehension_constraints" : [
        Node(
            "ConsConstraint",
            [
                Nonterm("head", "constraint", InLine()),
                Nonterm("tail", "comprehension_constraints", NewLine())
            ]
        ),

        Node(
            "SingleConstraint",
            [
                Nonterm("contents", "constraint", InLine())
            ]
        ),

    ],

    "sequence_ExceptHandler" : [
        Node(
            "ConsExceptHandler",
            [
                Nonterm("head", "ExceptHandler", InLine()),
                Nonterm("tail", "sequence_ExceptHandler", NewLine())
            ]
        ),

        Node(
            "SingleExceptHandler",
            [
                Nonterm("contents", "ExceptHandler", InLine())
            ]
        ),

    ],

    "conditions" : [

        Node(
            "ElifCond",
            [
                Nonterm("contents", "ElifBlock", NewLine()),
                Nonterm("tail", "conditions", InLine())
            ]
        ),

        Node(
            "ElseCond",
            [
                Nonterm("contents", "ElseBlock", NewLine())
            ]
        ),

        Node(
            "NoCond",
            []
        )

    ],

    "function_def" : [
        Node(
            "FunctionDef",
            [ 
                Terminal("def "),
                Vocab("name", "identifier"),
                Terminal("("),
                Nonterm("params", "parameters", InLine()),
                Terminal(")"),
                Nonterm("ret_typ", "return_type", InLine()),
                Terminal(":"),
                Nonterm("body", "statements", IndentLine())
            ]
        ),

        Node(
            "AsyncFunctionDef",
            [
                Terminal("async def "),
                Vocab("name", "identifier"),
                Terminal("("),
                Nonterm("params", "parameters", InLine()),
                Terminal(")"),
                Nonterm("ret_typ", "return_type", InLine()),
                Terminal(":"),
                Nonterm("body", "statements", IndentLine())
            ]
        ),
    ],


    "stmt" : [
        Node(
            "DecFunctionDef",
            [ 
                Nonterm("decs", "decorators", InLine()),
                Nonterm("fun_def", "function_def", NewLine())
            ]
        ),

        Node(
            "DecAsyncFunctionDef",
            [
                Nonterm("decs", "decorators", InLine()),
                Nonterm("fun_def", "function_def", NewLine())
            ]
        ),

        Node(
            "DecClassDef",
            [
                Nonterm("decs", "decorators", InLine()),
                Nonterm("class_def", "ClassDef", NewLine())
            ]
        ),


        Node(
            "ReturnSomething",
            [
                Terminal("return "), 
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Node(
            "Return",
            [
                Terminal("return ")
            ]
        ),

        Node(
            "Delete",
            [
                Terminal("del"),
                Nonterm("targets", "comma_exprs", InLine())
            ]
        ),

        Node(
            "Assign",
            [
                Nonterm("targets", "target_exprs", InLine()),
                Terminal(" = "),
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Node(
            "AugAssign",
            [
                Nonterm("target", "expr", InLine()),
                Terminal(" "),
                Nonterm("op", "operator", InLine()),
                Terminal("= "),
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Node(
            "TypedAssign", 
            [
                Nonterm("target", "expr", InLine()),
                Terminal(" : "),
                Nonterm("type", "expr", InLine()),
                Terminal(" = "),
                Nonterm("contents", "expr", InLine())
            ],
        ),

        Node(
            "TypedDeclare", 
            [
                Nonterm("target", "expr", InLine()),
                Terminal(" : "),
                Nonterm("type", "expr", InLine())
            ],
        ),

        Node(
            "For",
            [
                Terminal("for "),
                Nonterm("target", "expr", InLine()),
                Terminal(" in "),
                Nonterm("iter", "expr", InLine()),
                Terminal(": "),
                Nonterm("body", "statements", IndentLine())
            ]
        ),

        Node(
            "ForElse",
            [
                Terminal("for "),
                Nonterm("target", "expr", InLine()),
                Terminal(" in "),
                Nonterm("iter", "expr", InLine()),
                Terminal(": "),
                Nonterm("body", "statements", IndentLine()),
                Nonterm("orelse", "ElseBlock", NewLine())
            ]
        ),

        Node(
            "AsyncFor",
            [
                Terminal("async for "),
                Nonterm("target", "expr", InLine()),
                Terminal(" in "),
                Nonterm("iter", "expr", InLine()),
                Terminal(": "),
                Nonterm("body", "statements", IndentLine())
            ]
        ),

        Node(
            "AsyncForElse",
            [
                Terminal("async for "),
                Nonterm("target", "expr", InLine()),
                Terminal(" in "),
                Nonterm("iter", "expr", InLine()),
                Terminal(": "),
                Nonterm("body", "statements", IndentLine()),
                Nonterm("orelse", "ElseBlock", NewLine())
            ]
        ),

        Node(
            "While",
            [
                Terminal("while "),
                Nonterm("test", "expr", InLine()),
                Terminal(": "),
                Nonterm("body", "statements", IndentLine()),
            ]
        ),

        Node(
            "WhileElse",
            [
                Terminal("while "),
                Nonterm("test", "expr", InLine()),
                Terminal(": "),
                Nonterm("body", "statements", IndentLine()),
                Nonterm("orelse", "ElseBlock", NewLine())
            ]
        ),

        Node(
            "If",
            [
                Terminal("if "),
                Nonterm("test", "expr", InLine()),
                Terminal(": "),
                Nonterm("body", "statements", IndentLine()),
                Nonterm("orelse", "conditions", InLine())
            ]
        ),

        Node(
            "With",
            [
                Terminal("with "),
                Nonterm("items", "sequence_Withitem", InLine()),
                Terminal(":"),
                Nonterm("body", "statements", IndentLine())
            ]
        ),

        Node(
            "AsyncWith",
            [
                Terminal("async with "),
                Nonterm("items", "sequence_Withitem", InLine()),
                Terminal(":"),
                Nonterm("body", "statements", IndentLine())
            ]
        ),

        Node(
            "Raise",
            [
                Terminal("raise")
            ]
        ),

        Node(
            "RaiseExc",
            [
                Terminal("raise"),
                Nonterm("exc", "expr", IndentLine())
            ]
        ),

        Node(
            "RaiseFrom",
            [
                Terminal("raise"),
                Nonterm("exc", "expr", InLine()),
                Terminal(" from "),
                Nonterm("caus", "expr", InLine())
            ]
        ),


        Node(
            "Try",
            [
                Terminal("try:"),
                Nonterm("body", "statements", IndentLine()),
                Nonterm("handlers", "sequence_ExceptHandler", NewLine()),
            ]
        ),

        Node(
            "TryElse",
            [
                Terminal("try:"),
                Nonterm("body", "statements", IndentLine()),
                Nonterm("handlers", "sequence_ExceptHandler", NewLine()),
                Nonterm("orelse", "ElseBlock", NewLine())
            ]
        ),

        Node(
            "TryFin",
            [
                Terminal("try:"),
                Nonterm("body", "statements", IndentLine()),
                Nonterm("handlers", "sequence_ExceptHandler", NewLine()),
                Nonterm("fin", "FinallyBlock", NewLine())
            ]
        ),

        Node(
            "TryElseFin",
            [
                Terminal("try:"),
                Nonterm("body", "statements", IndentLine()),
                Nonterm("handlers", "sequence_ExceptHandler", NewLine()),
                Nonterm("orelse", "ElseBlock", NewLine()),
                Nonterm("fin", "FinallyBlock", NewLine())
            ]
        ),


        Node(
            "Assert",
            [
                Terminal("assert "),
                Nonterm("test", "expr", InLine())
            ]
        ),

        Node(
            "AssertMsg",
            [
                Terminal("assert "),
                Nonterm("test", "expr", InLine()),
                Terminal(", "),
                Nonterm("msg", "expr", InLine())
            ]
        ),



        Node(
            "Import",
            [
                Terminal("import "),
                Nonterm("names", "sequence_ImportName", InLine())
            ]
        ),

        Node(
            "ImportFrom",
            [
                Terminal("from "),
                Nonterm("module", "module_id", InLine()),
                Terminal(" import "),
                Nonterm("names", "sequence_ImportName", InLine())
            ]
        ),

        Node(
            "ImportWildCard",
            [
                Terminal("from "),
                Nonterm("module", "module_id", InLine()),
                Terminal(" import *")
            ]
        ),

        Node(
            "Global",
            [
                Terminal("global "),
                Nonterm("names", "sequence_var", InLine())
            ]
        ),

        Node(
            "Nonlocal",
            [
                Terminal("nonlocal "),
                Nonterm("names", "sequence_var", InLine())
            ]
        ),

        Node(
            "Expr",
            [
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Node(
            "Pass",
            [
                Terminal("pass")
            ]
        ),

        Node(
            "Break",
            [
                Terminal("break")
            ]
        ),

        Node(
            "Continue",
            [
                Terminal("continue")
            ]
        ),

    ],

    "expr" : [

        Node(
            "BoolOp",
            [
                Terminal("("),
                Nonterm("left", "expr", InLine()),
                Terminal(" "),
                Nonterm("op", "boolop", InLine()),
                Terminal(" "),
                Nonterm("right", "expr", InLine()),
                Terminal(")")
            ]
        ),

        Node(
            "NamedExpr",
            [
                Nonterm("target", "expr", InLine()),
                Terminal(" := "),
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Node(
            "BinOp",
            [
                Terminal("("),
                Nonterm("left", "expr", InLine()),
                Terminal(" "),
                Nonterm("op", "operator", InLine()),
                Terminal(" "),
                Nonterm("right", "expr", InLine()),
                Terminal(")")
            ]
        ),

        Node(
            "UnaryOp",
            [
                Terminal("("),
                Nonterm("op", "unaryop", InLine()),
                Terminal(" "),
                Nonterm("right", "expr", InLine()),
                Terminal(")")
            ]
        ),

        Node(
            "Lambda",
            [
                Terminal("lambda "),
                Nonterm("params", "parameters", InLine()),
                Terminal(" :"),
                Nonterm("body", "expr", InLine())
            ]
        ),

        Node(
            "IfExp",
            [
                Nonterm("body", "expr", InLine()),
                Terminal("if "),
                Nonterm("test", "expr", InLine()),
                Terminal(" else"),
                Nonterm("orelse", "expr", NewLine())
            ]
        ),

        Node(
            "Dictionary",
            [
                Terminal("{"),
                Nonterm("contents", "dictionary_contents", IndentLine()),
                Terminal("}")
            ]
        ),

        Node(
            "EmptyDictionary",
            [
                Terminal("{}")
            ]
        ),

        Node(
            "Set",
            [
                Terminal("{"),
                Nonterm("contents", "comma_exprs", IndentLine()),
                Terminal("}")
            ]
        ),

        Node(
            "ListComp",
            [
                Terminal("["),
                Nonterm("contents", "expr", IndentLine()),
                Nonterm("constraints", "comprehension_constraints", IndentLine()),
                Terminal("]"),
            ]
        ),

        Node(
            "SetComp",
            [
                Terminal("{"),
                Nonterm("contents", "expr", IndentLine()),
                Nonterm("constraints", "comprehension_constraints", IndentLine()),
                Terminal("}")
            ]
        ),

        Node(
            "DictionaryComp",
            [
                Terminal("{"),
                Nonterm("key", "expr", IndentLine()),
                Terminal(": "),
                Nonterm("contents", "expr", InLine()),
                Nonterm("constraints", "comprehension_constraints", IndentLine()),
                Terminal("}")
            ]
        ),

        Node(
            "GeneratorExp",
            [
                Terminal("("),
                Nonterm("contents", "expr", IndentLine()),
                Nonterm("constraints", "comprehension_constraints", IndentLine()),
                Terminal(")")
            ]
        ),

        Node(
            "Await",
            [
                Terminal("await "),
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Node(
            "YieldNothing",
            [
                Terminal("yield")
            ]
        ),

        Node(
            "Yield",
            [
                Terminal("yield "),
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Node(
            "YieldFrom",
            [
                Terminal("yield from "),
                Nonterm("contents", "expr", InLine())
            ]
        ),

        # need sequences for compare to distinguish between
        # x < 4 < 3 and (x < 4) < 3
        Node(
            "Compare",
            [
                Nonterm("left", "expr", InLine()),
                Terminal(" "),
                Nonterm("comps", "comparisons", InLine())
            ]
        ),

        Node(
            "Call",
            [
                Nonterm("func", "expr", InLine()),
                Terminal("()")
            ]
        ),

        Node(
            "CallArgs",
            [
                Nonterm("func", "expr", InLine()),
                Terminal("("),
                Nonterm("args", "arguments", InLine()),
                Terminal(")")
            ]
        ),

        Node(
            "Integer",
            [
                Vocab("contents", "integer")
            ]
        ),

        Node(
            "Float",
            [
                Vocab("contents", "float")
            ]
        ),

        Node(
            "ConcatString",
            [
                Nonterm("contents", "sequence_string", InLine())
            ]
        ),

        Node(
            "True_",
            [
                Terminal("True")
            ]
        ),

        Node(
            "False_",
            [
                Terminal("False")
            ]
        ),


        Node(
            "None_",
            [
                Terminal("None")
            ]
        ),

        Node(
            "Ellip",
            [
                Terminal("...")
            ]
        ),

        Node(
            "Attribute",
            [
                Nonterm("contents", "expr", InLine()),
                Terminal("."),
                Vocab("name", "identifier")
            ]
        ),

        Node(
            "Subscript",
            [
                Nonterm("contents", "expr", InLine()),
                Terminal("["),
                Nonterm("slice", "expr", InLine()),
                Terminal("]")
            ]
        ),

        Node(
            "Starred",
            [
                Terminal("*"),
                Nonterm("contents", "expr", InLine()),
            ]
        ),

        Node(
            "Name",
            [
                Vocab("contents", "identifier")
            ]
        ),

        Node(
            "List",
            [
                Terminal("["),
                Nonterm("contents", "comma_exprs", InLine()),
                Terminal("]")
            ]
        ),

        Node(
            "EmptyList",
            [
                Terminal("[]"),
            ]
        ),

        Node(
            "Tuple",
            [
                Terminal("("),
                Nonterm("contents", "comma_exprs", InLine()),
                Terminal(")")
            ]
        ),

        Node(
            "EmptyTuple",
            [
                Terminal("()")
            ]
        ),

        Node(
            "Slice",
            [
                Nonterm("lower", "option_expr", InLine()),
                Terminal(":"),
                Nonterm("upper", "option_expr", InLine()),
                Terminal(":"),
                Nonterm("step", "option_expr", InLine())
            ]
        ),

    ],

    "boolop" : [
        Node(
            "And",
            [
                Terminal("and")
            ] 
        ),

        Node(
            "Or",
            [
                Terminal("or")
            ] 
        )
    ], 

    "operator" : [
        Node(
            "Add",
            [Terminal("+")]
        ),

        Node(
            "Sub",
            [Terminal("-")]
        ),

        Node(
            "Mult",
            [Terminal("*")]
        ),

        Node(
            "MatMult",
            [Terminal("@")]
        ),

        Node(
            "Div",
            [Terminal("/")]
        ),

        Node(
            "Mod",
            [Terminal("%")]
        ),

        Node(
            "Pow",
            [Terminal("**")]
        ),

        Node(
            "LShift",
            [Terminal("<<")]
        ),

        Node(
            "RShift",
            [Terminal(">>")]
        ),

        Node(
            "BitOr",
            [Terminal("|")]
        ),

        Node(
            "BitXor",
            [Terminal("^")]
        ),

        Node(
            "BitAnd",
            [Terminal("&")]
        ),

        Node(
            "FloorDiv",
            [Terminal("//")]
        ),
    ],

    "unaryop" : [
        Node(
            "Invert",
            [Terminal("~")]
        ),

        Node(
            "Not",
            [Terminal("not")]
        ),

        Node(
            "UAdd",
            [Terminal("+")]
        ),

        Node(
            "USub",
            [Terminal("-")]
        ),
    ],

    "cmpop" : [
        Node(
            "Eq",
            [Terminal("==")]
        ),

        Node(
            "NotEq",
            [Terminal("!=")]
        ),

        Node(
            "Lt",
            [Terminal("<")]
        ),

        Node(
            "LtE",
            [Terminal("<=")]
        ),

        Node(
            "Gt",
            [Terminal(">")]
        ),

        Node(
            "GtE",
            [Terminal(">=")]
        ),

        Node(
            "Is",
            [Terminal("is")]
        ),

        Node(
            "IsNot",
            [Terminal("is not")]
        ),

        Node(
            "In",
            [Terminal("in")]
        ),

        Node(
            "NotIn",
            [Terminal("not in")]
        ),
    ],

    "constraint" : [

        Node(
            "AsyncConstraint",
            [
                Terminal("async for "),
                Nonterm("target", "expr", InLine()),
                Terminal(" in "),
                Nonterm("search_space", "expr", InLine()),
                Nonterm("filts", "constraint_filters", NewLine())
            ] 
        ),

        Node(
            "Constraint",
            [
                Terminal("for "),
                Nonterm("target", "expr", InLine()),
                Terminal(" in "),
                Nonterm("search_space", "expr", InLine()),
                Nonterm("filts", "constraint_filters", NewLine())
            ] 
        ),

    ]
}


singles : list[Node] = [

    Node(
        "Module",
        [
            Nonterm("body", "statements", InLine())
        ]
    ),

    Node(
        "CompareRight",
        [
            Nonterm("op", "cmpop", InLine()),
            Terminal(" "),
            Nonterm("rand", "expr", InLine())
        ]
    ),

    Node(
        "ExceptHandler",
        [
            Terminal("except "),
            Nonterm("arg", "except_arg", InLine()),
            Terminal(":"),
            Nonterm("body", "statements", IndentLine())
        ]
    ),

    Node(
        "Param",
        [
            Vocab("name", "identifier"),
            Nonterm("type", "param_type", InLine()),
            Nonterm("default", "param_default", InLine())
        ]
    ),

    Node(
        "ImportName",
        [
            Vocab("name", "module_identifier"),
            Nonterm("as_name", "alias", InLine())
        ]
    ),


    Node(
        "Withitem",
        [
            Nonterm("contet", "expr", InLine()),
            Nonterm("target", "alias_expr", InLine())
        ]
    ),

    Node(
        "ClassDef",
        [
            Terminal("class "),
            Vocab("name", "identifier"),
            Nonterm("bs", "bases", InLine()),
            Terminal(":"), 
            Nonterm("body", "statements", IndentLine())
        ]
    ),

    Node(
        "ElifBlock",
        [
            Terminal("elif "),
            Nonterm("test", "expr", InLine()),
            Terminal(":"),
            Nonterm("body", "statements", IndentLine()),
        ]
    ),

    Node(
        "ElseBlock",
        [
            Terminal("else:"),
            Nonterm("body", "statements", IndentLine()),
        ]
    ),

    Node(
        "FinallyBlock",
        [
            Terminal("finally:"),
            Nonterm("body", "statements", IndentLine())
        ]
    )


]

# map from a node id (sequence id) to node (sequence) 
node_map = {
    node.name : node 
    for node in singles
} | {
    node.name : node 
    for nodes in choices.values()
    for node in nodes 
}

# map from a nonterminal to choices of nodes (sequences)
grammar = {
    node.name : [schema.to_dictionary(node)]
    for node in singles 
} | {
    name : [schema.to_dictionary(node) for node in nodes]
    for name, nodes in choices.items()
}