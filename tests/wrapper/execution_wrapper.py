from typing import Callable, Any
from unittest.mock import patch

from test_data.greet import Greeter
from testscribe.execution import get_args_and_call, create_instance
from testscribe.namedvalues import NamedValues


def get_args_and_call_wrapper(func: Callable) -> Any:
    # Using the tool to patch prompt prevents the tool from getting the return value.
    with patch("testscribe.value_input_cli.prompt", autospec=True) as mock_prompt:
        mock_prompt.return_value = '"b"'
        return get_args_and_call(func=func, default=NamedValues())


def create_instance_wrapper():
    # Using the tool to patch prompt prevents the tool from getting the return value.
    with patch("testscribe.value_input_cli.prompt", autospec=True) as mock_prompt:
        mock_prompt.return_value = "a"
        r = create_instance(clazz=Greeter, test_to_infer_default_inputs=None)
        mock_prompt.assert_called_once_with(
            "Please provide the value for the parameter (my_name) of type: (str)",
            default="",
            type=str,
        )
        return r
