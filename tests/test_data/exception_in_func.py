from test_scribe.error import InputError


def exception_throwing_func():
    raise InputError("foo")
