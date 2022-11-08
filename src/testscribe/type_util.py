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
    Literal,
    AnyStr,
    NamedTuple,
    TypedDict,
    FrozenSet,
    DefaultDict,
    OrderedDict,
    ChainMap,
    Counter,
    Deque,
    Optional,
    Union,
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
        Literal,
        AnyStr,
        # PyYaml has trouble saving the value Ellipsis
        # type(Ellipsis),
    ] or is_function_type(t)


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
            TypedDict,
            FrozenSet,
            DefaultDict,
            OrderedDict,
            ChainMap,
            Counter,
            Deque,
        )
    )


def get_type_origin(t: type):
    # https://docs.python.org/3/library/typing.html#typing.get_origin
    if hasattr(typing, "get_origin"):
        return typing.get_origin(t)
    elif hasattr(t, "__origin__"):  # pragma: no cover
        # https://www.python.org/dev/peps/pep-0585/
        return t.__origin__
    else:  # pragma: no cover
        return None


def get_type_args(t: type):
    # https://docs.python.org/3/library/typing.html#typing.get_args
    if hasattr(typing, "get_args"):
        return typing.get_args(t)
    else:  # pragma: no cover
        # todo: work around for versions before python 3.8
        return None


def is_spec_value(value):
    return isinstance(value, type) or callable(value)


def is_union_type(t: type) -> bool:
    return get_type_origin(t) == Union
