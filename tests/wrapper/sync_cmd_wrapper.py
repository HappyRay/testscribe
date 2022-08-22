from testscribe.model_type import AllTests
from testscribe.sync_cmd import regenerate_test_names


def get_regenerated_test_names(all_tests: AllTests):
    regenerate_test_names(all_tests=all_tests)
    return [t.name for t in all_tests.tests]
