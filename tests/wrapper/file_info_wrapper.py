from pathlib import Path

from testscribe.file_info import get_module


def get_module_wrapper(test_file_name: str):
    """
    Creating this wrapper makes auto test genration data input easier.
    See generated.testscribe.test_file_info.test_get_module_0 for
    an altertive way to generate a test without such a wrapper.
    :param test_file_name:
    :return:
    """
    test_file_path = Path(test_file_name).absolute()
    return get_module(test_file_path)
