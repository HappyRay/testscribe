import test_scribe.model_type
from test_scribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from test_scribe.model_type import AllTests, add_test, build_name_to_index_dict, delete_test_by_name, get_mock_by_name, get_type_str, sort_tests, update_test


def test_does_test_exist_does_not_exist():
    instance = AllTests(module='mod', tests=[])
    result = instance.does_test_exist(test_name='f')
    assert result is False


def test_does_test_exist_exist():
    m_test_model: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    m_test_model.target_class_name = 'c'
    m_test_model.target_func_name = 'f'
    m_test_model.name = 'n'
    instance = AllTests(module='mod', tests=[m_test_model])
    result = instance.does_test_exist(test_name='n')
    assert result is True
    m_test_model.assert_not_called()


def test_get_test_index_by_name():
    input_mock: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    input_mock_1: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    input_mock.target_class_name = ''
    input_mock.target_func_name = 'b'
    input_mock.name = 't1'
    input_mock_1.target_class_name = ''
    input_mock_1.target_func_name = 'a'
    input_mock_1.name = 't2'
    instance = AllTests(module='m', tests=[input_mock, input_mock_1])
    result = instance.get_test_index_by_name(test_name='t1')
    assert result == 1
    input_mock.assert_not_called()
    input_mock_1.assert_not_called()


def test_get_test_index_by_name_does_not_exist():
    input_mock: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    input_mock_1: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    input_mock.target_class_name = 'c'
    input_mock.target_func_name = 'f'
    input_mock.name = 'a'
    input_mock_1.target_class_name = 'c'
    input_mock_1.target_func_name = 'f'
    input_mock_1.name = 'b'
    instance = AllTests(module='mod', tests=[input_mock, input_mock_1])
    result = instance.get_test_index_by_name(test_name='f')
    assert result == -1
    input_mock.assert_not_called()
    input_mock_1.assert_not_called()


def test_get_test_index_by_name_exist():
    input_mock: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    input_mock_1: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    input_mock.target_class_name = 'c'
    input_mock.target_func_name = 'f'
    input_mock.name = 'a'
    input_mock_1.target_class_name = 'c'
    input_mock_1.target_func_name = 'f'
    input_mock_1.name = 'f'
    instance = AllTests(module='mod', tests=[input_mock, input_mock_1])
    result = instance.get_test_index_by_name(test_name='f')
    assert result == 1
    input_mock.assert_not_called()
    input_mock_1.assert_not_called()


def test_add_test_new_test_should_appear_before_old():
    all_tests: test_scribe.model_type.AllTests = create_autospec(spec=test_scribe.model_type.AllTests)
    test: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    input_mock: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    all_tests.tests = [input_mock]
    all_tests.module = 'm'
    test.name = 't1'
    test.target_class_name = 'c'
    test.target_func_name = 'f'
    input_mock.target_class_name = 'c'
    input_mock.target_func_name = 'f'
    input_mock.name = 't'
    result = add_test(all_tests=all_tests, test=test)
    assert isinstance(result, test_scribe.model_type.AllTests)
    assert result.module == 'm'
    assert result.tests == [test, input_mock]
    assert result.name_to_index == {'t1': 0, 't': 1}
    all_tests.assert_not_called()
    test.assert_not_called()
    input_mock.assert_not_called()


def test_build_name_to_index_dict():
    input_mock: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    input_mock_1: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    input_mock.name = 'a'
    input_mock_1.name = 'b'
    result = build_name_to_index_dict(tests=[input_mock, input_mock_1])
    assert result == {'a': 0, 'b': 1}
    input_mock.assert_not_called()
    input_mock_1.assert_not_called()


def test_delete_test_by_name():
    all_tests: test_scribe.model_type.AllTests = create_autospec(spec=test_scribe.model_type.AllTests)
    m_test_model: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    m_test_model_1: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    all_tests.tests = [m_test_model, m_test_model_1]
    all_tests.module = 'module_a'
    m_test_model.name = 't'
    m_test_model_1.name = 't1'
    m_test_model_1.target_class_name = 'c'
    m_test_model_1.target_func_name = 'f'
    result = delete_test_by_name(all_tests=all_tests, name='t')
    assert isinstance(result, test_scribe.model_type.AllTests)
    assert result.module == 'module_a'
    assert result.tests == [m_test_model_1]
    assert result.name_to_index == {'t1': 0}
    all_tests.assert_not_called()
    m_test_model.assert_not_called()
    m_test_model_1.assert_not_called()


def test_get_mock_by_name_found():
    m_mock_model: test_scribe.model_type.MockModel = create_autospec(spec=test_scribe.model_type.MockModel)
    m_mock_model_1: test_scribe.model_type.MockModel = create_autospec(spec=test_scribe.model_type.MockModel)
    m_mock_model.name = 'b'
    m_mock_model_1.name = 'a'
    result = get_mock_by_name(mocks=[m_mock_model, m_mock_model_1], name='a')
    assert result is m_mock_model_1
    m_mock_model.assert_not_called()
    m_mock_model_1.assert_not_called()


def test_get_mock_by_name_not_found():
    m_mock_model: test_scribe.model_type.MockModel = create_autospec(spec=test_scribe.model_type.MockModel)
    m_mock_model.name = 'b'
    result = get_mock_by_name(mocks=[m_mock_model], name='a')
    assert result is None
    m_mock_model.assert_not_called()


def test_get_type_str_callable_model():
    result = get_type_str(v=test_scribe.model_type.CallableModel("foo", "call_mod"))
    assert result == 'Callable'


def test_get_type_str_non_model_type():
    result = get_type_str(v={'a': 1})
    assert result == "<class 'dict'>"


def test_sort_tests():
    m_test_model: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    m_test_model_1: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    m_test_model_2: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    m_test_model.target_class_name = 'c'
    m_test_model.target_func_name = 'b'
    m_test_model_1.target_class_name = ''
    m_test_model_1.target_func_name = 'a'
    m_test_model_2.target_class_name = 'c'
    m_test_model_2.target_func_name = 'a'
    result = sort_tests(tests=[m_test_model, m_test_model_1, m_test_model_2])
    assert result == [m_test_model_1, m_test_model_2, m_test_model]
    m_test_model.assert_not_called()
    m_test_model_1.assert_not_called()
    m_test_model_2.assert_not_called()


def test_update_test():
    all_tests: test_scribe.model_type.AllTests = create_autospec(spec=test_scribe.model_type.AllTests)
    test: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    m_test_model: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    m_test_model_1: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    all_tests.tests = [m_test_model, m_test_model_1]
    all_tests.module = 'm'
    test.target_class_name = 'c'
    test.target_func_name = 'f'
    test.name = 't'
    m_test_model_1.target_class_name = 'c'
    m_test_model_1.target_func_name = 'a'
    m_test_model_1.name = 't1'
    result = update_test(all_tests=all_tests, index=0, test=test)
    assert isinstance(result, test_scribe.model_type.AllTests)
    assert result.module == 'm'
    assert result.tests == [m_test_model_1, test]
    assert result.name_to_index == {'t1': 0, 't': 1}
    all_tests.assert_not_called()
    test.assert_not_called()
    m_test_model.assert_not_called()
    m_test_model_1.assert_not_called()
