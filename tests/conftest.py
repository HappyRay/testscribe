from pathlib import Path

from pytest import fixture

from fixture.helper import get_test_data_root_path


def assert_file_content_same(actual_path: Path, expected_path: Path):
    """
    conftest.py file is designed to be used as a place to share fixtures.
    This custom assert function is here so that pytest will rewrite the asserts here.

    Pytest with pytest-clarity plugin gives better multiline error report than other
    https://github.com/darrenburns/pytest-clarity
    libraries such as assertpy
    https://github.com/assertpy/assertpy

    :param actual_path:
    :param expected_path:
    :return:
    """
    # keep this in this test file so that the assert can be rewritten by pytest
    # see https://docs.pytest.org/en/6.2.x/assert.html
    assert actual_path.exists()
    actual = actual_path.read_text()
    expected = expected_path.read_text()
    assert actual == expected


@fixture
def expected_test_data_path():
    return get_test_data_root_path().joinpath("result")


def assert_same(actual, expected):
    if actual != expected:
        print(f"Actual ({actual}) doesn't match expected ({expected})")
    assert actual == expected
