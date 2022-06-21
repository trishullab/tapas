def foo(a = 2, *xs : int, y : int, z : int):
    return (a,) + xs + (y,z)

foo(2, 3, 4, y =1, z = 3)
foo(a = 2, y =1, z = 3)