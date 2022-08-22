import test_data.static_method
from testscribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from test_data.static_method import call_static_method


def test_call_static_method():
    m_static_service: test_data.static_method.StaticService = create_autospec(spec=test_data.static_method.StaticService)
    m_static_service.do.return_value = 2
    result = call_static_method(s=m_static_service)
    assert result == 2
    m_static_service_mock_calls = get_normalized_mock_calls(m_static_service, test_data.static_method.StaticService)
    assert m_static_service_mock_calls == [
        call.do(),
    ]
