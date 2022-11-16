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

from dataclasses import dataclass
from string import Template
from typing import Any, List, Tuple, Union

from testscribe.code_gen_util import (
    add_indentation,
    spec_contain_param_name_info,
    join_lines,
)
from testscribe.complex_value_util import contain_complex_value
from testscribe.config import g_indent
from testscribe.model_type import MockModel, MockCallModel
from testscribe.result_assertion import generate_assertion
from testscribe.value_util import get_value_repr


@dataclass
class MockCallParams:
    # used for the main assertion. The complex values will be
    # represented by ANY. Additional assertions will follow.
    param_str: str
    # key: parameter name of a complex parameter,  value: the value of that parameter
    name_to_value: dict
    # key: position(index) of a complex parameter in the parameter list
    # value: the value of that parameter.
    # used only when the parameter name is not available
    index_to_value: dict


def get_one_mock_call_arg_str(value_str: str, param_name: str) -> str:
    return f"{param_name}={value_str}" if param_name else value_str


def update_complex_mock_call_arg_map(
    name_to_value: dict,
    index_to_value: dict,
    index: int,
    param_name: str,
    v: Any,
):
    if param_name:
        name_to_value[param_name] = v
    else:
        index_to_value[index] = v
    # return these to make testing easier
    return name_to_value, index_to_value


def get_one_mock_call_param(
    arg_list: List[str],
    name_to_value: dict,
    index_to_value: dict,
    index: int,
    param_name: str,
    v: Any,
):
    if contain_complex_value(v):
        # If the value is too complex such as an object, use ANY here
        # and supplement with additional assertions.
        # todo: treat multi line string value as complex values too?
        value_str = "ANY"
        update_complex_mock_call_arg_map(
            name_to_value=name_to_value,
            index_to_value=index_to_value,
            index=index,
            param_name=param_name,
            v=v,
        )
    else:
        value_str = get_value_repr(v)
    arg_list.append(
        get_one_mock_call_arg_str(value_str=value_str, param_name=param_name)
    )
    # return these to make testing easier
    return arg_list, name_to_value, index_to_value


def get_mock_call_params(param_list: List[Tuple[str, Any]]) -> MockCallParams:
    """
    Generate mock call parameter string and
    dictionaries for complex values to support complex assertions.

    :param param_list: arguments list, the name is the argument name if available
        "" otherwise
    :return:
    """
    # Some functions e.g. some builtin functions may not have the parameter
    # names available.
    arg_list = []
    name_to_value = {}
    index_to_value = {}
    for index, (param_name, v) in enumerate(param_list):
        get_one_mock_call_param(
            arg_list=arg_list,
            name_to_value=name_to_value,
            index_to_value=index_to_value,
            index=index,
            param_name=param_name,
            v=v,
        )
    param_str = ", ".join(arg_list)
    return MockCallParams(
        param_str=param_str, name_to_value=name_to_value, index_to_value=index_to_value
    )


@dataclass
class ComplexMockCallParam:
    # The position of the mock call in the call list
    index: int
    # key: parameter name of a complex parameter,  value: the value of that parameter
    name_to_value: dict
    # key: position(index) of a complex parameter in the parameter list
    # value: the value of that parameter.
    # used only when the parameter name is not available
    index_to_value: dict


@dataclass
class MockCallList:
    # The string to be used in the main statement verifying mock calls
    call_list_str: str
    # Information needed to construct additional assertions for complex
    # parameter values
    complex_params: List[ComplexMockCallParam]


def generate_mock_call_list(m: MockModel) -> MockCallList:
    call_list = []
    complex_params: List[ComplexMockCallParam] = []
    for index, call in enumerate(m.calls):
        call_str, complex_call_param = generate_one_mock_call(index=index, call=call)
        call_list.append(call_str)
        if complex_call_param:
            complex_params.append(complex_call_param)
    return MockCallList(
        call_list_str="\n".join(call_list), complex_params=complex_params
    )


def generate_one_call_str(method_name: str, param_str: str):
    suffix = f".{method_name}" if method_name else ""
    return f"call{suffix}({param_str}),"


def get_one_complex_param(call_params: MockCallParams, index: int):
    if call_params.name_to_value or call_params.index_to_value:
        return ComplexMockCallParam(
            index=index,
            name_to_value=call_params.name_to_value,
            index_to_value=call_params.index_to_value,
        )
    else:
        return None


def generate_one_mock_call(
    index: int, call: MockCallModel
) -> Tuple[str, Union[None, ComplexMockCallParam]]:
    call_params = get_mock_call_params(call.parameters.as_list())
    call_str = generate_one_call_str(
        method_name=call.name, param_str=call_params.param_str
    )
    complex_call_param = get_one_complex_param(call_params=call_params, index=index)
    return call_str, complex_call_param


def get_mock_calls_variable_value(mock_name: str, spec_str: str) -> str:
    return (
        f"get_normalized_mock_calls({mock_name}, {spec_str})"
        if spec_contain_param_name_info(spec_str)
        else f"{mock_name}.mock_calls"
    )


def generate_mock_call_list_verfication(
    mock_name: str, spec_str: str, mock_calls_name: str, call_list_str: str
) -> str:
    """
    Generate the main statement for verifying mock calls for one mock object.

    :param mock_name:
    :param spec_str:
    :param mock_calls_name: the variable name for the actual mock calls
    :param call_list_str: the string representing the call objects
    :return:
    """
    mock_calls_variable_value = get_mock_calls_variable_value(mock_name, spec_str)
    template_str = """\
${mock_calls_name} = ${mock_calls_variable_value}
assert ${mock_calls_name} == [
$call_list_str
]"""
    template = Template(template_str)
    call_list_assertion_str = template.substitute(
        g_indent=g_indent,
        mock_name=mock_name,
        mock_calls_name=mock_calls_name,
        mock_calls_variable_value=mock_calls_variable_value,
        call_list_str=add_indentation(call_list_str, 1),
    )
    return add_indentation(call_list_assertion_str, 1)


def generate_complex_param_verification(
    params: ComplexMockCallParam, mock_calls_name: str
) -> List[str]:
    prefix = f"{mock_calls_name}[{params.index}]"
    # Call's kwargs and args attributes are introduced in Python 3.8
    # Use [2] and [1] respectively to make the generated code compatible with Python 3.7.
    keyword_args_statement = [
        generate_assertion(f"{prefix}[2][{repr(k)}]", v)
        for k, v in params.name_to_value.items()
    ]
    position_args_statement = [
        generate_assertion(f"{prefix}[1][{i}]", v)
        for i, v in params.index_to_value.items()
    ]
    return keyword_args_statement + position_args_statement


def generate_mock_call_verification(m: MockModel) -> str:
    call_list = generate_mock_call_list(m)
    if not call_list.call_list_str:
        # assert_not_called doesn't track the child mocks.
        # The mock_calls property does.
        return f"{g_indent}{m.name}.assert_not_called()"
    mock_name = m.name
    mock_calls_name = f"{mock_name}_mock_calls"
    call_list_verification_statement = generate_mock_call_list_verfication(
        mock_name=mock_name,
        spec_str=m.spec_str,
        mock_calls_name=mock_calls_name,
        call_list_str=call_list.call_list_str,
    )
    statements = [call_list_verification_statement]
    for params in call_list.complex_params:
        statements.extend(
            generate_complex_param_verification(
                params=params, mock_calls_name=mock_calls_name
            )
        )
    return join_lines(lines=statements, prepend_new_line=False)


def generate_mock_call_verification_str(mocks: List[MockModel]) -> str:
    statements = [generate_mock_call_verification(m) for m in mocks]
    return join_lines(statements, prepend_new_line=True)
