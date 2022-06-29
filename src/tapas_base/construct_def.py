from __future__ import annotations

from dataclasses import dataclass

import inflection

@dataclass(frozen=True, eq=True)
class Field:
    attr : str
    typ : str
    default : str

@dataclass(frozen=True, eq=True)
class Constructor:
    name: str 
    bases : list[str]
    fields: list[Field]


nl = "\n"
header = ("""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, TypeVar, Any, Generic, Union, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod

T = TypeVar('T')


@dataclass(frozen=True, eq=True)
class SourceFlag: 
    pass
""")

def generate_single(
    constructor : Constructor 
) -> str:

    bases_str = (
        '(' + ', '.join([
            base
            for  base in constructor.bases
        ]) + ')'
        if len(constructor.bases) > 0 else
        ""
    )

    code = (f"""
# type and constructor {constructor.name}
@dataclass(frozen=True, eq=True)
class {constructor.name}{bases_str}:
{nl.join([
    f"    {field.attr} : {field.typ}"
    for field in constructor.fields 
]) if len(constructor.fields) > 0 else "    pass"}


def make_{constructor.name}({",".join([f'''
    {field.attr} : {field.typ}''' + (f" = {field.default}" if field.default else "")
    for field in constructor.fields
])}
) -> {constructor.name}:
    return {constructor.name}({",".join([f'''
        {field.attr}'''
        for field in constructor.fields
    ])})

def update_{constructor.name}(source_{constructor.name} : {constructor.name}{''.join([
    f",{nl}    {field.attr} : Union[{field.typ}, SourceFlag] = SourceFlag()"
    for field in constructor.fields
])}
) -> {constructor.name}:
    return {constructor.name}({f", ".join([f'''
        source_{constructor.name}.{field.attr} if isinstance({field.attr}, SourceFlag) else {field.attr}'''
        for field in constructor.fields
    ])})

    """)
    return code 





def generate_choice(
    type_name : str,
    type_base : str,
    constructors : list[Constructor] 
) -> str:
    handlers_name = f"{inflection.camelize(type_name)}Handlers"


    def generate_constructor(constructor : Constructor) -> str:
        nonlocal handlers_name
        bases_str = ''.join([
            f', {base}'
            for  base in constructor.bases
        ])
        return (f"""
@dataclass(frozen=True, eq=True)
class {constructor.name}({type_name}{bases_str}):
{nl.join([
    f"    {field.attr} : {field.typ}"
    for field in constructor.fields
])}

    def match(self, handlers : {handlers_name}[T]) -> T:
        return handlers.case_{constructor.name}(self)

def make_{constructor.name}({", ".join([f'''
    {field.attr} : {field.typ}''' + (f" = {field.default}" if field.default else "")
    for field in constructor.fields
])}
) -> {type_name}:
    return {constructor.name}({",".join([f'''
        {field.attr}'''
        for field in constructor.fields
    ])}
    )

def update_{constructor.name}(source_{constructor.name} : {constructor.name}{''.join([
    f",{nl}    {field.attr} : Union[{field.typ}, SourceFlag] = SourceFlag()"
    for field in constructor.fields
])}
) -> {constructor.name}:
    return {constructor.name}({f",".join([f'''
        source_{constructor.name}.{field.attr} if isinstance({field.attr}, SourceFlag) else {field.attr}'''
        for field in constructor.fields
    ])}
    )

        """)

    code = (f"""
# type {type_name}
@dataclass(frozen=True, eq=True)
class {type_name}({type_base + ', ' if type_base else ''}ABC):
    # @abstractmethod
    def match(self, handlers : {handlers_name}[T]) -> T:
        raise Exception()


# constructors for type {type_name}
{nl.join([
    generate_constructor(constructor)
    for constructor in constructors
])}

# case handlers for type {type_name}
@dataclass(frozen=True, eq=True)
class {handlers_name}(Generic[T]):
{nl.join([
    f"    case_{constructor.name} : Callable[[{constructor.name}], T]"
    for constructor in constructors 
])}


# matching for type {type_name}
def match_{type_name}(o : {type_name}, handlers : {handlers_name}[T]) -> T :
    return o.match(handlers)


{type_name}_union = Union[{', '.join([ constructor.name for constructor in constructors ])}]

# unguarding for type {type_name}
def unguard_{type_name}(o : {type_name}) -> {type_name}_union :
    return match_{type_name}(o, {handlers_name}(
{f', {nl}'.join([
f"        case_{constructor.name} = lambda x : x"
    for constructor in constructors 
])}

    ))
    """)
    return code 

def generate_content(content_header : str, singles : list[Constructor], choices : dict[str, list[Constructor]]) -> str:

    return (f"""

{header}

{content_header}

{nl.join([
    generate_choice(type_name, '', cons)
    for type_name, cons in choices.items()
])} 

{nl.join([
    generate_single(con)
    for con in singles
])} 
    """)

def generate_choices_type_base(choices : dict[tuple[str, str], list[Constructor]]) -> str:
    return (f"""
{nl.join([
    generate_choice(type_name, type_base, cons)
    for (type_name, type_base), cons in choices.items()
])} 
    """)