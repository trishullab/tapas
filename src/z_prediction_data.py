from lib import util_system
import json

fpath = util_system.project_path('res/mbpp/abstract_data_0/mbpp.jsonl')

with open(fpath, 'r') as f:
    program_data_json = f.readline()

    program_data = json.loads(program_data_json)
    # print(f"program data: {program_data}")
    print(f"-----------------------------")
    from lib import util_system as us
    print(f"linearize: {us.linearize_list(program_data)}")

    print(f"-----------------------------")

    just_the_ps = [
        ptok
        for ptok in program_data
        if ptok[0] == "P"
    ]


    from lib import python_analysis_system as pals
    package = pals.analyze_typeshed(1)
    client = pals.spawn_analysis(package, "example")
    
    print(client.init_prim)
    for ptok in just_the_ps:
        print(ptok)
        inher_prim = client.next_prim(ptok)
        if inher_prim:
            print(inher_prim)
        else:
            # no change 
            pass




