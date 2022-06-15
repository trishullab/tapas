from __future__ import annotations

from collections.abc import Sequence
from typing import overload


@overload
def double(input_: int) -> int:
    ...

@overload
def double(input_: Sequence[int]) -> list[int]:
    ...

def double(input_: int | Sequence[int]) -> int | list[int]:
    if isinstance(input_, Sequence):
        return [i * 2 for i in input_]
    return input_ * 2


x : int = double(4)
ys : list[int] = double([1,2,3])