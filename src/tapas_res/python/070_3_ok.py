from typing import TypeVar, Generic

X = TypeVar("X")

class A(Generic[X]):
    def __init__(self, x : X):
        pass

a = A(1)
pass
