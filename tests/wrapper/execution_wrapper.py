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

from typing import Callable, Any
from unittest.mock import patch

from test_data.greet import Greeter
from testscribe.execution import get_args_and_call, create_instance
from testscribe.namedvalues import NamedValues


def get_args_and_call_wrapper(func: Callable) -> Any:
    # Using the tool to patch prompt prevents the tool from getting the return value.
    with patch("testscribe.value_input_cli.prompt", autospec=True) as mock_prompt:
        mock_prompt.return_value = '"b"'
        return get_args_and_call(func=func, default=NamedValues())


def create_instance_wrapper():
    # Using the tool to patch prompt prevents the tool from getting the return value.
    with patch("testscribe.value_input_cli.prompt", autospec=True) as mock_prompt:
        mock_prompt.return_value = "a"
        r = create_instance(clazz=Greeter, test_to_infer_default_inputs=None)
        mock_prompt.assert_called_once_with(
            "Please provide the value for the parameter (my_name) of type: (str)",
            default="",
            type=str,
        )
        return r
