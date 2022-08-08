import pathlib
import test_scribe.model_type
from test_scribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from test_scribe.delete_test_cmd import delete_test_internal


def test_delete_test_internal_test_not_exist():
    all_tests: test_scribe.model_type.AllTests = create_autospec(spec=test_scribe.model_type.AllTests)
    all_tests.does_test_exist.return_value = False
    result = delete_test_internal(scribe_file_path=pathlib.Path("foo"), test_name='not_exist', all_tests=all_tests)
    assert result is None
    all_tests_mock_calls = get_normalized_mock_calls(all_tests, test_scribe.model_type.AllTests)
    assert all_tests_mock_calls == [
        call.does_test_exist(test_name='not_exist'),
    ]
