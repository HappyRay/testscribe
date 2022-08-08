from wrapper.exception_decorator_wrapper import run_dummy_app


def test_run_dummy_app():
    result = run_dummy_app()
    assert result == (1, 'Aborted due to an exception:\nTraceback (most recent call last):\n  File "src/test_scribe/exception_decorator.py", line 27, in wrapper_decorator\n    return func(*args, **kwargs)\n  File "tests/test_data/dummy_app.py", line 10, in raise_exception\n    raise Exception("Test exception")\nException: Test exception\n\nAborted.\n')
