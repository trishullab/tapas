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

    codes = [
        '''
    def foo():
        return (
            #hello
            1 
            #hello
            )
        ''',

        '''
    x = (#first
        1 #hello
        #hello
        + #hello
        3 #last
    )
        ''',

        '''
    (#hello A
        1 #hello B
        , #hello C
        2 #hello D
        #hello E 
    ) #hello F
        ''',

        '''
    (not # hello A
        True # hello B
        # hello C
    )
        ''',

        '''
    def foo( #foo
    x #foo
    : int):
        return x

    foo( # hello A
        x #foo
        = #foo
        1 #hello B
        #hello C
    )
        ''',

        '''
    def foo( #foo
    x #foo
    : int):
        return x

    xs = {'x' : 1}
    foo( #hello
        ** #hello
        xs #hello
    )
        ''',

        '''
    def foo(x : int):
        return x

    foo( # hello A
        1 #hello B
        #hello C
    )
        ''',


        '''
    (# hello A
        0 #hello B
    if # hello C
    True # hello D
    else  # hello E
        1 #hello F
        #hello G 
    )
        ''',

        '''
    try: #hello
        pass #llo
    except Exception:
        pass #hello
    else:
        pass #hello
        ''',

        '''
    try: #hello
        pass #llo
    except Exception: #hello
        pass #hello
    else: #hello
        pass #hello
    finally: #hello
        pass #hello
        ''',

        '''
    x = 0
    if True: # comment after if
        # another comment
        x = 0 # comment 
        # comment
        x = x + 1
    elif False: # comment after elif
        x = 0 # comment 
        # comment
        x = x + 1
    else: # comment after else
        x = 0 # comment 
        # comment
        x = x + 1
        ''',

        '''
    def foo(x):
        return x
    @foo #hello
    # between decorators 
    @foo #bye
    class A: # this is a class header comment 
        pass
        ''',

        '''
    def foo(x : int): # this is a function header comment 
        # whole line comment 0 
        y = x + 1 # comment after stmt
        z = y + 1 
        # whole line comment 1 
        ''',

        '''
    { #hello
        'x' #hello
        : #hello 
        1 #hello
        , #hello
        'y' #hello
        : #hello 
        1 #hello
    } #hello
        ''',

        '''
    (True  #hello
    or #hello
    False #hello
    )
        ''',

        '''
    (x #hello
    := #hello 
    1)
        ''',


        '''
    (lambda #hello
    x #foo
    : #hello
    1)
        ''',

        '''
    [ #hello
        x # hello
        for # hello
        x #hello
        in #hello
        [1,2,3] #hello
        if #hello 
        1 == 1 #hello
        if #hello 
        True #hello
    ]
        ''',

        '''
    { #hello
        1 #hello
        : #hello
        x #hello
        for # hello
        x #hello
        in #hello
        [1,2,3] #hello
        if #hello 
        1 == 1 #hello
        if #hello 
        True #hello
    }
        ''',

        '''
    async def foo():
        return 1
    async def boo():
        x = (await #comment
        foo())
        ''',

        '''
    def foo():
        (yield #x 
        from #x
        [2,3,4] #x
        )
        (yield #x
        1 #x
        )
        ''',

        '''
    def foo():
        (yield #hello
        )
        ''',


        '''
    (1 #x
    < #x
    2 < #x
    3 # x
    )
    (1 not #hello
    in #hello
    [2,3]
    )
        ''',

        '''
    def foo(x = 1):
        return

    (foo #x
    ())

    (foo #x
    (1))
    '''

    '''
    class A:
        x = 1
    (A # hello
    . #hello
    x #hello
    ) 
        ''',

        '''
    (
        x[1,2]
    )
        ''',

        '''
    x = [1,2,3,4]
    (
        x #hello
        [ #hello
        0 # hello
        : #hello
        1 #hello
        : #hello
        2 #hello
        ]
    )
        ''',

        '''
    class A: pass
    class B(
        #hello
    ): pass
    class C( #hello
        A #hello
        , #hello
        B #hello
    ) : pass
        ''',

        '''
    def foo(
        #hello
        * #hello
        xs #hello
        : #hello
        int #hello
    ):
        return
        ''',

        '''
    def foo(
        #hello
        ** #hello
        xs #hello
        : #hello
        int #hello
    ):
        return
        ''',

        '''
    def foo(
        #hello
        x #hello
        : #hello
        int #hello
        = #hello
        1 #hello
    ):
        return
        ''',

        '''
    def foo(
        #hello
        x #hello
        = #hello
        1 #hello
    ):
        return
        ''',

        '''
    def foo(
        #hello
        x #hello
        : #hello
        int #hello
    ):
        return
        ''',

        '''
    def foo(x, y, # uno
    ** # mid
    xs # dos
    , z):
        return
        ''',

        '''
    def foo(x, y, # uno
    * # dos
    xs # tre
    , z):
        return
        ''',

        '''
    def foo(x, y, # uno
    * # dos
    , z):
        return
        ''',

        '''
    def foo(x, y, *, z):
        return
        ''',

        '''
    def foo( #hello
        p #hello 
        : #hello
        float#hello
        , #hello
        /#hello
        , #hello
        a #hello
        = #hello
        2#hello
        , #hello
        *#hello
        xs #hello
        : #hello
        int#hello
        , #hello
        y#hello
         : #hello
         int#hello
         , #hello
         z #hello
         : #hello
         int#hello
        ):
        return
        ''',

        '''
    (1,)
        '''

        '''
    y : int 
    x = y
    y = 1
    z = y
        ''',


        '''
    from __future__ import annotations
    from typing import Sequence, Union
    def double(input_: int | Sequence[int]) -> int | list[int]:
        if isinstance(input_, Sequence):
            return [i * 2 for i in input_]
        return input_ * 2
        ''',

        '''
        if True:
            pass
        ''',

        '''
        x, y = pair = 1, 2
        ''',

        '''
    if True: # comment after if
        # another comment
        x = 0 # comment 
        # comment
        x = x + 1 #hello
    #hello
    else: # comment after else
        x = 0 # comment 
        # comment
        x = x + 1
        ''',

        '''
    if True: # comment after if
        # another comment
        x = 0 # comment 
        # comment
        x = x + 1 #hello
    #hello
    elif True: # comment after else
        x = 0 # comment 
        # comment
        x = x + 1
    #hello
    else: # comment after else
        x = 0 # comment 
        # comment
        x = x + 1
    #hello
        ''',

        '''
    for x in []: #hello
        pass #hello
    #hello
    else: #hello
        pass #hello
    #hello
        ''',

        '''
    class A(Exception): pass
    try: #hello
        pass #hello
    #hello
    except A:
        pass #hello
    #hello
    except Exception:
        pass #hello
    #hello
    else:
        pass #hello
    #hello
    finally: #hello
        pass #hello
        ''',

        '''
        xs = [1,2,3]
        xs[1]
        ''',

        '''
        xs = [1,2,3]
        xs[1:]
        ''',
    
        '''
        xs : tuple[()]
        '''
    ]


    for code in codes:
        gnode = pgs.parse(code)
        # print("-- generic node --")  
        # print(pgs.dump(gnode))

        ######
        mod = pas.parse_from_generic_tree(gnode)
        seq = pas.serialize(mod)
        # print("-- AST --")  
        # print(pats.dump(seq))

        assert "HOLE" not in (pats.dump(seq)) 

if __name__ == "__main__":
    test_comment()
    pass