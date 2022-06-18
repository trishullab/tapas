class A:
    def x(self) -> int:
        return 1

    def y(self) -> int:
        return 2



class B(A):
    def x(self) -> int:
        return 3

    def y(self) -> int:
        return 4


sum = 0
for a in [A(), B()]:
    sum = sum + a.x() + a.y()


