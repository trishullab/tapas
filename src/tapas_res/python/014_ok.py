def sum(xs : list[int]) -> int:
    total = 0
    for x in xs:
        total = total + x
    return total

def is_even(xs : list[int]) -> bool:
    return sum(xs) % 2 == 0


result : bool = is_even([12,34,23,65,73,74])


