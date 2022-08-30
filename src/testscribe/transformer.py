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

from types import ModuleType, FunctionType
from typing import Callable, Any

from testscribe.complex_value_util import (
    contain_complex_value,
    object_contains_unstable_repr,
    has_custom_repr_method,
)
from testscribe.error import UnsupportedDataError
from testscribe.log import log
from testscribe.mock_proxy import is_mock_proxy
from testscribe.model_type import (
    ObjectModel,
    CallableModel,
    MockNameModel,
    ExpressionModel,
    ModuleModel,
    SetModel,
)
from testscribe.reflection_util import get_full_spec_name, get_module_str_from_object
from testscribe.type_util import (
    is_class_type,
)
from testscribe.util import generic_transform
from testscribe.value_util import InputValue


def transform_value(v):
    """
    Replace certain values that can't be encoded correctly in Yaml to special
    types.
    """
    return generic_transform(v=v, transform_func=transform_individual_value_to_model)


def transform_individual_value_to_model(v):
    t = type(v)
    if is_mock_proxy(v):
        # Only mock names are needed here since this is a reference.
        # The mock object details are encoded elsewhere.
        return MockNameModel(v.name_test_scribe_)
    elif isinstance(v, InputValue):
        # Only the expression part is needed to generate
        # unit tests. And the generated YAML file will be more compact
        # and readable.
        return ExpressionModel(v.expression)
    elif callable(v) and hasattr(v, "__qualname__"):
        # A class instance may be callable by implementing the __call__ method.
        # but since it is not a class, it doesn't have the __qulname__ attribute
        # e.g. an instance of MockCall
        # Only the name is needed.
        return create_callable_model(v)
    elif t == ModuleType:
        # Modules can't be loaded from its native yaml representation correctly.
        # repr of a module is like
        # <module 'test_data.simple' from '.../code/test-scribe/python/tests/test_data/simple.py'>
        return ModuleModel(name=v.__name__)
    elif t == set:
        # A native set YAML representation is not stable. The order of the elements may
        # change when it is regenerated.
        # todo: handle the case when the set can't be sorted.
        if contain_complex_value(v):
            # There is currently no reliable way to identify the items in a set
            # to generate individual asserts.
            log(
                f"The set:\n{repr(v)}\n"
                "contains complex objects. It is currently not supported."
            )
            raise UnsupportedDataError(
                "Sets that contain complex objects are not supported."
            )
        return SetModel(elements=sorted(v))
    elif is_class_type(t):
        # pyyaml need to load the modules in order to load the objects.
        # Also, it is not clear how pyyaml can encode all objects using
        # constructors.
        # Loading arbitray Python objects requires the use of pyyaml
        # unsafe_loader.
        # After execution, there is no need to reconstruct the objects anyway.
        return transform_class(v)
    else:
        return v


def create_callable_model(v: Callable):
    if v == FunctionType:
        # the "function" type is callable. And the name "function" is undefined.
        # translate to the proper name using the "types" module.
        name = "FunctionType"
        module = "types"
    else:
        name = v.__qualname__
        module = get_module_str_from_object(v)
    return CallableModel(name=name, module=module)


def transform_class(value):
    t = type(value)
    assert is_class_type(t)
    full_class_name = get_full_spec_name(t)
    if can_use_repr(value):
        # Use __repr__ instead of __str__ to capture more details of the object
        # Ideally __repr__ can be used to reconstruct the exact object.
        # see https://dzone.com/articles/python-str-vs-repr
        representation = repr(value)
        members = {}
    else:
        representation = ""
        # vars function includes only properties and its values.
        # It doesn't include methods and builtin properties.
        # vars() only works when the value has __dict__ attribute
        # module values for example don't have such an attribute.
        # such values should have been filtered out before calling this method.
        # In case such a value is missed, set the members to {} just in case.
        members = (
            {name: transform_value(v) for name, v in vars(value).items()}
            if hasattr(value, "__dict__")
            else {}
        )

    return ObjectModel(type=full_class_name, repr=representation, members=members)


def can_use_repr(value: Any) -> bool:
    return has_custom_repr_method(type(value)) and not object_contains_unstable_repr(
        value
    )
