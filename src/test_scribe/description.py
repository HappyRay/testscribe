from __future__ import annotations

from test_scribe import global_var
from test_scribe.model_type import AllTests


def get_test_description(
    all_tests: AllTests, index_of_test_to_update: int, ask_for_description: bool
) -> str:
    default_test_description = get_default_description(
        all_tests=all_tests, index_of_test_to_update=index_of_test_to_update
    )
    if ask_for_description:
        return global_var.g_io.get_test_description(default_test_description)
    else:
        return default_test_description


def get_default_description(all_tests: AllTests, index_of_test_to_update: int):
    if index_of_test_to_update >= 0:
        return all_tests.tests[index_of_test_to_update].description
    else:
        return ""
