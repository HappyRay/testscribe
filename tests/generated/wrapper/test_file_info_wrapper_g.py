import testscribe.error
import testscribe.module
import pytest
from wrapper.file_info_wrapper import get_module_wrapper


def test_get_module_wrapper_bad_input():
    """
    When the file path is not under any directory in the Python path.
    """
    with pytest.raises(testscribe.error.Error) as exception_info:
        get_module_wrapper(test_file_name='/a/b.py')
    assert "The file (/a/b.py) can't be loaded as a python module." == str(exception_info.value)


def test_get_module_wrapper_success():
    """
    Notice that the input is a relative path and thus is under one of the Python paths.
    """
    result = get_module_wrapper(test_file_name='a/b/c.py')
    assert isinstance(result, testscribe.module.Module)
    assert result.names == ('a', 'b', 'c')
