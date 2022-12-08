import click.exceptions
import pytest
from wrapper.value_input_cli_wrapper import get_one_value_cli_wrapper_abort


def test_get_one_value_cli_wrapper_abort():
    with pytest.raises(click.exceptions.Abort) as exception_info:
        get_one_value_cli_wrapper_abort()
    assert str(exception_info.value) == ''
