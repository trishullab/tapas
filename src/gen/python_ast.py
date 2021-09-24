
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, TypeVar, Any, Generic, Union, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod

T = TypeVar('T')



# type and constructor Module
@dataclass
class Module:
    body : statements
    


# type and constructor CompareRight
@dataclass
class CompareRight:
    op : cmpop
    rand : expr
    


# type and constructor ExceptHandler
@dataclass
class ExceptHandler:
    arg : except_arg
    body : statements
    


# type and constructor Param
@dataclass
class Param:
    id : Identifier
    type : param_type
    default : param_default
    


# type and constructor Field
@dataclass
class Field:
    key : expr
    content : expr
    


# type and constructor ImportName
@dataclass
class ImportName:
    name : Identifier
    as_name : alias
    


# type and constructor Identifier
@dataclass
class Identifier:
    symbol : str
    


# type and constructor Withitem
@dataclass
class Withitem:
    contet : expr
    target : alias_expr
    


# type and constructor ClassDef
@dataclass
class ClassDef:
    name : Identifier
    bs : bases
    body : statements
    


# type return_type
@dataclass
class return_type(ABC):
    @abstractmethod
    def _match(self, handlers : ReturnTypeHandlers[T]) -> T: pass


# constructors for type return_type

@dataclass
class SomeReturnType(return_type):
    content : expr

    def _match(self, handlers : ReturnTypeHandlers[T]) -> T:
        return handlers.case_SomeReturnType(self)


def make_SomeReturnType(
    content : expr
) -> return_type:
    return SomeReturnType(
        content
    )


@dataclass
class NoReturnType(return_type):

    def _match(self, handlers : ReturnTypeHandlers[T]) -> T:
        return handlers.case_NoReturnType(self)


def make_NoReturnType(
) -> return_type:
    return NoReturnType(
    )


# case handlers for type return_type
@dataclass
class ReturnTypeHandlers(Generic[T]):
    case_SomeReturnType : Callable[[SomeReturnType], T]
    case_NoReturnType : Callable[[NoReturnType], T]


# matching for type return_type
def match_return_type(o : return_type, handlers : ReturnTypeHandlers[T]) -> T :
    return o._match(handlers)


# type module_id
@dataclass
class module_id(ABC):
    @abstractmethod
    def _match(self, handlers : ModuleIdHandlers[T]) -> T: pass


# constructors for type module_id

@dataclass
class SomeModuleId(module_id):
    content : Identifier

    def _match(self, handlers : ModuleIdHandlers[T]) -> T:
        return handlers.case_SomeModuleId(self)


def make_SomeModuleId(
    content : Identifier
) -> module_id:
    return SomeModuleId(
        content
    )


@dataclass
class NoModuleId(module_id):

    def _match(self, handlers : ModuleIdHandlers[T]) -> T:
        return handlers.case_NoModuleId(self)


def make_NoModuleId(
) -> module_id:
    return NoModuleId(
    )


# case handlers for type module_id
@dataclass
class ModuleIdHandlers(Generic[T]):
    case_SomeModuleId : Callable[[SomeModuleId], T]
    case_NoModuleId : Callable[[NoModuleId], T]


# matching for type module_id
def match_module_id(o : module_id, handlers : ModuleIdHandlers[T]) -> T :
    return o._match(handlers)


# type except_arg
@dataclass
class except_arg(ABC):
    @abstractmethod
    def _match(self, handlers : ExceptArgHandlers[T]) -> T: pass


# constructors for type except_arg

@dataclass
class SomeExceptArg(except_arg):
    content : expr

    def _match(self, handlers : ExceptArgHandlers[T]) -> T:
        return handlers.case_SomeExceptArg(self)


def make_SomeExceptArg(
    content : expr
) -> except_arg:
    return SomeExceptArg(
        content
    )


@dataclass
class SomeExceptArgName(except_arg):
    content : expr
    name : Identifier

    def _match(self, handlers : ExceptArgHandlers[T]) -> T:
        return handlers.case_SomeExceptArgName(self)


def make_SomeExceptArgName(
    content : expr,
    name : Identifier
) -> except_arg:
    return SomeExceptArgName(
        content,
        name
    )


@dataclass
class NoExceptArg(except_arg):

    def _match(self, handlers : ExceptArgHandlers[T]) -> T:
        return handlers.case_NoExceptArg(self)


def make_NoExceptArg(
) -> except_arg:
    return NoExceptArg(
    )


# case handlers for type except_arg
@dataclass
class ExceptArgHandlers(Generic[T]):
    case_SomeExceptArg : Callable[[SomeExceptArg], T]
    case_SomeExceptArgName : Callable[[SomeExceptArgName], T]
    case_NoExceptArg : Callable[[NoExceptArg], T]


# matching for type except_arg
def match_except_arg(o : except_arg, handlers : ExceptArgHandlers[T]) -> T :
    return o._match(handlers)


# type param_type
@dataclass
class param_type(ABC):
    @abstractmethod
    def _match(self, handlers : ParamTypeHandlers[T]) -> T: pass


# constructors for type param_type

@dataclass
class SomeParamType(param_type):
    content : expr

    def _match(self, handlers : ParamTypeHandlers[T]) -> T:
        return handlers.case_SomeParamType(self)


def make_SomeParamType(
    content : expr
) -> param_type:
    return SomeParamType(
        content
    )


@dataclass
class NoParamType(param_type):

    def _match(self, handlers : ParamTypeHandlers[T]) -> T:
        return handlers.case_NoParamType(self)


def make_NoParamType(
) -> param_type:
    return NoParamType(
    )


# case handlers for type param_type
@dataclass
class ParamTypeHandlers(Generic[T]):
    case_SomeParamType : Callable[[SomeParamType], T]
    case_NoParamType : Callable[[NoParamType], T]


# matching for type param_type
def match_param_type(o : param_type, handlers : ParamTypeHandlers[T]) -> T :
    return o._match(handlers)


# type param_default
@dataclass
class param_default(ABC):
    @abstractmethod
    def _match(self, handlers : ParamDefaultHandlers[T]) -> T: pass


# constructors for type param_default

@dataclass
class SomeParamDefault(param_default):
    content : expr

    def _match(self, handlers : ParamDefaultHandlers[T]) -> T:
        return handlers.case_SomeParamDefault(self)


def make_SomeParamDefault(
    content : expr
) -> param_default:
    return SomeParamDefault(
        content
    )


@dataclass
class NoParamDefault(param_default):

    def _match(self, handlers : ParamDefaultHandlers[T]) -> T:
        return handlers.case_NoParamDefault(self)


def make_NoParamDefault(
) -> param_default:
    return NoParamDefault(
    )


# case handlers for type param_default
@dataclass
class ParamDefaultHandlers(Generic[T]):
    case_SomeParamDefault : Callable[[SomeParamDefault], T]
    case_NoParamDefault : Callable[[NoParamDefault], T]


# matching for type param_default
def match_param_default(o : param_default, handlers : ParamDefaultHandlers[T]) -> T :
    return o._match(handlers)


# type parameters_d
@dataclass
class parameters_d(ABC):
    @abstractmethod
    def _match(self, handlers : ParametersDHandlers[T]) -> T: pass


# constructors for type parameters_d

@dataclass
class ConsKwParam(parameters_d):
    head : Param
    tail : parameters_d

    def _match(self, handlers : ParametersDHandlers[T]) -> T:
        return handlers.case_ConsKwParam(self)


def make_ConsKwParam(
    head : Param,
    tail : parameters_d
) -> parameters_d:
    return ConsKwParam(
        head,
        tail
    )


@dataclass
class SingleKwParam(parameters_d):
    content : Param

    def _match(self, handlers : ParametersDHandlers[T]) -> T:
        return handlers.case_SingleKwParam(self)


def make_SingleKwParam(
    content : Param
) -> parameters_d:
    return SingleKwParam(
        content
    )


@dataclass
class DictionarySplatParam(parameters_d):
    content : Param

    def _match(self, handlers : ParametersDHandlers[T]) -> T:
        return handlers.case_DictionarySplatParam(self)


def make_DictionarySplatParam(
    content : Param
) -> parameters_d:
    return DictionarySplatParam(
        content
    )


# case handlers for type parameters_d
@dataclass
class ParametersDHandlers(Generic[T]):
    case_ConsKwParam : Callable[[ConsKwParam], T]
    case_SingleKwParam : Callable[[SingleKwParam], T]
    case_DictionarySplatParam : Callable[[DictionarySplatParam], T]


# matching for type parameters_d
def match_parameters_d(o : parameters_d, handlers : ParametersDHandlers[T]) -> T :
    return o._match(handlers)


# type parameters_c
@dataclass
class parameters_c(ABC):
    @abstractmethod
    def _match(self, handlers : ParametersCHandlers[T]) -> T: pass


# constructors for type parameters_c

@dataclass
class SingleListSplatParam(parameters_c):
    content : Param

    def _match(self, handlers : ParametersCHandlers[T]) -> T:
        return handlers.case_SingleListSplatParam(self)


def make_SingleListSplatParam(
    content : Param
) -> parameters_c:
    return SingleListSplatParam(
        content
    )


@dataclass
class TransListSplatParam(parameters_c):
    head : Param
    tail : parameters_d

    def _match(self, handlers : ParametersCHandlers[T]) -> T:
        return handlers.case_TransListSplatParam(self)


def make_TransListSplatParam(
    head : Param,
    tail : parameters_d
) -> parameters_c:
    return TransListSplatParam(
        head,
        tail
    )


@dataclass
class ParamsD(parameters_c):
    content : parameters_d

    def _match(self, handlers : ParametersCHandlers[T]) -> T:
        return handlers.case_ParamsD(self)


def make_ParamsD(
    content : parameters_d
) -> parameters_c:
    return ParamsD(
        content
    )


# case handlers for type parameters_c
@dataclass
class ParametersCHandlers(Generic[T]):
    case_SingleListSplatParam : Callable[[SingleListSplatParam], T]
    case_TransListSplatParam : Callable[[TransListSplatParam], T]
    case_ParamsD : Callable[[ParamsD], T]


# matching for type parameters_c
def match_parameters_c(o : parameters_c, handlers : ParametersCHandlers[T]) -> T :
    return o._match(handlers)


# type parameters_b
@dataclass
class parameters_b(ABC):
    @abstractmethod
    def _match(self, handlers : ParametersBHandlers[T]) -> T: pass


# constructors for type parameters_b

@dataclass
class ConsParam(parameters_b):
    head : Param
    tail : parameters_b

    def _match(self, handlers : ParametersBHandlers[T]) -> T:
        return handlers.case_ConsParam(self)


def make_ConsParam(
    head : Param,
    tail : parameters_b
) -> parameters_b:
    return ConsParam(
        head,
        tail
    )


@dataclass
class SingleParam(parameters_b):
    content : Param

    def _match(self, handlers : ParametersBHandlers[T]) -> T:
        return handlers.case_SingleParam(self)


def make_SingleParam(
    content : Param
) -> parameters_b:
    return SingleParam(
        content
    )


@dataclass
class ParamsC(parameters_b):
    content : parameters_c

    def _match(self, handlers : ParametersBHandlers[T]) -> T:
        return handlers.case_ParamsC(self)


def make_ParamsC(
    content : parameters_c
) -> parameters_b:
    return ParamsC(
        content
    )


# case handlers for type parameters_b
@dataclass
class ParametersBHandlers(Generic[T]):
    case_ConsParam : Callable[[ConsParam], T]
    case_SingleParam : Callable[[SingleParam], T]
    case_ParamsC : Callable[[ParamsC], T]


# matching for type parameters_b
def match_parameters_b(o : parameters_b, handlers : ParametersBHandlers[T]) -> T :
    return o._match(handlers)


# type parameters
@dataclass
class parameters(ABC):
    @abstractmethod
    def _match(self, handlers : ParametersHandlers[T]) -> T: pass


# constructors for type parameters

@dataclass
class ParamsA(parameters):
    content : parameters_a

    def _match(self, handlers : ParametersHandlers[T]) -> T:
        return handlers.case_ParamsA(self)


def make_ParamsA(
    content : parameters_a
) -> parameters:
    return ParamsA(
        content
    )


@dataclass
class ParamsB(parameters):
    content : parameters_b

    def _match(self, handlers : ParametersHandlers[T]) -> T:
        return handlers.case_ParamsB(self)


def make_ParamsB(
    content : parameters_b
) -> parameters:
    return ParamsB(
        content
    )


@dataclass
class NoParam(parameters):

    def _match(self, handlers : ParametersHandlers[T]) -> T:
        return handlers.case_NoParam(self)


def make_NoParam(
) -> parameters:
    return NoParam(
    )


# case handlers for type parameters
@dataclass
class ParametersHandlers(Generic[T]):
    case_ParamsA : Callable[[ParamsA], T]
    case_ParamsB : Callable[[ParamsB], T]
    case_NoParam : Callable[[NoParam], T]


# matching for type parameters
def match_parameters(o : parameters, handlers : ParametersHandlers[T]) -> T :
    return o._match(handlers)


# type parameters_a
@dataclass
class parameters_a(ABC):
    @abstractmethod
    def _match(self, handlers : ParametersAHandlers[T]) -> T: pass


# constructors for type parameters_a

@dataclass
class ConsPosParam(parameters_a):
    head : Param
    tail : parameters_a

    def _match(self, handlers : ParametersAHandlers[T]) -> T:
        return handlers.case_ConsPosParam(self)


def make_ConsPosParam(
    head : Param,
    tail : parameters_a
) -> parameters_a:
    return ConsPosParam(
        head,
        tail
    )


@dataclass
class SinglePosParam(parameters_a):
    content : Param

    def _match(self, handlers : ParametersAHandlers[T]) -> T:
        return handlers.case_SinglePosParam(self)


def make_SinglePosParam(
    content : Param
) -> parameters_a:
    return SinglePosParam(
        content
    )


@dataclass
class TransPosParam(parameters_a):
    head : Param
    tail : parameters_b

    def _match(self, handlers : ParametersAHandlers[T]) -> T:
        return handlers.case_TransPosParam(self)


def make_TransPosParam(
    head : Param,
    tail : parameters_b
) -> parameters_a:
    return TransPosParam(
        head,
        tail
    )


# case handlers for type parameters_a
@dataclass
class ParametersAHandlers(Generic[T]):
    case_ConsPosParam : Callable[[ConsPosParam], T]
    case_SinglePosParam : Callable[[SinglePosParam], T]
    case_TransPosParam : Callable[[TransPosParam], T]


# matching for type parameters_a
def match_parameters_a(o : parameters_a, handlers : ParametersAHandlers[T]) -> T :
    return o._match(handlers)


# type keyword
@dataclass
class keyword(ABC):
    @abstractmethod
    def _match(self, handlers : KeywordHandlers[T]) -> T: pass


# constructors for type keyword

@dataclass
class NamedKeyword(keyword):
    name : Identifier
    content : expr

    def _match(self, handlers : KeywordHandlers[T]) -> T:
        return handlers.case_NamedKeyword(self)


def make_NamedKeyword(
    name : Identifier,
    content : expr
) -> keyword:
    return NamedKeyword(
        name,
        content
    )


@dataclass
class SplatKeyword(keyword):
    content : expr

    def _match(self, handlers : KeywordHandlers[T]) -> T:
        return handlers.case_SplatKeyword(self)


def make_SplatKeyword(
    content : expr
) -> keyword:
    return SplatKeyword(
        content
    )


# case handlers for type keyword
@dataclass
class KeywordHandlers(Generic[T]):
    case_NamedKeyword : Callable[[NamedKeyword], T]
    case_SplatKeyword : Callable[[SplatKeyword], T]


# matching for type keyword
def match_keyword(o : keyword, handlers : KeywordHandlers[T]) -> T :
    return o._match(handlers)


# type alias
@dataclass
class alias(ABC):
    @abstractmethod
    def _match(self, handlers : AliasHandlers[T]) -> T: pass


# constructors for type alias

@dataclass
class SomeAlias(alias):
    content : Identifier

    def _match(self, handlers : AliasHandlers[T]) -> T:
        return handlers.case_SomeAlias(self)


def make_SomeAlias(
    content : Identifier
) -> alias:
    return SomeAlias(
        content
    )


@dataclass
class NoAlias(alias):

    def _match(self, handlers : AliasHandlers[T]) -> T:
        return handlers.case_NoAlias(self)


def make_NoAlias(
) -> alias:
    return NoAlias(
    )


# case handlers for type alias
@dataclass
class AliasHandlers(Generic[T]):
    case_SomeAlias : Callable[[SomeAlias], T]
    case_NoAlias : Callable[[NoAlias], T]


# matching for type alias
def match_alias(o : alias, handlers : AliasHandlers[T]) -> T :
    return o._match(handlers)


# type alias_expr
@dataclass
class alias_expr(ABC):
    @abstractmethod
    def _match(self, handlers : AliasExprHandlers[T]) -> T: pass


# constructors for type alias_expr

@dataclass
class SomeAliasExpr(alias_expr):
    content : expr

    def _match(self, handlers : AliasExprHandlers[T]) -> T:
        return handlers.case_SomeAliasExpr(self)


def make_SomeAliasExpr(
    content : expr
) -> alias_expr:
    return SomeAliasExpr(
        content
    )


@dataclass
class NoAliasExpr(alias_expr):

    def _match(self, handlers : AliasExprHandlers[T]) -> T:
        return handlers.case_NoAliasExpr(self)


def make_NoAliasExpr(
) -> alias_expr:
    return NoAliasExpr(
    )


# case handlers for type alias_expr
@dataclass
class AliasExprHandlers(Generic[T]):
    case_SomeAliasExpr : Callable[[SomeAliasExpr], T]
    case_NoAliasExpr : Callable[[NoAliasExpr], T]


# matching for type alias_expr
def match_alias_expr(o : alias_expr, handlers : AliasExprHandlers[T]) -> T :
    return o._match(handlers)


# type bases
@dataclass
class bases(ABC):
    @abstractmethod
    def _match(self, handlers : BasesHandlers[T]) -> T: pass


# constructors for type bases

@dataclass
class SomeBases(bases):
    bases : bases_a

    def _match(self, handlers : BasesHandlers[T]) -> T:
        return handlers.case_SomeBases(self)


def make_SomeBases(
    bases : bases_a
) -> bases:
    return SomeBases(
        bases
    )


@dataclass
class NoBases(bases):

    def _match(self, handlers : BasesHandlers[T]) -> T:
        return handlers.case_NoBases(self)


def make_NoBases(
) -> bases:
    return NoBases(
    )


# case handlers for type bases
@dataclass
class BasesHandlers(Generic[T]):
    case_SomeBases : Callable[[SomeBases], T]
    case_NoBases : Callable[[NoBases], T]


# matching for type bases
def match_bases(o : bases, handlers : BasesHandlers[T]) -> T :
    return o._match(handlers)


# type bases_a
@dataclass
class bases_a(ABC):
    @abstractmethod
    def _match(self, handlers : BasesAHandlers[T]) -> T: pass


# constructors for type bases_a

@dataclass
class ConsBase(bases_a):
    head : expr
    tail : bases_a

    def _match(self, handlers : BasesAHandlers[T]) -> T:
        return handlers.case_ConsBase(self)


def make_ConsBase(
    head : expr,
    tail : bases_a
) -> bases_a:
    return ConsBase(
        head,
        tail
    )


@dataclass
class SingleBase(bases_a):
    content : expr

    def _match(self, handlers : BasesAHandlers[T]) -> T:
        return handlers.case_SingleBase(self)


def make_SingleBase(
    content : expr
) -> bases_a:
    return SingleBase(
        content
    )


@dataclass
class KeywordsBase(bases_a):
    kws : keywords

    def _match(self, handlers : BasesAHandlers[T]) -> T:
        return handlers.case_KeywordsBase(self)


def make_KeywordsBase(
    kws : keywords
) -> bases_a:
    return KeywordsBase(
        kws
    )


# case handlers for type bases_a
@dataclass
class BasesAHandlers(Generic[T]):
    case_ConsBase : Callable[[ConsBase], T]
    case_SingleBase : Callable[[SingleBase], T]
    case_KeywordsBase : Callable[[KeywordsBase], T]


# matching for type bases_a
def match_bases_a(o : bases_a, handlers : BasesAHandlers[T]) -> T :
    return o._match(handlers)


# type keywords
@dataclass
class keywords(ABC):
    @abstractmethod
    def _match(self, handlers : KeywordsHandlers[T]) -> T: pass


# constructors for type keywords

@dataclass
class ConsKeyword(keywords):
    head : keyword
    tail : keywords

    def _match(self, handlers : KeywordsHandlers[T]) -> T:
        return handlers.case_ConsKeyword(self)


def make_ConsKeyword(
    head : keyword,
    tail : keywords
) -> keywords:
    return ConsKeyword(
        head,
        tail
    )


@dataclass
class SingleKeyword(keywords):
    content : keyword

    def _match(self, handlers : KeywordsHandlers[T]) -> T:
        return handlers.case_SingleKeyword(self)


def make_SingleKeyword(
    content : keyword
) -> keywords:
    return SingleKeyword(
        content
    )


# case handlers for type keywords
@dataclass
class KeywordsHandlers(Generic[T]):
    case_ConsKeyword : Callable[[ConsKeyword], T]
    case_SingleKeyword : Callable[[SingleKeyword], T]


# matching for type keywords
def match_keywords(o : keywords, handlers : KeywordsHandlers[T]) -> T :
    return o._match(handlers)


# type comparisons
@dataclass
class comparisons(ABC):
    @abstractmethod
    def _match(self, handlers : ComparisonsHandlers[T]) -> T: pass


# constructors for type comparisons

@dataclass
class ConsCompareRight(comparisons):
    head : CompareRight
    tail : comparisons

    def _match(self, handlers : ComparisonsHandlers[T]) -> T:
        return handlers.case_ConsCompareRight(self)


def make_ConsCompareRight(
    head : CompareRight,
    tail : comparisons
) -> comparisons:
    return ConsCompareRight(
        head,
        tail
    )


@dataclass
class SingleCompareRight(comparisons):
    content : CompareRight

    def _match(self, handlers : ComparisonsHandlers[T]) -> T:
        return handlers.case_SingleCompareRight(self)


def make_SingleCompareRight(
    content : CompareRight
) -> comparisons:
    return SingleCompareRight(
        content
    )


# case handlers for type comparisons
@dataclass
class ComparisonsHandlers(Generic[T]):
    case_ConsCompareRight : Callable[[ConsCompareRight], T]
    case_SingleCompareRight : Callable[[SingleCompareRight], T]


# matching for type comparisons
def match_comparisons(o : comparisons, handlers : ComparisonsHandlers[T]) -> T :
    return o._match(handlers)


# type option_expr
@dataclass
class option_expr(ABC):
    @abstractmethod
    def _match(self, handlers : OptionExprHandlers[T]) -> T: pass


# constructors for type option_expr

@dataclass
class SomeExpr(option_expr):
    content : expr

    def _match(self, handlers : OptionExprHandlers[T]) -> T:
        return handlers.case_SomeExpr(self)


def make_SomeExpr(
    content : expr
) -> option_expr:
    return SomeExpr(
        content
    )


@dataclass
class NoExpr(option_expr):

    def _match(self, handlers : OptionExprHandlers[T]) -> T:
        return handlers.case_NoExpr(self)


def make_NoExpr(
) -> option_expr:
    return NoExpr(
    )


# case handlers for type option_expr
@dataclass
class OptionExprHandlers(Generic[T]):
    case_SomeExpr : Callable[[SomeExpr], T]
    case_NoExpr : Callable[[NoExpr], T]


# matching for type option_expr
def match_option_expr(o : option_expr, handlers : OptionExprHandlers[T]) -> T :
    return o._match(handlers)


# type comma_exprs
@dataclass
class comma_exprs(ABC):
    @abstractmethod
    def _match(self, handlers : CommaExprsHandlers[T]) -> T: pass


# constructors for type comma_exprs

@dataclass
class ConsExpr(comma_exprs):
    head : expr
    tail : comma_exprs

    def _match(self, handlers : CommaExprsHandlers[T]) -> T:
        return handlers.case_ConsExpr(self)


def make_ConsExpr(
    head : expr,
    tail : comma_exprs
) -> comma_exprs:
    return ConsExpr(
        head,
        tail
    )


@dataclass
class SingleExpr(comma_exprs):
    content : expr

    def _match(self, handlers : CommaExprsHandlers[T]) -> T:
        return handlers.case_SingleExpr(self)


def make_SingleExpr(
    content : expr
) -> comma_exprs:
    return SingleExpr(
        content
    )


# case handlers for type comma_exprs
@dataclass
class CommaExprsHandlers(Generic[T]):
    case_ConsExpr : Callable[[ConsExpr], T]
    case_SingleExpr : Callable[[SingleExpr], T]


# matching for type comma_exprs
def match_comma_exprs(o : comma_exprs, handlers : CommaExprsHandlers[T]) -> T :
    return o._match(handlers)


# type decorators
@dataclass
class decorators(ABC):
    @abstractmethod
    def _match(self, handlers : DecoratorsHandlers[T]) -> T: pass


# constructors for type decorators

@dataclass
class ConsDec(decorators):
    head : expr
    tail : decorators

    def _match(self, handlers : DecoratorsHandlers[T]) -> T:
        return handlers.case_ConsDec(self)


def make_ConsDec(
    head : expr,
    tail : decorators
) -> decorators:
    return ConsDec(
        head,
        tail
    )


@dataclass
class NoDec(decorators):

    def _match(self, handlers : DecoratorsHandlers[T]) -> T:
        return handlers.case_NoDec(self)


def make_NoDec(
) -> decorators:
    return NoDec(
    )


# case handlers for type decorators
@dataclass
class DecoratorsHandlers(Generic[T]):
    case_ConsDec : Callable[[ConsDec], T]
    case_NoDec : Callable[[NoDec], T]


# matching for type decorators
def match_decorators(o : decorators, handlers : DecoratorsHandlers[T]) -> T :
    return o._match(handlers)


# type constraint_filters
@dataclass
class constraint_filters(ABC):
    @abstractmethod
    def _match(self, handlers : ConstraintFiltersHandlers[T]) -> T: pass


# constructors for type constraint_filters

@dataclass
class ConsFilter(constraint_filters):
    head : expr
    tail : constraint_filters

    def _match(self, handlers : ConstraintFiltersHandlers[T]) -> T:
        return handlers.case_ConsFilter(self)


def make_ConsFilter(
    head : expr,
    tail : constraint_filters
) -> constraint_filters:
    return ConsFilter(
        head,
        tail
    )


@dataclass
class SingleFilter(constraint_filters):
    content : expr

    def _match(self, handlers : ConstraintFiltersHandlers[T]) -> T:
        return handlers.case_SingleFilter(self)


def make_SingleFilter(
    content : expr
) -> constraint_filters:
    return SingleFilter(
        content
    )


# case handlers for type constraint_filters
@dataclass
class ConstraintFiltersHandlers(Generic[T]):
    case_ConsFilter : Callable[[ConsFilter], T]
    case_SingleFilter : Callable[[SingleFilter], T]


# matching for type constraint_filters
def match_constraint_filters(o : constraint_filters, handlers : ConstraintFiltersHandlers[T]) -> T :
    return o._match(handlers)


# type sequence_str
@dataclass
class sequence_str(ABC):
    @abstractmethod
    def _match(self, handlers : SequenceStrHandlers[T]) -> T: pass


# constructors for type sequence_str

@dataclass
class ConsStr(sequence_str):
    head : str
    tail : sequence_str

    def _match(self, handlers : SequenceStrHandlers[T]) -> T:
        return handlers.case_ConsStr(self)


def make_ConsStr(
    head : str,
    tail : sequence_str
) -> sequence_str:
    return ConsStr(
        head,
        tail
    )


@dataclass
class SingleStr(sequence_str):
    content : str

    def _match(self, handlers : SequenceStrHandlers[T]) -> T:
        return handlers.case_SingleStr(self)


def make_SingleStr(
    content : str
) -> sequence_str:
    return SingleStr(
        content
    )


# case handlers for type sequence_str
@dataclass
class SequenceStrHandlers(Generic[T]):
    case_ConsStr : Callable[[ConsStr], T]
    case_SingleStr : Callable[[SingleStr], T]


# matching for type sequence_str
def match_sequence_str(o : sequence_str, handlers : SequenceStrHandlers[T]) -> T :
    return o._match(handlers)


# type arguments
@dataclass
class arguments(ABC):
    @abstractmethod
    def _match(self, handlers : ArgumentsHandlers[T]) -> T: pass


# constructors for type arguments

@dataclass
class ConsArg(arguments):
    head : expr
    tail : arguments

    def _match(self, handlers : ArgumentsHandlers[T]) -> T:
        return handlers.case_ConsArg(self)


def make_ConsArg(
    head : expr,
    tail : arguments
) -> arguments:
    return ConsArg(
        head,
        tail
    )


@dataclass
class SingleArg(arguments):
    content : expr

    def _match(self, handlers : ArgumentsHandlers[T]) -> T:
        return handlers.case_SingleArg(self)


def make_SingleArg(
    content : expr
) -> arguments:
    return SingleArg(
        content
    )


@dataclass
class KeywordsArg(arguments):
    kws : keywords

    def _match(self, handlers : ArgumentsHandlers[T]) -> T:
        return handlers.case_KeywordsArg(self)


def make_KeywordsArg(
    kws : keywords
) -> arguments:
    return KeywordsArg(
        kws
    )


# case handlers for type arguments
@dataclass
class ArgumentsHandlers(Generic[T]):
    case_ConsArg : Callable[[ConsArg], T]
    case_SingleArg : Callable[[SingleArg], T]
    case_KeywordsArg : Callable[[KeywordsArg], T]


# matching for type arguments
def match_arguments(o : arguments, handlers : ArgumentsHandlers[T]) -> T :
    return o._match(handlers)


# type dictionary_contents
@dataclass
class dictionary_contents(ABC):
    @abstractmethod
    def _match(self, handlers : DictionaryContentsHandlers[T]) -> T: pass


# constructors for type dictionary_contents

@dataclass
class ConsField(dictionary_contents):
    head : Field
    tail : dictionary_contents

    def _match(self, handlers : DictionaryContentsHandlers[T]) -> T:
        return handlers.case_ConsField(self)


def make_ConsField(
    head : Field,
    tail : dictionary_contents
) -> dictionary_contents:
    return ConsField(
        head,
        tail
    )


@dataclass
class SingleField(dictionary_contents):
    content : Field

    def _match(self, handlers : DictionaryContentsHandlers[T]) -> T:
        return handlers.case_SingleField(self)


def make_SingleField(
    content : Field
) -> dictionary_contents:
    return SingleField(
        content
    )


# case handlers for type dictionary_contents
@dataclass
class DictionaryContentsHandlers(Generic[T]):
    case_ConsField : Callable[[ConsField], T]
    case_SingleField : Callable[[SingleField], T]


# matching for type dictionary_contents
def match_dictionary_contents(o : dictionary_contents, handlers : DictionaryContentsHandlers[T]) -> T :
    return o._match(handlers)


# type sequence_Identifier
@dataclass
class sequence_Identifier(ABC):
    @abstractmethod
    def _match(self, handlers : SequenceIdentifierHandlers[T]) -> T: pass


# constructors for type sequence_Identifier

@dataclass
class ConsId(sequence_Identifier):
    head : Identifier
    tail : sequence_Identifier

    def _match(self, handlers : SequenceIdentifierHandlers[T]) -> T:
        return handlers.case_ConsId(self)


def make_ConsId(
    head : Identifier,
    tail : sequence_Identifier
) -> sequence_Identifier:
    return ConsId(
        head,
        tail
    )


@dataclass
class SingleId(sequence_Identifier):
    content : Identifier

    def _match(self, handlers : SequenceIdentifierHandlers[T]) -> T:
        return handlers.case_SingleId(self)


def make_SingleId(
    content : Identifier
) -> sequence_Identifier:
    return SingleId(
        content
    )


# case handlers for type sequence_Identifier
@dataclass
class SequenceIdentifierHandlers(Generic[T]):
    case_ConsId : Callable[[ConsId], T]
    case_SingleId : Callable[[SingleId], T]


# matching for type sequence_Identifier
def match_sequence_Identifier(o : sequence_Identifier, handlers : SequenceIdentifierHandlers[T]) -> T :
    return o._match(handlers)


# type sequence_ImportName
@dataclass
class sequence_ImportName(ABC):
    @abstractmethod
    def _match(self, handlers : SequenceImportNameHandlers[T]) -> T: pass


# constructors for type sequence_ImportName

@dataclass
class ConsImportName(sequence_ImportName):
    head : ImportName
    tail : sequence_ImportName

    def _match(self, handlers : SequenceImportNameHandlers[T]) -> T:
        return handlers.case_ConsImportName(self)


def make_ConsImportName(
    head : ImportName,
    tail : sequence_ImportName
) -> sequence_ImportName:
    return ConsImportName(
        head,
        tail
    )


@dataclass
class SingleImportName(sequence_ImportName):
    content : ImportName

    def _match(self, handlers : SequenceImportNameHandlers[T]) -> T:
        return handlers.case_SingleImportName(self)


def make_SingleImportName(
    content : ImportName
) -> sequence_ImportName:
    return SingleImportName(
        content
    )


# case handlers for type sequence_ImportName
@dataclass
class SequenceImportNameHandlers(Generic[T]):
    case_ConsImportName : Callable[[ConsImportName], T]
    case_SingleImportName : Callable[[SingleImportName], T]


# matching for type sequence_ImportName
def match_sequence_ImportName(o : sequence_ImportName, handlers : SequenceImportNameHandlers[T]) -> T :
    return o._match(handlers)


# type sequence_Withitem
@dataclass
class sequence_Withitem(ABC):
    @abstractmethod
    def _match(self, handlers : SequenceWithitemHandlers[T]) -> T: pass


# constructors for type sequence_Withitem

@dataclass
class ConsWithitem(sequence_Withitem):
    head : Withitem
    tail : sequence_Withitem

    def _match(self, handlers : SequenceWithitemHandlers[T]) -> T:
        return handlers.case_ConsWithitem(self)


def make_ConsWithitem(
    head : Withitem,
    tail : sequence_Withitem
) -> sequence_Withitem:
    return ConsWithitem(
        head,
        tail
    )


@dataclass
class SingleWithitem(sequence_Withitem):
    content : Withitem

    def _match(self, handlers : SequenceWithitemHandlers[T]) -> T:
        return handlers.case_SingleWithitem(self)


def make_SingleWithitem(
    content : Withitem
) -> sequence_Withitem:
    return SingleWithitem(
        content
    )


# case handlers for type sequence_Withitem
@dataclass
class SequenceWithitemHandlers(Generic[T]):
    case_ConsWithitem : Callable[[ConsWithitem], T]
    case_SingleWithitem : Callable[[SingleWithitem], T]


# matching for type sequence_Withitem
def match_sequence_Withitem(o : sequence_Withitem, handlers : SequenceWithitemHandlers[T]) -> T :
    return o._match(handlers)


# type statements
@dataclass
class statements(ABC):
    @abstractmethod
    def _match(self, handlers : StatementsHandlers[T]) -> T: pass


# constructors for type statements

@dataclass
class ConsStmt(statements):
    head : stmt
    tail : statements

    def _match(self, handlers : StatementsHandlers[T]) -> T:
        return handlers.case_ConsStmt(self)


def make_ConsStmt(
    head : stmt,
    tail : statements
) -> statements:
    return ConsStmt(
        head,
        tail
    )


@dataclass
class SingleStmt(statements):
    content : stmt

    def _match(self, handlers : StatementsHandlers[T]) -> T:
        return handlers.case_SingleStmt(self)


def make_SingleStmt(
    content : stmt
) -> statements:
    return SingleStmt(
        content
    )


# case handlers for type statements
@dataclass
class StatementsHandlers(Generic[T]):
    case_ConsStmt : Callable[[ConsStmt], T]
    case_SingleStmt : Callable[[SingleStmt], T]


# matching for type statements
def match_statements(o : statements, handlers : StatementsHandlers[T]) -> T :
    return o._match(handlers)


# type comprehension_constraints
@dataclass
class comprehension_constraints(ABC):
    @abstractmethod
    def _match(self, handlers : ComprehensionConstraintsHandlers[T]) -> T: pass


# constructors for type comprehension_constraints

@dataclass
class ConsConstraint(comprehension_constraints):
    head : constraint
    tail : comprehension_constraints

    def _match(self, handlers : ComprehensionConstraintsHandlers[T]) -> T:
        return handlers.case_ConsConstraint(self)


def make_ConsConstraint(
    head : constraint,
    tail : comprehension_constraints
) -> comprehension_constraints:
    return ConsConstraint(
        head,
        tail
    )


@dataclass
class SingleConstraint(comprehension_constraints):
    content : constraint

    def _match(self, handlers : ComprehensionConstraintsHandlers[T]) -> T:
        return handlers.case_SingleConstraint(self)


def make_SingleConstraint(
    content : constraint
) -> comprehension_constraints:
    return SingleConstraint(
        content
    )


# case handlers for type comprehension_constraints
@dataclass
class ComprehensionConstraintsHandlers(Generic[T]):
    case_ConsConstraint : Callable[[ConsConstraint], T]
    case_SingleConstraint : Callable[[SingleConstraint], T]


# matching for type comprehension_constraints
def match_comprehension_constraints(o : comprehension_constraints, handlers : ComprehensionConstraintsHandlers[T]) -> T :
    return o._match(handlers)


# type sequence_ExceptHandler
@dataclass
class sequence_ExceptHandler(ABC):
    @abstractmethod
    def _match(self, handlers : SequenceExceptHandlerHandlers[T]) -> T: pass


# constructors for type sequence_ExceptHandler

@dataclass
class ConsExceptHandler(sequence_ExceptHandler):
    head : ExceptHandler
    tail : sequence_ExceptHandler

    def _match(self, handlers : SequenceExceptHandlerHandlers[T]) -> T:
        return handlers.case_ConsExceptHandler(self)


def make_ConsExceptHandler(
    head : ExceptHandler,
    tail : sequence_ExceptHandler
) -> sequence_ExceptHandler:
    return ConsExceptHandler(
        head,
        tail
    )


@dataclass
class SingleExceptHandler(sequence_ExceptHandler):
    content : ExceptHandler

    def _match(self, handlers : SequenceExceptHandlerHandlers[T]) -> T:
        return handlers.case_SingleExceptHandler(self)


def make_SingleExceptHandler(
    content : ExceptHandler
) -> sequence_ExceptHandler:
    return SingleExceptHandler(
        content
    )


# case handlers for type sequence_ExceptHandler
@dataclass
class SequenceExceptHandlerHandlers(Generic[T]):
    case_ConsExceptHandler : Callable[[ConsExceptHandler], T]
    case_SingleExceptHandler : Callable[[SingleExceptHandler], T]


# matching for type sequence_ExceptHandler
def match_sequence_ExceptHandler(o : sequence_ExceptHandler, handlers : SequenceExceptHandlerHandlers[T]) -> T :
    return o._match(handlers)


# type conditions
@dataclass
class conditions(ABC):
    @abstractmethod
    def _match(self, handlers : ConditionsHandlers[T]) -> T: pass


# constructors for type conditions

@dataclass
class ElifCond(conditions):
    test : expr
    body : statements
    tail : conditions

    def _match(self, handlers : ConditionsHandlers[T]) -> T:
        return handlers.case_ElifCond(self)


def make_ElifCond(
    test : expr,
    body : statements,
    tail : conditions
) -> conditions:
    return ElifCond(
        test,
        body,
        tail
    )


@dataclass
class ElseCond(conditions):
    content : else_block

    def _match(self, handlers : ConditionsHandlers[T]) -> T:
        return handlers.case_ElseCond(self)


def make_ElseCond(
    content : else_block
) -> conditions:
    return ElseCond(
        content
    )


# case handlers for type conditions
@dataclass
class ConditionsHandlers(Generic[T]):
    case_ElifCond : Callable[[ElifCond], T]
    case_ElseCond : Callable[[ElseCond], T]


# matching for type conditions
def match_conditions(o : conditions, handlers : ConditionsHandlers[T]) -> T :
    return o._match(handlers)


# type else_block
@dataclass
class else_block(ABC):
    @abstractmethod
    def _match(self, handlers : ElseBlockHandlers[T]) -> T: pass


# constructors for type else_block

@dataclass
class SomeElseBlock(else_block):
    body : statements

    def _match(self, handlers : ElseBlockHandlers[T]) -> T:
        return handlers.case_SomeElseBlock(self)


def make_SomeElseBlock(
    body : statements
) -> else_block:
    return SomeElseBlock(
        body
    )


@dataclass
class NoElseBlock(else_block):

    def _match(self, handlers : ElseBlockHandlers[T]) -> T:
        return handlers.case_NoElseBlock(self)


def make_NoElseBlock(
) -> else_block:
    return NoElseBlock(
    )


# case handlers for type else_block
@dataclass
class ElseBlockHandlers(Generic[T]):
    case_SomeElseBlock : Callable[[SomeElseBlock], T]
    case_NoElseBlock : Callable[[NoElseBlock], T]


# matching for type else_block
def match_else_block(o : else_block, handlers : ElseBlockHandlers[T]) -> T :
    return o._match(handlers)


# type final
@dataclass
class final(ABC):
    @abstractmethod
    def _match(self, handlers : FinalHandlers[T]) -> T: pass


# constructors for type final

@dataclass
class SomeFinal(final):
    body : statements

    def _match(self, handlers : FinalHandlers[T]) -> T:
        return handlers.case_SomeFinal(self)


def make_SomeFinal(
    body : statements
) -> final:
    return SomeFinal(
        body
    )


@dataclass
class NoFinal(final):

    def _match(self, handlers : FinalHandlers[T]) -> T:
        return handlers.case_NoFinal(self)


def make_NoFinal(
) -> final:
    return NoFinal(
    )


# case handlers for type final
@dataclass
class FinalHandlers(Generic[T]):
    case_SomeFinal : Callable[[SomeFinal], T]
    case_NoFinal : Callable[[NoFinal], T]


# matching for type final
def match_final(o : final, handlers : FinalHandlers[T]) -> T :
    return o._match(handlers)


# type function_def
@dataclass
class function_def(ABC):
    @abstractmethod
    def _match(self, handlers : FunctionDefHandlers[T]) -> T: pass


# constructors for type function_def

@dataclass
class FunctionDef(function_def):
    name : Identifier
    params : parameters
    ret_typ : return_type
    body : statements

    def _match(self, handlers : FunctionDefHandlers[T]) -> T:
        return handlers.case_FunctionDef(self)


def make_FunctionDef(
    name : Identifier,
    params : parameters,
    ret_typ : return_type,
    body : statements
) -> function_def:
    return FunctionDef(
        name,
        params,
        ret_typ,
        body
    )


@dataclass
class AsyncFunctionDef(function_def):
    name : Identifier
    params : parameters
    ret_typ : return_type
    body : statements

    def _match(self, handlers : FunctionDefHandlers[T]) -> T:
        return handlers.case_AsyncFunctionDef(self)


def make_AsyncFunctionDef(
    name : Identifier,
    params : parameters,
    ret_typ : return_type,
    body : statements
) -> function_def:
    return AsyncFunctionDef(
        name,
        params,
        ret_typ,
        body
    )


# case handlers for type function_def
@dataclass
class FunctionDefHandlers(Generic[T]):
    case_FunctionDef : Callable[[FunctionDef], T]
    case_AsyncFunctionDef : Callable[[AsyncFunctionDef], T]


# matching for type function_def
def match_function_def(o : function_def, handlers : FunctionDefHandlers[T]) -> T :
    return o._match(handlers)


# type stmt
@dataclass
class stmt(ABC):
    @abstractmethod
    def _match(self, handlers : StmtHandlers[T]) -> T: pass


# constructors for type stmt

@dataclass
class DecFunctionDef(stmt):
    decs : decorators
    fun_def : function_def

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_DecFunctionDef(self)


def make_DecFunctionDef(
    decs : decorators,
    fun_def : function_def
) -> stmt:
    return DecFunctionDef(
        decs,
        fun_def
    )


@dataclass
class DecAsyncFunctionDef(stmt):
    decs : decorators
    fun_def : function_def

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_DecAsyncFunctionDef(self)


def make_DecAsyncFunctionDef(
    decs : decorators,
    fun_def : function_def
) -> stmt:
    return DecAsyncFunctionDef(
        decs,
        fun_def
    )


@dataclass
class DecClassDef(stmt):
    decs : decorators
    class_def : ClassDef

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_DecClassDef(self)


def make_DecClassDef(
    decs : decorators,
    class_def : ClassDef
) -> stmt:
    return DecClassDef(
        decs,
        class_def
    )


@dataclass
class ReturnSomething(stmt):
    content : expr

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_ReturnSomething(self)


def make_ReturnSomething(
    content : expr
) -> stmt:
    return ReturnSomething(
        content
    )


@dataclass
class Return(stmt):

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_Return(self)


def make_Return(
) -> stmt:
    return Return(
    )


@dataclass
class Delete(stmt):
    targets : comma_exprs

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_Delete(self)


def make_Delete(
    targets : comma_exprs
) -> stmt:
    return Delete(
        targets
    )


@dataclass
class Assign(stmt):
    targets : comma_exprs
    content : expr

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_Assign(self)


def make_Assign(
    targets : comma_exprs,
    content : expr
) -> stmt:
    return Assign(
        targets,
        content
    )


@dataclass
class AugAssign(stmt):
    target : expr
    op : operator
    content : expr

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_AugAssign(self)


def make_AugAssign(
    target : expr,
    op : operator,
    content : expr
) -> stmt:
    return AugAssign(
        target,
        op,
        content
    )


@dataclass
class TypedAssign(stmt):
    target : expr
    type : expr
    content : expr

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_TypedAssign(self)


def make_TypedAssign(
    target : expr,
    type : expr,
    content : expr
) -> stmt:
    return TypedAssign(
        target,
        type,
        content
    )


@dataclass
class TypedDeclare(stmt):
    target : expr
    type : expr

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_TypedDeclare(self)


def make_TypedDeclare(
    target : expr,
    type : expr
) -> stmt:
    return TypedDeclare(
        target,
        type
    )


@dataclass
class For(stmt):
    target : expr
    iter : expr
    body : statements
    orelse : else_block

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_For(self)


def make_For(
    target : expr,
    iter : expr,
    body : statements,
    orelse : else_block
) -> stmt:
    return For(
        target,
        iter,
        body,
        orelse
    )


@dataclass
class AsyncFor(stmt):
    target : expr
    iter : expr
    body : statements
    orelse : else_block

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_AsyncFor(self)


def make_AsyncFor(
    target : expr,
    iter : expr,
    body : statements,
    orelse : else_block
) -> stmt:
    return AsyncFor(
        target,
        iter,
        body,
        orelse
    )


@dataclass
class While(stmt):
    test : expr
    body : statements
    orelse : else_block

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_While(self)


def make_While(
    test : expr,
    body : statements,
    orelse : else_block
) -> stmt:
    return While(
        test,
        body,
        orelse
    )


@dataclass
class If(stmt):
    test : expr
    body : statements
    orelse : conditions

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_If(self)


def make_If(
    test : expr,
    body : statements,
    orelse : conditions
) -> stmt:
    return If(
        test,
        body,
        orelse
    )


@dataclass
class With(stmt):
    items : sequence_Withitem
    body : statements

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_With(self)


def make_With(
    items : sequence_Withitem,
    body : statements
) -> stmt:
    return With(
        items,
        body
    )


@dataclass
class AsyncWith(stmt):
    items : sequence_Withitem
    body : statements

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_AsyncWith(self)


def make_AsyncWith(
    items : sequence_Withitem,
    body : statements
) -> stmt:
    return AsyncWith(
        items,
        body
    )


@dataclass
class Raise(stmt):

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_Raise(self)


def make_Raise(
) -> stmt:
    return Raise(
    )


@dataclass
class RaiseExc(stmt):
    exc : expr

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_RaiseExc(self)


def make_RaiseExc(
    exc : expr
) -> stmt:
    return RaiseExc(
        exc
    )


@dataclass
class RaiseFrom(stmt):
    exc : expr
    caus : expr

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_RaiseFrom(self)


def make_RaiseFrom(
    exc : expr,
    caus : expr
) -> stmt:
    return RaiseFrom(
        exc,
        caus
    )


@dataclass
class Try(stmt):
    body : statements
    handlers : sequence_ExceptHandler
    orelse : else_block
    fin : final

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_Try(self)


def make_Try(
    body : statements,
    handlers : sequence_ExceptHandler,
    orelse : else_block,
    fin : final
) -> stmt:
    return Try(
        body,
        handlers,
        orelse,
        fin
    )


@dataclass
class Assert(stmt):
    test : expr

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_Assert(self)


def make_Assert(
    test : expr
) -> stmt:
    return Assert(
        test
    )


@dataclass
class AssertMsg(stmt):
    test : expr
    msg : expr

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_AssertMsg(self)


def make_AssertMsg(
    test : expr,
    msg : expr
) -> stmt:
    return AssertMsg(
        test,
        msg
    )


@dataclass
class Import(stmt):
    names : sequence_ImportName

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_Import(self)


def make_Import(
    names : sequence_ImportName
) -> stmt:
    return Import(
        names
    )


@dataclass
class ImportFrom(stmt):
    module : module_id
    names : sequence_ImportName

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_ImportFrom(self)


def make_ImportFrom(
    module : module_id,
    names : sequence_ImportName
) -> stmt:
    return ImportFrom(
        module,
        names
    )


@dataclass
class ImportWildCard(stmt):
    module : module_id

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_ImportWildCard(self)


def make_ImportWildCard(
    module : module_id
) -> stmt:
    return ImportWildCard(
        module
    )


@dataclass
class Global(stmt):
    names : sequence_Identifier

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_Global(self)


def make_Global(
    names : sequence_Identifier
) -> stmt:
    return Global(
        names
    )


@dataclass
class Nonlocal(stmt):
    names : sequence_Identifier

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_Nonlocal(self)


def make_Nonlocal(
    names : sequence_Identifier
) -> stmt:
    return Nonlocal(
        names
    )


@dataclass
class Expr(stmt):
    content : expr

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_Expr(self)


def make_Expr(
    content : expr
) -> stmt:
    return Expr(
        content
    )


@dataclass
class Pass(stmt):

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_Pass(self)


def make_Pass(
) -> stmt:
    return Pass(
    )


@dataclass
class Break(stmt):

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_Break(self)


def make_Break(
) -> stmt:
    return Break(
    )


@dataclass
class Continue(stmt):

    def _match(self, handlers : StmtHandlers[T]) -> T:
        return handlers.case_Continue(self)


def make_Continue(
) -> stmt:
    return Continue(
    )


# case handlers for type stmt
@dataclass
class StmtHandlers(Generic[T]):
    case_DecFunctionDef : Callable[[DecFunctionDef], T]
    case_DecAsyncFunctionDef : Callable[[DecAsyncFunctionDef], T]
    case_DecClassDef : Callable[[DecClassDef], T]
    case_ReturnSomething : Callable[[ReturnSomething], T]
    case_Return : Callable[[Return], T]
    case_Delete : Callable[[Delete], T]
    case_Assign : Callable[[Assign], T]
    case_AugAssign : Callable[[AugAssign], T]
    case_TypedAssign : Callable[[TypedAssign], T]
    case_TypedDeclare : Callable[[TypedDeclare], T]
    case_For : Callable[[For], T]
    case_AsyncFor : Callable[[AsyncFor], T]
    case_While : Callable[[While], T]
    case_If : Callable[[If], T]
    case_With : Callable[[With], T]
    case_AsyncWith : Callable[[AsyncWith], T]
    case_Raise : Callable[[Raise], T]
    case_RaiseExc : Callable[[RaiseExc], T]
    case_RaiseFrom : Callable[[RaiseFrom], T]
    case_Try : Callable[[Try], T]
    case_Assert : Callable[[Assert], T]
    case_AssertMsg : Callable[[AssertMsg], T]
    case_Import : Callable[[Import], T]
    case_ImportFrom : Callable[[ImportFrom], T]
    case_ImportWildCard : Callable[[ImportWildCard], T]
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


def make_BoolOp(
    left : expr,
    op : boolop,
    right : expr
) -> expr:
    return BoolOp(
        left,
        op,
        right
    )


@dataclass
class NamedExpr(expr):
    target : expr
    content : expr

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_NamedExpr(self)


def make_NamedExpr(
    target : expr,
    content : expr
) -> expr:
    return NamedExpr(
        target,
        content
    )


@dataclass
class BinOp(expr):
    left : expr
    op : operator
    right : expr

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_BinOp(self)


def make_BinOp(
    left : expr,
    op : operator,
    right : expr
) -> expr:
    return BinOp(
        left,
        op,
        right
    )


@dataclass
class UnaryOp(expr):
    op : unaryop
    right : expr

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_UnaryOp(self)


def make_UnaryOp(
    op : unaryop,
    right : expr
) -> expr:
    return UnaryOp(
        op,
        right
    )


@dataclass
class Lambda(expr):
    params : parameters
    body : expr

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Lambda(self)


def make_Lambda(
    params : parameters,
    body : expr
) -> expr:
    return Lambda(
        params,
        body
    )


@dataclass
class IfExp(expr):
    body : expr
    test : expr
    orelse : expr

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_IfExp(self)


def make_IfExp(
    body : expr,
    test : expr,
    orelse : expr
) -> expr:
    return IfExp(
        body,
        test,
        orelse
    )


@dataclass
class Dictionary(expr):
    contents : dictionary_contents

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Dictionary(self)


def make_Dictionary(
    contents : dictionary_contents
) -> expr:
    return Dictionary(
        contents
    )


@dataclass
class EmptyDictionary(expr):

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_EmptyDictionary(self)


def make_EmptyDictionary(
) -> expr:
    return EmptyDictionary(
    )


@dataclass
class Set(expr):
    contents : comma_exprs

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Set(self)


def make_Set(
    contents : comma_exprs
) -> expr:
    return Set(
        contents
    )


@dataclass
class ListComp(expr):
    content : expr
    constraints : comprehension_constraints

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_ListComp(self)


def make_ListComp(
    content : expr,
    constraints : comprehension_constraints
) -> expr:
    return ListComp(
        content,
        constraints
    )


@dataclass
class SetComp(expr):
    content : expr
    constraints : comprehension_constraints

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_SetComp(self)


def make_SetComp(
    content : expr,
    constraints : comprehension_constraints
) -> expr:
    return SetComp(
        content,
        constraints
    )


@dataclass
class DictionaryComp(expr):
    key : expr
    content : expr
    constraints : comprehension_constraints

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_DictionaryComp(self)


def make_DictionaryComp(
    key : expr,
    content : expr,
    constraints : comprehension_constraints
) -> expr:
    return DictionaryComp(
        key,
        content,
        constraints
    )


@dataclass
class GeneratorExp(expr):
    content : expr
    constraints : comprehension_constraints

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_GeneratorExp(self)


def make_GeneratorExp(
    content : expr,
    constraints : comprehension_constraints
) -> expr:
    return GeneratorExp(
        content,
        constraints
    )


@dataclass
class Await(expr):
    content : expr

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Await(self)


def make_Await(
    content : expr
) -> expr:
    return Await(
        content
    )


@dataclass
class YieldNothing(expr):

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_YieldNothing(self)


def make_YieldNothing(
) -> expr:
    return YieldNothing(
    )


@dataclass
class Yield(expr):
    content : expr

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Yield(self)


def make_Yield(
    content : expr
) -> expr:
    return Yield(
        content
    )


@dataclass
class YieldFrom(expr):
    content : expr

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_YieldFrom(self)


def make_YieldFrom(
    content : expr
) -> expr:
    return YieldFrom(
        content
    )


@dataclass
class Compare(expr):
    left : expr
    comps : comparisons

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Compare(self)


def make_Compare(
    left : expr,
    comps : comparisons
) -> expr:
    return Compare(
        left,
        comps
    )


@dataclass
class Call(expr):
    func : expr

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Call(self)


def make_Call(
    func : expr
) -> expr:
    return Call(
        func
    )


@dataclass
class CallArgs(expr):
    func : expr
    args : arguments

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_CallArgs(self)


def make_CallArgs(
    func : expr,
    args : arguments
) -> expr:
    return CallArgs(
        func,
        args
    )


@dataclass
class Integer(expr):
    content : str

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Integer(self)


def make_Integer(
    content : str
) -> expr:
    return Integer(
        content
    )


@dataclass
class Float(expr):
    content : str

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Float(self)


def make_Float(
    content : str
) -> expr:
    return Float(
        content
    )


@dataclass
class ConcatString(expr):
    content : sequence_str

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_ConcatString(self)


def make_ConcatString(
    content : sequence_str
) -> expr:
    return ConcatString(
        content
    )


@dataclass
class True_(expr):

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_True_(self)


def make_True_(
) -> expr:
    return True_(
    )


@dataclass
class False_(expr):

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_False_(self)


def make_False_(
) -> expr:
    return False_(
    )


@dataclass
class None_(expr):

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_None_(self)


def make_None_(
) -> expr:
    return None_(
    )


@dataclass
class Ellip(expr):

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Ellip(self)


def make_Ellip(
) -> expr:
    return Ellip(
    )


@dataclass
class Attribute(expr):
    content : expr
    attr : Identifier

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Attribute(self)


def make_Attribute(
    content : expr,
    attr : Identifier
) -> expr:
    return Attribute(
        content,
        attr
    )


@dataclass
class Subscript(expr):
    content : expr
    slice : expr

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Subscript(self)


def make_Subscript(
    content : expr,
    slice : expr
) -> expr:
    return Subscript(
        content,
        slice
    )


@dataclass
class Starred(expr):
    content : expr

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Starred(self)


def make_Starred(
    content : expr
) -> expr:
    return Starred(
        content
    )


@dataclass
class Name(expr):
    id : Identifier

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Name(self)


def make_Name(
    id : Identifier
) -> expr:
    return Name(
        id
    )


@dataclass
class List(expr):
    contents : comma_exprs

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_List(self)


def make_List(
    contents : comma_exprs
) -> expr:
    return List(
        contents
    )


@dataclass
class EmptyList(expr):

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_EmptyList(self)


def make_EmptyList(
) -> expr:
    return EmptyList(
    )


@dataclass
class Tuple(expr):
    contents : comma_exprs

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Tuple(self)


def make_Tuple(
    contents : comma_exprs
) -> expr:
    return Tuple(
        contents
    )


@dataclass
class Slice(expr):
    lower : option_expr
    upper : option_expr
    step : option_expr

    def _match(self, handlers : ExprHandlers[T]) -> T:
        return handlers.case_Slice(self)


def make_Slice(
    lower : option_expr,
    upper : option_expr,
    step : option_expr
) -> expr:
    return Slice(
        lower,
        upper,
        step
    )


# case handlers for type expr
@dataclass
class ExprHandlers(Generic[T]):
    case_BoolOp : Callable[[BoolOp], T]
    case_NamedExpr : Callable[[NamedExpr], T]
    case_BinOp : Callable[[BinOp], T]
    case_UnaryOp : Callable[[UnaryOp], T]
    case_Lambda : Callable[[Lambda], T]
    case_IfExp : Callable[[IfExp], T]
    case_Dictionary : Callable[[Dictionary], T]
    case_EmptyDictionary : Callable[[EmptyDictionary], T]
    case_Set : Callable[[Set], T]
    case_ListComp : Callable[[ListComp], T]
    case_SetComp : Callable[[SetComp], T]
    case_DictionaryComp : Callable[[DictionaryComp], T]
    case_GeneratorExp : Callable[[GeneratorExp], T]
    case_Await : Callable[[Await], T]
    case_YieldNothing : Callable[[YieldNothing], T]
    case_Yield : Callable[[Yield], T]
    case_YieldFrom : Callable[[YieldFrom], T]
    case_Compare : Callable[[Compare], T]
    case_Call : Callable[[Call], T]
    case_CallArgs : Callable[[CallArgs], T]
    case_Integer : Callable[[Integer], T]
    case_Float : Callable[[Float], T]
    case_ConcatString : Callable[[ConcatString], T]
    case_True_ : Callable[[True_], T]
    case_False_ : Callable[[False_], T]
    case_None_ : Callable[[None_], T]
    case_Ellip : Callable[[Ellip], T]
    case_Attribute : Callable[[Attribute], T]
    case_Subscript : Callable[[Subscript], T]
    case_Starred : Callable[[Starred], T]
    case_Name : Callable[[Name], T]
    case_List : Callable[[List], T]
    case_EmptyList : Callable[[EmptyList], T]
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


def make_And(
) -> boolop:
    return And(
    )


@dataclass
class Or(boolop):

    def _match(self, handlers : BoolopHandlers[T]) -> T:
        return handlers.case_Or(self)


def make_Or(
) -> boolop:
    return Or(
    )


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


def make_Add(
) -> operator:
    return Add(
    )


@dataclass
class Sub(operator):

    def _match(self, handlers : OperatorHandlers[T]) -> T:
        return handlers.case_Sub(self)


def make_Sub(
) -> operator:
    return Sub(
    )


@dataclass
class Mult(operator):

    def _match(self, handlers : OperatorHandlers[T]) -> T:
        return handlers.case_Mult(self)


def make_Mult(
) -> operator:
    return Mult(
    )


@dataclass
class MatMult(operator):

    def _match(self, handlers : OperatorHandlers[T]) -> T:
        return handlers.case_MatMult(self)


def make_MatMult(
) -> operator:
    return MatMult(
    )


@dataclass
class Div(operator):

    def _match(self, handlers : OperatorHandlers[T]) -> T:
        return handlers.case_Div(self)


def make_Div(
) -> operator:
    return Div(
    )


@dataclass
class Mod(operator):

    def _match(self, handlers : OperatorHandlers[T]) -> T:
        return handlers.case_Mod(self)


def make_Mod(
) -> operator:
    return Mod(
    )


@dataclass
class Pow(operator):

    def _match(self, handlers : OperatorHandlers[T]) -> T:
        return handlers.case_Pow(self)


def make_Pow(
) -> operator:
    return Pow(
    )


@dataclass
class LShift(operator):

    def _match(self, handlers : OperatorHandlers[T]) -> T:
        return handlers.case_LShift(self)


def make_LShift(
) -> operator:
    return LShift(
    )


@dataclass
class RShift(operator):

    def _match(self, handlers : OperatorHandlers[T]) -> T:
        return handlers.case_RShift(self)


def make_RShift(
) -> operator:
    return RShift(
    )


@dataclass
class BitOr(operator):

    def _match(self, handlers : OperatorHandlers[T]) -> T:
        return handlers.case_BitOr(self)


def make_BitOr(
) -> operator:
    return BitOr(
    )


@dataclass
class BitXor(operator):

    def _match(self, handlers : OperatorHandlers[T]) -> T:
        return handlers.case_BitXor(self)


def make_BitXor(
) -> operator:
    return BitXor(
    )


@dataclass
class BitAnd(operator):

    def _match(self, handlers : OperatorHandlers[T]) -> T:
        return handlers.case_BitAnd(self)


def make_BitAnd(
) -> operator:
    return BitAnd(
    )


@dataclass
class FloorDiv(operator):

    def _match(self, handlers : OperatorHandlers[T]) -> T:
        return handlers.case_FloorDiv(self)


def make_FloorDiv(
) -> operator:
    return FloorDiv(
    )


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


def make_Invert(
) -> unaryop:
    return Invert(
    )


@dataclass
class Not(unaryop):

    def _match(self, handlers : UnaryopHandlers[T]) -> T:
        return handlers.case_Not(self)


def make_Not(
) -> unaryop:
    return Not(
    )


@dataclass
class UAdd(unaryop):

    def _match(self, handlers : UnaryopHandlers[T]) -> T:
        return handlers.case_UAdd(self)


def make_UAdd(
) -> unaryop:
    return UAdd(
    )


@dataclass
class USub(unaryop):

    def _match(self, handlers : UnaryopHandlers[T]) -> T:
        return handlers.case_USub(self)


def make_USub(
) -> unaryop:
    return USub(
    )


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


def make_Eq(
) -> cmpop:
    return Eq(
    )


@dataclass
class NotEq(cmpop):

    def _match(self, handlers : CmpopHandlers[T]) -> T:
        return handlers.case_NotEq(self)


def make_NotEq(
) -> cmpop:
    return NotEq(
    )


@dataclass
class Lt(cmpop):

    def _match(self, handlers : CmpopHandlers[T]) -> T:
        return handlers.case_Lt(self)


def make_Lt(
) -> cmpop:
    return Lt(
    )


@dataclass
class LtE(cmpop):

    def _match(self, handlers : CmpopHandlers[T]) -> T:
        return handlers.case_LtE(self)


def make_LtE(
) -> cmpop:
    return LtE(
    )


@dataclass
class Gt(cmpop):

    def _match(self, handlers : CmpopHandlers[T]) -> T:
        return handlers.case_Gt(self)


def make_Gt(
) -> cmpop:
    return Gt(
    )


@dataclass
class GtE(cmpop):

    def _match(self, handlers : CmpopHandlers[T]) -> T:
        return handlers.case_GtE(self)


def make_GtE(
) -> cmpop:
    return GtE(
    )


@dataclass
class Is(cmpop):

    def _match(self, handlers : CmpopHandlers[T]) -> T:
        return handlers.case_Is(self)


def make_Is(
) -> cmpop:
    return Is(
    )


@dataclass
class IsNot(cmpop):

    def _match(self, handlers : CmpopHandlers[T]) -> T:
        return handlers.case_IsNot(self)


def make_IsNot(
) -> cmpop:
    return IsNot(
    )


@dataclass
class In(cmpop):

    def _match(self, handlers : CmpopHandlers[T]) -> T:
        return handlers.case_In(self)


def make_In(
) -> cmpop:
    return In(
    )


@dataclass
class NotIn(cmpop):

    def _match(self, handlers : CmpopHandlers[T]) -> T:
        return handlers.case_NotIn(self)


def make_NotIn(
) -> cmpop:
    return NotIn(
    )


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
    search_space : expr
    filts : constraint_filters

    def _match(self, handlers : ConstraintHandlers[T]) -> T:
        return handlers.case_AsyncConstraint(self)


def make_AsyncConstraint(
    target : expr,
    search_space : expr,
    filts : constraint_filters
) -> constraint:
    return AsyncConstraint(
        target,
        search_space,
        filts
    )


@dataclass
class Constraint(constraint):
    target : expr
    search_space : expr
    filts : constraint_filters

    def _match(self, handlers : ConstraintHandlers[T]) -> T:
        return handlers.case_Constraint(self)


def make_Constraint(
    target : expr,
    search_space : expr,
    filts : constraint_filters
) -> constraint:
    return Constraint(
        target,
        search_space,
        filts
    )


# case handlers for type constraint
@dataclass
class ConstraintHandlers(Generic[T]):
    case_AsyncConstraint : Callable[[AsyncConstraint], T]
    case_Constraint : Callable[[Constraint], T]


# matching for type constraint
def match_constraint(o : constraint, handlers : ConstraintHandlers[T]) -> T :
    return o._match(handlers)