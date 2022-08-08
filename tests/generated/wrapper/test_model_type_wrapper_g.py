import test_data.simple
import test_data.value
from wrapper.model_type_wrapper import callable_model_repr, get_exception_model_str, get_expression_model_repr, get_expression_model_str, get_mockname_model_hash, get_mockname_model_repr, get_mockname_model_str, get_module_model_str, get_object_model_hash, get_object_model_repr, get_set_model_repr


def test_callable_model_repr_builtin_function():
    result = callable_model_repr(c=len)
    assert result == 'len'


def test_callable_model_repr_function():
    result = callable_model_repr(c=test_data.simple.foo)
    assert result == 'test_data.simple.foo'


def test_get_exception_model_str():
    result = get_exception_model_str()
    assert result == 'Exception: type ( TypeError ), message ( wrong type )'


def test_get_expression_model_repr():
    result = get_expression_model_repr()
    assert result == 'a + 1'


def test_get_expression_model_str():
    result = get_expression_model_str()
    assert result == 'Expression( a + 1 )'


def test_get_mockname_model_hash():
    result = get_mockname_model_hash()
    assert result == 1715668806187408293


def test_get_mockname_model_repr():
    result = get_mockname_model_repr()
    assert result == 'a'


def test_get_mockname_model_str():
    result = get_mockname_model_str()
    assert result == 'Mock( name: a )'


def test_get_module_model_str():
    result = get_module_model_str()
    assert result == 'Module( a.b )'


def test_get_object_model_hash():
    result = get_object_model_hash()
    assert result == 1013608481905991709


def test_get_object_model_repr():
    result = get_object_model_repr(o=test_data.value.object_model_d)
    assert result == 'test_data.simple.ReadOnlyData(a=1)'


def test_get_object_model_repr_no_repr_object():
    result = get_object_model_repr(o=test_data.value.object_model_c)
    assert result == "Object(type (test_data.simple.C), members ({'a': 1}))"


def test_get_set_model_repr():
    result = get_set_model_repr()
    assert result == 'set([1, 2])'
