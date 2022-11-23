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
import collections
import typing
from functools import partial
from inspect import Parameter, Signature, getmembers, signature, getattr_static
from typing import Any, Callable, get_type_hints, List, Iterable

from testscribe.custom_type import Spec
from testscribe.error import Error
from testscribe.special_type import SingleLineString
from testscribe.type_util import (
    is_class_type,
    is_typing_callable_type,
    is_function_instance,
    get_type_args,
    get_type_origin,
)
from testscribe.util import BUILTIN_MODULE_NAME, load_object

TYPE_TO_TYPE_NAME = {
    Any: "any",
    SingleLineString: "str",
    Parameter.empty: "unknown",
    Signature.empty: "unknown",
}


def get_type_name(t: type) -> str:
    if t in TYPE_TO_TYPE_NAME:
        return TYPE_TO_TYPE_NAME[t]
    if is_class_type(t):
        return get_full_spec_name(t)
    if hasattr(t, "__name__"):
        return t.__name__
    return str(t)


def get_full_spec_name(t: Spec) -> str:
    """
    Return the fully qualified name of an object based on where it is defined
    not how it is imported.
    e.g. if t is a function foo defined in module mod_a and imported into module mod_b
    using "from mod_a import foo as f2" calling this function with mod_b.f2 will return
    mod_a.foo

    :param t:
    :return: full name including module
    """
    if is_callable_type(t):
        # Callable or Callable[[int], int] doesn't have the __qualname__
        # attribute prior to Python 3.10. In Python 3.10, the __qualname__ attribute doesn't contain the
        # parameter type.
        return repr(t)
    module_name = t.__module__
    module_str = "" if module_name == BUILTIN_MODULE_NAME else module_name + "."
    return f"{module_str}{t.__qualname__}"


def has_param_names(spec: Spec):
    """
    return True if the spec has information about the names of the parameters.
    e.g. Callable[[int], int] doesn't.
    :param spec:
    :return:
    """
    # todo: find a more reliable way to check
    return not is_callable_type(spec)


def is_callable_type(t: Spec) -> bool:
    origin = get_type_origin(t)
    return origin is collections.abc.Callable


def get_typing_callable_return_type(t: type):
    assert is_typing_callable_type(t)
    args = get_type_args(t)
    if args:
        return args[1]
    else:
        return Parameter.empty


def is_method(clazz: type, name: str):
    """
    Return true if the attribute is a method defined by this class

    :param clazz: the Class definition
    :param name:
    :return:
    """
    if name in dir(clazz):
        attrib = getattr(clazz, name)
        # todo: make it work with a callable class variable
        return callable(attrib)
    return False


def get_method(clazz: type, method_name: str):
    methods = getmembers(clazz)
    for n, func in methods:
        if n == method_name and callable(func):
            # Can't use is_function_instance(func) to valify that the member is a method
            # __str__ method of a mock object for example has a class type.
            return func
    return None


def is_instance_method(clazz: type, method_name: str):
    try:
        m = getattr_static(clazz, method_name)
        return not (isinstance(m, staticmethod) or isinstance(m, classmethod))
    except AttributeError:
        return False


def get_return_type(func: Callable) -> type:
    sig = signature(func)
    return_annotation = sig.return_annotation
    if isinstance(return_annotation, str):
        # delayed annotation processing is enabled.
        # see https://www.python.org/dev/peps/pep-0563/
        name_to_annotation_dict = get_type_hints(func)
        return name_to_annotation_dict["return"]
    else:
        return return_annotation


def get_param_list(func: Callable) -> List[Parameter]:
    """
    Return a normalized list of Parameter
    This is needed because with from __future__ import annotations
    the types returned from signature() will all be strings.
    get_type_hints() however will process the type strings into type classes.

    :param func: a function or method object
    :return:
    """
    sig = signature(func)
    # Unlike signature(), get_type_hint() doesn't automatically return
    # the annotation for the __init__ method.
    func_to_get_type_info = (
        func if is_function_instance(func) else getattr(func, "__init__")
    )
    name_to_annotation_dict = get_type_hints(func_to_get_type_info)
    param_info_list = sig.parameters.values()

    def normalize(p: Parameter) -> Parameter:
        annotation = p.annotation
        if isinstance(annotation, str):
            name = p.name
            annotation_type = name_to_annotation_dict[name]
            return Parameter(name=name, kind=p.kind, annotation=annotation_type)
        else:
            return p

    return [normalize(p) for p in param_info_list]


def get_method_signature_for_caller(clazz: type, name: str):
    """
    Get the method signature as used by the caller.
    e.g. if this is an instance method, the signature should not include self.
    :param clazz:
    :param name:
    :return:
    """
    method = get_method(clazz, name)
    if method is None:
        raise Error(f"{name} is not a method of the class {clazz}")
    # todo: Some builtin objects don't provide signatures. e.g. dict.items()
    if is_instance_method(clazz, name):
        return signature(partial(method, None))
    else:
        return signature(method)


def get_bound_arguments(sig, args: Iterable, kwargs: dict) -> dict:
    return sig.bind(*args, **kwargs).arguments


def remove_brackets(full_name: str) -> str:
    """
    Remove everything after the first "["
    for the input like typing.Callable[[typing.Any], bool]
    """
    name, _, _ = full_name.partition("[")
    return name


def get_module_and_symbol(full_name: str) -> typing.Tuple[str, str]:
    """
    Can't handle a method name e.g. test_data.simple.C.bar

    :param full_name: assumes the last component as separated by "." is the symbol name.
    :return: tuple( module name, symbol name)
    """
    name = remove_brackets(full_name)
    components = name.split(".")
    module_parts = components[:-1]
    return ".".join(module_parts), components[-1]


def get_module_str(full_name: str) -> str:
    return get_module_and_symbol(full_name)[0]


def get_module_str_from_object(obj: Any) -> str:
    # Objects not implemented in python may not have the __module__ attribute
    if hasattr(obj, "__module__"):
        return obj.__module__
    else:
        return ""


def get_symbol(full_name: str):
    module_name, symbol = get_module_and_symbol(full_name)
    obj = load_object(symbol_name=symbol, module_str=module_name)
    if obj is None:
        raise Error(f"{full_name} is not a valid identifier.")
    return obj
