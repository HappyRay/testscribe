import pathlib
import setup
import testscribe.cli
import testscribe.error
import pytest
from testscribe.config import get_output_root_path, get_setup_func, initialize_io, load_config_data


def test_get_output_root_path_default():
    result = get_output_root_path(data={})
    assert isinstance(result, pathlib.PosixPath)
    assert repr(result) == "PosixPath('.')"


def test_get_output_root_path_key_exists():
    result = get_output_root_path(data={'output-root-dir': 'a/b'})
    assert isinstance(result, pathlib.PosixPath)
    assert repr(result) == "PosixPath('a/b')"


def test_get_setup_func_value_is_a_method():
    with pytest.raises(testscribe.error.Error) as exception_info:
        get_setup_func(data={'setup-function': 'test_data.simple.C.bar'})
    assert "The setup function as specified by the setup-function key is:test_data.simple.C.bar. It should be a valid fully qualified function name. Can't load this symbol.\nerror detail:\nNo module named 'test_data.simple.C'; 'test_data.simple' is not a package" == str(exception_info.value)


def test_get_setup_func_invalid_symbol():
    with pytest.raises(testscribe.error.Error) as exception_info:
        get_setup_func(data={'setup-function': 'invalid'})
    assert "The setup function as specified by the setup-function key is:invalid. It should be a valid fully qualified function name. Can't load this symbol.\nerror detail:\nEmpty module name" == str(exception_info.value)


def test_get_setup_func_value_not_a_string():
    with pytest.raises(testscribe.error.Error) as exception_info:
        get_setup_func(data={'setup-function': 1})
    assert 'The setup function as specified by the setup-function key is:1. It should be a valid fully qualified function name. The value is not a string or is an empty string.' == str(exception_info.value)


def test_get_setup_func_value_is_empty_string():
    with pytest.raises(testscribe.error.Error) as exception_info:
        get_setup_func(data={'setup-function': ''})
    assert 'The setup function as specified by the setup-function key is:. It should be a valid fully qualified function name. The value is not a string or is an empty string.' == str(exception_info.value)


def test_get_setup_func_no_key():
    result = get_setup_func(data={})
    assert result is None


def test_get_setup_func():
    result = get_setup_func(data={'setup-function': 'setup.setup'})
    assert result == setup.setup


def test_initialize_io_default():
    result = initialize_io(data={})
    assert isinstance(result, testscribe.cli.CLI)


def test_load_config_data_invalid_config_file_path():
    result = load_config_data(config_file_path=pathlib.Path("not exist"))
    assert result == {}
