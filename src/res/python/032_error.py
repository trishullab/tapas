from typing import Protocol
class A(Protocol):
    def uno(self) -> int: ... 
    def dos(self) -> int: ... 

A()