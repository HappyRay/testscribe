import collections
import test_data.simple
import testscribe.global_var
import testscribe.mock_call
import testscribe.model_type
import testscribe.namedvalues
import testscribe.special_type
import types
import typing
from testscribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from unittest.mock import patch
import pytest
from testscribe.mock_proxy_support import check_unsupported_attributes, create_default_mock_name, create_mock_call, create_mock_name, create_unique_mock_name, get_attribute_type, get_default_mock_attribute_value, get_previous_call_count, get_spec_name, get_type_from_type_hints, infer_default_mock_attribute_value_from_mock


def test_check_unsupported_attributes_supported():
    result = check_unsupported_attributes(attribute_name='foo')
    assert result is None


def test_check_unsupported_attributes_len_magic_method_is_not_supported():
    with pytest.raises(AttributeError) as exception_info:
        check_unsupported_attributes(attribute_name='__len__')
    assert 'mocking the __len__ method is not supported.' == str(exception_info.value)


def test_create_default_mock_name():
    result = create_default_mock_name(spec=test_data.simple.C)
    assert result == 'm_c'


def test_create_mock_call():
    result = create_mock_call(method_name='f', mock_name='m', spec=test_data.simple.C, mock_calls=[])
    assert isinstance(result, testscribe.mock_call.MockCall)
    assert result.method_name == 'f'
    assert result.mock_name == 'm'
    assert result.spec == test_data.simple.C
    assert result.previous_call_count == 0
    assert isinstance(result.args, testscribe.namedvalues.NamedValues)
    assert repr(result.args) == 'NamedValues([])'
    assert result.return_value is None


def test_create_mock_name_default_name():
    with patch('testscribe.global_var.g_mock_name_counter', collections.Counter(testscribe.global_var.g_mock_name_counter)):
        result = create_mock_name(name='', spec=test_data.simple.C)
    assert result == 'm_c'


def test_create_mock_name_has_explict_name():
    with patch('testscribe.global_var.g_mock_name_counter', collections.Counter(testscribe.global_var.g_mock_name_counter)):
        result = create_mock_name(name='a', spec=test_data.simple.C)
    assert result == 'a'


def test_create_unique_mock_name_special_name_m():
    """
    There should be no mock object named "m" which conflicts with the function m.
    """
    with patch('testscribe.global_var.g_mock_name_counter', collections.Counter(testscribe.global_var.g_mock_name_counter)):
        result = create_unique_mock_name(name='m')
    assert result == 'm_1'


def test_get_attribute_type_function():
    result = get_attribute_type(spec=test_data.simple.foo, name='a')
    assert result == int


def test_get_attribute_type_data_class():
    result = get_attribute_type(spec=test_data.simple.SimpleDataClass, name='a')
    assert result == int


def test_get_attribute_type_field():
    result = get_attribute_type(spec=test_data.simple.C, name='a')
    assert result == int


def test_get_attribute_type_method():
    result = get_attribute_type(spec=test_data.simple.C, name='bar')
    assert result == types.FunctionType


def test_get_default_mock_attribute_value_no_matching_mock_in_the_test_to_infer():
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_test_model.mocks = []
    result = get_default_mock_attribute_value(mock_name='m', attribute_name='a', test_to_infer_default_inputs=m_test_model)
    assert result == testscribe.special_type.NoDefault
    m_test_model.assert_not_called()


def test_get_default_mock_attribute_value_no_test_to_infer():
    result = get_default_mock_attribute_value(mock_name='m', attribute_name='a', test_to_infer_default_inputs=None)
    assert result == testscribe.special_type.NoDefault


def test_get_previous_call_count():
    m_mock_call: testscribe.mock_call.MockCall = create_autospec(spec=testscribe.mock_call.MockCall)
    m_mock_call_1: testscribe.mock_call.MockCall = create_autospec(spec=testscribe.mock_call.MockCall)
    m_mock_call_2: testscribe.mock_call.MockCall = create_autospec(spec=testscribe.mock_call.MockCall)
    m_mock_call.method_name = 'f'
    m_mock_call_1.method_name = 'f1'
    m_mock_call_2.method_name = 'f'
    result = get_previous_call_count(mock_calls=[m_mock_call, m_mock_call_1, m_mock_call_2], method_name='f')
    assert result == 2
    m_mock_call.assert_not_called()
    m_mock_call_1.assert_not_called()
    m_mock_call_2.assert_not_called()


def test_get_spec_name_class():
    result = get_spec_name(spec=test_data.simple.C)
    assert result == 'C'


def test_get_spec_name_callable():
    result = get_spec_name(spec=typing.Callable[[int], int])
    assert result == 'Callable'


def test_get_type_from_type_hints_data_class_field_with_inconsistent_initialization():
    result = get_type_from_type_hints(spec=test_data.simple.SimpleDataClass, attribute_name='s')
    assert result == str


def test_infer_default_mock_attribute_value_from_mock_has_a_matching_attribute():
    m_mock_model: testscribe.model_type.MockModel = create_autospec(spec=testscribe.model_type.MockModel)
    m_mock_model.attributes = {'a': 1}
    result = infer_default_mock_attribute_value_from_mock(attribute_name='a', existing_mock=m_mock_model)
    assert result == 1
    m_mock_model.assert_not_called()


def test_infer_default_mock_attribute_value_from_mock_no_matching_mock_attribute_to_infer():
    m_mock_model: testscribe.model_type.MockModel = create_autospec(spec=testscribe.model_type.MockModel)
    m_mock_model.attributes = {}
    result = infer_default_mock_attribute_value_from_mock(attribute_name='a', existing_mock=m_mock_model)
    assert result == testscribe.special_type.NoDefault
    m_mock_model.assert_not_called()


def test_infer_default_mock_attribute_value_from_mock_no_mock_to_infer():
    result = infer_default_mock_attribute_value_from_mock(attribute_name='a', existing_mock=None)
    assert result == testscribe.special_type.NoDefault
