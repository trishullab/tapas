

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, TypeVar, Any, Generic, Union, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod

T = TypeVar('T')



# type and constructor Module
@dataclass
class Module:
    body : list[stmt]



# type stmt
@dataclass
class stmt(ABC):
    @abstractmethod
    def _match(self, handlers : StmtHandlers[T]) -> T: pass


# constructors for type stmt
@dataclass
class FunctionDef(stmt):
    name : Identifier
    param_group : ParamGroup
    body : list[stmt]
    decorator_list : list[expr]
    returns : Optional[expr]

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_FunctionDef(self)

@dataclass
class AsyncFunctionDef(stmt):
    name : Identifier
    param_group : ParamGroup
    body : list[stmt]
    decorator_list : list[expr]
    returns : Optional[expr]

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_AsyncFunctionDef(self)

@dataclass
class ClassDef(stmt):
    name : Identifier
    bases : list[expr]
    keywords : list[Keyword]
    body : list[stmt]
    decorator_list : list[expr]

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_ClassDef(self)

@dataclass
class Return(stmt):
    value : Optional[expr]

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_Return(self)

@dataclass
class Delete(stmt):
    targets : list[expr]

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_Delete(self)

@dataclass
class Assign(stmt):
    targets : list[expr]
    value : expr

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_Assign(self)

@dataclass
class AugAssign(stmt):
    target : expr
    op : operator
    value : expr

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_AugAssign(self)

@dataclass
class AnnAssign(stmt):
    target : expr
    annotation : expr
    value : Optional[expr]

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_AnnAssign(self)

@dataclass
class AnnAssignSimple(stmt):
    target : expr
    annotation : expr
    value : Optional[expr]

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_AnnAssignSimple(self)

@dataclass
class For(stmt):
    target : expr
    iter : expr
    body : list[stmt]
    orelse : list[stmt]

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_For(self)

@dataclass
class AsyncFor(stmt):
    target : expr
    iter : expr
    body : list[stmt]
    orelse : list[stmt]

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_AsyncFor(self)

@dataclass
class While(stmt):
    test : expr
    body : list[stmt]
    orelse : list[stmt]

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_While(self)

@dataclass
class If(stmt):
    test : expr
    body : list[stmt]
    orelse : list[stmt]

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_If(self)

@dataclass
class With(stmt):
    items : list[Withitem]
    body : list[stmt]

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_With(self)

@dataclass
class AsyncWith(stmt):
    items : list[Withitem]
    body : list[stmt]

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_AsyncWith(self)

@dataclass
class Raise(stmt):
    exc : Optional[expr]
    cause : Optional[expr]

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_Raise(self)

@dataclass
class Try(stmt):
    body : list[stmt]
    handlers : list[ExceptHandler]
    orelse : list[stmt]
    finalbody : list[stmt]

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_Try(self)

@dataclass
class Assert(stmt):
    test : expr
    msg : Optional[expr]

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_Assert(self)

@dataclass
class Import(stmt):
    names : list[Alias]

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_Import(self)

@dataclass
class ImportFrom(stmt):
    module : Optional[Identifier]
    names : list[Alias]
    level : Optional[int]

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_ImportFrom(self)

@dataclass
class Global(stmt):
    names : list[Identifier]

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_Global(self)

@dataclass
class Nonlocal(stmt):
    names : list[Identifier]

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_Nonlocal(self)

@dataclass
class Expr(stmt):
    value : expr

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_Expr(self)

@dataclass
class Pass(stmt):

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_Pass(self)

@dataclass
class Break(stmt):

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_Break(self)

@dataclass
class Continue(stmt):

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_Continue(self)


# case handlers for type stmt
@dataclass
class StmtHandlers(Generic[T]):
    case_FunctionDef : Callable[[FunctionDef], T]
    case_AsyncFunctionDef : Callable[[AsyncFunctionDef], T]
    case_ClassDef : Callable[[ClassDef], T]
    case_Return : Callable[[Return], T]
    case_Delete : Callable[[Delete], T]
    case_Assign : Callable[[Assign], T]
    case_AugAssign : Callable[[AugAssign], T]
    case_AnnAssign : Callable[[AnnAssign], T]
    case_AnnAssignSimple : Callable[[AnnAssignSimple], T]
    case_For : Callable[[For], T]
    case_AsyncFor : Callable[[AsyncFor], T]
    case_While : Callable[[While], T]
    case_If : Callable[[If], T]
    case_With : Callable[[With], T]
    case_AsyncWith : Callable[[AsyncWith], T]
    case_Raise : Callable[[Raise], T]
    case_Try : Callable[[Try], T]
    case_Assert : Callable[[Assert], T]
    case_Import : Callable[[Import], T]
    case_ImportFrom : Callable[[ImportFrom], T]
    case_Global : Callable[[Global], T]
    case_Nonlocal : Callable[[Nonlocal], T]
    case_Expr : Callable[[Expr], T]
    case_Pass : Callable[[Pass], T]
    case_Break : Callable[[Break], T]
    case_Continue : Callable[[Continue], T]


# matching for type stmt
def match_stmt(o : stmt, handlers : StmtHandlers[T]) -> T :
    return o._match(handlers)


# type expr
@dataclass
class expr(ABC):
    @abstractmethod
    def _match(self, handlers : ExprHandlers[T]) -> T: pass


# constructors for type expr
@dataclass
class BoolOp(expr):
    left : expr
    op : boolop
    right : expr

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_BoolOp(self)

@dataclass
class NamedExpr(expr):
    target : expr
    value : expr

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_NamedExpr(self)

@dataclass
class BinOp(expr):
    left : expr
    op : operator
    right : expr

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_BinOp(self)

@dataclass
class UnaryOp(expr):
    op : unaryop
    operand : expr

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_UnaryOp(self)

@dataclass
class Lambda(expr):
    param_group : ParamGroup
    body : expr

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Lambda(self)

@dataclass
class IfExp(expr):
    test : expr
    body : expr
    orelse : expr

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_IfExp(self)

@dataclass
class Dict(expr):
    entries : list[Entry]

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Dict(self)

@dataclass
class Set(expr):
    elts : list[expr]

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Set(self)

@dataclass
class ListComp(expr):
    elt : expr
    constraints : list[constraint]

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_ListComp(self)

@dataclass
class SetComp(expr):
    elt : expr
    constraints : list[constraint]

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_SetComp(self)

@dataclass
class DictComp(expr):
    key : expr
    value : expr
    constraints : list[constraint]

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_DictComp(self)

@dataclass
class GeneratorExp(expr):
    elt : expr
    constraints : list[constraint]

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_GeneratorExp(self)

@dataclass
class Await(expr):
    value : expr

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Await(self)

@dataclass
class Yield(expr):
    value : Optional[expr]

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Yield(self)

@dataclass
class YieldFrom(expr):
    value : expr

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_YieldFrom(self)

@dataclass
class Compare(expr):
    left : expr
    ops : list[cmpop]
    comparators : list[expr]

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Compare(self)

@dataclass
class Call(expr):
    func : expr
    args : list[expr]
    keywords : list[Keyword]

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Call(self)

@dataclass
class Integer(expr):
    value : str

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Integer(self)

@dataclass
class Float(expr):
    value : str

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Float(self)

@dataclass
class String(expr):
    value : str

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_String(self)

@dataclass
class True_(expr):

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_True_(self)

@dataclass
class False_(expr):

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_False_(self)

@dataclass
class None_(expr):

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_None_(self)

@dataclass
class Ellip(expr):

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Ellip(self)

@dataclass
class ConcatString(expr):
    values : list[str]

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_ConcatString(self)

@dataclass
class Attribute(expr):
    value : expr
    attr : Identifier

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Attribute(self)

@dataclass
class Subscript(expr):
    value : expr
    slice : expr

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Subscript(self)

@dataclass
class Starred(expr):
    value : expr

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Starred(self)

@dataclass
class Name(expr):
    id : Identifier

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Name(self)

@dataclass
class List(expr):
    elts : list[expr]

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_List(self)

@dataclass
class Tuple(expr):
    elts : list[expr]

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Tuple(self)

@dataclass
class Slice(expr):
    lower : Optional[expr]
    upper : Optional[expr]
    step : Optional[expr]

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Slice(self)


# case handlers for type expr
@dataclass
class ExprHandlers(Generic[T]):
    case_BoolOp : Callable[[BoolOp], T]
    case_NamedExpr : Callable[[NamedExpr], T]
    case_BinOp : Callable[[BinOp], T]
    case_UnaryOp : Callable[[UnaryOp], T]
    case_Lambda : Callable[[Lambda], T]
    case_IfExp : Callable[[IfExp], T]
    case_Dict : Callable[[Dict], T]
    case_Set : Callable[[Set], T]
    case_ListComp : Callable[[ListComp], T]
    case_SetComp : Callable[[SetComp], T]
    case_DictComp : Callable[[DictComp], T]
    case_GeneratorExp : Callable[[GeneratorExp], T]
    case_Await : Callable[[Await], T]
    case_Yield : Callable[[Yield], T]
    case_YieldFrom : Callable[[YieldFrom], T]
    case_Compare : Callable[[Compare], T]
    case_Call : Callable[[Call], T]
    case_Integer : Callable[[Integer], T]
    case_Float : Callable[[Float], T]
    case_String : Callable[[String], T]
    case_True_ : Callable[[True_], T]
    case_False_ : Callable[[False_], T]
    case_None_ : Callable[[None_], T]
    case_Ellip : Callable[[Ellip], T]
    case_ConcatString : Callable[[ConcatString], T]
    case_Attribute : Callable[[Attribute], T]
    case_Subscript : Callable[[Subscript], T]
    case_Starred : Callable[[Starred], T]
    case_Name : Callable[[Name], T]
    case_List : Callable[[List], T]
    case_Tuple : Callable[[Tuple], T]
    case_Slice : Callable[[Slice], T]


# matching for type expr
def match_expr(o : expr, handlers : ExprHandlers[T]) -> T :
    return o._match(handlers)


# type boolop
@dataclass
class boolop(ABC):
    @abstractmethod
    def _match(self, handlers : BoolopHandlers[T]) -> T: pass


# constructors for type boolop
@dataclass
class And(boolop):

    def _match(self, handlers : BoolopHandlers[T]) -> T:
        return handlers.case_And(self)

@dataclass
class Or(boolop):

    def _match(self, handlers : BoolopHandlers[T]) -> T:
        return handlers.case_Or(self)


# case handlers for type boolop
@dataclass
class BoolopHandlers(Generic[T]):
    case_And : Callable[[And], T]
    case_Or : Callable[[Or], T]


# matching for type boolop
def match_boolop(o : boolop, handlers : BoolopHandlers[T]) -> T :
    return o._match(handlers)


# type operator
@dataclass
class operator(ABC):
    @abstractmethod
    def _match(self, handlers : OperatorHandlers[T]) -> T: pass


# constructors for type operator
@dataclass
class Add(operator):

    def _match(self, handlers : OperatorHandlers[T]) -> T:
        return handlers.case_Add(self)

@dataclass
class Sub(operator):

    def _match(self, handlers : OperatorHandlers[T]) -> T:
        return handlers.case_Sub(self)

@dataclass
class Mult(operator):

    def _match(self, handlers : OperatorHandlers[T]) -> T:
        return handlers.case_Mult(self)

@dataclass
class MatMult(operator):

    def _match(self, handlers : OperatorHandlers[T]) -> T:
        return handlers.case_MatMult(self)

@dataclass
class Div(operator):

    def _match(self, handlers : OperatorHandlers[T]) -> T:
        return handlers.case_Div(self)

@dataclass
class Mod(operator):

    def _match(self, handlers : OperatorHandlers[T]) -> T:
        return handlers.case_Mod(self)

@dataclass
class Pow(operator):

    def _match(self, handlers : OperatorHandlers[T]) -> T:
        return handlers.case_Pow(self)

@dataclass
class LShift(operator):

    def _match(self, handlers : OperatorHandlers[T]) -> T:
        return handlers.case_LShift(self)

@dataclass
class RShift(operator):

    def _match(self, handlers : OperatorHandlers[T]) -> T:
        return handlers.case_RShift(self)

@dataclass
class BitOr(operator):

    def _match(self, handlers : OperatorHandlers[T]) -> T:
        return handlers.case_BitOr(self)

@dataclass
class BitXor(operator):

    def _match(self, handlers : OperatorHandlers[T]) -> T:
        return handlers.case_BitXor(self)

@dataclass
class BitAnd(operator):

    def _match(self, handlers : OperatorHandlers[T]) -> T:
        return handlers.case_BitAnd(self)

@dataclass
class FloorDiv(operator):

    def _match(self, handlers : OperatorHandlers[T]) -> T:
        return handlers.case_FloorDiv(self)


# case handlers for type operator
@dataclass
class OperatorHandlers(Generic[T]):
    case_Add : Callable[[Add], T]
    case_Sub : Callable[[Sub], T]
    case_Mult : Callable[[Mult], T]
    case_MatMult : Callable[[MatMult], T]
    case_Div : Callable[[Div], T]
    case_Mod : Callable[[Mod], T]
    case_Pow : Callable[[Pow], T]
    case_LShift : Callable[[LShift], T]
    case_RShift : Callable[[RShift], T]
    case_BitOr : Callable[[BitOr], T]
    case_BitXor : Callable[[BitXor], T]
    case_BitAnd : Callable[[BitAnd], T]
    case_FloorDiv : Callable[[FloorDiv], T]


# matching for type operator
def match_operator(o : operator, handlers : OperatorHandlers[T]) -> T :
    return o._match(handlers)


# type unaryop
@dataclass
class unaryop(ABC):
    @abstractmethod
    def _match(self, handlers : UnaryopHandlers[T]) -> T: pass


# constructors for type unaryop
@dataclass
class Invert(unaryop):

    def _match(self, handlers : UnaryopHandlers[T]) -> T:
        return handlers.case_Invert(self)

@dataclass
class Not(unaryop):

    def _match(self, handlers : UnaryopHandlers[T]) -> T:
        return handlers.case_Not(self)

@dataclass
class UAdd(unaryop):

    def _match(self, handlers : UnaryopHandlers[T]) -> T:
        return handlers.case_UAdd(self)

@dataclass
class USub(unaryop):

    def _match(self, handlers : UnaryopHandlers[T]) -> T:
        return handlers.case_USub(self)


# case handlers for type unaryop
@dataclass
class UnaryopHandlers(Generic[T]):
    case_Invert : Callable[[Invert], T]
    case_Not : Callable[[Not], T]
    case_UAdd : Callable[[UAdd], T]
    case_USub : Callable[[USub], T]


# matching for type unaryop
def match_unaryop(o : unaryop, handlers : UnaryopHandlers[T]) -> T :
    return o._match(handlers)


# type cmpop
@dataclass
class cmpop(ABC):
    @abstractmethod
    def _match(self, handlers : CmpopHandlers[T]) -> T: pass


# constructors for type cmpop
@dataclass
class Eq(cmpop):

    def _match(self, handlers : CmpopHandlers[T]) -> T:
        return handlers.case_Eq(self)

@dataclass
class NotEq(cmpop):

    def _match(self, handlers : CmpopHandlers[T]) -> T:
        return handlers.case_NotEq(self)

@dataclass
class Lt(cmpop):

    def _match(self, handlers : CmpopHandlers[T]) -> T:
        return handlers.case_Lt(self)

@dataclass
class LtE(cmpop):

    def _match(self, handlers : CmpopHandlers[T]) -> T:
        return handlers.case_LtE(self)

@dataclass
class Gt(cmpop):

    def _match(self, handlers : CmpopHandlers[T]) -> T:
        return handlers.case_Gt(self)

@dataclass
class GtE(cmpop):

    def _match(self, handlers : CmpopHandlers[T]) -> T:
        return handlers.case_GtE(self)

@dataclass
class Is(cmpop):

    def _match(self, handlers : CmpopHandlers[T]) -> T:
        return handlers.case_Is(self)

@dataclass
class IsNot(cmpop):

    def _match(self, handlers : CmpopHandlers[T]) -> T:
        return handlers.case_IsNot(self)

@dataclass
class In(cmpop):

    def _match(self, handlers : CmpopHandlers[T]) -> T:
        return handlers.case_In(self)

@dataclass
class NotIn(cmpop):

    def _match(self, handlers : CmpopHandlers[T]) -> T:
        return handlers.case_NotIn(self)


# case handlers for type cmpop
@dataclass
class CmpopHandlers(Generic[T]):
    case_Eq : Callable[[Eq], T]
    case_NotEq : Callable[[NotEq], T]
    case_Lt : Callable[[Lt], T]
    case_LtE : Callable[[LtE], T]
    case_Gt : Callable[[Gt], T]
    case_GtE : Callable[[GtE], T]
    case_Is : Callable[[Is], T]
    case_IsNot : Callable[[IsNot], T]
    case_In : Callable[[In], T]
    case_NotIn : Callable[[NotIn], T]


# matching for type cmpop
def match_cmpop(o : cmpop, handlers : CmpopHandlers[T]) -> T :
    return o._match(handlers)


# type constraint
@dataclass
class constraint(ABC):
    @abstractmethod
    def _match(self, handlers : ConstraintHandlers[T]) -> T: pass


# constructors for type constraint
@dataclass
class AsyncConstraint(constraint):
    target : expr
    iter : expr
    ifs : list[expr]

    def _match(self, handlers : ConstraintHandlers[T]) -> T:
        return handlers.case_AsyncConstraint(self)

@dataclass
class Constraint(constraint):
    target : expr
    iter : expr
    ifs : list[expr]

    def _match(self, handlers : ConstraintHandlers[T]) -> T:
        return handlers.case_Constraint(self)


# case handlers for type constraint
@dataclass
class ConstraintHandlers(Generic[T]):
    case_AsyncConstraint : Callable[[AsyncConstraint], T]
    case_Constraint : Callable[[Constraint], T]


# matching for type constraint
def match_constraint(o : constraint, handlers : ConstraintHandlers[T]) -> T :
    return o._match(handlers)


# type and constructor ExceptHandler
@dataclass
class ExceptHandler:
    type : Optional[expr]
    name : Optional[Identifier]
    body : list[stmt]



# type and constructor ParamGroup
@dataclass
class ParamGroup:
    pos_params : list[Param]
    params : list[Param]
    list_splat : Optional[Param]
    kw_params : list[Param]
    dictionary_splat : Optional[Param]



# type and constructor Param
@dataclass
class Param:
    id : Identifier
    annotation : Optional[expr]
    default : Optional[expr]



# type and constructor Keyword
@dataclass
class Keyword:
    name : Optional[Identifier]
    value : expr



# type and constructor Entry
@dataclass
class Entry:
    key : expr
    value : expr



# type and constructor Alias
@dataclass
class Alias:
    name : Identifier
    asname : Optional[Identifier]



# type and constructor Withitem
@dataclass
class Withitem:
    context_expr : expr
    optional_vars : Optional[expr]



# type and constructor Identifier
@dataclass
class Identifier:
    symbol : str


