from pyrsistent.typing import PMap, PSet
from pyrsistent import pmap, m, pset, s
from tapas_lib import python_aux_system as pals
from tapas_lib import python_ast_system as pas
from tapas_lib import python_generic_tree_system as pgs 
from tapas_lib import python_abstract_token_system as pats
from tapas_base import abstract_token_system as ats
from tapas_base import util_system as us

import json
import pytest

from tapas_lib.python_aux_construct_autogen import RecordType, make_RecordType

package : PMap[str, pals.ModulePackage] = pals.analyze_typeshed_cache()

def load_source(name : str) -> str:
    path = us.project_path(f"tapas_res/python/{name}.py")
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
    # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    t = aux.local_env.get('type')
    assert t
    assert isinstance(t.type, pals.IntLitType)
    with pytest.raises(pals.ApplyRatorTypeCheck):
        analyze("055_error", 10)

def test_055_1_ok():
    analyze("055_1_ok")

def test_055_2_ok():
    analyze("055_2_ok")

def test_056_error():
    code, aux = analyze("056_error", 8)
    # print(code)
    # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    f = aux.local_env.get('f')
    assert f 
    assert isinstance(f.type, pals.IntLitType)
    with pytest.raises(pals.ApplyRatorTypeCheck):
        analyze("056_error")

def test_057_error():
    code, aux = analyze("057_error", 9)
    # print(code)
    # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    i = aux.local_env.get('i')
    assert i == None 
    with pytest.raises(pals.LookupDecCheck):
        analyze("057_error")

def test_057_1_error():
    with pytest.raises(pals.LookupDecCheck):
        analyze("057_1_error")

def test_057_2_error():
    with pytest.raises(pals.LookupDecCheck):
        analyze("057_2_error")

def test_058_ok():
    code, aux = analyze("058_ok", 5)
    # print(code)
    # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    x = aux.local_env.get('x')
    assert x
    x_type = x.type
    assert isinstance(x_type, pals.DictLitType)
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
    # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    foo = aux.local_env.get('foo')
    assert foo
    foo_type = foo.type
    assert isinstance(foo_type, pals.FunctionType)
    foo_return_type = foo_type.return_type
    assert isinstance(foo_return_type, pals.RecordType)
    assert foo_return_type.class_key == "builtins.int"

def test_061_ok():
    code, aux = analyze("061_ok", 2)
    # print(code)
    # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    final_str = aux.local_env.get('final_str')
    assert final_str 
    final_str_type = final_str.type
    assert isinstance(final_str_type, pals.RecordType)
    assert final_str_type.class_key == "builtins.str"

def test_062_ok():
    analyze("062_ok")

def test_063_error():
    with pytest.raises(pals.AssignTypeCheck):
        analyze("063_error")

def test_064_ok():
    analyze("064_ok")

def test_065_ok():
    code_pre, aux_pre = analyze("065_ok", 2)
    # print(code_pre)
    # print(json.dumps(pals.from_env_to_primitive_verbose(aux_pre.local_env), indent=4))
    xs_pre = aux_pre.local_env.get('xs')
    il = pals.IntLitType
    assert xs_pre 
    assert xs_pre.type == pals.ListLitType(item_types=(il('1'),il('2'),il('3')))

    code_post, aux_post = analyze("065_ok", 3)
    # print(code_post)
    # print(json.dumps(pals.from_env_to_primitive_verbose(aux_post.local_env), indent=4))
    xs_post = aux_post.local_env.get('xs')
    il = pals.IntLitType
    assert xs_post 
    assert xs_post.type == pals.make_RecordType(
        class_key="builtins.list",
        type_args=(pals.make_RecordType(class_key="builtins.int"),)
    )

def test_066_ok():
    code_pre, aux_pre = analyze("066_ok", 2)
    # print(code_pre)
    # print(json.dumps(pals.from_env_to_primitive_verbose(aux_pre.local_env), indent=4))
    xs_pre = aux_pre.local_env.get('xs')
    il = pals.IntLitType
    assert xs_pre 
    assert xs_pre.type == pals.ListLitType(item_types=(il('1'),il('2'),il('3')))

    code_post, aux_post = analyze("066_ok", 3)
    xs_post = aux_post.local_env.get('xs')
    # print(code_post)
    # print(json.dumps(pals.from_env_to_primitive_verbose(aux_post.local_env), indent=4))
    assert xs_post 
    xs_post_type = xs_post.type
    assert (
        isinstance(xs_post_type, pals.RecordType) and
        xs_post_type.class_key == "builtins.list" and
        pals.make_RecordType(class_key="builtins.int") in xs_post_type.type_args and
        pals.make_RecordType(class_key="builtins.str") in xs_post_type.type_args
    )

def test_067_ok():
    code, aux = analyze("067_ok", 4)
    # print(code)
    # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    assert 'x' in aux.local_env
    code, aux = analyze("067_ok", 7)
    # print(code)
    # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    assert 'x' not in aux.local_env
    assert 'self' in aux.local_env

def test_068_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        analyze("068_error")

def test_069_ok():
    analyze("069_ok")


def test_070_0_ok():
    code, aux = analyze("070_0_ok",2)
    print(code)
    print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    x = aux.local_env.get("x")
    assert x
    x_type = x.type
    assert isinstance(x_type, RecordType)
    assert x_type.class_key == "builtins.list"
    x_type_args = x_type.type_args
    assert len(x_type_args) == 1 
    assert x_type_args[0] == make_RecordType(class_key="builtins.int")

def test_070_1_ok():
    analyze("070_1_ok")

def test_070_2_ok():
    analyze("070_2_ok")

def test_070_3_ok():
    code, aux = analyze("070_3_ok", 9)
    print(code)
    print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    a = aux.local_env.get("a")
    assert a
    assert a.type == make_RecordType(class_key="070_3_ok.A", type_args=(
        make_RecordType(class_key="builtins.int"),
    ))

def test_070_4_ok():
    code, aux = analyze("070_4_ok", 7)
    print(code)
    print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    x = aux.local_env.get("x")
    assert x
    assert x.type == make_RecordType(class_key="builtins.int")

def test_070_ok():
    analyze("070_ok")

def test_071_ok():
    analyze("071_ok")

def test_072_ok():
    analyze("072_ok")

def test_073_ok():
    analyze("073_ok")

def test_074_1_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        analyze("074_1_error")

def test_074_ok():
    analyze("074_ok")

def test_075_1_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        analyze("075_1_error")

def test_075_ok():
    analyze("075_ok")

def test_076_ok():
    analyze("076_ok")

def test_077_ok():
    analyze("077_ok")

def test_078_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        analyze("078_error")

def test_079_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        analyze("079_error")

def test_080_ok():
    analyze("080_ok")

if __name__ == "__main__":
    pass