from types import ModuleType
from typing import Any, Callable

from test_scribe.model_type import ObjectModel, ModuleModel, SetModel
from test_scribe.type_util import is_class_type, is_a_class_instance


def generic_is_special_type(
    value: Any, is_special_type_func: Callable[[Any], bool]
) -> bool:
    """

    :param is_special_type_func:
    :param value:
    :return: True if the value is a type that contains a type that will return
    True by the is_special_type_func check.
    """
    if is_special_type_func(value):
        return True
    elif is_enumerable_type(value):
        items = value
    elif isinstance(value, dict):
        items = value.values()
    else:
        return False

    for i in items:
        if generic_is_special_type(value=i, is_special_type_func=is_special_type_func):
            return True
    return False


def is_enumerable_type(value):
    return isinstance(value, list) or isinstance(value, tuple) or isinstance(value, set)


def is_complex_value(value):
    """
    Is this value of a type that need special assertions.

    :param value:
    :return:
    """
    t = type(value)
    return t in (ObjectModel, ModuleModel, SetModel)


def contain_complex_value(value):
    return generic_is_special_type(value=value, is_special_type_func=is_complex_value)


def has_unstable_repr_single_item(value) -> bool:
    """

    :param value: The value of a member of a class instance
    :return:
    """
    t = type(value)
    if callable(value) or t == ModuleType:
        return True
    if is_class_type(t):
        # If the member object doesn't implement __repr__,
        # it will be represented like
        # <test_data.simple.Dummy object at 0x7f55748d2be0>
        return not has_custom_repr_method(t) or object_contains_unstable_repr(value)
    return False


def has_unstable_repr(value) -> bool:
    return generic_is_special_type(
        value=value, is_special_type_func=has_unstable_repr_single_item
    )


def object_contains_unstable_repr(value) -> bool:
    """
    The value is an instance of a class. It contains a member that its repr is not
    stable i.e. it can change when run on different machines.
    e.g.
    a function's repr is like <function foo at 0x7fe688ff6b80>
    a module's repr is like
    <module 'test_data.simple' from '.../code/test-scribe/python/tests/test_data/simple.py'>
    a class instance's default repr is like <<test_data.simple.Dummy object
      at 0x7f55748d2be0>
    :param value:
    :return:
    """
    assert is_a_class_instance(value)
    if hasattr(value, "__dict__"):
        for name, v in vars(value).items():
            if has_unstable_repr(v):
                return True
    return False


def has_custom_repr_method(t: type) -> bool:
    """
    Return True if the type implements a custom __repr__ method.

    Return True also if the class inherit from a class that implements a
    custom __repr__ method. Ideally it should only return False in this case.
    There doesn't seem to be a reliable way to detect it though.
    """

    return t.__repr__ is not object.__repr__
