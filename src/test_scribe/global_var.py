from __future__ import annotations

from collections import Counter

# io provider
from test_scribe.api.io_provider import IOProvider
from test_scribe.cli import CLI

g_io: IOProvider = CLI()

# No type hints to avoid circular dependency

# target string as key, Patcher object as value
g_patchers = {}

# set to True during the test generation process
g_test_generating_mode = False

g_test_to_infer_default_inputs = None
g_index_of_test_to_update = -1


def get_initial_mock_name_counter():
    # Make sure there is no mock object named "m" which conflicts with
    # the function m.
    return Counter("m")


# How many times a mock name is shared among mocks
g_mock_name_counter = get_initial_mock_name_counter()
# Mock name to MockProxy instance mapping
g_name_mock_dict = {}
