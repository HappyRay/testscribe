from unittest.mock import Mock

from test_data.service import Service
from test_scribe.api.mock_api import get_normalized_mock_calls


def get_normalized_mock_calls_wrapper():
    m = Mock(Service)
    child_mock = m.search_a_name("a")
    child_mock.foo(1)
    m.search_person("b")
    return get_normalized_mock_calls(mock=m, spec=Service)
