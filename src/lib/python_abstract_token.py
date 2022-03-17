from __future__ import annotations
from typing import Iterator

from lib.abstract_token import abstract_token 
import lib.abstract_token

from lib.python_ast_construct_autogen import * 
from lib.abstract_token_construct_autogen import abstract_token, Grammar

from lib.python_util import Inher
from lib import python_util

from pyrsistent import s, m, pmap, v
from typing import Iterator
from pyrsistent.typing import PMap 

import threading
from queue import Queue

from lib import python_abstract_token_analyze
from lib.python_abstract_token_analyze import Server
from lib.python_util_construct_autogen import LocalEnvSynth


from lib import python_schema

def dump(instances : tuple[abstract_token, ...]):
    return lib.abstract_token.dump(python_schema.rule_map, instances)

def concretize(instances : tuple[abstract_token, ...]):
    return lib.abstract_token.concretize(python_schema.rule_map, instances)


@dataclass
class Client: 
    init_inher : Inher
    next : Callable[[abstract_token], Union[Inher, Exception]]
    close : Callable[[], None]

def analyze() -> Client:

    in_stream : Queue[abstract_token] = Queue()
    out_stream : Queue[Union[Exception, Inher]] = Queue()

    server : Server = Server(in_stream, out_stream)
    inher = Inher(
        global_env = m(), 
        nonlocal_env = m(), 
        local_env = m(),
        module_env = m(),
        mode = python_util.ModuleMode() 
    )


    def run():
        try:
            nonlocal inher
            synth = server.analyze_module(inher)
            assert isinstance(synth, LocalEnvSynth) 

            inher = Inher(
                mode = python_util.ModuleMode(),
                local_env = m(),
                nonlocal_env = m(), 
                global_env = m(), 
                module_env = m(
                my_module = f"{synth.additions}"  
                )
            )
            server.next(inher)
        except Exception as ex:
            out_stream.put(ex)


    thread = threading.Thread(target = run)
    thread.start()

    def next(tok : abstract_token) -> Union[Inher, Exception]:
        in_stream.put(tok) 
        return out_stream.get() 

    def close() -> None:
        tok : abstract_token = Grammar("done", "Done")
        in_stream.put(tok)


    attr_0 = out_stream.get()
    assert isinstance(attr_0, Inher)   

    client = Client(attr_0, next, close)


    return client 