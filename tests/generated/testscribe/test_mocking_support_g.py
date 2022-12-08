import test_data.simple
import testscribe.error
import pytest
from testscribe.mocking_support import check_target_can_be_used_as_spec, get_mock_target_str, get_target_str_from_obj


def test_check_target_can_be_used_as_spec_func_can_be_a_spec():
    result = check_target_can_be_used_as_spec(obj=test_data.simple.foo)
    assert result is None


def test_check_target_can_be_used_as_spec_int_not_a_spec():
    with pytest.raises(testscribe.error.Error) as exception_info:
        check_target_can_be_used_as_spec(obj=1)
    assert str(exception_info.value) == "1 is not a type or Callable. It can't be used as a spec for a mock object."


def test_get_mock_target_str_class():
    result = get_mock_target_str(target=test_data.simple.C)
    assert result == 'test_data.simple.C'


def test_get_mock_target_str_str():
    result = get_mock_target_str(target='a')
    assert result == 'a'


def test_get_target_str_from_obj_invalid_object_for_spec():
    with pytest.raises(testscribe.error.Error) as exception_info:
        get_target_str_from_obj(obj=1)
    assert str(exception_info.value) == "1 is not a type or Callable. It can't be used as a spec for a mock object."


def test_get_target_str_from_obj_class():
    result = get_target_str_from_obj(obj=test_data.simple.C)
    assert result == 'test_data.simple.C'
