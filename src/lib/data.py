
from tree_sitter import Language

import logging
import os
import pathlib
import tree_sitter
import json
from lib.abstract_token_construct_autogen import AbstractTokenHandlers, match_abstract_token, Vocab

from lib import generic_tree

from lib import python_ast
from lib.util import write, project_path
from lib.abstract_token import abstract_token 
from lib.abstract_token_construct_autogen import Vocab



from lib.python_abstract_token import concretize, analyze, Client
# from lib.abstract_token import abstract_token
from lib.python_util import Inher, from_Inher_to_string
from lib.python_util import Inher, from_Inher_to_dictionary
# from typing import Union
import lib.abstract_token
from typing import Any, Union



def generate_file(dirname : str, name : str, vocab : dict):

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
        processed_count = 0
        rec_error_count = 0
        error_count = 0
        total_count = 0
        line = f.readline()
        while line: 

            line_obj = json.loads(line)

            source_code = line_obj['code']

            tree = generic_tree.parse('python', source_code, 'utf8')


            abstract_tokens : tuple[abstract_token, ...] = () 

            try:

                mod = python_ast.parse_from_generic_tree(tree)
                # mod = python_ast_rename.rename_Module(mod, {}, {}, {})

                abstract_tokens = python_ast.serialize(mod)


                # if total_count < 50:

                    # print(f"-------------------------")
                    # print(f"line number: {total_count + 1}")
                    # print(f"-------------------------")

                    # concrete_code = python_instance.concretize(instances)

                    # print(f"-------------------------")
                    # print(f"generic tree:")
                    # print(generic_tree.dump(tree))

                    # print(f"-------------------------")
                    # print(f"production tree:")
                    # print(python_instance.dump(instances))

                    # print(f"-------------------------")
                    # print(f"source:")
                    # print(source_code)

                    # print(f"-------------------------")
                    # print(f"concretized:")
                    # print(concrete_code)



                def triple_from_instance(inst : abstract_token) -> tuple[str, str, str]:
                    return match_abstract_token(inst, AbstractTokenHandlers[tuple[str, str, str]](
                        case_Grammar=lambda o : (
                            ("grammar", o.options, o.selection)
                        ),
                        case_Vocab=lambda o : (
                            ("vocab", o.options, o.selection)
                        )
                    )) 


                # data = [
                #     f"[{t[0]},{t[1]},{t[2]}]"
                #     for i in instances
                #     for t in [triple_from_instance(i)] 
                # ]
                # write(abstract_data_dirpath, f'{abstract_data_base}_training.txt', "[" + ",".join(data) + "]" + '\n\n<|endoftext|>\n\n', append=True)

                # print(f"\n-------------------------\n")
                # print(f"---Source Code---")
                # print(source_code)



                client : Client = analyze()
                from lib.python_util import from_env_to_dictionary
                inher : Inher = client.init_inher
                atok = ['A', from_env_to_dictionary(inher.local_env), from_env_to_dictionary(inher.nonlocal_env), from_env_to_dictionary(inher.global_env)]
                json_data = [atok]
                for tok in abstract_tokens:
                    triple = triple_from_instance(tok)
                    json_data.append(['P', triple[0], triple[1], triple[2]])
                    inher = client.next(tok)
                    new_atok = ['A', from_env_to_dictionary(inher.local_env), from_env_to_dictionary(inher.nonlocal_env), from_env_to_dictionary(inher.global_env)]
                    if (new_atok != atok):
                        json_data.append(new_atok)
                        atok = new_atok
                client.close()

                # print(f"generating json program: {json_data}")
                write(abstract_data_dirpath, f'{abstract_data_base}.jsonl', json.dumps(json_data) + '\n', append=True)
                assert False

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
                # print(f"\n\n")

                # print(f"""--Generic Tree--\n{
                #     generic_tree.dump(tree, 
                #         text_cond = lambda n : len(n.children) == 0 or n.syntax_part == "string"
                #     )
                # }\n""")

                # print(f"\n\n")
                # print(f"---Source Code---")
                # print(source_code)
                # print(f"-------------------------")
                # print(f"recursion error line number: {count}")
                # print("RECURSION ERROR")
                # return

            except Exception as x:
                error_count += 1
                # print(f"\n-------------------------\n")
                # print(f"""--Generic Tree--\n{
                #     generic_tree.dump(tree, 
                #         text_cond = lambda n : len(n.children) == 0 or n.syntax_part == "string"
                #     )
                # }\n""")


                # print(f"\n-------------------------\n")
                # print(f"---Source Code---")
                # print(source_code)

                # print(f"\n-------------------------\n")
                # print(f"line number: {count}")


                # raise x
            except:
                pass
                # print(f"\n-------------------------\n")
                # print(f"---Source Code---")
                # print(source_code)

            # update
            line = f.readline()
            total_count += 1

        #endwhile

    end = datetime.now()

    stats = \
    f"""
        id: {dirname} :: {name}"
        time: {end - start}
        total count: {total_count}
        processed count: {processed_count}
        error count: {error_count}
        rec error count: {rec_error_count}
    """

    write(abstract_data_dirpath, f'{abstract_data_base}_stats.txt', stats)


def generate_file_tuple(triple):
    generate_file(triple[0], triple[1], triple[2])

def generate_dir(dirname : str):
    concrete_data_dirpath = project_path(f"res/{dirname}/concrete_data")
    vocab : dict[str, set[str]] = {}

    abstract_data_dirpath = project_path(f"res/{dirname}/abstract_data")
    write(abstract_data_dirpath, f'vocab.json', '')


    import multiprocessing
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    pool.map(generate_file_tuple, [(dirname, n, vocab) for n in os.listdir(concrete_data_dirpath)])

    # for filename in os.listdir(concrete_data_dirpath):
    #     generate_file(filename)

    write(abstract_data_dirpath, f'vocab.json', json.dumps(
        {
            k:list(v)
            for k,v in vocab.items()
        },
        indent=4
    ), append=True)