

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, TypeVar, Any, Generic, Union, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod

T = TypeVar('T')



# type and constructor GenericNode
@dataclass
class GenericNode:
    syntax_part : str
    text : str
    children : list[GenericNode]


