
x = 4
def foo():
    x = "hello"
    y = 4
    def goo():
        nonlocal y
        global x
        print(f"global x {x}")
        y+=1

    def boo():
        nonlocal y
        x = 5
        # nonlocal x
        print(f"nonlocal x {x}")
        y+=1

    goo()
    boo()

foo()

# conclusion: for renaming need three maps for renaming: global_map, nonlocal_map, and local_map
# nonlocal_map and local_map must be separate to avoid introducing a fresh variable with each assignment inside of a loop or condition. 
# only the first assignment per variable of the local scope introduces a fresh variable.