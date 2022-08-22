import test_data.simple
from testscribe.base_reflection_util import get_class_instance_repr_with_full_name, get_full_module_name


def test_get_class_instance_repr_with_full_name_has_module_name():
    result = get_class_instance_repr_with_full_name(instance=test_data.simple.SimpleDataClass(1))
    assert result == 'test_data.simple.SimpleDataClass(a=1, s=None)'


def test_get_class_instance_repr_with_full_name_no_module_name():
    result = get_class_instance_repr_with_full_name(instance=Exception("foo"))
    assert result == "Exception('foo')"


def test_get_full_module_name_no_module_name():
    result = get_full_module_name(symbol=Exception("foo"))
    assert result == ''


def test_get_full_module_name_has_module_name():
    result = get_full_module_name(symbol=test_data.simple.C)
    assert result == 'test_data.simple'
