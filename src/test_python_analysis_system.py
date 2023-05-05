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
from tapas_base.util_system import InsertOrderMap, iom

import json
import pytest

from tapas_lib.python_aux_construct_autogen import ModulePackage
package : InsertOrderMap[str, pals.ModulePackage] = pals.with_cache('tapas_res/cache/typeshed_cache', lambda: pals.analyze_typeshed(), False)
# package : InsertOrderMap[str, pals.ModulePackage] = iom()
# package = pals.with_cache('tapas_res/cache/pandas_cache', lambda: pals.analyze_pandas_stubs(package, 3))
# package = pals.analyze_pandas_stubs(pals.analyze_typeshed())
# package = pals.analyze_numpy_stubs(package)


def check(module_name : str, checks = pals.all_checks) -> None:
    (inspect, kill) = spawn_inspect(module_name, checks)
    try:
        inspect('')
    finally:
        kill()

def check_code(module_name : str, code : str, checks = pals.all_checks) -> None:
    (inspect, kill) = spawn_inspect_code(module_name, code, checks)
    try:
        inspect('')
    finally:
        kill()

def load_source(name : str) -> str:
    path = us.project_path(f"tapas_res/python/{name}.py")
    with open(path, 'r') as f:
        return f.read()


def spawn_inspect(module_name : str, checks = pals.all_checks, package = package) -> tuple[Callable[[str], tuple[str, pals.InherAux]], Callable[[], None]]:
    code = load_source(module_name) 
    return spawn_inspect_code(module_name, code, checks)


def spawn_inspect_code(module_name, code : str, checks = pals.all_checks) -> tuple[Callable[[str], tuple[str, pals.InherAux]], Callable[[], None]]:
    return pals.spawn_inspect_code(module_name, code, package, checks)

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
    inspect, kill = spawn_inspect("055_error")
    try:
        code, aux = inspect('type') 
        t = aux.local_env['type']
        # print(code)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
        assert isinstance(t.type, pals.IntLitType)

        with pytest.raises(pals.ApplyRatorTypeCheck):
            inspect('')
    finally:
        kill()

def test_055_1_ok():
    check("055_1_ok")

def test_055_2_ok():
    check("055_2_ok")

def test_056_error():
    inspect, kill = spawn_inspect("056_error")
    try:
        code, aux = inspect('f')
        f = aux.local_env['f']
        # print(code)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
        assert isinstance(f.type, pals.IntLitType)

        with pytest.raises(pals.ApplyRatorTypeCheck):
            inspect('')
    finally:
        kill()

def test_057_error():
    code = '''
def remove_Occ(s, ch):
  for i in range(len(s)):
    if s[i] == ch:
      s = (s[0:i:] + s[(i + 1)::])
      ch += 1

  _break = ''

  if ch == 2:
    s = s(ch)
  if ch[(i + len(ch))] == s:
    len(ch)
    '''
    inspect, kill = spawn_inspect_code("main", code)
    try:
        code, aux = inspect('_break')
        # print(code)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
        i = aux.local_env.get('i')
        assert i == None 
        with pytest.raises(pals.LookupDecCheck):
            inspect('')
    finally:
        kill()

def test_057_1_error():
    with pytest.raises(pals.LookupDecCheck):
        check("057_1_error")

def test_057_2_error():
    with pytest.raises(pals.LookupDecCheck):
        check("057_2_error")

def test_058_ok():
    inspect, kill = spawn_inspect("058_ok")
    try:
        code, aux = inspect('x')
        # print(code)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
        x = aux.local_env['x']
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
    finally:
        kill()

def test_059_ok():
    check("059_ok")

def test_060_ok():
    inspect, kill = spawn_inspect("060_ok")
    try:
        code, aux = inspect('foo')
        # print(code)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
        foo = aux.local_env['foo']
        foo_type = foo.type
        assert isinstance(foo_type, pals.FunctionType)
        foo_return_type = foo_type.return_type
        assert isinstance(foo_return_type, pals.RecordType)
        assert foo_return_type.class_key == "builtins.int"
    finally:
        kill()

def test_061_ok():
    inspect, kill = spawn_inspect("061_ok")
    try:
        code, aux = inspect('final_str')
        # print(code)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
        final_str = aux.local_env['final_str']
        final_str_type = final_str.type
        assert isinstance(final_str_type, pals.RecordType)
        assert final_str_type.class_key == "builtins.str"
    finally:
        kill()

def test_062_ok():
    check("062_ok")

def test_063_error():
    with pytest.raises(pals.AssignTypeCheck):
        check("063_error")

def test_064_ok():
    check("064_ok")

def test_065_ok():
    code = '''
xs = [1,2,3]
xs.append(4)
_break = ''
pass
    '''

    inspect, kill = spawn_inspect_code('main', code)
    try:
        code_pre, aux_pre = inspect("xs")
        # print(code_pre)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux_pre.local_env), indent=4))
        xs_pre = aux_pre.local_env['xs']
        il = pals.IntLitType
        assert xs_pre 
        assert xs_pre.type == pals.ListLitType(item_types=(il('1'),il('2'),il('3')))

        code_post, aux_post = inspect("_break")
        # print(code_post)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux_post.local_env), indent=4))
        xs_post = aux_post.local_env['xs']
        il = pals.IntLitType
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
    finally:
        kill()

def test_goldilocks_object():
    code = '''
#pyright is too strict here: this should be allowed since there's no annotation
xs = [1,2,3]
xs.append("hi")
_break = ''
pass
    '''
    inspect, kill = spawn_inspect_code("main", code)
    try:
        code_pre, aux_pre = inspect('xs')
        # print(code_pre)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux_pre.local_env), indent=4))
        xs_pre = aux_pre.local_env['xs']
        il = pals.IntLitType
        assert xs_pre.type == pals.ListLitType(item_types=(il('1'),il('2'),il('3')))

        code_post, aux_post = inspect('_break')
        xs_post = aux_post.local_env['xs']
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

    finally:
        kill()

def test_067_ok():
    inspect, kill = spawn_inspect("067_ok")
    try:
        code, aux = inspect('x')
        # print(code)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
        code, aux = inspect('self')
        # print(code)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
        assert 'x' not in aux.local_env
    finally:
        kill()

def test_068_error():
    with pytest.raises(pals.ApplyArgTypeCheck):
        check("068_error")

def test_069_ok():
    check("069_ok")

def test_070_0_ok():
    inspect, kill = spawn_inspect("070_0_ok")
    try:
        code, aux = inspect('x')
        # print(code)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
        x = aux.local_env['x']
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
    finally:
        kill()

def test_070_1_ok():
    check("070_1_ok")

def test_070_2_ok():
    check("070_2_ok")

def test_070_3_ok():
    inspect, kill = spawn_inspect("070_3_ok")
    try:
        code, aux = inspect('a')
        # print(code)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
        a = aux.local_env['a']
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
    finally:
        kill()

def test_070_4_ok():
    code = '''
from typing import TypeVar, Generic
X = TypeVar("X")
def foo(x : X) -> X:
    return x
y = foo(1)
pass

    '''
    inspect, kill = spawn_inspect_code("main", code)
    try:
        code, aux = inspect('y')
        # print(code)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
        x = aux.local_env['y']
        assert x.type == pals.make_RecordType(class_key="builtins.int")
    finally:
        kill()

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
    inspect, kill = spawn_inspect("081_ok")
    try:
        code, aux = inspect('x')
        # print(code)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
        x = aux.local_env['x']
        assert x.type == pals.IntLitType('1')
        code, aux = inspect('y')
        y = aux.local_env['y']
        assert y.type == pals.IntLitType('2')
        code, aux = inspect('z')
        z = aux.local_env['z']
        assert z.type == pals.make_RecordType(class_key="builtins.int")
    finally:
        kill()

def test_082_ok():
    # test for convergence in subsumption with combined inheritance and protocols in Generator <: Iterator
    check("082_ok")

def test_083_ok():
    # test class type as param type 
    check("083_ok")

def test_084_ok():
    check("084_ok")

def test_params_dont_traverse():
    code = '''
def foo(x = 0, y : int = 1, *zs : int, a : int = 4, b = 5, **cs : int):
    _break = ''
    pass
    return
    '''
    (inspect, kill) = spawn_inspect_code('main', code)
    try:
        code, aux = inspect('x')
        # print(code)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
        for sym in 'x', 'y', 'zs', 'a', 'b', 'cs':
            assert sym in aux.local_env
    finally:
        kill()

def test_converges():
    (inspect, kill) = spawn_inspect("converges", pset())
    try:
        code, aux = inspect('')
        # print(code)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    finally:
        kill()

def test_import_alias():
    (inspect, kill) = spawn_inspect("import_alias")
    try:
        code, aux = inspect('dumps')
        dumps = aux.local_env['dumps']
        assert isinstance(dumps.type, pals.FunctionType)
        # print(code)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
        inspect('')
    finally:
        kill()

def test_import_from_alias():
    (inspect, kill) = spawn_inspect("import_from_alias")
    try:
        code, aux = inspect('d')
        d = aux.local_env['d']
        assert d 
        assert isinstance(d.type, pals.FunctionType)
        # print(code)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
        inspect('')
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
    code = '''
from typing import Type
class A():
    a = 1
    b = a + 1
    def uno(self):
        with open("") as self.f:
            pass
        self.x = 1
        self.z : int = 2
        pass

    @classmethod
    def dos(cls):
        (cls.y, i) = pair = 1, 2
        cls.w : int = 2
        return (i, pair)

    _break = ''


ai = A().a
bi = A().b

a = A.a
b = A.b

f = A().f
x = A().x
z = A().z

yi = A().y
wi = A().w

y = A.y
w = A.w
pass
    '''

    (inspect, kill) = spawn_inspect_code('main', code)
    try:
        inspect('')
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
        code, aux = inspect('x')
        x = aux.local_env['x']
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
        inspect('')
    finally:
        kill()

def test_pandas():
# import pdb; pdb.set_trace()
    code = '''
import pandas as pd
d = {'col1': [0, 1, 2, 3], 'col2': pd.Series([2, 3], index=[2, 3])}
df = pd.DataFrame(data=d, index=[0, 1, 2, 3])
dates = pd.date_range("20130101", periods=6)
index=df.index
res=df.to_numpy()
df2=df.T
df3=df[0:2]
df4 = df.dtypes
pass
    '''

# df4=df.iloc[1]


    (inspect, kill) = spawn_inspect_code("main", code, checks = pset())
    try:
        code, aux = inspect('df4')
        print(code)
        print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))


        inspect('')
    finally:
        kill()


def test_attribute_1():

    code = '''
        a = True
        b = a[-1]
        c = b.shape()
        _break = ''
        pass
    '''

    (inspect, kill) = spawn_inspect_code("main", code)

    with pytest.raises(pals.LookupTypeCheck):
        try:
            code, aux = inspect('_break')
            print(code)
            print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))


            inspect('')
        finally:
            kill()

def test_attribute_2():

    code = '''
        x = (- 0.75)
        y = x.apply()
        _break = ''
        pass
    '''

    (inspect, kill) = spawn_inspect_code("main", code)

    with pytest.raises(pals.LookupTypeCheck):
        try:
            code, aux = inspect('_break')
            print(code)
            print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))


            inspect('')
        finally:
            kill()

def test_union_typing_1():
    code = '''
    from typing import Union
    x : Union[int, str] = "hello"
    y : Union[str, int] = x 
    _break = ''
    pass
    '''

    (inspect, kill) = spawn_inspect_code('main', code)
    try:
        code, aux = inspect('x')
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
        assert isinstance(aux.local_env['x'].type, pals.UnionType)
        code, aux = inspect('y')
        assert isinstance(aux.local_env['y'].type, pals.UnionType)
        # print(code)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))

    finally:
        kill()

def test_union_typing_2():
    code = '''
    from typing import Union
    x : Union[int, str] = "hello"
    y : Union[str] = x 
    _break = ''
    pass
    '''
    with pytest.raises(pals.AssignTypeCheck):
        check_code('main', code)

def test_union_typing_3():
    code = '''
    from typing import Union
    x : int | str = "hello"
    y : str | int = x 
    _break = ''
    pass
    '''

    (inspect, kill) = spawn_inspect_code('main', code)
    try:
        code, aux = inspect('x')
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
        assert isinstance(aux.local_env['x'].type, pals.UnionType)
        code, aux = inspect('y')
        assert isinstance(aux.local_env['y'].type, pals.UnionType)
        # print(code)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))

    finally:
        kill()



def test_shadowed_package_1():
    leaf_package = pals.analyze_code(package, "top.leaf", '''
def foo(x : int): str = ...
    ''', checks=pset())

    (inspect, kill) = pals.spawn_inspect_code('top', '''
from top import leaf as leaf 
x = leaf.foo
pass
    ''', leaf_package, pset())
    try:
        code, aux = inspect('x')
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
        assert isinstance(aux.local_env['x'].type, pals.FunctionType)

    finally:
        kill()

def test_shadowed_package_2():
    leaf_package = pals.analyze_code(package, "top.leaf", '''
def foo(x : int): str = ...
    ''', checks=pset())

    top_package = pals.analyze_code(leaf_package, "top", '''
from top import leaf as leaf 
    ''', checks=pset())

    (inspect, kill) = pals.spawn_inspect_code('main', '''
from top import leaf
x = leaf.foo
pass
    ''', top_package, pset())
    try:
        code, aux = inspect('x')
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
        assert isinstance(aux.local_env['x'].type, pals.FunctionType)

    finally:
        kill()

def test_shadowed_package_3():
    leaf_package = pals.analyze_code(package, "top.leaf", '''
def foo(x : int): str = ...
    ''', checks=pset())

    (inspect, kill) = pals.spawn_inspect_code('top', '''
from top import leaf as leaf
x = leaf.foo
pass
    ''', leaf_package, pset())
    try:
        code, aux = inspect('x')
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
        assert isinstance(aux.local_env['x'].type, pals.FunctionType)
        assert isinstance(aux.local_env['leaf'].type, pals.ModuleType)

    finally:
        kill()

def test_relative_package():
    leaf_package = pals.analyze_code(package, "top.leaf", '''
def foo(x : int): str = ...
    ''', checks=pset())

    (inspect, kill) = pals.spawn_inspect_code('top', '''
from . import leaf as leaf
x = leaf.foo
pass
    ''', leaf_package, pset())
    try:
        code, aux = inspect('x')
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
        assert isinstance(aux.local_env['x'].type, pals.FunctionType)
        assert isinstance(aux.local_env['leaf'].type, pals.ModuleType)

    finally:
        kill()


def test_analysis_complete():
    abstract_tokens = pas.serialize(pas.parse('''
x = 1
y = 2
pass
    ''')) + (ats.from_primitive(['P', 'grammar', 'conditions', 'NoCond']),)

    partial_tokens = [] 
    client : pals.Client = pals.spawn_analysis(package, 'main', pset())
    partial_code = ""
    inher_aux : pals.InherAux = client.init

    for i, token in enumerate(abstract_tokens):
        partial_tokens.append(token)
        partial_code = pats.concretize(tuple(partial_tokens))
        if i < len(abstract_tokens) - 1:
            inher_aux = client.next(token)
        else:
            with pytest.raises(pals.AnalysisComplete):
                inher_aux = client.next(token)

def test_fresh_type_var():
    code = '''
LOYALBOOKS_GENRE = list()
LOYALBOOKS_GENRE.append(["Adventure", "Adventure"])
LOYALBOOKS_GENRE.append(["Advice", "Advice"])
LOYALBOOKS_GENRE.append(["Art", "Art"])
LOYALBOOKS_GENRE.append(["Ancient Texts", "Ancient_Texts"])
LOYALBOOKS_GENRE.append(["Animals", "Animals"])
LOYALBOOKS_GENRE.append(["Biography", "Biography"])
LOYALBOOKS_GENRE.append(["Children", "Children"])
LOYALBOOKS_GENRE.append(["Classics (antiquity)", "Classics_antiquity"])
LOYALBOOKS_GENRE.append(["Comedy", "Comedy"])
_break = ""
pass
    '''

    (inspect, kill) = pals.spawn_inspect_code('main', code, package, pset())
    try:
        code, aux = inspect('_break')
        lb_type = aux.local_env['LOYALBOOKS_GENRE'].type 
        assert isinstance(lb_type, pals.RecordType)
        assert lb_type.class_key == "builtins.list" 
        assert len(lb_type.type_args) == 1
        targ = lb_type.type_args[0]
        assert isinstance(targ, pals.UnionType)
        assert len(targ.type_choices) == 2

    finally:
        kill()


def test_typetype_1():
    code = '''
A = type
B = type[int]
pass
    '''

    # (inspect, kill) = pals.spawn_inspect_code('main', code, package, set())
    (inspect, kill) = pals.spawn_inspect_code('main', code, package, pals.all_checks)
    try:
        code, aux = inspect('C')
        A = aux.local_env['A'].type
        assert isinstance(A, pals.TypeType)
        assert isinstance(A.content, pals.RecordType)
        assert A.content.class_key == "builtins.type"
        B = aux.local_env['B'].type
        assert isinstance(B, pals.TypeType)
        assert isinstance(B.content, pals.TypeType)
        B_int = B.content.content
        assert isinstance(B_int, pals.RecordType)
        assert B_int.class_key == "builtins.int"
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    finally:
        kill()

def test_typetype_2():
    code = '''
Z = type({"x" : 1})
pass
    '''
    # (inspect, kill) = pals.spawn_inspect_code('main', code, package, set())
    (inspect, kill) = pals.spawn_inspect_code('main', code, package, pals.all_checks)
    try:
        code, aux = inspect('Z')
        Z = aux.local_env['Z'].type
        assert isinstance(Z, pals.TypeType)
        assert isinstance(Z.content, pals.DictLitType)
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    finally:
        kill()

def test_tuple():
    code = '''
X = tuple[int, ...]
x = X((1,2))
pass
    '''
    # (inspect, kill) = pals.spawn_inspect_code('main', code, package, set())
    (inspect, kill) = pals.spawn_inspect_code('main', code, package, pals.all_checks)
    try:
        code, aux = inspect('x')
        x = aux.local_env['x'].type
        assert isinstance(x, pals.VariedTupleType)
        x_item = x.item_type
        assert isinstance(x_item, pals.RecordType)
        assert x_item.class_key == "builtins.int"
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    finally:
        kill()

def test_namedtuple():
    code = '''
import sys
import heapq
from collections import (namedtuple)
Pair = namedtuple('Pair', ['left', 'right'])
pair = Pair(1, 2)
pass
    '''

    # (inspect, kill) = pals.spawn_inspect_code('main', code, package, set())
    (inspect, kill) = pals.spawn_inspect_code('main', code, package, pals.all_checks)
    try:
        code, aux = inspect('pair')
        pair = aux.local_env['pair'].type
        assert isinstance(pair, pals.NamedTupleType)
        assert pair.name == "Pair"
        assert pair.fields[0] == "left"
        assert pair.fields[1] == "right"
        # print(json.dumps(pals.from_env_to_primitive_verbose(aux.local_env), indent=4))
    finally:
        kill()

def test_unify_iteration_tuples():
    code = ('''
def foo(x : int): 
    return x

for (x, y) in [(1,1),(2,2),(3,3)]:
    foo(y)
    ''')
    check_code("main", code, pals.all_checks.remove(pals.LookupDecCheck()))

def test_unify_iteration_lists():
    code = ('''
def foo(x : int): 
    return x

for [x, y] in [[1,1],[2,2],[3,3]]:
    foo(y)
    ''')
    check_code("main", code, pals.all_checks.remove(pals.LookupDecCheck()))

def test_lookup_vartype():
    # TODO: figure out how to handle "_typeshed.SupportsRichComparisonT"
    code = ('''
min([(1, "here"), (2, "thing"), (3, "hello")], key = lambda a :a[1])[0]
    ''')
    check_code("main", code, pals.all_checks.remove(pals.LookupDecCheck()))

if __name__ == "__main__":
    pass