import pathlib
import setup
import test_scribe.config
from wrapper.init_wrapper import add_additional_python_paths_no_key, init_config_wrapper


def test_add_additional_python_paths_no_key():
    result = add_additional_python_paths_no_key()
    assert result is None


def test_init_config_wrapper():
    result = init_config_wrapper()
    assert isinstance(result, test_scribe.config.Config)
    assert isinstance(result.output_root_path, pathlib.PosixPath)
    assert repr(result.output_root_path) == "PosixPath('tests/generated')"
    assert result.setup_function == setup.setup
