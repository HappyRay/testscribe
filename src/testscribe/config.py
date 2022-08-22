from __future__ import annotations

import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Union

from yaml import safe_load

from testscribe import global_var
from testscribe.api.io_provider import IOProvider
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


def add_additional_python_paths(data: dict):
    path_strings = data.get(ADDITIONAL_PYTHON_PATH_KEY, [])
    sys.path.extend(path_strings)


def get_output_root_path(data: dict) -> Path:
    output_root_dir = data.get(OUTPUT_ROOT_DIR_KEY, "")
    if output_root_dir:
        return Path(output_root_dir)
    else:
        return Path()


def initialize_io(data: dict) -> IOProvider:
    io_provider_class_name = data.get(IO_PROVIDER_CLASS_NAME, "")
    if io_provider_class_name:
        io_provider_class = get_symbol(io_provider_class_name)
        global_var.g_io = io_provider_class()
    return global_var.g_io


def init_config(config_file_path: Path) -> Config:
    # todo: make io provider configurable
    data = load_config_data(config_file_path)
    add_additional_python_paths(data)
    initialize_io(data)
    output_root_path = get_output_root_path(data)
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
