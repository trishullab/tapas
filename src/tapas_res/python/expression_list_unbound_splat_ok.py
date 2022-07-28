from typing import Any
def foo() -> list[Any]: ...
g : list[Any] = foo()

x, y, z = 3, *g
pass
x, y, z = *g, 3
pass
x, y, z = *g, 3, *g
pass