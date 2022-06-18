def foo():
    global x
    x += 1
    return x

def goo():
    x()
    return x


x = 1