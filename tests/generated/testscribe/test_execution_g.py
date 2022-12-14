import test_data.simple
import test_data.value
import testscribe.error
import testscribe.execution
import testscribe.model_type
import testscribe.namedvalues
import testscribe.patcher
import unittest.mock
from testscribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
import pytest
from testscribe.execution import create_instance, get_default_init_parameters, get_test_to_infer_default_inputs, run_target_function, show_result, show_result_internal, stop_patches, transform_and_show_result, transform_named_values


def test_create_instance():
    result = create_instance(clazz=test_data.simple.Dummy, test_to_infer_default_inputs=None)
    assert isinstance(result, testscribe.execution.CallResult)
    assert isinstance(result.arguments, testscribe.namedvalues.NamedValues)
    assert repr(result.arguments) == 'NamedValues([])'
    assert isinstance(result.result, test_data.simple.Dummy)
    assert result.exception is None


def test_get_default_init_parameters():
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_named_values: testscribe.namedvalues.NamedValues = create_autospec(spec=testscribe.namedvalues.NamedValues)
    m_test_model.init_parameters = m_named_values
    result = get_default_init_parameters(test_to_infer_default_inputs=m_test_model)
    assert result is m_named_values
    m_test_model.assert_not_called()
    m_named_values.assert_not_called()


def test_get_default_init_parameters_no_default_test():
    result = get_default_init_parameters(test_to_infer_default_inputs=None)
    assert isinstance(result, testscribe.namedvalues.NamedValues)
    assert repr(result) == 'NamedValues([])'


def test_get_test_to_infer_default_inputs_index_provided():
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_test_model.name = 't1'
    result = get_test_to_infer_default_inputs(tests=[m_test_model], index_of_test_to_update=0, function_name='f', class_name='c')
    assert result is m_test_model
    m_test_model.assert_not_called()


def test_get_test_to_infer_default_inputs_no_match():
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_test_model.target_func_name = 'g'
    result = get_test_to_infer_default_inputs(tests=[m_test_model], index_of_test_to_update=-1, function_name='f', class_name='c')
    assert result is None
    m_test_model.assert_not_called()


def test_get_test_to_infer_default_inputs_match_function_name_class_name():
    t1: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    t2: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    t1.target_func_name = 'f'
    t1.target_class_name = ''
    t2.target_func_name = 'f'
    t2.target_class_name = 'c'
    t2.name = 't2'
    result = get_test_to_infer_default_inputs(tests=[t1, t2], index_of_test_to_update=-1, function_name='f', class_name='c')
    assert result is t2
    t1.assert_not_called()
    t2.assert_not_called()


def test_run_target_function_exception_in_class_constructor():
    result = run_target_function(constructor_exception=Exception("foo"), func=test_data.simple.foo, test_to_infer_default_inputs=None)
    assert isinstance(result, testscribe.execution.CallResult)
    assert repr(result) == "CallResult(arguments=None, result=None, exception=Exception('foo'))"


def test_show_result():
    result = show_result(result='a')
    assert result == """\
***** Result:
type: <class 'str'>
value:
a
***** Result end"""


def test_show_result_internal_exception_model():
    result = show_result_internal(result=testscribe.model_type.ExceptionModel("a.b.C", "msg"))
    assert result == """\
type: Exception
value:
Exception: type ( a.b.C ), message ( msg )"""


def test_show_result_internal_set():
    result = show_result_internal(result=testscribe.model_type.SetModel([1, 2]))
    assert result == """\
type: Set
value:
set([1, 2])"""


def test_show_result_internal_module():
    result = show_result_internal(result=testscribe.model_type.ModuleModel("m"))
    assert result == """\
type: Module
value:
Module( m )"""


def test_show_result_internal_expression_model():
    result = show_result_internal(result=testscribe.model_type.ExpressionModel("a + 1"))
    assert result == """\
type: Expression
value:
Expression( a + 1 )"""


def test_show_result_internal_callable_model():
    result = show_result_internal(result=testscribe.model_type.CallableModel("foo", "call_mod"))
    assert result == """\
type: Callable
value:
call_mod.foo"""


def test_show_result_internal_mock_name_model():
    result = show_result_internal(result=testscribe.model_type.MockNameModel("a"))
    assert result == """\
type: Mock
value:
Mock( name: a )"""


def test_show_result_internal_object():
    result = show_result_internal(result=test_data.value.object_model_c)
    assert result == """\
type: test_data.simple.C
value:
Object(type (test_data.simple.C), members ({'a': 1}))"""


def test_stop_patches():
    m_patcher: testscribe.patcher.Patcher = create_autospec(spec=testscribe.patcher.Patcher)
    m_patcher_1: testscribe.patcher.Patcher = create_autospec(spec=testscribe.patcher.Patcher)
    m__patch: unittest.mock._patch = create_autospec(spec=unittest.mock._patch)
    m__patch_1: unittest.mock._patch = create_autospec(spec=unittest.mock._patch)
    m_patcher.instance = m__patch
    m_patcher_1.instance = m__patch_1
    result = stop_patches(patchers={'a': m_patcher, 'b': m_patcher_1})
    assert result is None
    m_patcher.assert_not_called()
    m_patcher_1.assert_not_called()
    m__patch_mock_calls = get_normalized_mock_calls(m__patch, unittest.mock._patch)
    assert m__patch_mock_calls == [
        call.stop(),
    ]
    m__patch_1_mock_calls = get_normalized_mock_calls(m__patch_1, unittest.mock._patch)
    assert m__patch_1_mock_calls == [
        call.stop(),
    ]


def test_transform_and_show_result_unsupported_data():
    m_call_result: testscribe.execution.CallResult = create_autospec(spec=testscribe.execution.CallResult)
    m_call_result.exception = None
    m_call_result.result = [1, {test_data.value.object_model_c, 2}]
    with pytest.raises(testscribe.error.UnsupportedDataError) as exception_info:
        transform_and_show_result(call_result=m_call_result)
    assert str(exception_info.value) == 'Sets that contain complex objects are not supported.'
    m_call_result.assert_not_called()


def test_transform_named_values():
    result = transform_named_values(named_values=testscribe.namedvalues.NamedValues([("a", test_data.simple.foo)]))
    assert isinstance(result, testscribe.namedvalues.NamedValues)
    assert repr(result) == "NamedValues([('a', test_data.simple.foo)])"
