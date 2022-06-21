from typing import TypeVar, Generic

X = TypeVar("X")

def foo(x : X) -> X:
    return x

x = foo(1)
pass
