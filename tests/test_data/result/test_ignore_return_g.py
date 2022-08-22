import test_data.ignore_return
from testscribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from test_data.ignore_return import ignore_return


def test_ignore_return():
    m_s: test_data.ignore_return.S = create_autospec(spec=test_data.ignore_return.S)
    result = ignore_return(s=m_s)
    assert result is None
    m_s_mock_calls = get_normalized_mock_calls(m_s, test_data.ignore_return.S)
    assert m_s_mock_calls == [
        call.do(),
    ]
