from inspect import Parameter
from pathlib import Path
from typing import Any, List

from testscribe.context import Context
from testscribe.namedvalues import NamedValues


class IOProvider:
    """
    The input and output plugin module implementations need to support these methods.
    """

    def __init__(self):
        pass

    def end(self, scribe_file_path: Path):
        pass

    def log(self, s: str) -> None:
        raise NotImplementedError()

    def get_parameter_value(
        self, param_info_list: List[Parameter], defaults: list, context: Context
    ) -> NamedValues:
        """

        :param param_info_list: the list should not be empty, the no parameter case
        should have been handled by the caller.
        :param defaults: corresponding default values for the parameters
        :param context:
        :return:
        """
        raise NotImplementedError()

    def get_one_value(
        self, prompt_name: str, name: str, t: type, default: Any, context: Context
    ) -> Any:
        raise NotImplementedError()

    def get_test_description(self, default: str) -> str:
        raise NotImplementedError()

    def get_short_test_name(self, default_short_name: str) -> str:
        raise NotImplementedError()
