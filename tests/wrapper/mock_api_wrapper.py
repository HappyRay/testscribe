from unittest.mock import Mock

from fixture.helper import patch_globals_modified_by_mock_proxy
from test_data.service import Service
from test_data.simple import C
from test_scribe.api.mock_api import get_normalized_mock_calls, m
from test_scribe.mock_proxy import MockProxy


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
