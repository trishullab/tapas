
from __future__ import annotations
from lib import production_instance as prod_inst 
from gen.python_ast import *
from gen.line_format import InLine, NewLine, IndentLine




@dataclass
class SP_Module:
    o : Module 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_Module(
    o : Module, depth : int = 0, relation : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []


    stack : list[Union[SP_Module, list[prod_inst.instance]]] = [SP_Module(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_Module):
            o = item.o

            stack.append(
                serialize_statements(o.body, item.depth + 1, "body", 
                    prod_inst.next_indent_width(item.indent_width, InLine()),
                    True,
                )
            )
            stack.append(
                [prod_inst.make_Grammar(
                    nonterminal = 'Module',
                    sequence_id = 'Module',
                    depth = item.depth,
                    relation = item.relation,
                    indent_width = item.indent_width,
                    inline = item.inline
                )]
            )
        else:
            result += item

    return result



@dataclass
class SP_CompareRight:
    o : CompareRight 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_CompareRight(
    o : CompareRight, depth : int = 0, relation : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []


    stack : list[Union[SP_CompareRight, list[prod_inst.instance]]] = [SP_CompareRight(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_CompareRight):
            o = item.o

            stack.append(
                serialize_expr(o.rand, item.depth + 1, "rand", 
                    prod_inst.next_indent_width(item.indent_width, InLine()),
                    True,
                )
            )
            stack.append(
                serialize_cmpop(o.op, item.depth + 1, "op", 
                    prod_inst.next_indent_width(item.indent_width, InLine()),
                    True,
                )
            )
            stack.append(
                [prod_inst.make_Grammar(
                    nonterminal = 'CompareRight',
                    sequence_id = 'CompareRight',
                    depth = item.depth,
                    relation = item.relation,
                    indent_width = item.indent_width,
                    inline = item.inline
                )]
            )
        else:
            result += item

    return result



@dataclass
class SP_ExceptHandler:
    o : ExceptHandler 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_ExceptHandler(
    o : ExceptHandler, depth : int = 0, relation : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []


    stack : list[Union[SP_ExceptHandler, list[prod_inst.instance]]] = [SP_ExceptHandler(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_ExceptHandler):
            o = item.o

            stack.append(
                serialize_statements(o.body, item.depth + 1, "body", 
                    prod_inst.next_indent_width(item.indent_width, IndentLine()),
                    False,
                )
            )
            stack.append(
                serialize_except_arg(o.arg, item.depth + 1, "arg", 
                    prod_inst.next_indent_width(item.indent_width, InLine()),
                    True,
                )
            )
            stack.append(
                [prod_inst.make_Grammar(
                    nonterminal = 'ExceptHandler',
                    sequence_id = 'ExceptHandler',
                    depth = item.depth,
                    relation = item.relation,
                    indent_width = item.indent_width,
                    inline = item.inline
                )]
            )
        else:
            result += item

    return result



@dataclass
class SP_Param:
    o : Param 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_Param(
    o : Param, depth : int = 0, relation : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []


    stack : list[Union[SP_Param, list[prod_inst.instance]]] = [SP_Param(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_Param):
            o = item.o

            stack.append(
                serialize_param_default(o.default, item.depth + 1, "default", 
                    prod_inst.next_indent_width(item.indent_width, InLine()),
                    True,
                )
            )
            stack.append(
                serialize_param_type(o.type, item.depth + 1, "type", 
                    prod_inst.next_indent_width(item.indent_width, InLine()),
                    True,
                )
            )
            stack.append(
                [prod_inst.make_Vocab(
                    choices_id = 'identifier',
                    word = o.name,
                    depth = item.depth + 1,
                    relation = "name"
                )]
            )
            stack.append(
                [prod_inst.make_Grammar(
                    nonterminal = 'Param',
                    sequence_id = 'Param',
                    depth = item.depth,
                    relation = item.relation,
                    indent_width = item.indent_width,
                    inline = item.inline
                )]
            )
        else:
            result += item

    return result



@dataclass
class SP_Field:
    o : Field 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_Field(
    o : Field, depth : int = 0, relation : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []


    stack : list[Union[SP_Field, list[prod_inst.instance]]] = [SP_Field(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_Field):
            o = item.o

            stack.append(
                serialize_expr(o.contents, item.depth + 1, "contents", 
                    prod_inst.next_indent_width(item.indent_width, InLine()),
                    True,
                )
            )
            stack.append(
                serialize_expr(o.key, item.depth + 1, "key", 
                    prod_inst.next_indent_width(item.indent_width, InLine()),
                    True,
                )
            )
            stack.append(
                [prod_inst.make_Grammar(
                    nonterminal = 'Field',
                    sequence_id = 'Field',
                    depth = item.depth,
                    relation = item.relation,
                    indent_width = item.indent_width,
                    inline = item.inline
                )]
            )
        else:
            result += item

    return result



@dataclass
class SP_ImportName:
    o : ImportName 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_ImportName(
    o : ImportName, depth : int = 0, relation : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []


    stack : list[Union[SP_ImportName, list[prod_inst.instance]]] = [SP_ImportName(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_ImportName):
            o = item.o

            stack.append(
                serialize_alias(o.as_name, item.depth + 1, "as_name", 
                    prod_inst.next_indent_width(item.indent_width, InLine()),
                    True,
                )
            )
            stack.append(
                [prod_inst.make_Vocab(
                    choices_id = 'module_identifier',
                    word = o.name,
                    depth = item.depth + 1,
                    relation = "name"
                )]
            )
            stack.append(
                [prod_inst.make_Grammar(
                    nonterminal = 'ImportName',
                    sequence_id = 'ImportName',
                    depth = item.depth,
                    relation = item.relation,
                    indent_width = item.indent_width,
                    inline = item.inline
                )]
            )
        else:
            result += item

    return result



@dataclass
class SP_Withitem:
    o : Withitem 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_Withitem(
    o : Withitem, depth : int = 0, relation : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []


    stack : list[Union[SP_Withitem, list[prod_inst.instance]]] = [SP_Withitem(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_Withitem):
            o = item.o

            stack.append(
                serialize_alias_expr(o.target, item.depth + 1, "target", 
                    prod_inst.next_indent_width(item.indent_width, InLine()),
                    True,
                )
            )
            stack.append(
                serialize_expr(o.contet, item.depth + 1, "contet", 
                    prod_inst.next_indent_width(item.indent_width, InLine()),
                    True,
                )
            )
            stack.append(
                [prod_inst.make_Grammar(
                    nonterminal = 'Withitem',
                    sequence_id = 'Withitem',
                    depth = item.depth,
                    relation = item.relation,
                    indent_width = item.indent_width,
                    inline = item.inline
                )]
            )
        else:
            result += item

    return result



@dataclass
class SP_ClassDef:
    o : ClassDef 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_ClassDef(
    o : ClassDef, depth : int = 0, relation : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []


    stack : list[Union[SP_ClassDef, list[prod_inst.instance]]] = [SP_ClassDef(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_ClassDef):
            o = item.o

            stack.append(
                serialize_statements(o.body, item.depth + 1, "body", 
                    prod_inst.next_indent_width(item.indent_width, IndentLine()),
                    False,
                )
            )
            stack.append(
                serialize_bases(o.bs, item.depth + 1, "bs", 
                    prod_inst.next_indent_width(item.indent_width, InLine()),
                    True,
                )
            )
            stack.append(
                [prod_inst.make_Vocab(
                    choices_id = 'identifier',
                    word = o.name,
                    depth = item.depth + 1,
                    relation = "name"
                )]
            )
            stack.append(
                [prod_inst.make_Grammar(
                    nonterminal = 'ClassDef',
                    sequence_id = 'ClassDef',
                    depth = item.depth,
                    relation = item.relation,
                    indent_width = item.indent_width,
                    inline = item.inline
                )]
            )
        else:
            result += item

    return result



@dataclass
class SP_ElifBlock:
    o : ElifBlock 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_ElifBlock(
    o : ElifBlock, depth : int = 0, relation : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []


    stack : list[Union[SP_ElifBlock, list[prod_inst.instance]]] = [SP_ElifBlock(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_ElifBlock):
            o = item.o

            stack.append(
                serialize_statements(o.body, item.depth + 1, "body", 
                    prod_inst.next_indent_width(item.indent_width, IndentLine()),
                    False,
                )
            )
            stack.append(
                serialize_expr(o.test, item.depth + 1, "test", 
                    prod_inst.next_indent_width(item.indent_width, InLine()),
                    True,
                )
            )
            stack.append(
                [prod_inst.make_Grammar(
                    nonterminal = 'ElifBlock',
                    sequence_id = 'ElifBlock',
                    depth = item.depth,
                    relation = item.relation,
                    indent_width = item.indent_width,
                    inline = item.inline
                )]
            )
        else:
            result += item

    return result



@dataclass
class SP_ElseBlock:
    o : ElseBlock 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_ElseBlock(
    o : ElseBlock, depth : int = 0, relation : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []


    stack : list[Union[SP_ElseBlock, list[prod_inst.instance]]] = [SP_ElseBlock(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_ElseBlock):
            o = item.o

            stack.append(
                serialize_statements(o.body, item.depth + 1, "body", 
                    prod_inst.next_indent_width(item.indent_width, IndentLine()),
                    False,
                )
            )
            stack.append(
                [prod_inst.make_Grammar(
                    nonterminal = 'ElseBlock',
                    sequence_id = 'ElseBlock',
                    depth = item.depth,
                    relation = item.relation,
                    indent_width = item.indent_width,
                    inline = item.inline
                )]
            )
        else:
            result += item

    return result



@dataclass
class SP_FinallyBlock:
    o : FinallyBlock 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_FinallyBlock(
    o : FinallyBlock, depth : int = 0, relation : str = "", 
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []


    stack : list[Union[SP_FinallyBlock, list[prod_inst.instance]]] = [SP_FinallyBlock(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_FinallyBlock):
            o = item.o

            stack.append(
                serialize_statements(o.body, item.depth + 1, "body", 
                    prod_inst.next_indent_width(item.indent_width, IndentLine()),
                    False,
                )
            )
            stack.append(
                [prod_inst.make_Grammar(
                    nonterminal = 'FinallyBlock',
                    sequence_id = 'FinallyBlock',
                    depth = item.depth,
                    relation = item.relation,
                    indent_width = item.indent_width,
                    inline = item.inline
                )]
            )
        else:
            result += item

    return result




@dataclass
class SP_return_type:
    o : return_type 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_return_type(
    o : return_type, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_return_type, list[prod_inst.instance]]] = [SP_return_type(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_return_type):
            o = item.o

            def handle_SomeReturnType(o : SomeReturnType): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_return_type)

                stack.append(
                    serialize_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'return_type',
                        sequence_id = 'SomeReturnType',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_NoReturnType(o : NoReturnType): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_return_type)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'return_type',
                        sequence_id = 'NoReturnType',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_return_type(o, ReturnTypeHandlers(
                case_SomeReturnType = handle_SomeReturnType,  
                case_NoReturnType = handle_NoReturnType 
            ))

        else:
            result += item

    return result




@dataclass
class SP_module_id:
    o : module_id 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_module_id(
    o : module_id, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_module_id, list[prod_inst.instance]]] = [SP_module_id(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_module_id):
            o = item.o

            def handle_SomeModuleId(o : SomeModuleId): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_module_id)

                stack.append(
                    [prod_inst.make_Vocab(
                        choices_id = 'module_identifier',
                        word = o.contents,
                        depth = item.depth + 1,
                        relation = "contents"
                    )]
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'module_id',
                        sequence_id = 'SomeModuleId',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_NoModuleId(o : NoModuleId): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_module_id)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'module_id',
                        sequence_id = 'NoModuleId',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_module_id(o, ModuleIdHandlers(
                case_SomeModuleId = handle_SomeModuleId,  
                case_NoModuleId = handle_NoModuleId 
            ))

        else:
            result += item

    return result




@dataclass
class SP_except_arg:
    o : except_arg 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_except_arg(
    o : except_arg, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_except_arg, list[prod_inst.instance]]] = [SP_except_arg(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_except_arg):
            o = item.o

            def handle_SomeExceptArg(o : SomeExceptArg): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_except_arg)

                stack.append(
                    serialize_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'except_arg',
                        sequence_id = 'SomeExceptArg',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_SomeExceptArgName(o : SomeExceptArgName): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_except_arg)

                stack.append(
                    [prod_inst.make_Vocab(
                        choices_id = 'identifier',
                        word = o.name,
                        depth = item.depth + 1,
                        relation = "name"
                    )]
                )
                stack.append(
                    serialize_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'except_arg',
                        sequence_id = 'SomeExceptArgName',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_NoExceptArg(o : NoExceptArg): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_except_arg)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'except_arg',
                        sequence_id = 'NoExceptArg',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_except_arg(o, ExceptArgHandlers(
                case_SomeExceptArg = handle_SomeExceptArg,  
                case_SomeExceptArgName = handle_SomeExceptArgName,  
                case_NoExceptArg = handle_NoExceptArg 
            ))

        else:
            result += item

    return result




@dataclass
class SP_param_type:
    o : param_type 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_param_type(
    o : param_type, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_param_type, list[prod_inst.instance]]] = [SP_param_type(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_param_type):
            o = item.o

            def handle_SomeParamType(o : SomeParamType): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_param_type)

                stack.append(
                    serialize_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'param_type',
                        sequence_id = 'SomeParamType',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_NoParamType(o : NoParamType): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_param_type)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'param_type',
                        sequence_id = 'NoParamType',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_param_type(o, ParamTypeHandlers(
                case_SomeParamType = handle_SomeParamType,  
                case_NoParamType = handle_NoParamType 
            ))

        else:
            result += item

    return result




@dataclass
class SP_param_default:
    o : param_default 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_param_default(
    o : param_default, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_param_default, list[prod_inst.instance]]] = [SP_param_default(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_param_default):
            o = item.o

            def handle_SomeParamDefault(o : SomeParamDefault): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_param_default)

                stack.append(
                    serialize_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'param_default',
                        sequence_id = 'SomeParamDefault',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_NoParamDefault(o : NoParamDefault): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_param_default)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'param_default',
                        sequence_id = 'NoParamDefault',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_param_default(o, ParamDefaultHandlers(
                case_SomeParamDefault = handle_SomeParamDefault,  
                case_NoParamDefault = handle_NoParamDefault 
            ))

        else:
            result += item

    return result




@dataclass
class SP_parameters_d:
    o : parameters_d 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_parameters_d(
    o : parameters_d, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_parameters_d, list[prod_inst.instance]]] = [SP_parameters_d(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_parameters_d):
            o = item.o

            def handle_ConsKwParam(o : ConsKwParam): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_parameters_d)

                stack.append(
                    SP_parameters_d(o.tail, item.depth + 1, "tail", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_Param(o.head, item.depth + 1, "head", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'parameters_d',
                        sequence_id = 'ConsKwParam',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_SingleKwParam(o : SingleKwParam): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_parameters_d)

                stack.append(
                    serialize_Param(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'parameters_d',
                        sequence_id = 'SingleKwParam',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_DictionarySplatParam(o : DictionarySplatParam): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_parameters_d)

                stack.append(
                    serialize_Param(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'parameters_d',
                        sequence_id = 'DictionarySplatParam',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_parameters_d(o, ParametersDHandlers(
                case_ConsKwParam = handle_ConsKwParam,  
                case_SingleKwParam = handle_SingleKwParam,  
                case_DictionarySplatParam = handle_DictionarySplatParam 
            ))

        else:
            result += item

    return result




@dataclass
class SP_parameters_c:
    o : parameters_c 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_parameters_c(
    o : parameters_c, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_parameters_c, list[prod_inst.instance]]] = [SP_parameters_c(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_parameters_c):
            o = item.o

            def handle_SingleListSplatParam(o : SingleListSplatParam): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_parameters_c)

                stack.append(
                    serialize_Param(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'parameters_c',
                        sequence_id = 'SingleListSplatParam',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_TransListSplatParam(o : TransListSplatParam): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_parameters_c)

                stack.append(
                    serialize_parameters_d(o.tail, item.depth + 1, "tail", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_Param(o.head, item.depth + 1, "head", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'parameters_c',
                        sequence_id = 'TransListSplatParam',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_ParamsD(o : ParamsD): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_parameters_c)

                stack.append(
                    serialize_parameters_d(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'parameters_c',
                        sequence_id = 'ParamsD',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_parameters_c(o, ParametersCHandlers(
                case_SingleListSplatParam = handle_SingleListSplatParam,  
                case_TransListSplatParam = handle_TransListSplatParam,  
                case_ParamsD = handle_ParamsD 
            ))

        else:
            result += item

    return result




@dataclass
class SP_parameters_b:
    o : parameters_b 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_parameters_b(
    o : parameters_b, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_parameters_b, list[prod_inst.instance]]] = [SP_parameters_b(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_parameters_b):
            o = item.o

            def handle_ConsParam(o : ConsParam): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_parameters_b)

                stack.append(
                    SP_parameters_b(o.tail, item.depth + 1, "tail", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_Param(o.head, item.depth + 1, "head", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'parameters_b',
                        sequence_id = 'ConsParam',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_SingleParam(o : SingleParam): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_parameters_b)

                stack.append(
                    serialize_Param(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'parameters_b',
                        sequence_id = 'SingleParam',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_ParamsC(o : ParamsC): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_parameters_b)

                stack.append(
                    serialize_parameters_c(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'parameters_b',
                        sequence_id = 'ParamsC',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_parameters_b(o, ParametersBHandlers(
                case_ConsParam = handle_ConsParam,  
                case_SingleParam = handle_SingleParam,  
                case_ParamsC = handle_ParamsC 
            ))

        else:
            result += item

    return result




@dataclass
class SP_parameters:
    o : parameters 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_parameters(
    o : parameters, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_parameters, list[prod_inst.instance]]] = [SP_parameters(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_parameters):
            o = item.o

            def handle_ParamsA(o : ParamsA): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_parameters)

                stack.append(
                    serialize_parameters_a(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'parameters',
                        sequence_id = 'ParamsA',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_ParamsB(o : ParamsB): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_parameters)

                stack.append(
                    serialize_parameters_b(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'parameters',
                        sequence_id = 'ParamsB',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_NoParam(o : NoParam): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_parameters)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'parameters',
                        sequence_id = 'NoParam',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_parameters(o, ParametersHandlers(
                case_ParamsA = handle_ParamsA,  
                case_ParamsB = handle_ParamsB,  
                case_NoParam = handle_NoParam 
            ))

        else:
            result += item

    return result




@dataclass
class SP_parameters_a:
    o : parameters_a 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_parameters_a(
    o : parameters_a, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_parameters_a, list[prod_inst.instance]]] = [SP_parameters_a(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_parameters_a):
            o = item.o

            def handle_ConsPosParam(o : ConsPosParam): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_parameters_a)

                stack.append(
                    SP_parameters_a(o.tail, item.depth + 1, "tail", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_Param(o.head, item.depth + 1, "head", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'parameters_a',
                        sequence_id = 'ConsPosParam',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_SinglePosParam(o : SinglePosParam): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_parameters_a)

                stack.append(
                    serialize_Param(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'parameters_a',
                        sequence_id = 'SinglePosParam',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_TransPosParam(o : TransPosParam): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_parameters_a)

                stack.append(
                    serialize_parameters_b(o.tail, item.depth + 1, "tail", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_Param(o.head, item.depth + 1, "head", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'parameters_a',
                        sequence_id = 'TransPosParam',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_parameters_a(o, ParametersAHandlers(
                case_ConsPosParam = handle_ConsPosParam,  
                case_SinglePosParam = handle_SinglePosParam,  
                case_TransPosParam = handle_TransPosParam 
            ))

        else:
            result += item

    return result




@dataclass
class SP_keyword:
    o : keyword 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_keyword(
    o : keyword, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_keyword, list[prod_inst.instance]]] = [SP_keyword(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_keyword):
            o = item.o

            def handle_NamedKeyword(o : NamedKeyword): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_keyword)

                stack.append(
                    serialize_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Vocab(
                        choices_id = 'identifier',
                        word = o.name,
                        depth = item.depth + 1,
                        relation = "name"
                    )]
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'keyword',
                        sequence_id = 'NamedKeyword',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_SplatKeyword(o : SplatKeyword): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_keyword)

                stack.append(
                    serialize_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'keyword',
                        sequence_id = 'SplatKeyword',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_keyword(o, KeywordHandlers(
                case_NamedKeyword = handle_NamedKeyword,  
                case_SplatKeyword = handle_SplatKeyword 
            ))

        else:
            result += item

    return result




@dataclass
class SP_alias:
    o : alias 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_alias(
    o : alias, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_alias, list[prod_inst.instance]]] = [SP_alias(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_alias):
            o = item.o

            def handle_SomeAlias(o : SomeAlias): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_alias)

                stack.append(
                    [prod_inst.make_Vocab(
                        choices_id = 'identifier',
                        word = o.contents,
                        depth = item.depth + 1,
                        relation = "contents"
                    )]
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'alias',
                        sequence_id = 'SomeAlias',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_NoAlias(o : NoAlias): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_alias)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'alias',
                        sequence_id = 'NoAlias',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_alias(o, AliasHandlers(
                case_SomeAlias = handle_SomeAlias,  
                case_NoAlias = handle_NoAlias 
            ))

        else:
            result += item

    return result




@dataclass
class SP_alias_expr:
    o : alias_expr 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_alias_expr(
    o : alias_expr, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_alias_expr, list[prod_inst.instance]]] = [SP_alias_expr(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_alias_expr):
            o = item.o

            def handle_SomeAliasExpr(o : SomeAliasExpr): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_alias_expr)

                stack.append(
                    serialize_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'alias_expr',
                        sequence_id = 'SomeAliasExpr',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_NoAliasExpr(o : NoAliasExpr): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_alias_expr)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'alias_expr',
                        sequence_id = 'NoAliasExpr',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_alias_expr(o, AliasExprHandlers(
                case_SomeAliasExpr = handle_SomeAliasExpr,  
                case_NoAliasExpr = handle_NoAliasExpr 
            ))

        else:
            result += item

    return result




@dataclass
class SP_bases:
    o : bases 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_bases(
    o : bases, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_bases, list[prod_inst.instance]]] = [SP_bases(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_bases):
            o = item.o

            def handle_SomeBases(o : SomeBases): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_bases)

                stack.append(
                    serialize_bases_a(o.bases, item.depth + 1, "bases", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'bases',
                        sequence_id = 'SomeBases',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_NoBases(o : NoBases): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_bases)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'bases',
                        sequence_id = 'NoBases',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_bases(o, BasesHandlers(
                case_SomeBases = handle_SomeBases,  
                case_NoBases = handle_NoBases 
            ))

        else:
            result += item

    return result




@dataclass
class SP_bases_a:
    o : bases_a 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_bases_a(
    o : bases_a, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_bases_a, list[prod_inst.instance]]] = [SP_bases_a(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_bases_a):
            o = item.o

            def handle_ConsBase(o : ConsBase): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_bases_a)

                stack.append(
                    SP_bases_a(o.tail, item.depth + 1, "tail", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_expr(o.head, item.depth + 1, "head", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'bases_a',
                        sequence_id = 'ConsBase',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_SingleBase(o : SingleBase): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_bases_a)

                stack.append(
                    serialize_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'bases_a',
                        sequence_id = 'SingleBase',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_KeywordsBase(o : KeywordsBase): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_bases_a)

                stack.append(
                    serialize_keywords(o.kws, item.depth + 1, "kws", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'bases_a',
                        sequence_id = 'KeywordsBase',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_bases_a(o, BasesAHandlers(
                case_ConsBase = handle_ConsBase,  
                case_SingleBase = handle_SingleBase,  
                case_KeywordsBase = handle_KeywordsBase 
            ))

        else:
            result += item

    return result




@dataclass
class SP_keywords:
    o : keywords 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_keywords(
    o : keywords, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_keywords, list[prod_inst.instance]]] = [SP_keywords(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_keywords):
            o = item.o

            def handle_ConsKeyword(o : ConsKeyword): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_keywords)

                stack.append(
                    SP_keywords(o.tail, item.depth + 1, "tail", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_keyword(o.head, item.depth + 1, "head", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'keywords',
                        sequence_id = 'ConsKeyword',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_SingleKeyword(o : SingleKeyword): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_keywords)

                stack.append(
                    serialize_keyword(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'keywords',
                        sequence_id = 'SingleKeyword',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_keywords(o, KeywordsHandlers(
                case_ConsKeyword = handle_ConsKeyword,  
                case_SingleKeyword = handle_SingleKeyword 
            ))

        else:
            result += item

    return result




@dataclass
class SP_comparisons:
    o : comparisons 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_comparisons(
    o : comparisons, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_comparisons, list[prod_inst.instance]]] = [SP_comparisons(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_comparisons):
            o = item.o

            def handle_ConsCompareRight(o : ConsCompareRight): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_comparisons)

                stack.append(
                    SP_comparisons(o.tail, item.depth + 1, "tail", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_CompareRight(o.head, item.depth + 1, "head", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'comparisons',
                        sequence_id = 'ConsCompareRight',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_SingleCompareRight(o : SingleCompareRight): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_comparisons)

                stack.append(
                    serialize_CompareRight(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'comparisons',
                        sequence_id = 'SingleCompareRight',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_comparisons(o, ComparisonsHandlers(
                case_ConsCompareRight = handle_ConsCompareRight,  
                case_SingleCompareRight = handle_SingleCompareRight 
            ))

        else:
            result += item

    return result




@dataclass
class SP_option_expr:
    o : option_expr 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_option_expr(
    o : option_expr, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_option_expr, list[prod_inst.instance]]] = [SP_option_expr(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_option_expr):
            o = item.o

            def handle_SomeExpr(o : SomeExpr): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_option_expr)

                stack.append(
                    serialize_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'option_expr',
                        sequence_id = 'SomeExpr',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_NoExpr(o : NoExpr): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_option_expr)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'option_expr',
                        sequence_id = 'NoExpr',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_option_expr(o, OptionExprHandlers(
                case_SomeExpr = handle_SomeExpr,  
                case_NoExpr = handle_NoExpr 
            ))

        else:
            result += item

    return result




@dataclass
class SP_comma_exprs:
    o : comma_exprs 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_comma_exprs(
    o : comma_exprs, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_comma_exprs, list[prod_inst.instance]]] = [SP_comma_exprs(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_comma_exprs):
            o = item.o

            def handle_ConsExpr(o : ConsExpr): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_comma_exprs)

                stack.append(
                    SP_comma_exprs(o.tail, item.depth + 1, "tail", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_expr(o.head, item.depth + 1, "head", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'comma_exprs',
                        sequence_id = 'ConsExpr',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_SingleExpr(o : SingleExpr): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_comma_exprs)

                stack.append(
                    serialize_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'comma_exprs',
                        sequence_id = 'SingleExpr',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_comma_exprs(o, CommaExprsHandlers(
                case_ConsExpr = handle_ConsExpr,  
                case_SingleExpr = handle_SingleExpr 
            ))

        else:
            result += item

    return result




@dataclass
class SP_target_exprs:
    o : target_exprs 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_target_exprs(
    o : target_exprs, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_target_exprs, list[prod_inst.instance]]] = [SP_target_exprs(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_target_exprs):
            o = item.o

            def handle_ConsTargetExpr(o : ConsTargetExpr): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_target_exprs)

                stack.append(
                    SP_target_exprs(o.tail, item.depth + 1, "tail", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_expr(o.head, item.depth + 1, "head", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'target_exprs',
                        sequence_id = 'ConsTargetExpr',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_SingleTargetExpr(o : SingleTargetExpr): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_target_exprs)

                stack.append(
                    serialize_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'target_exprs',
                        sequence_id = 'SingleTargetExpr',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_target_exprs(o, TargetExprsHandlers(
                case_ConsTargetExpr = handle_ConsTargetExpr,  
                case_SingleTargetExpr = handle_SingleTargetExpr 
            ))

        else:
            result += item

    return result




@dataclass
class SP_decorators:
    o : decorators 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_decorators(
    o : decorators, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_decorators, list[prod_inst.instance]]] = [SP_decorators(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_decorators):
            o = item.o

            def handle_ConsDec(o : ConsDec): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_decorators)

                stack.append(
                    SP_decorators(o.tail, item.depth + 1, "tail", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_expr(o.head, item.depth + 1, "head", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'decorators',
                        sequence_id = 'ConsDec',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_NoDec(o : NoDec): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_decorators)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'decorators',
                        sequence_id = 'NoDec',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_decorators(o, DecoratorsHandlers(
                case_ConsDec = handle_ConsDec,  
                case_NoDec = handle_NoDec 
            ))

        else:
            result += item

    return result




@dataclass
class SP_constraint_filters:
    o : constraint_filters 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_constraint_filters(
    o : constraint_filters, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_constraint_filters, list[prod_inst.instance]]] = [SP_constraint_filters(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_constraint_filters):
            o = item.o

            def handle_ConsFilter(o : ConsFilter): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_constraint_filters)

                stack.append(
                    SP_constraint_filters(o.tail, item.depth + 1, "tail", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_expr(o.head, item.depth + 1, "head", 
                        prod_inst.next_indent_width(item.indent_width, NewLine()),
                        False,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'constraint_filters',
                        sequence_id = 'ConsFilter',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_SingleFilter(o : SingleFilter): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_constraint_filters)

                stack.append(
                    serialize_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, NewLine()),
                        False,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'constraint_filters',
                        sequence_id = 'SingleFilter',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_NoFilter(o : NoFilter): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_constraint_filters)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'constraint_filters',
                        sequence_id = 'NoFilter',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_constraint_filters(o, ConstraintFiltersHandlers(
                case_ConsFilter = handle_ConsFilter,  
                case_SingleFilter = handle_SingleFilter,  
                case_NoFilter = handle_NoFilter 
            ))

        else:
            result += item

    return result




@dataclass
class SP_sequence_string:
    o : sequence_string 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_sequence_string(
    o : sequence_string, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_sequence_string, list[prod_inst.instance]]] = [SP_sequence_string(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_sequence_string):
            o = item.o

            def handle_ConsStr(o : ConsStr): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_sequence_string)

                stack.append(
                    SP_sequence_string(o.tail, item.depth + 1, "tail", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Vocab(
                        choices_id = 'string',
                        word = o.head,
                        depth = item.depth + 1,
                        relation = "head"
                    )]
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'sequence_string',
                        sequence_id = 'ConsStr',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_SingleStr(o : SingleStr): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_sequence_string)

                stack.append(
                    [prod_inst.make_Vocab(
                        choices_id = 'string',
                        word = o.contents,
                        depth = item.depth + 1,
                        relation = "contents"
                    )]
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'sequence_string',
                        sequence_id = 'SingleStr',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_sequence_string(o, SequenceStringHandlers(
                case_ConsStr = handle_ConsStr,  
                case_SingleStr = handle_SingleStr 
            ))

        else:
            result += item

    return result




@dataclass
class SP_arguments:
    o : arguments 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_arguments(
    o : arguments, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_arguments, list[prod_inst.instance]]] = [SP_arguments(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_arguments):
            o = item.o

            def handle_ConsArg(o : ConsArg): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_arguments)

                stack.append(
                    SP_arguments(o.tail, item.depth + 1, "tail", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_expr(o.head, item.depth + 1, "head", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'arguments',
                        sequence_id = 'ConsArg',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_SingleArg(o : SingleArg): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_arguments)

                stack.append(
                    serialize_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'arguments',
                        sequence_id = 'SingleArg',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_KeywordsArg(o : KeywordsArg): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_arguments)

                stack.append(
                    serialize_keywords(o.kws, item.depth + 1, "kws", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'arguments',
                        sequence_id = 'KeywordsArg',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_arguments(o, ArgumentsHandlers(
                case_ConsArg = handle_ConsArg,  
                case_SingleArg = handle_SingleArg,  
                case_KeywordsArg = handle_KeywordsArg 
            ))

        else:
            result += item

    return result




@dataclass
class SP_dictionary_contents:
    o : dictionary_contents 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_dictionary_contents(
    o : dictionary_contents, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_dictionary_contents, list[prod_inst.instance]]] = [SP_dictionary_contents(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_dictionary_contents):
            o = item.o

            def handle_ConsField(o : ConsField): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_dictionary_contents)

                stack.append(
                    SP_dictionary_contents(o.tail, item.depth + 1, "tail", 
                        prod_inst.next_indent_width(item.indent_width, NewLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_Field(o.head, item.depth + 1, "head", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'dictionary_contents',
                        sequence_id = 'ConsField',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_SingleField(o : SingleField): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_dictionary_contents)

                stack.append(
                    serialize_Field(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'dictionary_contents',
                        sequence_id = 'SingleField',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_dictionary_contents(o, DictionaryContentsHandlers(
                case_ConsField = handle_ConsField,  
                case_SingleField = handle_SingleField 
            ))

        else:
            result += item

    return result




@dataclass
class SP_sequence_var:
    o : sequence_var 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_sequence_var(
    o : sequence_var, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_sequence_var, list[prod_inst.instance]]] = [SP_sequence_var(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_sequence_var):
            o = item.o

            def handle_ConsId(o : ConsId): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_sequence_var)

                stack.append(
                    SP_sequence_var(o.tail, item.depth + 1, "tail", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Vocab(
                        choices_id = 'identifier',
                        word = o.head,
                        depth = item.depth + 1,
                        relation = "head"
                    )]
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'sequence_var',
                        sequence_id = 'ConsId',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_SingleId(o : SingleId): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_sequence_var)

                stack.append(
                    [prod_inst.make_Vocab(
                        choices_id = 'identifier',
                        word = o.contents,
                        depth = item.depth + 1,
                        relation = "contents"
                    )]
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'sequence_var',
                        sequence_id = 'SingleId',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_sequence_var(o, SequenceVarHandlers(
                case_ConsId = handle_ConsId,  
                case_SingleId = handle_SingleId 
            ))

        else:
            result += item

    return result




@dataclass
class SP_sequence_ImportName:
    o : sequence_ImportName 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_sequence_ImportName(
    o : sequence_ImportName, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_sequence_ImportName, list[prod_inst.instance]]] = [SP_sequence_ImportName(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_sequence_ImportName):
            o = item.o

            def handle_ConsImportName(o : ConsImportName): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_sequence_ImportName)

                stack.append(
                    SP_sequence_ImportName(o.tail, item.depth + 1, "tail", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_ImportName(o.head, item.depth + 1, "head", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'sequence_ImportName',
                        sequence_id = 'ConsImportName',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_SingleImportName(o : SingleImportName): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_sequence_ImportName)

                stack.append(
                    serialize_ImportName(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'sequence_ImportName',
                        sequence_id = 'SingleImportName',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_sequence_ImportName(o, SequenceImportNameHandlers(
                case_ConsImportName = handle_ConsImportName,  
                case_SingleImportName = handle_SingleImportName 
            ))

        else:
            result += item

    return result




@dataclass
class SP_sequence_Withitem:
    o : sequence_Withitem 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_sequence_Withitem(
    o : sequence_Withitem, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_sequence_Withitem, list[prod_inst.instance]]] = [SP_sequence_Withitem(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_sequence_Withitem):
            o = item.o

            def handle_ConsWithitem(o : ConsWithitem): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_sequence_Withitem)

                stack.append(
                    SP_sequence_Withitem(o.tail, item.depth + 1, "tail", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_Withitem(o.head, item.depth + 1, "head", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'sequence_Withitem',
                        sequence_id = 'ConsWithitem',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_SingleWithitem(o : SingleWithitem): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_sequence_Withitem)

                stack.append(
                    serialize_Withitem(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'sequence_Withitem',
                        sequence_id = 'SingleWithitem',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_sequence_Withitem(o, SequenceWithitemHandlers(
                case_ConsWithitem = handle_ConsWithitem,  
                case_SingleWithitem = handle_SingleWithitem 
            ))

        else:
            result += item

    return result




@dataclass
class SP_statements:
    o : statements 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_statements(
    o : statements, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_statements, list[prod_inst.instance]]] = [SP_statements(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_statements):
            o = item.o

            def handle_ConsStmt(o : ConsStmt): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_statements)

                stack.append(
                    SP_statements(o.tail, item.depth + 1, "tail", 
                        prod_inst.next_indent_width(item.indent_width, NewLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_stmt(o.head, item.depth + 1, "head", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'statements',
                        sequence_id = 'ConsStmt',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_SingleStmt(o : SingleStmt): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_statements)

                stack.append(
                    serialize_stmt(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'statements',
                        sequence_id = 'SingleStmt',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_statements(o, StatementsHandlers(
                case_ConsStmt = handle_ConsStmt,  
                case_SingleStmt = handle_SingleStmt 
            ))

        else:
            result += item

    return result




@dataclass
class SP_comprehension_constraints:
    o : comprehension_constraints 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_comprehension_constraints(
    o : comprehension_constraints, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_comprehension_constraints, list[prod_inst.instance]]] = [SP_comprehension_constraints(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_comprehension_constraints):
            o = item.o

            def handle_ConsConstraint(o : ConsConstraint): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_comprehension_constraints)

                stack.append(
                    SP_comprehension_constraints(o.tail, item.depth + 1, "tail", 
                        prod_inst.next_indent_width(item.indent_width, NewLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_constraint(o.head, item.depth + 1, "head", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'comprehension_constraints',
                        sequence_id = 'ConsConstraint',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_SingleConstraint(o : SingleConstraint): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_comprehension_constraints)

                stack.append(
                    serialize_constraint(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'comprehension_constraints',
                        sequence_id = 'SingleConstraint',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_comprehension_constraints(o, ComprehensionConstraintsHandlers(
                case_ConsConstraint = handle_ConsConstraint,  
                case_SingleConstraint = handle_SingleConstraint 
            ))

        else:
            result += item

    return result




@dataclass
class SP_sequence_ExceptHandler:
    o : sequence_ExceptHandler 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_sequence_ExceptHandler(
    o : sequence_ExceptHandler, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_sequence_ExceptHandler, list[prod_inst.instance]]] = [SP_sequence_ExceptHandler(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_sequence_ExceptHandler):
            o = item.o

            def handle_ConsExceptHandler(o : ConsExceptHandler): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_sequence_ExceptHandler)

                stack.append(
                    SP_sequence_ExceptHandler(o.tail, item.depth + 1, "tail", 
                        prod_inst.next_indent_width(item.indent_width, NewLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_ExceptHandler(o.head, item.depth + 1, "head", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'sequence_ExceptHandler',
                        sequence_id = 'ConsExceptHandler',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_SingleExceptHandler(o : SingleExceptHandler): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_sequence_ExceptHandler)

                stack.append(
                    serialize_ExceptHandler(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'sequence_ExceptHandler',
                        sequence_id = 'SingleExceptHandler',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_sequence_ExceptHandler(o, SequenceExceptHandlerHandlers(
                case_ConsExceptHandler = handle_ConsExceptHandler,  
                case_SingleExceptHandler = handle_SingleExceptHandler 
            ))

        else:
            result += item

    return result




@dataclass
class SP_conditions:
    o : conditions 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_conditions(
    o : conditions, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_conditions, list[prod_inst.instance]]] = [SP_conditions(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_conditions):
            o = item.o

            def handle_ElifCond(o : ElifCond): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_conditions)

                stack.append(
                    SP_conditions(o.tail, item.depth + 1, "tail", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_ElifBlock(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, NewLine()),
                        False,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'conditions',
                        sequence_id = 'ElifCond',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_ElseCond(o : ElseCond): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_conditions)

                stack.append(
                    serialize_ElseBlock(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, NewLine()),
                        False,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'conditions',
                        sequence_id = 'ElseCond',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_NoCond(o : NoCond): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_conditions)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'conditions',
                        sequence_id = 'NoCond',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_conditions(o, ConditionsHandlers(
                case_ElifCond = handle_ElifCond,  
                case_ElseCond = handle_ElseCond,  
                case_NoCond = handle_NoCond 
            ))

        else:
            result += item

    return result




@dataclass
class SP_function_def:
    o : function_def 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_function_def(
    o : function_def, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_function_def, list[prod_inst.instance]]] = [SP_function_def(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_function_def):
            o = item.o

            def handle_FunctionDef(o : FunctionDef): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_function_def)

                stack.append(
                    serialize_statements(o.body, item.depth + 1, "body", 
                        prod_inst.next_indent_width(item.indent_width, IndentLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_return_type(o.ret_typ, item.depth + 1, "ret_typ", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_parameters(o.params, item.depth + 1, "params", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Vocab(
                        choices_id = 'identifier',
                        word = o.name,
                        depth = item.depth + 1,
                        relation = "name"
                    )]
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'function_def',
                        sequence_id = 'FunctionDef',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_AsyncFunctionDef(o : AsyncFunctionDef): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_function_def)

                stack.append(
                    serialize_statements(o.body, item.depth + 1, "body", 
                        prod_inst.next_indent_width(item.indent_width, IndentLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_return_type(o.ret_typ, item.depth + 1, "ret_typ", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_parameters(o.params, item.depth + 1, "params", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Vocab(
                        choices_id = 'identifier',
                        word = o.name,
                        depth = item.depth + 1,
                        relation = "name"
                    )]
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'function_def',
                        sequence_id = 'AsyncFunctionDef',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_function_def(o, FunctionDefHandlers(
                case_FunctionDef = handle_FunctionDef,  
                case_AsyncFunctionDef = handle_AsyncFunctionDef 
            ))

        else:
            result += item

    return result




@dataclass
class SP_stmt:
    o : stmt 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_stmt(
    o : stmt, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_stmt, list[prod_inst.instance]]] = [SP_stmt(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_stmt):
            o = item.o

            def handle_DecFunctionDef(o : DecFunctionDef): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_function_def(o.fun_def, item.depth + 1, "fun_def", 
                        prod_inst.next_indent_width(item.indent_width, NewLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_decorators(o.decs, item.depth + 1, "decs", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'DecFunctionDef',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_DecAsyncFunctionDef(o : DecAsyncFunctionDef): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_function_def(o.fun_def, item.depth + 1, "fun_def", 
                        prod_inst.next_indent_width(item.indent_width, NewLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_decorators(o.decs, item.depth + 1, "decs", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'DecAsyncFunctionDef',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_DecClassDef(o : DecClassDef): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_ClassDef(o.class_def, item.depth + 1, "class_def", 
                        prod_inst.next_indent_width(item.indent_width, NewLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_decorators(o.decs, item.depth + 1, "decs", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'DecClassDef',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_ReturnSomething(o : ReturnSomething): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'ReturnSomething',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Return(o : Return): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'Return',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Delete(o : Delete): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_comma_exprs(o.targets, item.depth + 1, "targets", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'Delete',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Assign(o : Assign): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_target_exprs(o.targets, item.depth + 1, "targets", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'Assign',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_AugAssign(o : AugAssign): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_operator(o.op, item.depth + 1, "op", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_expr(o.target, item.depth + 1, "target", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'AugAssign',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_TypedAssign(o : TypedAssign): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_expr(o.type, item.depth + 1, "type", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_expr(o.target, item.depth + 1, "target", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'TypedAssign',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_TypedDeclare(o : TypedDeclare): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_expr(o.type, item.depth + 1, "type", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_expr(o.target, item.depth + 1, "target", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'TypedDeclare',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_For(o : For): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_statements(o.body, item.depth + 1, "body", 
                        prod_inst.next_indent_width(item.indent_width, IndentLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_expr(o.iter, item.depth + 1, "iter", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_expr(o.target, item.depth + 1, "target", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'For',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_ForElse(o : ForElse): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_ElseBlock(o.orelse, item.depth + 1, "orelse", 
                        prod_inst.next_indent_width(item.indent_width, NewLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_statements(o.body, item.depth + 1, "body", 
                        prod_inst.next_indent_width(item.indent_width, IndentLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_expr(o.iter, item.depth + 1, "iter", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_expr(o.target, item.depth + 1, "target", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'ForElse',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_AsyncFor(o : AsyncFor): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_statements(o.body, item.depth + 1, "body", 
                        prod_inst.next_indent_width(item.indent_width, IndentLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_expr(o.iter, item.depth + 1, "iter", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_expr(o.target, item.depth + 1, "target", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'AsyncFor',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_AsyncForElse(o : AsyncForElse): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_ElseBlock(o.orelse, item.depth + 1, "orelse", 
                        prod_inst.next_indent_width(item.indent_width, NewLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_statements(o.body, item.depth + 1, "body", 
                        prod_inst.next_indent_width(item.indent_width, IndentLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_expr(o.iter, item.depth + 1, "iter", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_expr(o.target, item.depth + 1, "target", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'AsyncForElse',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_While(o : While): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_statements(o.body, item.depth + 1, "body", 
                        prod_inst.next_indent_width(item.indent_width, IndentLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_expr(o.test, item.depth + 1, "test", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'While',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_WhileElse(o : WhileElse): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_ElseBlock(o.orelse, item.depth + 1, "orelse", 
                        prod_inst.next_indent_width(item.indent_width, NewLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_statements(o.body, item.depth + 1, "body", 
                        prod_inst.next_indent_width(item.indent_width, IndentLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_expr(o.test, item.depth + 1, "test", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'WhileElse',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_If(o : If): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_conditions(o.orelse, item.depth + 1, "orelse", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_statements(o.body, item.depth + 1, "body", 
                        prod_inst.next_indent_width(item.indent_width, IndentLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_expr(o.test, item.depth + 1, "test", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'If',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_With(o : With): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_statements(o.body, item.depth + 1, "body", 
                        prod_inst.next_indent_width(item.indent_width, IndentLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_sequence_Withitem(o.items, item.depth + 1, "items", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'With',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_AsyncWith(o : AsyncWith): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_statements(o.body, item.depth + 1, "body", 
                        prod_inst.next_indent_width(item.indent_width, IndentLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_sequence_Withitem(o.items, item.depth + 1, "items", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'AsyncWith',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Raise(o : Raise): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'Raise',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_RaiseExc(o : RaiseExc): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_expr(o.exc, item.depth + 1, "exc", 
                        prod_inst.next_indent_width(item.indent_width, IndentLine()),
                        False,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'RaiseExc',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_RaiseFrom(o : RaiseFrom): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_expr(o.caus, item.depth + 1, "caus", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_expr(o.exc, item.depth + 1, "exc", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'RaiseFrom',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Try(o : Try): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_sequence_ExceptHandler(o.handlers, item.depth + 1, "handlers", 
                        prod_inst.next_indent_width(item.indent_width, NewLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_statements(o.body, item.depth + 1, "body", 
                        prod_inst.next_indent_width(item.indent_width, IndentLine()),
                        False,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'Try',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_TryElse(o : TryElse): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_ElseBlock(o.orelse, item.depth + 1, "orelse", 
                        prod_inst.next_indent_width(item.indent_width, NewLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_sequence_ExceptHandler(o.handlers, item.depth + 1, "handlers", 
                        prod_inst.next_indent_width(item.indent_width, NewLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_statements(o.body, item.depth + 1, "body", 
                        prod_inst.next_indent_width(item.indent_width, IndentLine()),
                        False,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'TryElse',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_TryFin(o : TryFin): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_FinallyBlock(o.fin, item.depth + 1, "fin", 
                        prod_inst.next_indent_width(item.indent_width, NewLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_sequence_ExceptHandler(o.handlers, item.depth + 1, "handlers", 
                        prod_inst.next_indent_width(item.indent_width, NewLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_statements(o.body, item.depth + 1, "body", 
                        prod_inst.next_indent_width(item.indent_width, IndentLine()),
                        False,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'TryFin',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_TryElseFin(o : TryElseFin): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_FinallyBlock(o.fin, item.depth + 1, "fin", 
                        prod_inst.next_indent_width(item.indent_width, NewLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_ElseBlock(o.orelse, item.depth + 1, "orelse", 
                        prod_inst.next_indent_width(item.indent_width, NewLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_sequence_ExceptHandler(o.handlers, item.depth + 1, "handlers", 
                        prod_inst.next_indent_width(item.indent_width, NewLine()),
                        False,
                    )
                )
                stack.append(
                    serialize_statements(o.body, item.depth + 1, "body", 
                        prod_inst.next_indent_width(item.indent_width, IndentLine()),
                        False,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'TryElseFin',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Assert(o : Assert): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_expr(o.test, item.depth + 1, "test", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'Assert',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_AssertMsg(o : AssertMsg): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_expr(o.msg, item.depth + 1, "msg", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_expr(o.test, item.depth + 1, "test", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'AssertMsg',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Import(o : Import): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_sequence_ImportName(o.names, item.depth + 1, "names", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'Import',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_ImportFrom(o : ImportFrom): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_sequence_ImportName(o.names, item.depth + 1, "names", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_module_id(o.module, item.depth + 1, "module", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'ImportFrom',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_ImportWildCard(o : ImportWildCard): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_module_id(o.module, item.depth + 1, "module", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'ImportWildCard',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Global(o : Global): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_sequence_var(o.names, item.depth + 1, "names", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'Global',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Nonlocal(o : Nonlocal): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_sequence_var(o.names, item.depth + 1, "names", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'Nonlocal',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Expr(o : Expr): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    serialize_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'Expr',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Pass(o : Pass): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'Pass',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Break(o : Break): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'Break',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Continue(o : Continue): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_stmt)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'stmt',
                        sequence_id = 'Continue',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_stmt(o, StmtHandlers(
                case_DecFunctionDef = handle_DecFunctionDef,  
                case_DecAsyncFunctionDef = handle_DecAsyncFunctionDef,  
                case_DecClassDef = handle_DecClassDef,  
                case_ReturnSomething = handle_ReturnSomething,  
                case_Return = handle_Return,  
                case_Delete = handle_Delete,  
                case_Assign = handle_Assign,  
                case_AugAssign = handle_AugAssign,  
                case_TypedAssign = handle_TypedAssign,  
                case_TypedDeclare = handle_TypedDeclare,  
                case_For = handle_For,  
                case_ForElse = handle_ForElse,  
                case_AsyncFor = handle_AsyncFor,  
                case_AsyncForElse = handle_AsyncForElse,  
                case_While = handle_While,  
                case_WhileElse = handle_WhileElse,  
                case_If = handle_If,  
                case_With = handle_With,  
                case_AsyncWith = handle_AsyncWith,  
                case_Raise = handle_Raise,  
                case_RaiseExc = handle_RaiseExc,  
                case_RaiseFrom = handle_RaiseFrom,  
                case_Try = handle_Try,  
                case_TryElse = handle_TryElse,  
                case_TryFin = handle_TryFin,  
                case_TryElseFin = handle_TryElseFin,  
                case_Assert = handle_Assert,  
                case_AssertMsg = handle_AssertMsg,  
                case_Import = handle_Import,  
                case_ImportFrom = handle_ImportFrom,  
                case_ImportWildCard = handle_ImportWildCard,  
                case_Global = handle_Global,  
                case_Nonlocal = handle_Nonlocal,  
                case_Expr = handle_Expr,  
                case_Pass = handle_Pass,  
                case_Break = handle_Break,  
                case_Continue = handle_Continue 
            ))

        else:
            result += item

    return result




@dataclass
class SP_expr:
    o : expr 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_expr(
    o : expr, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_expr, list[prod_inst.instance]]] = [SP_expr(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_expr):
            o = item.o

            def handle_BoolOp(o : BoolOp): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    SP_expr(o.right, item.depth + 1, "right", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_boolop(o.op, item.depth + 1, "op", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    SP_expr(o.left, item.depth + 1, "left", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'BoolOp',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_NamedExpr(o : NamedExpr): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    SP_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    SP_expr(o.target, item.depth + 1, "target", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'NamedExpr',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_BinOp(o : BinOp): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    SP_expr(o.right, item.depth + 1, "right", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_operator(o.op, item.depth + 1, "op", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    SP_expr(o.left, item.depth + 1, "left", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'BinOp',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_UnaryOp(o : UnaryOp): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    SP_expr(o.right, item.depth + 1, "right", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_unaryop(o.op, item.depth + 1, "op", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'UnaryOp',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Lambda(o : Lambda): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    SP_expr(o.body, item.depth + 1, "body", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_parameters(o.params, item.depth + 1, "params", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'Lambda',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_IfExp(o : IfExp): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    SP_expr(o.orelse, item.depth + 1, "orelse", 
                        prod_inst.next_indent_width(item.indent_width, NewLine()),
                        False,
                    )
                )
                stack.append(
                    SP_expr(o.test, item.depth + 1, "test", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    SP_expr(o.body, item.depth + 1, "body", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'IfExp',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Dictionary(o : Dictionary): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    serialize_dictionary_contents(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, IndentLine()),
                        False,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'Dictionary',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_EmptyDictionary(o : EmptyDictionary): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'EmptyDictionary',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Set(o : Set): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    serialize_comma_exprs(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, IndentLine()),
                        False,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'Set',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_ListComp(o : ListComp): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    serialize_comprehension_constraints(o.constraints, item.depth + 1, "constraints", 
                        prod_inst.next_indent_width(item.indent_width, IndentLine()),
                        False,
                    )
                )
                stack.append(
                    SP_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, IndentLine()),
                        False,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'ListComp',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_SetComp(o : SetComp): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    serialize_comprehension_constraints(o.constraints, item.depth + 1, "constraints", 
                        prod_inst.next_indent_width(item.indent_width, IndentLine()),
                        False,
                    )
                )
                stack.append(
                    SP_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, IndentLine()),
                        False,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'SetComp',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_DictionaryComp(o : DictionaryComp): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    serialize_comprehension_constraints(o.constraints, item.depth + 1, "constraints", 
                        prod_inst.next_indent_width(item.indent_width, IndentLine()),
                        False,
                    )
                )
                stack.append(
                    SP_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    SP_expr(o.key, item.depth + 1, "key", 
                        prod_inst.next_indent_width(item.indent_width, IndentLine()),
                        False,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'DictionaryComp',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_GeneratorExp(o : GeneratorExp): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    serialize_comprehension_constraints(o.constraints, item.depth + 1, "constraints", 
                        prod_inst.next_indent_width(item.indent_width, IndentLine()),
                        False,
                    )
                )
                stack.append(
                    SP_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, IndentLine()),
                        False,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'GeneratorExp',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Await(o : Await): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    SP_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'Await',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_YieldNothing(o : YieldNothing): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'YieldNothing',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Yield(o : Yield): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    SP_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'Yield',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_YieldFrom(o : YieldFrom): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    SP_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'YieldFrom',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Compare(o : Compare): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    serialize_comparisons(o.comps, item.depth + 1, "comps", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    SP_expr(o.left, item.depth + 1, "left", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'Compare',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Call(o : Call): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    SP_expr(o.func, item.depth + 1, "func", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'Call',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_CallArgs(o : CallArgs): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    serialize_arguments(o.args, item.depth + 1, "args", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    SP_expr(o.func, item.depth + 1, "func", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'CallArgs',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Integer(o : Integer): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    [prod_inst.make_Vocab(
                        choices_id = 'integer',
                        word = o.contents,
                        depth = item.depth + 1,
                        relation = "contents"
                    )]
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'Integer',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Float(o : Float): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    [prod_inst.make_Vocab(
                        choices_id = 'float',
                        word = o.contents,
                        depth = item.depth + 1,
                        relation = "contents"
                    )]
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'Float',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_ConcatString(o : ConcatString): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    serialize_sequence_string(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'ConcatString',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_True_(o : True_): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'True_',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_False_(o : False_): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'False_',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_None_(o : None_): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'None_',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Ellip(o : Ellip): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'Ellip',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Attribute(o : Attribute): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    [prod_inst.make_Vocab(
                        choices_id = 'identifier',
                        word = o.name,
                        depth = item.depth + 1,
                        relation = "name"
                    )]
                )
                stack.append(
                    SP_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'Attribute',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Subscript(o : Subscript): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    SP_expr(o.slice, item.depth + 1, "slice", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    SP_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'Subscript',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Starred(o : Starred): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    SP_expr(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'Starred',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Name(o : Name): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    [prod_inst.make_Vocab(
                        choices_id = 'identifier',
                        word = o.contents,
                        depth = item.depth + 1,
                        relation = "contents"
                    )]
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'Name',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_List(o : List): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    serialize_comma_exprs(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'List',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_EmptyList(o : EmptyList): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'EmptyList',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Tuple(o : Tuple): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    serialize_comma_exprs(o.contents, item.depth + 1, "contents", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'Tuple',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_EmptyTuple(o : EmptyTuple): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'EmptyTuple',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Slice(o : Slice): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_expr)

                stack.append(
                    serialize_option_expr(o.step, item.depth + 1, "step", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_option_expr(o.upper, item.depth + 1, "upper", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_option_expr(o.lower, item.depth + 1, "lower", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'expr',
                        sequence_id = 'Slice',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_expr(o, ExprHandlers(
                case_BoolOp = handle_BoolOp,  
                case_NamedExpr = handle_NamedExpr,  
                case_BinOp = handle_BinOp,  
                case_UnaryOp = handle_UnaryOp,  
                case_Lambda = handle_Lambda,  
                case_IfExp = handle_IfExp,  
                case_Dictionary = handle_Dictionary,  
                case_EmptyDictionary = handle_EmptyDictionary,  
                case_Set = handle_Set,  
                case_ListComp = handle_ListComp,  
                case_SetComp = handle_SetComp,  
                case_DictionaryComp = handle_DictionaryComp,  
                case_GeneratorExp = handle_GeneratorExp,  
                case_Await = handle_Await,  
                case_YieldNothing = handle_YieldNothing,  
                case_Yield = handle_Yield,  
                case_YieldFrom = handle_YieldFrom,  
                case_Compare = handle_Compare,  
                case_Call = handle_Call,  
                case_CallArgs = handle_CallArgs,  
                case_Integer = handle_Integer,  
                case_Float = handle_Float,  
                case_ConcatString = handle_ConcatString,  
                case_True_ = handle_True_,  
                case_False_ = handle_False_,  
                case_None_ = handle_None_,  
                case_Ellip = handle_Ellip,  
                case_Attribute = handle_Attribute,  
                case_Subscript = handle_Subscript,  
                case_Starred = handle_Starred,  
                case_Name = handle_Name,  
                case_List = handle_List,  
                case_EmptyList = handle_EmptyList,  
                case_Tuple = handle_Tuple,  
                case_EmptyTuple = handle_EmptyTuple,  
                case_Slice = handle_Slice 
            ))

        else:
            result += item

    return result




@dataclass
class SP_boolop:
    o : boolop 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_boolop(
    o : boolop, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_boolop, list[prod_inst.instance]]] = [SP_boolop(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_boolop):
            o = item.o

            def handle_And(o : And): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_boolop)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'boolop',
                        sequence_id = 'And',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Or(o : Or): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_boolop)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'boolop',
                        sequence_id = 'Or',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_boolop(o, BoolopHandlers(
                case_And = handle_And,  
                case_Or = handle_Or 
            ))

        else:
            result += item

    return result




@dataclass
class SP_operator:
    o : operator 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_operator(
    o : operator, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_operator, list[prod_inst.instance]]] = [SP_operator(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_operator):
            o = item.o

            def handle_Add(o : Add): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_operator)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'operator',
                        sequence_id = 'Add',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Sub(o : Sub): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_operator)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'operator',
                        sequence_id = 'Sub',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Mult(o : Mult): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_operator)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'operator',
                        sequence_id = 'Mult',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_MatMult(o : MatMult): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_operator)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'operator',
                        sequence_id = 'MatMult',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Div(o : Div): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_operator)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'operator',
                        sequence_id = 'Div',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Mod(o : Mod): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_operator)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'operator',
                        sequence_id = 'Mod',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Pow(o : Pow): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_operator)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'operator',
                        sequence_id = 'Pow',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_LShift(o : LShift): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_operator)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'operator',
                        sequence_id = 'LShift',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_RShift(o : RShift): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_operator)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'operator',
                        sequence_id = 'RShift',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_BitOr(o : BitOr): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_operator)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'operator',
                        sequence_id = 'BitOr',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_BitXor(o : BitXor): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_operator)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'operator',
                        sequence_id = 'BitXor',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_BitAnd(o : BitAnd): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_operator)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'operator',
                        sequence_id = 'BitAnd',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_FloorDiv(o : FloorDiv): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_operator)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'operator',
                        sequence_id = 'FloorDiv',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_operator(o, OperatorHandlers(
                case_Add = handle_Add,  
                case_Sub = handle_Sub,  
                case_Mult = handle_Mult,  
                case_MatMult = handle_MatMult,  
                case_Div = handle_Div,  
                case_Mod = handle_Mod,  
                case_Pow = handle_Pow,  
                case_LShift = handle_LShift,  
                case_RShift = handle_RShift,  
                case_BitOr = handle_BitOr,  
                case_BitXor = handle_BitXor,  
                case_BitAnd = handle_BitAnd,  
                case_FloorDiv = handle_FloorDiv 
            ))

        else:
            result += item

    return result




@dataclass
class SP_unaryop:
    o : unaryop 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_unaryop(
    o : unaryop, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_unaryop, list[prod_inst.instance]]] = [SP_unaryop(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_unaryop):
            o = item.o

            def handle_Invert(o : Invert): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_unaryop)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'unaryop',
                        sequence_id = 'Invert',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Not(o : Not): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_unaryop)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'unaryop',
                        sequence_id = 'Not',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_UAdd(o : UAdd): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_unaryop)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'unaryop',
                        sequence_id = 'UAdd',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_USub(o : USub): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_unaryop)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'unaryop',
                        sequence_id = 'USub',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_unaryop(o, UnaryopHandlers(
                case_Invert = handle_Invert,  
                case_Not = handle_Not,  
                case_UAdd = handle_UAdd,  
                case_USub = handle_USub 
            ))

        else:
            result += item

    return result




@dataclass
class SP_cmpop:
    o : cmpop 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_cmpop(
    o : cmpop, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_cmpop, list[prod_inst.instance]]] = [SP_cmpop(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_cmpop):
            o = item.o

            def handle_Eq(o : Eq): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_cmpop)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'cmpop',
                        sequence_id = 'Eq',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_NotEq(o : NotEq): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_cmpop)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'cmpop',
                        sequence_id = 'NotEq',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Lt(o : Lt): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_cmpop)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'cmpop',
                        sequence_id = 'Lt',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_LtE(o : LtE): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_cmpop)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'cmpop',
                        sequence_id = 'LtE',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Gt(o : Gt): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_cmpop)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'cmpop',
                        sequence_id = 'Gt',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_GtE(o : GtE): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_cmpop)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'cmpop',
                        sequence_id = 'GtE',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Is(o : Is): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_cmpop)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'cmpop',
                        sequence_id = 'Is',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_IsNot(o : IsNot): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_cmpop)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'cmpop',
                        sequence_id = 'IsNot',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_In(o : In): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_cmpop)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'cmpop',
                        sequence_id = 'In',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_NotIn(o : NotIn): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_cmpop)

                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'cmpop',
                        sequence_id = 'NotIn',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_cmpop(o, CmpopHandlers(
                case_Eq = handle_Eq,  
                case_NotEq = handle_NotEq,  
                case_Lt = handle_Lt,  
                case_LtE = handle_LtE,  
                case_Gt = handle_Gt,  
                case_GtE = handle_GtE,  
                case_Is = handle_Is,  
                case_IsNot = handle_IsNot,  
                case_In = handle_In,  
                case_NotIn = handle_NotIn 
            ))

        else:
            result += item

    return result




@dataclass
class SP_constraint:
    o : constraint 
    depth : int
    relation : str
    indent_width : int 
    inline : bool

def serialize_constraint(
    o : constraint, depth : int = 0, relation : str = "",
    indent_width : int = 0, inline : bool = True
) -> list[prod_inst.instance]:

    result = []

    stack : list[Union[SP_constraint, list[prod_inst.instance]]] = [SP_constraint(o, depth, relation, indent_width, inline)]
    while stack:
        item = stack.pop()
        if isinstance(item, SP_constraint):
            o = item.o

            def handle_AsyncConstraint(o : AsyncConstraint): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_constraint)

                stack.append(
                    serialize_constraint_filters(o.filts, item.depth + 1, "filts", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_expr(o.search_space, item.depth + 1, "search_space", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_expr(o.target, item.depth + 1, "target", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'constraint',
                        sequence_id = 'AsyncConstraint',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )

            def handle_Constraint(o : Constraint): 
                nonlocal stack
                nonlocal item 
                assert isinstance(item, SP_constraint)

                stack.append(
                    serialize_constraint_filters(o.filts, item.depth + 1, "filts", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_expr(o.search_space, item.depth + 1, "search_space", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    serialize_expr(o.target, item.depth + 1, "target", 
                        prod_inst.next_indent_width(item.indent_width, InLine()),
                        True,
                    )
                )
                stack.append(
                    [prod_inst.make_Grammar(
                        nonterminal = 'constraint',
                        sequence_id = 'Constraint',
                        depth = item.depth,
                        relation = item.relation,
                        indent_width = item.indent_width,
                        inline = item.inline
                    )]
                )


            match_constraint(o, ConstraintHandlers(
                case_AsyncConstraint = handle_AsyncConstraint,  
                case_Constraint = handle_Constraint 
            ))

        else:
            result += item

    return result