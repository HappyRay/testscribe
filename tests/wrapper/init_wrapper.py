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

import sys
from pathlib import Path

from conftest import assert_same
from fixture.helper import get_project_root_path
from testscribe.config import init_config, add_additional_python_paths


def convert_to_absolute_path_str(s: str) -> str:
    return str(Path(s).absolute())


def init_config_wrapper():
    """
    Test the Python path is updated.

    :return:
    """
    # make a copy
    old_sys_path = list(sys.path)
    project_root_path = get_project_root_path()
    config = init_config(
        config_file_path=project_root_path / "test-scribe-config.yml"
    )
    # The sys.path may contain absolute paths and paths that depend on
    # the environment in which it runs. So it doesn't work to return
    # the new sys.path to have the assertions generated.
    expected_additional_path_strs = [str(project_root_path / "tests"), str(project_root_path)]
    assert_same(actual=sys.path, expected=old_sys_path + expected_additional_path_strs)
    # The output root path contains the path to the project root path.
    # The tool can't generate the correct assertion automatically.
    assert_same(actual=config.output_root_path, expected=project_root_path.joinpath("tests/generated"))
    return config.setup_function


def add_additional_python_paths_no_key() -> None:
    # make a copy first
    old_sys_path = list(sys.path)
    add_additional_python_paths(config_file_path=Path(), data={})
    current = sorted(sys.path)
    expected = sorted(old_sys_path + ["."])
    assert_same(actual=current, expected=expected)
