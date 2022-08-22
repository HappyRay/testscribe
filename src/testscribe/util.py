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
        new_v = {_transform(k): _transform(value) for k, value in v.items()}
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
