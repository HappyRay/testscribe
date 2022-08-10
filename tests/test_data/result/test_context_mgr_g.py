import test_data.context_mgr
from test_scribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from test_data.context_mgr import use_resource


def test_use_resource():
    m_gate: test_data.context_mgr.Gate = create_autospec(spec=test_data.context_mgr.Gate)
    m_gate.__enter__.return_value = 1
    m_gate.__exit__.return_value = True
    result = use_resource(g=m_gate)
    assert result == 1
    m_gate_mock_calls = get_normalized_mock_calls(m_gate, test_data.context_mgr.Gate)
    assert m_gate_mock_calls == [
        call.__enter__(),
        call.__exit__(a_type=None, value=None, traceback=None),
    ]
