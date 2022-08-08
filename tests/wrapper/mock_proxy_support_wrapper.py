from unittest.mock import patch

from fixture.helper import patch_g_mock_name_counter
from test_data.simple import D
from test_scribe.mock_proxy_support import (
    create_unique_mock_name,
    get_mock_attribute_value,
)


def create_mock_name_twice():
    patch_g_mock_name_counter()
    name1 = create_unique_mock_name("a")
    name2 = create_unique_mock_name("a")
    return name1, name2


def get_mock_attribute_value_wrapper():
    with patch("test_scribe.value_input_cli.prompt", autospec=True) as mock_prompt, patch(
        "test_scribe.mock_proxy_support.show_user_call_stack", autospec=True
    ) as mock_show_user_call_stack, patch(
        "test_scribe.mock_proxy_support.global_var.g_test_to_infer_default_inputs", None
    ):
        mock_prompt.return_value = "1"
        r = get_mock_attribute_value(attribute_name="a", mock_name="m", spec=D)
        mock_show_user_call_stack.assert_called_once()
        mock_prompt.assert_called_once_with(
            "Please provide the value for the a attribute of type: (any)",
            default="",
            type=str,
        )
        return r
