from functools import partial
from typing import Callable, Any

from dataclasses import dataclass
from tree_sitter import Language
import tree_sitter
import ast
import json
from typing import Iterator, Optional

from lib import generic_tree

from lib import python_abstract_token
# from lib.generic_tree import GenericNode


# def run_concrete(concrete : str):
#     mod = None
#     try:
#         mod = python_ast.parse(concrete)
#     except python_ast.ConcreteParsingError:
#         pass
#     else:
#         assert mod
#         python_ast.assert_serialize_reconstitute_bidirectional(mod)
#         python_ast.assert_concretize_parse_bidrectional(mod)


# from lib import util
# import os
# dirpath = util.project_path("res/test/python/concrete_data")

# def test_cubert():
#     return util.run_jsonl_file(os.path.join(dirpath, "cubert_583.jsonl"), run_concrete)


from lib import python_ast
from lib.abstract_token_construct_autogen import Vocab, abstract_token
from lib.python_abstract_token import concretize, dump, analyze, Client
from lib.abstract_token import abstract_token
from lib.python_analysis import Inher, from_Inher_to_string
from typing import Union
import lib.abstract_token
from lib.util import project_path

@dataclass
class Generator:
    run_next : Callable[[], None]
    run_n :Callable[[int], None]  
    run_all : Callable[[], None]

from lib.abstract_token import Vocab
from lib import python_generic_tree
from lib import python_ast_parse

def make_generator(code : str) -> Generator:
    print("--------source code----------")
    print(code)
    print("------------------")

    gnode = python_generic_tree.parse(code)

    # print("--------generic tree dump----------")
    # print(python_generic_tree.dump(gnode))
    # print("------------------")

    mod = python_ast_parse.from_generic_tree(gnode)

    abstract_tokens = python_ast.serialize(mod)

    # print("--------ast dump----------")
    # d = python_abstract_token.dump(abstract_tokens)
    # print(d)
    # print("------------------")

    it = iter(abstract_tokens)

    partial_tokens = () 

    client : Client = analyze()
    iattr : Inher = client.init_inher
    token = None
    print(from_Inher_to_string(iattr))
    print("***")

    def run_next() -> bool :
        nonlocal partial_tokens
        nonlocal iattr 
        nonlocal token 
        token = next(it, None)
        if (not token):
            return True

        partial_tokens += tuple([token])
        print(lib.abstract_token.to_string(token))
        print("---")

        print(concretize(partial_tokens))
        print("###")

        iattr_or_ex = client.next(token)
        if isinstance(iattr_or_ex, Exception):
            ex = iattr_or_ex
            raise ex
        else:
            iattr = iattr_or_ex
            print(from_Inher_to_string(iattr))
            print("***")
            return False 

    def run_all():
        done = run_next()
        while not done:
            done = run_next()

    def run_n(n : int):
        done = run_next()
        n -= 1
        while not done and n > 0 :
            done = run_next()
            n -= 1
    
    return Generator(lambda : (run_next(), None)[-1], run_n, run_all) 


# def new_gen():
#     return make_generator(f'''
# def foo():
#     a = 1
#     a += 2
#     b : int
#     for d in [1,2, a]:
#         b = d

#     return (a, b)

# (x, y) = foo()

# x += 1

# z : int

# z = 1

# z + y
#     ''')

# def new_gen():
#     return make_generator(f'''
# a = 3
# e = 4
# def foo(a : int, b, c):
#     e : int
#     for d in [1,2, a]:
#         e = d 
#         e += a * b + c

#     return (a, e)

# (x, y) = foo(4, 7, 8)
#     ''')

# def new_gen():
#     return make_generator(f'''
# a = 3
# e = 4
# def foo(a : int, b, c):
#     return (a, b)

# (x, y) = foo(4, 7, 8)
#     ''')

# def new_gen():
#     return make_generator(f'''
# try:
#     raise BExcpetion("hello")
# except (y := BExcpetion) as x:
#     print(x)
#     print(y)
#     ''')

# def new_gen():
#     return make_generator(f'''
# a = 1
# class A:
#     a = a + 1 
#     def foo():
#        return 

#     def boo(self, n):
#         return n + a

# x = A().a
#     ''')



# def new_gen():
#     return make_generator(f'''
# import os

# def write(dirpath : str, fname : str, code : str, append : bool = False):
#     if not os.path.exists(dirpath):
#         os.makedirs(dirpath)

#     fpath = os.path.join(dirpath, fname)

#     with open(fpath, 'a' if append else 'w') as f:
#         f.write(code)
#     ''')

# def new_gen():
#     return make_generator(f'''
# if (x := (z := "59293"), False)[-1]:
#     q = (x, z) 
# else:
#     w = (x, z) 

# import os


# for ooga in (xs := [1, 2, 3]):
#     l = 2
#     print(xs)
#     print(ooga)

# print(xs)

# def write(dirpath : str, fname : str, code : str, append : bool = False):
#     if not os.path.exists(dirpath):
#         os.makedirs(dirpath)

#     fpath = os.path.join(dirpath, fname)

#     with (g := open(fpath, 'a' if append else 'w')) as f:
#         f.write(code)

#     d = g
#     e = f

# (y := x, z)
#     ''')

def new_gen():
    with open(project_path("res/cubert/concrete_data/example.py")) as f:
        return make_generator(f.read())

# def new_gen():
#     return make_generator(f'''
#     print("hello"), print("bye") 
#     ''')

if __name__ == "__main__":
    gen = new_gen()
    gen.run_all()
