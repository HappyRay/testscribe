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

from unittest.mock import patch, create_autospec

from testscribe.model_type import MockNameModel, TestModel, MockModel
from testscribe.value_input_util import transform_real_default_value


def transform_real_default_value_wrapper():
    m_test_model = create_autospec(spec=TestModel)
    m_mock_model = create_autospec(spec=MockModel)
    m_test_model.mocks = [m_mock_model]
    m_mock_model.name = "a"
    m_mock_model.spec_str = "spec"

    # During the test run global_var.g_test_to_infer_default_inputs is set
    # after the setup function is called so using the setup function to patch
    # doesn't work.
    with patch(
        "testscribe.value_input_util.global_var.g_test_to_infer_default_inputs",
        m_test_model,
    ):
        return transform_real_default_value(MockNameModel("a"))
