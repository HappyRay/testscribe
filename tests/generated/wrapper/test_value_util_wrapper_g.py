import collections
import test_scribe.global_var
from unittest.mock import patch
from wrapper.value_util_wrapper import get_value_repr_wrapper_mock_proxy


def test_get_value_repr_wrapper_mock_proxy():
    with patch('test_scribe.global_var.g_mock_name_counter', collections.Counter(test_scribe.global_var.g_mock_name_counter)), patch('test_scribe.global_var.g_name_mock_dict', {}):
        result = get_value_repr_wrapper_mock_proxy()
    assert result == "Mock: name (a) spec (<class 'test_data.simple.C'>)"
