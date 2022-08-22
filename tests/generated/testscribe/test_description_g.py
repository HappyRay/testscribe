import testscribe.model_type
from testscribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from testscribe.description import get_default_description, get_test_description


def test_get_default_description_new_test():
    all_tests: testscribe.model_type.AllTests = create_autospec(spec=testscribe.model_type.AllTests)
    result = get_default_description(all_tests=all_tests, index_of_test_to_update=-1)
    assert result == ''
    all_tests.assert_not_called()


def test_get_default_description_update_test():
    all_tests: testscribe.model_type.AllTests = create_autospec(spec=testscribe.model_type.AllTests)
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    all_tests.tests = [m_test_model]
    m_test_model.description = 'a'
    result = get_default_description(all_tests=all_tests, index_of_test_to_update=0)
    assert result == 'a'
    all_tests.assert_not_called()
    m_test_model.assert_not_called()


def test_get_test_description_new_test_default():
    all_tests: testscribe.model_type.AllTests = create_autospec(spec=testscribe.model_type.AllTests)
    result = get_test_description(all_tests=all_tests, index_of_test_to_update=-1, ask_for_description=False)
    assert result == ''
    all_tests.assert_not_called()
