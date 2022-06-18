def foo():
    global x
    x += 1
    return x

def x(): pass
# x = 1