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

from typing import Callable

from testscribe import global_var
from testscribe.context import Context
from testscribe.namedvalues import NamedValues, NameNotFound
from testscribe.reflection_util import get_param_list
from testscribe.special_type import NoDefault


def get_parameter_value(
    func: Callable, context: Context, default: NamedValues
) -> NamedValues:
    param_info_list = get_param_list(func=func)
    if not param_info_list:
        return NamedValues()
    default_values = [
        get_default_value_from_old_params(default=default, index=index, name=param.name)
        for index, param in enumerate(param_info_list)
    ]
    # g_io is initialized after the module is imported
    # so directly importing g_io will get the default value only.
    return global_var.g_io.get_parameter_value(
        param_info_list=param_info_list, defaults=default_values, context=context
    )


def get_default_value_from_old_params(default: NamedValues, index: int, name: str):
    default_length = default.get_size()
    default_value = default.get_value_by_name(name)
    if default_value is NameNotFound:
        # If the name can't be found, it may be because the parameter
        # name has changed.
        # fall back to default to the parameter in the same position.
        if index < default_length:
            _, default_value = default[index]
        else:
            default_value = NoDefault
    return default_value
