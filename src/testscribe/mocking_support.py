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
from functools import partial
from inspect import signature
from typing import Union, Any, Callable, Optional
from unittest.mock import Mock, call

from testscribe import global_var
from testscribe.custom_type import Spec
from testscribe.error import Error
from testscribe.mock_proxy import MockProxy, is_mock_proxy
from testscribe.patcher import patch_common, remove_duplicate_patch
from testscribe.reflection_util import (
    has_param_names,
    get_bound_arguments,
    get_symbol,
    get_method_signature_for_caller,
    get_full_spec_name,
)
from testscribe.type_util import is_spec_value

logger = logging.getLogger(__name__)


def normalize_mock_call(mock_call, spec: Spec):
    """
    Return a tuple representing a mock call with the keyword arguments only.

    :param mock_call: a mock call of a Mock object
    :param spec: the spec of the Mock object
    :return: a tuple
        name: method name if this is a method call or "" if this is a call on the
        object itself
        args: should be ()
        kargs: keyword arguments dictionary
    """
    name, args, kwargs = mock_call
    get_bound_arguments_partial = partial(get_bound_arguments, args=args, kwargs=kwargs)
    if name:
        # this is a method call
        # todo: handle the error that the method doesn't exist.
        # The error should have been caught error when the method is
        # invoked.
        method_sig = get_method_signature_for_caller(clazz=spec, name=name)
        args = get_bound_arguments_partial(sig=method_sig)
        return getattr(call, name)(**args)
    else:
        # todo: handle __call__
        # If the parameter names are not available, it is simper to compare
        # directly with mock.mock_calls instead of using this function.
        assert has_param_names(spec)
        args = get_bound_arguments_partial(sig=signature(spec))
        return call(**args)


def get_direct_mock_calls(mock: Mock) -> list:
    # filter out the calls on the returned instances (child mocks).
    return [c for c in mock.mock_calls if "()" not in c[0]]


def get_normalized_mock_calls_internal(mock: Mock, spec: Spec) -> list:
    # The calls on the returned instances (child mocks) are asserted separately.
    direct_calls = get_direct_mock_calls(mock)
    actual_calls = [normalize_mock_call(mock_call=c, spec=spec) for c in direct_calls]
    return actual_calls


def get_target_str_from_obj(obj: Union[type, Callable, MockProxy]) -> str:
    """
    :param obj: An object to be patched e.g. class, function
    :return: The fully qualified name for the object
    """
    check_target_can_be_used_as_spec(obj)
    # The obj may have been patched.
    obj_source = obj.spec_test_scribe_ if is_mock_proxy(obj) else obj
    return get_full_spec_name(obj_source)


def check_target_can_be_used_as_spec(obj):
    if not is_spec_value(obj):
        msg = (
            f"{obj} is not a type or Callable."
            " It can't be used as a spec for a mock object."
        )
        raise Error(msg)


def get_mock_target_str(target: Union[str, type, Callable, MockProxy]) -> str:
    if isinstance(target, str):
        return target
    else:
        return get_target_str_from_obj(target)


def patch_with_mock_internal(
    target: Union[str, type, Callable, MockProxy], mock_name: str, spec: Optional[Spec]
) -> None:
    """
    See patch_with_mock
    """
    if not global_var.g_test_generating_mode:
        logger.debug("This is not a test generation session. Ignore patch.")
        return
    target_str = get_mock_target_str(target)
    # has to remove duplicate patches first before creating a mock
    # to avoid interference of the mock name creation.
    remove_duplicate_patch(target_str)
    if spec is None:
        obj = get_symbol(target_str)
        check_target_can_be_used_as_spec(obj)
        spec = obj
    mock_obj = MockProxy(spec=spec, name=mock_name)
    patch_common(target_str=target_str, replacement=mock_obj)


def patch_with_expression_internal(target_str: str, expression: str) -> None:
    """
    See patch_with_expression

    It's possible to derive the type so that the m and c convenience symbols
    can be used without specifying spec types.
    However, it may not be necessary given the patch_with_mock function.
    """
    if not global_var.g_test_generating_mode:
        logger.debug("This is not a test generation session. Ignore patch.")
        return
    remove_duplicate_patch(target_str)

    # avoid circular dependencies
    from testscribe.eval_expression import eval_expression

    replacement = eval_expression(user_input=expression, t=Any)
    patch_common(target_str=target_str, replacement=replacement)
