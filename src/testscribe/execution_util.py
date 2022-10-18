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

from logging import getLogger, basicConfig
from logging.config import fileConfig
from pathlib import Path
from re import match
from traceback import extract_stack, format_list
from typing import List, Optional

from testscribe.config import init_config, CONFIG_FILE_NAME, Config
from testscribe.constant import SCRIBE_FILE_SUFFIX
from testscribe.error import Error
from testscribe.log import log
from testscribe.model_type import TestModel

logger = getLogger(__name__)

LOGGING_CONFIG_FILE_NAME = "test_scribe_logging.conf"
ERROR_RETURN_CODE = 1


def remove_file_if_no_test(file_path: Path, tests: List[TestModel]) -> bool:
    """
    Make sure the target file is deleted if there is no test.

    :param file_path:
    :param tests:
    :return: True if there is no test.
    """
    if tests:
        return False
    if file_path.exists():
        # The missing_ok parameter is added in python 3.8
        file_path.unlink()
        log(f"There is no more tests in the file {file_path}. Delete.")
    return True


def init(config_file_path: Optional[Path] = None) -> Config:
    config_logging()
    if config_file_path is None:
        config_file_path = Path() / CONFIG_FILE_NAME
    config = init_config(config_file_path)
    return config


def does_logging_config_file_exist() -> bool:
    return Path(LOGGING_CONFIG_FILE_NAME).exists()


def config_logging():
    if does_logging_config_file_exist():
        fileConfig(LOGGING_CONFIG_FILE_NAME, disable_existing_loggers=False)
    else:
        basicConfig()


def create_unit_test_file_name(base_name: str):
    return f"test_{base_name}_g.py"


def infer_unit_test_file_path_from_scribe_file(scribe_file_path: Path) -> Path:
    parent = scribe_file_path.parent
    module_name = scribe_file_path.stem
    file_name = create_unit_test_file_name(module_name)
    return parent.joinpath(file_name)


def call_target_function(func, binded_args):
    """
    The function name is used later to find this stack frame.

    :param func:
    :param binded_args:
    :return:
    """
    return func(*binded_args.args, **binded_args.kwargs)


def get_user_code_frames(additional_num_system_frame: int) -> list:
    """
    Return the call stack that belong to the user code being tested.

    Algorithm:
    Search from the bottom of the call stack less the known system frames on top
    looking for the function call_target_function.
    The user call frames start from the call after this frame.

    The number of known system frames on top depend on the caller of this
    function.
    The top most two frames are always the same:
    show_user_call_stack
    get_user_code_frames
    additional_num_system_frame parameter defines the number of additional system
    frames after these two frames.
    """
    frames = extract_stack()
    num_of_system_frames_on_top = 2 + additional_num_system_frame
    i = len(frames) - num_of_system_frames_on_top
    last_system_frame_name = call_target_function.__name__
    while True:
        if frames[i].name == last_system_frame_name:
            last_system_frame_index = i
            break
        else:
            i -= 1
    return frames[last_system_frame_index + 1: -num_of_system_frames_on_top]


def show_user_call_stack(additional_num_system_frame: int) -> None:
    """

    :param additional_num_system_frame: The number of additional system
    ( not user code frames on the top of the stack above the
    get_user_code_frames, show_user_call_stack functions)
    :return:
    """
    user_code_frames = get_user_code_frames(additional_num_system_frame)
    log("Call stack:")
    for frame_str in format_list(user_code_frames):
        log(frame_str)


def get_all_scribe_files(root_path: Path):
    return sorted(root_path.glob("**/*.tscribe"))


def infer_scribe_file_path(file_path: Path) -> Path:
    """
    Assumption: the scribe files should have the patten of <module name>.tscribe
    and the unit test files have the pattern of test_<module name>_g.py
    Raise an exception if the file path doesn't match either pattern above.

    :param file_path: a scribe file or unit test file path
    :return:
    """
    if file_path.suffix == SCRIBE_FILE_SUFFIX:
        return file_path
    module_name = infer_module_name_from_test_file_path(file_path.name)
    if module_name == "":
        raise Error(f"{file_path} is not a valid scribe file or a generated unit test file.")
    file_name = module_name + SCRIBE_FILE_SUFFIX
    return file_path.parent.joinpath(file_name)


def infer_module_name_from_test_file_path(file_name: str) -> str:
    result = match(pattern=r"test_(.+)_g\.py$", string=file_name)
    if result:
        return result.group(1)
    else:
        return ""
