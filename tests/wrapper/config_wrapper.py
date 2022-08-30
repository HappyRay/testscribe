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

from inspect import Parameter
from typing import Any, List

from testscribe import global_var
from testscribe.api.io_provider import IOProvider
from testscribe.api.mock_api import patch_with_expression
from testscribe.config import initialize_io
from testscribe.context import Context
from testscribe.namedvalues import NamedValues


class TestIo(IOProvider):

    def log(self, s: str) -> None:
        pass

    def get_parameter_value(self, param_info_list: List[Parameter], defaults: list, context: Context) -> NamedValues:
        pass

    def get_one_value(self, prompt_name: str, name: str, t: type, default: Any, context: Context) -> Any:
        pass

    def get_test_description(self, default: str) -> str:
        pass

    def get_short_test_name(self, default_short_name: str) -> str:
        pass


def initialize_io_wrapper():
    # patch the global g_io so that it is restored after the test
    patch_with_expression(target_str="testscribe.global_var.g_io", expression="None")
    initialize_io({"io-provider-full-class-name": "wrapper.config_wrapper.TestIo"})
    assert isinstance(global_var.g_io, TestIo)
