

from __future__ import annotations
import lib.instance
from gen.instance import instance, Vocab, Grammar
from gen.python_ast import *
from gen.line_format import InLine, NewLine, IndentLine
    

# definitions operate on reversed lists of instances, starting from the right, going left. 

def to_return_type(xs : list[instance]) -> tuple[return_type, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "return_type"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "SomeReturnType": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SomeReturnType(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("SomeReturnType", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SomeReturnType", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "NoReturnType": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    NoReturnType(),
                    next_remainder
                )
            
            else:
                stack.append(("NoReturnType", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], return_type)
    return result
    

def to_module_id(xs : list[instance]) -> tuple[module_id, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "module_id"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "SomeModuleId": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SomeModuleId(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_str(next_remainder)
                stack.append(("SomeModuleId", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SomeModuleId", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], module_id)
    return result
    

def to_except_arg(xs : list[instance]) -> tuple[except_arg, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "except_arg"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "SomeExceptArg": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SomeExceptArg(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("SomeExceptArg", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SomeExceptArg", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "SomeExceptArgName": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SomeExceptArgName(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("SomeExceptArgName", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_str(next_remainder)
                stack.append(("SomeExceptArgName", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SomeExceptArgName", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "NoExceptArg": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    NoExceptArg(),
                    next_remainder
                )
            
            else:
                stack.append(("NoExceptArg", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], except_arg)
    return result
    

def to_param_type(xs : list[instance]) -> tuple[param_type, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "param_type"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "SomeParamType": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SomeParamType(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("SomeParamType", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SomeParamType", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "NoParamType": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    NoParamType(),
                    next_remainder
                )
            
            else:
                stack.append(("NoParamType", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], param_type)
    return result
    

def to_param_default(xs : list[instance]) -> tuple[param_default, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "param_default"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "SomeParamDefault": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SomeParamDefault(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("SomeParamDefault", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SomeParamDefault", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "NoParamDefault": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    NoParamDefault(),
                    next_remainder
                )
            
            else:
                stack.append(("NoParamDefault", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], param_default)
    return result
    

def to_parameters_d(xs : list[instance]) -> tuple[parameters_d, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "parameters_d"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "ConsKwParam": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ConsKwParam(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_Param(next_remainder)
                stack.append(("ConsKwParam", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ConsKwParam", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "SingleKwParam": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SingleKwParam(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_Param(next_remainder)
                stack.append(("SingleKwParam", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SingleKwParam", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "DictionarySplatParam": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    DictionarySplatParam(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_Param(next_remainder)
                stack.append(("DictionarySplatParam", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("DictionarySplatParam", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], parameters_d)
    return result
    

def to_parameters_c(xs : list[instance]) -> tuple[parameters_c, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "parameters_c"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "SingleListSplatParam": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SingleListSplatParam(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_Param(next_remainder)
                stack.append(("SingleListSplatParam", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SingleListSplatParam", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "TransListSplatParam": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    TransListSplatParam(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_Param(next_remainder)
                stack.append(("TransListSplatParam", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_parameters_d(next_remainder)
                stack.append(("TransListSplatParam", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("TransListSplatParam", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "ParamsD": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ParamsD(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_parameters_d(next_remainder)
                stack.append(("ParamsD", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ParamsD", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], parameters_c)
    return result
    

def to_parameters_b(xs : list[instance]) -> tuple[parameters_b, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "parameters_b"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "ConsParam": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ConsParam(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_Param(next_remainder)
                stack.append(("ConsParam", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ConsParam", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "SingleParam": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SingleParam(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_Param(next_remainder)
                stack.append(("SingleParam", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SingleParam", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "ParamsC": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ParamsC(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_parameters_c(next_remainder)
                stack.append(("ParamsC", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ParamsC", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], parameters_b)
    return result
    

def to_parameters(xs : list[instance]) -> tuple[parameters, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "parameters"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "ParamsA": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ParamsA(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_parameters_a(next_remainder)
                stack.append(("ParamsA", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ParamsA", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "ParamsB": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ParamsB(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_parameters_b(next_remainder)
                stack.append(("ParamsB", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ParamsB", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "NoParam": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    NoParam(),
                    next_remainder
                )
            
            else:
                stack.append(("NoParam", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], parameters)
    return result
    

def to_parameters_a(xs : list[instance]) -> tuple[parameters_a, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "parameters_a"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "ConsPosParam": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ConsPosParam(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_Param(next_remainder)
                stack.append(("ConsPosParam", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ConsPosParam", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "SinglePosParam": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SinglePosParam(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_Param(next_remainder)
                stack.append(("SinglePosParam", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SinglePosParam", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "TransPosParam": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    TransPosParam(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_Param(next_remainder)
                stack.append(("TransPosParam", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_parameters_b(next_remainder)
                stack.append(("TransPosParam", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("TransPosParam", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], parameters_a)
    return result
    

def to_keyword(xs : list[instance]) -> tuple[keyword, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "keyword"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "NamedKeyword": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    NamedKeyword(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_str(next_remainder)
                stack.append(("NamedKeyword", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("NamedKeyword", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("NamedKeyword", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "SplatKeyword": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SplatKeyword(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("SplatKeyword", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SplatKeyword", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], keyword)
    return result
    

def to_alias(xs : list[instance]) -> tuple[alias, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "alias"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "SomeAlias": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SomeAlias(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_str(next_remainder)
                stack.append(("SomeAlias", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SomeAlias", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "NoAlias": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    NoAlias(),
                    next_remainder
                )
            
            else:
                stack.append(("NoAlias", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], alias)
    return result
    

def to_alias_expr(xs : list[instance]) -> tuple[alias_expr, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "alias_expr"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "SomeAliasExpr": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SomeAliasExpr(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("SomeAliasExpr", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SomeAliasExpr", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "NoAliasExpr": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    NoAliasExpr(),
                    next_remainder
                )
            
            else:
                stack.append(("NoAliasExpr", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], alias_expr)
    return result
    

def to_bases(xs : list[instance]) -> tuple[bases, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "bases"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "SomeBases": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SomeBases(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_bases_a(next_remainder)
                stack.append(("SomeBases", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SomeBases", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "NoBases": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    NoBases(),
                    next_remainder
                )
            
            else:
                stack.append(("NoBases", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], bases)
    return result
    

def to_bases_a(xs : list[instance]) -> tuple[bases_a, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "bases_a"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "ConsBase": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ConsBase(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("ConsBase", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ConsBase", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "SingleBase": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SingleBase(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("SingleBase", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SingleBase", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "KeywordsBase": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    KeywordsBase(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_keywords(next_remainder)
                stack.append(("KeywordsBase", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("KeywordsBase", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], bases_a)
    return result
    

def to_keywords(xs : list[instance]) -> tuple[keywords, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "keywords"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "ConsKeyword": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ConsKeyword(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_keyword(next_remainder)
                stack.append(("ConsKeyword", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ConsKeyword", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "SingleKeyword": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SingleKeyword(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_keyword(next_remainder)
                stack.append(("SingleKeyword", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SingleKeyword", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], keywords)
    return result
    

def to_comparisons(xs : list[instance]) -> tuple[comparisons, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "comparisons"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "ConsCompareRight": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ConsCompareRight(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_CompareRight(next_remainder)
                stack.append(("ConsCompareRight", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ConsCompareRight", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "SingleCompareRight": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SingleCompareRight(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_CompareRight(next_remainder)
                stack.append(("SingleCompareRight", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SingleCompareRight", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], comparisons)
    return result
    

def to_option_expr(xs : list[instance]) -> tuple[option_expr, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "option_expr"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "SomeExpr": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SomeExpr(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("SomeExpr", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SomeExpr", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "NoExpr": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    NoExpr(),
                    next_remainder
                )
            
            else:
                stack.append(("NoExpr", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], option_expr)
    return result
    

def to_comma_exprs(xs : list[instance]) -> tuple[comma_exprs, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "comma_exprs"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "ConsExpr": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ConsExpr(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("ConsExpr", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ConsExpr", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "SingleExpr": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SingleExpr(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("SingleExpr", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SingleExpr", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], comma_exprs)
    return result
    

def to_target_exprs(xs : list[instance]) -> tuple[target_exprs, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "target_exprs"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "ConsTargetExpr": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ConsTargetExpr(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("ConsTargetExpr", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ConsTargetExpr", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "SingleTargetExpr": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SingleTargetExpr(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("SingleTargetExpr", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SingleTargetExpr", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], target_exprs)
    return result
    

def to_decorators(xs : list[instance]) -> tuple[decorators, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "decorators"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "ConsDec": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ConsDec(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("ConsDec", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ConsDec", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "NoDec": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    NoDec(),
                    next_remainder
                )
            
            else:
                stack.append(("NoDec", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], decorators)
    return result
    

def to_constraint_filters(xs : list[instance]) -> tuple[constraint_filters, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "constraint_filters"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "ConsFilter": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ConsFilter(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("ConsFilter", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ConsFilter", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "SingleFilter": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SingleFilter(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("SingleFilter", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SingleFilter", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "NoFilter": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    NoFilter(),
                    next_remainder
                )
            
            else:
                stack.append(("NoFilter", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], constraint_filters)
    return result
    

def to_sequence_string(xs : list[instance]) -> tuple[sequence_string, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "sequence_string"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "ConsStr": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ConsStr(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_str(next_remainder)
                stack.append(("ConsStr", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ConsStr", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "SingleStr": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SingleStr(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_str(next_remainder)
                stack.append(("SingleStr", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SingleStr", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], sequence_string)
    return result
    

def to_arguments(xs : list[instance]) -> tuple[arguments, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "arguments"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "ConsArg": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ConsArg(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("ConsArg", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ConsArg", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "SingleArg": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SingleArg(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("SingleArg", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SingleArg", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "KeywordsArg": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    KeywordsArg(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_keywords(next_remainder)
                stack.append(("KeywordsArg", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("KeywordsArg", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], arguments)
    return result
    

def to_dictionary_item(xs : list[instance]) -> tuple[dictionary_item, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "dictionary_item"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "Field": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Field(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("Field", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("Field", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("Field", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "DictionarySplatFields": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    DictionarySplatFields(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("DictionarySplatFields", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("DictionarySplatFields", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], dictionary_item)
    return result
    

def to_dictionary_contents(xs : list[instance]) -> tuple[dictionary_contents, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "dictionary_contents"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "ConsDictionaryItem": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ConsDictionaryItem(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_dictionary_item(next_remainder)
                stack.append(("ConsDictionaryItem", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ConsDictionaryItem", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "SingleDictionaryItem": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SingleDictionaryItem(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_dictionary_item(next_remainder)
                stack.append(("SingleDictionaryItem", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SingleDictionaryItem", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], dictionary_contents)
    return result
    

def to_sequence_var(xs : list[instance]) -> tuple[sequence_var, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "sequence_var"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "ConsId": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ConsId(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_str(next_remainder)
                stack.append(("ConsId", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ConsId", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "SingleId": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SingleId(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_str(next_remainder)
                stack.append(("SingleId", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SingleId", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], sequence_var)
    return result
    

def to_sequence_ImportName(xs : list[instance]) -> tuple[sequence_ImportName, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "sequence_ImportName"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "ConsImportName": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ConsImportName(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_ImportName(next_remainder)
                stack.append(("ConsImportName", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ConsImportName", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "SingleImportName": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SingleImportName(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_ImportName(next_remainder)
                stack.append(("SingleImportName", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SingleImportName", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], sequence_ImportName)
    return result
    

def to_sequence_Withitem(xs : list[instance]) -> tuple[sequence_Withitem, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "sequence_Withitem"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "ConsWithitem": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ConsWithitem(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_Withitem(next_remainder)
                stack.append(("ConsWithitem", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ConsWithitem", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "SingleWithitem": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SingleWithitem(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_Withitem(next_remainder)
                stack.append(("SingleWithitem", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SingleWithitem", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], sequence_Withitem)
    return result
    

def to_statements(xs : list[instance]) -> tuple[statements, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "statements"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "ConsStmt": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ConsStmt(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_stmt(next_remainder)
                stack.append(("ConsStmt", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ConsStmt", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "SingleStmt": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SingleStmt(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_stmt(next_remainder)
                stack.append(("SingleStmt", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SingleStmt", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], statements)
    return result
    

def to_comprehension_constraints(xs : list[instance]) -> tuple[comprehension_constraints, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "comprehension_constraints"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "ConsConstraint": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ConsConstraint(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_constraint(next_remainder)
                stack.append(("ConsConstraint", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ConsConstraint", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "SingleConstraint": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SingleConstraint(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_constraint(next_remainder)
                stack.append(("SingleConstraint", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SingleConstraint", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], comprehension_constraints)
    return result
    

def to_sequence_ExceptHandler(xs : list[instance]) -> tuple[sequence_ExceptHandler, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "sequence_ExceptHandler"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "ConsExceptHandler": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ConsExceptHandler(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_ExceptHandler(next_remainder)
                stack.append(("ConsExceptHandler", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ConsExceptHandler", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "SingleExceptHandler": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SingleExceptHandler(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_ExceptHandler(next_remainder)
                stack.append(("SingleExceptHandler", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SingleExceptHandler", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], sequence_ExceptHandler)
    return result
    

def to_conditions(xs : list[instance]) -> tuple[conditions, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "conditions"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "ElifCond": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ElifCond(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_ElifBlock(next_remainder)
                stack.append(("ElifCond", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ElifCond", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "ElseCond": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ElseCond(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_ElseBlock(next_remainder)
                stack.append(("ElseCond", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ElseCond", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "NoCond": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    NoCond(),
                    next_remainder
                )
            
            else:
                stack.append(("NoCond", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], conditions)
    return result
    

def to_function_def(xs : list[instance]) -> tuple[function_def, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "function_def"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "FunctionDef": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 4

            index = len(next_children)
            if index == total_num_children:
                result = (
                    FunctionDef(next_children[0], next_children[1], next_children[2], next_children[3]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_str(next_remainder)
                stack.append(("FunctionDef", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_parameters(next_remainder)
                stack.append(("FunctionDef", next_children + [next_child], next_remainder))
                

            elif index == 2:
                (next_child, next_remainder) = to_return_type(next_remainder)
                stack.append(("FunctionDef", next_children + [next_child], next_remainder))
                

            elif index == 3:
                (next_child, next_remainder) = to_statements(next_remainder)
                stack.append(("FunctionDef", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("FunctionDef", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "AsyncFunctionDef": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 4

            index = len(next_children)
            if index == total_num_children:
                result = (
                    AsyncFunctionDef(next_children[0], next_children[1], next_children[2], next_children[3]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_str(next_remainder)
                stack.append(("AsyncFunctionDef", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_parameters(next_remainder)
                stack.append(("AsyncFunctionDef", next_children + [next_child], next_remainder))
                

            elif index == 2:
                (next_child, next_remainder) = to_return_type(next_remainder)
                stack.append(("AsyncFunctionDef", next_children + [next_child], next_remainder))
                

            elif index == 3:
                (next_child, next_remainder) = to_statements(next_remainder)
                stack.append(("AsyncFunctionDef", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("AsyncFunctionDef", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], function_def)
    return result
    

def to_stmt(xs : list[instance]) -> tuple[stmt, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "stmt"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "DecFunctionDef": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    DecFunctionDef(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_decorators(next_remainder)
                stack.append(("DecFunctionDef", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_function_def(next_remainder)
                stack.append(("DecFunctionDef", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("DecFunctionDef", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "DecAsyncFunctionDef": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    DecAsyncFunctionDef(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_decorators(next_remainder)
                stack.append(("DecAsyncFunctionDef", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_function_def(next_remainder)
                stack.append(("DecAsyncFunctionDef", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("DecAsyncFunctionDef", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "DecClassDef": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    DecClassDef(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_decorators(next_remainder)
                stack.append(("DecClassDef", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_ClassDef(next_remainder)
                stack.append(("DecClassDef", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("DecClassDef", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "ReturnSomething": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ReturnSomething(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("ReturnSomething", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ReturnSomething", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Return": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Return(),
                    next_remainder
                )
            
            else:
                stack.append(("Return", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Delete": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Delete(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_comma_exprs(next_remainder)
                stack.append(("Delete", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("Delete", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Assign": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Assign(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_target_exprs(next_remainder)
                stack.append(("Assign", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("Assign", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("Assign", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "AugAssign": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 3

            index = len(next_children)
            if index == total_num_children:
                result = (
                    AugAssign(next_children[0], next_children[1], next_children[2]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("AugAssign", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_operator(next_remainder)
                stack.append(("AugAssign", next_children + [next_child], next_remainder))
                

            elif index == 2:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("AugAssign", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("AugAssign", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "TypedAssign": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 3

            index = len(next_children)
            if index == total_num_children:
                result = (
                    TypedAssign(next_children[0], next_children[1], next_children[2]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("TypedAssign", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("TypedAssign", next_children + [next_child], next_remainder))
                

            elif index == 2:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("TypedAssign", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("TypedAssign", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "TypedDeclare": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    TypedDeclare(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("TypedDeclare", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("TypedDeclare", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("TypedDeclare", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "For": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 3

            index = len(next_children)
            if index == total_num_children:
                result = (
                    For(next_children[0], next_children[1], next_children[2]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("For", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("For", next_children + [next_child], next_remainder))
                

            elif index == 2:
                (next_child, next_remainder) = to_statements(next_remainder)
                stack.append(("For", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("For", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "ForElse": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 4

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ForElse(next_children[0], next_children[1], next_children[2], next_children[3]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("ForElse", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("ForElse", next_children + [next_child], next_remainder))
                

            elif index == 2:
                (next_child, next_remainder) = to_statements(next_remainder)
                stack.append(("ForElse", next_children + [next_child], next_remainder))
                

            elif index == 3:
                (next_child, next_remainder) = to_ElseBlock(next_remainder)
                stack.append(("ForElse", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ForElse", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "AsyncFor": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 3

            index = len(next_children)
            if index == total_num_children:
                result = (
                    AsyncFor(next_children[0], next_children[1], next_children[2]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("AsyncFor", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("AsyncFor", next_children + [next_child], next_remainder))
                

            elif index == 2:
                (next_child, next_remainder) = to_statements(next_remainder)
                stack.append(("AsyncFor", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("AsyncFor", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "AsyncForElse": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 4

            index = len(next_children)
            if index == total_num_children:
                result = (
                    AsyncForElse(next_children[0], next_children[1], next_children[2], next_children[3]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("AsyncForElse", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("AsyncForElse", next_children + [next_child], next_remainder))
                

            elif index == 2:
                (next_child, next_remainder) = to_statements(next_remainder)
                stack.append(("AsyncForElse", next_children + [next_child], next_remainder))
                

            elif index == 3:
                (next_child, next_remainder) = to_ElseBlock(next_remainder)
                stack.append(("AsyncForElse", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("AsyncForElse", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "While": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    While(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("While", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_statements(next_remainder)
                stack.append(("While", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("While", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "WhileElse": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 3

            index = len(next_children)
            if index == total_num_children:
                result = (
                    WhileElse(next_children[0], next_children[1], next_children[2]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("WhileElse", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_statements(next_remainder)
                stack.append(("WhileElse", next_children + [next_child], next_remainder))
                

            elif index == 2:
                (next_child, next_remainder) = to_ElseBlock(next_remainder)
                stack.append(("WhileElse", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("WhileElse", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "If": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 3

            index = len(next_children)
            if index == total_num_children:
                result = (
                    If(next_children[0], next_children[1], next_children[2]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("If", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_statements(next_remainder)
                stack.append(("If", next_children + [next_child], next_remainder))
                

            elif index == 2:
                (next_child, next_remainder) = to_conditions(next_remainder)
                stack.append(("If", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("If", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "With": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    With(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_sequence_Withitem(next_remainder)
                stack.append(("With", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_statements(next_remainder)
                stack.append(("With", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("With", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "AsyncWith": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    AsyncWith(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_sequence_Withitem(next_remainder)
                stack.append(("AsyncWith", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_statements(next_remainder)
                stack.append(("AsyncWith", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("AsyncWith", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Raise": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Raise(),
                    next_remainder
                )
            
            else:
                stack.append(("Raise", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "RaiseExc": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    RaiseExc(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("RaiseExc", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("RaiseExc", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "RaiseFrom": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    RaiseFrom(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("RaiseFrom", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("RaiseFrom", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("RaiseFrom", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Try": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Try(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_statements(next_remainder)
                stack.append(("Try", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_sequence_ExceptHandler(next_remainder)
                stack.append(("Try", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("Try", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "TryElse": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 3

            index = len(next_children)
            if index == total_num_children:
                result = (
                    TryElse(next_children[0], next_children[1], next_children[2]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_statements(next_remainder)
                stack.append(("TryElse", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_sequence_ExceptHandler(next_remainder)
                stack.append(("TryElse", next_children + [next_child], next_remainder))
                

            elif index == 2:
                (next_child, next_remainder) = to_ElseBlock(next_remainder)
                stack.append(("TryElse", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("TryElse", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "TryExceptFin": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 3

            index = len(next_children)
            if index == total_num_children:
                result = (
                    TryExceptFin(next_children[0], next_children[1], next_children[2]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_statements(next_remainder)
                stack.append(("TryExceptFin", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_sequence_ExceptHandler(next_remainder)
                stack.append(("TryExceptFin", next_children + [next_child], next_remainder))
                

            elif index == 2:
                (next_child, next_remainder) = to_FinallyBlock(next_remainder)
                stack.append(("TryExceptFin", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("TryExceptFin", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "TryFin": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    TryFin(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_statements(next_remainder)
                stack.append(("TryFin", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_FinallyBlock(next_remainder)
                stack.append(("TryFin", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("TryFin", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "TryElseFin": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 4

            index = len(next_children)
            if index == total_num_children:
                result = (
                    TryElseFin(next_children[0], next_children[1], next_children[2], next_children[3]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_statements(next_remainder)
                stack.append(("TryElseFin", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_sequence_ExceptHandler(next_remainder)
                stack.append(("TryElseFin", next_children + [next_child], next_remainder))
                

            elif index == 2:
                (next_child, next_remainder) = to_ElseBlock(next_remainder)
                stack.append(("TryElseFin", next_children + [next_child], next_remainder))
                

            elif index == 3:
                (next_child, next_remainder) = to_FinallyBlock(next_remainder)
                stack.append(("TryElseFin", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("TryElseFin", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Assert": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Assert(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("Assert", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("Assert", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "AssertMsg": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    AssertMsg(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("AssertMsg", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("AssertMsg", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("AssertMsg", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Import": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Import(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_sequence_ImportName(next_remainder)
                stack.append(("Import", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("Import", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "ImportFrom": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ImportFrom(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_module_id(next_remainder)
                stack.append(("ImportFrom", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_sequence_ImportName(next_remainder)
                stack.append(("ImportFrom", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ImportFrom", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "ImportWildCard": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ImportWildCard(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_module_id(next_remainder)
                stack.append(("ImportWildCard", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ImportWildCard", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Global": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Global(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_sequence_var(next_remainder)
                stack.append(("Global", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("Global", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Nonlocal": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Nonlocal(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_sequence_var(next_remainder)
                stack.append(("Nonlocal", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("Nonlocal", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Expr": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Expr(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("Expr", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("Expr", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Pass": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Pass(),
                    next_remainder
                )
            
            else:
                stack.append(("Pass", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Break": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Break(),
                    next_remainder
                )
            
            else:
                stack.append(("Break", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Continue": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Continue(),
                    next_remainder
                )
            
            else:
                stack.append(("Continue", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], stmt)
    return result
    

def to_expr(xs : list[instance]) -> tuple[expr, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "expr"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "BoolOp": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 3

            index = len(next_children)
            if index == total_num_children:
                result = (
                    BoolOp(next_children[0], next_children[1], next_children[2]),
                    next_remainder
                )
            
            elif index == 1:
                (next_child, next_remainder) = to_boolop(next_remainder)
                stack.append(("BoolOp", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("BoolOp", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "NamedExpr": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    NamedExpr(next_children[0], next_children[1]),
                    next_remainder
                )
            
            else:
                stack.append(("NamedExpr", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "BinOp": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 3

            index = len(next_children)
            if index == total_num_children:
                result = (
                    BinOp(next_children[0], next_children[1], next_children[2]),
                    next_remainder
                )
            
            elif index == 1:
                (next_child, next_remainder) = to_operator(next_remainder)
                stack.append(("BinOp", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("BinOp", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "UnaryOp": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    UnaryOp(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_unaryop(next_remainder)
                stack.append(("UnaryOp", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("UnaryOp", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Lambda": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Lambda(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_parameters(next_remainder)
                stack.append(("Lambda", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("Lambda", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "IfExp": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 3

            index = len(next_children)
            if index == total_num_children:
                result = (
                    IfExp(next_children[0], next_children[1], next_children[2]),
                    next_remainder
                )
            
            else:
                stack.append(("IfExp", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Dictionary": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Dictionary(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_dictionary_contents(next_remainder)
                stack.append(("Dictionary", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("Dictionary", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "EmptyDictionary": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    EmptyDictionary(),
                    next_remainder
                )
            
            else:
                stack.append(("EmptyDictionary", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Set": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Set(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_comma_exprs(next_remainder)
                stack.append(("Set", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("Set", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "ListComp": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ListComp(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 1:
                (next_child, next_remainder) = to_comprehension_constraints(next_remainder)
                stack.append(("ListComp", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ListComp", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "SetComp": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    SetComp(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 1:
                (next_child, next_remainder) = to_comprehension_constraints(next_remainder)
                stack.append(("SetComp", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("SetComp", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "DictionaryComp": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 3

            index = len(next_children)
            if index == total_num_children:
                result = (
                    DictionaryComp(next_children[0], next_children[1], next_children[2]),
                    next_remainder
                )
            
            elif index == 2:
                (next_child, next_remainder) = to_comprehension_constraints(next_remainder)
                stack.append(("DictionaryComp", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("DictionaryComp", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "GeneratorExp": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    GeneratorExp(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 1:
                (next_child, next_remainder) = to_comprehension_constraints(next_remainder)
                stack.append(("GeneratorExp", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("GeneratorExp", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Await": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Await(next_children[0]),
                    next_remainder
                )
            
            else:
                stack.append(("Await", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "YieldNothing": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    YieldNothing(),
                    next_remainder
                )
            
            else:
                stack.append(("YieldNothing", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Yield": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Yield(next_children[0]),
                    next_remainder
                )
            
            else:
                stack.append(("Yield", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "YieldFrom": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    YieldFrom(next_children[0]),
                    next_remainder
                )
            
            else:
                stack.append(("YieldFrom", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Compare": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Compare(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 1:
                (next_child, next_remainder) = to_comparisons(next_remainder)
                stack.append(("Compare", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("Compare", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Call": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Call(next_children[0]),
                    next_remainder
                )
            
            else:
                stack.append(("Call", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "CallArgs": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    CallArgs(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 1:
                (next_child, next_remainder) = to_arguments(next_remainder)
                stack.append(("CallArgs", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("CallArgs", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Integer": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Integer(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_str(next_remainder)
                stack.append(("Integer", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("Integer", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Float": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Float(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_str(next_remainder)
                stack.append(("Float", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("Float", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "ConcatString": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    ConcatString(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_sequence_string(next_remainder)
                stack.append(("ConcatString", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("ConcatString", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "True_": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    True_(),
                    next_remainder
                )
            
            else:
                stack.append(("True_", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "False_": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    False_(),
                    next_remainder
                )
            
            else:
                stack.append(("False_", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "None_": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    None_(),
                    next_remainder
                )
            
            else:
                stack.append(("None_", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Ellip": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Ellip(),
                    next_remainder
                )
            
            else:
                stack.append(("Ellip", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Attribute": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Attribute(next_children[0], next_children[1]),
                    next_remainder
                )
            
            elif index == 1:
                (next_child, next_remainder) = to_str(next_remainder)
                stack.append(("Attribute", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("Attribute", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Subscript": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 2

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Subscript(next_children[0], next_children[1]),
                    next_remainder
                )
            
            else:
                stack.append(("Subscript", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Starred": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Starred(next_children[0]),
                    next_remainder
                )
            
            else:
                stack.append(("Starred", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Name": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Name(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_str(next_remainder)
                stack.append(("Name", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("Name", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "List": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    List(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_comma_exprs(next_remainder)
                stack.append(("List", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("List", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "EmptyList": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    EmptyList(),
                    next_remainder
                )
            
            else:
                stack.append(("EmptyList", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Tuple": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 1

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Tuple(next_children[0]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_comma_exprs(next_remainder)
                stack.append(("Tuple", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("Tuple", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "EmptyTuple": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    EmptyTuple(),
                    next_remainder
                )
            
            else:
                stack.append(("EmptyTuple", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Slice": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 3

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Slice(next_children[0], next_children[1], next_children[2]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_option_expr(next_remainder)
                stack.append(("Slice", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_option_expr(next_remainder)
                stack.append(("Slice", next_children + [next_child], next_remainder))
                

            elif index == 2:
                (next_child, next_remainder) = to_option_expr(next_remainder)
                stack.append(("Slice", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("Slice", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], expr)
    return result
    

def to_boolop(xs : list[instance]) -> tuple[boolop, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "boolop"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "And": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    And(),
                    next_remainder
                )
            
            else:
                stack.append(("And", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Or": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Or(),
                    next_remainder
                )
            
            else:
                stack.append(("Or", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], boolop)
    return result
    

def to_operator(xs : list[instance]) -> tuple[operator, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "operator"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "Add": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Add(),
                    next_remainder
                )
            
            else:
                stack.append(("Add", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Sub": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Sub(),
                    next_remainder
                )
            
            else:
                stack.append(("Sub", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Mult": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Mult(),
                    next_remainder
                )
            
            else:
                stack.append(("Mult", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "MatMult": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    MatMult(),
                    next_remainder
                )
            
            else:
                stack.append(("MatMult", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Div": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Div(),
                    next_remainder
                )
            
            else:
                stack.append(("Div", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Mod": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Mod(),
                    next_remainder
                )
            
            else:
                stack.append(("Mod", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Pow": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Pow(),
                    next_remainder
                )
            
            else:
                stack.append(("Pow", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "LShift": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    LShift(),
                    next_remainder
                )
            
            else:
                stack.append(("LShift", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "RShift": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    RShift(),
                    next_remainder
                )
            
            else:
                stack.append(("RShift", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "BitOr": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    BitOr(),
                    next_remainder
                )
            
            else:
                stack.append(("BitOr", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "BitXor": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    BitXor(),
                    next_remainder
                )
            
            else:
                stack.append(("BitXor", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "BitAnd": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    BitAnd(),
                    next_remainder
                )
            
            else:
                stack.append(("BitAnd", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "FloorDiv": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    FloorDiv(),
                    next_remainder
                )
            
            else:
                stack.append(("FloorDiv", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], operator)
    return result
    

def to_unaryop(xs : list[instance]) -> tuple[unaryop, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "unaryop"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "Invert": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Invert(),
                    next_remainder
                )
            
            else:
                stack.append(("Invert", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Not": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Not(),
                    next_remainder
                )
            
            else:
                stack.append(("Not", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "UAdd": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    UAdd(),
                    next_remainder
                )
            
            else:
                stack.append(("UAdd", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "USub": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    USub(),
                    next_remainder
                )
            
            else:
                stack.append(("USub", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], unaryop)
    return result
    

def to_cmpop(xs : list[instance]) -> tuple[cmpop, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "cmpop"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "Eq": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Eq(),
                    next_remainder
                )
            
            else:
                stack.append(("Eq", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "NotEq": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    NotEq(),
                    next_remainder
                )
            
            else:
                stack.append(("NotEq", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Lt": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Lt(),
                    next_remainder
                )
            
            else:
                stack.append(("Lt", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "LtE": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    LtE(),
                    next_remainder
                )
            
            else:
                stack.append(("LtE", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Gt": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Gt(),
                    next_remainder
                )
            
            else:
                stack.append(("Gt", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "GtE": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    GtE(),
                    next_remainder
                )
            
            else:
                stack.append(("GtE", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Is": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Is(),
                    next_remainder
                )
            
            else:
                stack.append(("Is", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "IsNot": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    IsNot(),
                    next_remainder
                )
            
            else:
                stack.append(("IsNot", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "In": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    In(),
                    next_remainder
                )
            
            else:
                stack.append(("In", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "NotIn": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 0

            index = len(next_children)
            if index == total_num_children:
                result = (
                    NotIn(),
                    next_remainder
                )
            
            else:
                stack.append(("NotIn", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], cmpop)
    return result
    

def to_constraint(xs : list[instance]) -> tuple[constraint, list[instance]]:

    x = xs[-1]
    assert isinstance(x, Grammar)
    assert x.options == "constraint"

    initial = (x.selection, [], xs[:-1])
    stack : list[tuple[str, list[Any], list[instance]]]= [initial]

    result = None 
    while stack:
        (rule_name, children, remainder) = stack.pop()

        if False:
            pass
        
        elif rule_name == "AsyncConstraint": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 3

            index = len(next_children)
            if index == total_num_children:
                result = (
                    AsyncConstraint(next_children[0], next_children[1], next_children[2]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("AsyncConstraint", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("AsyncConstraint", next_children + [next_child], next_remainder))
                

            elif index == 2:
                (next_child, next_remainder) = to_constraint_filters(next_remainder)
                stack.append(("AsyncConstraint", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("AsyncConstraint", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

        elif rule_name == "Constraint": 
            next_children = children
            next_remainder = remainder
            if result:
                (next_child, next_remainder) = result
                next_children = children + [next_child]
                result = None

            total_num_children = 3

            index = len(next_children)
            if index == total_num_children:
                result = (
                    Constraint(next_children[0], next_children[1], next_children[2]),
                    next_remainder
                )
            
            elif index == 0:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("Constraint", next_children + [next_child], next_remainder))
                

            elif index == 1:
                (next_child, next_remainder) = to_expr(next_remainder)
                stack.append(("Constraint", next_children + [next_child], next_remainder))
                

            elif index == 2:
                (next_child, next_remainder) = to_constraint_filters(next_remainder)
                stack.append(("Constraint", next_children + [next_child], next_remainder))
                
            else:
                stack.append(("Constraint", next_children, next_remainder))
                child_head = next_remainder[-1] 
                child_remainder = next_remainder[:-1]
                assert isinstance(child_head, Grammar)
                stack.append((child_head.selection, [], child_remainder))
        

    assert result
    assert isinstance(result[0], constraint)
    return result
     


def to_Module(xs : list[instance]) -> tuple[Module, list[instance]]:
    x_0 = xs[-1]
    xs_0 = xs[:-1]
    assert isinstance(x_0, Grammar)
    assert x_0.selection == "Module"

    (body, xs_1) = to_statements(xs_0)
    return (Module(body), xs_1)
    

def to_CompareRight(xs : list[instance]) -> tuple[CompareRight, list[instance]]:
    x_0 = xs[-1]
    xs_0 = xs[:-1]
    assert isinstance(x_0, Grammar)
    assert x_0.selection == "CompareRight"

    (op, xs_1) = to_cmpop(xs_0)
    (rand, xs_2) = to_expr(xs_1)
    return (CompareRight(op, rand), xs_2)
    

def to_ExceptHandler(xs : list[instance]) -> tuple[ExceptHandler, list[instance]]:
    x_0 = xs[-1]
    xs_0 = xs[:-1]
    assert isinstance(x_0, Grammar)
    assert x_0.selection == "ExceptHandler"

    (arg, xs_1) = to_except_arg(xs_0)
    (body, xs_2) = to_statements(xs_1)
    return (ExceptHandler(arg, body), xs_2)
    

def to_Param(xs : list[instance]) -> tuple[Param, list[instance]]:
    x_0 = xs[-1]
    xs_0 = xs[:-1]
    assert isinstance(x_0, Grammar)
    assert x_0.selection == "Param"

    (name, xs_1) = to_str(xs_0)
    (type, xs_2) = to_param_type(xs_1)
    (default, xs_3) = to_param_default(xs_2)
    return (Param(name, type, default), xs_3)
    

def to_ImportName(xs : list[instance]) -> tuple[ImportName, list[instance]]:
    x_0 = xs[-1]
    xs_0 = xs[:-1]
    assert isinstance(x_0, Grammar)
    assert x_0.selection == "ImportName"

    (name, xs_1) = to_str(xs_0)
    (as_name, xs_2) = to_alias(xs_1)
    return (ImportName(name, as_name), xs_2)
    

def to_Withitem(xs : list[instance]) -> tuple[Withitem, list[instance]]:
    x_0 = xs[-1]
    xs_0 = xs[:-1]
    assert isinstance(x_0, Grammar)
    assert x_0.selection == "Withitem"

    (contet, xs_1) = to_expr(xs_0)
    (target, xs_2) = to_alias_expr(xs_1)
    return (Withitem(contet, target), xs_2)
    

def to_ClassDef(xs : list[instance]) -> tuple[ClassDef, list[instance]]:
    x_0 = xs[-1]
    xs_0 = xs[:-1]
    assert isinstance(x_0, Grammar)
    assert x_0.selection == "ClassDef"

    (name, xs_1) = to_str(xs_0)
    (bs, xs_2) = to_bases(xs_1)
    (body, xs_3) = to_statements(xs_2)
    return (ClassDef(name, bs, body), xs_3)
    

def to_ElifBlock(xs : list[instance]) -> tuple[ElifBlock, list[instance]]:
    x_0 = xs[-1]
    xs_0 = xs[:-1]
    assert isinstance(x_0, Grammar)
    assert x_0.selection == "ElifBlock"

    (test, xs_1) = to_expr(xs_0)
    (body, xs_2) = to_statements(xs_1)
    return (ElifBlock(test, body), xs_2)
    

def to_ElseBlock(xs : list[instance]) -> tuple[ElseBlock, list[instance]]:
    x_0 = xs[-1]
    xs_0 = xs[:-1]
    assert isinstance(x_0, Grammar)
    assert x_0.selection == "ElseBlock"

    (body, xs_1) = to_statements(xs_0)
    return (ElseBlock(body), xs_1)
    

def to_FinallyBlock(xs : list[instance]) -> tuple[FinallyBlock, list[instance]]:
    x_0 = xs[-1]
    xs_0 = xs[:-1]
    assert isinstance(x_0, Grammar)
    assert x_0.selection == "FinallyBlock"

    (body, xs_1) = to_statements(xs_0)
    return (FinallyBlock(body), xs_1)
     


def to_str(xs : list[instance]) -> tuple[str, list[instance]]:
    hd = xs[-1]
    tl = xs[:-1]
    assert isinstance(hd, Vocab)
    return (hd.selection, tl)
    