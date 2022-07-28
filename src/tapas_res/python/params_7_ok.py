def foo(p : float, /, a = 2, *xs : int, y : int, z : int):
    return (p,) + (a,) + xs + (y,z)

foo(1, 2, 3, 4, y =1, z = 3)
foo(1, a = 2, y =1, z = 3)