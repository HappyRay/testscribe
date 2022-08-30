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
#

from __future__ import annotations

from inspect import Parameter
from typing import Any, List

from click import echo, prompt

from testscribe.api.io_provider import IOProvider
from testscribe.constant import GET_TEST_NAME_PROMPT
from testscribe.context import Context
from testscribe.namedvalues import NamedValues
from testscribe.parameter_value_input_cli import get_parameter_value_cli
from testscribe.value_input_cli import get_one_value_cli
from testscribe.value_input_util import get_string_value


class CLI(IOProvider):
    def log(self, s: str) -> None:
        echo(s)

    def get_parameter_value(
        self, param_info_list: List[Parameter], defaults: list, context: Context
    ) -> NamedValues:
        return get_parameter_value_cli(
            param_info_list=param_info_list, defaults=defaults
        )

    def get_one_value(
        self, prompt_name: str, name: str, t: type, default: Any, context: Context
    ) -> Any:
        return get_one_value_cli(prompt_name=prompt_name, t=t, default=default)

    def get_test_description(self, default: str) -> str:
        return get_test_description_cli(default)

    def get_short_test_name(self, default_short_name: str) -> str:
        return get_short_test_name_cli(default_short_name)


def get_test_description_cli(default: str):
    prompt_str = "Provide a description of the test."
    input_str = prompt(prompt_str, default=default)
    # todo format the text so that each line is within a maximum size.
    return get_string_value(input_str)


def get_short_test_name_cli(default_short_name: str) -> str:
    return prompt(GET_TEST_NAME_PROMPT, default=default_short_name)
