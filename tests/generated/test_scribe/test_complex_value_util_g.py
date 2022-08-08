import pathlib
import test_data
import test_data.greet
import test_data.person
import test_data.simple
import test_data.value
import test_scribe.model_type
import typing
from test_scribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from test_scribe.complex_value_util import contain_complex_value, generic_is_special_type, has_custom_repr_method, has_unstable_repr, is_complex_value, is_enumerable_type, object_contains_unstable_repr


def test_contain_complex_value_tuple():
    result = contain_complex_value(value=(1, 2))
    assert result is False


def test_contain_complex_value_tag_in_nested_collections():
    result = contain_complex_value(value=(1, [test_data.value.object_model_c]))
    assert result is True


def test_contain_complex_value_str():
    result = contain_complex_value(value='a')
    assert result is False


def test_contain_complex_value_set():
    result = contain_complex_value(value={1, 2})
    assert result is False


def test_contain_complex_value_object_tag_in_tuple():
    result = contain_complex_value(value=(test_data.value.object_model_c, 1))
    assert result is True


def test_contain_complex_value_object_tag_in_list():
    result = contain_complex_value(value=[test_data.value.object_model_c])
    assert result is True


def test_contain_complex_value_object_tag_in_dict():
    result = contain_complex_value(value={'a': test_data.value.object_model_c})
    assert result is True


def test_contain_complex_value_object_tag():
    result = contain_complex_value(value=test_data.value.object_model_c)
    assert result is True


def test_contain_complex_value_list():
    result = contain_complex_value(value=[1, 2])
    assert result is False


def test_contain_complex_value_int():
    result = contain_complex_value(value=1)
    assert result is False


def test_contain_complex_value_float():
    result = contain_complex_value(value=1.1)
    assert result is False


def test_contain_complex_value_dict():
    result = contain_complex_value(value={'a': 1})
    assert result is False


def test_contain_complex_value_callable_type_in_list():
    result = contain_complex_value(value=[test_data.value.callable_model_foo])
    assert result is False


def test_contain_complex_value_callable_tag():
    result = contain_complex_value(value=test_data.value.callable_model_foo)
    assert result is False


def test_contain_complex_value_bool():
    result = contain_complex_value(value=True)
    assert result is False


def test_generic_is_special_type_value_is_special():
    is_special_type_func: typing.Callable[[typing.Any], bool] = create_autospec(spec=typing.Callable[[typing.Any], bool])
    is_special_type_func.return_value = True
    result = generic_is_special_type(value=1, is_special_type_func=is_special_type_func)
    assert result is True
    is_special_type_func_mock_calls = is_special_type_func.mock_calls
    assert is_special_type_func_mock_calls == [
        call(1),
    ]


def test_generic_is_special_type_simple_value_not_special_type():
    is_special_type_func: typing.Callable[[typing.Any], bool] = create_autospec(spec=typing.Callable[[typing.Any], bool])
    is_special_type_func.return_value = False
    result = generic_is_special_type(value=1, is_special_type_func=is_special_type_func)
    assert result is False
    is_special_type_func_mock_calls = is_special_type_func.mock_calls
    assert is_special_type_func_mock_calls == [
        call(1),
    ]


def test_generic_is_special_type_enumeralbe_false():
    is_special_type_func: typing.Callable[[typing.Any], bool] = create_autospec(spec=typing.Callable[[typing.Any], bool])
    is_special_type_func.return_value = False
    result = generic_is_special_type(value=[1], is_special_type_func=is_special_type_func)
    assert result is False
    is_special_type_func_mock_calls = is_special_type_func.mock_calls
    assert is_special_type_func_mock_calls == [
        call([1]),
        call(1),
    ]


def test_generic_is_special_type_enumberable_true():
    is_special_type_func: typing.Callable[[typing.Any], bool] = create_autospec(spec=typing.Callable[[typing.Any], bool])
    is_special_type_func.side_effect = [False, True]
    result = generic_is_special_type(value=[1], is_special_type_func=is_special_type_func)
    assert result is True
    is_special_type_func_mock_calls = is_special_type_func.mock_calls
    assert is_special_type_func_mock_calls == [
        call([1]),
        call(1),
    ]


def test_generic_is_special_type_dict_true():
    is_special_type_func: typing.Callable[[typing.Any], bool] = create_autospec(spec=typing.Callable[[typing.Any], bool])
    is_special_type_func.side_effect = [False, True]
    result = generic_is_special_type(value={'a': 1}, is_special_type_func=is_special_type_func)
    assert result is True
    is_special_type_func_mock_calls = is_special_type_func.mock_calls
    assert is_special_type_func_mock_calls == [
        call({'a': 1}),
        call(1),
    ]


def test_has_custom_repr_method_data_class_has_repr():
    result = has_custom_repr_method(t=test_data.person.Person)
    assert result is True


def test_has_custom_repr_method_false_case():
    result = has_custom_repr_method(t=test_data.greet.Greeter)
    assert result is False


def test_has_custom_repr_method_path_has_repr_method():
    result = has_custom_repr_method(t=pathlib.Path)
    assert result is True


def test_has_unstable_repr_func_member_in_list():
    result = has_unstable_repr(value=[test_data.simple.FuncMember(test_data.simple.foo)])
    assert result is True


def test_has_unstable_repr_repr_contains_objects_without_custom_repr():
    result = has_unstable_repr(value=test_data.simple.DataClassWithSimpleObject(test_data.simple.Dummy()))
    assert result is True


def test_has_unstable_repr_class_with_custom_repr():
    result = has_unstable_repr(value=test_data.simple.SimpleDataClass(1))
    assert result is False


def test_is_complex_value_object_model():
    result = is_complex_value(value=test_data.value.object_model_c)
    assert result is True


def test_is_complex_value_module_model():
    result = is_complex_value(value=test_scribe.model_type.ModuleModel("foo"))
    assert result is True


def test_is_complex_value_int():
    result = is_complex_value(value=1)
    assert result is False


def test_is_enumerable_type_list():
    result = is_enumerable_type(value=[1])
    assert result is True


def test_is_enumerable_type_tuple():
    result = is_enumerable_type(value=(1, 2))
    assert result is True


def test_is_enumerable_type_set():
    result = is_enumerable_type(value={1})
    assert result is True


def test_is_enumerable_type_int():
    result = is_enumerable_type(value=1)
    assert result is False


def test_is_enumerable_type_dict():
    result = is_enumerable_type(value={'a': 1})
    assert result is False


def test_object_contains_unstable_repr_with_func():
    result = object_contains_unstable_repr(value=test_data.simple.FuncMember(test_data.simple.foo))
    assert result is True


def test_object_contains_unstable_repr_module():
    result = object_contains_unstable_repr(value=test_data.simple.ModuleMember(test_data.simple))
    assert result is True


def test_object_contains_unstable_repr_regular():
    result = object_contains_unstable_repr(value=test_data.simple.C(1))
    assert result is False


def test_object_contains_unstable_repr_class_without_dict_members():
    result = object_contains_unstable_repr(value=pathlib.Path())
    assert result is False
