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
from collections.abc import Callable
from typing import List, get_type_hints, Any, Optional

from testscribe import global_var
from testscribe.context import Context
from testscribe.custom_type import Spec
from testscribe.execution_util import show_user_call_stack
from testscribe.log import log
from testscribe.mock_call import MockCall
from testscribe.model_type import TestModel, MockModel, get_mock_by_name
from testscribe.special_type import NoDefault
from testscribe.type_util import get_type_origin
from testscribe.util import convert_camel_case_to_snake_case

UNSUPPORTED_ATTRIBUTES = {"__len__"}

logger = logging.getLogger(__name__)


def create_mock_name(name: str, spec: Spec) -> str:
    base_name = create_default_mock_name(spec) if name == "" else name
    return create_unique_mock_name(base_name)


def create_default_mock_name(spec: Spec) -> str:
    type_name_in_camel_case = convert_camel_case_to_snake_case(get_spec_name(spec))
    return f"m_{type_name_in_camel_case}"


def get_spec_name(spec: Spec) -> str:
    type_origin = get_type_origin(spec)
    if type_origin is Callable:
        # Callable doesn't have __qualname__ nor __name__ attribute
        return "Callable"
    else:
        # todo: is it possible that __qualname__ is not available?
        return spec.__qualname__


def create_unique_mock_name(name: str) -> str:
    counter = global_var.g_mock_name_counter
    unique_name = f"{name}_{counter[name]}" if name in counter else name
    counter[name] += 1
    return unique_name


def check_unsupported_attributes(attribute_name: str):
    # Debuggers call hasattr("<unsupported method name") which results in
    # these calls which are not part of the program's logic.
    if attribute_name in UNSUPPORTED_ATTRIBUTES:
        raise AttributeError(f"mocking the {attribute_name} method is not supported.")


def create_mock_call(
    method_name: str, mock_name: str, spec: Spec, mock_calls: List[MockCall]
) -> MockCall:
    logger.debug(f"Creating a new mock call ({method_name})")
    previous_call_count = get_previous_call_count(
        mock_calls=mock_calls, method_name=method_name
    )
    method = MockCall(
        method_name=method_name,
        mock_name=mock_name,
        spec=spec,
        previous_call_count=previous_call_count,
    )
    return method


def get_previous_call_count(mock_calls: List[MockCall], method_name: str) -> int:
    # how many times has this method been called
    count = 0
    for call in mock_calls:
        if call.method_name == method_name:
            count += 1
    return count


def get_attribute_type(spec: Spec, name: str) -> type:
    t = get_type_from_type_hints(spec, name)
    if t is None:
        if name in dir(spec):
            # type hints method below doesn't work for methods
            attrib = getattr(spec, name)
            t = type(attrib)
        else:
            t = Any
    return t


def get_type_from_type_hints(spec: Spec, attribute_name: str) -> Optional[type]:
    """
    Get type information from attribute's type annotation.

    dataclass for example doesn't seem to have a way to define class variables
    for the purpose of providing type information for a field.
    e.g.
    field1 = 5 will create a class variable but not a field.

    field1: int = 5 will not create a class variable
    get_type_hints(data class) will return {'field1': <class 'int'>} in this case.

    get_type_hints(a function) will return type annotations for the
    parameters and return value
    e.g. {'p': <class 'test_data.person.Person'>, 'return': <class 'str'>}

    """
    hints = get_type_hints(spec)
    return hints.get(attribute_name, None)


def get_default_mock_attribute_value(
    mock_name: str,
    attribute_name: str,
    test_to_infer_default_inputs: Optional[TestModel],
) -> Any:
    if test_to_infer_default_inputs:
        existing_mock = get_mock_by_name(
            mocks=test_to_infer_default_inputs.mocks, name=mock_name
        )
        return infer_default_mock_attribute_value_from_mock(
            attribute_name=attribute_name, existing_mock=existing_mock
        )
    return NoDefault


def infer_default_mock_attribute_value_from_mock(
    attribute_name: str, existing_mock: Optional[MockModel]
) -> Any:
    if existing_mock:
        return existing_mock.attributes.get(attribute_name, NoDefault)
    else:
        return NoDefault


def get_mock_attribute_value(attribute_name: str, mock_name: str, spec: Spec):
    # todo: create a strict mode to check the spec for valid
    #  attributes.
    # Many attributes are created dynamically, so it is error
    # prone to check by default. see
    # https://docs.python.org/3/library/unittest.mock.html#auto-speccing
    log(
        f"Mock object {mock_name}'s ( {attribute_name} )"
        " attribute is accessed for the first time."
    )
    # 3 frames between user code and show_user_call_stack
    # __getattr__, record_attribute, get_mock_attribute_value
    # if the call stack changes, adjust the parameter here.
    show_user_call_stack(additional_num_system_frame=3)
    description = f"Mock object {mock_name}'s {attribute_name} attribute"
    t = get_attribute_type(spec=spec, name=attribute_name)
    default = get_default_mock_attribute_value(
        mock_name=mock_name,
        attribute_name=attribute_name,
        test_to_infer_default_inputs=global_var.g_test_to_infer_default_inputs,
    )
    # avoid circular dependency
    from testscribe.value_input import get_one_value

    input_value = get_one_value(
        prompt_name=f"the {attribute_name} attribute",
        t=t,
        context=Context(description),
        default=default,
    )
    return input_value
