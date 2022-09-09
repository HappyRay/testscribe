import logging
import logging.config
import pathlib
import testscribe.execution_util
import testscribe.model_type
from testscribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from unittest.mock import patch
from testscribe.execution_util import config_logging, create_unit_test_file_name, infer_unit_test_file_path_from_scribe_file, remove_file_if_no_test


def test_config_logging_no_config_file():
    m_does_logging_config_file_exist: testscribe.execution_util.does_logging_config_file_exist = create_autospec(spec=testscribe.execution_util.does_logging_config_file_exist)
    m_basic_config: logging.basicConfig = create_autospec(spec=logging.basicConfig)
    m_does_logging_config_file_exist.return_value = False
    with patch('testscribe.execution_util.does_logging_config_file_exist', m_does_logging_config_file_exist), patch('testscribe.execution_util.basicConfig', m_basic_config):
        result = config_logging()
    assert result is None
    m_does_logging_config_file_exist_mock_calls = get_normalized_mock_calls(m_does_logging_config_file_exist, testscribe.execution_util.does_logging_config_file_exist)
    assert m_does_logging_config_file_exist_mock_calls == [
        call(),
    ]
    m_basic_config_mock_calls = get_normalized_mock_calls(m_basic_config, logging.basicConfig)
    assert m_basic_config_mock_calls == [
        call(),
    ]


def test_config_logging_with_config_file():
    m_does_logging_config_file_exist: testscribe.execution_util.does_logging_config_file_exist = create_autospec(spec=testscribe.execution_util.does_logging_config_file_exist)
    m_file_config: logging.config.fileConfig = create_autospec(spec=logging.config.fileConfig)
    m_does_logging_config_file_exist.return_value = True
    with patch('testscribe.execution_util.does_logging_config_file_exist', m_does_logging_config_file_exist), patch('testscribe.execution_util.fileConfig', m_file_config):
        result = config_logging()
    assert result is None
    m_does_logging_config_file_exist_mock_calls = get_normalized_mock_calls(m_does_logging_config_file_exist, testscribe.execution_util.does_logging_config_file_exist)
    assert m_does_logging_config_file_exist_mock_calls == [
        call(),
    ]
    m_file_config_mock_calls = get_normalized_mock_calls(m_file_config, logging.config.fileConfig)
    assert m_file_config_mock_calls == [
        call(fname='test_scribe_logging.conf', disable_existing_loggers=False),
    ]


def test_create_unit_test_file_name():
    result = create_unit_test_file_name(base_name='b')
    assert result == 'test_b_g.py'


def test_infer_unit_test_file_path_from_scribe_file():
    result = infer_unit_test_file_path_from_scribe_file(scribe_file_path=pathlib.Path("foo/bar/a.tscribe"))
    assert isinstance(result, pathlib.PosixPath)
    assert repr(result) == "PosixPath('foo/bar/test_a_g.py')"


def test_remove_file_if_no_test_has_test():
    file_path: pathlib.Path = create_autospec(spec=pathlib.Path)
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    result = remove_file_if_no_test(file_path=file_path, tests=[m_test_model])
    assert result is False
    file_path.assert_not_called()
    m_test_model.assert_not_called()


def test_remove_file_if_no_test_no_test_no_target_file():
    file_path: pathlib.Path = create_autospec(spec=pathlib.Path)
    file_path.exists.return_value = False
    result = remove_file_if_no_test(file_path=file_path, tests=[])
    assert result is True
    file_path_mock_calls = get_normalized_mock_calls(file_path, pathlib.Path)
    assert file_path_mock_calls == [
        call.exists(),
    ]


def test_remove_file_if_no_test_no_test_existing_file_is_deleted():
    file_path: pathlib.Path = create_autospec(spec=pathlib.Path)
    file_path.exists.return_value = True
    file_path.__str__.return_value = 'm'
    result = remove_file_if_no_test(file_path=file_path, tests=[])
    assert result is True
    file_path_mock_calls = get_normalized_mock_calls(file_path, pathlib.Path)
    assert file_path_mock_calls == [
        call.exists(),
        call.unlink(),
        call.__str__(),
    ]
