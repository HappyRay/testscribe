import fixture.helper
import pathlib
from wrapper.execution_util_wrapper import get_all_scribe_files_wrapper


def test_get_all_scribe_files_wrapper():
    result = get_all_scribe_files_wrapper(root_path=fixture.helper.get_test_data_root_path() / "file_test_data")
    assert isinstance(result, list)
    assert len(result) == 3
    assert isinstance(result[0], pathlib.PosixPath)
    assert repr(result[0]) == "PosixPath('a.tscribe')"
    assert isinstance(result[1], pathlib.PosixPath)
    assert repr(result[1]) == "PosixPath('b.tscribe')"
    assert isinstance(result[2], pathlib.PosixPath)
    assert repr(result[2]) == "PosixPath('sub/sub_a.tscribe')"
