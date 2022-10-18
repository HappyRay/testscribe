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

from testscribe.execution import save_file
from testscribe.execution_util import init, infer_scribe_file_path
from testscribe.load_scribe_file import load_scribe_file
from testscribe.log import log
from testscribe.model_type import delete_test_by_name, AllTests

logger = logging.getLogger(__name__)


def delete_test_internal(scribe_file_path: Path, test_name: str, all_tests: AllTests):
    if all_tests.does_test_exist(test_name):
        new_all_tests = delete_test_by_name(all_tests=all_tests, name=test_name)
        save_file(scribe_file_path=scribe_file_path, all_tests=new_all_tests)
    else:
        log(f"The test name ({test_name}) doesn't exist")
        return


def delete_test(file_path: Path, test_name: str):
    init()
    scribe_file_path = infer_scribe_file_path(file_path)
    log(f"Deleting the test {test_name} from {scribe_file_path}.")
    all_tests = load_scribe_file(scribe_file_path)
    # todo: if test_name is not specified, show a list of test names
    #  and allow users to choose one to delete
    delete_test_internal(
        scribe_file_path=scribe_file_path, test_name=test_name, all_tests=all_tests
    )
