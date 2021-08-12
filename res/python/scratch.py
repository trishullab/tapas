def foo(x : int):
    return [
        x + y 
        for y in [1,2,3,4,5,6,7,8][0:3:3]
        if y < 5
    ]