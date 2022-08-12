from inspect import Parameter
from typing import Any, List

from test_scribe import global_var
from test_scribe.api.io_provider import IOProvider
from test_scribe.api.mock_api import patch_with_expression
from test_scribe.config import initialize_io
from test_scribe.context import Context
from test_scribe.namedvalues import NamedValues


class TestIo(IOProvider):

    def log(self, s: str) -> None:
        pass

    def get_parameter_value(self, param_info_list: List[Parameter], defaults: list, context: Context) -> NamedValues:
        pass

    def get_one_value(self, prompt_name: str, name: str, t: type, default: Any, context: Context) -> Any:
        pass

    def get_test_description(self, default: str) -> str:
        pass

    def get_short_test_name(self, default_short_name: str) -> str:
        pass


def initialize_io_wrapper():
    # patch the global g_io so that it is restored after the test
    patch_with_expression(target_str="test_scribe.global_var.g_io", expression="None")
    initialize_io({"io-provider-full-class-name": "wrapper.config_wrapper.TestIo"})
    assert isinstance(global_var.g_io, TestIo)
