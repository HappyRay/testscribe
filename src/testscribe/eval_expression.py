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

import logging
import re
from inspect import Signature, Parameter
from typing import Any

import testscribe.api.mock_api
from testscribe import global_var
from testscribe.api.alias import g_aliases
from testscribe.complex_value_util import generic_is_special_type
from testscribe.error import InputError
from testscribe.log import log
from testscribe.mock_proxy import MockProxy, is_mock_proxy
from testscribe.reflection_util import get_full_spec_name
from testscribe.type_util import get_class_type, get_type_origin, get_type_args
from testscribe.value_input_util import is_simple_value, import_modules_from_expression
from testscribe.value_util import InputValue

logger = logging.getLogger(__name__)


def eval_expression(user_input: str, t: type) -> Any:
    expression = expand_aliases(t=t, user_input=user_input)
    value = eval_with_injected_names(expression)
    # Have to use the user input string to generate the scribe and unit test
    # files if the input contains
    # classes or non builtin functions.
    # Can't use whether a fully qualified module name is detected as a test
    # because the m(type) expression should not be sufficient to be
    # stored as an expression.
    post_value = process_mock_marker(t=t, v=value)
    return wrap_input_value(expression=expression, v=post_value)


def expand_aliases(t: type, user_input: str) -> str:
    expression = expand_string_aliases(user_input)
    return expand_class_alias(t=t, expression=expression)


def expand_string_aliases(expression: str):
    for alias, full_str in g_aliases.items():
        expression = expand_one_string_alias(
            expression=expression, alias=alias, full_str=full_str
        )
    return expression


def expand_one_string_alias(expression: str, alias: str, full_str: str) -> str:
    """
    Replace user defined string aliases with their replacement strings in the
    expression.

    :param expression: input expression
    :param alias:
    :param full_str: replacement string
    :return: expanded expression
    """
    # The alias has to be surrounded by at least one non word or digit
    # Use ?: non-capturing group to avoid replacing these parts.
    # see
    # https://stackoverflow.com/questions/3512471/what-is-a-non-capturing-group-in-regular-expressions
    pattern = f"(?P<pre>^|\\W+){alias}(?P<after>$|\\W+)"
    logger.debug(f"Alias pattern: {pattern}")
    # Add the captured groups one before and one after the alias to avoid changing them.
    # Use named group instead of \1 and \2 to allow full_str to start with numbers.
    replacement_pattern = r"\g<pre>" + full_str + r"\g<after>"
    logger.debug(f"expression: {expression}")
    replaced, replacement_count = re.subn(
        pattern=pattern, repl=replacement_pattern, string=expression
    )
    if replacement_count:
        log(f"Expanded alias: {alias} {replacement_count} times.")
        log(f"Result after the expansion: {replaced}")
    return replaced


def expand_class_alias(t: type, expression: str) -> str:
    """
    Replace the expression with a new expression with the 'c' alias replaced
    with the class constructor.

    :param t: the expected type.
    :param expression: input expression
    :return: expanded expression if it contains a valid 'c' alias that can be matched
    to a class type
    """
    class_type = get_class_type(t)
    if class_type:
        # allows the name c to be used as an alias for the class type name.
        if expression.startswith("c("):
            expression = get_full_spec_name(class_type) + expression[1:]
    return expression


def eval_with_injected_names(expression: str) -> Any:
    # Mock object names are defined inside the generated functions, so they have
    # local scope.
    global_dict = global_var.g_name_mock_dict.copy()
    # Make the m function available to the expression.
    # The 'm' mock name is reserved so that there will be no name conflict.
    global_dict["m"] = testscribe.api.mock_api.m
    top_level_modules, _ = import_modules_from_expression(expression)
    value = eval(expression, top_level_modules, global_dict)
    return value


def process_mock_marker(t: type, v: Any) -> Any:
    """
    Translate the 'm' (mock marker) into mock objects in expressions
    e.g.
    [m] for a type List[C] is translated to [MockProxy(C)]
    See the unit tests for more examples.

    :param t: the expected type for the value
    :param v: the value the expression evaluates to
    :return: the translated value
    """
    if is_type_infor_unavailable(t):
        return v
    if is_mock_marker(v):
        return process_mock_marker_value(t=t)
    elif isinstance(v, list):
        return process_mock_marker_list(t=t, v=v)
    elif isinstance(v, tuple):
        return process_mock_marker_tuple(t=t, v=v)
    # mock marker in a set is not supported since a match by position
    # in the value is impossible.
    elif isinstance(v, dict):
        return process_mock_marker_dict(t=t, v=v)
    else:
        return v


def is_type_infor_unavailable(t: type) -> bool:
    return t in (Any, Signature.empty, Parameter.empty)


def is_mock_marker(value) -> bool:
    return value is testscribe.api.mock_api.m


def process_mock_marker_value(t: type):
    class_type = get_class_type(t)
    if class_type:
        return MockProxy(spec=class_type)
    else:
        raise_mock_marker_type_mismatch_error(f"The type ({t}) can't be mocked.")


def raise_mock_marker_type_mismatch_error(msg: str):
    raise InputError(msg)


def process_mock_marker_list(t: type, v: Any):
    # todo: handle Iterable type in a similar way
    if get_type_origin(t) is list:
        item_types = get_type_args(t)
        if len(item_types) == 1:
            # if List is used, there may not be any type information for its items
            (item_type,) = item_types
            return [process_mock_marker(v=item, t=item_type) for item in v]
    # The type may be Any or unknown, skip processing the mock marker.
    # In that case, it should be fine when the input value doesn't contain any
    # mock marker.
    # todo: check if the type is indeed Any or unknown, otherwise throw an exception.
    return v


def process_mock_marker_tuple(t: type, v: Any):
    if get_type_origin(t) is tuple:
        item_types = get_normalized_item_types(t=t, v=v)
        if not item_types:
            # Element type is unknown. e.g. the type is Tuple
            return v
        if len(v) != len(item_types):
            raise InputError(
                f"tuple value ({v}) size doesn't match the tuple type ({t})."
            )
        return tuple(
            [
                process_mock_marker(v=item, t=item_type)
                for item, item_type in zip(v, item_types)
            ]
        )
    else:
        # The type may be Any or unknown, skip processing the mock marker.
        # In that case, it should be fine when the input value doesn't contain any
        # mock marker.
        # todo: check if the type is indeed Any or unknown, otherwise throw an exception.
        return v


def get_normalized_item_types(t: type, v: Any):
    """
    Handle special case of ellipsis. e.g. Tuple[int, ...]
    :param t:
    :param v: a value of the type
    :return: tuple representing the types of the subcomponents
    """
    item_types = get_type_args(t)
    if len(item_types) == 2 and item_types[1] == Ellipsis:
        item_types_list = []
        for i in range(len(v)):
            item_types_list.append(item_types[0])
        item_types = tuple(item_types_list)
    return item_types


def process_mock_marker_dict(t: type, v: Any):
    if get_type_origin(t) is dict:
        args = get_type_args(t)
        if len(args) == 2:
            _, value_type = args
            return {
                key: process_mock_marker(t=value_type, v=value)
                for key, value in v.items()
            }
    # The dict type doesn't provide enough type information to support
    # the mock marker.
    # The type may be Any or unknown, skip processing the mock marker.
    # In that case, it should be fine when the input value doesn't contain any
    # mock marker.
    # todo: check if the type is indeed Any or unknown, otherwise throw an exception.
    return v


def wrap_input_value(expression: str, v: Any) -> Any:
    """
    Unlike output values which only need to be evaluated,
    input values need to be recreated in the generated tests.
    It's more reliable to use the user input instead of translating the value
    back to a proper constructor.
    e.g.
    If the expression evaluates to a class instance, it's easier to inspect/assert
    the class members than choosing the right constructor.
    Thus, is_simple_value only returns True for cases when constructing the value
    is reliable.
    :param expression: user input string after expanding aliases and mock markers.
    :param v: the value the expression evaluates to
    :return:
    """
    if is_simple_value(v):
        return v
    else:
        return process_complex_value(value=v, expression=expression)


def process_complex_value(value: Any, expression: str):
    if contain_mock_proxy(value) and is_m_function_in_expression(expression):
        # e.g. (m(test_data.simple.C), test_data.simple.C(1))
        # Generated code for parameter in the above example will be
        # (m_c, Object(type (test_data.simple.C), members ({'a': 1})))
        # It is ok if the MockProxy object is introduced via a
        # mock object name e.g. a parameter that is mocked.
        log(
            "Warning: mixing the 'm' function to create a mock object and other "
            "non primitive types in a user input will generate incorrect test files.\n"
            "Use a wrapper function to introduce the mock object via a named parameter "
            "and use that name in expressions instead.\n"
            "It still works to verify the test result one time and discard the "
            "generated test."
        )
        return value
        # todo: format the expression.
    return InputValue(expression=expression, value=value)


def contain_mock_proxy(value: Any) -> bool:
    """
    This method can't detect all cases. e.g.
    if a MockProxy object is used in the constructor of another object such as
    NamedValues.
    :param value:
    :return:
    """
    return generic_is_special_type(value=value, is_special_type_func=is_mock_proxy)


def is_m_function_in_expression(expression: str) -> bool:
    return M_FUNCTION_IN_EXPRESSION_PATTERN.search(expression) is not None


M_FUNCTION_IN_EXPRESSION_PATTERN = re.compile(r"(^|\W+)m *\(")
