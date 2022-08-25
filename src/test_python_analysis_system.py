from pyrsistent.typing import PMap, PSet
from pyrsistent import pmap, m, pset, s

from typing import Callable
from tapas_base.abstract_token_construct_autogen import unguard_abstract_token

from tapas_lib import generic_tree_system, python_aux_system as pals
from tapas_lib import python_ast_system as pas
from tapas_lib import python_generic_tree_system as pgs 
from tapas_lib import python_abstract_token_system as pats
from tapas_base import abstract_token_system as ats
from tapas_base import util_system as us

import json
import pytest

package : PMap[str, pals.ModulePackage] = pals.with_cache('tapas_res/stub_cache', pals.analyze_typeshed)
# package = pals.analyze_numpy_stubs(package)

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

def analyze_test(module_name : str, line_limit: int = -1, package = package) -> tuple[str, pals.InherAux]:

    code = load_source(module_name) 
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

def check(module_name : str, checks = pals.all_checks) -> None:
    (inspect, kill) = spawn_inspect(module_name, checks)
    inspect(-1)
    kill()

def check_code(module_name : str, code : str, checks = pals.all_checks, package = package) -> None:
    (inspect, kill) = spawn_inspect_code(module_name, code, checks, package)
    inspect(-1)
    kill()

def spawn_inspect(module_name : str, checks = pals.all_checks, package = package) -> tuple[Callable[[int], tuple[str, pals.InherAux]], Callable[[], None]]:
    code = load_source(module_name) 
    return spawn_inspect_code(module_name, code, checks, package)

def spawn_inspect_code(module_name, code : str, checks = pals.all_checks, package = package) -> tuple[Callable[[int], tuple[str, pals.InherAux]], Callable[[], None]]:
    gnode = pgs.parse(code)
    # print(pgs.dump(gnode))
    # raise Exception()

    mod = pas.parse_from_generic_tree(gnode)
    abstract_tokens = pas.serialize(mod)
    # print(pas.dump(mod))
    # raise Exception()

    partial_tokens = [] 
    client : pals.Client = pals.spawn_analysis(package, module_name, checks)
    partial_code = ""
    inher_aux : pals.InherAux = client.init
    max_len = len(abstract_tokens)

    def kill():
        class TestKill(Exception): pass
        client.kill(TestKill())


    def inspect(l : int) -> tuple[str, pals.InherAux]:
        nonlocal partial_code
        nonlocal inher_aux
        l = l if l >= 0 else max_len
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
    check("000_0_ok")

def test_000_1_error():
    with pytest.raises(pals.LookupDecCheck):
        check("000_1_error")



def test_000_2_error():
    with pytest.raises(pals.LookupInitCheck):
        check("000_2_error")
    code = load_source("000_2_error")
    assert pals.analyze_summary(package, "main", code) == "lookup_init_check"

def test_000_3_ok():
    check("000_3_ok")

def test_000_4_error():
    with pytest.raises(pals.LookupInitCheck):
        check("000_4_error")

def test_001_ok():
    check("001_ok")

def test_002_error():
    with pytest.raises(pals.AssignTypeCheck):
        check("002_error")

def test_003_ok():
    check("003_ok")

def test_004_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        check("004_error")

def test_005_ok():
        check("005_ok")

def test_006_error():
    with pytest.raises(pals.AssignTypeCheck):
        check("006_error")

def test_007_ok():
    check("007_ok")

def test_008_error():
    with pytest.raises(pals.AssignTypeCheck):
        check("008_error")

def test_009_error():
    with pytest.raises(pals.AssignTypeCheck):
        check("009_error")

def test_010_ok():
    check("010_ok")

def test_011_error():
    with pytest.raises(pals.AssignTypeCheck):
        check("011_error")

def test_012_ok():
    check("012_ok")

def test_013_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        check("013_error")

def test_014_ok():
    check("014_ok")

def test_015_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        check("015_error")

def test_016_error():
    with pytest.raises(pals.ReturnTypeCheck):
        check("016_error")

def test_017_ok():
    check("017_ok")

def test_018_ok():
    check("018_ok")

def test_019_error():
    with pytest.raises(pals.LookupTypeCheck):
        check("019_error")

def test_020_ok():
    check("020_ok")

def test_021_error():
    with pytest.raises(pals.UpdateCheck):
        check("021_error")

def test_022_ok():
    check("022_ok")

def test_023_ok():
    check("023_ok")

def test_024_ok():
    check("024_ok")

def test_025_error():
    with pytest.raises(pals.UpdateCheck):
        check("025_error")

def test_026_error():
    with pytest.raises(pals.UpdateCheck):
        check("026_error")

def test_027_error():
    with pytest.raises(pals.UpdateCheck):
        check("027_error")

def test_028_ok():
    check("028_ok")

def test_029_ok():
    check("029_ok")

def test_030_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        check("030_error")

def test_031_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        check("031_error")

def test_032_error():
    with pytest.raises(pals.ApplyRatorTypeCheck):
        check("032_error")

def test_034_ok():
    check("034_ok")

def test_035_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        check("035_error")

def test_036_ok():
    check("036_ok")

def test_037_ok():
    check("037_ok")

def test_038_ok():
    check("038_ok")

def test_039_error():
    with pytest.raises(Exception):
        check("039_error")

def test_040_ok():
    check("040_ok")

def test_041_error():
    with pytest.raises(Exception):
        check("041_error")

def test_042_error():
    with pytest.raises(pals.LookupDecCheck):
        check("042_error")

def test_043_error():
    with pytest.raises(pals.LookupDecCheck):
        check("043_error")


def test_044_ok():
    check("044_ok")

def test_045_error():
    with pytest.raises(pals.LookupDecCheck):
        check("045_error")

def test_046_error():
    with pytest.raises(pals.LookupDecCheck):
        check("046_error")

def test_047_error():
    with pytest.raises(pals.LookupDecCheck):
        check("047_error")

def test_048_error():
    check("048_ok")

def test_049_error():
    with pytest.raises(pals.LookupDecCheck):
        check("049_error")

def test_050_error():
    with pytest.raises(pals.LookupDecCheck):
        check("050_error")

def test_051_error():
    with pytest.raises(pals.LookupDecCheck):
        check("051_error")

def test_052_error():
    with pytest.raises(pals.LookupDecCheck):
        check("052_error")

def test_053_ok():
    check("053_ok")

def test_054_ok():
    check("054_ok")

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
    check("055_1_ok")

def test_055_2_ok():
    check("055_2_ok")

def test_056_error():
    code, aux = analyze_test("056_error", 8)
    # print(code)
    # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    f = aux.local_env.get('f')
    assert f 
    assert isinstance(f.type, pals.IntLitType)
    with pytest.raises(pals.ApplyRatorTypeCheck):
        check("056_error")

def test_057_error():
    code, aux = analyze_test("057_error", 9)
    # print(code)
    # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    i = aux.local_env.get('i')
    assert i == None 
    with pytest.raises(pals.LookupDecCheck):
        check("057_error")

def test_057_1_error():
    with pytest.raises(pals.LookupDecCheck):
        check("057_1_error")

def test_057_2_error():
    with pytest.raises(pals.LookupDecCheck):
        check("057_2_error")

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
    check("059_ok")

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
    check("062_ok")

def test_063_error():
    with pytest.raises(pals.AssignTypeCheck):
        check("063_error")

def test_064_ok():
    check("064_ok")

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
    xs_post_type = xs_post.type
    assert isinstance(xs_post_type, pals.RecordType) and xs_post_type.class_key == "builtins.list"
    assert len(xs_post_type.type_args) == 1
    assert len(xs_post_type.type_args) == 1
    xs_post_content_type = xs_post_type.type_args[0]
    assert isinstance(xs_post_content_type, pals.UnionType)
    xs_post_type_choices = xs_post_content_type.type_choices
    assert len(xs_post_type_choices) == 2
    assert us.exists(xs_post_type_choices, lambda choice :
        isinstance(choice, pals.RecordType) and choice.class_key == "builtins.int"
    )

def test_goldilocks_object():
    code_pre, aux_pre = analyze_test("goldilocks_object", 2)
    # print(code_pre)
    # print(json.dumps(pals.from_env_to_primitive_verbose(aux_pre.local_env), indent=4))
    xs_pre = aux_pre.local_env.get('xs')
    il = pals.IntLitType
    assert xs_pre 
    assert xs_pre.type == pals.ListLitType(item_types=(il('1'),il('2'),il('3')))

    code_post, aux_post = analyze_test("goldilocks_object", 3)
    xs_post = aux_post.local_env.get('xs')
    # print(code_post)
    # print(json.dumps(pals.from_env_to_primitive_verbose(aux_post.local_env), indent=4))
    assert xs_post 
    xs_post_type = xs_post.type
    assert isinstance(xs_post_type, pals.RecordType) and xs_post_type.class_key == "builtins.list"
    assert len(xs_post_type.type_args) == 1
    xs_post_content_type = xs_post_type.type_args[0]
    assert isinstance(xs_post_content_type, pals.UnionType)
    xs_post_type_choices = xs_post_content_type.type_choices
    assert len(xs_post_type_choices) == 3
    assert us.exists(xs_post_type_choices, lambda choice :
        isinstance(choice, pals.RecordType) and choice.class_key == "builtins.int"
    )
    assert us.exists(xs_post_type_choices, lambda choice :
        isinstance(choice, pals.RecordType) and choice.class_key == "builtins.str"
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
        check("068_error")

def test_069_ok():
    check("069_ok")

def test_070_0_ok():
    code, aux = analyze_test("070_0_ok",2)
    # print(code)
    # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    x = aux.local_env.get("x")
    assert x
    x_type = x.type
    assert isinstance(x_type, pals.RecordType)
    assert x_type.class_key == "builtins.list"
    x_type_args = x_type.type_args
    assert len(x_type_args) == 1 
    x_content_type = x_type_args[0]
    assert isinstance(x_content_type, pals.UnionType)
    x_content_choices = x_content_type.type_choices
    assert us.exists(x_content_choices, lambda choice :
        isinstance(choice, pals.RecordType) and choice.class_key == "builtins.int"
    )

def test_070_1_ok():
    check("070_1_ok")

def test_070_2_ok():
    check("070_2_ok")

def test_070_3_ok():
    code, aux = analyze_test("070_3_ok", 9)
    # print(code)
    # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    a = aux.local_env.get("a")
    assert a
    a_type = a.type 
    assert isinstance(a_type, pals.RecordType)
    assert len(a_type.type_args) == 1
    a_type_content = a_type.type_args[0]
    assert isinstance(a_type_content, pals.UnionType)
    xs_post_type_choices = a_type_content.type_choices
    assert len(xs_post_type_choices) == 2
    assert us.exists(xs_post_type_choices, lambda choice :
        isinstance(choice, pals.RecordType) and choice.class_key == "builtins.int"
    )
    assert us.exists(xs_post_type_choices, lambda choice :
        isinstance(choice, pals.VarType)
    )

def test_070_4_ok():
    code, aux = analyze_test("070_4_ok", 7)
    print(code)
    print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    x = aux.local_env.get("x")
    assert x
    assert x.type == pals.make_RecordType(class_key="builtins.int")

def test_070_ok():
    check("070_ok")

def test_071_ok():
    check("071_ok")

def test_072_ok():
    check("072_ok")

def test_073_ok():
    check("073_ok")

def test_080_ok():
    check("080_ok")

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
    check("082_ok")

def test_083_ok():
    # test class type as param type 
    check("083_ok")

def test_084_ok():
    check("084_ok")

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

def test_converges():
    (inspect, kill) = spawn_inspect("converges", pset())
    try:
        code, aux = inspect(-1)
        # print(code)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    finally:
        kill()

def test_import_alias():
    (inspect, kill) = spawn_inspect("import_alias")
    try:
        code, aux = inspect(20)
        dumps = aux.local_env.get("dumps")
        assert dumps
        assert isinstance(dumps.type, pals.FunctionType)
        # print(code)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
        inspect(-1)
    finally:
        kill()

def test_import_from_alias():
    (inspect, kill) = spawn_inspect("import_from_alias")
    try:
        code, aux = inspect(10)
        d = aux.local_env.get("d")
        assert d 
        assert isinstance(d.type, pals.FunctionType)
        # print(code)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
        inspect(-1)
    finally:
        kill()


def test_params_1_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        check("params_1_error")

def test_params_2_ok():
    check("params_2_ok")

def test_params_3_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        check("params_3_error")

def test_args_splat_1_ok():
    check("args_splat_1_ok")

def test_splat_bundle_1_ok():
    check("splat_bundle_1_ok")

def test_params_4_ok():
    check("params_4_ok")

def test_params_5_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        check("params_5_error")

def test_params_6_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        check("params_6_error")

def test_params_7_ok():
    check("params_7_ok")

def test_params_8_ok():
    check("params_8_ok")


def test_class_field_ok():
    (inspect, kill) = spawn_inspect("class_field_ok")
    try:
        code, aux = inspect(20)
        # print(code)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))

        code, aux = inspect(30)
        # print(code)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))

        code, aux = inspect(40)
        # print(code)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))

        code, aux = inspect(45)
        # print(code)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))

        inspect(-1)
    finally:
        kill()

# def test_class_field_error_1():
#     with pytest.raises(pals.LookupDecCheck):
#         check("class_field_error_1")

# def test_class_field_error_2():
#     with pytest.raises(pals.LookupDecCheck):
#         check("class_field_error_2")

# def test_class_field_error_3():
#     with pytest.raises(pals.LookupDecCheck):
#         check("class_field_error_3")

# def test_class_field_error_4():
#     with pytest.raises(pals.LookupDecCheck):
#         check("class_field_error_4")

def test_expression_list_splat_ok():
    check("expression_list_splat_ok")

# def test_expression_list_unbound_splat_ok():
#     check("expression_list_unbound_splat_ok")

# def test_import_numpy():
#     (inspect, kill) = spawn_inspect("import_numpy")
#     try:
#         code, aux = inspect(8)
#         arange = aux.local_env.get("arange")
#         print(code)
#         print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
#         assert arange
#         assert not isinstance(arange.type, pals.AnyType)
#         inspect(-1)
#     finally:
#         kill()

def test_str_type_annotation():
    (inspect, kill) = spawn_inspect("str_type_annotation")
    try:
        code, aux = inspect(16)
        x = aux.local_env.get("x")
        assert x
        t = x.type
        assert isinstance(t, pals.TupleLitType)
        int_type = t.item_types[0]
        assert isinstance(int_type, pals.RecordType)
        assert int_type.class_key == "builtins.int"
        str_type = t.item_types[1]
        assert isinstance(str_type, pals.RecordType)
        assert str_type.class_key == "builtins.str"
        # print(code)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
        inspect(-1)
    finally:
        kill()


if __name__ == "__main__":
    check_code("main", '''

def foo(x):
    return x

@foo #hello
# between decorators 
@foo #bye
class A: # this is a class header comment 
    pass

def foo(x : int): # this is a function header comment 
    # whole line comment 0 
    y = x + 1 # comment after stmt
    z = y + 1 
    # whole line comment 1 

    ''', checks = pals.all_checks, package=m())
    pass