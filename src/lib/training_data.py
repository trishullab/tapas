
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
from lib.file import write_res, write_append_res, write_append_res_gen

from lib.production_instance import instance



def generate(name : str):
    logging.basicConfig(level=logging.INFO)
    base_path = pathlib.Path(__file__).parent.absolute()
    dirpath = os.path.join(base_path, "../../res")
    fpath = os.path.join(dirpath, f"{name}.jsonl")

    with open(fpath, 'r') as f:
        count = 1
        line = f.readline()
        while line: 

            line_obj = json.loads(line)

            source_code = line_obj['code']

            tree = generic_tree.parse('python', source_code, 'utf8')


            try:
                mod = from_generic_ast(tree)

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
                    if (0 <= count <= 1):

                        print(f"-------------------------")
                        print(f"line number: {count}")
                        print(f"-------------------------")

                        concrete_code = python_instance.concretize(instances)

                        # print(f"-------------------------")
                        # print(f"generic tree:")
                        # print(generic_tree.dump(tree))

                        print(f"-------------------------")
                        print(f"production tree:")
                        print(python_instance.dump(instances))

                        print(f"-------------------------")
                        print(f"source:")
                        print(source_code)

                        print(f"-------------------------")
                        print(f"concretized:")
                        print(concrete_code)

                    else:
                        break


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
                        triple_from_instance(i) 
                        for i in instances
                    ]

                    write_append_res_gen(f'{name}_training.txt', json.dumps(training_data) + '\n\n<|endoftext|>\n\n')

            except Exception as x:

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
                print(f"line number: {count}")

                raise x

            # update
            line = f.readline()
            count += 1
