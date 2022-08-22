import pathlib
import test_data.complex_mock_call
from testscribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from test_data.complex_mock_call import call_mock_service_with_object


def test_call_mock_service_with_object():
    m_service: test_data.complex_mock_call.Service = create_autospec(spec=test_data.complex_mock_call.Service)
    m_service.f.return_value = None
    result = call_mock_service_with_object(s=m_service)
    assert result is None
    m_service_mock_calls = get_normalized_mock_calls(m_service, test_data.complex_mock_call.Service)
    assert m_service_mock_calls == [
        call.f(p=ANY),
    ]
    assert isinstance(m_service_mock_calls[0].kwargs['p'], pathlib.PosixPath)
    assert repr(m_service_mock_calls[0].kwargs['p']) == "PosixPath('foo')"
