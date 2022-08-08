import collections
import test_data.simple
import test_scribe.global_var
import test_scribe.mock_call
import test_scribe.namedvalues
from test_scribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from unittest.mock import patch
import pytest
from wrapper.mock_proxy_wrapper import is_mock_proxy_wrapper, magic_len_method_throw_exception, mock_pass_is_instance, mock_proxy_method_call


def test_is_mock_proxy_wrapper():
    with patch('test_scribe.global_var.g_mock_name_counter', collections.Counter(test_scribe.global_var.g_mock_name_counter)), patch('test_scribe.global_var.g_name_mock_dict', {}):
        result = is_mock_proxy_wrapper()
    assert result is True


def test_magic_len_method_throw_exception():
    with patch('test_scribe.global_var.g_mock_name_counter', collections.Counter(test_scribe.global_var.g_mock_name_counter)), patch('test_scribe.global_var.g_name_mock_dict', {}):
        with pytest.raises(AttributeError) as exception_info:
            magic_len_method_throw_exception()
        assert 'mocking the __len__ method is not supported.' == str(exception_info.value)


def test_mock_pass_is_instance():
    c: test_data.simple.C = create_autospec(spec=test_data.simple.C)
    result = mock_pass_is_instance(c=c)
    assert result is True
    c.assert_not_called()


def test_mock_proxy_method_call():
    with patch('test_scribe.global_var.g_mock_name_counter', collections.Counter(test_scribe.global_var.g_mock_name_counter)), patch('test_scribe.global_var.g_name_mock_dict', {}):
        result = mock_proxy_method_call()
    assert isinstance(result, test_scribe.mock_call.MockCall)
    assert result.method_name == 'bar'
    assert result.mock_name == 'm_c'
    assert result.spec == test_data.simple.C
    assert result.previous_call_count == 0
    assert isinstance(result.args, test_scribe.namedvalues.NamedValues)
    assert repr(result.args) == 'NamedValues([])'
    assert result.return_value is None
