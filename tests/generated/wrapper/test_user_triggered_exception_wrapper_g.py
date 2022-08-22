import testscribe.error
from wrapper.user_triggered_exception_wrapper import get_user_triggered_exception_repr


def test_get_user_triggered_exception_repr_custom_exception():
    result = get_user_triggered_exception_repr(e=testscribe.error.InputError("foo"))
    assert result == "testscribe.error.InputError('foo')"


def test_get_user_triggered_exception_repr_builtin_exception():
    result = get_user_triggered_exception_repr(e=Exception("foo"))
    assert result == "Exception('foo')"
