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

import collections.abc
import typing
from inspect import Parameter, Signature
from types import (
    FunctionType,
    BuiltinFunctionType,
    MethodType,
    ModuleType,
)
from typing import (
    Any,
    AnyStr,
    NamedTuple,
    FrozenSet,
    DefaultDict,
    OrderedDict,
    ChainMap,
    Counter,
    Deque,
    Optional,
    Union,
    TypeVar,
)


def is_function_type(t: type):
    # doesn't include typing.Callable[[], int] or Callable
    return t in (FunctionType, BuiltinFunctionType, MethodType)


def is_function_instance(v: Any) -> bool:
    """
    Include method instances.

    :param v:
    :return:
    """
    return is_function_type(type(v))


def is_typing_callable_type(t: type):
    """
    Classes are callable. But this function only returns True
    for the Callable and its decorated form e.g. Callable[[int], int].
    :param t:
    :return:
    """
    return t in (typing.Callable, collections.abc.Callable) or get_type_origin(t) in (
        typing.Callable,
        collections.abc.Callable,
    )


def is_a_class_instance(v: Any) -> bool:
    return is_class_type(type(v))


def is_class_type(t: type) -> bool:
    if is_primitive_type(t) or is_container_type(t) or is_union_type(t):
        return False
    if type(t) is TypeVar:
        # Don't support mocking a TypeVar.
        # In Python3.7, get_type_args(List) returns (~T,) T is a TypeVar.
        # This check allows the mock marker matching logic to safely ignore these types.
        return False
    # Callable types are considered class types
    # Thus they can be mocked. e.g. a method can return Callable
    # todo: more checks for additional types
    # todo: find a more reliable way to test if it is a class type
    return True


def get_class_type(t: type) -> Optional[type]:
    """
    If the type is either a class type or a union type with at least one class type,
    returns the first class type.
    Return None otherwise.

    :param t:
    :return:
    """
    if is_class_type(t):
        return t
    if get_type_origin(t) == Union:
        element_types = get_type_args(t)
        for e_t in element_types:
            if is_class_type(e_t):
                return e_t
    return None


def is_primitive_type(t: type) -> bool:
    return t in [
        int,
        bool,
        str,
        float,
        bytes,
        type(None),
        ModuleType,
        Any,
        Parameter.empty,
        Signature.empty,
        AnyStr,
        # PyYaml has trouble saving the value Ellipsis
        # type(Ellipsis),
    ] or is_function_type(t)
    # todo: Literal type is introduced in Python 3.8. Check it?


def is_primitive_container_type(t: type):
    return t in [list, tuple, set, dict]


def is_container_type(t: type) -> bool:
    # todo: check for other container types
    # https://docs.python.org/3/library/typing.html
    return (
        is_primitive_container_type(t)
        or is_primitive_container_type(get_type_origin(t))
        or t
        in (
            NamedTuple,
            FrozenSet,
            DefaultDict,
            OrderedDict,
            ChainMap,
            Counter,
            Deque,
        )
        # todo: handle TypedDicts which is introduced in Python 3.8
    )


def get_type_origin(t: type):
    # https://docs.python.org/3/library/typing.html#typing.get_origin
    if hasattr(typing, "get_origin"):  # pragma: no cover
        # This gets executed on Python 3.8 and above only.
        return typing.get_origin(t)
    else:
        return getattr(t, "__origin__", None)


def get_type_args(t: type):
    # https://docs.python.org/3/library/typing.html#typing.get_args
    if hasattr(typing, "get_args"):  # pragma: no cover
        # This gets executed on Python 3.8 and above only.
        return typing.get_args(t)
    else:
        # There are differences between this attribute and get_args.
        # for typing.Callable[[str] ,int]
        # Expected :([<class 'str'>], <class 'int'>)
        # Actual   :(<class 'str'>, <class 'int'>)
        # Fortunately, Callable type's arguments are currently not used by this tool.

        # for typing.List
        # Expected :()
        # Actual   :(~T,)
        # for typing.Dict
        # Expected :()
        # Actual   :(typing.~KT, typing.~VT)
        # The TypeVar types will be safely ignored during the mock marker processing. See is_class_type.
        # So the difference doesn't matter as long as the unit tests don't test these cases.
        return getattr(t, "__args__", None)


def is_spec_value(value):
    return isinstance(value, type) or callable(value)


def is_union_type(t: type) -> bool:
    return get_type_origin(t) == Union
