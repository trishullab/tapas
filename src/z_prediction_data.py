from tapas_base import abstract_token_system
from tapas_base import util_system
import json



from tapas_base import abstract_token_system as ats
from tapas_lib import python_abstract_token_system as pats
from tapas_lib import python_ast_system as pas
def concretize_ptokens(ptoks : list[str]) -> str:

    triples = [ptoks[i:i + 3] for i in range(0, len(ptoks), 3)]

    toks : tuple[ats.abstract_token, ...] = tuple(
        (
            ats.make_Grammar(triple[1], triple[2])
            if triple[0] == "grammar" else

            ats.make_Vocab(triple[1], triple[2])

        )
        for triple in triples
    )

    return pats.concretize(toks)

# fpath = util_system.project_path('res/mbpp/abstract_data_0/mbpp.jsonl')

# with open(fpath, 'r') as f:
#     program_data_json = f.readline()

#     program_data = json.loads(program_data_json)
#     # print(f"program data: {program_data}")
#     print(f"-----------------------------")
#     from lib import util_system as us
#     print(f"linearize: {us.linearize_list(program_data)}")

#     print(f"-----------------------------")

#     just_the_ps = [
#         ptok
#         for ptok in program_data
#         if ptok[0] == "P"
#     ]


#     print("@@@@@@@@@@@@")
#     print(concretize_ptokens(just_the_ps))
#     print("@@@@@@@@@@@@")


    # from lib import python_analysis_system as pals
    # package = pals.analyze_typeshed()
    # client = pals.spawn_analysis(package, "example")
    
    # atok = client.init_prim
    # print(atok)
    # for ptok in just_the_ps:
    #     print(ptok)
    #     atok = client.next_prim(ptok)
    #     if atok:
    #         print(atok)
    #     else:
    #         # no change 
    #         pass


# from lib import python_schema_system as pss

# vocab = set({})

# for rule in pss.node_schema.values():
#     for item in rule.content:
#         if isinstance(item, pss.Vocab):
#             vocab.add(item.vocab)

# print(vocab)

concrete_fpath = util_system.project_path('res/mbpp/concrete_data/mbpp.jsonl')

with open(concrete_fpath, 'r') as f:
    program_data_json = f.readline()
    code = json.loads(program_data_json)['code']
#     code = '''
# x = 1
# y = 2
# x + y * 2
# if x == 1: 
#     5
#     '''

    print("")
    print("######### original ###########")
    print(code)

    print("")
    print("######### original tokens ###########")
    tree = pas.parse(code)
    toks = pas.serialize(tree)
    print([ats.to_primitive(t) for t in toks])

    print("")
    print("######### concretized ###########")
    print(pats.concretize(toks))

    print("")
    print("######### truncated ###########")
    truncated = pas.truncate(code, .5)
    print(truncated)

    print("")
    print("######### truncated tokens ###########")
    tree = pas.parse(truncated)
    toks = pas.serialize(tree)
    print([ats.to_primitive(t) for t in toks])

    print("")
    print("######### truncated concretized ###########")
    print(pats.concretize(toks))
