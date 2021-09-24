from __future__ import annotations

from dataclasses import dataclass

import inflection
import jinja2

@dataclass
class Field:
    attr : str
    typ : str

@dataclass
class Constructor:
    name: str 
    fields: list[Field]


jinja_env = jinja2.Environment(trim_blocks=True)

header = """
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, TypeVar, Any, Generic, Union, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod

T = TypeVar('T')
"""

def generate_intersection(
    constructor : Constructor 
) -> str:
    
    tmpl = jinja_env.from_string(
    """
# type and constructor {{ constructor.name }}
@dataclass
class {{ constructor.name }}:
{% for field in constructor.fields %}
    {{ field.attr }} : {{ field.typ }}
{% endfor %}
    """
    )
    code : str = tmpl.render(
        constructor = constructor
    )
    return code 

def generate_union(
    type_name : str,
    constructors : list[Constructor] 
) -> str:
    handlers_name = f"{inflection.camelize(type_name)}Handlers"

    tmpl = jinja_env.from_string(
"""
# type {{ type_name }}
@dataclass
class {{ type_name }}(ABC):
    @abstractmethod
    def _match(self, handlers : {{ handlers_name }}[T]) -> T: pass


# constructors for type {{ type_name }}
{% for constructor in constructors %}

@dataclass
class {{ constructor.name }}({{ type_name }}):
{% for field in constructor.fields %}
    {{ field.attr }} : {{ field.typ }}
{% endfor %}

    def _match(self, handlers : {{ handlers_name }}[T]) -> T:
        return handlers.case_{{ constructor.name }}(self)


def make_{{ constructor.name }}(
{% for field in constructor.fields %}
    {{ field.attr }} : {{ field.typ }}{% if not loop.last %},{% endif %}

{% endfor %}
) -> {{ type_name }}:
    return {{ constructor.name }}(
{% for field in constructor.fields %}
        {{ field.attr }}{% if not loop.last %},{% endif %}

{% endfor %}
    )

{% endfor %}

# case handlers for type {{ type_name }}
@dataclass
class {{ handlers_name }}(Generic[T]):
{% for constructor in constructors %}
    case_{{ constructor.name }} : Callable[[{{ constructor.name }}], T]
{% endfor %}


# matching for type {{ type_name }}
def match_{{ type_name }}(o : {{ type_name }}, handlers : {{ handlers_name }}[T]) -> T :
    return o._match(handlers)
"""
    )
    code : str = tmpl.render(
        type_name = type_name, 
        constructors = constructors,
        handlers_name = handlers_name
    )
    return code 


