
from tree_sitter import Language

import logging
import os
import pathlib
import tree_sitter
import json

from lib import generic_tree

from lib.python_ast_from_generic_ast import from_generic_ast
from lib.python_ast_serialize import serialize_Module
from lib import python_instance
from lib import generic_instance as inst 
from lib.file import write_res, write_append_res, write_append_res_gen



def generate(name : str):
    logging.basicConfig(level=logging.INFO)
    base_path = pathlib.Path(__file__).parent.absolute()
    dirpath = os.path.join(base_path, "../../res")
    fpath = os.path.join(dirpath, f"{name}.jsonl")

    with open(fpath, 'r') as f:
        count = 1
        line = f.readline()
        while line: 

            print(f"line number: {count}")

            line_obj = json.loads(line)

            source_code = line_obj['code']

            tree = generic_tree.parse('python', source_code, 'utf8')


            try:
                mod = from_generic_ast(tree)

                instance_nodes = []
                try:
                    instance_nodes = serialize_Module(mod)
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
                    concrete_code = python_instance.concretize(instance_nodes)


                    training_data = [
                        {'lhs' : n.lhs, 'rhs' : n.rhs}
                        for n in instance_nodes
                    ]

                    output_line = {'training_data' : training_data, 'concretized' : concrete_code}
                    write_append_res_gen(f'{name}_training.jsonl', json.dumps(output_line))

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
