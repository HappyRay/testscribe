import collections
import testscribe.global_var
from unittest.mock import patch
from wrapper.mocking_support_wrapper import get_direct_mock_calls_func, get_direct_mock_calls_method, get_target_str_from_obj_mock_proxy, normalize_function_mock_call, normalize_method_mock_call


def test_get_direct_mock_calls_func():
    result = get_direct_mock_calls_func()
    assert result == [('', (), {})]


def test_get_direct_mock_calls_method():
    result = get_direct_mock_calls_method()
    assert result == [('search_a_name', ('a',), {}), ('search_person', ('b',), {})]


def test_get_target_str_from_obj_mock_proxy():
    with patch('testscribe.global_var.g_mock_name_counter', collections.Counter(testscribe.global_var.g_mock_name_counter)), patch('testscribe.global_var.g_name_mock_dict', {}):
        result = get_target_str_from_obj_mock_proxy()
    assert result == 'test_data.simple.C'


def test_normalize_function_mock_call():
    result = normalize_function_mock_call()
    assert result == ('', (), {'a': 1, 'b': 2})


def test_normalize_method_mock_call():
    result = normalize_method_mock_call()
    assert result == ('search_a_name', (), {'keyword': 'a'})
