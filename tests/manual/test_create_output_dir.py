from testscribe.input_params import create_output_dir_for_module
from testscribe.module import Module


def test_create_output_dir_for_module(tmp_path):
    # See the generated test for comparison.
    # The generated test relies on mocks, this test actually create files and
    # directories.
    r = create_output_dir_for_module(
        output_root_dir=tmp_path, module=Module(["foo", "bar", "m"])
    )
    target_output_path = tmp_path.joinpath("foo", "bar")
    assert r == target_output_path
    # print(f"target output path: {target_output_path}")
    assert target_output_path.exists()
    # allow pytest to delete old temp directories automatically
    # see https://code-maven.com/temporary-files-and-directory-for-pytest
