import test_scribe.error
import pytest
from test_data.exception_in_func import exception_throwing_func


def test_exception_throwing_func():
    with pytest.raises(test_scribe.error.InputError) as exception_info:
        exception_throwing_func()
    assert 'foo' == str(exception_info.value)
