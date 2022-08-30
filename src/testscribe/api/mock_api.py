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

from typing import Callable, Union, Optional
from unittest.mock import Mock

from testscribe import mocking_support
from testscribe.custom_type import Spec
from testscribe.mock_proxy import MockProxy
from testscribe.user_triggered_exception import UserTriggeredException


def throw(e: BaseException = Exception()):
    """
    Use this function in an input expression to cause a mock call to throw the
    given exception.
    :param e:
    :return:
    """
    return UserTriggeredException(exception=e)


def patch_with_mock(
    target: Union[str, type, Callable], mock_name: str = "", spec: Optional[Spec] = None
) -> None:
    mocking_support.patch_with_mock_internal(
        target=target, mock_name=mock_name, spec=spec
    )


def patch_with_expression(target_str: str, expression: str) -> None:
    mocking_support.patch_with_expression_internal(
        target_str=target_str, expression=expression
    )


def get_normalized_mock_calls(mock: Mock, spec: Spec) -> list:
    """
    Used in the generated unit test code to allow verifying mock calls consistently
    with keyword arguments when parameter names are available.

    :param mock:
    :param spec:
    :return:
    """
    return mocking_support.get_normalized_mock_calls_internal(mock=mock, spec=spec)


def m(spec: Spec, name: str = ""):
    return MockProxy(spec=spec, name=name)
