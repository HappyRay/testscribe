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

from testscribe import global_var
from testscribe.model_type import AllTests


def get_test_description(
    all_tests: AllTests, index_of_test_to_update: int, ask_for_description: bool
) -> str:
    default_test_description = get_default_description(
        all_tests=all_tests, index_of_test_to_update=index_of_test_to_update
    )
    if ask_for_description:
        return global_var.g_io.get_test_description(default_test_description)
    else:
        return default_test_description


def get_default_description(all_tests: AllTests, index_of_test_to_update: int):
    if index_of_test_to_update >= 0:
        return all_tests.tests[index_of_test_to_update].description
    else:
        return ""
