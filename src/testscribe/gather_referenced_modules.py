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

from typing import Optional, List, Any

from testscribe.model_type import (
    ExpressionModel,
    MockModel,
    TestModel,
    PatchModel,
    ObjectModel,
    CallableModel,
)
from testscribe.namedvalues import NamedValues
from testscribe.reflection_util import get_module_str
from testscribe.util import flattern_list, BUILTIN_MODULE_NAME
from testscribe.value_input_util import import_modules_from_expression


def is_expression(v):
    return isinstance(v, ExpressionModel)


def gather_expressions_from_named_values(
    nv: Optional[NamedValues],
) -> List[ExpressionModel]:
    if nv is None:
        return []
    return [v for _, v in nv.as_list() if is_expression(v)]


def gather_expressions_from_mock_attributes(m: MockModel) -> List[ExpressionModel]:
    return [attrib for attrib in m.attributes.values() if is_expression(attrib)]


def gather_expressions_from_mock_call_return(m: MockModel) -> List[ExpressionModel]:
    return [c.return_value for c in m.calls if is_expression(c.return_value)]


def gather_expressions_from_a_mock(m: MockModel) -> List[ExpressionModel]:
    return gather_expressions_from_mock_attributes(
        m
    ) + gather_expressions_from_mock_call_return(m)


def gather_expressions_from_mocks(t: TestModel) -> List[ExpressionModel]:
    list_of_list = [gather_expressions_from_a_mock(m) for m in t.mocks]
    return flattern_list(list_of_list)


def gather_expressions_from_patches(patches: List[PatchModel]) -> List[ExpressionModel]:
    return [p.replacement for p in patches if is_expression(p.replacement)]


def gather_expressions(t: TestModel) -> List[ExpressionModel]:
    return (
        gather_expressions_from_mocks(t)
        + gather_expressions_from_named_values(t.init_parameters)
        + gather_expressions_from_named_values(t.parameters)
        + gather_expressions_from_patches(t.patches)
    )


def gather_modules_from_expressions(expressions: List[ExpressionModel]) -> List[str]:
    module_names = []
    for exp in expressions:
        _, names = import_modules_from_expression(exp.expression)
        module_names.extend(names)
    return module_names


def get_module_names_from_expressions(t: TestModel):
    """
    Can't rely on global variables to gather the module names needed to support
    input expressions
    since the global variables are only available for the current test.

    :param t:
    :return:
    """
    expressions = gather_expressions(t)
    return gather_modules_from_expressions(expressions)


def get_module_names_in_mock_specs(test: TestModel) -> List[str]:
    return [get_module_str(m.spec_str) for m in test.mocks]


def get_module_names_from_value(v: Any) -> List[str]:
    t = type(v)
    names = []
    items = []
    if t is ObjectModel:
        names.append(get_module_str(v.type))
        items = v.members.values()
    elif t is CallableModel:
        names.append(v.module)
    elif t in (list, tuple, set):
        items = v
    elif t is dict:
        items = list(v.values()) + list(v.keys())

    for i in items:
        names.extend(get_module_names_from_value(i))

    return names


def get_module_names_in_result(test: TestModel) -> List[str]:
    exception = test.exception
    if exception:
        return [get_module_str(exception.type)]
    else:
        return get_module_names_from_value(test.result)


def get_module_names_in_one_mock_call_param(params: NamedValues) -> List[str]:
    return flattern_list([get_module_names_from_value(v) for _, v in params.as_list()])


def get_module_names_in_mock_call_params(t: TestModel) -> List[str]:
    names_list = [
        get_module_names_in_one_mock_call_param(c.parameters)
        for m in t.mocks
        for c in m.calls
    ]
    names = flattern_list(names_list)
    return names


def get_referenced_modules_in_a_test(t: TestModel) -> List[str]:
    return flattern_list(
        [
            get_module_names_in_mock_specs(t),
            get_module_names_in_mock_call_params(t),
            get_module_names_in_result(t),
            get_module_names_from_expressions(t=t),
        ]
    )


def gather_import_statements_from_module_names(module_names: List[str]):
    # Conver to a set first to remove duplicates
    sorted_module_names = sorted(set(module_names))
    return [
        f"import {name}"
        for name in sorted_module_names
        if name and name != BUILTIN_MODULE_NAME
    ]


def gather_import_statements_for_referenced_modules(
    tests: List[TestModel],
) -> List[str]:
    module_names_lists = [get_referenced_modules_in_a_test(t) for t in tests]
    module_names = flattern_list(module_names_lists)
    return gather_import_statements_from_module_names(module_names)
