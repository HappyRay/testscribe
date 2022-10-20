from wrapper.exception_decorator_wrapper import run_dummy_app_that_raise_exception


def test_run_dummy_app_that_raise_exception():
    result = run_dummy_app_that_raise_exception()
    assert result == 1
