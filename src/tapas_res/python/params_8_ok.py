def foo(p, /, a = 2, *, y : int, z : int):
    return (a,) + (y,z)

foo(1, 2, y =1, z = 3)
foo(1, a = 2, y =1, z = 3)