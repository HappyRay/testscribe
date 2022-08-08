import test_scribe.error
import pytest
from wrapper.error_wrapper import raise_custom_error


def test_raise_custom_error():
    with pytest.raises(test_scribe.error.Error) as exception_info:
        raise_custom_error()
    assert 'foo' == str(exception_info.value)
