import collections
import test_data.simple
import test_scribe.global_var
from unittest.mock import patch
from wrapper.mock_api_wrapper import get_normalized_mock_calls_wrapper, m_wrapper


def test_get_normalized_mock_calls_wrapper():
    result = get_normalized_mock_calls_wrapper()
    assert result == [('search_a_name', (), {'keyword': 'a'}), ('search_person', (), {'name': 'b'})]


def test_m_wrapper_default_no_name():
    with patch('test_scribe.global_var.g_mock_name_counter', collections.Counter(test_scribe.global_var.g_mock_name_counter)), patch('test_scribe.global_var.g_name_mock_dict', {}):
        result = m_wrapper(name='')
    assert result == (test_data.simple.C, 'm_c')


def test_m_wrapper():
    with patch('test_scribe.global_var.g_mock_name_counter', collections.Counter(test_scribe.global_var.g_mock_name_counter)), patch('test_scribe.global_var.g_name_mock_dict', {}):
        result = m_wrapper(name='a')
    assert result == (test_data.simple.C, 'a')
