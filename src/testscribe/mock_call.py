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
from collections.abc import Iterable
from inspect import signature, Signature
from typing import Any, List, Optional

from testscribe import global_var
from testscribe.context import Context
from testscribe.custom_type import Spec
from testscribe.execution_util import show_user_call_stack
from testscribe.log import log
from testscribe.model_type import TestModel, MockCallModel, get_mock_by_name
from testscribe.namedvalues import NamedValues
from testscribe.reflection_util import (
    has_param_names,
    get_typing_callable_return_type,
    get_method,
    get_return_type,
    is_instance_method,
)
from testscribe.special_type import NoDefault
from testscribe.type_util import is_typing_callable_type, is_function_instance
from testscribe.user_triggered_exception import UserTriggeredException
from testscribe.value_util import get_value

logger = logging.getLogger(__name__)

STR_MAGIC_METHOD_NAME = "__str__"


class MockCall:
    # Define class variables here to provide type information for the instant variables
    # spec field is missing here because there is no good default value
    # to provide. If set to str for example, the field spec will be detected
    # as a method since str is callable.
    method_name = ""
    mock_name = ""
    previous_call_count = 0
    args = NamedValues()

    def __init__(
        self,
        method_name: str,
        mock_name: str,
        spec: Spec,
        previous_call_count: int,
    ):
        """

        :param method_name: '' if this is a direct call on the mock object
        :param mock_name: the name of the mock object associated with this call
        :param spec: the spec of the mock object
        :param previous_call_count: how many times this method of the mock object
        has been called before this call
        """
        #
        self.method_name = method_name
        self.mock_name = mock_name
        self.spec = spec
        self.previous_call_count = previous_call_count

        # The args is a transformed deep copy of the mock call parameters.
        self.args = NamedValues()
        self.return_value = None

    def __call__(self, *args, **kwargs) -> Any:
        return self.call_internal(*args, **kwargs)

    def call_internal(self, *args, **kwargs) -> Any:
        self.args = save_args(self, args, kwargs)
        value = get_return_value(self)

        # Unlike mock attributes, the return value is not used again
        # during the execution of the target function. So there is
        # no need to keep a separate copy of the transformed value.
        self.return_value = prepare_value_for_storage(value)
        return get_true_return_value(value)


def save_args(mock_call: MockCall, args: Iterable, kwargs: dict) -> NamedValues:
    args_list = get_args_list(mock_call=mock_call, args=args, kwargs=kwargs)

    # transform the value early to keep a copy of the original value
    # in case the value is changed after execution.
    transformed = prepare_value_for_storage(args_list)
    return NamedValues(transformed)


def prepare_value_for_storage(v: Any):
    # avoid circular reference
    from testscribe.transformer import transform_value

    return transform_value(v)


def get_args_list(mock_call: MockCall, args: Iterable, kwargs: dict) -> list:
    # todo: handle the TypeError exception that may be thrown in bind
    #  if the parameters don't match the signature
    # https://docs.python.org/3/library/inspect.html#inspect.Signature
    sig = get_mock_call_signature(mock_call)
    return get_args_list_internal(
        method_name=mock_call.method_name,
        sig=sig,
        spec=mock_call.spec,
        args=args,
        kwargs=kwargs,
    )


def get_mock_call_signature(mock_call: MockCall) -> Signature:
    # todo: Some builtin objects don't provide signatures. e.g. dict.items()
    spec = mock_call.spec
    method_name = mock_call.method_name
    if method_name:
        method = get_method(spec, method_name)
        sig = signature(method)
    else:
        # This is a call on the mock directly.
        # Either the mock is a function or it is a call to instantiate
        # a class.
        sig = signature(spec)
    logger.debug(f"Mock call signature {sig}")
    return sig


def get_args_list_internal(
    method_name: str,
    sig: Signature,
    spec: Spec,
    args: Iterable,
    kwargs: dict,
):
    if is_instance_method(clazz=spec, method_name=method_name):
        # Since this is a method call, the first argument is always self.
        bound_args = sig.bind(None, *args, **kwargs)
        args_list = list(bound_args.arguments.items())[1:]
    else:
        args_list = get_func_args_list(sig=sig, spec=spec, args=args, kwargs=kwargs)
    return args_list


def get_func_args_list(
    sig: Signature, spec: Spec, args: Iterable, kwargs: dict
) -> list:
    if has_param_names(spec):
        bound_args = sig.bind(*args, **kwargs)
        # noinspection PyTypeChecker
        args_list = list(bound_args.arguments.items())
    else:
        positional_args = [("", v) for v in args]
        args_list = positional_args + list(kwargs.items())
    return args_list


def get_return_value(mock_call: MockCall) -> Any:
    description = get_call_description(mock_call)
    default = get_default_mock_call_return_value(mock_call)
    return_type = get_mock_call_return_type(
        method_name=mock_call.method_name, spec=mock_call.spec
    )
    # avoid circular references
    from testscribe.value_input import get_one_value

    value = get_one_value(
        prompt_name="the return value",
        t=return_type,
        context=Context(description),
        default=default,
    )
    log(f"Mock call return value: {repr(value)}")
    return value


def get_call_description(mock_call: MockCall) -> str:
    arg_str_display = get_arg_str_display(mock_call)
    subject = get_call_subject(mock_call)
    description = f"{subject} is called{arg_str_display}."
    log(description)
    show_user_call_stack(additional_num_system_frame=4)
    return description


def get_arg_str_display(mock_call: MockCall):
    arg_str = mock_call.args.as_arg_str()
    arg_str_display = f"\nwith: {arg_str}" if arg_str else ""
    return arg_str_display


def get_call_subject(mock_call: MockCall) -> str:
    mock_name = mock_call.mock_name
    method_name = mock_call.method_name
    if method_name:
        return f"{mock_name}'s {mock_call.method_name} method"
    else:
        return mock_name


def get_default_mock_call_return_value(mock_call: MockCall) -> Any:
    if mock_call.method_name == STR_MAGIC_METHOD_NAME:
        return f"mock {mock_call.mock_name}"
    return get_default_return_value_internal(
        mock_call=mock_call,
        test_to_infer_default_inputs=global_var.g_test_to_infer_default_inputs,
    )


def get_default_return_value_internal(
    mock_call: MockCall, test_to_infer_default_inputs: Optional[TestModel]
):
    # disable the debug log since it makes generated tests more complex.
    # logger.debug(f"infer default input from test: {test_to_infer_default_inputs}")
    if test_to_infer_default_inputs is None:
        return NoDefault
    existing_mock = get_mock_by_name(
        mocks=test_to_infer_default_inputs.mocks, name=mock_call.mock_name
    )
    if existing_mock is None:
        return NoDefault
    return get_default_return_value_from_models(
        mock_call_models=existing_mock.calls, mock_call=mock_call
    )


def get_default_return_value_from_models(
    mock_call_models: List[MockCallModel], mock_call: MockCall
) -> Any:
    existing_return_values = [
        call.return_value
        for call in mock_call_models
        if call.name == mock_call.method_name
    ]
    size = len(existing_return_values)
    # There will be cases when the default value is not picked
    # correctly.
    # todo: make all possible values selectable.
    if size > 0:
        # The new production code may have different number of calls to
        # this method. Select from the existing test's calls in a round-robin fashion.
        return existing_return_values[mock_call.previous_call_count % size]
    else:
        return NoDefault


def get_mock_call_return_type(method_name: str, spec: Spec) -> type:
    if method_name == STR_MAGIC_METHOD_NAME:
        # __str__'s signature returned by the get_return_type is _empty
        return_type = str
    elif method_name:
        method = get_method(spec, method_name)
        return_type = get_return_type(func=method)
    elif is_function_instance(spec):
        return_type = get_return_type(spec)
    elif is_typing_callable_type(spec):
        return_type = get_typing_callable_return_type(spec)
    else:
        # This is a call to instantiate a class
        # the return type should be the target class but the function
        # signature has None as return type
        # todo: support Callable e.g. Callable, Callable[[int], str]
        return_type = spec
    logger.debug(f"return type {return_type}")
    return return_type


def get_true_return_value(value: Any) -> Any:
    """
    Return the return value needed to run the target function

    :param value:
    :return:
    """
    true_value = get_value(value)
    if isinstance(true_value, UserTriggeredException):
        user_exeception = true_value.exception
        raise user_exeception
    else:
        return true_value
