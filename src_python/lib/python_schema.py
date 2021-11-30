from __future__ import annotations
from gen.rule import ItemHandlers, Rule, Vocab, Terminal, Nonterm 
from gen.line_format import NewLine, InLine, IndentLine
import lib.rule



choices : dict[str, list[Rule]] = {

    "return_type" : [

        Rule(
            "SomeReturnType",
            [
                Terminal(" -> "),
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Rule(
            "NoReturnType",
            []
        )
    ],

    "module_id" : [

        Rule(
            "SomeModuleId",
            [
                Vocab("contents", "module_identifier")
            ]
        ),

        Rule(
            "NoModuleId",
            [
                Terminal(".")
            ]
        )
    ],

    "except_arg" : [
        Rule(
            "SomeExceptArg",
            [
                Terminal(" "),
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Rule(
            "SomeExceptArgName",
            [
                Terminal(" "),
                Nonterm("contents", "expr", InLine()),
                Terminal(" as "),
                Vocab("name", "identifier"),
            ]
        ),

        Rule(
            "NoExceptArg",
            []
        )
    ],

    "param_type" : [
        Rule(
            "SomeParamType",
            [
                Terminal(" : "),
                Nonterm("contents", "expr", InLine()),
            ]
        ),

        Rule(
            "NoParamType",
            []
        ),
    ],

    "param_default" : [
        Rule(
            "SomeParamDefault",
            [
                Terminal(" = "),
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Rule(
            "NoParamDefault",
            []
        ),
    ],

    "parameters_d" : [
        Rule(
            "ConsKwParam",
            [
                Nonterm("head", "Param", InLine()),
                Terminal(", "),
                Nonterm("tail", "parameters_d", InLine())
            ]
        ),

        Rule(
            "SingleKwParam",
            [
                Nonterm("contents", "Param", InLine())
            ]
        ),

        Rule(
            "DictionarySplatParam",
            [
                Terminal("**"),
                Nonterm("contents", "Param", InLine())
            ]
        )

    ],

    "parameters_c" : [
        Rule(
            "SingleListSplatParam",
            [
                Terminal("*"),
                Nonterm("contents", "Param", InLine())
            ]
        ),

        Rule(
            "TransListSplatParam",
            [
                Terminal("*"),
                Nonterm("head", "Param", InLine()),
                Terminal(", "),
                Nonterm("tail", "parameters_d", InLine())
            ]
        ),

        Rule(
            "ParamsD",
            [
                Terminal("*, "),
                Nonterm("contents", "parameters_d", InLine())
            ]
        ),
    ],

    "parameters_b" : [
        Rule(
            "ConsParam",
            [
                Nonterm("head", "Param", InLine()),
                Terminal(", "),
                Nonterm("tail", "parameters_b", InLine())
            ]
        ),

        Rule(
            "SingleParam",
            [
                Nonterm("contents", "Param", InLine())
            ]
        ),

        Rule(
            "ParamsC",
            [
                Nonterm("contents", "parameters_c", InLine())
            ]
        ),

    ],

    "parameters" : [
        Rule(
            "ParamsA",
            [
                Nonterm("contents", "parameters_a", InLine())
            ]
        ),


        Rule(
            "ParamsB",
            [
                Nonterm("contents", "parameters_b", InLine())
            ]
        ),

        Rule(
            "NoParam",
            []
        )
    ],


    "parameters_a" : [
        Rule(
            "ConsPosParam",
            [
                Nonterm("head", "Param", InLine()),
                Terminal(", "),
                Nonterm("tail", "parameters_a", InLine())
            ]
        ),

        Rule(
            "SinglePosParam",
            [
                Nonterm("contents", "Param", InLine()),
                Terminal(", /")
            ]
        ),

        Rule(
            "TransPosParam",
            [
                Nonterm("head", "Param", InLine()),
                Terminal(", /, "),
                Nonterm("tail", "parameters_b", InLine()),
            ]
        )

    ],


    "keyword" : [

        Rule(
            "NamedKeyword",
            [
                Vocab("name", "identifier"),
                Terminal(" = "),
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Rule(
            "SplatKeyword",
            [
                Terminal("**"),
                Nonterm("contents", "expr", InLine())
            ]
        ),
    ],

    "alias" : [

        Rule(
            "SomeAlias",
            [
                Terminal(" as "),
                Vocab("contents", "identifier")
            ]
        ),

        Rule(
            "NoAlias",
            []
        ),

    ],

    "alias_expr" : [

        Rule(
            "SomeAliasExpr",
            [
                Terminal(" as "),
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Rule(
            "NoAliasExpr",
            []
        ),

    ],

    "bases" : [
        Rule(
            "SomeBases",
            [
                Terminal("("),
                Nonterm("bases", "bases_a", InLine()),
                Terminal(")")
            ]
        ),

        Rule(
            "NoBases",
            []
        )
    ],

    "bases_a" : [
        Rule(
            "ConsBase",
            [
                Nonterm("head", "expr", InLine()),
                Terminal(", "),
                Nonterm("tail", "bases_a", InLine()),
            ]
        ),

        Rule(
            "SingleBase",
            [
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Rule(
            "KeywordsBase",
            [
                Nonterm("kws", "keywords", InLine())
            ]
        ),

    ],

    "keywords" : [
        Rule(
            "ConsKeyword",
            [
                Nonterm("head", "keyword", InLine()),
                Terminal(", "),
                Nonterm("tail", "keywords", InLine()),
            ]
        ),

        Rule(
            "SingleKeyword",
            [
                Nonterm("contents", "keyword", InLine()),
            ]
        ),

    ],

    "comparisons" : [
        Rule(
            "ConsCompareRight",
            [
                Nonterm("head", "CompareRight", InLine()),
                Terminal(" "),
                Nonterm("tail", "comparisons", InLine()),
            ]
        ),

        Rule(
            "SingleCompareRight",
            [
                Nonterm("contents", "CompareRight", InLine())
            ]
        ),

    ],

    "option_expr" : [
        Rule(
            "SomeExpr",
            [
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Rule(
            "NoExpr",
            []
        )
    ],


    "comma_exprs" : [
        Rule(
            "ConsExpr",
            [
                Nonterm("head", "expr", InLine()),
                Terminal(", "),
                Nonterm("tail", "comma_exprs", InLine())
            ]
        ),

        Rule(
            "SingleExpr",
            [
                Nonterm("contents", "expr", InLine())
            ]
        ),

    ],

    "target_exprs" : [
        Rule(
            "ConsTargetExpr",
            [
                Nonterm("head", "expr", InLine()),
                Terminal(" = "),
                Nonterm("tail", "target_exprs", InLine()),
            ]
        ),

        Rule(
            "SingleTargetExpr",
            [
                Nonterm("contents", "expr", InLine())
            ]
        ),

    ],

    "decorators" : [
        Rule(
            "ConsDec",
            [
                Terminal("@"),
                Nonterm("head", "expr", InLine()),
                Nonterm("tail", "decorators", InLine())
            ]
        ),

        Rule(
            "NoDec",
            []
        ),

    ],

    "constraint_filters" : [
        Rule(
            "ConsFilter",
            [
                Terminal("if "),
                Nonterm("head", "expr", InLine()),
                Nonterm("tail", "constraint_filters", NewLine())
            ]
        ),

        Rule(
            "SingleFilter",
            [
                Terminal("if "),
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Rule(
            "NoFilter",
            []
        ),

    ],

    "sequence_string" : [
        Rule(
            "ConsStr",
            [
                Vocab("head", "string"),
                Terminal(" "),
                Nonterm("tail", "sequence_string", InLine()),
            ]
        ),

        Rule(
            "SingleStr",
            [
                Vocab("contents", "string"),
            ]
        ),

    ],

    "arguments" : [
        Rule(
            "ConsArg",
            [
                Nonterm("head", "expr", InLine()),
                Terminal(", "),
                Nonterm("tail", "arguments", InLine()),
            ]
        ),

        Rule(
            "SingleArg",
            [
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Rule(
            "KeywordsArg",
            [
                Nonterm("kws", "keywords", InLine())
            ]
        ),

    ],

    "dictionary_item" : [

        Rule(
            "Field",
            [
                Nonterm("key", "expr", InLine()),
                Terminal(" : "),
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Rule(
            "DictionarySplatFields",
            [
                Terminal("**"),
                Nonterm("contents", "expr", InLine())
            ]
        )

    ],

    "dictionary_contents" : [
        Rule(
            "ConsDictionaryItem",
            [
                Nonterm("head", "dictionary_item", InLine()),
                Terminal(", "),
                Nonterm("tail", "dictionary_contents", NewLine())
            ]
        ),

        Rule(
            "SingleDictionaryItem",
            [
                Nonterm("contents", "dictionary_item", InLine())
            ]
        ),

    ],

    "sequence_var" : [
        Rule(
            "ConsId",
            [
                Vocab("head", "identifier"),
                Terminal(", "),
                Nonterm("tail", "sequence_var", InLine())
            ]
        ),

        Rule(
            "SingleId",
            [
                Vocab("contents", "identifier")
            ]
        ),

    ],


    "sequence_ImportName" : [
        Rule(
            "ConsImportName",
            [
                Nonterm("head", "ImportName", InLine()),
                Terminal(", "),
                Nonterm("tail", "sequence_ImportName", InLine()),
            ]
        ),

        Rule(
            "SingleImportName",
            [
                Nonterm("contents", "ImportName", InLine())
            ]
        ),

    ],

    "sequence_Withitem" : [
        Rule(
            "ConsWithitem",
            [
                Nonterm("head", "Withitem", InLine()),
                Terminal(", "),
                Nonterm("tail", "sequence_Withitem", InLine())
            ]
        ),

        Rule(
            "SingleWithitem",
            [
                Nonterm("contents", "Withitem", InLine())
            ]
        ),

    ],


    "statements" : [
        Rule(
            "ConsStmt",
            [
                Nonterm("head", "stmt", InLine()),
                Nonterm("tail", "statements", NewLine())
            ]
        ),

        Rule(
            "SingleStmt",
            [
                Nonterm("contents", "stmt", InLine())
            ]
        ),

    ],

    "comprehension_constraints" : [
        Rule(
            "ConsConstraint",
            [
                Nonterm("head", "constraint", InLine()),
                Nonterm("tail", "comprehension_constraints", NewLine())
            ]
        ),

        Rule(
            "SingleConstraint",
            [
                Nonterm("contents", "constraint", InLine())
            ]
        ),

    ],

    "sequence_ExceptHandler" : [
        Rule(
            "ConsExceptHandler",
            [
                Nonterm("head", "ExceptHandler", InLine()),
                Nonterm("tail", "sequence_ExceptHandler", NewLine())
            ]
        ),

        Rule(
            "SingleExceptHandler",
            [
                Nonterm("contents", "ExceptHandler", InLine())
            ]
        ),

    ],

    "conditions" : [

        Rule(
            "ElifCond",
            [
                Nonterm("contents", "ElifBlock", NewLine()),
                Nonterm("tail", "conditions", InLine())
            ]
        ),

        Rule(
            "ElseCond",
            [
                Nonterm("contents", "ElseBlock", NewLine())
            ]
        ),

        Rule(
            "NoCond",
            []
        )

    ],

    "function_def" : [
        Rule(
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

        Rule(
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
        Rule(
            "DecFunctionDef",
            [ 
                Nonterm("decs", "decorators", InLine()),
                Nonterm("fun_def", "function_def", NewLine())
            ]
        ),

        Rule(
            "DecAsyncFunctionDef",
            [
                Nonterm("decs", "decorators", InLine()),
                Nonterm("fun_def", "function_def", NewLine())
            ]
        ),

        Rule(
            "DecClassDef",
            [
                Nonterm("decs", "decorators", InLine()),
                Nonterm("class_def", "ClassDef", NewLine())
            ]
        ),


        Rule(
            "ReturnSomething",
            [
                Terminal("return "), 
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Rule(
            "Return",
            [
                Terminal("return ")
            ]
        ),

        Rule(
            "Delete",
            [
                Terminal("del"),
                Nonterm("targets", "comma_exprs", InLine())
            ]
        ),

        Rule(
            "Assign",
            [
                Nonterm("targets", "target_exprs", InLine()),
                Terminal(" = "),
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Rule(
            "AugAssign",
            [
                Nonterm("target", "expr", InLine()),
                Terminal(" "),
                Nonterm("op", "operator", InLine()),
                Terminal("= "),
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Rule(
            "TypedAssign", 
            [
                Nonterm("target", "expr", InLine()),
                Terminal(" : "),
                Nonterm("type", "expr", InLine()),
                Terminal(" = "),
                Nonterm("contents", "expr", InLine())
            ],
        ),

        Rule(
            "TypedDeclare", 
            [
                Nonterm("target", "expr", InLine()),
                Terminal(" : "),
                Nonterm("type", "expr", InLine())
            ],
        ),

        Rule(
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

        Rule(
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

        Rule(
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

        Rule(
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

        Rule(
            "While",
            [
                Terminal("while "),
                Nonterm("test", "expr", InLine()),
                Terminal(": "),
                Nonterm("body", "statements", IndentLine()),
            ]
        ),

        Rule(
            "WhileElse",
            [
                Terminal("while "),
                Nonterm("test", "expr", InLine()),
                Terminal(": "),
                Nonterm("body", "statements", IndentLine()),
                Nonterm("orelse", "ElseBlock", NewLine())
            ]
        ),

        Rule(
            "If",
            [
                Terminal("if "),
                Nonterm("test", "expr", InLine()),
                Terminal(": "),
                Nonterm("body", "statements", IndentLine()),
                Nonterm("orelse", "conditions", InLine())
            ]
        ),

        Rule(
            "With",
            [
                Terminal("with "),
                Nonterm("items", "sequence_Withitem", InLine()),
                Terminal(":"),
                Nonterm("body", "statements", IndentLine())
            ]
        ),

        Rule(
            "AsyncWith",
            [
                Terminal("async with "),
                Nonterm("items", "sequence_Withitem", InLine()),
                Terminal(":"),
                Nonterm("body", "statements", IndentLine())
            ]
        ),

        Rule(
            "Raise",
            [
                Terminal("raise")
            ]
        ),

        Rule(
            "RaiseExc",
            [
                Terminal("raise"),
                Nonterm("exc", "expr", IndentLine())
            ]
        ),

        Rule(
            "RaiseFrom",
            [
                Terminal("raise"),
                Nonterm("exc", "expr", InLine()),
                Terminal(" from "),
                Nonterm("caus", "expr", InLine())
            ]
        ),


        Rule(
            "Try",
            [
                Terminal("try:"),
                Nonterm("body", "statements", IndentLine()),
                Nonterm("handlers", "sequence_ExceptHandler", NewLine()),
            ]
        ),

        Rule(
            "TryElse",
            [
                Terminal("try:"),
                Nonterm("body", "statements", IndentLine()),
                Nonterm("handlers", "sequence_ExceptHandler", NewLine()),
                Nonterm("orelse", "ElseBlock", NewLine())
            ]
        ),

        Rule(
            "TryFin",
            [
                Terminal("try:"),
                Nonterm("body", "statements", IndentLine()),
                Nonterm("handlers", "sequence_ExceptHandler", NewLine()),
                Nonterm("fin", "FinallyBlock", NewLine())
            ]
        ),

        Rule(
            "TryElseFin",
            [
                Terminal("try:"),
                Nonterm("body", "statements", IndentLine()),
                Nonterm("handlers", "sequence_ExceptHandler", NewLine()),
                Nonterm("orelse", "ElseBlock", NewLine()),
                Nonterm("fin", "FinallyBlock", NewLine())
            ]
        ),


        Rule(
            "Assert",
            [
                Terminal("assert "),
                Nonterm("test", "expr", InLine())
            ]
        ),

        Rule(
            "AssertMsg",
            [
                Terminal("assert "),
                Nonterm("test", "expr", InLine()),
                Terminal(", "),
                Nonterm("msg", "expr", InLine())
            ]
        ),



        Rule(
            "Import",
            [
                Terminal("import "),
                Nonterm("names", "sequence_ImportName", InLine())
            ]
        ),

        Rule(
            "ImportFrom",
            [
                Terminal("from "),
                Nonterm("module", "module_id", InLine()),
                Terminal(" import "),
                Nonterm("names", "sequence_ImportName", InLine())
            ]
        ),

        Rule(
            "ImportWildCard",
            [
                Terminal("from "),
                Nonterm("module", "module_id", InLine()),
                Terminal(" import *")
            ]
        ),

        Rule(
            "Global",
            [
                Terminal("global "),
                Nonterm("names", "sequence_var", InLine())
            ]
        ),

        Rule(
            "Nonlocal",
            [
                Terminal("nonlocal "),
                Nonterm("names", "sequence_var", InLine())
            ]
        ),

        Rule(
            "Expr",
            [
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Rule(
            "Pass",
            [
                Terminal("pass")
            ]
        ),

        Rule(
            "Break",
            [
                Terminal("break")
            ]
        ),

        Rule(
            "Continue",
            [
                Terminal("continue")
            ]
        ),

    ],

    "expr" : [

        Rule(
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

        Rule(
            "NamedExpr",
            [
                Nonterm("target", "expr", InLine()),
                Terminal(" := "),
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Rule(
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

        Rule(
            "UnaryOp",
            [
                Terminal("("),
                Nonterm("op", "unaryop", InLine()),
                Terminal(" "),
                Nonterm("right", "expr", InLine()),
                Terminal(")")
            ]
        ),

        Rule(
            "Lambda",
            [
                Terminal("lambda "),
                Nonterm("params", "parameters", InLine()),
                Terminal(" :"),
                Nonterm("body", "expr", InLine())
            ]
        ),

        Rule(
            "IfExp",
            [
                Nonterm("body", "expr", InLine()),
                Terminal("if "),
                Nonterm("test", "expr", InLine()),
                Terminal(" else"),
                Nonterm("orelse", "expr", NewLine())
            ]
        ),

        Rule(
            "Dictionary",
            [
                Terminal("{"),
                Nonterm("contents", "dictionary_contents", IndentLine()),
                Terminal("}")
            ]
        ),

        Rule(
            "EmptyDictionary",
            [
                Terminal("{}")
            ]
        ),

        Rule(
            "Set",
            [
                Terminal("{"),
                Nonterm("contents", "comma_exprs", IndentLine()),
                Terminal("}")
            ]
        ),

        Rule(
            "ListComp",
            [
                Terminal("["),
                Nonterm("contents", "expr", IndentLine()),
                Nonterm("constraints", "comprehension_constraints", IndentLine()),
                Terminal("]"),
            ]
        ),

        Rule(
            "SetComp",
            [
                Terminal("{"),
                Nonterm("contents", "expr", IndentLine()),
                Nonterm("constraints", "comprehension_constraints", IndentLine()),
                Terminal("}")
            ]
        ),

        Rule(
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

        Rule(
            "GeneratorExp",
            [
                Terminal("("),
                Nonterm("contents", "expr", IndentLine()),
                Nonterm("constraints", "comprehension_constraints", IndentLine()),
                Terminal(")")
            ]
        ),

        Rule(
            "Await",
            [
                Terminal("await "),
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Rule(
            "YieldNothing",
            [
                Terminal("yield")
            ]
        ),

        Rule(
            "Yield",
            [
                Terminal("yield "),
                Nonterm("contents", "expr", InLine())
            ]
        ),

        Rule(
            "YieldFrom",
            [
                Terminal("yield from "),
                Nonterm("contents", "expr", InLine())
            ]
        ),

        # need sequences for compare to distinguish between
        # x < 4 < 3 and (x < 4) < 3
        Rule(
            "Compare",
            [
                Nonterm("left", "expr", InLine()),
                Terminal(" "),
                Nonterm("comps", "comparisons", InLine())
            ]
        ),

        Rule(
            "Call",
            [
                Nonterm("func", "expr", InLine()),
                Terminal("()")
            ]
        ),

        Rule(
            "CallArgs",
            [
                Nonterm("func", "expr", InLine()),
                Terminal("("),
                Nonterm("args", "arguments", InLine()),
                Terminal(")")
            ]
        ),

        Rule(
            "Integer",
            [
                Vocab("contents", "integer")
            ]
        ),

        Rule(
            "Float",
            [
                Vocab("contents", "float")
            ]
        ),

        Rule(
            "ConcatString",
            [
                Nonterm("contents", "sequence_string", InLine())
            ]
        ),

        Rule(
            "True_",
            [
                Terminal("True")
            ]
        ),

        Rule(
            "False_",
            [
                Terminal("False")
            ]
        ),


        Rule(
            "None_",
            [
                Terminal("None")
            ]
        ),

        Rule(
            "Ellip",
            [
                Terminal("...")
            ]
        ),

        Rule(
            "Attribute",
            [
                Nonterm("contents", "expr", InLine()),
                Terminal("."),
                Vocab("name", "identifier")
            ]
        ),

        Rule(
            "Subscript",
            [
                Nonterm("contents", "expr", InLine()),
                Terminal("["),
                Nonterm("slice", "expr", InLine()),
                Terminal("]")
            ]
        ),

        Rule(
            "Starred",
            [
                Terminal("*"),
                Nonterm("contents", "expr", InLine()),
            ]
        ),

        Rule(
            "Name",
            [
                Vocab("contents", "identifier")
            ]
        ),

        Rule(
            "List",
            [
                Terminal("["),
                Nonterm("contents", "comma_exprs", InLine()),
                Terminal("]")
            ]
        ),

        Rule(
            "EmptyList",
            [
                Terminal("[]"),
            ]
        ),

        Rule(
            "Tuple",
            [
                Terminal("("),
                Nonterm("contents", "comma_exprs", InLine()),
                Terminal(")")
            ]
        ),

        Rule(
            "EmptyTuple",
            [
                Terminal("()")
            ]
        ),

        Rule(
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
        Rule(
            "And",
            [
                Terminal("and")
            ] 
        ),

        Rule(
            "Or",
            [
                Terminal("or")
            ] 
        )
    ], 

    "operator" : [
        Rule(
            "Add",
            [Terminal("+")]
        ),

        Rule(
            "Sub",
            [Terminal("-")]
        ),

        Rule(
            "Mult",
            [Terminal("*")]
        ),

        Rule(
            "MatMult",
            [Terminal("@")]
        ),

        Rule(
            "Div",
            [Terminal("/")]
        ),

        Rule(
            "Mod",
            [Terminal("%")]
        ),

        Rule(
            "Pow",
            [Terminal("**")]
        ),

        Rule(
            "LShift",
            [Terminal("<<")]
        ),

        Rule(
            "RShift",
            [Terminal(">>")]
        ),

        Rule(
            "BitOr",
            [Terminal("|")]
        ),

        Rule(
            "BitXor",
            [Terminal("^")]
        ),

        Rule(
            "BitAnd",
            [Terminal("&")]
        ),

        Rule(
            "FloorDiv",
            [Terminal("//")]
        ),
    ],

    "unaryop" : [
        Rule(
            "Invert",
            [Terminal("~")]
        ),

        Rule(
            "Not",
            [Terminal("not")]
        ),

        Rule(
            "UAdd",
            [Terminal("+")]
        ),

        Rule(
            "USub",
            [Terminal("-")]
        ),
    ],

    "cmpop" : [
        Rule(
            "Eq",
            [Terminal("==")]
        ),

        Rule(
            "NotEq",
            [Terminal("!=")]
        ),

        Rule(
            "Lt",
            [Terminal("<")]
        ),

        Rule(
            "LtE",
            [Terminal("<=")]
        ),

        Rule(
            "Gt",
            [Terminal(">")]
        ),

        Rule(
            "GtE",
            [Terminal(">=")]
        ),

        Rule(
            "Is",
            [Terminal("is")]
        ),

        Rule(
            "IsNot",
            [Terminal("is not")]
        ),

        Rule(
            "In",
            [Terminal("in")]
        ),

        Rule(
            "NotIn",
            [Terminal("not in")]
        ),
    ],

    "constraint" : [

        Rule(
            "AsyncConstraint",
            [
                Terminal("async for "),
                Nonterm("target", "expr", InLine()),
                Terminal(" in "),
                Nonterm("search_space", "expr", InLine()),
                Nonterm("filts", "constraint_filters", NewLine())
            ] 
        ),

        Rule(
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


singles : list[Rule] = [

    Rule(
        "Module",
        [
            Nonterm("body", "statements", InLine())
        ]
    ),

    Rule(
        "CompareRight",
        [
            Nonterm("op", "cmpop", InLine()),
            Terminal(" "),
            Nonterm("rand", "expr", InLine())
        ]
    ),

    Rule(
        "ExceptHandler",
        [
            Terminal("except "),
            Nonterm("arg", "except_arg", InLine()),
            Terminal(":"),
            Nonterm("body", "statements", IndentLine())
        ]
    ),

    Rule(
        "Param",
        [
            Vocab("name", "identifier"),
            Nonterm("type", "param_type", InLine()),
            Nonterm("default", "param_default", InLine())
        ]
    ),

    Rule(
        "ImportName",
        [
            Vocab("name", "module_identifier"),
            Nonterm("as_name", "alias", InLine())
        ]
    ),


    Rule(
        "Withitem",
        [
            Nonterm("contet", "expr", InLine()),
            Nonterm("target", "alias_expr", InLine())
        ]
    ),

    Rule(
        "ClassDef",
        [
            Terminal("class "),
            Vocab("name", "identifier"),
            Nonterm("bs", "bases", InLine()),
            Terminal(":"), 
            Nonterm("body", "statements", IndentLine())
        ]
    ),

    Rule(
        "ElifBlock",
        [
            Terminal("elif "),
            Nonterm("test", "expr", InLine()),
            Terminal(":"),
            Nonterm("body", "statements", IndentLine()),
        ]
    ),

    Rule(
        "ElseBlock",
        [
            Terminal("else:"),
            Nonterm("body", "statements", IndentLine()),
        ]
    ),

    Rule(
        "FinallyBlock",
        [
            Terminal("finally:"),
            Nonterm("body", "statements", IndentLine())
        ]
    )


]

# map from a node id (sequence id) to node (sequence) 
rule_map = {
    r.name : r 
    for r in singles
} | {
    r.name : r 
    for rs in choices.values()
    for r in rs 
}

nonterminal_map = {
    rule.name : [rule]
    for rule in singles 
} | choices

# map from a nonterminal to choices of nodes (sequences)
portable = {
    name : [lib.rule.to_dictionary(rule) for rule in rules]
    for name, rules in nonterminal_map.items()
}