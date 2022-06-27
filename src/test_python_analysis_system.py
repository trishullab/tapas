from pyrsistent.typing import PMap, PSet
from pyrsistent import pmap, m, pset, s

from typing import Callable

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

def analyze_test(module_name : str, line_limit: int = -1) -> tuple[str, pals.InherAux]:

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

def spawn_inspect(module_name : str) -> tuple[Callable[[int], tuple[str, pals.InherAux]], Callable[[], None]]:
    code = load_source(module_name) 
    gnode = pgs.parse(code)
    mod = pas.parse_from_generic_tree(gnode)
    abstract_tokens = pas.serialize(mod)

    partial_tokens = [] 
    client : pals.Client = pals.spawn_analysis(package, module_name)
    partial_code = ""
    inher_aux : pals.InherAux = client.init
    max_len = len(abstract_tokens)

    def kill():
        class TestKill(Exception): pass
        client.kill(TestKill())


    def inspect(l : int) -> tuple[str, pals.InherAux]:
        nonlocal partial_code
        nonlocal inher_aux
        i : int = len(partial_tokens) 
        while i < min(l, max_len):
            token = abstract_tokens[i]
            inher_aux = client.next(token)
            partial_tokens.append(token)
            partial_code = pats.concretize(tuple(partial_tokens))
            i += 1

        return (partial_code, inher_aux)

    return (inspect, kill)

def test_000_0_ok():
    analyze_test("000_0_ok")

def test_000_1_error():
    with pytest.raises(pals.LookupDecCheck):
        analyze_test("000_1_error")



def test_000_2_error():
    with pytest.raises(pals.LookupInitCheck):
        analyze_test("000_2_error")
    code = load_source("000_2_error")
    assert pals.analyze_summary(package, "main", code) == "lookup_init_check"

def test_000_3_ok():
    analyze_test("000_3_ok")

def test_000_4_error():
    with pytest.raises(pals.LookupInitCheck):
        analyze_test("000_4_error")

def test_001_ok():
    analyze_test("001_ok")

def test_002_error():
    with pytest.raises(pals.AssignTypeCheck):
        analyze_test("002_error")

def test_003_ok():
    analyze_test("003_ok")

def test_004_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        analyze_test("004_error")

def test_005_ok():
        analyze_test("005_ok")

def test_006_error():
    with pytest.raises(pals.AssignTypeCheck):
        analyze_test("006_error")

def test_007_ok():
    analyze_test("007_ok")

def test_008_error():
    with pytest.raises(pals.AssignTypeCheck):
        analyze_test("008_error")

def test_009_error():
    with pytest.raises(pals.AssignTypeCheck):
        analyze_test("009_error")

def test_010_ok():
    analyze_test("010_ok")

def test_011_error():
    with pytest.raises(pals.AssignTypeCheck):
        analyze_test("011_error")

def test_012_ok():
    analyze_test("012_ok")

def test_013_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        analyze_test("013_error")

def test_014_ok():
    analyze_test("014_ok")

def test_015_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        analyze_test("015_error")

def test_016_error():
    with pytest.raises(pals.ReturnTypeCheck):
        analyze_test("016_error")

def test_017_ok():
    analyze_test("017_ok")

def test_018_ok():
    analyze_test("018_ok")

def test_019_error():
    with pytest.raises(pals.LookupTypeCheck):
        analyze_test("019_error")

def test_020_ok():
    analyze_test("020_ok")

def test_021_error():
    with pytest.raises(pals.UpdateCheck):
        analyze_test("021_error")

def test_022_ok():
    analyze_test("022_ok")

def test_023_ok():
    analyze_test("023_ok")

def test_024_ok():
    analyze_test("024_ok")

def test_025_error():
    with pytest.raises(pals.UpdateCheck):
        analyze_test("025_error")

def test_026_error():
    with pytest.raises(pals.UpdateCheck):
        analyze_test("026_error")

def test_027_error():
    with pytest.raises(pals.UpdateCheck):
        analyze_test("027_error")

def test_028_ok():
    analyze_test("028_ok")

def test_029_ok():
    analyze_test("029_ok")

def test_030_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        analyze_test("030_error")

def test_031_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        analyze_test("031_error")

def test_032_error():
    with pytest.raises(pals.ApplyRatorTypeCheck):
        analyze_test("032_error")

def test_034_ok():
    analyze_test("034_ok")

def test_035_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        analyze_test("035_error")

def test_036_ok():
    analyze_test("036_ok")

def test_037_ok():
    analyze_test("037_ok")

def test_038_ok():
    analyze_test("038_ok")

def test_039_error():
    with pytest.raises(Exception):
        analyze_test("039_error")

def test_040_ok():
    analyze_test("040_ok")

def test_041_error():
    with pytest.raises(Exception):
        analyze_test("041_error")

def test_042_error():
    with pytest.raises(pals.LookupDecCheck):
        analyze_test("042_error")

def test_043_error():
    with pytest.raises(pals.LookupDecCheck):
        analyze_test("043_error")


def test_044_ok():
    analyze_test("044_ok")

def test_045_error():
    with pytest.raises(pals.LookupDecCheck):
        analyze_test("045_error")

def test_046_error():
    with pytest.raises(pals.LookupDecCheck):
        analyze_test("046_error")

def test_047_error():
    with pytest.raises(pals.LookupDecCheck):
        analyze_test("047_error")

def test_048_error():
    analyze_test("048_ok")

def test_049_error():
    with pytest.raises(pals.LookupDecCheck):
        analyze_test("049_error")

def test_050_error():
    with pytest.raises(pals.LookupDecCheck):
        analyze_test("050_error")

def test_051_error():
    with pytest.raises(pals.LookupDecCheck):
        analyze_test("051_error")

def test_052_error():
    with pytest.raises(pals.LookupDecCheck):
        analyze_test("052_error")

def test_053_ok():
    analyze_test("053_ok")

def test_054_ok():
    analyze_test("054_ok")

def test_055_error():
    code, aux = analyze_test("055_error", 9)
    # print(code)
    # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    t = aux.local_env.get('type')
    assert t
    assert isinstance(t.type, pals.IntLitType)
    with pytest.raises(pals.ApplyRatorTypeCheck):
        analyze_test("055_error", 10)

def test_055_1_ok():
    analyze_test("055_1_ok")

def test_055_2_ok():
    analyze_test("055_2_ok")

def test_056_error():
    code, aux = analyze_test("056_error", 8)
    # print(code)
    # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    f = aux.local_env.get('f')
    assert f 
    assert isinstance(f.type, pals.IntLitType)
    with pytest.raises(pals.ApplyRatorTypeCheck):
        analyze_test("056_error")

def test_057_error():
    code, aux = analyze_test("057_error", 9)
    # print(code)
    # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    i = aux.local_env.get('i')
    assert i == None 
    with pytest.raises(pals.LookupDecCheck):
        analyze_test("057_error")

def test_057_1_error():
    with pytest.raises(pals.LookupDecCheck):
        analyze_test("057_1_error")

def test_057_2_error():
    with pytest.raises(pals.LookupDecCheck):
        analyze_test("057_2_error")

def test_058_ok():
    code, aux = analyze_test("058_ok", 5)
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
    analyze_test("059_ok")

def test_060_ok():
    code, aux = analyze_test("060_ok", 4)
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
    code, aux = analyze_test("061_ok", 2)
    # print(code)
    # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    final_str = aux.local_env.get('final_str')
    assert final_str 
    final_str_type = final_str.type
    assert isinstance(final_str_type, pals.RecordType)
    assert final_str_type.class_key == "builtins.str"

def test_062_ok():
    analyze_test("062_ok")

def test_063_error():
    with pytest.raises(pals.AssignTypeCheck):
        analyze_test("063_error")

def test_064_ok():
    analyze_test("064_ok")

def test_065_ok():
    code_pre, aux_pre = analyze_test("065_ok", 2)
    # print(code_pre)
    # print(json.dumps(pals.from_env_to_primitive_verbose(aux_pre.local_env), indent=4))
    xs_pre = aux_pre.local_env.get('xs')
    il = pals.IntLitType
    assert xs_pre 
    assert xs_pre.type == pals.ListLitType(item_types=(il('1'),il('2'),il('3')))

    code_post, aux_post = analyze_test("065_ok", 3)
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
    code_pre, aux_pre = analyze_test("066_ok", 2)
    # print(code_pre)
    # print(json.dumps(pals.from_env_to_primitive_verbose(aux_pre.local_env), indent=4))
    xs_pre = aux_pre.local_env.get('xs')
    il = pals.IntLitType
    assert xs_pre 
    assert xs_pre.type == pals.ListLitType(item_types=(il('1'),il('2'),il('3')))

    code_post, aux_post = analyze_test("066_ok", 3)
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
    code, aux = analyze_test("067_ok", 4)
    # print(code)
    # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    assert 'x' in aux.local_env
    code, aux = analyze_test("067_ok", 7)
    # print(code)
    # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    assert 'x' not in aux.local_env
    assert 'self' in aux.local_env

def test_068_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        analyze_test("068_error")

def test_069_ok():
    analyze_test("069_ok")


def test_070_0_ok():
    code, aux = analyze_test("070_0_ok",2)
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
    analyze_test("070_1_ok")

def test_070_2_ok():
    analyze_test("070_2_ok")

def test_070_3_ok():
    code, aux = analyze_test("070_3_ok", 9)
    print(code)
    print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    a = aux.local_env.get("a")
    assert a
    assert a.type == make_RecordType(class_key="070_3_ok.A", type_args=(
        make_RecordType(class_key="builtins.int"),
    ))

def test_070_4_ok():
    code, aux = analyze_test("070_4_ok", 7)
    print(code)
    print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    x = aux.local_env.get("x")
    assert x
    assert x.type == make_RecordType(class_key="builtins.int")

def test_070_ok():
    analyze_test("070_ok")

def test_071_ok():
    analyze_test("071_ok")

def test_072_ok():
    analyze_test("072_ok")

def test_073_ok():
    analyze_test("073_ok")

def test_074_1_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        analyze_test("074_1_error")

def test_074_ok():
    analyze_test("074_ok")

def test_075_1_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        analyze_test("075_1_error")

def test_075_ok():
    analyze_test("075_ok")

def test_076_ok():
    analyze_test("076_ok")

def test_077_ok():
    analyze_test("077_ok")

def test_078_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        analyze_test("078_error")

def test_079_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        analyze_test("079_error")

def test_080_ok():
    analyze_test("080_ok")

def test_081_ok():
    code, aux = analyze_test("081_ok", 4)
    # print(code)
    # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    x = aux.local_env.get("x")
    assert x and x.type == pals.IntLitType('1')
    y = aux.local_env.get("y")
    assert y and y.type == pals.IntLitType('2')
    z = aux.local_env.get("z")
    assert z and z.type == pals.make_RecordType(class_key="builtins.int")

def test_082_ok():
    # test for convergence in subsumption with combined inheritance and protocols in Generator <: Iterator
    analyze_test("082_ok")

def test_083_ok():
    # test class type as param type 
    analyze_test("083_ok")

def test_084_ok():
    analyze_test("084_ok")

def test_params_dont_traverse():
    (inspect, kill) = spawn_inspect("params_dont_traverse")
    try:
        for param_sep in 9, 14, 24, 31, 40, 47, 53:
            code, aux = inspect(param_sep)
            assert not aux.local_env
            # print(code)
            # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))

        code, aux = inspect(54)
        # print(code)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
        for sym in 'x', 'y', 'zs', 'a', 'b', 'cs':
            assert sym in aux.local_env
    finally:
        kill()

if __name__ == "__main__":
    pass