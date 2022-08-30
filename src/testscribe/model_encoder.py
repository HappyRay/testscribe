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

from typing import Dict, List

from testscribe import scribe_file_key as key
from testscribe.model_type import (
    AllTests,
    TestModel,
    PatchModel,
    MockModel,
    MockCallModel,
)
from testscribe.namedvalues import NamedValues


def encode_model(all_tests: AllTests) -> dict:
    # It's possible to store the tests as dictionary keyed by the
    # test name.
    # however, since before python 3.6 (2016/12)
    # the dictionary won't keep the key insertion order.
    # Storing as a dictionary may result in unnecessary changes.
    # Also, the order is harder to control when updating, creating new tests.
    # see
    # https://stackoverflow.com/questions/1867861/how-to-keep-keys-values-in-same-order-as-declared
    # https://en.wikipedia.org/wiki/History_of_Python
    tests = encode_tests(all_tests)
    content = {
        key.FORMAT_VERSION: 1,
        key.MODULE: all_tests.module,
        key.TESTS: tests,
    }
    return content


def encode_tests(all_tests: AllTests) -> List[dict]:
    return [encode_one_test(t) for t in all_tests.tests]


def encode_one_test(test_model: TestModel) -> Dict:
    test = encode_name_and_description(test_model)
    # Encode information most tests share first
    # ensure consistency in the order of information among tests.
    encode_target(test=test, test_model=test_model)
    encode_parameters(test=test, test_model=test_model)
    encode_result(test=test, test_model=test_model)
    # encode patches before mocks since mocks may be more complex
    encode_patches(test=test, patches=test_model.patches)
    encode_mocks(test=test, mocks=test_model.mocks)
    return test


def encode_name_and_description(test_model: TestModel) -> dict:
    test = {key.NAME: test_model.name, key.SHORT_NAME: test_model.short_name}
    description = test_model.description
    if description:
        test[key.DESCRIPTION] = description
    return test


def encode_target(test: dict, test_model: TestModel) -> dict:
    target = {key.NAME: test_model.target_func_name}
    if test_model.target_class_name:
        target[key.CLASS_NAME] = test_model.target_class_name
    test[key.TARGET] = target
    return test


def encode_parameters(test: dict, test_model: TestModel) -> dict:
    init_values = encode_named_values(test_model.init_parameters)
    if init_values:
        # Don't include the key since a function (not a method)  will not have a need
        # for init parameters.
        test[key.INIT_PARAMETERS] = init_values
    if test_model.parameters:
        test[key.PARAMETERS] = encode_named_values(test_model.parameters)
    return test


def encode_named_values(values: NamedValues) -> List[dict]:
    # Encode as a list of dictionaries with the key "name" and "value"
    # Can't be a dictionary since some values may not have names.
    return [
        {key.NAME: name, key.VALUE: value} if name else {key.VALUE: value}
        for name, value in values.as_list()
    ]


def encode_result(test: dict, test_model: TestModel) -> dict:
    exception_model = test_model.exception
    if exception_model:
        test[key.EXCEPTION] = {
            key.TYPE: exception_model.type,
            key.MESSAGE: exception_model.message,
        }
    else:
        test[key.RESULT] = test_model.result
    return test


def encode_patches(test: dict, patches: List[PatchModel]) -> dict:
    if patches:
        test[key.PATCHES] = [
            {key.TARGET: p.target, key.PATCH_REPLACEMENT: p.replacement}
            for p in patches
        ]
    return test


def encode_mocks(test: dict, mocks: List[MockModel]) -> Dict:
    if mocks:
        test[key.MOCKS] = [encode_a_mock(m) for m in mocks]
    return test


def encode_a_mock(m: MockModel) -> Dict:
    encoded = {
        key.NAME: m.name,
        key.SPEC: m.spec_str,
    }
    calls = encode_mock_calls(m)
    if calls:
        encoded[key.CALLS] = calls
    attributes = m.attributes
    if attributes:
        encoded[key.ATTRIBUTES] = attributes
    return encoded


def encode_mock_calls(m: MockModel) -> List[dict]:
    return [encode_one_mock_call(c) for c in m.calls]


def encode_one_mock_call(mock_call: MockCallModel) -> dict:
    name = mock_call.name
    encoded = encode_one_mock_call_name(name)
    # noinspection PyTypeChecker
    encoded[key.PARAMETERS] = encode_named_values(mock_call.parameters)
    return_value = mock_call.return_value
    if return_value is not None:
        encoded[key.RETURN_VALUE] = return_value
    return encoded


def encode_one_mock_call_name(name: str) -> dict:
    return {key.NAME: name} if name else {}
