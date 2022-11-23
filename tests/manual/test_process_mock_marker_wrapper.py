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
import typing
from unittest.mock import create_autospec, patch, call

import testscribe
from testscribe.api.mock_api import get_normalized_mock_calls
from wrapper.eval_expression_wrapper import process_mock_marker_wrapper


def test_process_mock_marker_wrapper_callable_with_parameter_types():
    """
    Based on a generated test.
    The generated version has this assertion
        assert m_mock_proxy_mock_calls[0][2]['spec']._special is False
    the _special attribute of the Callable type is no longer available on Python3.9
    Plus this version simplifies the assertion.
    :return:
    """
    m_mock_proxy: testscribe.mock_proxy.MockProxy = create_autospec(spec=testscribe.mock_proxy.MockProxy)
    m_mock_proxy.return_value = 1
    with patch('testscribe.eval_expression.MockProxy', m_mock_proxy):
        result = process_mock_marker_wrapper(t=typing.Callable[[int], int], v=testscribe.api.mock_api.m)
    assert result == 1
    m_mock_proxy_mock_calls = get_normalized_mock_calls(m_mock_proxy, testscribe.mock_proxy.MockProxy)
    assert m_mock_proxy_mock_calls == [
        call(spec=typing.Callable[[int], int]),
    ]


def test_process_mock_marker_wrapper_callable():
    """
    Based on a generated test.
    The generated version has this assertion
    assert isinstance(m_mock_proxy_mock_calls[0][2]['spec'], typing._VariadicGenericAlias)
    the _VariadicGenericAlias is no longer available on Python3.9
    Plus this version simplifies the assertion.

    """
    m_mock_proxy: testscribe.mock_proxy.MockProxy = create_autospec(spec=testscribe.mock_proxy.MockProxy)
    m_mock_proxy.return_value = 1
    with patch('testscribe.eval_expression.MockProxy', m_mock_proxy):
        result = process_mock_marker_wrapper(t=typing.Callable, v=testscribe.api.mock_api.m)
    assert result == 1
    m_mock_proxy_mock_calls = get_normalized_mock_calls(m_mock_proxy, testscribe.mock_proxy.MockProxy)
    assert m_mock_proxy_mock_calls == [
        call(spec=typing.Callable),
    ]
