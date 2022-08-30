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

from inspect import Parameter
from pathlib import Path
from typing import Any, List

from testscribe.context import Context
from testscribe.namedvalues import NamedValues


class IOProvider:
    """
    The input and output plugin module implementations need to support these methods.
    """

    def __init__(self):
        pass

    def end(self, scribe_file_path: Path):
        pass

    def log(self, s: str) -> None:
        raise NotImplementedError()

    def get_parameter_value(
        self, param_info_list: List[Parameter], defaults: list, context: Context
    ) -> NamedValues:
        """

        :param param_info_list: the list should not be empty, the no parameter case
        should have been handled by the caller.
        :param defaults: corresponding default values for the parameters
        :param context:
        :return:
        """
        raise NotImplementedError()

    def get_one_value(
        self, prompt_name: str, name: str, t: type, default: Any, context: Context
    ) -> Any:
        raise NotImplementedError()

    def get_test_description(self, default: str) -> str:
        raise NotImplementedError()

    def get_short_test_name(self, default_short_name: str) -> str:
        raise NotImplementedError()
