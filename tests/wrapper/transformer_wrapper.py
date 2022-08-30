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

from fixture.helper import patch_globals_modified_by_mock_proxy
from test_data import simple
from test_data.simple import C
from testscribe.mock_proxy import MockProxy
from testscribe.transformer import transform_value


def tranform_module():
    """
    The tool can't automatically import the module using an expression
    like test_data.simple yet.

    :return:
    """
    return transform_value(simple)


def transform_mock_proxy():
    """
    Without the wrapper, the tool will generate a statement like
    result = transform_value(v=a)
    since the mockproxy object will be replaced by its name.
    It doesn't work in this special case.

    :return:
    """
    patch_globals_modified_by_mock_proxy()
    return transform_value(MockProxy(C, "a"))
