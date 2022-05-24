from pyrsistent.typing import PMap, PSet
from pyrsistent import pmap, m, pset, s
from lib import python_analysis_system as pals
from lib import python_ast_system as pas
from lib import python_generic_tree_system as pgs 
from lib import python_abstract_token_system as pats
from lib import abstract_token_system as ats
from lib import util_system as us

import json
import pytest


def test_analyze_typeshed():
    pals.analyze_typeshed()

package : PMap[str, pals.ModulePackage] = pals.analyze_typeshed()

def load_source(name : str) -> str:
    path = us.project_path(f"res/test/python/source/{name}.py")
    with open(path, 'r') as f:
        return f.read()

def translate(module_name : str):
    code = load_source(module_name) 
    print(f"***************************************")
    print(f"OOGA: {module_name}")
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

    # pals.analyze_code(package, module_name, code)
    partial_tokens = []
    for token, code, inher_aux in pals.analyze_in_steps(module_name, code, package):
        partial_tokens.append(token)
        print(f"""
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
-----------------------------
{code}
-----------------------------
{ats.to_string(token)}
-----------------------------
{json.dumps(pals.from_inher_aux_to_primitive(inher_aux), sort_keys=False, indent=4)}
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
""")

def test_000_0_ok():
    analyze("000_0_ok")

def test_000_1_error():
    with pytest.raises(pals.LookupDecError):
        analyze("000_1_error")

def test_000_2_error():
    with pytest.raises(pals.LookupInitError):
        analyze("000_2_error")

def test_001_ok():
    analyze("001_ok")

def test_002_error():
    with pytest.raises(pals.AssignTypeError):
        analyze("002_error")

def test_003_ok():
    analyze("003_ok")

def test_004_error():
    with pytest.raises(pals.ApplyArgTypeError):
        analyze("004_error")

def test_005_ok():
        analyze("005_ok")

def test_006_error():
    with pytest.raises(pals.AssignTypeError):
        analyze("006_error")

def test_007_ok():
    analyze("007_ok")

def test_008_error():
    with pytest.raises(pals.AssignTypeError):
        analyze("008_error")

def test_009_error():
    with pytest.raises(pals.AssignTypeError):
        analyze("009_error")

def test_010_ok():
    analyze("010_ok")

def test_011_error():
    with pytest.raises(pals.AssignTypeError):
        analyze("011_error")

def test_012_ok():
    analyze("012_ok")

def test_013_error():
    with pytest.raises(pals.ApplyArgTypeError):
        analyze("013_error")

def test_014_ok():
    analyze("014_ok")

def test_015_error():
    with pytest.raises(pals.ApplyArgTypeError):
        analyze("015_error")

def test_016_error():
    with pytest.raises(pals.ReturnTypeError):
        analyze("016_error")

def test_017_ok():
    analyze("017_ok")

def test_018_ok():
    analyze("018_ok")

def test_019_error():
    with pytest.raises(pals.LookupTypeError):
        analyze("019_error")

def test_020_ok():
    analyze("020_ok")

def test_021_error():
    with pytest.raises(pals.UpdateError):
        analyze("021_error")

if __name__ == "__main__":
    # analyze("020_ok")
    pass