from lib import util_system
import json

from lib.python_analysis_system import from_inher_aux_to_primitive

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

    program_data = json.loads(program_data_json)
    # print(f"program data: {program_data}")
    # print(f"linearize: {linearize_list(program_data)}")
    just_the_ps = [
        ptok
        for ptok in program_data
        if ptok[0] == "P"
    ]


    from lib import python_analysis_system as pals
    inher_aux = pals.update_InherAux(pals.analyze_typeshed(1),
        external_path="example"
    )
    client = pals.spawn_analysis(inher_aux)
    
    print(from_inher_aux_to_primitive(inher_aux))
    for ptok in just_the_ps:
        print(ptok)
        inher_prim = client.next_prim(ptok)
        if inher_prim:
            print(inher_prim)
        else:
            # no change 
            pass




