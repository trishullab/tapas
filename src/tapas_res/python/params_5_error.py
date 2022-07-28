def foo(a = 2, *xs : int, y : int, z : int):
    return (a,) + xs + (y,z)

foo(4, 2, 3, 4, y =1, z = 3, f = 7)