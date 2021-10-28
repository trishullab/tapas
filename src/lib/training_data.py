
from tree_sitter import Language

import logging
import os
import pathlib
import tree_sitter
import json
from gen.production_instance import InstanceHandlers, match_instance

from lib import generic_tree

from lib.python_ast_from_generic_ast import from_generic_ast
from lib.python_ast_serialize import serialize_Module
from lib import python_instance
from lib.file import write

from lib.production_instance import instance
from gen import python_ast_rename


base_path = pathlib.Path(__file__).parent.absolute()


def generate(dirname : str, name : str):
    logging.basicConfig(level=logging.INFO)
    dir = os.path.join(base_path, f"../../res/{dirname}")

    read_path = os.path.join(dir, f"{name}.jsonl")


    vocab : dict[str, set[str]] = {}

    write(dir, f'{name}_vocab.json', '')
    write(dir, f'{name}_training.txt', '')
    write(dir, f'{name}_training_json.txt', '')

    from datetime import datetime

    start = datetime.now()

    with open(read_path, 'r') as f:
        count = 1
        line = f.readline()
        while line: 

            line_obj = json.loads(line)

            source_code = line_obj['code']

            tree = generic_tree.parse('python', source_code, 'utf8')


            try:
                mod = from_generic_ast(tree)
                mod = python_ast_rename.rename_Module(mod, {}, {}, {})

                instances = []
                try:
                    instances = serialize_Module(mod)
                except RecursionError:
                    print(f"\n\n")

                    print(f"""--Generic Tree--\n{
                        generic_tree.dump(tree, 
                            text_cond = lambda n : len(n.children) == 0 or n.syntax_part == "string"
                        )
                    }\n""")

                    print(f"\n\n")
                    print(f"---Source Code---")
                    print(source_code)
                    print(f"-------------------------")
                    print(f"recursion error line number: {count}")
                    print("RECURSION ERROR")
                    return

                else:

                    if count < 50:

                        print(f"-------------------------")
                        print(f"line number: {count}")
                        print(f"-------------------------")

                        concrete_code = python_instance.concretize(instances)

                        # print(f"-------------------------")
                        # print(f"generic tree:")
                        # print(generic_tree.dump(tree))

                        # print(f"-------------------------")
                        # print(f"production tree:")
                        # print(python_instance.dump(instances))

                        print(f"-------------------------")
                        print(f"source:")
                        print(source_code)

                        print(f"-------------------------")
                        print(f"concretized:")
                        print(concrete_code)



                    def triple_from_instance(inst : instance) -> tuple[str, str, str]:
                        return match_instance(inst, InstanceHandlers[tuple[str, str, str]](
                            case_Grammar=lambda o : (
                                ("grammar", o.nonterminal, o.sequence_id)
                            ),
                            case_Vocab=lambda o : (
                                ("vocab", o.choices_id, o.word)
                            )
                        )) 


                    training_data = [
                        f"[{t[0]},{t[1]},{t[2]}]"
                        for i in instances
                        for t in [triple_from_instance(i)] 
                    ]
                    write(dir, f'{name}_training.txt', "[" + ",".join(training_data) + "]" + '\n\n<|endoftext|>\n\n', append=True)


                    json_training_data = []
                    for i in instances:
                        triple = triple_from_instance(i)
                        for ti in triple:
                            json_training_data.append(ti)

                    write(dir, f'{name}_training_json.txt', json.dumps(json_training_data) + '\n\n<|endoftext|>\n\n', append=True)

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


            except Exception as x:


                print(f"Another Exception {x}")

                print(f"\n-------------------------\n")
                print(f"""--Generic Tree--\n{
                    generic_tree.dump(tree, 
                        text_cond = lambda n : len(n.children) == 0 or n.syntax_part == "string"
                    )
                }\n""")


                print(f"\n-------------------------\n")
                print(f"---Source Code---")
                print(source_code)

                print(f"\n-------------------------\n")
                print(f"line number: {count}")


                raise x

            # update
            line = f.readline()
            count += 1
        
        write(dir, f'{name}_vocab.json', json.dumps(
            {
                k:list(v)
                for k,v in vocab.items()
            },
            indent=4
        ), append=True)


    end = datetime.now()
    print(f"time: {end - start}")