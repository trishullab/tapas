
from tree_sitter import Language

import logging
import os
import pathlib
import tree_sitter
import json
from lib.abstract_token_construct_autogen import AbstractTokenHandlers, match_abstract_token, Vocab

from lib import generic_tree

from lib.python_ast_parse import Obsolete, Unsupported
from lib import python_ast
from lib.util import write, project_path
from lib.abstract_token import abstract_token
from lib.abstract_token_construct_autogen import Vocab



from lib.python_abstract_token import concretize, analyze, Client
from lib.python_abstract_token_analyze import AnalysisError
# from lib.abstract_token import abstract_token
from lib.python_util import Inher, from_Inher_to_string
from lib.python_util import Inher, from_Inher_to_dictionary
# from typing import Union
import lib.abstract_token
from typing import Any, Union


class BigCodeError(Exception):
    pass

def generate_file(dirname : str, name : str, vocab : dict) -> dict[str, Any]:

    processed_count = 0
    rec_error_count = 0
    big_code_error_count = 0
    obsolete_error_count = 0
    unsupported_error_count = 0
    analysis_error_count = 0
    error_count = 0
    total_count = 0

    concrete_data_dirpath = project_path(f"res/{dirname}/concrete_data")
    abstract_data_dirpath = project_path(f"res/{dirname}/abstract_data")

    logging.basicConfig(level=logging.INFO)

    concrete_data_path = os.path.join(concrete_data_dirpath, name)

    abstract_data_base = name.split(".")[0]  
    # write(abstract_data_dirpath, f'{abstract_data_base}_training.txt', '')
    write(abstract_data_dirpath, f'{abstract_data_base}.jsonl', '')
    write(abstract_data_dirpath, f'{abstract_data_base}_stats.txt', '')

    from datetime import datetime

    start = datetime.now()

    with open(concrete_data_path, 'r') as f:
        line = f.readline()
        while line: 
            try:

                line_obj = json.loads(line)

                source_code = line_obj['code']

                if len(source_code) > 10 ** 6:
                    raise BigCodeError(len(source_code))

                tree = generic_tree.parse('python', source_code, 'utf8')

                mod = python_ast.parse_from_generic_tree(tree)

                abstract_tokens = python_ast.serialize(mod)

                def triple_from_instance(inst : abstract_token) -> tuple[str, str, str]:
                    return match_abstract_token(inst, AbstractTokenHandlers[tuple[str, str, str]](
                        case_Grammar=lambda o : (
                            ("grammar", o.options, o.selection)
                        ),
                        case_Vocab=lambda o : (
                            ("vocab", o.options, o.selection)
                        )
                    )) 


                client : Client = analyze()
                from lib.python_util import from_env_to_dictionary
                inher : Union[Inher, Exception] = client.init_inher
                atok = ['A', 
                    from_env_to_dictionary(inher.local_env), 
                    from_env_to_dictionary(inher.nonlocal_env), 
                    from_env_to_dictionary(inher.global_env)
                ]
                json_data = [atok]

                for tok in abstract_tokens:
                    triple = triple_from_instance(tok)
                    json_data.append(['P', triple[0], triple[1], triple[2]])

                    inher = client.next(tok)
                    if isinstance(inher, Exception):
                        ex = inher
                        raise AnalysisError() from ex

                    new_atok = ['A', 
                        from_env_to_dictionary(inher.local_env), 
                        from_env_to_dictionary(inher.nonlocal_env), 
                        from_env_to_dictionary(inher.global_env)
                    ]
                    if (new_atok != atok):
                        json_data.append(new_atok)
                        atok = new_atok

                client.close()

                write(abstract_data_dirpath, f'{abstract_data_base}.jsonl', json.dumps(json_data) + '\n', append=True)

                def handle_Vocab(o : Vocab):
                    if o.options in vocab.keys():
                        vocab[o.options].add(o.selection)
                    else:
                        vocab[o.options] = {o.selection}

                # update vocabulary
                for inst in abstract_tokens:

                    match_abstract_token(inst, AbstractTokenHandlers(
                        case_Grammar=lambda o : (),
                        case_Vocab=handle_Vocab 
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

            except AnalysisError as ex:
                analysis_error_count += 1
                error_count += 1

            except Exception as ex:
                # print(f"")
                # print(f"ERROR index: {total_count}")
                # line_obj = json.loads(line)
                # source_code = line_obj['code']
                # print(f"ERROR source code:\n{source_code}")
                # print(f"ERROR code length: {len(source_code)}")
                # print(f"ERROR index: {total_count}")
                # print(f"")
                # raise Exception() from ex
                error_count += 1

            # update
            line = f.readline()
            total_count += 1
            
            print(f"")
            print(f"total_count: {total_count}")
            print(f"processed_count: {processed_count}")
            print(f"")

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
        'analysis_error_count' : analysis_error_count,
        'error_count' : error_count,
        'total_count' : total_count
    }
    print(f"FILE STATS: {stats}")
    write(abstract_data_dirpath, f'{abstract_data_base}_stats.json', json.dumps(stats))
    return stats


def generate_file_tuple(triple) -> dict[str, Any]:
    stats = generate_file(triple[0], triple[1], triple[2])
    return stats

def generate_dir(dirname : str):
    concrete_data_dirpath = project_path(f"res/{dirname}/concrete_data")
    vocab : dict[str, set[str]] = {}

    abstract_data_dirpath = project_path(f"res/{dirname}/abstract_data")
    write(abstract_data_dirpath, f'vocab.json', '')


    import multiprocessing
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    stats_collection = pool.map(generate_file_tuple, [(dirname, n, vocab) for n in os.listdir(concrete_data_dirpath)])
    pool.close()
    pool.join()


    time = 0
    processed_count = 0
    rec_error_count = 0
    big_code_error_count = 0
    obsolete_error_count = 0
    unsupported_error_count = 0
    analysis_error_count = 0
    error_count = 0
    total_count = 0

    print(f"stats_collection length: {len(stats_collection)}")

    for stats in stats_collection:
        time += stats['time']
        processed_count += stats['processed_count']
        rec_error_count += stats['rec_error_count']
        big_code_error_count += stats['big_code_error_count'] 
        obsolete_error_count += stats['obsolete_error_count'] 
        unsupported_error_count += stats['unsupported_error_count'] 
        analysis_error_count += stats['analysis_error_count'] 
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

    print(f"DIR STATS: {stats}")
    write(abstract_data_dirpath, f'z_stats.json', json.dumps(stats))
    return stats


    


    # for filename in os.listdir(concrete_data_dirpath):
    #     generate_file(filename)

    write(abstract_data_dirpath, f'vocab.json', json.dumps(
        {
            k:list(v)
            for k,v in vocab.items()
        },
        indent=4
    ), append=True)