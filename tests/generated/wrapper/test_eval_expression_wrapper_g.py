import collections
import collections.abc
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


def test_process_mock_marker_wrapper_callable_with_parameter_types():
    m_mock_proxy: testscribe.mock_proxy.MockProxy = create_autospec(spec=testscribe.mock_proxy.MockProxy)
    m_mock_proxy.return_value = 1
    with patch('testscribe.eval_expression.MockProxy', m_mock_proxy):
        result = process_mock_marker_wrapper(t=typing.Callable[[int], int], v=testscribe.api.mock_api.m)
    assert result == 1
    m_mock_proxy_mock_calls = get_normalized_mock_calls(m_mock_proxy, testscribe.mock_proxy.MockProxy)
    assert m_mock_proxy_mock_calls == [
        call(spec=ANY),
    ]
    assert isinstance(m_mock_proxy_mock_calls[0][2]['spec'], typing._GenericAlias)
    assert m_mock_proxy_mock_calls[0][2]['spec']._inst is True
    assert m_mock_proxy_mock_calls[0][2]['spec']._special is False
    assert m_mock_proxy_mock_calls[0][2]['spec']._name == 'Callable'
    assert m_mock_proxy_mock_calls[0][2]['spec'].__origin__ == collections.abc.Callable
    assert m_mock_proxy_mock_calls[0][2]['spec'].__args__ == (int, int)
    assert m_mock_proxy_mock_calls[0][2]['spec'].__parameters__ == ()
    assert m_mock_proxy_mock_calls[0][2]['spec'].__slots__ is None


def test_process_mock_marker_wrapper_callable():
    m_mock_proxy: testscribe.mock_proxy.MockProxy = create_autospec(spec=testscribe.mock_proxy.MockProxy)
    m_mock_proxy.return_value = 1
    with patch('testscribe.eval_expression.MockProxy', m_mock_proxy):
        result = process_mock_marker_wrapper(t=typing.Callable, v=testscribe.api.mock_api.m)
    assert result == 1
    m_mock_proxy_mock_calls = get_normalized_mock_calls(m_mock_proxy, testscribe.mock_proxy.MockProxy)
    assert m_mock_proxy_mock_calls == [
        call(spec=ANY),
    ]
    assert isinstance(m_mock_proxy_mock_calls[0][2]['spec'], typing._VariadicGenericAlias)
    assert m_mock_proxy_mock_calls[0][2]['spec']._inst is True
    assert m_mock_proxy_mock_calls[0][2]['spec']._special is True
    assert m_mock_proxy_mock_calls[0][2]['spec']._name == 'Callable'
    assert m_mock_proxy_mock_calls[0][2]['spec'].__origin__ == collections.abc.Callable
    assert m_mock_proxy_mock_calls[0][2]['spec'].__args__ == ()
    assert m_mock_proxy_mock_calls[0][2]['spec'].__parameters__ == ()
    assert m_mock_proxy_mock_calls[0][2]['spec'].__slots__ is None
    assert m_mock_proxy_mock_calls[0][2]['spec'].__doc__ == """\
Callable type; Callable[[int], str] is a function of (int) -> str.

    The subscription syntax must always be used with exactly two
    values: the argument list and the return type.  The argument list
    must be a list of types or ellipsis; the return type must be a single type.

    There is no syntax to indicate optional or keyword arguments,
    such function types are rarely used as callback types.
    """


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
