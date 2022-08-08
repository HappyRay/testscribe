import test_scribe.error
from wrapper.user_triggered_exception_wrapper import get_user_triggered_exception_repr


def test_get_user_triggered_exception_repr_custom_exception():
    result = get_user_triggered_exception_repr(e=test_scribe.error.InputError("foo"))
    assert result == "test_scribe.error.InputError('foo')"


def test_get_user_triggered_exception_repr_builtin_exception():
    result = get_user_triggered_exception_repr(e=Exception("foo"))
    assert result == "Exception('foo')"
