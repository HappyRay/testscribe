import tempfile

from fixture.helper import (
    get_test_data_root_path,
    remove_project_root_directory_prefix,
    generate_create_cmd_args,
    run_cli,
)


def mock_property_output():
    return get_cli_output(
        file_name_only="property_access",
        func_name="get_car_year",
        test_input="m\n1\n\n\n",
    )


def function_call_output():
    return get_cli_output(
        file_name_only="service_call",
        func_name="gen_name",
        test_input="m\na\n1\nb\n2\n3\nsimple gen\nintegration test",
    )


def method_call_output():
    return get_cli_output(
        file_name_only="service",
        func_name="search_a_name",
        test_input="a\nb\n\n",
    )


def retry_invalid_input_output():
    return get_cli_output(
        file_name_only="echo",
        func_name="echo",
        test_input="a\ntest_data.simple.C(1)",
    )


def get_cli_output(file_name_only: str, func_name: str, test_input: str) -> str:
    test_file_path = get_test_data_root_path().joinpath(f"{file_name_only}.py")
    with tempfile.TemporaryDirectory() as output_dir:
        test_arguments = generate_create_cmd_args(
            test_file_name=str(test_file_path),
            test_func_name=func_name,
            output_root_dir=output_dir,
        )
        out = run_cli(
            test_arguments=test_arguments,
            test_input=test_input,
        )
        # Remove the directory names that depend on the test environment.
        return remove_project_root_directory_prefix(out).replace(output_dir, "")
