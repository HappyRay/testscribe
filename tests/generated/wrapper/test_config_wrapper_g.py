from unittest.mock import patch
from wrapper.config_wrapper import initialize_io_wrapper


def test_initialize_io_wrapper():
    with patch('testscribe.global_var.g_io', None):
        result = initialize_io_wrapper()
    assert result is None
