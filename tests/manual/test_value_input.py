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

import test_data.simple
from fixture.helper import create_mock_proxy
from testscribe.value_input_util import is_simple_value


def test_is_simple_value_mock():
    # This test can't be generated because MockProxy
    # is a special type and is replaced with a Mock object
    # when running the test.
    r = is_simple_value(create_mock_proxy(spec=test_data.simple.C))
    assert r is True
