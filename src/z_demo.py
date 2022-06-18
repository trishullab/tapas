from tapas_base import util_system as us 
from tapas_base import abstract_token_system as ats 
from tapas_lib import python_abstract_token_system as pats 
from tapas_lib import python_ast_system as pas
from tapas_lib import python_aux_system as pals
from tapas_lib import python_generic_tree_system as pgs
import json

from pyrsistent.typing import PMap

def make_demo_code(module_name, code :str, package : PMap[str, pals.ModulePackage], step_size : int = 1):
    acc = [] 

    gnode = pgs.parse(code)
    mod = pas.parse_from_generic_tree(gnode)
    abstract_tokens = pas.serialize(mod)

    partial_tokens = [] 
    client : pals.Client = pals.spawn_analysis(package, module_name)

    inher_aux : pals.InherAux = client.init
    for token in abstract_tokens:
        inher_aux = client.next(token)
        partial_tokens.append(token)
        code = pats.concretize(tuple(partial_tokens))
        acc += [f"""
<<<<
{ats.to_string(token)}
---
{code}
---
{json.dumps(pals.from_inher_aux_to_primitive(inher_aux), sort_keys=False, indent=4)}
>>>>
        """]
        if acc == step_size:
            yield "".join(acc)
            acc = []
    if len(acc) > 0:
        yield "".join(acc)


from pyrsistent import m

def make_demo_file(path = "res/example.py", n : int = 1):

    parts = path.split("/")
    first_parts = parts[:-1]
    last_part = parts[-1]
    last_part_name = last_part[:-3]
    module_name = f"{'.'.join(first_parts)}.{last_part_name}"
    with open(us.project_path(path)) as f:
        return make_demo_code(module_name, f.read(), m(), n)


if __name__ == "__main__":
    pals.analyze_typeshed()
#     for out in make_demo_code(
#         "main", """
# print "hello world"
#     """, pals.analyze_typeshed(), 
#     1):
#         print(out)