from __future__ import annotations

import logging
import sys
from importlib import import_module
from inspect import isfunction, getmembers, isclass
from pathlib import Path
from typing import List, Tuple, Union

from testscribe.error import Error
from testscribe.module import Module
from testscribe.util import load_object

logger = logging.getLogger(__name__)


def get_module(target_file: Path) -> Module:
    """
    Walk up the target file path to find the first parent that is in the sys.path.

    :param target_file:
    :return:
    """
    absolute_sys_paths = [Path(s).absolute() for s in sys.path]

    def get_module_name(dir_path: Path) -> List[str]:
        if dir_path.name == "":
            raise Error(f"The file ({target_file}) can't be loaded as a python module.")

        if dir_path in absolute_sys_paths:
            return []
        parent_path = dir_path.parent
        names = get_module_name(parent_path)
        names.append(dir_path.name)
        return names

    module_names = get_module_name(target_file.parent)
    module_names.append(target_file.stem)
    return Module(module_names)


def get_function(
    module_name: str, func_name: str
) -> Tuple[callable, Union[type, None]]:
    """

    :param module_name:
    :param func_name:
    :return: A tuple of the function object and class type if this is a method
    """
    obj = load_object(symbol_name=func_name, module_str=module_name)
    if isfunction(obj):
        return obj, None

    # todo: add a class parameter to explicitly indicate the target class
    # in a rare case when the target function is defined in two classes in the
    # same file.
    mod = import_module(module_name)
    classes = getmembers(mod, isclass)
    for class_name, class_type in classes:
        methods = getmembers(class_type, isfunction)
        for method_name, method_obj in methods:
            if method_name == func_name:
                return method_obj, class_type
    raise Error(
        f"Can't find the function or method with the name {func_name} in module {module_name}."
    )
