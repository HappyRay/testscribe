import collections
import testscribe.global_var
from unittest.mock import patch
from wrapper.mock_proxy_support_wrapper import create_mock_name_twice, get_mock_attribute_value_wrapper


def test_create_mock_name_twice_should_generate_unique_names():
    with patch('testscribe.global_var.g_mock_name_counter', collections.Counter(testscribe.global_var.g_mock_name_counter)):
        result = create_mock_name_twice()
    assert result == ('a', 'a_1')


def test_get_mock_attribute_value_wrapper():
    result = get_mock_attribute_value_wrapper()
    assert result == 1
