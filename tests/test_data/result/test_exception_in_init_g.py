import pytest
from test_data.exception_in_init import BadInit


def test_f():
    with pytest.raises(Exception) as exception_info:
        instance = BadInit()
        
    assert str(exception_info.value) == 'bad init'
