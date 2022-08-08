import pathlib
import test_scribe.execution_util
import test_scribe.model_type
from test_scribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from unittest.mock import patch
from test_scribe.save_scribe_file import generate_scribe_file


def test_generate_scribe_file_no_test_calls_remove_file():
    m_remove_file_if_no_test: test_scribe.execution_util.remove_file_if_no_test = create_autospec(spec=test_scribe.execution_util.remove_file_if_no_test)
    all_tests: test_scribe.model_type.AllTests = create_autospec(spec=test_scribe.model_type.AllTests)
    m_remove_file_if_no_test.return_value = True
    all_tests.tests = []
    with patch('test_scribe.save_scribe_file.remove_file_if_no_test', m_remove_file_if_no_test):
        result = generate_scribe_file(scribe_file_path=pathlib.Path("foo"), all_tests=all_tests)
    assert result is None
    m_remove_file_if_no_test_mock_calls = get_normalized_mock_calls(m_remove_file_if_no_test, test_scribe.execution_util.remove_file_if_no_test)
    assert m_remove_file_if_no_test_mock_calls == [
        call(file_path=ANY, tests=[]),
    ]
    assert isinstance(m_remove_file_if_no_test_mock_calls[0].kwargs['file_path'], pathlib.PosixPath)
    assert repr(m_remove_file_if_no_test_mock_calls[0].kwargs['file_path']) == "PosixPath('foo')"
    all_tests.assert_not_called()


def test_generate_scribe_file_no_test():
    all_tests: test_scribe.model_type.AllTests = create_autospec(spec=test_scribe.model_type.AllTests)
    all_tests.tests = []
    result = generate_scribe_file(scribe_file_path=pathlib.Path("foo"), all_tests=all_tests)
    assert result is None
    all_tests.assert_not_called()
