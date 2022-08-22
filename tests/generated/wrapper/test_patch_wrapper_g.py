import collections
from unittest.mock import patch
from wrapper.patch_wrapper import patch_common_code_gen


def test_patch_common_code_gen_dict():
    with patch('testscribe.global_var.g_mock_name_counter', collections.Counter()):
        result = patch_common_code_gen(value={'a': 1})
    assert result == """\

    with patch('t', {'a': 1}):"""


def test_patch_common_code_gen_list():
    with patch('testscribe.global_var.g_mock_name_counter', collections.Counter()):
        result = patch_common_code_gen(value=[1, 2])
    assert result == """\

    with patch('t', [1, 2]):"""


def test_patch_common_code_gen_str():
    with patch('testscribe.global_var.g_mock_name_counter', collections.Counter()):
        result = patch_common_code_gen(value='a')
    assert result == """\

    with patch('t', 'a'):"""


def test_patch_common_code_gen_int():
    with patch('testscribe.global_var.g_mock_name_counter', collections.Counter()):
        result = patch_common_code_gen(value=1)
    assert result == """\

    with patch('t', 1):"""
