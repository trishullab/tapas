def foo(**kwparams : int):
    return kwparams.keys() 
aa = {'a': 2, 'b': 4}
tt = foo(**aa)
pass
