from lib import util_system
import json

fpath = util_system.project_path('res/mbpp/abstract_data_0/mbpp.jsonl')

def linearize_dict(d : dict) -> list: 
    return ['{'] + [
        item
        for k, v in d.items()
        for item in [k] + (
            linearize_dict(v) if isinstance(v, dict) else
            linearize_list(v) if isinstance(v, list) else
            [v]
        )
    ] +  ['}']

def linearize_list(xs : list) -> list: 
    return ['['] + [
        item
        for x in xs
        for item in (
            linearize_dict(x) if isinstance(x, dict) else
            linearize_list(x) if isinstance(x, list) else
            [x]
        )
    ] + [']']

with open(fpath, 'r') as f:
    program_data_json = f.readline()

    while program_data_json:
        program_data = json.loads(program_data_json)
        # print(f"program data: {program_data}")
        print(f"linearize: {linearize_list(program_data)}")
