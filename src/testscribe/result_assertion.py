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
from typing import Any

from testscribe.code_gen_util import pretty_format_repr_string, add_indentation
from testscribe.complex_value_util import contain_complex_value
from testscribe.config import g_indent
from testscribe.model_type import MockNameModel, ObjectModel, ModuleModel, SetModel

logger = logging.getLogger(__name__)


def generate_class_assertion(target, value: ObjectModel) -> str:
    """
    indentation becomes more complex due to the use of for multiline strings.
    They can't be indented the same way.
    Thus, indentation has to be handled in each special assertion functions.

    :param target:
    :param value:
    :return:
    """
    assert isinstance(value, ObjectModel)
    class_type_assertion = f"{g_indent}assert isinstance({target}, {value.type})"
    representation = value.repr
    if representation:
        member_assertions = [
            generate_assertion(target=f"repr({target})", value=representation)
        ]
    else:
        member_assertions = [
            generate_assertion(f"{target}.{name}", value)
            for name, value in value.members.items()
        ]
    return "\n".join([class_type_assertion] + member_assertions)


def generate_special_collection_assertion(target: str, value) -> str:
    type_assertion = f"{g_indent}assert isinstance({target}, {type(value).__name__})"
    length_assertion = f"{g_indent}assert len({target}) == {len(value)}"
    if isinstance(value, list) or isinstance(value, tuple):
        member_assertions = [
            generate_assertion(f"{target}[{index}]", item)
            for index, item in enumerate(value)
        ]
    else:
        # set that contains complex values should have generated an error earlier.
        # There isn't a reliable way to identify an element in a set
        # to assert separately.
        assert isinstance(value, dict)
        member_assertions = [
            generate_assertion(f"{target}[{repr(key)}]", item)
            for key, item in value.items()
        ]
    return "\n".join([type_assertion, length_assertion] + member_assertions)


def generate_module_assertion(target: str, value: ModuleModel) -> str:
    assert isinstance(value, ModuleModel)
    # Use local import since this is rare
    import_module_type = "from types import ModuleType"
    type_assertion = f"assert type({target}) == ModuleType"
    member_assertion = f"{target}.__name__ == {repr(value.name)}"
    statement = "\n".join([import_module_type, type_assertion, member_assertion])
    return add_indentation(s=statement, level=1)


def generate_set_assertion(target: str, value: SetModel) -> str:
    # Set members are not sorted, use the sorted member list for the generated
    # assertions to keep the result stable.

    # python3 doesn't allow sorting set with mixed types e.g.
    #     s = set([1, 2, 'string'])
    #     print(sorted(list(s)))
    # will result in an error
    #  TypeError: '<' not supported between instances of 'int' and 'str'
    # todo: find a solution. Maybe a switch to disable sorting or catch the exception
    #  and generate a non sorted version?
    assert isinstance(value, SetModel)
    type_assertion = f"{g_indent}assert isinstance({target}, set)"
    member_assertions = generate_assertion(f"sorted(list({target}))", value.elements)
    return "\n".join([type_assertion, member_assertions])


g_complex_type_assertion_function_look_up = {
    ObjectModel: generate_class_assertion,
    ModuleModel: generate_module_assertion,
    SetModel: generate_set_assertion,
}


def generate_complex_type_assertion(target: str, value) -> str:
    func = g_complex_type_assertion_function_look_up.get(
        type(value), generate_special_collection_assertion
    )
    return func(target=target, value=value)


def generate_assertion(target: str, value: Any) -> str:
    if contain_complex_value(value):
        return generate_complex_type_assertion(target, value)
    str_repr = (
        pretty_format_repr_string(value) if isinstance(value, str) else repr(value)
    )
    if (
        value is None
        or isinstance(value, bool)
        # using == to compare a mock object will result in an unwanted __eq__ call.
        # This may mess up the assertion of the mock object's behavior.
        or isinstance(value, MockNameModel)
    ):
        operator = "is"
    else:
        operator = "=="
    return f"{g_indent}assert {target} {operator} {str_repr}"


def generate_result_assertion(result: Any) -> str:
    assertions = generate_assertion("result", result)
    return "\n" + assertions
