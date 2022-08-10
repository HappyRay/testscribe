import os
from pathlib import Path
from shutil import copy

from pytest import fixture

from conftest import assert_file_content_same
from fixture.helper import (
    TEST_DATA_MODULE_NAME,
    get_test_data_root_path,
    get_test_input_path,
    generate_create_cmd_args,
    run_cli,
)
from test_scribe.execution_util import create_unit_test_file_name

COPY_TEST_RESULT_ENV_VAR = "copy_test_result"


@fixture
def generated_data_path(tmp_path):
    p = tmp_path.joinpath(TEST_DATA_MODULE_NAME)
    p.mkdir()
    return p


@fixture()
def run_create_test_and_verify(
    tmp_path,
    verify_output_files,
):
    """
    Define this fixture function so that the other dependent fixtures don't have be
    requested by individual tests and passed to the helper function.
    """

    # Use partial function is easier to implement. However, IDE fails to infer
    # parameter information of the returned function.
    def _run_create_test_and_verify(
        file_name_only: str,
        function_name: str,
        test_input: str = "",
        expected_file_prefix="",
        config_file: str = "",
    ):
        test_file_name = file_name_only + ".py"
        test_file_path = get_test_data_root_path().joinpath(test_file_name)
        test_arguments = generate_create_cmd_args(
            test_file_name=str(test_file_path),
            test_func_name=function_name,
            output_root_dir=tmp_path,
            config_file=config_file,
        )
        out = run_cli(test_arguments=test_arguments, test_input=test_input)
        verify_output_files(
            file_name_only=file_name_only,
            expected_file_prefix=expected_file_prefix,
        )
        return out

    return _run_create_test_and_verify


def copy_file(src, dest):
    print(f"Copy file from {src} to {dest}")
    copy(src, dest)


@fixture
def verify_output_files(
    expected_test_data_path,
    generated_data_path,
):
    def _verify_output_files(
        file_name_only, expected_file_prefix="", do_not_copy_result=False
    ):
        scribe_file_name = file_name_only + ".tscribe"
        generated_scribe_file_path = generated_data_path.joinpath(scribe_file_name)
        prefix = f"{expected_file_prefix}_" if expected_file_prefix else ""
        expected_scribe_file_path = expected_test_data_path.joinpath(
            f"{prefix}{scribe_file_name}"
        )

        test_output_file_name = create_unit_test_file_name(file_name_only)
        generated_test_file_path = generated_data_path.joinpath(test_output_file_name)
        expected_test_file_path = expected_test_data_path.joinpath(
            f"{prefix}{test_output_file_name}"
        )

        if not do_not_copy_result and COPY_TEST_RESULT_ENV_VAR in os.environ:
            print(
                f"Environment varaible {COPY_TEST_RESULT_ENV_VAR} is detected."
                " Copy the result files."
            )
            copy_file(src=generated_scribe_file_path, dest=expected_scribe_file_path)
            copy_file(src=generated_test_file_path, dest=expected_test_file_path)
        else:
            assert_file_content_same(
                generated_scribe_file_path, expected_scribe_file_path
            )
            assert_file_content_same(generated_test_file_path, expected_test_file_path)

    return _verify_output_files


@fixture()
def copy_input_scribe_file(copy_input_file):
    def _copy_input_scribe_file(
        file_name_only: str, output_file_name: str = ""
    ) -> Path:
        if output_file_name:
            output_file_name = f"{output_file_name}.tscribe"
        return copy_input_file(
            file_name=f"{file_name_only}.tscribe", output_file_name=output_file_name
        )

    return _copy_input_scribe_file


@fixture()
def copy_input_file(generated_data_path):
    def _copy_input_file(file_name: str, output_file_name: str = "") -> Path:
        input_file = get_test_input_path().joinpath(f"{file_name}")
        if not output_file_name:
            output_file_name = file_name
        target_file_path = generated_data_path.joinpath(f"{output_file_name}")
        copy(input_file, target_file_path)
        return target_file_path

    return _copy_input_file


def test_simple_calculator_func(run_create_test_and_verify):
    """
    A simple end-to-end test.
    Also enables generating the result files to be used as input to other tests.
    """
    run_create_test_and_verify(
        file_name_only="calculator",
        function_name="add",
        test_input="1\n2\n\n\n",
    )


def test_end_to_end_cli(tmp_path, run_create_test_and_verify):
    run_create_test_and_verify(
        file_name_only="service_call",
        function_name="gen_name",
        test_input="m\na\n1\nb\n2\n3\nsimple gen\nintegration test",
    )


def test_end_to_end_cli_method(run_create_test_and_verify):
    run_create_test_and_verify(
        file_name_only="service",
        function_name="search_a_name",
        test_input="a\nb\n\n",
    )


def test_mock_property(run_create_test_and_verify):
    run_create_test_and_verify(
        file_name_only="property_access",
        function_name="get_car_year",
        test_input="m\n1\n\n\n",
    )


def test_mock_property_access_twice(run_create_test_and_verify):
    run_create_test_and_verify(
        file_name_only="property_access2",
        function_name="print_car_year_twice",
        test_input="m\n1\n\n\n",
    )


def test_mock_str_method(run_create_test_and_verify):
    run_create_test_and_verify(
        file_name_only="mock_str_method",
        function_name="print_simple_data_class",
        test_input="m\n\n\n\n",
    )


def test_mock_context_mgr(run_create_test_and_verify):
    run_create_test_and_verify(
        file_name_only="context_mgr",
        function_name="use_resource",
        test_input="m\nm\nm\nt\n\n\n",
    )


def test_class_input_output(run_create_test_and_verify):
    """
    Test an expression that instantiates a class and return a class
    """
    run_create_test_and_verify(
        file_name_only="echo",
        function_name="echo",
        test_input="test_data.simple.C(1)",
    )


def test_retry_invalid_input(run_create_test_and_verify):
    run_create_test_and_verify(
        file_name_only="echo",
        function_name="echo",
        test_input="a\ntest_data.simple.C(1)",
    )


def test_class_result(run_create_test_and_verify):
    """
    The result class modules should be imported correctly.
    """
    run_create_test_and_verify(
        file_name_only="return_class",
        function_name="create_fixed_product_owner",
    )


def test_callable(run_create_test_and_verify):
    """
    Callable as parameters and result.
    """
    run_create_test_and_verify(
        file_name_only="return_callable",
        function_name="echo_func",
        test_input="test_data.simple.foo",
    )


def test_mock_callable(run_create_test_and_verify):
    """
    Mock a Callable parameter.
    """
    run_create_test_and_verify(
        file_name_only="function_as_param", function_name="calc", test_input="1\nm\n3"
    )


def test_list_of_objects_result(run_create_test_and_verify):
    """
    The result class modules should be imported correctly.

    """
    run_create_test_and_verify(
        file_name_only="return_list_of_objects",
        function_name="create_person_list",
    )


def test_merge_tests(copy_input_scribe_file, run_create_test_and_verify):
    file_name_only = "calculator"
    copy_input_scribe_file(file_name_only=file_name_only)

    run_create_test_and_verify(
        file_name_only=file_name_only,
        function_name="add",
        test_input="3\n4\n\n",
        expected_file_prefix="merged",
    )


def test_patch(run_create_test_and_verify):
    run_create_test_and_verify(
        file_name_only="patch_function_for_integration_test_wrapper",
        function_name="foo_wrapper",
    )


def test_patch_with_setup(run_create_test_and_verify):
    run_create_test_and_verify(
        file_name_only="patch_function_for_integration_test",
        function_name="foo",
        config_file="test_data/test-patch-func-config.yml",
    )


def test_patch_in_method(run_create_test_and_verify):
    run_create_test_and_verify(
        file_name_only="patch_in_method",
        function_name="foo",
        test_input="1\n\n\n",
        config_file="test_data/test-patch-config.yml",
    )


def test_remove_duplicate_patches(run_create_test_and_verify):
    run_create_test_and_verify(
        file_name_only="duplicate_patch",
        function_name="duplicate_patches",
    )


def test_patch_with_expression(run_create_test_and_verify):
    run_create_test_and_verify(
        file_name_only="patch_dict",
        function_name="get_patched_dict",
    )


def test_exception_throwing_func(run_create_test_and_verify):
    run_create_test_and_verify(
        file_name_only="exception_in_func",
        function_name="exception_throwing_func",
        test_input="",
    )


def test_object_as_dict_key(run_create_test_and_verify):
    run_create_test_and_verify(
        file_name_only="object_as_dict_key",
        function_name="get_dict_with_object_key",
        test_input="",
    )


def test_delete_cmd(
    copy_input_scribe_file,
    verify_output_files,
):
    file_name_only = "calculator"
    test_scribe_file_path = copy_input_scribe_file(
        file_name_only="merged_calculator", output_file_name=file_name_only
    )
    test_arguments = ["delete", str(test_scribe_file_path), "test_add_1"]
    run_cli(test_arguments=test_arguments, test_input="")
    verify_output_files(
        file_name_only=file_name_only, expected_file_prefix="after_delete"
    )


def test_move_cmd(
    tmp_path,
    copy_input_file,
    verify_output_files,
    generated_data_path,
):
    simple_scribe_file = "simple.tscribe"
    simple_test_file = "test_simple_g.py"
    copy_input_file(file_name=simple_scribe_file)
    copy_input_file(file_name=simple_test_file)
    copy_input_file(file_name="service.tscribe")
    copy_input_file(file_name="test_service_g.py")
    source_file_path = get_test_data_root_path().joinpath("calculator.py")
    test_arguments = [
        "move",
        str(source_file_path),
        "add",
        "--output-root-dir",
        str(tmp_path),
    ]
    run_cli(test_arguments=test_arguments, test_input="")
    verify_output_files(file_name_only="calculator", do_not_copy_result=True)
    verify_output_files(file_name_only="service", do_not_copy_result=True)
    assert not generated_data_path.joinpath(simple_test_file).exists()
    assert not generated_data_path.joinpath(simple_scribe_file).exists()


def test_sync_cmd(
    copy_input_scribe_file,
    verify_output_files,
):
    file_name_only = "calculator"
    test_scribe_file_path = copy_input_scribe_file(file_name_only=file_name_only)

    test_arguments = ["sync", str(test_scribe_file_path)]
    run_cli(test_arguments=test_arguments, test_input="")
    verify_output_files(file_name_only=file_name_only, do_not_copy_result=True)


def test_sync_test_names(
    copy_input_scribe_file,
    verify_output_files,
):
    file_name_only = "modified_merged_calculator"
    output_file_name_only = "calculator"
    test_scribe_file_path = copy_input_scribe_file(
        file_name_only=file_name_only, output_file_name=output_file_name_only
    )

    test_arguments = ["sync", str(test_scribe_file_path)]
    run_cli(test_arguments=test_arguments, test_input="")
    verify_output_files(
        file_name_only=output_file_name_only,
        expected_file_prefix="merged",
        do_not_copy_result=True,
    )


def test_sync_all_cmd(
    tmp_path, generated_data_path, copy_input_scribe_file, verify_output_files
):
    file_name_only = "calculator"
    copy_input_scribe_file(file_name_only=file_name_only)

    test_arguments = [
        "sync-all",
        "--output-root-dir",
        str(generated_data_path),
    ]
    run_cli(test_arguments=test_arguments, test_input="")
    verify_output_files(file_name_only=file_name_only, do_not_copy_result=True)


def update_test_common(
    copy_input_scribe_file,
    verify_output_files,
    file_name_only,
    test_function_name,
    test_input,
):
    test_scribe_file_path = copy_input_scribe_file(file_name_only=file_name_only)
    test_arguments = ["update", str(test_scribe_file_path), test_function_name]
    # verify that the old test's value is taken as default by entering '\n'.
    out = run_cli(test_arguments=test_arguments, test_input=test_input)
    verify_output_files(
        file_name_only=file_name_only,
        expected_file_prefix="after_update",
    )
    return out


def test_update_cmd(copy_input_scribe_file, verify_output_files):
    file_name_only = "calculator"
    test_input = "\n\n\nnew\n"
    test_function_name = "test_add"
    update_test_common(
        copy_input_scribe_file,
        verify_output_files,
        file_name_only,
        test_function_name,
        test_input,
    )


def test_update_recreate_patch(copy_input_scribe_file, verify_output_files):
    file_name_only = "patch_function_for_integration_test"
    test_input = "\n\n\n"
    test_function_name = "test_foo"
    update_test_common(
        copy_input_scribe_file,
        verify_output_files,
        file_name_only,
        test_function_name,
        test_input,
    )


def test_update_cmd_patch_wrapper_not_create_duplicate_patches(
    copy_input_scribe_file, verify_output_files
):
    """
    Test the update cmd works with patches.

    :param copy_input_scribe_file:
    :param verify_output_files:
    :return:
    """
    file_name_only = "patch_function_for_integration_test_wrapper"
    test_input = "\n\nnew\n"
    test_function_name = "test_foo_wrapper"
    out = update_test_common(
        copy_input_scribe_file,
        verify_output_files,
        file_name_only,
        test_function_name,
        test_input,
    )
    assert (
        "Create patch with target "
        "( test_data.patch_function_for_integration_test.func_with_side_effect )"
        " replacement ( Mock( name: m_func_with_side_effect ) )? [True]:"
    ) in out
    assert (
        "Remove previous patch of the same target "
        "test_data.patch_function_for_integration_test.func_with_side_effect"
    ) in out


def test_use_last_test_for_default(
    copy_input_scribe_file,
    run_create_test_and_verify,
):
    file_name_only = "echo"
    copy_input_scribe_file(file_name_only=file_name_only)

    run_create_test_and_verify(
        file_name_only=file_name_only,
        function_name="echo",
        # verify that the old test's value is taken as default by entering '\n'.
        test_input="\n\nnew\n",
        expected_file_prefix="after_new_test",
    )


def test_mock_marker_in_expression(run_create_test_and_verify):
    run_create_test_and_verify(
        file_name_only="product",
        function_name="get_a_product_total",
        test_input="m\n[m, m]\n1\n2\n\n\n",
    )


def test_throw_exception_in_mock_call(run_create_test_and_verify):
    run_create_test_and_verify(
        file_name_only="greet_wrapper",
        function_name="greet_mock_greeter",
        test_input="m\na\nb\nthrow()\n\n\n",
    )


def test_ignore_single_mock_call_return_value(run_create_test_and_verify):
    run_create_test_and_verify(
        file_name_only="ignore_return",
        function_name="ignore_return",
        test_input="m\nignore\n\n\n",
    )


def test_ignore_some_mock_call_return_values(run_create_test_and_verify):
    run_create_test_and_verify(
        file_name_only="ignore_some_returns",
        function_name="ignore_some_returns",
        test_input="m\nignore\n2\n\n\n",
    )


def test_static_method(run_create_test_and_verify):
    run_create_test_and_verify(
        file_name_only="static_method",
        function_name="call_static_method",
        test_input="m\n2\n\n\n",
    )


def test_class_method(run_create_test_and_verify):
    run_create_test_and_verify(
        file_name_only="class_method",
        function_name="call_class_method",
        test_input="m\n2\n\n\n",
    )


def test_str_method(run_create_test_and_verify):
    out = run_create_test_and_verify(
        file_name_only="str_method",
        function_name="get_str",
        test_input="m\n\n\n\n",
    )

    assert "c's __str__ method is called" in out
    assert (
        "Please provide the value for the return value of type: (str) [mock m_c]:"
        in out
    )


def test_complex_mock_call(run_create_test_and_verify):
    run_create_test_and_verify(
        file_name_only="complex_mock_call",
        function_name="call_mock_service_with_object",
        test_input="m\n\n\n",
    )


def test_set(run_create_test_and_verify):
    run_create_test_and_verify(
        file_name_only="set_handling",
        function_name="echo_set",
        test_input="{2, 1}\n\n\n",
    )
