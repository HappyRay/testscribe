#  Copyright 2022 Ruiguo (Ray) Yang
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#

import logging
from pathlib import Path
from typing import Any, Union, Callable

from typer import prompt

from testscribe import global_var
from testscribe.config import Config
from testscribe.constant import INVALID_TEST_INDEX
from testscribe.execution import execute_and_generate, run_setup_func
from testscribe.execution_util import ERROR_RETURN_CODE, init, infer_scribe_file_path
from testscribe.input_params import create_input_params
from testscribe.load_scribe_file import load_scribe_file
from testscribe.log import log
from testscribe.mock_proxy import MockProxy
from testscribe.mocking_support import (
    patch_with_mock_internal,
    patch_with_expression_internal,
)
from testscribe.model_type import (
    AllTests,
    TestModel,
    PatchModel,
    MockNameModel,
    ExpressionModel,
    get_mock_by_name,
)
from testscribe.module import get_module_from_str, Module
from testscribe.reflection_util import get_symbol
from testscribe.util import remove_trailing_numbers

logger = logging.getLogger(__name__)


def update_test_cmd(
    file_path: Path,
    test_name: str,
) -> int:
    config = init()
    scribe_file_path = infer_scribe_file_path(file_path)
    log(f"Update the test {test_name} in {scribe_file_path}")
    all_tests = load_scribe_file(scribe_file_path)
    index = all_tests.get_test_index_by_name(test_name)
    logger.debug(f"Index of the test being updated: {index}")
    if index != INVALID_TEST_INDEX:
        update_test(
            index=index,
            all_tests=all_tests,
            scribe_file_path=scribe_file_path,
            config=config,
        )
        return 0
    else:
        log(
            f"The test ({test_name}) doesn't exist in the file "
            f"({scribe_file_path})."
        )
        return ERROR_RETURN_CODE


def update_test(
    index: int, all_tests: AllTests, scribe_file_path: Path, config: Config
):
    test = all_tests.tests[index]

    # Save to global variables to avoid passing this information via
    # many layers of calls which don't need this information.
    global_var.g_index_of_test_to_update = index
    module_name = all_tests.module
    log(f"Updating module ({module_name}).")
    module = get_module_from_str(module_name)
    output_root_dir = infer_output_root_dir_from_module(module, scribe_file_path)
    log(f"Output root directory: {output_root_dir}")
    create_patches_from_existing_test(all_tests.tests[index])
    # Patches defined in a setup function overrides the existing patches
    # thus they have to be called later.
    # todo: add a test
    run_setup_func(config.setup_function)
    # Unlike the create command, update cmd indicates that the scribe file
    # is likely to be maintained. In such a case, a meaningful name and
    # description become more useful.
    # It's likely that the test name and descriptions may need updating.
    input_params = create_input_params(
        module=module,
        function_name=test.target_func_name,
        output_root_dir=output_root_dir,
        ask_for_test_name=True,
        ask_for_description=True,
    )
    execute_and_generate(
        input_params=input_params, all_tests=all_tests, index_of_test_to_update=index
    )


def infer_output_root_dir_from_module(module: Module, scribe_file_path: Path) -> Path:
    """

    :param module: the module the scribe file is targeting.
    :param scribe_file_path:
    :return: the output root path
    """
    package_depth = len(module.get_package_name_list())
    return scribe_file_path.parents[package_depth]


def create_patches_from_existing_test(test: TestModel):
    if test.patches:
        log("Recreating patches from the existing test.")
        for p in test.patches:
            create_patcher_from_model(patch_model=p, test=test)


def create_patcher_from_model(patch_model: PatchModel, test: TestModel) -> bool:
    if should_recreate_patch(patch_model):
        really_create_patcher_from_model(patch_model=patch_model, test=test)
        return True
    else:
        log(f"Skipped the patch for {patch_model.target}.")
        return False


def should_recreate_patch(patch_model: PatchModel) -> bool:
    prompt_str = (
        f"Create patch with target ( {patch_model.target} )"
        f" replacement ( {patch_model.replacement} )?"
    )
    # noinspection PyTypeChecker
    # the default value should be a bool here not a string
    return prompt(prompt_str, default=True, type=bool)


def really_create_patcher_from_model(patch_model: PatchModel, test: TestModel) -> None:
    value = patch_model.replacement
    if isinstance(value, MockNameModel):
        create_mock_patcher_from_model(
            mock_name=value.name, target=patch_model.target, test=test
        )
    else:
        patch_with_expression_internal(
            target_str=patch_model.target, expression=get_expression_str(value)
        )


def create_mock_patcher_from_model(
    mock_name: str, target: Union[str, type, Callable, MockProxy], test: TestModel
):
    mock = get_mock_by_name(mocks=test.mocks, name=mock_name)
    spec = get_symbol(mock.spec_str)
    normalized_name = remove_trailing_numbers(mock_name)
    patch_with_mock_internal(target=target, mock_name=normalized_name, spec=spec)


def get_expression_str(value: Any) -> str:
    if isinstance(value, ExpressionModel):
        return value.expression
    return repr(value)
