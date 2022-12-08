import inspect
import test_data.simple
import testscribe.mock_call
import testscribe.model_type
import testscribe.namedvalues
import testscribe.special_type
import testscribe.user_triggered_exception
import testscribe.value_util
import typing
from testscribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
import pytest
from testscribe.mock_call import get_arg_str_display, get_args_list_internal, get_call_subject, get_default_mock_call_return_value, get_default_return_value_from_models, get_default_return_value_internal, get_func_args_list, get_mock_call_return_type, get_mock_call_signature, get_true_return_value, save_args


def test_get_arg_str_display_has_argument():
    mock_call: testscribe.mock_call.MockCall = create_autospec(spec=testscribe.mock_call.MockCall)
    mock_call.args = testscribe.namedvalues.NamedValues([("p", 1)])
    result = get_arg_str_display(mock_call=mock_call)
    assert result == """\

with: p=1"""
    mock_call.assert_not_called()


def test_get_arg_str_display_empty_argument():
    mock_call: testscribe.mock_call.MockCall = create_autospec(spec=testscribe.mock_call.MockCall)
    mock_call.args = testscribe.namedvalues.NamedValues()
    result = get_arg_str_display(mock_call=mock_call)
    assert result == ''
    mock_call.assert_not_called()


def test_get_args_list_internal_method():
    result = get_args_list_internal(method_name='bar', sig=inspect.signature(test_data.simple.C.bar), spec=test_data.simple.C, args=(1,), kwargs={})
    assert result == [('a', 1)]


def test_get_args_list_internal_function():
    result = get_args_list_internal(method_name='', sig=inspect.signature(test_data.simple.foo), spec=test_data.simple.foo, args=(1,), kwargs={})
    assert result == [('a', 1)]


def test_get_call_subject_function():
    mock_call: testscribe.mock_call.MockCall = create_autospec(spec=testscribe.mock_call.MockCall)
    mock_call.mock_name = 'm_f'
    mock_call.method_name = ''
    result = get_call_subject(mock_call=mock_call)
    assert result == 'm_f'
    mock_call.assert_not_called()


def test_get_call_subject_method():
    mock_call: testscribe.mock_call.MockCall = create_autospec(spec=testscribe.mock_call.MockCall)
    mock_call.mock_name = 'm_c'
    mock_call.method_name = 'bar'
    result = get_call_subject(mock_call=mock_call)
    assert result == "m_c's bar method"
    mock_call.assert_not_called()


def test_get_default_mock_call_return_value_str_magic_method():
    mock_call: testscribe.mock_call.MockCall = create_autospec(spec=testscribe.mock_call.MockCall)
    mock_call.method_name = '__str__'
    mock_call.mock_name = 'm_f'
    result = get_default_mock_call_return_value(mock_call=mock_call)
    assert result == 'mock m_f'
    mock_call.assert_not_called()


def test_get_default_return_value_from_models_match_calls():
    m_mock_call_model: testscribe.model_type.MockCallModel = create_autospec(spec=testscribe.model_type.MockCallModel)
    mock_call: testscribe.mock_call.MockCall = create_autospec(spec=testscribe.mock_call.MockCall)
    m_mock_call_model.name = 'f1'
    m_mock_call_model.return_value = 1
    mock_call.method_name = 'f1'
    mock_call.previous_call_count = 2
    result = get_default_return_value_from_models(mock_call_models=[m_mock_call_model], mock_call=mock_call)
    assert result == 1
    m_mock_call_model.assert_not_called()
    mock_call.assert_not_called()


def test_get_default_return_value_from_models_no_existing_call():
    m_mock_call_model: testscribe.model_type.MockCallModel = create_autospec(spec=testscribe.model_type.MockCallModel)
    mock_call: testscribe.mock_call.MockCall = create_autospec(spec=testscribe.mock_call.MockCall)
    m_mock_call_model.name = 'f1'
    mock_call.method_name = 'f'
    result = get_default_return_value_from_models(mock_call_models=[m_mock_call_model], mock_call=mock_call)
    assert result == testscribe.special_type.NoDefault
    m_mock_call_model.assert_not_called()
    mock_call.assert_not_called()


def test_get_default_return_value_internal_match_mock():
    mock_call: testscribe.mock_call.MockCall = create_autospec(spec=testscribe.mock_call.MockCall)
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_mock_model: testscribe.model_type.MockModel = create_autospec(spec=testscribe.model_type.MockModel)
    mock_call.mock_name = 'm_f'
    m_test_model.mocks = [m_mock_model]
    m_mock_model.name = 'm_f'
    m_mock_model.calls = []
    result = get_default_return_value_internal(mock_call=mock_call, test_to_infer_default_inputs=m_test_model)
    assert result == testscribe.special_type.NoDefault
    mock_call.assert_not_called()
    m_test_model.assert_not_called()
    m_mock_model.assert_not_called()


def test_get_default_return_value_internal_no_matching_mock():
    mock_call: testscribe.mock_call.MockCall = create_autospec(spec=testscribe.mock_call.MockCall)
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    mock_call.mock_name = 'm_f'
    m_test_model.mocks = []
    result = get_default_return_value_internal(mock_call=mock_call, test_to_infer_default_inputs=m_test_model)
    assert result == testscribe.special_type.NoDefault
    mock_call.assert_not_called()
    m_test_model.assert_not_called()


def test_get_default_return_value_internal_no_test_to_infer():
    mock_call: testscribe.mock_call.MockCall = create_autospec(spec=testscribe.mock_call.MockCall)
    result = get_default_return_value_internal(mock_call=mock_call, test_to_infer_default_inputs=None)
    assert result == testscribe.special_type.NoDefault
    mock_call.assert_not_called()


def test_get_func_args_list_no_param_name():
    result = get_func_args_list(sig=inspect.signature(typing.Callable), spec=typing.Callable, args=(1,), kwargs={'a': 2})
    assert result == [('', 1), ('a', 2)]


def test_get_func_args_list_has_param_name():
    result = get_func_args_list(sig=inspect.signature(test_data.simple.foo), spec=test_data.simple.foo, args=(1,), kwargs={})
    assert result == [('a', 1)]


def test_get_mock_call_return_type_class():
    result = get_mock_call_return_type(method_name='', spec=test_data.simple.C)
    assert result == test_data.simple.C


def test_get_mock_call_return_type_typing_callable():
    result = get_mock_call_return_type(method_name='', spec=typing.Callable[[str] ,int])
    assert result == int


def test_get_mock_call_return_type_function():
    result = get_mock_call_return_type(method_name='', spec=test_data.simple.foo)
    assert result == int


def test_get_mock_call_return_type_method():
    result = get_mock_call_return_type(method_name='bar', spec=test_data.simple.C)
    assert result == int


def test_get_mock_call_return_type_magic_str_method():
    result = get_mock_call_return_type(method_name='__str__', spec=test_data.simple.C)
    assert result == str


def test_get_mock_call_signature_function():
    mock_call: testscribe.mock_call.MockCall = create_autospec(spec=testscribe.mock_call.MockCall)
    mock_call.spec = test_data.simple.foo
    mock_call.method_name = ''
    result = get_mock_call_signature(mock_call=mock_call)
    assert isinstance(result, inspect.Signature)
    assert repr(result) == '<Signature (a: int) -> int>'
    mock_call.assert_not_called()


def test_get_mock_call_signature_method():
    mock_call: testscribe.mock_call.MockCall = create_autospec(spec=testscribe.mock_call.MockCall)
    mock_call.spec = test_data.simple.C
    mock_call.method_name = 'bar'
    result = get_mock_call_signature(mock_call=mock_call)
    assert isinstance(result, inspect.Signature)
    assert repr(result) == '<Signature (self, a: int) -> int>'
    mock_call.assert_not_called()


def test_get_true_return_value_exception_expression():
    with pytest.raises(Exception) as exception_info:
        get_true_return_value(value=testscribe.value_util.InputValue(expression="throw Exception()", value=testscribe.user_triggered_exception.UserTriggeredException(Exception())))
    assert str(exception_info.value) == ''


def test_get_true_return_value_non_exception_expression():
    result = get_true_return_value(value=testscribe.value_util.InputValue("a + 1", 2))
    assert result == 2


def test_get_true_return_value_regular():
    result = get_true_return_value(value=1)
    assert result == 1


def test_save_args():
    mock_call: testscribe.mock_call.MockCall = create_autospec(spec=testscribe.mock_call.MockCall)
    mock_call.spec = test_data.simple.foo
    mock_call.method_name = ''
    result = save_args(mock_call=mock_call, args=(1,), kwargs={})
    assert isinstance(result, testscribe.namedvalues.NamedValues)
    assert repr(result) == "NamedValues([('a', 1)])"
    mock_call.assert_not_called()
