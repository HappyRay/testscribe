import pytest
from test_data.exception_in_init import BadInit


def test_f():
    with pytest.raises(Exception) as exception_info:
        instance = BadInit()
        
    assert 'bad init' == str(exception_info.value)
