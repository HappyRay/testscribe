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

from pathlib import Path

from testscribe.file_info import get_module


def get_module_wrapper(test_file_name: str):
    """
    Creating this wrapper makes auto test genration data input easier.
    See generated.testscribe.test_file_info.test_get_module_0 for
    an altertive way to generate a test without such a wrapper.
    :param test_file_name:
    :return:
    """
    test_file_path = Path(test_file_name).absolute()
    return get_module(test_file_path)
