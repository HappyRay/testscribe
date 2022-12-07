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
from typing import Any

from test_data.simple import D
from testscribe.mock_proxy_support import get_attribute_type


def test_get_attribute_type_dynamic_field_without_type_info():
    """
    Modified from a generated test.
    assert isinstance(result, typing._SpecialForm)
    no longer works in Python 3.11
    :return:
    """
    result = get_attribute_type(spec=D, name='a')
    assert result is Any
