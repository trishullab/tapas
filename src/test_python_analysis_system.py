from pyrsistent.typing import PMap, PSet
from pyrsistent import pmap, m, pset, s
from lib import python_aux_system as pals
from lib import python_ast_system as pas
from lib import python_generic_tree_system as pgs 
from lib import python_abstract_token_system as pats
from base import abstract_token_system as ats
from base import util_system as us

import json
import pytest


def test_analyze_typeshed():
    pals.analyze_typeshed()

package : PMap[str, pals.ModulePackage] = pals.analyze_typeshed()

def load_source(name : str) -> str:
    path = us.project_path(f"res/python/{name}.py")
    with open(path, 'r') as f:
        return f.read()

def translate(module_name : str):
    code = load_source(module_name) 
    print(f"***************************************")
    print(f"-- module: {module_name} --")
    print(f"- code --")
    print(code)
    print(f"-------------------------------------")
    print(f"-- tree = pas.parse(code) --")
    tree = pas.parse(code)
    print(tree)
    print(f"-------------------------------------")
    print(f"-- abstract_tokens = pas.seralize(tree) --")
    abstract_tokens = pas.serialize(tree)
    print(abstract_tokens)
    print(f"-------------------------------------")
    print(f"-- abstract_string =pats.dump(abstract_tokens) --")
    abstract_string = pats.dump(abstract_tokens) 
    print(abstract_string)
    print(f"***************************************")

def analyze(module_name : str):

    code = load_source(module_name) 
    print(f"***************************************")
    print(f"module: {module_name}")
    print(f"-------------------------------------")
    tokens = pas.serialize(pas.parse(code))
    print(pats.dump(tokens))
    print(f"***************************************")

    gnode = pgs.parse(code)
    mod = pas.parse_from_generic_tree(gnode)
    abstract_tokens = pas.serialize(mod)

    partial_tokens = [] 
    client : pals.Client = pals.spawn_analysis(package, module_name)

    inher_aux : pals.InherAux = client.init
    for token in abstract_tokens:
        inher_aux = client.next(token)
        partial_tokens.append(token)
        partial_code = pats.concretize(tuple(partial_tokens))
        print(f"""
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
-----------------------------
{partial_code}
-----------------------------
{ats.to_string(token)}
-----------------------------
{json.dumps(pals.from_inher_aux_to_primitive(inher_aux), sort_keys=False, indent=4)}
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
""")

def test_000_0_ok():
    analyze("000_0_ok")

def test_000_1_error():
    with pytest.raises(pals.LookupDecCheck):
        analyze("000_1_error")

def test_000_2_error():
    with pytest.raises(pals.LookupInitCheck):
        analyze("000_2_error")

def test_001_ok():
    analyze("001_ok")

def test_002_error():
    with pytest.raises(pals.AssignTypeCheck):
        analyze("002_error")

def test_003_ok():
    analyze("003_ok")

def test_004_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        analyze("004_error")

def test_005_ok():
        analyze("005_ok")

def test_006_error():
    with pytest.raises(pals.AssignTypeCheck):
        analyze("006_error")

def test_007_ok():
    analyze("007_ok")

def test_008_error():
    with pytest.raises(pals.AssignTypeCheck):
        analyze("008_error")

def test_009_error():
    with pytest.raises(pals.AssignTypeCheck):
        analyze("009_error")

def test_010_ok():
    analyze("010_ok")

def test_011_error():
    with pytest.raises(pals.AssignTypeCheck):
        analyze("011_error")

def test_012_ok():
    analyze("012_ok")

def test_013_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        analyze("013_error")

def test_014_ok():
    analyze("014_ok")

def test_015_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        analyze("015_error")

def test_016_error():
    with pytest.raises(pals.ReturnTypeCheck):
        analyze("016_error")

def test_017_ok():
    analyze("017_ok")

def test_018_ok():
    analyze("018_ok")

def test_019_error():
    with pytest.raises(pals.LookupTypeCheck):
        analyze("019_error")

def test_020_ok():
    analyze("020_ok")

def test_021_error():
    with pytest.raises(pals.UpdateCheck):
        analyze("021_error")

def test_022_ok():
    analyze("022_ok")

def test_023_ok():
    analyze("023_ok")

def test_024_ok():
    analyze("024_ok")

def test_025_error():
    with pytest.raises(pals.UpdateCheck):
        analyze("025_error")

def test_026_error():
    with pytest.raises(pals.UpdateCheck):
        analyze("026_error")

def test_027_error():
    with pytest.raises(pals.UpdateCheck):
        analyze("027_error")

def test_028_ok():
    analyze("028_ok")

def test_029_ok():
    analyze("029_ok")

def test_030_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        analyze("030_error")

def test_031_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        analyze("031_error")

def test_032_error():
    with pytest.raises(pals.ApplyRatorTypeCheck):
        analyze("032_error")

def test_034_ok():
    analyze("034_ok")

def test_035_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        analyze("035_error")

def test_036_ok():
    analyze("036_ok")

def test_037_ok():
    analyze("037_ok")

def test_038_ok():
    analyze("038_ok")

def test_039_error():
    with pytest.raises(Exception):
        analyze("039_error")

def test_040_ok():
    analyze("040_ok")

def test_041_error():
    with pytest.raises(Exception):
        analyze("041_error")

if __name__ == "__main__":
    pass