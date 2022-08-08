from __future__ import annotations

from distutils.util import strtobool
from typing import Any

from click import prompt

from test_scribe.eval_expression import eval_expression
from test_scribe.log import log
from test_scribe.reflection_util import get_type_name
from test_scribe.value_input_util import transform_default_value, eval_special_value, \
    get_string_value
from test_scribe.value_util import InputValue


def get_one_value_cli(prompt_name: str, t: type, default: Any):
    default_str = transform_default_value_cli(default=default, t=t)
    while True:
        try:
            return get_one_value_cli_internal(
                prompt_name=prompt_name, t=t, default=default_str
            )
        except Exception as e:
            msg = f"The value is invalid. Please try again.\nError detail:\n{str(e)}"
            log(msg)
            continue


def transform_default_value_cli(default: Any, t: type) -> str:
    default_str = transform_default_value(default=default, t=t)
    if isinstance(default, str) and t is not str:
        # Quote the string in case the type information is not available
        return repr(default_str)
    else:
        return default_str


def get_one_value_cli_internal(prompt_name: str, t: type, default: str):
    prompt_str = (
        f"Please provide the value for {prompt_name} of type: ({get_type_name(t)})"
    )
    raw_input_str = prompt(prompt_str, default=default, type=str)
    return post_process_raw_input(raw_input_str=raw_input_str, t=t)


def post_process_raw_input(raw_input_str: str, t: type) -> Any:
    eval_value = eval_special_value(raw_input_str)
    if eval_value is not None:
        return InputValue(expression=raw_input_str, value=eval_value)
    if t in {int, float, bool}:
        # noinspection PyTypeChecker
        return type_to_convert_func[t](raw_input_str)
    elif t is str:
        return get_string_value(raw_input_str)
    else:
        # assume the string is a valid python expression
        # ex. [1,2], ["a"], {"a": 2}, ('a', 1)
        return eval_expression(user_input=raw_input_str, t=t)


def convert_str_to_bool(s: str) -> bool:
    """
    True values are y, yes, t, true, on and 1; false values are n, no, f, false,
    off and 0.
    The input string is case-insensitive.
    Raises ValueError if s is anything else.

    :param s:
    :return:
    """
    return bool(strtobool(s))


type_to_convert_func = {int: int, float: float, bool: convert_str_to_bool}
