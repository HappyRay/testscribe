import test_data.person
import test_data.simple
import test_data.value
import testscribe.model_type
import testscribe.transformer
from testscribe.result_assertion import generate_assertion, generate_complex_type_assertion, generate_module_assertion, generate_result_assertion, generate_set_assertion, generate_special_collection_assertion


def test_generate_assertion_module_type():
    result = generate_assertion(target='a', value=testscribe.model_type.ModuleModel("m"))
    assert result == """\
    from types import ModuleType
    assert type(a) == ModuleType
    a.__name__ == 'm'"""


def test_generate_assertion_class_result():
    result = generate_assertion(target='a', value=testscribe.transformer.transform_value(test_data.simple.C(1)))
    assert result == """\
    assert isinstance(a, test_data.simple.C)
    assert a.a == 1"""


def test_generate_complex_type_assertion_module_type():
    result = generate_complex_type_assertion(target='t', value=testscribe.model_type.ModuleModel("m"))
    assert result == """\
    from types import ModuleType
    assert type(t) == ModuleType
    t.__name__ == 'm'"""


def test_generate_module_assertion():
    result = generate_module_assertion(target='t', value=testscribe.model_type.ModuleModel("m"))
    assert result == """\
    from types import ModuleType
    assert type(t) == ModuleType
    t.__name__ == 'm'"""


def test_generate_result_assertion_bytes():
    result = generate_result_assertion(result=b"\x01")
    assert result == "\n    assert result == b'\\x01'"


def test_generate_result_assertion_string():
    result = generate_result_assertion(result='a')
    assert result == """\

    assert result == 'a'"""


def test_generate_result_assertion_none():
    result = generate_result_assertion(result=None)
    assert result == """\

    assert result is None"""


def test_generate_result_assertion_with_class_with_class_member():
    result = generate_result_assertion(result=testscribe.transformer.transform_value(test_data.person.Family(husband=test_data.person.Person("a", 1), wife=test_data.person.Person("b", 2), kids=[])))
    assert result == """\

    assert isinstance(result, test_data.person.Family)
    assert isinstance(result.husband, test_data.person.Person)
    assert repr(result.husband) == "Person(name='a', age=1)"
    assert isinstance(result.wife, test_data.person.Person)
    assert repr(result.wife) == "Person(name='b', age=2)"
    assert result.kids == []"""


def test_generate_result_assertion_bool():
    result = generate_result_assertion(result=True)
    assert result == """\

    assert result is True"""


def test_generate_result_assertion_float():
    result = generate_result_assertion(result=1.2)
    assert result == """\

    assert result == 1.2"""


def test_generate_result_assertion_int():
    result = generate_result_assertion(result=1)
    assert result == """\

    assert result == 1"""


def test_generate_result_assertion_mock():
    result = generate_result_assertion(result=testscribe.model_type.MockNameModel("a"))
    assert result == """\

    assert result is a"""


def test_generate_set_assertion_target_str_not_a_valid_identifier_name():
    result = generate_set_assertion(target='result[1]', value=testscribe.model_type.SetModel([1, 2]))
    assert result == """\
    assert isinstance(result[1], set)
    assert sorted(list(result[1])) == [1, 2]"""


def test_generate_set_assertion():
    result = generate_set_assertion(target='r', value=testscribe.model_type.SetModel([1, 2]))
    assert result == """\
    assert isinstance(r, set)
    assert sorted(list(r)) == [1, 2]"""


def test_generate_special_collection_assertion_complex_tuple_in_list():
    result = generate_special_collection_assertion(target='a', value=[ (1,2), {'k': False}, (3, test_data.value.object_model_c)])
    assert result == """\
    assert isinstance(a, list)
    assert len(a) == 3
    assert a[0] == (1, 2)
    assert a[1] == {'k': False}
    assert isinstance(a[2], tuple)
    assert len(a[2]) == 2
    assert a[2][0] == 3
    assert isinstance(a[2][1], test_data.simple.C)
    assert a[2][1].a == 1"""


def test_generate_special_collection_assertion_object_in_dict():
    result = generate_special_collection_assertion(target='a', value={'k': test_data.value.object_model_c, 'z': 1})
    assert result == """\
    assert isinstance(a, dict)
    assert len(a) == 2
    assert isinstance(a['k'], test_data.simple.C)
    assert a['k'].a == 1
    assert a['z'] == 1"""


def test_generate_special_collection_assertion_object_in_tuple():
    result = generate_special_collection_assertion(target='a', value=(test_data.value.object_model_c, 's'))
    assert result == """\
    assert isinstance(a, tuple)
    assert len(a) == 2
    assert isinstance(a[0], test_data.simple.C)
    assert a[0].a == 1
    assert a[1] == 's'"""


def test_generate_special_collection_assertion_object_tag_in_list():
    result = generate_special_collection_assertion(target='a', value=[1, test_data.value.object_model_c])
    assert result == """\
    assert isinstance(a, list)
    assert len(a) == 2
    assert a[0] == 1
    assert isinstance(a[1], test_data.simple.C)
    assert a[1].a == 1"""
