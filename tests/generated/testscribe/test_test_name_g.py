import testscribe.model_type
from testscribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from testscribe.test_name import create_proper_short_name, create_proper_test_name, generate_unique_test_name, get_default_short_name, get_other_test_names, get_raw_short_name, get_short_name, get_test_name, replace_leading_underscore_with_function_name


def test_create_proper_short_name_space():
    result = create_proper_short_name(raw_short_name='Hi you')
    assert result == 'hi_you'


def test_create_proper_short_name_camel_case():
    result = create_proper_short_name(raw_short_name='HelloWorld')
    assert result == 'hello_world'


def test_create_proper_test_name():
    result = create_proper_test_name(short_name='_foo', target_func_name='f')
    assert result == 'test_f_foo'


def test_generate_unique_test_name_conflict():
    all_tests: testscribe.model_type.AllTests = create_autospec(spec=testscribe.model_type.AllTests)
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_test_model_1: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    all_tests.tests = [m_test_model, m_test_model_1]
    m_test_model.name = 'a'
    m_test_model_1.name = 'a_2'
    result = generate_unique_test_name(base_name='a', all_tests=all_tests, test_to_update_index=-1)
    assert result == 'a_1'
    all_tests.assert_not_called()
    m_test_model.assert_not_called()
    m_test_model_1.assert_not_called()


def test_generate_unique_test_name_no_conflict():
    all_tests: testscribe.model_type.AllTests = create_autospec(spec=testscribe.model_type.AllTests)
    all_tests.tests = []
    result = generate_unique_test_name(base_name='a', all_tests=all_tests, test_to_update_index=-1)
    assert result == 'a'
    all_tests.assert_not_called()


def test_get_default_short_name_update():
    all_tests: testscribe.model_type.AllTests = create_autospec(spec=testscribe.model_type.AllTests)
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    all_tests.tests = [m_test_model]
    m_test_model.short_name = 's'
    result = get_default_short_name(all_tests=all_tests, index_of_test_to_update=0)
    assert result == 's'
    all_tests.assert_not_called()
    m_test_model.assert_not_called()


def test_get_default_short_name_add():
    all_tests: testscribe.model_type.AllTests = create_autospec(spec=testscribe.model_type.AllTests)
    result = get_default_short_name(all_tests=all_tests, index_of_test_to_update=-1)
    assert result == '_'
    all_tests.assert_not_called()


def test_get_other_test_names_update():
    all_tests: testscribe.model_type.AllTests = create_autospec(spec=testscribe.model_type.AllTests)
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_test_model_1: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    all_tests.tests = [m_test_model, m_test_model_1]
    m_test_model_1.name = 't2'
    result = get_other_test_names(test_to_update_index=0, all_tests=all_tests)
    assert isinstance(result, set)
    assert sorted(list(result)) == ['t2']
    all_tests.assert_not_called()
    m_test_model.assert_not_called()
    m_test_model_1.assert_not_called()


def test_get_other_test_names_add():
    all_tests: testscribe.model_type.AllTests = create_autospec(spec=testscribe.model_type.AllTests)
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    all_tests.tests = [m_test_model]
    m_test_model.name = 't'
    result = get_other_test_names(test_to_update_index=-1, all_tests=all_tests)
    assert isinstance(result, set)
    assert sorted(list(result)) == ['t']
    all_tests.assert_not_called()
    m_test_model.assert_not_called()


def test_get_raw_short_name_do_not_ask_for_name():
    result = get_raw_short_name(default_short_name='s', ask_for_test_name=False)
    assert result == 's'


def test_get_short_name():
    all_tests: testscribe.model_type.AllTests = create_autospec(spec=testscribe.model_type.AllTests)
    result = get_short_name(all_tests=all_tests, ask_for_test_name=False, index_of_test_to_update=-1)
    assert result == '_'
    all_tests.assert_not_called()


def test_get_test_name():
    all_tests: testscribe.model_type.AllTests = create_autospec(spec=testscribe.model_type.AllTests)
    all_tests.tests = []
    result = get_test_name(all_tests=all_tests, index_of_test_to_update=-1, ask_for_test_name=False, target_func_name='f')
    assert result == ('_', 'test_f')
    all_tests.assert_not_called()


def test_replace_leading_underscore_with_function_name_no_place_holder():
    result = replace_leading_underscore_with_function_name(s='foo', function_name='f')
    assert result == 'foo'


def test_replace_leading_underscore_with_function_name_lead_with_underscore():
    result = replace_leading_underscore_with_function_name(s='_foo', function_name='f')
    assert result == 'f_foo'


def test_replace_leading_underscore_with_function_name_underscore_only():
    result = replace_leading_underscore_with_function_name(s='_', function_name='f')
    assert result == 'f'
