import test_data.simple
from test_scribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from test_data.mock_str_method import print_simple_data_class


def test_print_simple_data_class():
    m_simple_data_class: test_data.simple.SimpleDataClass = create_autospec(spec=test_data.simple.SimpleDataClass)
    m_simple_data_class.__str__.return_value = 'mock m_simple_data_class'
    result = print_simple_data_class(s=m_simple_data_class)
    assert result == 'mock m_simple_data_class'
    m_simple_data_class_mock_calls = get_normalized_mock_calls(m_simple_data_class, test_data.simple.SimpleDataClass)
    assert m_simple_data_class_mock_calls == [
        call.__str__(),
    ]
