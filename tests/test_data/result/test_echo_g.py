import test_data.simple
from test_data.echo import echo


def test_echo():
    result = echo(v=test_data.simple.C(1))
    assert isinstance(result, test_data.simple.C)
    assert result.a == 1
