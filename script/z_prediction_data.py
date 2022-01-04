
from tree_sitter import Language

import logging
import os
import pathlib
import tree_sitter
import json
from gen.instance_construct import InstanceHandlers, match_instance

import lib.python_sequence
from lib.file import write

from lib.instance import instance
import lib.instance 

import re

def test(fpath : str):

    with open(fpath, 'r') as f:
        all_prediction_data = f.read()
        # print(f"all pd: {all_prediction_data}")
        print(f"-----------------------------")

        program_delim_regex = (
            r'(?=(?!".*)\n\n<\|endoftext\|>\n\n(?!".*))' + 
            r"\n\n<\|endoftext\|>\n\n"
        )

        count = 0
        for prediction_data in re.split(program_delim_regex, all_prediction_data):

            print(f"\n-------------------------\n")
            print(f"count: {count}")
            count += 1


            prediction_list = json.loads(prediction_data)
            # print(f"\n-------------------------\n")
            # print(f"pd: {prediction_data}")
            # print(f"\n-------------------------\n")
            # print(f"prediction_list:")
            # print(prediction_list)

            triples = [prediction_list[i:i + 3] for i in range(0, len(prediction_list), 3)]

            print(f"\n-------------------------\n")
            print(f"triples:")
            for t in triples:
                print(t)

            prediction_instances : list[instance] = [
                (
                    lib.instance.make_Grammar(triple[1], triple[2])
                    if triple[0] == "grammar" else

                    lib.instance.make_Vocab(triple[1], triple[2])

                )
                for triple in triples
            ]


            print(f"\n-------------------------\n")
            print(f"prediction instances:")
            for pi in prediction_instances:
                print(pi)

            # print(f"\n-------------------------\n")
            # print(f"instance tree:")
            # print(python_instance.dump(prediction_instances))


            concrete_code = lib.python_sequence.concretize(prediction_instances)
            print(f"\n-------------------------\n")
            print(f"concretized:")
            print(concrete_code)

            # print(f"\n-------------------------\n")




base_path = pathlib.Path(__file__).parent.absolute()
fpath = os.path.join(base_path, '../res/mbpp/mbpp_prediction_20211028.txt')
test(fpath)