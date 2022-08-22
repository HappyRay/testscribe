import test_data.simple
from testscribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from test_data.str_method import get_str


def test_get_str():
    m_c: test_data.simple.C = create_autospec(spec=test_data.simple.C)
    m_c.__str__.return_value = 'mock m_c'
    result = get_str(c=m_c)
    assert result == 'mock m_c'
    m_c_mock_calls = get_normalized_mock_calls(m_c, test_data.simple.C)
    assert m_c_mock_calls == [
        call.__str__(),
    ]
