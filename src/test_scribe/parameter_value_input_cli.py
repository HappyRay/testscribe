from __future__ import annotations

from inspect import Parameter
from typing import List

from test_scribe.context import Context
from test_scribe.namedvalues import NamedValues
from test_scribe.value_input import get_one_value


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
