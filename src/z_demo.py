from lib import util_system as us 
from lib import abstract_token_system as ats 
from lib import python_abstract_token_system as pats 
from lib import python_ast_system as pas
from lib import python_analysis_system as pals
import json

def make_demo_code(code :str, n : int = 1):
    acc = [] 
    for token, code, inher_aux in pals.make_demo(code):
        acc += [f"""
<<<<
{ats.to_string(token)}
---
{code}
---
{json.dumps(pals.from_inher_aux_to_primitive(inher_aux), sort_keys=False, indent=4)}
>>>>
        """]
        if acc == n:
            yield "".join(acc)
            acc = []
    if len(acc) > 0:
        yield "".join(acc)

def make_demo_file(path = "res/example.py", n : int = 1):
    with open(us.project_path(path)) as f:
        return make_demo_code(f.read())


if __name__ == "__main__":


    typeshed_inher_aux : pals.InherAux = pals.analyze_typeshed()

    print("****************")
    print(pals.from_package_to_primitive(typeshed_inher_aux.package))
    print("****************")

#     for out in make_demo_code("""
# print "hello world"
#     """, 1):
#         print(out)