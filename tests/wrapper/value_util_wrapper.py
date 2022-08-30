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
from test_data.simple import C
from testscribe.mock_proxy import MockProxy
from testscribe.value_util import get_value_repr


def get_value_repr_wrapper_mock_proxy():
    """
    Need this wrapper to avoid MockProxy to be translated to its name
    or a MagicMock object in the generated code.
    """
    patch_globals_modified_by_mock_proxy()
    return get_value_repr(MockProxy(spec=C, name="a"))
