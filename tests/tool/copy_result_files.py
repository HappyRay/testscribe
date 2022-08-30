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

"""
Copy the result files to the end-to-end test result directory.
"""

import sys
from pathlib import Path
from shutil import copy2

from fixture.helper import get_test_result_path


def copy_files(source_path: Path, file_name_only: str):
    print(f"source dir: {source_path}. file name: {file_name_only}")
    dest_path = get_test_result_path()
    scribe_file = source_path.joinpath(f"{file_name_only}.tscribe")
    print(f"Copy {scribe_file} to {dest_path}")
    copy2(scribe_file, dest_path)
    test_file = source_path.joinpath(f"test_{file_name_only}.py")
    print(f"Copy {test_file} to {dest_path}")
    copy2(test_file, dest_path)


def main():
    arguments = sys.argv
    copy_files(source_path=Path(arguments[1]), file_name_only=arguments[2])


if __name__ == "__main__":
    main()
