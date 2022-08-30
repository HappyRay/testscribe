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

from test_data.patch_function_for_integration_test import func_with_side_effect
from testscribe.api.mock_api import patch_with_expression, patch_with_mock


def patch_simple_int_value():
    patch_with_expression(
        target_str="test_data.simple.INT_VALUE", expression="2"
    )


def patch_func_with_side_effect():
    patch_with_mock(target=func_with_side_effect)
