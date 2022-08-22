from collections import Counter
from pathlib import Path
from typing import List
from unittest.mock import patch

from typer.testing import CliRunner

from testscribe import global_var
from testscribe.__main__ import app
from testscribe.api.mock_api import patch_with_expression
from testscribe.custom_type import Spec
from testscribe.global_var import get_initial_mock_name_counter
from testscribe.mock_proxy import MockProxy

TEST_DATA_MODULE_NAME = "test_data"


def get_absolute_path(file_path_str: str) -> Path:
    return Path(file_path_str).absolute()


def get_test_root_path():
    return Path(__file__).parent.parent


def get_test_data_root_path():
    return get_test_root_path().joinpath(TEST_DATA_MODULE_NAME)


def get_test_result_path():
    return get_test_data_root_path().joinpath("result")


def get_test_input_path():
    return get_test_data_root_path().joinpath("input")


def get_project_root_path():
    return get_test_root_path().parent


def patch_g_mock_name_counter():
    patch_with_expression(
        target_str="testscribe.global_var.g_mock_name_counter",
        expression="collections.Counter(testscribe.global_var.g_mock_name_counter)",
    )


def patch_g_name_mock_dict():
    patch_with_expression(
        target_str="testscribe.global_var.g_name_mock_dict",
        expression="{}",
    )


def patch_globals_modified_by_mock_proxy():
    """
    Generate test code that
    restores the global variables after the test so that they don't affect
    the end-to-end tests.
    """
    patch_g_mock_name_counter()
    patch_g_name_mock_dict()


def create_mock_proxy(spec: Spec, name: str = "") -> MockProxy:
    """
    Use it for manual tests that need to create MockProxys directly.
    Restore the global variables affected by the MockProxy before returning
    so that they don't affect other tests.
    It means the callers need to make sure the names are unique.
    """
    with patch(
        target="testscribe.global_var.g_mock_name_counter",
        new=Counter(global_var.g_mock_name_counter),
    ), patch(target="testscribe.global_var.g_name_mock_dict", new={}):
        return MockProxy(spec=spec, name=name)


def remove_project_root_directory_prefix(s: str) -> str:
    root_dir = str(get_project_root_path().absolute()) + "/"
    return s.replace(root_dir, "")


def reset_global_variables():
    global_var.g_name_mock_dict.clear()
    global_var.g_patchers.clear()
    global_var.g_test_to_infer_default_inputs = None
    global_var.g_index_of_test_to_update = -1
    global_var.g_test_generating_mode = False
    global_var.g_mock_name_counter = get_initial_mock_name_counter()


def generate_create_cmd_args(
    test_file_name: str,
    test_func_name: str,
    output_root_dir: Path,
    config_file: str = "",
) -> List[str]:
    args = [
        "create",
        test_file_name,
        test_func_name,
        "--output-root-dir",
        str(output_root_dir),
    ]
    if not config_file:
        config_file = str(get_project_root_path().joinpath("test-scribe-config.yml"))
    args.extend(["--config-file", config_file])
    return args


def run_cli(test_arguments: List[str], test_input: str) -> str:
    reset_global_variables()
    try:
        return run_cli_internal(test_arguments=test_arguments, test_input=test_input)
    finally:
        reset_global_variables()


def run_cli_internal(test_arguments: List[str], test_input: str) -> str:
    runner = CliRunner()
    result = runner.invoke(app, test_arguments, input=test_input)
    out = result.stdout
    print("Test run output:")
    print(out)
    if result.exception:
        print(f"Exception: {result.exception}")
    assert result.exit_code == 0
    return out
