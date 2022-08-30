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

from typing import Any
from unittest.mock import patch, create_autospec

from typer import prompt

from test_data.simple import C
from testscribe.execution_util import show_user_call_stack
from testscribe.mock_call import MockCall, get_call_description


def call_mock_call() -> Any:
    m_prompt = create_autospec(spec=prompt)
    m_prompt.return_value = 2
    m_show_user_call_stack = create_autospec(spec=show_user_call_stack)
    with patch("testscribe.value_input_cli.prompt", m_prompt), patch(
        "testscribe.mock_call.show_user_call_stack", m_show_user_call_stack
    ), patch("testscribe.mock_call.global_var.g_test_to_infer_default_inputs", None):
        m_c = MockCall(
            method_name="bar",
            mock_name="mock_name",
            spec=C,
            previous_call_count=0,
        )
        result = m_c(1)
    m_prompt.assert_called_once_with(
        "Please provide the value for the return value of type: (int)",
        default="",
        type=str,
    )
    m_show_user_call_stack.assert_called_once()
    return result, m_c


def get_call_description_wrapper(mock_call: MockCall) -> str:
    """
    Patching the show_user_call_stack using the tool itself interferes with
    the tool's function since the generated mock object will trigger the call.

    :param mock_call:
    :return:
    """
    m_show_user_call_stack = create_autospec(spec=show_user_call_stack)
    with patch("testscribe.mock_call.show_user_call_stack", m_show_user_call_stack):
        result = get_call_description(mock_call)
    m_show_user_call_stack.assert_called_once()
    return result
