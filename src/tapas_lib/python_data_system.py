from regex import W
from tree_sitter import Language

import logging
import os
import pathlib
import tree_sitter
import json


from pyrsistent import pset

from tapas_base.abstract_token_construct_autogen import AbstractTokenHandlers, abstract_token, match_abstract_token, Vocab
from tapas_lib import generic_tree_system

from tapas_lib import python_abstract_token_system

from tapas_lib.python_ast_parse import Obsolete, Unsupported
from tapas_lib import python_ast_system
from tapas_base.util_system import write, project_path


from tapas_base import abstract_token_system as ats
from tapas_base.abstract_token_system import Vocab
from tapas_lib import python_aux_system as pals 
from typing import Any, Union
import multiprocessing


class BigCodeError(Exception):
    pass


concrete_dir_name = "concrete_data"

from pyrsistent.typing import PMap


def error_to_string(err : Exception) -> str:

    if isinstance(err, RecursionError):
        return "recursion_error"
    elif isinstance(err, BigCodeError):
        return "big_code_error"
    elif isinstance(err, Obsolete):
        return "obsolete_error"
    elif isinstance(err, Unsupported):
        return "unsupported_error"
    elif isinstance(err, pals.ApplyArgTypeCheck):
        return "apply_arg_type_error"
    elif isinstance(err, pals.IterateTypeCheck):
        return "iterate_type_error"
    elif isinstance(err, AssertionError):
        return "assertion_error"

    else:
        return f"{err}"


from pyrsistent.typing import PMap
from pyrsistent import pmap, m

from typing import Iterable, Sequence

def inc_key(map : PMap[str, int], error_key) -> PMap[str, int]:
    if error_key in map:
        return map + pmap({error_key : map[error_key] + 1}) 
    else:
        return map + pmap({error_key : 1}) 

def add_semantic_data(abstract_tokens : Sequence[abstract_token],  package : PMap[str, pals.ModulePackage]):

    client : pals.Client = pals.spawn_analysis(package, "main",
        checks=pset()
        # checks=pals.all_checks.remove(pals.DeclareCheck())
    )

    atok = client.init_prim
    abstract_program_data = [atok]

    for tok in abstract_tokens:
        abstract_program_data.append(ats.to_primitive(tok))

        inher = client.next(tok)

        new_atok = pals.from_inher_aux_to_primitive(inher)
        if (new_atok != atok):
            abstract_program_data.append(new_atok)
            atok = new_atok

    client.kill(Exception())
    return abstract_program_data


def write_data(
    abstract_data_dirpath : str, 
    file_name : str, 
    data : Iterable,
) -> PMap[str, int]:

    count_map : PMap[str, int] = m() 

    write(abstract_data_dirpath, file_name, '')
    br = ""
    for data_gen in data:
        try:

            content = br + json.dumps(data_gen())
            if content.strip():
                write(abstract_data_dirpath, file_name, content, append=True)

            count_map = inc_key(count_map, 'processed')

        except Exception as ex:
            content = br + json.dumps([])
            write(abstract_data_dirpath, file_name, content, append=True)
            count_map = inc_key(count_map, error_to_string(ex))
            count_map = inc_key(count_map, 'total_error')


        # update
        br = "\n"
        count_map = inc_key(count_map, 'total')
        print(f"")
        print(f"programs processed in file: {count_map.get('processed', 0)}/{count_map.get('total', 0)}")
        print(f"")

    return count_map


def generate_file(
    package : PMap[str, pals.ModulePackage], 
    dirname : str, 
    name : str, 
    vocab : dict, 
    abstract_dir_name : str
) -> tuple[dict[str, Any], dict]:

    count_map : PMap[str, int] = m() 

    concrete_data_dirpath = project_path(f"tapas_res/{dirname}/{concrete_dir_name}")

    logging.basicConfig(level=logging.INFO)

    concrete_data_path = os.path.join(concrete_data_dirpath, name)

    abstract_data_base = name.split(".")[0]  

    abstract_data_dirpath = project_path(f"tapas_res/{dirname}/{abstract_dir_name}")
    write(abstract_data_dirpath, f'{abstract_data_base}.jsonl', '')

    from datetime import datetime

    start = datetime.now()

    def code_gen():
        nonlocal vocab
        with open(concrete_data_path, 'r') as f:
            for line in f: 
                def data_gen(): 
                    line_obj = json.loads(line)
                    source_code : str = line_obj['code']

                    if len(source_code) > 50000:
                        raise BigCodeError(len(source_code))

                    abstract_tokens = python_ast_system.serialize(python_ast_system.parse(source_code))

                    def handle_Vocab(o : Vocab):
                        if o.options in vocab.keys():
                            vocab[o.options].add(o.selection)
                        else:
                            vocab[o.options] = {o.selection}

                    # update vocabulary
                    for inst in abstract_tokens:

                        match_abstract_token(inst, AbstractTokenHandlers(
                            case_Grammar=lambda _ : (),
                            case_Vocab=handle_Vocab,
                            case_Hole=lambda _ : () 
                        )) 

                    return add_semantic_data(abstract_tokens, package)
                yield data_gen

    count_map = write_data(abstract_data_dirpath, f'{abstract_data_base}.jsonl', code_gen())

                
    end = datetime.now()


    stats_cm : PMap[str, Any] = count_map 
    stats_supp : PMap[str, Any] = pmap({
        'id' : f"{dirname}//{name}",
        'time': (end - start).total_seconds()
    })
    stats = dict(stats_supp + stats_cm)
    print(f"FILE STATS: {stats}")
    write(abstract_data_dirpath, f'{abstract_data_base}_stats.json', json.dumps(stats))
    return stats, vocab


def generate_file_tuple(tup) -> tuple[dict[str, Any], dict]:
    stats, vocab = generate_file(tup[0], tup[1], tup[2], tup[3], tup[4])
    return stats, vocab

def generate_dir(package : PMap[str, pals.ModulePackage], dirname : str, suffix = ""):
    concrete_data_dirpath = project_path(f"tapas_res/{dirname}/{concrete_dir_name}")
    vocab : dict[str, set[str]] = {}

    concrete_data_file_names : list[str] = sorted(os.listdir(concrete_data_dirpath))
    cdpl = len(concrete_data_file_names)
    stepsize = 50 
    chunks = [concrete_data_file_names[i:i + stepsize] for i in range(0, cdpl, stepsize)]
    for i, chunk in enumerate(chunks):

        # skip chunks
        # if i in [0]: continue 
        abstract_dir_name = (
            f"abstract_data_{suffix}_{i}"
            if suffix else
            f"abstract_data_{i}"
        ) 
        # abstract_data_{dir_count}

        abstract_data_dirpath = project_path(f"tapas_res/{dirname}/{abstract_dir_name}")
        # write(abstract_data_dirpath, f'vocab.json', '')
    
        # multi processor:
        stats_vocab_collection = []
        cpu_count = int(min(multiprocessing.cpu_count() * 3/4, 8))
        with multiprocessing.get_context('spawn').Pool(cpu_count) as pool:
            stats_vocab_collection = pool.map(generate_file_tuple, [(package, dirname, n, vocab, abstract_dir_name) for n in chunk])

        # #single processor:
        # for n in chunk: 
        #     stats, vocab = generate_file(package, dirname, n, vocab, abstract_dir_name)
        #     stats_vocab_collection.append((stats, vocab))


        stats = {} 
        for next_stats, next_vocab in stats_vocab_collection:

            for k, v in next_stats.items():
                if k == "id":
                    pass
                elif k in stats:
                    stats[k] = stats[k] + v
                else:
                    stats[k] = v
            
            vocab.update(next_vocab) 
            
        print(f"DIR STATS: {stats}")
        write(abstract_data_dirpath, f'z_stats.json', json.dumps(stats))

        # write(abstract_data_dirpath, f'vocab.json', json.dumps(
        #     {
        #         k:list(v)
        #         for k,v in vocab.items()
        #     },
        #     indent=4
        # ), append=True)