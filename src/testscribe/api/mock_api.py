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
    """
    Patch an object with a mock.

    patch_with_expression can do the same. This function is easier to use
    for common use cases of mocking a function.

    :param target:
    If it is not a string, it should be the symbol that can to be
    patched with a mock object. e.g. if a function module_a.foo calls a function module_b.bar
    and the bar function is called with the form module_b.bar, bar can be mocked simply with patch_with_mock(bar).
    If they don't e.g. module_b.bar is imported
    into module_a as from module_b import bar and invoked as bar, to mock the invocation,
    use patch_with_mock("module_a.bar")
    This is the same "where to patch" rule as Python's patch function. See
    https://realpython.com/python-mock-library/#where-to-patch for more details.

    If bar is imported in mod_b with "from mod_a import foo as bar", given bar as the target, there is no way
    I can find to get "mod_b.bar" string. Thus,this API has to support the string form.
    :param mock_name: customize the mock object name
    :param spec: If None, which is the default, infer the spec from the target
    This parameter is useful when the target's signature is not available, e.g. the open function
    supply a spec object in this case to have a stronger signature check.
    See an example in the test for test_data.file_op.write_to_file
    """

    mocking_support.patch_with_mock_internal(
        target=target, mock_name=mock_name, spec=spec
    )


def patch_with_expression(target_str: str, expression: str) -> None:
    """
    Patch an object with the value of an expression.

    :param target_str: Take the same value as the target parameter of the patch function.
    See https://docs.python.org/3/library/unittest.mock.html#patch and
        https://realpython.com/python-mock-library/#where-to-patch
    :param expression: a valid Python expression. If the expression is a string, it has to be
    quoted. e.g. use "'abc'" to replace the target with a string value of abc
    """
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
