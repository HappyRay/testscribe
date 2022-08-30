"""
The in memory representation of all the tests
"""
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
from typing import Optional, List

from testscribe import global_var
from testscribe.description import get_test_description
from testscribe.input_params import (
    InputParams,
    get_target_function_name,
    get_target_class_name,
)
from testscribe.mock_proxy import MockProxy
from testscribe.model_type import (
    MockCallModel,
    MockModel,
    PatchModel,
    ExceptionModel,
    TestModel,
    AllTests,
    add_test,
    update_test,
)
from testscribe.patcher import Patcher
from testscribe.reflection_util import get_full_spec_name
from testscribe.runtime_values import RuntimeValues
from testscribe.test_name import get_test_name

logger = logging.getLogger(__name__)


def generate_model(
    input_params: InputParams,
    runtime_values: RuntimeValues,
    all_tests: AllTests,
    index_of_test_to_update: int,
) -> AllTests:
    target_func_name = get_target_function_name(input_params)
    short_name, test_name = get_test_name(
        all_tests=all_tests,
        index_of_test_to_update=index_of_test_to_update,
        ask_for_test_name=input_params.ask_for_test_name,
        target_func_name=target_func_name,
    )
    description = get_test_description(
        all_tests=all_tests,
        index_of_test_to_update=index_of_test_to_update,
        ask_for_description=input_params.ask_for_description,
    )
    new_test = TestModel(
        name=test_name,
        short_name=short_name,
        description=description,
        target_func_name=target_func_name,
        target_class_name=get_target_class_name(input_params),
        init_parameters=runtime_values.init_values,
        parameters=runtime_values.values,
        exception=get_exception_model(runtime_values.exception),
        result=runtime_values.result,
        mocks=get_mock_models(global_var.g_name_mock_dict.values()),
        patches=get_patch_models(global_var.g_patchers.values()),
    )
    return create_new_all_tests(
        all_tests=all_tests,
        index_of_test_to_update=index_of_test_to_update,
        new_test=new_test,
    )


def get_exception_model(exception: Optional[Exception]) -> Optional[ExceptionModel]:
    if exception:
        return ExceptionModel(
            type=get_full_spec_name(type(exception)), message=str(exception)
        )
    else:
        return None


def get_mock_models(mocks: List[MockProxy]) -> List[MockModel]:
    return [generate_mock_model(m) for m in mocks]


def generate_mock_model(mock: MockProxy):
    call_models = [
        MockCallModel(
            name=c.method_name,
            parameters=c.args,
            return_value=c.return_value,
        )
        for c in mock.calls_test_scribe_
        # todo: c.args is None only when MockCall is not called.
        # can this happen when a mock's method is referenced but not called?
        # document an example.
        if c.args
    ]
    return MockModel(
        name=mock.name_test_scribe_,
        spec_str=get_full_spec_name(mock.spec_test_scribe_),
        calls=call_models,
        attributes=mock.attributes_transformed_test_scribe_,
    )


def get_patch_models(patches: List[Patcher]) -> List[PatchModel]:
    return [create_patch_model(p) for p in patches]


def create_patch_model(p: Patcher):
    # This assumes the replacement_spec contains transformed value.
    return PatchModel(target=p.target, replacement=p.replacement_spec)


def create_new_all_tests(
    all_tests: AllTests, index_of_test_to_update: int, new_test: TestModel
):
    if index_of_test_to_update < 0:
        new_all_tests = add_test(all_tests=all_tests, test=new_test)
    else:
        new_all_tests = update_test(
            all_tests=all_tests, index=index_of_test_to_update, test=new_test
        )
    return new_all_tests
