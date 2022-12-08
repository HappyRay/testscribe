import collections
import test_data.simple
import testscribe.global_var
from testscribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from unittest.mock import patch
import pytest
from test_data.mock_hash_method import get_dict, hash_mock_proxy, use_not_hashable


def test_get_dict():
    d: test_data.simple.ReadOnlyData = create_autospec(spec=test_data.simple.ReadOnlyData)
    result = get_dict(d=d)
    assert result == {d: 1}
    d.assert_not_called()


def test_hash_mock_proxy():
    with patch('testscribe.global_var.g_mock_name_counter', collections.Counter(testscribe.global_var.g_mock_name_counter)), patch('testscribe.global_var.g_name_mock_dict', {}):
        result = hash_mock_proxy()
    assert result == 578569609205554811


def test_use_not_hashable():
    with patch('testscribe.global_var.g_mock_name_counter', collections.Counter(testscribe.global_var.g_mock_name_counter)), patch('testscribe.global_var.g_name_mock_dict', {}):
        with pytest.raises(TypeError) as exception_info:
            use_not_hashable()
        assert str(exception_info.value) == "The mock target <class 'test_data.simple.SimpleDataClass'> is not hashable."
