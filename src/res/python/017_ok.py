class A:
    def id(self, x : int) -> int:
        return x


def foo() -> int:
    a = A()
    return a.id(4) 


