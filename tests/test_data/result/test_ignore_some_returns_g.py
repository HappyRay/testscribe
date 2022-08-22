import test_data.ignore_some_returns
from testscribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from test_data.ignore_some_returns import ignore_some_returns


def test_ignore_some_returns():
    m_s: test_data.ignore_some_returns.S = create_autospec(spec=test_data.ignore_some_returns.S)
    m_s.do.side_effect = ['Ignored', 2]
    result = ignore_some_returns(s=m_s)
    assert result == 2
    m_s_mock_calls = get_normalized_mock_calls(m_s, test_data.ignore_some_returns.S)
    assert m_s_mock_calls == [
        call.do(i=1),
        call.do(i=2),
    ]
