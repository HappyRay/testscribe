from typing import Callable, Union, Optional
from unittest.mock import Mock

from test_scribe import mocking_support
from test_scribe.custom_type import Spec
from test_scribe.mock_proxy import MockProxy
from test_scribe.user_triggered_exception import UserTriggeredException


def throw(e: BaseException = Exception()):
    """
    Use this function in an input expression to cause a mock call to throw the
    given exception.
    :param e:
    :return:
    """
    return UserTriggeredException(exception=e)


def patch_with_mock(
    target: Union[str, type, Callable], mock_name: str = "", spec: Optional[Spec] = None
) -> None:
    mocking_support.patch_with_mock_internal(
        target=target, mock_name=mock_name, spec=spec
    )


def patch_with_expression(target_str: str, expression: str) -> None:
    mocking_support.patch_with_expression_internal(
        target_str=target_str, expression=expression
    )


def get_normalized_mock_calls(mock: Mock, spec: Spec) -> list:
    """
    Used in the generated unit test code to allow verifying mock calls consistently
    with keyword arguments when parameter names are available.

    :param mock:
    :param spec:
    :return:
    """
    return mocking_support.get_normalized_mock_calls_internal(mock=mock, spec=spec)


class TextFileSpec:
    """
    see https://docs.python.org/3/library/io.html#io.TextIOBase
    signature function can't get the signature from the TextIOBase class.
    """

    def write(self, content: str) -> int:
        pass

    def read(self, size=-1) -> str:
        pass

    def readline(self, size=-1) -> str:
        pass


class TextFileContextMgrSpec:
    def __enter__(self) -> TextFileSpec:
        pass

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        pass


# noinspection PyUnusedLocal
def text_open_spec(
    file,
    mode="r",
    buffering=-1,
    encoding=None,
    errors=None,
    newline=None,
    closefd=True,
    opener=None,
) -> TextFileContextMgrSpec:
    """
    Use as a spec for patching the builtin open function.

    The builtin open function doesn't provide return type annotation.
    See: https://docs.python.org/3/library/functions.html#open
    :param file:
    :param mode:
    :param buffering:
    :param encoding:
    :param errors:
    :param newline:
    :param closefd:
    :param opener:
    :return:
    """
    pass


def m(spec: Spec, name: str = ""):
    return MockProxy(spec=spec, name=name)
