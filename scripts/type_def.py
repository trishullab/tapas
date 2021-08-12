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



def to_field(thing : tuple[str, str]) -> Field:
    (attr, type_) = thing
    return Field(attr, type_)

def to_shape(thing : tuple[str, list[tuple[str, str]]]) -> Shape:
    (shape_name, field_things) = thing
    case_name = f"case_{shape_name}"
    return Shape(shape_name, case_name, list(map(to_field, field_things)))

def to_shape_list(things : list[tuple[str, list[tuple[str, str]]]]) -> list[Shape]:
    return list(map(to_shape, things))


def generate_type_intersection_def(
    name : str,
    intersection :  list[tuple[str, str]] 
) -> str:
    fields = list(map(to_field, intersection))

    tmpl = jinja_env.from_string(intersection_template_str)
    code : str = tmpl.render(
        name=name, 
        fields=fields
    )
    return code 

def generate_type_union_def(
    type_name : str,
    union : list[tuple[str, list[tuple[str, str]]]] 
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


