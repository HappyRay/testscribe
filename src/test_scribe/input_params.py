from __future__ import annotations

import logging
from dataclasses import dataclass
from inspect import signature
from pathlib import Path
from typing import Callable, Optional

from test_scribe.file_info import get_function
from test_scribe.log import log
from test_scribe.module import Module

logger = logging.getLogger(__name__)


def create_output_dir_for_module(output_root_dir: Path, module: Module) -> Path:
    output_dir = output_root_dir.joinpath(*module.get_package_name_list())
    # Make sure the directory exists. If it doesn't exist,
    # create it including the parent directories.
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def get_scribe_file_path(output_root_dir: Path, module: Module) -> Path:
    """
    This function will ensure the parent directory exists.

    :param output_root_dir:
    :param module:
    :return:
    """
    output_dir = create_output_dir_for_module(
        output_root_dir=output_root_dir, module=module
    )
    module_name = module.get_module_name_only()
    return output_dir.joinpath(f"{module_name}.tscribe")


def get_target_function_name(input_params: InputParams) -> str:
    return input_params.func.__name__


def get_target_class_name(input_params: InputParams) -> str:
    clazz = input_params.clazz
    if clazz:
        return clazz.__qualname__
    else:
        return ""


@dataclass(frozen=True)
class InputParams:
    func: Callable
    output_root_dir: Path
    module: Module
    # if the target is a method, this is the class type of the associated class
    clazz: Optional[type]
    ask_for_test_name: bool
    ask_for_description: bool


def create_input_params(
    module: Module,
    function_name: str,
    output_root_dir: Path,
    ask_for_test_name: bool,
    ask_for_description: bool,
) -> InputParams:
    func, clazz = get_function(module.get_module_str(), function_name)
    sig = signature(func)
    log(f"The target function: {function_name} has the signature: {sig}")
    if clazz:
        log(f"The target class is: {clazz}")
    return InputParams(
        func=func,
        output_root_dir=output_root_dir,
        module=module,
        clazz=clazz,
        ask_for_test_name=ask_for_test_name,
        ask_for_description=ask_for_description,
    )
