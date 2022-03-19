
# from __future__ import annotations 


# def even(n : int) -> bool:
#     if n == 0:
#         return True
#     else:
#         return odd(n - 1)

# def odd(n : int) -> bool:
#     if n == 1:
#         return True
#     else:
#         return even(n - 1)


    



# # def split(zs : tuple) -> list[tuple[tuple, tuple]]:
# #     nil = tuple([])
# #     snoc = lambda xs, x : xs + tuple([x])
# #     return (
# #         [(zs, nil)] + 
# #         ([(ys, snoc(xs,hd))
# #           for hd in [zs[-1]]
# #           for zs_tl in [zs[:-1]]
# #           for (ys, xs) in split(zs_tl)
# #          ] if len(zs) > 0 else [])
# #     ) 


# # import json
# # for ys, xs in split((1,2,3,4)):
# #     print(json.dumps(ys) + "     " + json.dumps(xs)) 


# # x = None

# # if x :
# #     print("truthy")
# # else:
# #     print("falsy")


# # from pyrsistent import m, pmap, v

# # # No mutation of maps once created, instead they are
# # # "evolved" leaving the original untouched
# # m1 = m(a=1, b=2)
# # m2 = m1.set('c', 3)
# # m3 = m2.set('a', 5)
# # print(f"ooga: {m1}")
# # print(f"ooga: {m2}")
# # print(f"ooga: {m3}")
# # print(f"ooga: {m3['a']}")


# # from pyrsistent import m, pmap, v
# # from typing import Iterator
# # from pyrsistent.typing import PMap 
# # from lib.instance import instance

# # import threading, queue
# # from queue import Queue
# # q = queue.Queue()

# # def foo(q : Queue[instance], global_env : PMap[str, str], out : Queue[PMap[str, str]]) -> None:
# #     out.put(m())
# #     m() + m()
# #     def p():
# #         Q()
# #     pass

# # class Q:
# #     pass


# # x = 1 + (y := 2) 
# # (x, (y := 2)) = (4, 5) 

# # possible target exprs: tuple, list, or name

# # print (f"ooga x: {x}")
# # print (f"ooga y: {y}")


# from lib.python_ast_construct_autogen import Assign


# x = 4
# y = 5
# class cloo():
#     def __init__(self):
#         self.y = self.foo()

#     def foo(self):
#         def goo():
#             return 2 + y + x

#         return goo()

# def foo():
#     y = 2
#     def goo():
#         nonlocal y
#         (x, y) += 0
#         del y

#     goo()
#     return y

from dataclasses import dataclass


a = 1
b = 2
def foo():
    global a
    global b
    a, c = b = (a + 1 + b, 4)
# y = 3
# (x, y) += 3

# print(f"ooga x: {x}")
# print(f"ooga y: {y}")

# x = 4
# y = 5

# from pyrsistent import m, pmap, v, s
# from typing import Iterator
# from pyrsistent.typing import PMap 

# test = m(x = 1, y = 2, z = 3)

# xs = s('x', 'z')

# print(f"test {test}")


# result = test
# for x in xs:
#     result = result.remove(x)

# print(f"result {result}")

# from typing import Callable

# x : Callable[[int], tuple[int, int]] = lambda x : (x, 1)


# y = 1

# class ooga:
#     def __enter__(self):
#         pass
#     def __exit__(self):
#         pass

# y = ooga()


# def boo():
#     with ooga() as y, (z := ooga()) as x, z as q, x as w:
#         (y, z)


# with open('file_path', 'w') as file, file as f, f as (y, y):
#     file.write('hello world !')



# print("hello.world.ads".split("."))


# from typing import Callable
# class Thing: 

#     def __init__(self):  
#         self.foo : Callable[[], int] = lambda : 4 
#         self.boo : Callable[[int], None] = lambda x : None 

#         self.x = "X" 



# for i in range(0, 10):
#     print(f"asdf {i}")

# x : tuple[int, ...] = tuple([1, 2, 3])


# class A:
#     def __init__(self):
#         self.x = "defined in A" 


#     def goo(self) -> str:
#         return self.foo(A())

#     def foo(self, o : A) -> str:
#         return o.x

# class B(A):
#     def __init__(self):
#         self.x = "(x) defined in B" 
#         self.y = "(y) defined in B" 

#     # def goo(self) -> str:
#     #     return self.foo(self)

#     def foo(self, o : B) -> str:
#         return o.y


# print(f"OOGA: {B().goo()}")



# class BExcpetion(Exception):
#     pass




# try:
#     raise BExcpetion("hello")
# except (y := BExcpetion) as x:
#     print(f"ooga {x} / {y}")


# class Y:
#     a = 1

# class X(Y):
#     a += 4


# x : X = X()

# print(f"OOGA {X.a} / {X().a} / {isinstance(X, X)}")

# a = 1
# class A:
#     a = a + 1 
#     def foo():
#        return 

#     def boo(self, n):
#         return n + a

# A().a

# print()

# import os
# def write(dirpath : str, fname : str, code : str, append : bool = False):
#     if not os.path.exists(dirpath):
#         os.makedirs(dirpath)

#     fpath = os.path.join(dirpath, f"{fname}")

#     with open(fpath, 'a' if append else 'w') as f:
#         # logging.info(f"Writing file: {fpath}")
#         f.write(code)

# if (x := "59293", False)[-1]:
#     print (f"True {x}")
# else:
#     print (f"False {x}")

# import os

# def write(dirpath : str, fname : str, code : str, append : bool = False):
#     if not os.path.exists(dirpath):
#         os.makedirs(dirpath)

#     fpath = os.path.join(dirpath, fname)

#     with open(fpath, 'a' if append else 'w') as f:
#         f.write(code)


# (y := x)

# from lib.zzz import y, x, z, write, l, ooga


# i = [1,2,3,4]
# for n in [0, 2]: 
#     del i[n] 

# print(i)


# thing = "hello\nfriend\n".strip().split("\n")
# print(thing)
# equal = ['hello', 'world'] == ['hello', 'world']
# print(f"equal?: {equal}")


# x = [1,2,3]
# i = 1
# def boo():
#     x[i] += 1 + x[i]

# d = 1

# for x in (y := [1,2,3]):
#     # del d
#     pass


# print(f"hello {d}")


# class B():
#     c : str = "hello"

#     def foo(self) -> int:
#         return 1

# class A():
#     b : B = B()


# def boo():
#     return A()

# a = A()
# del boo().b.c
# del a.b.foo


# def boo(*xs):
#     ys: tuple = xs
#     print(xs)

# boo(1,2,3,4)


def boo():
    return 4
if boo() > 1:
    d = 4 
elif boo() > 2: 
    d = 4 
else:
    d : int 

d = d + 1

