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

from typing import List, Iterable

from testscribe.config import g_indent
from testscribe.model_type import MockCallModel, ExpressionModel
from testscribe.type_util import is_class_type
from testscribe.util import BUILTIN_MODULE_NAME
from testscribe.value_input_util import eval_special_value


def pretty_format_repr_string(s: str) -> str:
    """
    Use triple double quotes for repr of a multi line string.
    except a string that
    only contains a single '\n' at the end
    or
    contains '\' or triple double quotes

    It's more readable than strings with multiple escape characters.

    :param s:
    :return:
    """
    if "\n" in s[:-1] and not ("\\" in s or '"""' in s):
        if s.endswith('"'):
            # escape the last double quote to avoid a syntax error.
            s = s[:-1] + '\\"'
        format_string = '''\
"""\\
{multi_line_string}"""'''
        return format_string.format(multi_line_string=s)
    return repr(s)


def join_lines(
    lines: List[str], prepend_new_line: bool = True, indentation_level: int = 0
) -> str:
    """
    Join lines with the new line character.
    If there is no line, returns an empty string.

    :param lines:
    :param prepend_new_line: has no effect if there is no line
    :param indentation_level:
    :return:
    """
    assert indentation_level >= 0
    normalized = remove_empty(lines)
    if normalized:
        if indentation_level:
            normalized = add_indentation_to_str_list(normalized, indentation_level)
        statements_str = "\n".join(normalized)
        if prepend_new_line:
            return "\n" + statements_str
        else:
            return statements_str
    else:
        return ""


def is_same_value(values: Iterable) -> bool:
    first = values[0]
    for v in values:
        if v != first:
            return False
    return True


def spec_contain_param_name_info(spec_str: str):
    return not (
        spec_str.startswith("typing.Callable")
        or spec_str.startswith("collections.abc.Callable")
        or spec_str.startswith("collections.Callable")
    )


def get_module_name(v: any) -> str:
    t = type(v)
    if is_class_type(t):
        module_name = t.__module__
        if BUILTIN_MODULE_NAME != module_name:
            return module_name
    return ""


def translate_special_mock_return_value(value):
    """
    Translate possible special values in a mock call return value.

    :param value:
    :return:
    """
    v = value
    if isinstance(value, ExpressionModel):
        special_value = eval_special_value(value.expression)
        if special_value is not None:
            v = special_value
    return v


def collect_return_values(mock_calls: List[MockCallModel]):
    """

    even if a method has no return value it implictly returns "None"
    "None" can also be a valid return value
    Without setting the mock return value in the generated code,
    a mock object will be returned.
    So evern if the return value is None, it is still necessary to set it.
    """
    return [translate_special_mock_return_value(m.return_value) for m in mock_calls]


def add_indentation(s: str, level: int) -> str:
    lines = s.split("\n")
    indented_lines = add_indentation_to_str_list(lines=lines, level=level)
    return "\n".join(indented_lines)


def add_indentation_to_str_list(lines: List[str], level: int) -> List[str]:
    leading_spaces = g_indent * level
    return [f"{leading_spaces}{line}" for line in lines]


def remove_empty(a_list: list) -> list:
    return [e for e in a_list if e]
