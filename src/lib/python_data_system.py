
from regex import W
from tree_sitter import Language

import logging
import os
import pathlib
import tree_sitter
import json


from pyrsistent import pset

from base.abstract_token_construct_autogen import AbstractTokenHandlers, match_abstract_token, Vocab
from lib import generic_tree_system

from lib import python_abstract_token_system

from lib.python_ast_parse import Obsolete, Unsupported
from lib import python_ast_system
from base.util_system import write, project_path


from base import abstract_token_system as ats
from base.abstract_token_system import Vocab
from lib import python_aux_system as pals 
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

def inc_key(map : PMap[str, int], error_key) -> PMap[str, int]:
    if error_key in map:
        return map + pmap({error_key : map[error_key] + 1}) 
    else:
        return map + pmap({error_key : 1}) 

def generate_file(
    package : PMap[str, pals.ModulePackage], 
    dirname : str, 
    name : str, 
    vocab : dict, 
    dir_count : int
) -> dict[str, Any]:

    count_map : PMap[str, int] = m() 

    concrete_data_dirpath = project_path(f"res/{dirname}/{concrete_dir_name}")

    logging.basicConfig(level=logging.INFO)

    concrete_data_path = os.path.join(concrete_data_dirpath, name)

    abstract_data_base = name.split(".")[0]  

    abstract_data_dirpath = project_path(f"res/{dirname}/abstract_data_{dir_count}")
    write(abstract_data_dirpath, f'{abstract_data_base}.jsonl', '')

    from datetime import datetime

    start = datetime.now()

    with open(concrete_data_path, 'r') as f:
        br = ""
        line = f.readline()
        while line: 
            partial_program = []
            try:

                line_obj = json.loads(line)

                source_code = line_obj['code']

                if len(source_code) > 50000:
                    raise BigCodeError(len(source_code))

                tree = generic_tree_system.parse('python', source_code, 'utf8')

                mod = python_ast_system.parse_from_generic_tree(tree)

                abstract_tokens = python_ast_system.serialize(mod)

                client : pals.Client = pals.spawn_analysis(package, "main",
                    checks=pset()
                    # checks=pals.all_checks.remove(pals.DeclareCheck())
                )

                atok = client.init_prim
                abstract_program_data = [atok]

                for tok in abstract_tokens:
                    partial_program.append(tok)
                    abstract_program_data.append(ats.to_primitive(tok))

                    inher = client.next(tok)

                    new_atok = pals.from_inher_aux_to_primitive(inher)
                    if (new_atok != atok):
                        abstract_program_data.append(new_atok)
                        atok = new_atok


                content = br + json.dumps(abstract_program_data)
                if content.strip():
                    write(abstract_data_dirpath, f'{abstract_data_base}.jsonl', content, append=True)

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
                
                count_map = inc_key(count_map, 'processed')

            except Exception as ex:
                count_map = inc_key(count_map, error_to_string(ex))
                count_map = inc_key(count_map, 'total_error')

                # if isinstance(ex, pals.IterateTypeError):
                #     print(f"")
                #     print(f"** ERROR index: {count_map.get('total')}")
                #     line_obj = json.loads(line)
                #     source_code = line_obj['code']
                #     print(f"** ERROR source code:\n{source_code}")
                #     print(f"** ERROR index: {count_map.get('total')}")
                #     print("** partial_program **")
                #     print(python_abstract_token_system.concretize(tuple(partial_program)))
                #     print("*********************")
                #     print(f"")
                #     raise ex

            # update
            br = "\n"
            line = f.readline()
            count_map = inc_key(count_map, 'total')
            print(f"")
            print(f"total_count : {count_map['total']}")
            print(f"")
            
        #endwhile

    end = datetime.now()


    stats_cm : PMap[str, Any] = count_map 
    stats_supp : PMap[str, Any] = pmap({
        'id' : f"{dirname}//{name}",
        'time': (end - start).total_seconds()
    })
    stats = dict(stats_supp + stats_cm)
    print(f"FILE STATS: {stats}")
    write(abstract_data_dirpath, f'{abstract_data_base}_stats.json', json.dumps(stats))
    return stats


def generate_file_tuple(tup) -> dict[str, Any]:
    stats = generate_file(tup[0], tup[1], tup[2], tup[3], tup[4])
    return stats

def generate_dir(package : PMap[str, pals.ModulePackage], dirname : str):
    concrete_data_dirpath = project_path(f"res/{dirname}/{concrete_dir_name}")
    vocab : dict[str, set[str]] = {}

    concrete_data_file_names : list[str] = sorted(os.listdir(concrete_data_dirpath))
    cdpl = len(concrete_data_file_names)
    stepsize = 50 
    chunks = [concrete_data_file_names[i:i + stepsize] for i in range(0, cdpl, stepsize)]
    for i, chunk in enumerate(chunks):

        # skip chunks
        # if i in [0]: continue 

        abstract_data_dirpath = project_path(f"res/{dirname}/abstract_data_{i}")
        write(abstract_data_dirpath, f'vocab.json', '')
    
        cpu_count = int(min(multiprocessing.cpu_count()/2, 8))
        with multiprocessing.Pool(cpu_count) as pool:
            stats_collection = pool.map(generate_file_tuple, [(package, dirname, n, vocab, i) for n in chunk])

        stats = {} 
        for next_stats in stats_collection:

            for k, v in next_stats.items():
                if k == "id":
                    pass
                elif k in stats:
                    stats[k] = stats[k] + v
                else:
                    stats[k] = v
            
        print(f"DIR STATS: {stats}")
        write(abstract_data_dirpath, f'z_stats.json', json.dumps(stats))

        write(abstract_data_dirpath, f'vocab.json', json.dumps(
            {
                k:list(v)
                for k,v in vocab.items()
            },
            indent=4
        ), append=True)