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
from test_data.service import Service
from test_data.simple import C
from testscribe.api.mock_api import get_normalized_mock_calls, m
from testscribe.mock_proxy import MockProxy


def get_normalized_mock_calls_wrapper():
    m_service = Mock(Service)
    child_mock = m_service.search_a_name("a")
    child_mock.foo(1)
    m_service.search_person("b")
    return get_normalized_mock_calls(mock=m_service, spec=Service)


def m_wrapper(name: str):
    """
    Since the return value is a MockProxy which is treated differently by the tool,
    this wrapper is needed to get around the issue.
    :return:
    """
    patch_globals_modified_by_mock_proxy()
    m_proxy = m(spec=C, name=name) if name else m(spec=C)
    assert isinstance(m_proxy, MockProxy)
    return m_proxy.spec_test_scribe_, m_proxy.name_test_scribe_
