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

from collections import Counter
from unittest.mock import patch, Mock, MagicMock

from pytest import fixture

import testscribe
from test_data.simple import C, foo
from testscribe.mock_call import MockCall
from testscribe.mock_proxy import MockProxy
from testscribe.model_type import MockNameModel


# Mocking out the functions such as prompt will distrupt the functions of
# the tool itself. Thus, these tests can't be generated.


@fixture(autouse=True)
def clear_mock_proxy_modified_globals():
    with patch(
        "testscribe.global_var.g_mock_name_counter",
        Counter(testscribe.global_var.g_mock_name_counter),
    ), patch("testscribe.global_var.g_name_mock_dict", {}):
        yield


@patch("testscribe.mock_call.show_user_call_stack", autospec=True)
@patch("testscribe.value_input_cli.prompt", autospec=True)
def test_mock_proxy_class_construction(mock_prompt, mock_show_user_call_stack: Mock):
    mock_prompt.return_value = "m"
    m = MockProxy(spec=C, name="m_c")
    c = m(1)
    assert isinstance(c, MockProxy)
    assert c.name_test_scribe_ == "m_c_1"
    assert c.spec_test_scribe_ == C
    mock_show_user_call_stack.assert_called_once()


@patch("testscribe.mock_call.show_user_call_stack", autospec=True)
@patch("testscribe.value_input_cli.prompt", autospec=True)
def test_mock_proxy_multiple_class_construction(
    mock_prompt, mock_show_user_call_stack: Mock
):
    """
    Test invoking mock proxy object multiple times

    :param mock_prompt:
    :param mock_show_user_call_stack:
    :return:
    """
    mock_prompt.return_value = "m"
    m = MockProxy(spec=C, name="m_c")
    c = m(1)
    assert isinstance(c, MockProxy)
    assert c.name_test_scribe_ == "m_c_1"
    assert c.spec_test_scribe_ == C
    mock_show_user_call_stack.assert_called_once()
    c2 = m(2)
    assert isinstance(c2, MockProxy)
    assert c2.name_test_scribe_ == "m_c_2"
    assert c2.spec_test_scribe_ == C
    calls = m.calls_test_scribe_
    assert len(calls) == 2
    i = calls[0]
    assert isinstance(i, MockCall)
    assert i.args.params == [("a", 1)]
    assert i.return_value == MockNameModel("m_c_1")

    i1 = calls[1]
    assert isinstance(i1, MockCall)
    assert i1.args.params == [("a", 2)]
    assert i1.return_value == MockNameModel("m_c_2")


@patch("testscribe.mock_proxy_support.MockCall", autospec=True)
def test_mock_proxy_mock_function(mock_mock_call: Mock):
    m_call = MagicMock()
    mock_mock_call.return_value = m_call
    m_call.call_internal.return_value = 0
    m = MockProxy(spec=foo, name="m_foo")
    r = m(1)
    assert r == 0
    assert m.calls_test_scribe_ == [m_call]
    m_call.call_internal.assert_called_once_with(1)
    mock_mock_call.assert_called_once_with(
        method_name="", spec=foo, mock_name="m_foo", previous_call_count=0
    )
