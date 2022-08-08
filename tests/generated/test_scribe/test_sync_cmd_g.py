import pathlib
import test_scribe.execution_util
import test_scribe.sync_cmd
from test_scribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from unittest.mock import patch
from test_scribe.sync_cmd import regenerate_all_tests_internal


def test_regenerate_all_tests_internal():
    m_regenerate_tests: test_scribe.sync_cmd.regenerate_tests = create_autospec(spec=test_scribe.sync_cmd.regenerate_tests)
    m_get_all_scribe_files: test_scribe.execution_util.get_all_scribe_files = create_autospec(spec=test_scribe.execution_util.get_all_scribe_files)
    m_regenerate_tests.return_value = None
    m_get_all_scribe_files.return_value = [1, 2]
    with patch('test_scribe.sync_cmd.regenerate_tests', m_regenerate_tests), patch('test_scribe.sync_cmd.get_all_scribe_files', m_get_all_scribe_files):
        result = regenerate_all_tests_internal(output_root_path=pathlib.Path("a"))
    assert result == 2
    m_regenerate_tests_mock_calls = get_normalized_mock_calls(m_regenerate_tests, test_scribe.sync_cmd.regenerate_tests)
    assert m_regenerate_tests_mock_calls == [
        call(scribe_file_path=1),
        call(scribe_file_path=2),
    ]
    m_get_all_scribe_files_mock_calls = get_normalized_mock_calls(m_get_all_scribe_files, test_scribe.execution_util.get_all_scribe_files)
    assert m_get_all_scribe_files_mock_calls == [
        call(root_path=ANY),
    ]
    assert isinstance(m_get_all_scribe_files_mock_calls[0].kwargs['root_path'], pathlib.PosixPath)
    assert repr(m_get_all_scribe_files_mock_calls[0].kwargs['root_path']) == "PosixPath('a')"
