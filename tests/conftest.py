#  Copyright 2022 Ruiguo (Ray) Yang
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

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
