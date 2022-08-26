from unittest.mock import patch, create_autospec

from click import prompt
from click.exceptions import Abort
from testscribe.value_input_cli import get_one_value_cli


def get_one_value_cli_wrapper_abort():
    """
    Simulate users type ctrl-c to abort the program
    The patch interferes with the tool itself. Thus, it has to use a wrapper.
    """
    m_prompt = create_autospec(prompt, side_effect=Abort())
    with patch("testscribe.value_input_cli.prompt", m_prompt):
        get_one_value_cli(prompt_name="p", t=str, default="d")
