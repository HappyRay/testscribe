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

from unittest.mock import Mock, call

from testscribe.api.mock_api import get_normalized_mock_calls


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
