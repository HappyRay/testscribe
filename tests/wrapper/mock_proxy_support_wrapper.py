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

from unittest.mock import patch

from fixture.helper import patch_g_mock_name_counter
from test_data.simple import D
from testscribe.mock_proxy_support import (
    create_unique_mock_name,
    get_mock_attribute_value,
)


def create_mock_name_twice():
    patch_g_mock_name_counter()
    name1 = create_unique_mock_name("a")
    name2 = create_unique_mock_name("a")
    return name1, name2


def get_mock_attribute_value_wrapper():
    with patch("testscribe.value_input_cli.prompt", autospec=True) as mock_prompt, patch(
        "testscribe.mock_proxy_support.show_user_call_stack", autospec=True
    ) as mock_show_user_call_stack, patch(
        "testscribe.mock_proxy_support.global_var.g_test_to_infer_default_inputs", None
    ):
        mock_prompt.return_value = "1"
        r = get_mock_attribute_value(attribute_name="a", mock_name="m", spec=D)
        mock_show_user_call_stack.assert_called_once()
        mock_prompt.assert_called_once_with(
            "Please provide the value for the a attribute of type: (any)",
            default="",
            type=str,
        )
        return r
