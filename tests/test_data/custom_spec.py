"""
The custom specs are provided as a convenience when python reflection doesn't provide
enough type information.
"""


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
