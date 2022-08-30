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
from typing import Tuple, Set

from testscribe import global_var
from testscribe.model_type import AllTests
from testscribe.util import convert_camel_case_to_snake_case

logger = logging.getLogger(__name__)


def get_test_name(
    all_tests: AllTests,
    index_of_test_to_update: int,
    ask_for_test_name: bool,
    target_func_name: str,
) -> Tuple[str, str]:
    short_name = get_short_name(
        all_tests=all_tests,
        ask_for_test_name=ask_for_test_name,
        index_of_test_to_update=index_of_test_to_update,
    )
    test_name = create_test_name(
        all_tests=all_tests,
        index_of_test_to_update=index_of_test_to_update,
        short_name=short_name,
        target_func_name=target_func_name,
    )
    return short_name, test_name


def get_short_name(
    all_tests: AllTests, ask_for_test_name: bool, index_of_test_to_update: int
) -> str:
    default_short_name = get_default_short_name(
        all_tests=all_tests, index_of_test_to_update=index_of_test_to_update
    )
    raw_short_name = get_raw_short_name(
        default_short_name=default_short_name, ask_for_test_name=ask_for_test_name
    )
    short_name = create_proper_short_name(raw_short_name)
    return short_name


def get_default_short_name(all_tests: AllTests, index_of_test_to_update: int) -> str:
    if index_of_test_to_update < 0:
        return "_"
    else:
        return all_tests.tests[index_of_test_to_update].short_name


def get_raw_short_name(default_short_name: str, ask_for_test_name: bool) -> str:
    if ask_for_test_name:
        return global_var.g_io.get_short_test_name(default_short_name)
    else:
        return default_short_name


def create_proper_short_name(raw_short_name: str) -> str:
    return convert_camel_case_to_snake_case(raw_short_name.replace(" ", "_"))


def create_test_name(
    all_tests: AllTests,
    index_of_test_to_update: int,
    short_name: str,
    target_func_name: str,
) -> str:
    base_name = create_proper_test_name(
        short_name=short_name, target_func_name=target_func_name
    )
    test_name = generate_unique_test_name(
        base_name=base_name,
        all_tests=all_tests,
        test_to_update_index=index_of_test_to_update,
    )
    return test_name


def create_proper_test_name(short_name: str, target_func_name: str) -> str:
    # It's easier to read and simpler to implement if we don't include
    # class name in the test name.
    # Assuming it is rare there will be methods/functions with same name in
    # the same module. Even when it happens, the test names will still be unique
    # in the same file.
    name = replace_leading_underscore_with_function_name(
        s=short_name, function_name=target_func_name
    )
    return "test_" + name


def replace_leading_underscore_with_function_name(s: str, function_name: str) -> str:
    if s == "_":
        return function_name
    if s.startswith("_"):
        return function_name + s
    return s


def generate_unique_test_name(
    base_name: str, all_tests: AllTests, test_to_update_index: int
) -> str:
    name = base_name
    count = 0
    other_test_names = get_other_test_names(
        test_to_update_index=test_to_update_index, all_tests=all_tests
    )
    while name in other_test_names:
        # This will try to find the smallest postfix number that avoids name conflict.
        # e.g. If there is a test_foo and test_foo_2 test, it will generate test_foo_1
        count += 1
        name = f"{base_name}_{count}"
    return name


def get_other_test_names(test_to_update_index: int, all_tests: AllTests) -> Set[str]:
    tests = all_tests.tests
    return {
        # If this is part of an update test operation, the name of this test
        # should be ignored for the purpose of avoiding name conflicts
        # since it will be overwritten.
        tests[i].name
        for i in range(len(tests))
        if i != test_to_update_index
    }
