from unittest.mock import Mock, call

from test_scribe.api.mock_api import get_normalized_mock_calls


def foo(a, b):
    pass


class C:
    def __init__(self, j: int):
        pass

    def hi(self, i: int):
        pass


def test_get_normalized_mock_calls_func():
    """
    This test can be generated with a wrapper function.

    However, the assertion will look like
    assert result == [('', (), {'a': 1, 'b': 2})]
    The right side is the repr of a call.
    It's not as readable.
    """
    m = Mock(foo)
    m(1, 2)
    # as an example of how mock calls can normally be asserted.
    m.assert_called_with(1, 2)
    m.assert_called_with(1, b=2)
    # Calls are asserted using the keyword arguments form consistently.
    assert get_normalized_mock_calls(m, foo) == [call(a=1, b=2)]


def test_get_normalized_mock_calls_method():
    m = Mock(C)
    m.hi(1)
    m(2)
    assert get_normalized_mock_calls(m, C) == [call.hi(i=1), call(j=2)]
