# THIS FILE IS AUTOGENERATED
# CHANGES MAY BE LOST


from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, TypeVar, Any, Generic, Union, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod

T = TypeVar('T')


from pyrsistent.typing import PMap, PSet
from lib.abstract_token import abstract_token 


# type and constructor Declaration
@dataclass(frozen=True, eq=True)
class Declaration:
    initialized : bool



# type and constructor Inher
@dataclass(frozen=True, eq=True)
class Inher:
    global_env : PMap[str, Declaration]
    nonlocal_env : PMap[str, Declaration]
    local_env : PMap[str, Declaration]
    module_env : PMap[str, str]
    mode : mode



# type mode
@dataclass(frozen=True, eq=True)
class mode(ABC):
    @abstractmethod
    def _match(self, handlers : ModeHandlers[T]) -> T: pass


# constructors for type mode

@dataclass(frozen=True, eq=True)
class ModuleMode(mode):


    def _match(self, handlers : ModeHandlers[T]) -> T:
        return handlers.case_ModuleMode(self)

def make_ModuleMode() -> mode:
    return ModuleMode()
        

@dataclass(frozen=True, eq=True)
class FunctionMode(mode):


    def _match(self, handlers : ModeHandlers[T]) -> T:
        return handlers.case_FunctionMode(self)

def make_FunctionMode() -> mode:
    return FunctionMode()
        

@dataclass(frozen=True, eq=True)
class ClassMode(mode):


    def _match(self, handlers : ModeHandlers[T]) -> T:
        return handlers.case_ClassMode(self)

def make_ClassMode() -> mode:
    return ClassMode()
        

@dataclass(frozen=True, eq=True)
class NameTargetMode(mode):


    def _match(self, handlers : ModeHandlers[T]) -> T:
        return handlers.case_NameTargetMode(self)

def make_NameTargetMode() -> mode:
    return NameTargetMode()
        

@dataclass(frozen=True, eq=True)
class PatternTargetMode(mode):


    def _match(self, handlers : ModeHandlers[T]) -> T:
        return handlers.case_PatternTargetMode(self)

def make_PatternTargetMode() -> mode:
    return PatternTargetMode()
        

@dataclass(frozen=True, eq=True)
class SourceMode(mode):


    def _match(self, handlers : ModeHandlers[T]) -> T:
        return handlers.case_SourceMode(self)

def make_SourceMode() -> mode:
    return SourceMode()
        

@dataclass(frozen=True, eq=True)
class OpenMode(mode):


    def _match(self, handlers : ModeHandlers[T]) -> T:
        return handlers.case_OpenMode(self)

def make_OpenMode() -> mode:
    return OpenMode()
        

@dataclass(frozen=True, eq=True)
class ImportMode(mode):
    context : str

    def _match(self, handlers : ModeHandlers[T]) -> T:
        return handlers.case_ImportMode(self)

def make_ImportMode(context : str) -> mode:
    return ImportMode(context)
        

@dataclass(frozen=True, eq=True)
class AttributeMode(mode):


    def _match(self, handlers : ModeHandlers[T]) -> T:
        return handlers.case_AttributeMode(self)

def make_AttributeMode() -> mode:
    return AttributeMode()
        

@dataclass(frozen=True, eq=True)
class DeleteMode(mode):


    def _match(self, handlers : ModeHandlers[T]) -> T:
        return handlers.case_DeleteMode(self)

def make_DeleteMode() -> mode:
    return DeleteMode()
        

# case handlers for type mode
@dataclass(frozen=True, eq=True)
class ModeHandlers(Generic[T]):
    case_ModuleMode : Callable[[ModuleMode], T]
    case_FunctionMode : Callable[[FunctionMode], T]
    case_ClassMode : Callable[[ClassMode], T]
    case_NameTargetMode : Callable[[NameTargetMode], T]
    case_PatternTargetMode : Callable[[PatternTargetMode], T]
    case_SourceMode : Callable[[SourceMode], T]
    case_OpenMode : Callable[[OpenMode], T]
    case_ImportMode : Callable[[ImportMode], T]
    case_AttributeMode : Callable[[AttributeMode], T]
    case_DeleteMode : Callable[[DeleteMode], T]


# matching for type mode
def match_mode(o : mode, handlers : ModeHandlers[T]) -> T :
    return o._match(handlers)
    


# type synth
@dataclass(frozen=True, eq=True)
class synth(ABC):
    @abstractmethod
    def _match(self, handlers : SynthHandlers[T]) -> T: pass


# constructors for type synth

@dataclass(frozen=True, eq=True)
class NoSynth(synth):


    def _match(self, handlers : SynthHandlers[T]) -> T:
        return handlers.case_NoSynth(self)

def make_NoSynth() -> synth:
    return NoSynth()
        

@dataclass(frozen=True, eq=True)
class LocalEnvSynth(synth):
    subtractions : PSet[str]
    additions : PMap[str, Declaration]

    def _match(self, handlers : SynthHandlers[T]) -> T:
        return handlers.case_LocalEnvSynth(self)

def make_LocalEnvSynth(subtractions : PSet[str], additions : PMap[str, Declaration]) -> synth:
    return LocalEnvSynth(subtractions, additions)
        

@dataclass(frozen=True, eq=True)
class DeleteSynth(synth):
    names : PSet[str]

    def _match(self, handlers : SynthHandlers[T]) -> T:
        return handlers.case_DeleteSynth(self)

def make_DeleteSynth(names : PSet[str]) -> synth:
    return DeleteSynth(names)
        

@dataclass(frozen=True, eq=True)
class SourceSynth(synth):
    env_additions : PMap[str, Declaration]
    env_refs : PSet[str]
    tokens : tuple[abstract_token, ...]

    def _match(self, handlers : SynthHandlers[T]) -> T:
        return handlers.case_SourceSynth(self)

def make_SourceSynth(env_additions : PMap[str, Declaration], env_refs : PSet[str], tokens : tuple[abstract_token, ...]) -> synth:
    return SourceSynth(env_additions, env_refs, tokens)
        

@dataclass(frozen=True, eq=True)
class TargetSynth(synth):
    env_names : PSet[str]
    tokens : tuple[abstract_token, ...]

    def _match(self, handlers : SynthHandlers[T]) -> T:
        return handlers.case_TargetSynth(self)

def make_TargetSynth(env_names : PSet[str], tokens : tuple[abstract_token, ...]) -> synth:
    return TargetSynth(env_names, tokens)
        

@dataclass(frozen=True, eq=True)
class MultiTargetSynth(synth):
    names : PSet[str]
    tokens : PSet[tuple[abstract_token, ...]]

    def _match(self, handlers : SynthHandlers[T]) -> T:
        return handlers.case_MultiTargetSynth(self)

def make_MultiTargetSynth(names : PSet[str], tokens : PSet[tuple[abstract_token, ...]]) -> synth:
    return MultiTargetSynth(names, tokens)
        

@dataclass(frozen=True, eq=True)
class OpenSynth(synth):
    path : str

    def _match(self, handlers : SynthHandlers[T]) -> T:
        return handlers.case_OpenSynth(self)

def make_OpenSynth(path : str) -> synth:
    return OpenSynth(path)
        

@dataclass(frozen=True, eq=True)
class ImportSynth(synth):
    path : str

    def _match(self, handlers : SynthHandlers[T]) -> T:
        return handlers.case_ImportSynth(self)

def make_ImportSynth(path : str) -> synth:
    return ImportSynth(path)
        

# case handlers for type synth
@dataclass(frozen=True, eq=True)
class SynthHandlers(Generic[T]):
    case_NoSynth : Callable[[NoSynth], T]
    case_LocalEnvSynth : Callable[[LocalEnvSynth], T]
    case_DeleteSynth : Callable[[DeleteSynth], T]
    case_SourceSynth : Callable[[SourceSynth], T]
    case_TargetSynth : Callable[[TargetSynth], T]
    case_MultiTargetSynth : Callable[[MultiTargetSynth], T]
    case_OpenSynth : Callable[[OpenSynth], T]
    case_ImportSynth : Callable[[ImportSynth], T]


# matching for type synth
def match_synth(o : synth, handlers : SynthHandlers[T]) -> T :
    return o._match(handlers)
    
    