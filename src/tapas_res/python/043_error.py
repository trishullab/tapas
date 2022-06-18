def foo():
    return (
        y := x + 1,
        x := 4,
        (x, y)
    )