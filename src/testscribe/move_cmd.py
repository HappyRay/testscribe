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
from inspect import isfunction, isclass
from pathlib import Path
from typing import List, Optional, Tuple

from testscribe.config import Config
from testscribe.constant import INVALID_TEST_INDEX
from testscribe.error import Error
from testscribe.execution import save_file
from testscribe.execution_util import (
    init,
    get_all_scribe_files,
)
from testscribe.file_info import get_module
from testscribe.input_params import (
    get_scribe_file_path,
)
from testscribe.load_scribe_file import load_scribe_file, load_or_create_model
from testscribe.log import log
from testscribe.model_type import TestModel, AllTests, add_test
from testscribe.module import Module
from testscribe.test_name import create_test_name
from testscribe.util import load_object

logger = logging.getLogger(__name__)


def move_tests(
    source_file: Path, class_or_function_name: str, config_file_path: Optional[Path]
):
    """

    :param source_file: the source file that the symbol currently is defined
    :param class_or_function_name: the class or function to move
    :param config_file_path:
    :return:
    """
    config = init(config_file_path=config_file_path)
    log(f"Move tests that target {class_or_function_name} of {source_file}.")
    module = get_module(target_file=source_file)
    module_str = module.get_module_str()
    log(f"Target module: {module_str}")
    tests_to_move = get_tests_to_move(
        class_or_function_name=class_or_function_name,
        output_root_path=config.output_root_path,
        module_str=module_str,
    )
    do_move(
        module=module,
        output_root_path=config.output_root_path,
        tests_to_move=tests_to_move,
    )


def do_move(module: Module, output_root_path: Path, tests_to_move: List[TestModel]):
    if tests_to_move:
        add_tests(
            output_root_path=output_root_path,
            module=module,
            tests_to_move=tests_to_move,
        )
        return True
    else:
        log("Can't find an existing test targetting this function or class.")
        return False


def get_output_root_path(config: Config, cmd_line_root_path: Optional[Path]) -> Path:
    if cmd_line_root_path:
        log(f"Output root directory cmd line option: {cmd_line_root_path}")
        return cmd_line_root_path
    else:
        return config.output_root_path


def get_tests_to_move(
    class_or_function_name: str, output_root_path: Path, module_str: str
) -> List[TestModel]:
    target_is_class = is_class_name(
        module_str=module_str, class_or_function_name=class_or_function_name
    )
    tests_to_move: List[TestModel] = []
    all_scribe_files = list(get_all_scribe_files(output_root_path))
    log(f"Searching {len(all_scribe_files)} of existing scribe files.")
    logger.debug(f"All scribe files: {all_scribe_files}")

    for scribe_file in all_scribe_files:
        tests = get_tests_to_move_from_one_file(
            class_or_function_name, target_is_class, scribe_file, module_str
        )
        tests_to_move.extend(tests)
    logger.info(f"Found total of {len(tests_to_move)} tests to move.")
    return tests_to_move


def is_class_name(module_str: str, class_or_function_name: str):
    obj = load_object(symbol_name=class_or_function_name, module_str=module_str)
    if isfunction(obj):
        log(f"Target function: {class_or_function_name}")
        return False
    if isclass(obj):
        log(f"Target class: {class_or_function_name}")
        return True
    raise Error(
        f"{class_or_function_name} is not a valid function or class in the module {module_str}"
    )


def get_tests_to_move_from_one_file(
    class_or_function_name: str,
    target_is_class: bool,
    scribe_file: Path,
    target_module_str: str,
) -> List[TestModel]:
    """
    Retrive the existing tests from a given scribe file that need to move.
    If found, it will remove these tests from the existing scribe file.

    If there is an exception when saving the new scribe file, these tests will be
    lost. It's highly suggsted to use a version control system to safeguard against
    such a possibility.

    :param class_or_function_name: the symbol to move
    :param target_is_class: is the target symbol a class name
    :param scribe_file: the scribe file to check
    :param target_module_str: the module to which the symbol now belongs
    :return:
    """
    logger.debug(f"Searching {scribe_file}")
    all_tests = load_scribe_file(scribe_file)
    if should_skip_module(
        module_str=all_tests.module,
        class_or_function_name=class_or_function_name,
        scribe_file=scribe_file,
        target_is_class=target_is_class,
        target_module_str=target_module_str,
    ):
        return []

    tests = all_tests.tests
    remaining_tests, tests_to_move = search_tests_to_remove(
        class_or_function_name=class_or_function_name,
        target_is_class=target_is_class,
        tests=tests,
    )
    if not tests_to_move:
        return []
    log(f"Found {len(tests_to_move)} tests to be moved in {scribe_file}.")
    all_tests.tests = remaining_tests
    # In the rare case when the tests to move fail to save, the information about
    # the existing tests are lost.
    # It's thus highly suggested that the generated scribe files are kept under source
    # control if users want to maintain them.
    save_file(scribe_file, all_tests)
    return tests_to_move


def should_skip_module(
    module_str: str,
    class_or_function_name: str,
    scribe_file: Path,
    target_is_class: bool,
    target_module_str: str,
) -> bool:
    if module_str == target_module_str:
        return True
    if module_contain_same_symbol(
        module_str=module_str,
        name=class_or_function_name,
        is_class=target_is_class,
        target_module_str=target_module_str,
    ):
        log(f"{scribe_file} contains a valid target that has the same name. Skip")
        return True
    return False


def module_contain_same_symbol(
    module_str: str, name: str, is_class: bool, target_module_str: str
) -> bool:
    """
    Return true if the module contains the same symbol name.
    :param module_str: the module to check
    :param name:
    :param is_class: is the name a class name
    :param target_module_str: the module to which the module belong
    :return:
    """
    obj = load_object(symbol_name=name, module_str=module_str)
    if obj is None or obj.__module__ == target_module_str:
        # If the same symbol is imported, it will exist as an attribute of this module.
        # However, the object's __module__ still points to the module where the
        # symbol is defined.
        return False
    if is_class:
        return isclass(obj)
    else:
        return isfunction(obj)


def search_tests_to_remove(
    class_or_function_name: str, target_is_class: bool, tests: List[TestModel]
) -> Tuple[List[TestModel], List[TestModel]]:
    tests_to_move: List[TestModel] = []
    remaining_tests: List[TestModel] = []
    for t in tests:
        if does_test_match_target_name(
            test=t,
            class_or_function_name=class_or_function_name,
            target_is_class=target_is_class,
        ):
            tests_to_move.append(t)
        else:
            remaining_tests.append(t)
    return remaining_tests, tests_to_move


def does_test_match_target_name(
    test: TestModel, class_or_function_name: str, target_is_class: bool
):
    source = get_name_to_compare_with(target_is_class=target_is_class, test=test)
    return source == class_or_function_name


def get_name_to_compare_with(target_is_class: bool, test: TestModel) -> str:
    return test.target_class_name if target_is_class else test.target_func_name


def add_tests(output_root_path: Path, module: Module, tests_to_move: List[TestModel]):
    target_scribe_file_path = get_scribe_file_path(
        output_root_dir=output_root_path, module=module
    )
    log(f"Target scribe file: {target_scribe_file_path}")
    all_tests = load_or_create_model(
        file_path=target_scribe_file_path, full_module_name=module.get_module_str()
    )
    for t in tests_to_move:
        all_tests = add_one_test(all_tests, t)
    save_file(target_scribe_file_path, all_tests)


def add_one_test(all_tests: AllTests, test: TestModel) -> AllTests:
    log(f"Moving test: {test.name}")
    test.name = create_test_name(
        all_tests=all_tests,
        index_of_test_to_update=INVALID_TEST_INDEX,
        short_name=test.short_name,
        target_func_name=test.target_func_name,
    )
    return add_test(all_tests=all_tests, test=test)
