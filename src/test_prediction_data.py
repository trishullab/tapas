
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
from lib import production_instance as prod_inst

import re

def test(fpath : str):

    with open(fpath, 'r') as f:
        all_prediction_data = f.read()
        # print(f"all pd: {all_prediction_data}")
        print(f"-----------------------------")

        program_delim_regex = (
            r'(?=(?!""".*)\n\n<\|endoftext\|>\n\n(?!""".*))' + 
            r"(?=(?!'''.*)\n\n<\|endoftext\|>\n\n(?!'''.*))" + 
            r"\n\n<\|endoftext\|>\n\n"
        )

        for prediction_data in re.split(program_delim_regex, all_prediction_data):

            print(f"pd: {prediction_data}")
            print(f"")
            print(f"-------")

            # prediction_instances : list[instance] = [
            #     (
            #         prod_inst.make_Grammar(triple[1], triple[2])
            #         if triple[0] == "grammar" else

            #         prod_inst.make_Vocab(triple[1], triple[2])

            #     )
            #     for match in re.findall(r"\[[^,]+,[^,]+,[^,]+\]", prediction_data[1:-1])
            #     for triple in [match[1:-1].split(",")]
            # ]

            # print(f"")
            # print(f"prediction instances:")
            # for pi in prediction_instances:
            #     print(pi)

            # print(f"-------------------------")
            # print(f"generic tree:")
            # print(generic_tree.dump(tree))


            # concrete_code = python_instance.concretize(prediction_instances)
            # print(f"")
            # print(f"concretized:")
            # print(concrete_code)
            # print(f"")
            # print(f"-------------------------")
            # print(f"")




base_path = pathlib.Path(__file__).parent.absolute()
fpath = os.path.join(base_path, '../res/mbpp/mbpp_prediction_test.txt')
test(fpath)