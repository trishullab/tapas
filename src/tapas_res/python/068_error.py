class A():
    def foo(self, x : int) -> int:
        return x

    pass

class B():

    def foo(self, x : str) -> str:
        return x
    pass


class C(A, B): pass


x = C()

x.foo("hello")