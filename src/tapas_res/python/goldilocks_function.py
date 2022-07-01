from typing import TypeVar, Callable, Any, Tuple
T = TypeVar('T')


def pair(x : T) -> Callable[[T], Tuple[T, T]]:
    return lambda y : (y, x)

def plus(x : int) -> Callable[[int], int]:
    return lambda y : x + y

pair_k = pair("hi")
(hi, five) = pair_k(5)

int_pair_k  : Callable[[int], Tuple[int, int]] = pair(1)
(one, five) = int_pair_k(5)