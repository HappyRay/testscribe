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
from typing import List

from testscribe.context import Context
from testscribe.namedvalues import NamedValues
from testscribe.value_input import get_one_value


def get_parameter_value_cli(
    param_info_list: List[Parameter], defaults: list
) -> NamedValues:
    params = []
    for param, default_value in zip(param_info_list, defaults):
        v = get_one_value(
            prompt_name=f"the parameter ({param.name})",
            name=param.name,
            t=param.annotation,
            context=Context(""),
            default=default_value,
        )
        params.append((param.name, v))
    # log(f"Params:{params}")
    return NamedValues(params)
