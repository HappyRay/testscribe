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
from typing import Optional

from testscribe.execution import save_file
from testscribe.execution_util import (
    init,
    get_all_scribe_files,
    infer_scribe_file_path,
)
from testscribe.load_scribe_file import load_scribe_file
from testscribe.log import log
from testscribe.model_type import AllTests
from testscribe.test_name import create_test_name

logger = logging.getLogger(__name__)


def regenerate_all_tests(config_file_path: Optional[Path]):
    config = init(config_file_path=config_file_path)
    regenerate_all_tests_internal(config.output_root_path)


def regenerate_all_tests_internal(output_root_path: Path):
    log(f"Regenerate all unit tests under {output_root_path}")
    total = 0
    for p in get_all_scribe_files(output_root_path):
        regenerate_tests(p)
        total += 1
    log(f"Regenerated {total} tests.")
    return total


def regenerate_tests(file_path: Path) -> None:
    init()
    scribe_file_path = infer_scribe_file_path(file_path)
    log(f"Regenerate unit tests from {scribe_file_path}")
    all_tests = load_scribe_file(scribe_file_path)
    regenerate_test_names(all_tests)
    save_file(scribe_file_path=scribe_file_path, all_tests=all_tests)


def regenerate_test_names(all_tests: AllTests):
    """
    Regenerate test names from the short names.
    Useful when the target function name changes, and it is used as a test prefix.
    :param all_tests:
    :return:
    """
    tests = all_tests.tests
    for i in range(len(tests) - 1, -1, -1):
        # Start from the last test to keep the test name stable
        # since older tests for the same target appear first.
        t = tests[i]
        t.name = create_test_name(
            all_tests=all_tests,
            index_of_test_to_update=i,
            short_name=t.short_name,
            target_func_name=t.target_func_name,
        )
