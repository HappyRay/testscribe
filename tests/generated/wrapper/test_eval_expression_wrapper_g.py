import collections
import test_data.simple
import testscribe.api.mock_api
import testscribe.global_var
import testscribe.mock_proxy
import typing
from testscribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from unittest.mock import patch
from wrapper.eval_expression_wrapper import contain_mock_proxy_wrapper, process_complex_value_wrapper_mixed_m_function_complex_obj, process_mock_marker_wrapper, wrap_input_value_wrapper_complex_value


def test_contain_mock_proxy_wrapper():
    with patch('testscribe.global_var.g_mock_name_counter', collections.Counter(testscribe.global_var.g_mock_name_counter)), patch('testscribe.global_var.g_name_mock_dict', {}):
        result = contain_mock_proxy_wrapper()
    assert result is True


def test_process_complex_value_wrapper_mixed_m_function_complex_obj():
    with patch('testscribe.global_var.g_mock_name_counter', collections.Counter(testscribe.global_var.g_mock_name_counter)), patch('testscribe.global_var.g_name_mock_dict', {}):
        result = process_complex_value_wrapper_mixed_m_function_complex_obj()
    assert isinstance(result, test_data.simple.C)
    assert result.a == 1


def test_process_mock_marker_wrapper_list_two_items():
    m_mock_proxy: testscribe.mock_proxy.MockProxy = create_autospec(spec=testscribe.mock_proxy.MockProxy)
    m_mock_proxy.side_effect = [1, 2]
    with patch('testscribe.eval_expression.MockProxy', m_mock_proxy):
        result = process_mock_marker_wrapper(t=typing.List[test_data.simple.C], v=[testscribe.api.mock_api.m, testscribe.api.mock_api.m])
    assert result == [1, 2]
    m_mock_proxy_mock_calls = get_normalized_mock_calls(m_mock_proxy, testscribe.mock_proxy.MockProxy)
    assert m_mock_proxy_mock_calls == [
        call(spec=test_data.simple.C),
        call(spec=test_data.simple.C),
    ]


def test_process_mock_marker_wrapper_tuple():
    m_mock_proxy: testscribe.mock_proxy.MockProxy = create_autospec(spec=testscribe.mock_proxy.MockProxy)
    m_mock_proxy.return_value = 2
    with patch('testscribe.eval_expression.MockProxy', m_mock_proxy):
        result = process_mock_marker_wrapper(t=typing.Tuple[int, test_data.simple.C], v=(1, testscribe.api.mock_api.m))
    assert result == (1, 2)
    m_mock_proxy_mock_calls = get_normalized_mock_calls(m_mock_proxy, testscribe.mock_proxy.MockProxy)
    assert m_mock_proxy_mock_calls == [
        call(spec=test_data.simple.C),
    ]


def test_process_mock_marker_wrapper_tuple_with_ellipsis():
    m_mock_proxy: testscribe.mock_proxy.MockProxy = create_autospec(spec=testscribe.mock_proxy.MockProxy)
    m_mock_proxy.side_effect = [1, 2]
    with patch('testscribe.eval_expression.MockProxy', m_mock_proxy):
        result = process_mock_marker_wrapper(t=typing.Tuple[test_data.simple.C, ...], v=(testscribe.api.mock_api.m, testscribe.api.mock_api.m))
    assert result == (1, 2)
    m_mock_proxy_mock_calls = get_normalized_mock_calls(m_mock_proxy, testscribe.mock_proxy.MockProxy)
    assert m_mock_proxy_mock_calls == [
        call(spec=test_data.simple.C),
        call(spec=test_data.simple.C),
    ]


def test_process_mock_marker_wrapper_dict():
    m_mock_proxy: testscribe.mock_proxy.MockProxy = create_autospec(spec=testscribe.mock_proxy.MockProxy)
    m_mock_proxy.side_effect = [1, 2]
    with patch('testscribe.eval_expression.MockProxy', m_mock_proxy):
        result = process_mock_marker_wrapper(t=typing.Dict[str, test_data.simple.C], v={'a': testscribe.api.mock_api.m, 'b': testscribe.api.mock_api.m})
    assert result == {'a': 1, 'b': 2}
    m_mock_proxy_mock_calls = get_normalized_mock_calls(m_mock_proxy, testscribe.mock_proxy.MockProxy)
    assert m_mock_proxy_mock_calls == [
        call(spec=test_data.simple.C),
        call(spec=test_data.simple.C),
    ]


def test_process_mock_marker_wrapper_optional_class():
    """
    put the optional class type in a list to avoid the tool trying to create a mock before the function is executed.
    """
    m_mock_proxy: testscribe.mock_proxy.MockProxy = create_autospec(spec=testscribe.mock_proxy.MockProxy)
    m_mock_proxy.return_value = 1
    with patch('testscribe.eval_expression.MockProxy', m_mock_proxy):
        result = process_mock_marker_wrapper(t=typing.List[typing.Optional[test_data.simple.C]], v=[testscribe.api.mock_api.m])
    assert result == [1]
    m_mock_proxy_mock_calls = get_normalized_mock_calls(m_mock_proxy, testscribe.mock_proxy.MockProxy)
    assert m_mock_proxy_mock_calls == [
        call(spec=test_data.simple.C),
    ]


def test_wrap_input_value_wrapper_complex_value():
    result = wrap_input_value_wrapper_complex_value(value=test_data.simple.C(1))
    assert isinstance(result, test_data.simple.C)
    assert result.a == 1
