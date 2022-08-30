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

import test_data
from test_data.simple import C
from testscribe import global_var
from testscribe.api.mock_api import patch_with_mock, patch_with_expression


def test_patch_with_mock_no_effect_when_not_in_test_session():
    assert not global_var.g_test_generating_mode
    patch_with_mock("test_data.simple.C")
    assert test_data.simple.C == C


def test_patch_with_expression_no_effect_when_not_in_test_session():
    assert not global_var.g_test_generating_mode
    patch_with_expression("test_data.simple.C", 1)
    assert test_data.simple.C == C
