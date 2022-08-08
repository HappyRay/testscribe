import test_data.simple
from test_data.return_callable import echo_func


def test_echo_func():
    result = echo_func(f=test_data.simple.foo)
    assert result == test_data.simple.foo
