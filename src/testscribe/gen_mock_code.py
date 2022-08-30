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

from collections import defaultdict
from typing import List, Any

from testscribe.code_gen_util import (
    collect_return_values,
    is_same_value,
    join_lines,
)
from testscribe.ignore import IGNORED
from testscribe.model_type import MockModel, MockCallModel
from testscribe.user_triggered_exception import UserTriggeredException


def generate_property_init_statements(mock: MockModel) -> List[str]:
    return [
        f"{mock.name}.{name} = {repr(value)}" for name, value in mock.attributes.items()
    ]


def create_call_dict_indexed_by_method_name(mock_calls: List[MockCallModel]) -> dict:
    call_by_method_name = defaultdict(list)
    for call in mock_calls:
        method_name = call.name
        call_by_method_name[method_name].append(call)
    return call_by_method_name


def has_not_ignored_return_value(values):
    for v in values:
        if v is not IGNORED:
            return True
    return False


def gen_mock_return_values_for_one_method_with_return_values(
    mock_object_name: str, method_name: str, return_values: List[Any]
) -> str:
    if return_values:
        name = get_full_mock_method_name(method_name, mock_object_name)
        first_value = return_values[0]
        if is_single_real_return_value(return_values):
            return f"{name}.return_value = {repr(first_value)}"
        elif has_not_ignored_return_value(return_values):
            return f"{name}.side_effect = {repr(return_values)}"
    return ""


def is_single_real_return_value(return_values: List[Any]) -> bool:
    first_value = return_values[0]
    return (
        is_same_value(return_values)
        and not isinstance(first_value, UserTriggeredException)
        and first_value is not IGNORED
    )


def get_full_mock_method_name(method_name: str, mock_object_name: str) -> str:
    """
    Return the string used to identify the mock method.
    If the mock call is a call on the mock object itself the string will be
    the name of the mock object.

    :param method_name:
    :param mock_object_name:
    :return:
    """
    name = f"{mock_object_name}"
    if method_name:
        name += f".{method_name}"
    return name


def gen_mock_return_values_for_one_method(
    mock_object_name: str, method_name: str, methods: List[MockCallModel]
):
    return_values = collect_return_values(methods)
    return gen_mock_return_values_for_one_method_with_return_values(
        mock_object_name=mock_object_name,
        method_name=method_name,
        return_values=return_values,
    )


def generate_mock_return_values(mock: MockModel) -> List[str]:
    call_by_method_name = create_call_dict_indexed_by_method_name(mock.calls)
    # Assume empty elements in the list will be filtered out later
    return [
        gen_mock_return_values_for_one_method(
            mock_object_name=mock.name, method_name=method_name, methods=methods
        )
        for method_name, methods in call_by_method_name.items()
    ]


def generate_one_mock_creation_statement(mock: MockModel) -> str:
    spec = mock.spec_str
    # todo: add an option to allow spec_set=True to be set for stronger checks
    # see
    # https://docs.python.org/3/library/unittest.mock.html#unittest.mock.create_autospec
    return f"{mock.name}: {spec} = create_autospec(spec={spec})"


def generate_behavior_statements_for_one_mock(mock: MockModel) -> List[str]:
    property_init_statements = generate_property_init_statements(mock)
    return_value_statements = generate_mock_return_values(mock)
    return property_init_statements + return_value_statements


def generate_mock_behavior_statements(mocks: List[MockModel]) -> List[str]:
    statements = []
    for m in mocks:
        statements_for_one_mock = generate_behavior_statements_for_one_mock(m)
        statements.extend(statements_for_one_mock)
    return statements


def generate_mocks_str(mocks: List[MockModel]) -> str:
    # Create all the mock creation statements first
    # so that they can be freely referenced later including as return values.
    mock_creation_statements = [generate_one_mock_creation_statement(m) for m in mocks]
    mock_behavior_statements = generate_mock_behavior_statements(mocks)
    return join_lines(
        mock_creation_statements + mock_behavior_statements,
        prepend_new_line=True,
        indentation_level=1,
    )
