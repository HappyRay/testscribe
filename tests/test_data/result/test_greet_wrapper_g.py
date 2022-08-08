import test_data.greet
from test_scribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
import pytest
from test_data.greet_wrapper import greet_mock_greeter


def test_greet_mock_greeter():
    m_greeter: test_data.greet.Greeter = create_autospec(spec=test_data.greet.Greeter)
    m_greeter.greet.side_effect = [Exception()]
    with pytest.raises(Exception) as exception_info:
        greet_mock_greeter(g=m_greeter, to='a', words='b')
    assert '' == str(exception_info.value)
    m_greeter_mock_calls = get_normalized_mock_calls(m_greeter, test_data.greet.Greeter)
    assert m_greeter_mock_calls == [
        call.greet(to='a'),
    ]
