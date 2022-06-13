from pyrsistent.typing import PMap, PSet
from pyrsistent import pmap, m, pset, s
from lib import python_aux_system as pals
from lib import python_ast_system as pas
from lib import python_generic_tree_system as pgs 
from lib import python_abstract_token_system as pats
from base import abstract_token_system as ats
from base import util_system as us

import os.path

import json
import pytest

from lib.python_aux_construct_autogen import DictLitType, RecordType, StrLitType

typeshed_cache = 'res/typeshed_object'
package : PMap[str, pals.ModulePackage] = (
    us.load_object(typeshed_cache)
    if os.path.exists(us.project_path(typeshed_cache)) else
    # if False else
    us.save_object(pals.analyze_typeshed(), typeshed_cache)
)

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

def analyze(module_name : str, line_limit: int = -1) -> tuple[str, pals.InherAux]:

    code = load_source(module_name) 
    # print(f"***************************************")
    # print(f"module: {module_name}")
    # print(f"-------------------------------------")
    # tokens = pas.serialize(pas.parse(code))
    # print(pats.dump(tokens))
    # print(f"***************************************")

    gnode = pgs.parse(code)
    mod = pas.parse_from_generic_tree(gnode)
    abstract_tokens = pas.serialize(mod)

    partial_tokens = [] 
    client : pals.Client = pals.spawn_analysis(package, module_name)

    partial_code = ""
    inher_aux : pals.InherAux = client.init
    for token in abstract_tokens:
        inher_aux = client.next(token)
        partial_tokens.append(token)
        partial_code = pats.concretize(tuple(partial_tokens))
        # partial_code
        # ats.to_string(token)
        # json.dumps(pals.from_inher_aux_to_primitive(inher_aux), sort_keys=False, indent=4)
        if line_limit > -1:
            line_count = len(partial_code.split('\n'))
            if line_count >= line_limit:
                class TestKill(Exception): pass
                client.kill(TestKill())
                return (partial_code, inher_aux)
    return (partial_code, inher_aux)

def test_000_0_ok():
    analyze("000_0_ok")

def test_000_1_error():
    with pytest.raises(pals.LookupDecCheck):
        analyze("000_1_error")



def test_000_2_error():
    with pytest.raises(pals.LookupInitCheck):
        analyze("000_2_error")
    code = load_source("000_2_error")
    assert pals.analyze_summary(package, "main", code) == "lookup_init_check"

def test_000_3_ok():
    analyze("000_3_ok")

def test_000_4_error():
    with pytest.raises(pals.LookupInitCheck):
        analyze("000_4_error")

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

def test_042_error():
    with pytest.raises(pals.LookupDecCheck):
        analyze("042_error")

def test_043_error():
    with pytest.raises(pals.LookupDecCheck):
        analyze("043_error")


def test_044_ok():
    analyze("044_ok")

def test_045_error():
    with pytest.raises(pals.LookupDecCheck):
        analyze("045_error")

def test_046_error():
    with pytest.raises(pals.LookupDecCheck):
        analyze("046_error")

def test_047_error():
    with pytest.raises(pals.LookupDecCheck):
        analyze("047_error")

def test_048_error():
    analyze("048_ok")

def test_049_error():
    with pytest.raises(pals.LookupDecCheck):
        analyze("049_error")

def test_050_error():
    with pytest.raises(pals.LookupDecCheck):
        analyze("050_error")

def test_051_error():
    with pytest.raises(pals.LookupDecCheck):
        analyze("051_error")

def test_052_error():
    with pytest.raises(pals.LookupDecCheck):
        analyze("052_error")

def test_053_ok():
    analyze("053_ok")

def test_054_ok():
    analyze("054_ok")

def test_055_error():
    code, aux = analyze("055_error", 9)
    # print(code)
    # print(json.dumps(pals.from_env_to_primitive(aux.local_env), indent=4))
    t = aux.local_env.get('type')
    assert t
    assert isinstance(t.type, pals.IntLitType)
    with pytest.raises(pals.ApplyRatorTypeCheck):
        analyze("055_error", 10)

def test_056_error():
    code, aux = analyze("056_error", 8)
    # print(code)
    # print(json.dumps(pals.from_env_to_primitive(aux.local_env), indent=4))
    f = aux.local_env.get('f')
    assert f 
    assert isinstance(f.type, pals.IntLitType)
    with pytest.raises(pals.ApplyRatorTypeCheck):
        analyze("056_error")

def test_057_error():
    code, aux = analyze("057_error", 9)
    # print(code)
    # print(json.dumps(pals.from_env_to_primitive(aux.local_env), indent=4))
    i = aux.local_env.get('i')
    assert i == None 
    with pytest.raises(pals.LookupDecCheck):
        analyze("057_error")

def test_058_ok():
    code, aux = analyze("058_ok", 5)
    # print(code)
    # print(json.dumps(pals.from_env_to_primitive(aux.local_env), indent=4))
    x = aux.local_env.get('x')
    assert x
    x_type = x.type
    assert isinstance(x_type, DictLitType)
    assert len(x_type.pair_types) == 2

    entry_one = x_type.pair_types[0]
    entry_one_kt = entry_one[0] 
    entry_one_vt = entry_one[1] 
    assert entry_one_kt == pals.StrLitType("'hi'")
    assert entry_one_vt == pals.IntLitType('1')

    entry_two = x_type.pair_types[1]
    entry_two_kt = entry_two[0] 
    entry_two_vt = entry_two[1] 
    assert entry_two_kt == pals.IntLitType('2')
    assert entry_two_vt == pals.StrLitType("'bye'")

def test_059_ok():
    analyze("059_ok")

def test_060_ok():
    code, aux = analyze("060_ok", 4)
    # print(code)
    # print(json.dumps(pals.from_env_to_primitive(aux.local_env), indent=4))
    foo = aux.local_env.get('foo')
    assert foo
    foo_type = foo.type
    assert isinstance(foo_type, pals.FunctionType)
    foo_return_type = foo_type.return_type
    assert isinstance(foo_return_type, RecordType)
    assert foo_return_type.class_key == "builtins.int"

def test_061_ok():
    code, aux = analyze("061_ok", 2)
    # print(code)
    # print(json.dumps(pals.from_env_to_primitive(aux.local_env), indent=4))
    final_str = aux.local_env.get('final_str')
    assert final_str 
    final_str_type = final_str.type
    assert isinstance(final_str_type, RecordType)
    assert final_str_type.class_key == "builtins.str"


if __name__ == "__main__":
    pass