from typing import Callable, Any
from tapas_base import util_system
from tree_sitter import Language

from tapas_lib import generic_tree_system

from tapas_lib import python_ast_system
from tapas_lib.generic_tree_system import GenericNode


from typing import Callable

from tapas_lib import python_ast_system as pas
from tapas_lib import python_generic_tree_system as pgs 
from tapas_lib import python_abstract_token_system as pats
from tapas_base import abstract_token_system as ats
from tapas_base import util_system as us



def load_source(name : str) -> str:
    path = us.project_path(f"tapas_res/python/{name}.py")
    with open(path, 'r') as f:
        return f.read()


def run_concrete(concrete : str):
    mod = python_ast_system.parse(concrete)
    python_ast_system.assert_serialize_reconstitute_bidirectional(mod)
    python_ast_system.assert_concretize_parse_bidrectional(mod)


import os
dirpath = util_system.project_path("tapas_res/test/python/concrete_data")

def test_cubert():
    return util_system.run_jsonl_file(os.path.join(dirpath, "cubert_583.jsonl"), run_concrete)

def test_source_pointer_increasing():
    code = load_source("example") 
    gnode = pgs.parse(code)
    mod = pas.parse_from_generic_tree(gnode)
    abstract_tokens = pas.serialize(mod)
    last_token = abstract_tokens[0]
    last_index = 0
    i = 0
    for ti, tok in enumerate(abstract_tokens):
        if isinstance(tok, ats.Grammar):
            i = tok.source_start 

        assert i >= last_index
        # print(i)
        # if i < last_index:
        #     print(f"")
        #     print(f"*** regress: {tok} @ {ti}")
        #     print(f"---concretize---\n{pats.concretize(tuple(abstract_tokens[:ti]))}")
        #     print(f"*** prev_tok: {last_token}")
        #     print(f"*** regress: {tok} @ {ti}")
        #     print(f"*** i={i} < last_index={last_index}")
        #     print(f"")
        #     break

        last_token = tok
        last_index = i


def test_comment():

#     code = '''
# def foo():
#     return (
#         #hello
#         1 
#         #hello
#         )
#     '''

#     code = '''
# x = (#first
#     1 #hello
#     #hello
#     + #hello
#     3 #last
# )
#     '''

#     code = '''
# (#hello A
#     1 #hello B
#     , #hello C
#     2 #hello D
#     #hello E 
# ) #hello F
#     ''')


#     code = '''
# (not # hello A
#     True # hello B
#     # hello C
# )
#     '''

    # code = '''
# def foo( #foo
# x #foo
# : int):
#     return x

# foo( # hello A
#     x #foo
#     = #foo
#     1 #hello B
#     #hello C
# )
    # '''

#     code = '''
# def foo(x : int):
#     return x

# foo( # hello A
#     1 #hello B
#     #hello C
# )
#     '''

#################

    code = '''
(# hello A
    0 #hello B
if # hello C
True # hello D
else  # hello E
    1 #hello F
    #hello G 
)
    '''

#     code = '''
# def foo(x : int):
#     return x

# try:
#     foo()
# except Exception(): 
#     foo()
# else:
#     foo()
#     '''

#     code = '''
# x = 0
# if True: # comment after if
#     # another comment
#     x = 0 # comment 
#     # comment
#     x = x + 1
# elif False: # comment after elif
#     x = 0 # comment 
#     # comment
#     x = x + 1
# else: # comment after else
#     x = 0 # comment 
#     # comment
#     x = x + 1
#     '''


#     code = '''

# def foo(x):
#     return x

# @foo #hello
# # between decorators 
# @foo #bye
# class A: # this is a class header comment 
#     pass
#     '''

#     code = '''
# def foo(x : int): # this is a function header comment 
#     # whole line comment 0 
#     y = x + 1 # comment after stmt
#     z = y + 1 
#     # whole line comment 1 
#     '''

    gnode = pgs.parse(code)
    print("-- generic node --")  
    print(pgs.dump(gnode))

    ######
    mod = pas.parse_from_generic_tree(gnode)
    seq = pas.serialize(mod)

    print("-- AST --")  
    print(pats.dump(seq))

if __name__ == "__main__":
    test_comment()
    pass