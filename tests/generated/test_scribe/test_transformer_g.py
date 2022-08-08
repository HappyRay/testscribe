import test_data.greet
import test_data.simple
import test_data.value
import test_scribe.error
import test_scribe.model_type
import test_scribe.value_util
import pytest
from test_scribe.transformer import can_use_repr, create_callable_model, transform_class, transform_value


def test_can_use_repr_unstable_repr():
    result = can_use_repr(value=test_data.simple.FuncMember(test_data.simple.foo))
    assert result is False


def test_can_use_repr_no_custom_repr():
    result = can_use_repr(value=test_data.simple.C(1))
    assert result is False


def test_can_use_repr_has_normal_custom_repr():
    result = can_use_repr(value=test_data.simple.SimpleDataClass(1))
    assert result is True


def test_create_callable_model_function_type():
    result = create_callable_model(v=type(test_data.simple.foo))
    assert isinstance(result, test_scribe.model_type.CallableModel)
    assert repr(result) == 'types.FunctionType'


def test_create_callable_model_method():
    result = create_callable_model(v=test_data.greet.Greeter.greet)
    assert isinstance(result, test_scribe.model_type.CallableModel)
    assert repr(result) == 'test_data.greet.Greeter.greet'


def test_create_callable_model_func():
    result = create_callable_model(v=test_data.simple.foo)
    assert isinstance(result, test_scribe.model_type.CallableModel)
    assert repr(result) == 'test_data.simple.foo'


def test_transform_class_use_repr():
    result = transform_class(value=test_data.simple.CustomReprStr(1))
    assert isinstance(result, test_scribe.model_type.ObjectModel)
    assert repr(result) == 'test_data.simple.CustomReprStr(1)'


def test_transform_class_members_are_trasnformed():
    result = transform_class(value=test_data.simple.WithClassMembers(test_data.simple.C(1)))
    assert isinstance(result, test_scribe.model_type.ObjectModel)
    assert repr(result) == "Object(type (test_data.simple.WithClassMembers), members ({'c': Object(type (test_data.simple.C), members ({'a': 1}))}))"


def test_transform_class_no_repr():
    result = transform_class(value=test_data.simple.C(1))
    assert isinstance(result, test_scribe.model_type.ObjectModel)
    assert repr(result) == "Object(type (test_data.simple.C), members ({'a': 1}))"


def test_transform_value_complex_set_throw_exception():
    with pytest.raises(test_scribe.error.UnsupportedDataError) as exception_info:
        transform_value(v=[1, {test_data.value.object_model_c, 2}])
    assert 'Sets that contain complex objects are not supported.' == str(exception_info.value)


def test_transform_value_simple_1():
    result = transform_value(v=(1, 2))
    assert result == (1, 2)


def test_transform_value_set():
    result = transform_value(v=set([1, 2]))
    assert isinstance(result, test_scribe.model_type.SetModel)
    assert repr(result) == 'set([1, 2])'


def test_transform_value_recursive_transform():
    result = transform_value(v=[1, test_data.simple.foo])
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0] == 1
    assert isinstance(result[1], test_scribe.model_type.CallableModel)
    assert repr(result[1]) == 'test_data.simple.foo'


def test_transform_value_simple():
    result = transform_value(v=[1, 2])
    assert result == [1, 2]


def test_transform_value_callable():
    result = transform_value(v=test_data.simple.foo)
    assert isinstance(result, test_scribe.model_type.CallableModel)
    assert repr(result) == 'test_data.simple.foo'


def test_transform_value_callable_class_instance():
    result = transform_value(v=test_data.simple.CallableClass(1))
    assert isinstance(result, test_scribe.model_type.ObjectModel)
    assert repr(result) == "Object(type (test_data.simple.CallableClass), members ({'i': 1}))"


def test_transform_value_input_value():
    result = transform_value(v=test_scribe.value_util.InputValue("a + 1", 2))
    assert isinstance(result, test_scribe.model_type.ExpressionModel)
    assert repr(result) == 'a + 1'


def test_transform_value_class_instance():
    result = transform_value(v=test_data.simple.C(1))
    assert isinstance(result, test_scribe.model_type.ObjectModel)
    assert repr(result) == "Object(type (test_data.simple.C), members ({'a': 1}))"
