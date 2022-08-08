import logging
from typing import List

from test_scribe.code_gen_util import join_lines
from test_scribe.gather_referenced_modules import (
    gather_import_statements_for_referenced_modules,
)
from test_scribe.model_type import (
    TestModel,
    AllTests,
)

logger = logging.getLogger(__name__)


def need_mock_support(tests: List[TestModel]) -> bool:
    for t in tests:
        if t.mocks:
            return True
    return False


def gather_import_statements_for_mock_support(tests: List[TestModel]) -> List[str]:
    if need_mock_support(tests):
        # todo: only import when there is call verifications
        return [
            "from test_scribe.api.mock_api import get_normalized_mock_calls",
            "from unittest.mock import ANY, call, create_autospec",
        ]
    else:
        return []


def gather_import_statement_for_patch_support(tests: List[TestModel]) -> str:
    for t in tests:
        if t.patches:
            return "from unittest.mock import patch"
    return ""


def need_exception_support(tests: List[TestModel]) -> bool:
    for t in tests:
        if t.exception:
            return True
    return False


def gather_import_statement_for_exception_support(tests: List[TestModel]) -> str:
    if need_exception_support(tests):
        return "import pytest"
    else:
        return ""


def get_target_for_a_test(t: TestModel):
    target_class_name = t.target_class_name
    if target_class_name:
        # todo: handle nested classes
        target_name = target_class_name
    else:
        target_name = t.target_func_name
    return target_name


def gather_import_statements_for_test_targets(all_tests: AllTests) -> str:
    targets = {get_target_for_a_test(t) for t in all_tests.tests}
    target_str = ", ".join(sorted(targets))
    return f"from {all_tests.module} import {target_str}"


def generate_import_statement_str(all_tests: AllTests) -> str:
    statements = []
    tests = all_tests.tests
    statements.extend(gather_import_statements_for_referenced_modules(tests))
    statements.extend(gather_import_statements_for_mock_support(tests))
    statements.append(gather_import_statement_for_patch_support(tests))
    statements.append(gather_import_statement_for_exception_support(tests))
    statements.append(gather_import_statements_for_test_targets(all_tests))
    result = join_lines(statements, prepend_new_line=False) + "\n"
    return result
