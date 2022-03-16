from operator import mod
from pyrsistent.typing import PMap, PSet

from pyrsistent import m, pmap, v, PRecord, field
from pyrsistent.typing import PMap, PSet

from lib.python_util_construct_autogen import *




def from_env_to_string(pm : PMap) -> str:
    nl = "\n"
    return nl.join([
        f"      {k} |-> {v}"
        for k, v in pm.items()
    ])

def from_Inher_to_string(inher : Inher) -> str:

    return (
f"""attributes:
  mode = {inher.mode}
  local_env:
{from_env_to_string(inher.local_env)}
  nonlocal_env:
{from_env_to_string(inher.nonlocal_env)}
  global_env:
{from_env_to_string(inher.global_env)}
  module_env: 
{from_env_to_string(inher.module_env)}"""
    )

def from_env_to_dictionary(env : PMap[str, Declaration]) -> dict:
    return {
        symbol : {'init' : d.initialized}
        for symbol, d in env.items()
    }

def from_Inher_to_dictionary(inher : Inher) -> dict:
    return {
        'mode' : f"{inher.mode}",
        'local_env' : from_env_to_dictionary(inher.local_env),
        'nonlocal_env' : from_env_to_dictionary(inher.nonlocal_env),
        'global_env' : from_env_to_dictionary(inher.global_env)
    }

def set_local_env(inher : Inher, local_env : PMap[str, Declaration]) -> Inher:
    return Inher(
        mode = inher.mode,
        local_env = local_env, 
        nonlocal_env = inher.nonlocal_env,
        global_env = inher.global_env,
        module_env = inher.module_env
    )


def set_class_mode(inher : Inher) -> Inher:
    if isinstance(inher.mode, ModuleMode):
        return Inher(
            # copy local_decl into global_decl
            global_env = inher.local_env,
            nonlocal_env = inher.nonlocal_env, 
            local_env = inher.local_env, 
            module_env = inher.module_env, 
            # update mode
            mode = ClassMode() 
        )

    else:
        return Inher(
            global_env = inher.global_env,
            # copy local_decl into nonlocal_decl
            nonlocal_env = inher.nonlocal_env + inher.local_env, 
            local_env = inher.local_env, 
            module_env = inher.module_env, 
            # update mode
            mode = ClassMode() 
        )

def set_function_mode(inher : Inher) -> Inher:
    if isinstance(inher.mode, ModuleMode):
        return Inher(
            # move local_decl into global_decl
            global_env = inher.local_env,
            nonlocal_env = inher.nonlocal_env, 
            # reset local_decl
            local_env = m(), 
            module_env = inher.module_env,
            # update mode
            mode = FunctionMode() 
        )

    else:
        return Inher(
            global_env = inher.global_env,
            # move local_decl into nonlocal_decl 
            nonlocal_env = inher.nonlocal_env + inher.local_env, 
            # reset local_decl
            local_env = m(), 
            module_env = inher.module_env,
            mode = inher.mode 
        )

def set_delete_mode(inher : Inher) -> Inher:
    return Inher(
        mode = DeleteMode(),
        local_env = inher.local_env,
        nonlocal_env = inher.nonlocal_env, 
        global_env = inher.global_env,
        module_env = inher.module_env 
    )

def set_delete_slice_mode(inher : Inher) -> Inher:
    return Inher(
        mode = DeleteSliceMode(),
        local_env = inher.local_env,
        nonlocal_env = inher.nonlocal_env, 
        global_env = inher.global_env,
        module_env = inher.module_env 
    )

def set_attribute_mode(inher : Inher) -> Inher:
    return Inher(
        mode = AttributeMode(),
        local_env = inher.local_env,
        nonlocal_env = inher.nonlocal_env, 
        global_env = inher.global_env,
        module_env = inher.module_env 
    )

def set_pattern_target_mode(inher : Inher) -> Inher:
    return Inher(
        mode = PatternTargetMode(),
        local_env = inher.local_env,
        nonlocal_env = inher.nonlocal_env, 
        global_env = inher.global_env,
        module_env = inher.module_env 
    )

def set_name_target_mode(inher : Inher) -> Inher:
    return Inher(
        mode = NameTargetMode(),
        global_env = inher.global_env,
        nonlocal_env = inher.nonlocal_env, 
        local_env = inher.local_env,
        module_env = inher.module_env 
    )

def set_source_mode(inher : Inher) -> Inher:
    return Inher(
        mode = SourceMode(),
        local_env = inher.local_env,
        nonlocal_env = inher.nonlocal_env, 
        global_env = inher.global_env,
        module_env = inher.module_env 
    )

def set_open_mode(inher : Inher) -> Inher:
    return Inher(
        mode = OpenMode(),
        local_env = inher.local_env,
        nonlocal_env = inher.nonlocal_env, 
        global_env = inher.global_env,
        module_env = inher.module_env
    )

def set_import_mode(inher : Inher, path : str) -> Inher:
    return Inher(
        mode = ImportMode(path),
        local_env = inher.local_env,
        nonlocal_env = inher.nonlocal_env, 
        global_env = inher.global_env,
        module_env = inher.module_env
    )