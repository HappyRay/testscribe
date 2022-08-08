from __future__ import annotations

from typing import Callable

from test_scribe import global_var
from test_scribe.context import Context
from test_scribe.namedvalues import NamedValues, NameNotFound
from test_scribe.reflection_util import get_param_list
from test_scribe.special_type import NoDefault


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
