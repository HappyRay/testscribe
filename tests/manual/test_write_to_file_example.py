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
from unittest.mock import patch, mock_open

from test_data.write_to_file_example import write_to_file_example


# Demonstrate how to manually mock file open operations


@patch("test_data.write_to_file_example.open", new_callable=mock_open)
def test_write_to_file(m):
    write_to_file_example("hello", Path("write_to_file_test.txt"))
    m.assert_called_once_with(Path("write_to_file_test.txt"), "w")
    handle = m()
    handle.write.assert_called_once_with("hello")


@patch("test_data.write_to_file_example.open")
def test_write_to_file_without_mock_open(m):
    write_to_file_example("hello", Path("write_to_file_test.txt"))
    m.assert_called_once_with(Path("write_to_file_test.txt"), "w")
    handle = m().__enter__()
    handle.write.assert_called_once_with("hello")
