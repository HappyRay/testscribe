import testscribe.ignore
import testscribe.model
import testscribe.model_type
import testscribe.user_triggered_exception
from testscribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from testscribe.gen_mock_code import create_call_dict_indexed_by_method_name, gen_mock_return_values_for_one_method_with_return_values, generate_behavior_statements_for_one_mock, generate_mock_behavior_statements, generate_mock_return_values, generate_one_mock_creation_statement, generate_property_init_statements, get_full_mock_method_name, has_not_ignored_return_value, is_single_real_return_value


def test_create_call_dict_indexed_by_method_name():
    input_mock: testscribe.model.MockCallModel = create_autospec(spec=testscribe.model.MockCallModel)
    input_mock_1: testscribe.model.MockCallModel = create_autospec(spec=testscribe.model.MockCallModel)
    input_mock_2: testscribe.model.MockCallModel = create_autospec(spec=testscribe.model.MockCallModel)
    input_mock.name = 'a'
    input_mock_1.name = 'b'
    input_mock_2.name = 'a'
    result = create_call_dict_indexed_by_method_name(mock_calls=[input_mock, input_mock_1, input_mock_2])
    assert result == {'a': [input_mock, input_mock_2], 'b': [input_mock_1]}
    input_mock.assert_not_called()
    input_mock_1.assert_not_called()
    input_mock_2.assert_not_called()


def test_gen_mock_return_values_for_one_method_with_return_values_single_user_triggered_exception():
    result = gen_mock_return_values_for_one_method_with_return_values(mock_object_name='m', method_name='', return_values=[testscribe.user_triggered_exception.UserTriggeredException(Exception())])
    assert result == 'm.side_effect = [Exception()]'


def test_gen_mock_return_values_for_one_method_with_return_values_different_real_values():
    result = gen_mock_return_values_for_one_method_with_return_values(mock_object_name='m', method_name='foo', return_values=[1, 2])
    assert result == 'm.foo.side_effect = [1, 2]'


def test_gen_mock_return_values_for_one_method_with_return_values_only_ignored():
    result = gen_mock_return_values_for_one_method_with_return_values(mock_object_name='m', method_name='foo', return_values=[testscribe.ignore.IGNORED])
    assert result == ''


def test_gen_mock_return_values_for_one_method_with_return_values_same_single_value():
    result = gen_mock_return_values_for_one_method_with_return_values(mock_object_name='m', method_name='foo', return_values=[1, 1])
    assert result == 'm.foo.return_value = 1'


def test_gen_mock_return_values_for_one_method_with_return_values_no_return_value():
    result = gen_mock_return_values_for_one_method_with_return_values(mock_object_name='m', method_name='foo', return_values=[])
    assert result == ''


def test_generate_behavior_statements_for_one_mock():
    mock: testscribe.model_type.MockModel = create_autospec(spec=testscribe.model_type.MockModel)
    m_mock_call_model: testscribe.model_type.MockCallModel = create_autospec(spec=testscribe.model_type.MockCallModel)
    mock.attributes = {'a': 1}
    mock.name = 'm'
    mock.calls = [m_mock_call_model]
    m_mock_call_model.name = 'foo'
    m_mock_call_model.return_value = 2
    result = generate_behavior_statements_for_one_mock(mock=mock)
    assert result == ['m.a = 1', 'm.foo.return_value = 2']
    mock.assert_not_called()
    m_mock_call_model.assert_not_called()


def test_generate_mock_behavior_statements():
    m_mock_model: testscribe.model_type.MockModel = create_autospec(spec=testscribe.model_type.MockModel)
    m_mock_model_1: testscribe.model_type.MockModel = create_autospec(spec=testscribe.model_type.MockModel)
    m_mock_call_model: testscribe.model_type.MockCallModel = create_autospec(spec=testscribe.model_type.MockCallModel)
    m_mock_model.attributes = {'a': 1}
    m_mock_model.name = 'm'
    m_mock_model.calls = []
    m_mock_model_1.attributes = {}
    m_mock_model_1.calls = [m_mock_call_model]
    m_mock_model_1.name = 'm1'
    m_mock_call_model.name = 'foo'
    m_mock_call_model.return_value = 2
    result = generate_mock_behavior_statements(mocks=[m_mock_model, m_mock_model_1])
    assert result == ['m.a = 1', 'm1.foo.return_value = 2']
    m_mock_model.assert_not_called()
    m_mock_model_1.assert_not_called()
    m_mock_call_model.assert_not_called()


def test_generate_mock_return_values_one_method_different_return_values():
    mock: testscribe.model_type.MockModel = create_autospec(spec=testscribe.model_type.MockModel)
    input_mock: testscribe.model_type.MockCallModel = create_autospec(spec=testscribe.model_type.MockCallModel)
    input_mock_1: testscribe.model_type.MockCallModel = create_autospec(spec=testscribe.model_type.MockCallModel)
    mock.calls = [input_mock, input_mock_1]
    mock.name = 'm'
    input_mock.name = 'm1'
    input_mock.return_value = 1
    input_mock_1.name = 'm1'
    input_mock_1.return_value = 2
    result = generate_mock_return_values(mock=mock)
    assert result == ['m.m1.side_effect = [1, 2]']
    mock.assert_not_called()
    input_mock.assert_not_called()
    input_mock_1.assert_not_called()


def test_generate_mock_return_values_two_methods():
    mock: testscribe.model_type.MockModel = create_autospec(spec=testscribe.model_type.MockModel)
    input_mock: testscribe.model_type.MockCallModel = create_autospec(spec=testscribe.model_type.MockCallModel)
    input_mock_1: testscribe.model_type.MockCallModel = create_autospec(spec=testscribe.model_type.MockCallModel)
    mock.calls = [input_mock, input_mock_1]
    mock.name = 'm'
    input_mock.name = 'm1'
    input_mock.return_value = 1
    input_mock_1.name = 'm2'
    input_mock_1.return_value = 'a'
    result = generate_mock_return_values(mock=mock)
    assert result == ['m.m1.return_value = 1', "m.m2.return_value = 'a'"]
    mock.assert_not_called()
    input_mock.assert_not_called()
    input_mock_1.assert_not_called()


def test_generate_one_mock_creation_statement():
    mock: testscribe.model_type.MockModel = create_autospec(spec=testscribe.model_type.MockModel)
    mock.spec_str = 'a.B'
    mock.name = 'm'
    result = generate_one_mock_creation_statement(mock=mock)
    assert result == 'm: a.B = create_autospec(spec=a.B)'
    mock.assert_not_called()


def test_generate_property_init_statements():
    mock: testscribe.model_type.MockModel = create_autospec(spec=testscribe.model_type.MockModel)
    mock.attributes = {'a': 1, 'b': 'foo'}
    mock.name = 'm'
    result = generate_property_init_statements(mock=mock)
    assert result == ['m.a = 1', "m.b = 'foo'"]
    mock.assert_not_called()


def test_get_full_mock_method_name_call_a_method_on_the_mock():
    result = get_full_mock_method_name(method_name='foo', mock_object_name='m')
    assert result == 'm.foo'


def test_get_full_mock_method_name_direct_call_on_the_mock():
    result = get_full_mock_method_name(method_name='', mock_object_name='m')
    assert result == 'm'


def test_has_not_ignored_return_value_has_exception():
    result = has_not_ignored_return_value(values=[testscribe.user_triggered_exception.UserTriggeredException(Exception())])
    assert result is True


def test_has_not_ignored_return_value_only_ignored():
    result = has_not_ignored_return_value(values=[testscribe.ignore.IGNORED, testscribe.ignore.IGNORED])
    assert result is False


def test_has_not_ignored_return_value_has_real_value():
    result = has_not_ignored_return_value(values=[1, testscribe.ignore.IGNORED])
    assert result is True


def test_is_single_real_return_value_only_ignored():
    result = is_single_real_return_value(return_values=[testscribe.ignore.IGNORED])
    assert result is False


def test_is_single_real_return_value_only_user_triggered_exception():
    result = is_single_real_return_value(return_values=[testscribe.user_triggered_exception.UserTriggeredException(Exception())])
    assert result is False


def test_is_single_real_return_value_same_real_value():
    result = is_single_real_return_value(return_values=[1, 1])
    assert result is True


def test_is_single_real_return_value_not_same_real_value():
    result = is_single_real_return_value(return_values=[1, 2])
    assert result is False
