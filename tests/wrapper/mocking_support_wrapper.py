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

from unittest.mock import Mock

from fixture.helper import patch_globals_modified_by_mock_proxy
from test_data.calculator import add
from test_data.return_callable import return_fixed_func
from test_data.service import Service
from test_data.simple import C
from testscribe.mock_proxy import MockProxy
from testscribe.mocking_support import normalize_mock_call, get_direct_mock_calls, \
    get_target_str_from_obj


def normalize_method_mock_call():
    m = Mock(Service)
    m.search_a_name("a")
    return normalize_mock_call(m.mock_calls[0], Service)


def normalize_function_mock_call():
    m = Mock(add)
    m(1, b=2)
    return normalize_mock_call(m.mock_calls[0], add)


def get_direct_mock_calls_func():
    m = Mock(return_fixed_func)
    mock_foo = m()
    mock_foo()
    return get_direct_mock_calls(m)


def get_direct_mock_calls_method():
    m = Mock(Service)
    child_mock = m.search_a_name("a")
    child_mock.foo(1)
    child_mock2 = m.search_person("b")
    child_mock2()
    return get_direct_mock_calls(m)


def get_target_str_from_obj_mock_proxy():
    patch_globals_modified_by_mock_proxy()
    # has to explictly create MockProxy
    # if it is created via a parameter, in the generated test a MagicMock object
    # will be returned instead.
    return get_target_str_from_obj(MockProxy(spec=C, name="m_c"))
