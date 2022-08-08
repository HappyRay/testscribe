# Reflection related functions that don't depend on other modules in this project
from typing import Any

from test_scribe.type_util import is_a_class_instance


def get_full_module_name(symbol: Any) -> str:
    if hasattr(symbol, "__module__"):
        return symbol.__module__
    else:
        return ""


def get_class_instance_repr_with_full_name(instance) -> str:
    assert is_a_class_instance(instance)
    full_module_name = get_full_module_name(instance)
    module_str = full_module_name + "." if full_module_name else ""
    return f"{module_str}{repr(instance)}"
