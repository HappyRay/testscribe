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
from testscribe.mock_proxy import MockProxy, is_mock_proxy


def mock_proxy_method_call():
    patch_globals_modified_by_mock_proxy()
    # has to explictly create MockProxy
    # if it is created via a parameter, in the generated test a MagicMock object
    # will be returned instead.
    # This works when the mock method doesn't return any value.
    # Otherwise, the generated code won't have the code to set the return value.
    # In general because the MockProxy is special, the logic has to be tested
    # via end-to-end tests.
    m = MockProxy(spec=C, name="m_c")
    return m.bar


def magic_len_method_throw_exception():
    patch_globals_modified_by_mock_proxy()
    m = MockProxy(spec=C, name="m_c")
    return m.__len__()


def is_mock_proxy_wrapper():
    patch_globals_modified_by_mock_proxy()
    # has to explictly create MockProxy
    # if it is created via a parameter, in the generated test a MagicMock object
    # will be returned instead.
    return is_mock_proxy(MockProxy(spec=C, name="m_c"))


def mock_pass_is_instance(c: C) -> bool:
    return isinstance(c, C)
