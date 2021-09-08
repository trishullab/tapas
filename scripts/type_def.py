"""Generate multiple files from template."""
from __future__ import annotations

from dataclasses import dataclass

import inflection
import jinja2


header = """
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, TypeVar, Any, Generic, Union, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod

T = TypeVar('T')
"""

intersection_template_str = """
# type and constructor {{ name }}
@dataclass
class {{ name }}:
{% for field in fields %}
    {{ field.attribute }} : {{ field.type }}
{% endfor %}
"""

union_template_str = """
# type {{ type_name }}
@dataclass
class {{ type_name }}(ABC):
    @abstractmethod
    def _match(self, handlers : {{ handlers_name }}[T]) -> T: pass


# constructors for type {{ type_name }}
{% for shape in shapes %}
@dataclass
class {{ shape.name }}({{ type_name }}):
{% for field in shape.fields %}
    {{ field.attribute }} : {{ field.type }}
{% endfor %}

    def _match(self, handlers : {{ handlers_name }}[T]) -> T:
        return handlers.{{ shape.case_name }}(self)

{% endfor %}

# case handlers for type {{ type_name }}
@dataclass
class {{ handlers_name }}(Generic[T]):
{% for shape in shapes %}
    {{ shape.case_name }} : Callable[[{{ shape.name }}], T]
{% endfor %}


# matching for type {{ type_name }}
def match_{{ type_name }}(o : {{ type_name }}, handlers : {{ handlers_name }}[T]) -> T :
    return o._match(handlers)
"""

jinja_env = jinja2.Environment(trim_blocks=True)

@dataclass
class Field:
    attribute: str
    type: str

@dataclass
class Shape:
    name : str
    case_name : str
    fields : list[Field]



def to_field(attr : str, type_ : str) -> Field:
    return Field(attr, type_)

def to_shape(shape_name, field_things : dict[str, str]) -> Shape:
    case_name = f"case_{shape_name}"

    fields = [
        Field(k, v) 
        for k, v in field_things.items()
    ]
    return Shape(shape_name, case_name, fields)

def to_shape_list(things : dict[str, dict[str, str]]) -> list[Shape]:
    return [
        to_shape(name, field_things)
        for name, field_things in things.items()
    ]


def generate_type_intersection_def(
    name : str,
    intersection :  dict[str, str] 
) -> str:
    fields = [
        Field(k, v) 
        for k, v in intersection.items()
    ]
    
    tmpl = jinja_env.from_string(intersection_template_str)
    code : str = tmpl.render(
        name=name, 
        fields=fields
    )
    return code 

def generate_type_union_def(
    type_name : str,
    union : dict[str, dict[str, str]] 
) -> str:
    shapes = to_shape_list(union)
    handlers_name = f"{inflection.camelize(type_name)}Handlers"
    tmpl = jinja_env.from_string(union_template_str)
    code : str = tmpl.render(
        type_name=type_name, 
        shapes=shapes,
        handlers_name=handlers_name
    )
    return code 


