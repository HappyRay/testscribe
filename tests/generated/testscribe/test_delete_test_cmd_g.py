import pathlib
import testscribe.model_type
from testscribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from testscribe.delete_test_cmd import delete_test_internal


def test_delete_test_internal_test_not_exist():
    all_tests: testscribe.model_type.AllTests = create_autospec(spec=testscribe.model_type.AllTests)
    all_tests.does_test_exist.return_value = False
    result = delete_test_internal(scribe_file_path=pathlib.Path("foo"), test_name='not_exist', all_tests=all_tests)
    assert result is None
    all_tests_mock_calls = get_normalized_mock_calls(all_tests, testscribe.model_type.AllTests)
    assert all_tests_mock_calls == [
        call.does_test_exist(test_name='not_exist'),
    ]
