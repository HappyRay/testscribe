"""
Copy the files used for test inputs from the result directory
to the input directory.
"""
from shutil import copy2

from fixture.helper import get_test_result_path, get_test_input_path
from testscribe.load_scribe_file import load_scribe_file
from testscribe.save_scribe_file import generate_scribe_file


def main():
    scribe_file_only_list = [
        "calculator",
        "echo",
        "merged_calculator",
        "patch_function_for_integration_test_wrapper",
        # This generated tscribe file is the source file for
        # testing updating a test will recreate patches.
        # A wrapper function like foo_wrapper will interfere by
        # creating a patch in the wrapper function.
        "patch_function_for_integration_test",
    ]
    both_files_list = [
        "service",
    ]
    for name in scribe_file_only_list:
        copy_scribe_file(file_name_only=name, copy_test_file=False)
    for name in both_files_list:
        copy_scribe_file(file_name_only=name, copy_test_file=True)

    create_simple_tscribe_file()
    create_modified_merged_calculator_file()


def copy_scribe_file(file_name_only: str, copy_test_file: bool):
    copy_file(f"{file_name_only}.tscribe")
    if copy_test_file:
        copy_file(f"test_{file_name_only}_g.py")


def copy_file(file_name: str):
    print(f"Copy {file_name}")
    dest_dir = get_test_input_path()
    source = get_test_result_path().joinpath(file_name)
    copy2(source, dest_dir)
    print(f"Copied {source} to {dest_dir}")


def create_simple_tscribe_file():
    """
    This generated tscribe file is the source file for testing moving a test.
    This simulates the situation when the add function was defined in
    the simple module.
    """
    print("Creating the simple.tscribe file.")
    all_tests = load_scribe_file(get_test_result_path().joinpath("calculator.tscribe"))
    all_tests.module = "test_data.simple"
    generate_scribe_file(
        scribe_file_path=get_test_input_path().joinpath("simple.tscribe"),
        all_tests=all_tests,
    )


def create_modified_merged_calculator_file():
    print("Creating the modified_merged_calculator.tscribe file.")
    all_tests = load_scribe_file(
        get_test_result_path().joinpath("merged_calculator.tscribe")
    )
    tests = all_tests.tests
    # Simulate the situation when the target function used to be called old
    # and the new name is now add and the target function name has been updated
    # probably via a search and replace.
    tests[0].name = "test_old_1"
    tests[1].name = "test_old"

    generate_scribe_file(
        scribe_file_path=get_test_input_path().joinpath(
            "modified_merged_calculator.tscribe"
        ),
        all_tests=all_tests,
    )


if __name__ == "__main__":
    main()
