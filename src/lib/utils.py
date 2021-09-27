from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, TypeVar, Any, Generic, Union, Optional
from collections.abc import Callable

from abc import ABC, abstractmethod

T = TypeVar('T')

X = TypeVar('X')


def fail(msg : str):
    raise Exception(msg)

def map_option(f : Callable[[T], X], o : Optional[T]) -> Optional[X]:
    return f(o) if o != None else None

def match_d(k : T, d : dict[T, Callable[[], Any]], error_msg):
    return d.get(k, lambda: fail(error_msg))()
