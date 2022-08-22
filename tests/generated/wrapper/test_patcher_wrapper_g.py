import collections
from unittest.mock import patch
from wrapper.patcher_wrapper import remove_real_mock


def test_remove_real_mock():
    with patch('testscribe.patcher.global_var.g_name_mock_dict', {'a': 'c', 'a_1': 'd'}), patch('testscribe.patcher.global_var.g_mock_name_counter', collections.Counter({'a': 2})):
        result = remove_real_mock()
    assert result == ({'a': 'c'}, {'a': 1})
