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

from testscribe.input_params import create_output_dir_for_module
from testscribe.module import Module


def test_create_output_dir_for_module(tmp_path):
    # See the generated test for comparison.
    # The generated test relies on mocks, this test actually create files and
    # directories.
    r = create_output_dir_for_module(
        output_root_dir=tmp_path, module=Module(["foo", "bar", "m"])
    )
    target_output_path = tmp_path.joinpath("foo", "bar")
    assert r == target_output_path
    # print(f"target output path: {target_output_path}")
    assert target_output_path.exists()
    # allow pytest to delete old temp directories automatically
    # see https://code-maven.com/temporary-files-and-directory-for-pytest
