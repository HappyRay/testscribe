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

from __future__ import annotations

from collections import Counter

# io provider
from testscribe.api.io_provider import IOProvider
from testscribe.cli import CLI

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
