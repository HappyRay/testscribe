import logging
from pathlib import Path

from testscribe.execution import save_file
from testscribe.execution_util import init
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


def delete_test(scribe_file_path: Path, test_name: str):
    init()
    log(f"Deleting the test {test_name} from {scribe_file_path}.")
    all_tests = load_scribe_file(scribe_file_path)
    # todo: if test_name is not specified, show a list of test names
    #  and allow users to choose one to delete
    delete_test_internal(
        scribe_file_path=scribe_file_path, test_name=test_name, all_tests=all_tests
    )
