import setup
from wrapper.init_wrapper import add_additional_python_paths_no_key, init_config_wrapper


def test_add_additional_python_paths_no_key():
    result = add_additional_python_paths_no_key()
    assert result is None


def test_init_config_wrapper():
    result = init_config_wrapper()
    assert result == setup.setup
