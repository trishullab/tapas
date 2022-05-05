
from tree_sitter import Language

import logging
import os
import pathlib
import tree_sitter
import json
from lib.abstract_token_construct_autogen import AbstractTokenHandlers, match_abstract_token, Vocab

from lib import generic_tree_system, python_abstract_token_system

from lib.python_ast_parse import Obsolete, Unsupported
from lib import python_ast_system
from lib.util_system import write, project_path


from lib.python_analysis_system import AnalysisError
from lib import abstract_token_system as ats
from lib.abstract_token_system import Vocab
from lib import python_analysis_system as pals 
from typing import Any, Union
import multiprocessing


class BigCodeError(Exception):
    pass


concrete_dir_name = "concrete_data"

from pyrsistent.typing import PMap

def generate_file(
    package : PMap[str, pals.ModulePackage], 
    dirname : str, 
    name : str, 
    vocab : dict, 
    dir_count : int
) -> dict[str, Any]:

    processed_count = 0
    rec_error_count = 0
    big_code_error_count = 0
    obsolete_error_count = 0
    unsupported_error_count = 0
    arg_param_mismatch_error_count = 0
    analysis_error_count = 0
    assertion_error_count = 0
    error_count = 0
    total_count = 0

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

                client : pals.Client = pals.spawn_analysis(package, "main")

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
                
                processed_count += 1

            except RecursionError:
                rec_error_count += 1
                error_count += 1

            except BigCodeError as ex:
                big_code_error_count += 1
                error_count += 1

            except Obsolete as ex:
                obsolete_error_count += 1
                error_count += 1

            except Unsupported as ex:
                unsupported_error_count += 1
                error_count += 1

            except pals.ApplyArgTypeError as ex:
                arg_param_mismatch_error_count += 1
                error_count += 1
            except AnalysisError as ex:
                analysis_error_count += 1
                error_count += 1
                # print(f"")
                # print(f"** ERROR index: {total_count}")
                # line_obj = json.loads(line)
                # source_code = line_obj['code']
                # print(f"** ERROR source code:\n{source_code}")
                # print(f"** ERROR index: {total_count}")
                # print("** partial_program **")
                # print(python_abstract_token_system.concretize(tuple(partial_program)))
                # print("*********************")
                # print(f"")
                # raise ex
            except AssertionError as ex:
                assertion_error_count += 1
                error_count += 1
                # print(f"")
                # print(f"** ERROR index: {total_count}")
                # line_obj = json.loads(line)
                # source_code = line_obj['code']
                # print(f"** ERROR source code:\n{source_code}")
                # print(f"** ERROR index: {total_count}")
                # print("** partial_program **")
                # print(python_abstract_token_system.concretize(tuple(partial_program)))
                # print("*********************")
                # print(f"")
                # raise ex

            except Exception as ex:
                # raise ex
                error_count += 1

            # update
            br = "\n"
            line = f.readline()
            total_count += 1
            
            # print(f"")
            # print(f"total_count: {total_count}")
            # print(f"processed_count: {processed_count}")
            # print(f"")

        #endwhile

    end = datetime.now()


    stats = {
        'id' : f"{dirname}//{name}",
        'time': (end - start).total_seconds(),
        'processed_count' : processed_count,
        'rec_error_count' : rec_error_count,
        'big_code_error_count' : big_code_error_count,
        'obsolete_error_count' : obsolete_error_count,
        'unsupported_error_count' : unsupported_error_count,
        'arg_param_mismatch_error_count' : arg_param_mismatch_error_count,
        'analysis_error_count' : analysis_error_count,
        'assertion_error_count' :  assertion_error_count,
        'error_count' : error_count,
        'total_count' : total_count
    }
    print(f"FILE STATS: {stats}")
    write(abstract_data_dirpath, f'{abstract_data_base}_stats.json', json.dumps(stats))
    return stats


def generate_file_tuple(tup) -> dict[str, Any]:
    stats = generate_file(tup[0], tup[1], tup[2], tup[3], tup[4])
    return stats

def generate_dir(package : PMap[str, pals.ModulePackage], dirname : str):
    concrete_data_dirpath = project_path(f"res/{dirname}/{concrete_dir_name}")
    vocab : dict[str, set[str]] = {}

    concrete_data_file_names = os.listdir(concrete_data_dirpath)
    cdpl = len(concrete_data_file_names)
    stepsize = 50
    chunks = [concrete_data_file_names[i:i + stepsize] for i in range(0, cdpl, stepsize)]
    for i, chunk in enumerate(chunks):

        abstract_data_dirpath = project_path(f"res/{dirname}/abstract_data_{i}")
        write(abstract_data_dirpath, f'vocab.json', '')
    
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        stats_collection = pool.map(generate_file_tuple, [(package, dirname, n, vocab, i) for n in chunk])
        pool.close()
        pool.join()

        time = 0
        processed_count = 0
        rec_error_count = 0
        big_code_error_count = 0
        obsolete_error_count = 0
        unsupported_error_count = 0
        arg_param_mismatch_error_count = 0
        analysis_error_count = 0
        assertion_error_count = 0
        error_count = 0
        total_count = 0

        # print(f"stats_collection length: {len(stats_collection)}")

        for stats in stats_collection:
            time += stats['time']
            processed_count += stats['processed_count']
            rec_error_count += stats['rec_error_count']
            big_code_error_count += stats['big_code_error_count'] 
            obsolete_error_count += stats['obsolete_error_count'] 
            unsupported_error_count += stats['unsupported_error_count'] 
            arg_param_mismatch_error_count += stats['arg_param_mismatch_error_count'] 
            analysis_error_count += stats['analysis_error_count'] 
            assertion_error_count += stats['assertion_error_count'] 
            error_count += stats['error_count'] 
            total_count += stats['total_count'] 

        stats = {
            'id' : f"{dirname}",
            'time' : time,
            'processed_count' : processed_count,
            'rec_error_count' : rec_error_count,
            'big_code_error_count' : big_code_error_count,
            'obsolete_error_count' : obsolete_error_count,
            'unsupported_error_count' : unsupported_error_count,
            'analysis_error_count' : analysis_error_count,
            'error_count' : error_count,
            'total_count' : total_count
        }

        # print(f"DIR STATS: {stats}")
        write(abstract_data_dirpath, f'z_stats.json', json.dumps(stats))

        write(abstract_data_dirpath, f'vocab.json', json.dumps(
            {
                k:list(v)
                for k,v in vocab.items()
            },
            indent=4
        ), append=True)