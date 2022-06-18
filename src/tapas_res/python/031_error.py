from typing import Protocol
class A(Protocol):
    def uno(self) -> int: ... 
    def dos(self) -> int: ... 


class B():
    def uno(self) -> int: return 1 

class C():
    def dos(self) -> int: return 1 

class D(B): pass


def foo(x : A): return x


foo(D())