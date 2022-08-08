import pathlib
import test_scribe.config
from test_scribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from test_scribe.create_test_cmd import get_output_root_dir


def test_get_output_root_dir_from_config():
    config: test_scribe.config.Config = create_autospec(spec=test_scribe.config.Config)
    m_path: pathlib.Path = create_autospec(spec=pathlib.Path)
    config.output_root_path = m_path
    m_path.resolve.return_value = 1
    result = get_output_root_dir(output_root_dir=None, config=config)
    assert result == 1
    config.assert_not_called()
    m_path_mock_calls = get_normalized_mock_calls(m_path, pathlib.Path)
    assert m_path_mock_calls == [
        call.resolve(),
    ]
