import test_data.class_method
from testscribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from test_data.class_method import call_class_method


def test_call_class_method():
    m_class_service: test_data.class_method.ClassService = create_autospec(spec=test_data.class_method.ClassService)
    m_class_service.do.return_value = 2
    result = call_class_method(s=m_class_service)
    assert result == 2
    m_class_service_mock_calls = get_normalized_mock_calls(m_class_service, test_data.class_method.ClassService)
    assert m_class_service_mock_calls == [
        call.do(),
    ]
