
from tree_sitter import Language

import logging
import os
import pathlib
import tree_sitter
import json
from gen.production_instance import InstanceHandlers, match_instance

from lib import generic_tree

from lib.python_ast_from_generic_ast import from_generic_ast
from gen.python_ast_serialize import serialize_Module
from lib import python_instance
from lib.file import write

from lib.production_instance import instance
from gen import python_ast_rename

base_path = pathlib.Path(__file__).parent.absolute()

def generate_dir(dirname):
    input_dirpath = os.path.join(base_path, f"../../res/{dirname}/input")
    vocab : dict[str, set[str]] = {}

    output_dirpath = os.path.join(base_path, f"../../res/{dirname}/output")
    write(output_dirpath, f'vocab.json', '')

    def generate_file(name : str):
        nonlocal input_dirpath
        nonlocal vocab

        logging.basicConfig(level=logging.INFO)

        input_path = os.path.join(input_dirpath, name)

        output_base = name.split(".")[0]  
        # write(output_dirpath, f'{output_base}_training.txt', '')
        write(output_dirpath, f'{output_base}_json.txt', '')
        write(output_dirpath, f'{output_base}_stats.txt', '')

        from datetime import datetime

        start = datetime.now()

        with open(input_path, 'r') as f:
            processed_count = 0
            rec_error_count = 0
            error_count = 0
            total_count = 0
            line = f.readline()
            while line: 

                line_obj = json.loads(line)

                source_code = line_obj['code']

                tree = generic_tree.parse('python', source_code, 'utf8')


                instances : list[instance] = []

                try:
                    mod = from_generic_ast(tree)
                    # mod = python_ast_rename.rename_Module(mod, {}, {}, {})

                    instances = serialize_Module(mod)

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



                    def triple_from_instance(inst : instance) -> tuple[str, str, str]:
                        return match_instance(inst, InstanceHandlers[tuple[str, str, str]](
                            case_Grammar=lambda o : (
                                ("grammar", o.nonterminal, o.sequence_id)
                            ),
                            case_Vocab=lambda o : (
                                ("vocab", o.choices_id, o.word)
                            )
                        )) 


                    # data = [
                    #     f"[{t[0]},{t[1]},{t[2]}]"
                    #     for i in instances
                    #     for t in [triple_from_instance(i)] 
                    # ]
                    # write(output_dirpath, f'{output_base}_training.txt', "[" + ",".join(data) + "]" + '\n\n<|endoftext|>\n\n', append=True)


                    json_data = []
                    for i in instances:
                        triple = triple_from_instance(i)
                        for ti in triple:
                            json_data.append(ti)

                    write(output_dirpath, f'{output_base}_json.txt', json.dumps(json_data) + '\n\n<|endoftext|>\n\n', append=True)

                    def handle_Vocab(o):
                        if o.choices_id in vocab.keys():
                            vocab[o.choices_id].add(o.word)
                        else:
                            vocab[o.choices_id] = {o.word}

                    # update vocabulary
                    for inst in instances:

                        match_instance(inst, InstanceHandlers(
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
                    # print(f"Another Exception {x}")

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

                # update
                line = f.readline()
                total_count += 1

            

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

        write(output_dirpath, f'{output_base}_stats.txt', stats)


    for filename in os.listdir(input_dirpath):
        generate_file(filename)

    write(output_dirpath, f'vocab.json', json.dumps(
        {
            k:list(v)
            for k,v in vocab.items()
        },
        indent=4
    ), append=True)