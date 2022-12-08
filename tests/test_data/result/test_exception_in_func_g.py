import testscribe.error
import pytest
from test_data.exception_in_func import exception_throwing_func


def test_exception_throwing_func():
    with pytest.raises(testscribe.error.InputError) as exception_info:
        exception_throwing_func()
    assert str(exception_info.value) == 'foo'
