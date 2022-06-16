from __future__ import annotations

from collections.abc import Sequence
from typing import overload

@overload
def foo(input_: int) -> int:
    ...

@overload
def foo(input_: Sequence[int]) -> list[int]:
    ...

def foo(input_: int | Sequence[int]) -> int | list[int]:
    if isinstance(input_, Sequence):
        return [2]
    return 2


x : int = foo(4)
ys : list[int] = foo([1,2,3])