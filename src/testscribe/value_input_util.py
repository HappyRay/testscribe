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
from typing import Any, List, Tuple, Optional

from testscribe import global_var
from testscribe.ignore import IGNORED
from testscribe.mock_proxy import MockProxy
from testscribe.model_type import (
    MockNameModel,
    MockModel,
    get_mock_by_name,
    ExpressionModel,
    SetModel,
    TestModel,
)
from testscribe.reflection_util import get_module_str
from testscribe.special_type import NoDefault
from testscribe.user_triggered_exception import UserTriggeredException
from testscribe.util import remove_trailing_numbers, generic_transform

logger = logging.getLogger(__name__)


def is_simple_value(v) -> bool:
    """
    Does the value consist of str, bool, int, float, None, MockProxy only
    including all elements if the value is a collection.

    MockProxy will be represented by its name in the generated code.
    Thus, it is considered a "simple" value that doesn't need special handling.

    :param v:
    :return:
    """
    if v is None:
        return True
    t = type(v)
    if t in (str, bool, int, float, MockProxy):
        return True
    if t in (set, tuple, list):
        items = v
    elif t is dict:
        items = v.values()
    else:
        return False

    for e in items:
        if not is_simple_value(e):
            return False
    return True


def eval_special_value(
    value_str: str,
):
    """
    Check if the expression evaluates to UserTriggeredException or ignored
    if so return it otherwise return None.
    It doesn't raise an exception.
    """
    # avoid circular references
    from testscribe.api.mock_api import throw

    global_dict = {throw.__name__: throw, "ignore": IGNORED}
    # noinspection PyBroadException
    try:
        value = eval(value_str, {}, global_dict)
        if isinstance(value, UserTriggeredException) or value is IGNORED:
            return value
        else:
            return None
    except Exception:
        return None


def transform_default_value(default: Any, t: type) -> str:
    """
    Translate the default value into a string suitable as raw input.

    :param default:
    :param t: the expected type. Note it can be Any
    """
    if default is NoDefault:
        return transform_no_default_value(t)
    else:
        return transform_real_default_value(default)


def transform_real_default_value(default: Any) -> str:
    if default is None:
        return "None"
    elif isinstance(default, str):
        return default
    elif isinstance(default, ExpressionModel):
        return default.expression
    elif isinstance(default, SetModel) or is_simple_value(default):
        return repr(default)
    else:
        return transform_mock_names_to_mock_expression(
            v=default,
            test_to_infer_default_inputs=global_var.g_test_to_infer_default_inputs,
        )


def transform_no_default_value(t: type) -> str:
    if t is bool:
        return "False"
    else:
        return ""


def transform_mock_names_to_mock_expression(
    v: Any, test_to_infer_default_inputs: Optional[TestModel]
) -> str:
    """
    It's used to transform mock object value in a default value back to an expression
    string which can be used to recreate the same mock object.
    """
    if test_to_infer_default_inputs:

        def transform_one_mock_name_to_mock_expression_with_test(val: Any):
            return transform_one_mock_name_to_mock_expression(
                value=val, test_to_infer_default_inputs=test_to_infer_default_inputs
            )

        transformed = generic_transform(
            v=v, transform_func=transform_one_mock_name_to_mock_expression_with_test
        )
    else:
        transformed = v
    return repr(transformed)


def transform_one_mock_name_to_mock_expression(
    value: Any, test_to_infer_default_inputs: TestModel
):
    if isinstance(value, MockNameModel):
        mock_name = value.name
        mock_model: MockModel = get_mock_by_name(
            mocks=test_to_infer_default_inputs.mocks, name=mock_name
        )
        # Translate back to what users will have to type to create the same mock object.
        base_mock_name = remove_trailing_numbers(mock_name)
        return ExpressionModel(f"m({mock_model.spec_str}, '{base_mock_name}')")
    else:
        return value


def get_string_value(value: str) -> str:
    """
    Handle strings that are quoted which are necessary to support multiline strings.

    :param value: raw string input
    :return: string value
    """
    if value.startswith('"') or value.startswith("'"):
        # Allow multiline string input by allowing e.g. "a\nb"
        # i.e. enclose the input with "" or ''
        # to use escape characters.
        return eval(value)
    else:
        return value


def import_modules_from_expression(user_input: str) -> Tuple[dict, List[str]]:
    """
    Import modules referenced in the user input expression

    :param user_input:
    :return: tuple ( dict ( top package name -> top package reference),
    list of full module names found )
    """
    full_names = get_possible_fully_qualified_names(user_input)
    imports = {}
    module_names = []
    for name in full_names:
        top_package, module_name = try_import_module(name)
        if top_package:
            imports[top_package.__name__] = top_package
            module_names.append(module_name)
    return imports, module_names


def get_possible_fully_qualified_names(expression: str) -> List[str]:
    """
    Given a python expression string, return a list of possible fully qualified
    class names in the string.
    :param expression:
    :return:
    """
    all_captures = QUALIFIED_CLASS_NAME_PATTERN.findall(expression)
    return [full for full, _ in all_captures]


QUALIFIED_CLASS_NAME_PATTERN = re.compile(r"((\w+\.)+\w+)")


def try_import_module(name: str):
    """

    :param name: the fully qualified name of an object
    :return: a tuple ( top level package, full module name string ) or ( None, None) if
    the module can't be loaded.
    """
    while name:
        module_name = get_module_str(name)
        if module_name:
            top_package = import_module(module_name)
            if top_package:
                return top_package, module_name
        # The next component may be a class name etc. not a module name
        # e.g. inspect.Parameter.empty inspect is the module not inspect.Parameter.
        # todo: detect errors that a module name may be mis-spelled.
        name = module_name
    return None, None


def import_module(module_name: str):
    try:
        top_package = __import__(module_name)
        return top_package
    except ModuleNotFoundError:
        # This warning may show up when generating a new test and the file contains
        # a test with incorrectly detected module name in an expression.
        # todo: re-evalue
        # log(f"Failed to import possible module: ({module_name}). " f"exception: {e}")
        return None
