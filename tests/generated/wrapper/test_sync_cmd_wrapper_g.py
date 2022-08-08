import test_scribe.model_type
from test_scribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from wrapper.sync_cmd_wrapper import get_regenerated_test_names


def test_get_regenerated_test_names():
    all_tests: test_scribe.model_type.AllTests = create_autospec(spec=test_scribe.model_type.AllTests)
    m_test_model: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    m_test_model_1: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    all_tests.tests = [m_test_model, m_test_model_1]
    m_test_model.name = 'old_name'
    m_test_model.short_name = '_'
    m_test_model.target_func_name = 'f'
    m_test_model_1.short_name = '_'
    m_test_model_1.target_func_name = 'f'
    result = get_regenerated_test_names(all_tests=all_tests)
    assert result == ['test_f_1', 'test_f']
    all_tests.assert_not_called()
    m_test_model.assert_not_called()
    m_test_model_1.assert_not_called()
