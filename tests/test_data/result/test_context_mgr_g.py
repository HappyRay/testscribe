import test_data.context_mgr
from test_scribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from test_data.context_mgr import use_resource


def test_use_resource():
    m_gate: test_data.context_mgr.Gate = create_autospec(spec=test_data.context_mgr.Gate)
    m_gate_1: test_data.context_mgr.Gate = create_autospec(spec=test_data.context_mgr.Gate)
    m_resource: test_data.context_mgr.Resource = create_autospec(spec=test_data.context_mgr.Resource)
    m_gate.return_value = m_gate_1
    m_gate_1.__enter__.return_value = m_resource
    m_gate_1.__exit__.return_value = True
    m_resource.do_somthing.return_value = None
    result = use_resource(g=m_gate)
    assert result is None
    m_gate_mock_calls = get_normalized_mock_calls(m_gate, test_data.context_mgr.Gate)
    assert m_gate_mock_calls == [
        call(name='a'),
    ]
    m_gate_1_mock_calls = get_normalized_mock_calls(m_gate_1, test_data.context_mgr.Gate)
    assert m_gate_1_mock_calls == [
        call.__enter__(),
        call.__exit__(type=None, value=None, traceback=None),
    ]
    m_resource_mock_calls = get_normalized_mock_calls(m_resource, test_data.context_mgr.Resource)
    assert m_resource_mock_calls == [
        call.do_somthing(),
    ]
