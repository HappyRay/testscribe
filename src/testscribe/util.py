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

import itertools
import logging
import re
from hashlib import md5
from importlib import import_module
from typing import List, Any

logger = logging.getLogger(__name__)

BUILTIN_MODULE_NAME = "builtins"


def generic_transform(v: Any, transform_func: callable) -> Any:
    def _transform(value: Any) -> Any:
        return generic_transform(v=value, transform_func=transform_func)

    # todo: transform the member values if it is a class.
    if isinstance(v, list):
        new_v = [_transform(item) for item in v]
    elif isinstance(v, tuple):
        new_v = tuple([_transform(item) for item in v])
    elif isinstance(v, set):
        new_v = {_transform(item) for item in v}
    elif isinstance(v, dict):
        new_v = {}
        # In python 3.7, the dict comprehension constructs value first.
        # new_v = {_transform(k): _transform(value) for k, value in v.items()}
        # This breaks a unit test.
        # To avoid this difference, have a tighter control on the order.
        for k, value in v.items():
            new_key = _transform(k)
            new_value = _transform(value)
            new_v[new_key] = new_value
    else:
        new_v = v
    return transform_func(new_v)


pattern = re.compile(r"(?<!^)(?=[A-Z])")


def convert_camel_case_to_snake_case(s: str):
    # adopted from
    # https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    snake_case_str = pattern.sub("_", s).lower()
    return snake_case_str


TRAILING_NUMBERS_PATTERN = re.compile(r"_\d+$")


def remove_trailing_numbers(s: str) -> str:
    return TRAILING_NUMBERS_PATTERN.sub("", s)


def flattern_list(list_of_list: List[List]):
    """
    It doesn't recursively flattern lists. e.g. input [[["a"]]]
    will result in [["a"]].
    :param list_of_list:
    :return:
    """
    return list(itertools.chain(*list_of_list))


def consistent_hash_str(s: str) -> int:
    return int(md5(s.encode()).hexdigest(), 16)


def load_object(symbol_name: str, module_str: str) -> Any:
    module_obj = import_module(module_str)
    obj = getattr(module_obj, symbol_name, None)
    return obj
