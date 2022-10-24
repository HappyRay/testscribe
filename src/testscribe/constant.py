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

INVALID_TEST_INDEX = -1
GET_TEST_NAME_PROMPT = (
    "Test name help: 'test_' prefix will be added automatically. "
    "Use a leading '_' to include the target function name as "
    "part of the prefix.\n"
    "Test name:"
)
SCRIBE_FILE_SUFFIX = ".tscribe"
DEFAULT_OUTPUT_ROOT_DIR_NAME = "test_scribe_tests"
