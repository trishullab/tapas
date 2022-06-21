def foo(**kwparams : int):
    return kwparams.keys()
tt = foo(a = 2, b = "hello")
pass