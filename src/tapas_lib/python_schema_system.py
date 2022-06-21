from __future__ import annotations
from tapas_base.rule_construct_autogen import ItemHandlers, Rule, Vocab, Terminal, Nonterm 
from tapas_base.line_format_construct_autogen import NewLine, InLine, IndentLine
from tapas_base import rule_system as rs

choices_schema : dict[str, list[Rule]] = {

    "return_annotation" : [

        Rule(
            "SomeReturnAnno",
            [
                Terminal(" -> "),
                Nonterm("content", "expr", InLine())
            ]
        ),

        Rule(
            "NoReturnAnno",
            []
        )
    ],

    "except_arg" : [
        Rule(
            "SomeExceptArg",
            [
                Terminal(" "),
                Nonterm("content", "expr", InLine())
            ]
        ),

        Rule(
            "SomeExceptArgName",
            [
                Terminal(" "),
                Nonterm("content", "expr", InLine()),
                Terminal(" as "),
                Vocab("name", "identifier"),
            ]
        ),

        Rule(
            "NoExceptArg",
            []
        )
    ],

    "param_annotation" : [
        Rule(
            "SomeParamAnno",
            [
                Terminal(" : "),
                Nonterm("content", "expr", InLine()),
            ]
        ),

        Rule(
            "NoParamAnno",
            []
        ),
    ],

    "param_default" : [
        Rule(
            "SomeParamDefault",
            [
                Terminal(" = "),
                Nonterm("content", "expr", InLine())
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
                Nonterm("content", "Param", InLine())
            ]
        ),

        Rule(
            "TransKwParam",
            [
                Nonterm("head", "Param", InLine()),
                Terminal("**"),
                Nonterm("tail", "Param", InLine())
            ]
        )

    ],

    "parameters_c" : [
        Rule(
            "SingleTupleBundleParam",
            [
                Terminal("*"),
                Nonterm("content", "Param", InLine())
            ]
        ),

        Rule(
            "TransTupleBundleParam",
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
                Nonterm("content", "parameters_d", InLine())
            ]
        ),

        Rule(
            "DoubleBundleParam",
            [
                Terminal("*"),
                Nonterm("tuple_param", "Param", InLine()),
                Terminal("**"),
                Nonterm("dict_param", "Param", InLine())
            ]
        ),

        Rule(
            "DictionaryBundleParam",
            [
                Terminal("**"),
                Nonterm("content", "Param", InLine())
            ]
        )
    ],

    "parameters_b" : [
        Rule(
            "ConsPosKeyParam",
            [
                Nonterm("head", "Param", InLine()),
                Terminal(", "),
                Nonterm("tail", "parameters_b", InLine())
            ]
        ),

        Rule(
            "SinglePosKeyParam",
            [
                Nonterm("content", "Param", InLine())
            ]
        ),

        Rule(
            "ParamsC",
            [
                Nonterm("content", "parameters_c", InLine())
            ]
        ),

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
                Nonterm("content", "Param", InLine()),
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

    "parameters" : [
        Rule(
            "ParamsA",
            [
                Nonterm("content", "parameters_a", InLine())
            ]
        ),


        Rule(
            "ParamsB",
            [
                Nonterm("content", "parameters_b", InLine())
            ]
        ),

        Rule(
            "NoParam",
            []
        )
    ],


    "keyword" : [

        Rule(
            "NamedKeyword",
            [
                Vocab("name", "identifier"),
                Terminal(" = "),
                Nonterm("content", "expr", InLine())
            ]
        ),

        Rule(
            "SplatKeyword",
            [
                Terminal("**"),
                Nonterm("content", "expr", InLine())
            ]
        ),
    ],

    "import_name" : [

        Rule(
            "ImportNameAlias",
            [
                Vocab("name", "identifier"),
                Terminal(" as "),
                Vocab("alias", "identifier")
            ]
        ),

        Rule(
            "ImportNameOnly",
            [
                Vocab("name", "identifier"),
            ]
        )

    ],

    "with_item" : [

        Rule(
            "WithItemAlias",
            [
                Nonterm("content", "expr", InLine()),
                Terminal(" as "),
                Nonterm("alias", "expr", InLine())
            ]
        ),


        Rule(
            "WithItemOnly",
            [
                Nonterm("content", "expr", InLine())
            ]
        )

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
                Nonterm("content", "expr", InLine())
            ]
        ),

        Rule(
            "KeywordBases",
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
                Nonterm("content", "keyword", InLine()),
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
                Nonterm("content", "CompareRight", InLine())
            ]
        ),

    ],

    "option_expr" : [
        Rule(
            "SomeExpr",
            [
                Nonterm("content", "expr", InLine())
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
                Nonterm("content", "expr", InLine())
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
                Nonterm("content", "expr", InLine())
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
                Nonterm("content", "expr", InLine())
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
                Vocab("content", "string"),
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
                Nonterm("content", "expr", InLine())
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
                Nonterm("content", "expr", InLine())
            ]
        ),

        Rule(
            "DictionarySplatFields",
            [
                Terminal("**"),
                Nonterm("content", "expr", InLine())
            ]
        )

    ],

    "dictionary_content" : [
        Rule(
            "ConsDictionaryItem",
            [
                Nonterm("head", "dictionary_item", InLine()),
                Terminal(", "),
                Nonterm("tail", "dictionary_content", NewLine())
            ]
        ),

        Rule(
            "SingleDictionaryItem",
            [
                Nonterm("content", "dictionary_item", InLine())
            ]
        ),

    ],

    "sequence_name" : [
        Rule(
            "ConsId",
            [
                Vocab("head", "identifier"),
                Terminal(", "),
                Nonterm("tail", "sequence_name", InLine())
            ]
        ),

        Rule(
            "SingleId",
            [
                Vocab("content", "identifier")
            ]
        ),

    ],


    "sequence_import_name" : [
        Rule(
            "ConsImportName",
            [
                Nonterm("head", "import_name", InLine()),
                Terminal(", "),
                Nonterm("tail", "sequence_import_name", InLine()),
            ]
        ),

        Rule(
            "SingleImportName",
            [
                Nonterm("content", "import_name", InLine())
            ]
        ),

    ],

    "sequence_with_item" : [
        Rule(
            "ConsWithItem",
            [
                Nonterm("head", "with_item", InLine()),
                Terminal(", "),
                Nonterm("tail", "sequence_with_item", InLine())
            ]
        ),

        Rule(
            "SingleWithItem",
            [
                Nonterm("content", "with_item", InLine())
            ]
        ),

    ],

    "module" : [
        Rule(
            "FutureMod",
            [
                Terminal("from __future__ import "),
                Nonterm("names", "sequence_import_name", InLine()),
                Nonterm("body", "statements", NewLine())
            ]
        ),

        Rule(
            "SimpleMod",
            [
                Nonterm("body", "statements", InLine())
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
                Nonterm("content", "stmt", InLine())
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
                Nonterm("content", "constraint", InLine())
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
                Nonterm("content", "ExceptHandler", InLine())
            ]
        ),

    ],

    "conditions" : [

        Rule(
            "ElifCond",
            [
                Nonterm("content", "ElifBlock", NewLine()),
                Nonterm("tail", "conditions", InLine())
            ]
        ),

        Rule(
            "ElseCond",
            [
                Nonterm("content", "ElseBlock", NewLine())
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
                Nonterm("ret_anno", "return_annotation", InLine()),
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
                Nonterm("ret_anno", "return_annotation", InLine()),
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
                Nonterm("content", "expr", InLine())
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
                Terminal("del "),
                Nonterm("targets", "comma_exprs", InLine())
            ]
        ),

        Rule(
            "Assign",
            [
                Nonterm("targets", "target_exprs", InLine()),
                Terminal(" = "),
                Nonterm("content", "expr", InLine())
            ]
        ),

        Rule(
            "AugAssign",
            [
                Nonterm("target", "expr", InLine()),
                Terminal(" "),
                Nonterm("op", "bin_rator", InLine()),
                Terminal("= "),
                Nonterm("content", "expr", InLine())
            ]
        ),

        Rule(
            "AnnoAssign", 
            [
                Nonterm("target", "expr", InLine()),
                Terminal(" : "),
                Nonterm("anno", "expr", InLine()),
                Terminal(" = "),
                Nonterm("content", "expr", InLine())
            ],
        ),

        Rule(
            "AnnoDeclar", 
            [
                Nonterm("target", "expr", InLine()),
                Terminal(" : "),
                Nonterm("anno", "expr", InLine())
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
                Nonterm("items", "sequence_with_item", InLine()),
                Terminal(":"),
                Nonterm("body", "statements", IndentLine())
            ]
        ),

        Rule(
            "AsyncWith",
            [
                Terminal("async with "),
                Nonterm("items", "sequence_with_item", InLine()),
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
                Terminal("raise "),
                Nonterm("exc", "expr", InLine())
            ]
        ),

        Rule(
            "RaiseFrom",
            [
                Terminal("raise "),
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
            "TryExceptFin",
            [
                Terminal("try:"),
                Nonterm("body", "statements", IndentLine()),
                Nonterm("handlers", "sequence_ExceptHandler", NewLine()),
                Nonterm("fin", "FinallyBlock", NewLine())
            ]
        ),

        Rule(
            "TryFin",
            [
                Terminal("try:"),
                Nonterm("body", "statements", IndentLine()),
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
                Nonterm("names", "sequence_import_name", InLine())
            ]
        ),

        Rule(
            "ImportFrom",
            [
                Terminal("from "),
                Vocab("module", "identifier"),
                Terminal(" import "),
                Nonterm("names", "sequence_import_name", InLine())
            ]
        ),

        Rule(
            "ImportWildCard",
            [
                Terminal("from "),
                Vocab("module", "identifier"),
                Terminal(" import *")
            ]
        ),

        Rule(
            "Global",
            [
                Terminal("global "),
                Nonterm("names", "sequence_name", InLine())
            ]
        ),

        Rule(
            "Nonlocal",
            [
                Terminal("nonlocal "),
                Nonterm("names", "sequence_name", InLine())
            ]
        ),

        Rule(
            "Expr",
            [
                Nonterm("content", "expr", InLine())
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
                Nonterm("op", "bool_rator", InLine()),
                Terminal(" "),
                Nonterm("right", "expr", InLine()),
                Terminal(")")
            ]
        ),

        Rule(
            "AssignExpr",
            [
                Nonterm("target", "expr", InLine()),
                Terminal(" := "),
                Nonterm("content", "expr", InLine())
            ]
        ),

        Rule(
            "BinOp",
            [
                Terminal("("),
                Nonterm("left", "expr", InLine()),
                Terminal(" "),
                Nonterm("rator", "bin_rator", InLine()),
                Terminal(" "),
                Nonterm("right", "expr", InLine()),
                Terminal(")")
            ]
        ),

        Rule(
            "UnaryOp",
            [
                Terminal("("),
                Nonterm("rator", "unary_rator", InLine()),
                Terminal(" "),
                Nonterm("rand", "expr", InLine()),
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
                Nonterm("content", "dictionary_content", IndentLine()),
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
                Nonterm("content", "comma_exprs", IndentLine()),
                Terminal("}")
            ]
        ),

        Rule(
            "ListComp",
            [
                Terminal("["),
                Nonterm("content", "expr", IndentLine()),
                Nonterm("constraints", "comprehension_constraints", IndentLine()),
                Terminal("]"),
            ]
        ),

        Rule(
            "SetComp",
            [
                Terminal("{"),
                Nonterm("content", "expr", IndentLine()),
                Nonterm("constraints", "comprehension_constraints", IndentLine()),
                Terminal("}")
            ]
        ),

        Rule(
            "DictionaryComp",
            [
                Terminal("{"),
                Nonterm("key", "expr", IndentLine()),
                Terminal(" : "),
                Nonterm("content", "expr", InLine()),
                Nonterm("constraints", "comprehension_constraints", IndentLine()),
                Terminal("}")
            ]
        ),

        Rule(
            "GeneratorExp",
            [
                Terminal("("),
                Nonterm("content", "expr", IndentLine()),
                Nonterm("constraints", "comprehension_constraints", IndentLine()),
                Terminal(")")
            ]
        ),

        Rule(
            "Await",
            [
                Terminal("await "),
                Nonterm("content", "expr", InLine())
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
                Nonterm("content", "expr", InLine())
            ]
        ),

        Rule(
            "YieldFrom",
            [
                Terminal("yield from "),
                Nonterm("content", "expr", InLine())
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
                Vocab("content", "integer")
            ]
        ),

        Rule(
            "Float",
            [
                Vocab("content", "float")
            ]
        ),

        Rule(
            "ConcatString",
            [
                Nonterm("content", "sequence_string", InLine())
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
                Nonterm("content", "expr", InLine()),
                Terminal("."),
                Vocab("name", "identifier")
            ]
        ),

        Rule(
            "Subscript",
            [
                Nonterm("content", "expr", InLine()),
                Terminal("["),
                Nonterm("slice", "expr", InLine()),
                Terminal("]")
            ]
        ),

        Rule(
            "Starred",
            [
                Terminal("*"),
                Nonterm("content", "expr", InLine()),
            ]
        ),

        Rule(
            "Name",
            [
                Vocab("content", "identifier")
            ]
        ),

        Rule(
            "List",
            [
                Terminal("["),
                Nonterm("content", "comma_exprs", InLine()),
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
                Nonterm("content", "comma_exprs", InLine()),
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

    "bool_rator" : [
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

    "bin_rator" : [
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

    "unary_rator" : [
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

    "cmp_rator" : [
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


singles_schema : list[Rule] = [

    Rule(
        "CompareRight",
        [
            Nonterm("rator", "cmp_rator", InLine()),
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
            Nonterm("anno", "param_annotation", InLine()),
            Nonterm("default", "param_default", InLine())
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
node_schema = {
    r.name : r 
    for r in singles_schema
} | {
    r.name : r 
    for rs in choices_schema.values()
    for r in rs 
}

schema = {
    rule.name : [rule]
    for rule in singles_schema 
} | choices_schema

# map from a nonterminal to choices of nodes (sequences)
portable_schema = {
    name : [rs.to_dictionary(rule) for rule in rules]
    for name, rules in schema.items()
}