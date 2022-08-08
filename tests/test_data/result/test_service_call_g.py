import test_data.service
from test_scribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from test_data.service_call import gen_name


def test_simple_gen():
    """
    integration test
    """
    m_service: test_data.service.Service = create_autospec(spec=test_data.service.Service)
    m_service.search_a_name.return_value = 'b'
    m_service.search_a_number.side_effect = [2, 3]
    result = gen_name(service=m_service, keyword='a', start_number=1)
    assert result == '{"name": "b", "number": 5}'
    m_service_mock_calls = get_normalized_mock_calls(m_service, test_data.service.Service)
    assert m_service_mock_calls == [
        call.search_a_name(keyword='key: a'),
        call.search_a_number(seed_number=1),
        call.search_a_number(seed_number=2),
    ]
