import test_scribe.api.mock_api
from test_scribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from unittest.mock import patch
from test_data.file_op import write_to_file


def test_write_to_file():
    m_text_open_spec: test_scribe.api.mock_api.text_open_spec = create_autospec(spec=test_scribe.api.mock_api.text_open_spec)
    m_text_file_context_mgr_spec: test_scribe.api.mock_api.TextFileContextMgrSpec = create_autospec(spec=test_scribe.api.mock_api.TextFileContextMgrSpec)
    m_text_file_spec: test_scribe.api.mock_api.TextFileSpec = create_autospec(spec=test_scribe.api.mock_api.TextFileSpec)
    m_text_open_spec.return_value = m_text_file_context_mgr_spec
    m_text_file_context_mgr_spec.__enter__.return_value = m_text_file_spec
    m_text_file_context_mgr_spec.__exit__.return_value = True
    m_text_file_spec.write.return_value = 1
    with patch('test_data.file_op.open', m_text_open_spec):
        result = write_to_file(content='a', file_name='f')
    assert result is None
    m_text_open_spec_mock_calls = get_normalized_mock_calls(m_text_open_spec, test_scribe.api.mock_api.text_open_spec)
    assert m_text_open_spec_mock_calls == [
        call(file='f', mode='w'),
    ]
    m_text_file_context_mgr_spec_mock_calls = get_normalized_mock_calls(m_text_file_context_mgr_spec, test_scribe.api.mock_api.TextFileContextMgrSpec)
    assert m_text_file_context_mgr_spec_mock_calls == [
        call.__enter__(),
        call.__exit__(exc_type=None, exc_value=None, traceback=None),
    ]
    m_text_file_spec_mock_calls = get_normalized_mock_calls(m_text_file_spec, test_scribe.api.mock_api.TextFileSpec)
    assert m_text_file_spec_mock_calls == [
        call.write(content='a'),
    ]
