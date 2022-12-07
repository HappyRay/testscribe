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

import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Union

from yaml import safe_load

from testscribe import global_var
from testscribe.api.io_provider import IOProvider
from testscribe.constant import DEFAULT_OUTPUT_ROOT_DIR_NAME
from testscribe.error import Error
from testscribe.file_info import get_function
from testscribe.reflection_util import get_module_and_symbol, get_symbol

g_indent = "    "

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Config:
    output_root_path: Path
    setup_function: Callable


CONFIG_FILE_NAME = "test-scribe-config.yml"
ADDITIONAL_PYTHON_PATH_KEY = "python-paths"
OUTPUT_ROOT_DIR_KEY = "output-root-dir"
SETUP_FUNCTION_KEY = "setup-function"
IO_PROVIDER_CLASS_NAME = "io-provider-full-class-name"


def get_setup_func(data: dict) -> Union[Callable, None]:
    if SETUP_FUNCTION_KEY not in data:
        return None
    full_name = data[SETUP_FUNCTION_KEY]
    base_msg = (
        f"The setup function as specified by the {SETUP_FUNCTION_KEY} key is:"
        f"{full_name}. It should be a valid fully qualified function name."
    )
    if not isinstance(full_name, str) or full_name == "":
        raise Error(f"{base_msg} The value is not a string or is an empty string.")
    try:
        module_str, function_name = get_module_and_symbol(full_name)
        func, clazz = get_function(module_name=module_str, func_name=function_name)
    except Exception as e:
        raise Error(f"{base_msg} Can't load this symbol.\nerror detail:\n{e}")
    # get_module_and_symbol assumes the name represents a function.
    # It can't handle a method name e.g. test_data.simple.C.bar
    assert clazz is None
    return func


def add_additional_python_paths(config_file_path: Path, data: dict):
    path_strings = data.get(ADDITIONAL_PYTHON_PATH_KEY, [])
    # Always append the config file path (which is the working directory by default)
    # to the sys.path
    # This is to make it easier to set up for common use cases.
    # Note that when invoking the tool using testscribe wrapper script, the current working directory
    # is not added to the sys.path.
    # If this is undesirable, the config file has to be defined at a path that should be in the sys.path.
    path_strings.append(".")
    # The path is relative to the location of the config file where it is defined.
    resolved_path_strings = [
        str(resolve_path(config_file_path=config_file_path, path_str=p)) for p in path_strings
    ]
    sys.path.extend(resolved_path_strings)


def get_output_root_path(config_file_path: Path, data: dict) -> Path:
    output_root_dir = data.get(OUTPUT_ROOT_DIR_KEY, "")
    if output_root_dir:
        return resolve_path(config_file_path=config_file_path, path_str=output_root_dir)
    else:
        # Default to a subdirectory under the current directory
        # to make clean up easier.
        return Path(DEFAULT_OUTPUT_ROOT_DIR_NAME)


def resolve_path(config_file_path: Path, path_str: str) -> Path:
    """
    Resolve the configured path string to a Path object
    :param config_file_path:
    :param path_str: configured path string
    :return:
    """
    config_file_dir_path = config_file_path.parent
    # todo: handle absolute path
    return config_file_dir_path.joinpath(path_str)


def initialize_io(data: dict) -> IOProvider:
    io_provider_class_name = data.get(IO_PROVIDER_CLASS_NAME, "")
    if io_provider_class_name:
        io_provider_class = get_symbol(io_provider_class_name)
        global_var.g_io = io_provider_class()
    return global_var.g_io


def init_config(config_file_path: Path) -> Config:
    data = load_config_data(config_file_path)
    add_additional_python_paths(config_file_path=config_file_path, data=data)
    initialize_io(data)
    output_root_path = get_output_root_path(config_file_path=config_file_path, data=data)
    func = get_setup_func(data)
    return Config(
        output_root_path=output_root_path,
        setup_function=func,
    )


def load_config_data(config_file_path: Path) -> dict:
    data = {}
    if config_file_path.exists():
        with open(config_file_path) as file:
            data = safe_load(file)
    return data
