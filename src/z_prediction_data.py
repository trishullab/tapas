
# from tree_sitter import Language

# import logging
# import os
# import pathlib
# import tree_sitter
# import json
# from lib.abstract_token_construct_autogen import AbstractTokenHandlers, match_abstract_token

# import lib.python_abstract_token
# from lib.util import write
# from lib import util

# from lib.abstract_token import abstract_token
# import lib.abstract_token 

# import re

# def test(fpath : str):

#     with open(fpath, 'r') as f:
#         all_prediction_data = f.read()
#         # print(f"all pd: {all_prediction_data}")
#         print(f"-----------------------------")

#         program_delim_regex = (
#             r'(?=(?!".*)\n\n<\|endoftext\|>\n\n(?!".*))' + 
#             r"\n\n<\|endoftext\|>\n\n"
#         )

#         count = 0
#         for prediction_data in re.split(program_delim_regex, all_prediction_data):

#             print(f"\n-------------------------\n")
#             print(f"count: {count}")
#             count += 1


#             prediction_list = json.loads(prediction_data)
#             # print(f"\n-------------------------\n")
#             # print(f"pd: {prediction_data}")
#             # print(f"\n-------------------------\n")
#             # print(f"prediction_list:")
#             # print(prediction_list)

#             triples = [prediction_list[i:i + 3] for i in range(0, len(prediction_list), 3)]

#             print(f"\n-------------------------\n")
#             print(f"triples:")
#             for t in triples:
#                 print(t)

#             prediction_abstract_tokens : list[abstract_token] = [
#                 (
#                     lib.abstract_token.make_Grammar(triple[1], triple[2])
#                     if triple[0] == "grammar" else

#                     lib.abstract_token.make_Vocab(triple[1], triple[2])

#                 )
#                 for triple in triples
#             ]


#             print(f"\n-------------------------\n")
#             print(f"prediction abstract_tokens:")
#             for pi in prediction_abstract_tokens:
#                 print(pi)

#             # print(f"\n-------------------------\n")
#             # print(f"abstract_token tree:")
#             # print(python_abstract_token.dump(prediction_abstract_tokens))


#             concrete_code = lib.python_abstract_token.concretize(tuple(prediction_abstract_tokens))
#             print(f"\n-------------------------\n")
#             print(f"concretized:")
#             print(concrete_code)

#             # print(f"\n-------------------------\n")

# fpath = util.project_path('res/mbpp/abstract_data/mbpp.jsonl')
# test(fpath)

from lib import util
import json
import re

fpath = util.project_path('res/mbpp/abstract_data/mbpp.jsonl')

with open(fpath, 'r') as f:
    json_list = f.read().strip().split("\n")

    for json_program in json_list:
        program_data = json.loads(json_program)
        print(f"program data: {program_data}")



# with open(fpath, 'r') as f:
#     all_prediction_data = f.read()
#     # print(f"all pd: {all_prediction_data}")
#     program_delim_regex = (
#         r'(?=(?!".*)\n\n<\|endoftext\|>\n\n(?!".*))' + 
#         r"\n\n<\|endoftext\|>\n\n"
#     )
#     re.split(program_delim_regex, all_prediction_data)

#     for prediction_data_json in re.split(program_delim_regex, all_prediction_data):
#         program_data = json.loads(prediction_data_json)


# with open(fpath, 'r') as f:
#     program_data_json = f.readline()

#     while program_data_json:
#         program_data = json.loads(program_data_json)
#         # print(f"program data: {program_data}")



# with open(fpath, 'r') as f:
#     all_program_data = f.read()

#     count = 0
#     for program_data in json.loads(all_program_data):
#         ...
