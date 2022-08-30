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

import logging
from dataclasses import dataclass
from typing import Any, List, Optional, Dict

from testscribe.constant import INVALID_TEST_INDEX
from testscribe.namedvalues import NamedValues
from testscribe.reflection_util import get_module_str
from testscribe.util import BUILTIN_MODULE_NAME, consistent_hash_str

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ObjectModel:
    type: str
    repr: str
    members: dict

    # The default __hash__ function can't hash a field that is a dictionary.
    # which is mutable. The error will be "TypeError: unhashable type: 'dict'".
    def __hash__(self):
        return consistent_hash_str(str(self))

    def __str__(self):
        if self.members:
            value_str = f"members ({self.members})"
        else:
            value_str = f"repr ({self.repr})"
        return f"Object(type ({get_type_str(self)}), {value_str})"

    def __repr__(self):
        if self.repr:
            module_str = get_module_str(self.type)
            prefix = module_str + "." if module_str else ""
            # Use the fully qualified name for the constructor assuming
            # the repr from a custom type starts with the type name.
            return prefix + self.repr
        else:
            # fall back to the str representation.
            # this type of object can't be used as keys in a dictionary.
            return str(self)


@dataclass(frozen=True)
class CallableModel:
    name: str
    module: str

    def __repr__(self):
        """
        Override the default implementation to allow the class instance to be
        used correctly when generating the test code.
        It can appear as a parameter value.
        :return:
        """
        if self.module == BUILTIN_MODULE_NAME:
            return self.name
        else:
            return f"{self.module}.{self.name}"


@dataclass(frozen=True)
class MockNameModel:
    name: str

    def __repr__(self):
        """
        Override the default implementation to allow the class instance to be
        used correctly when generating the test code.
        :return:
        """
        return self.name

    def __hash__(self):
        return consistent_hash_str(self.name)

    def __str__(self):
        return f"Mock( name: {self.name} )"


@dataclass(frozen=True)
class ExpressionModel:
    expression: str

    def __repr__(self):
        """
        Override the default implementation to allow the class instance to be
        used correctly when generating the test code.
        :return:
        """
        return self.expression

    def __str__(self):
        return f"Expression( {self.expression} )"


@dataclass(frozen=True)
class ModuleModel:
    name: str

    def __str__(self):
        return f"Module( {self.name} )"


@dataclass(frozen=True)
class SetModel:
    elements: list

    def __repr__(self):
        """
        Override the default implementation to allow the instance to be
        used correctly when generating the test code.
        It can appear as a parameter value.
        :return:
        """
        return f"set({repr(self.elements)})"


@dataclass
class MockCallModel:
    name: str
    parameters: NamedValues
    return_value: Any


@dataclass
class MockModel:
    name: str
    spec_str: str
    calls: List[MockCallModel]
    attributes: dict


@dataclass
class PatchModel:
    target: str
    replacement: Any


@dataclass
class ExceptionModel:
    type: str
    message: str

    def __str__(self):
        return f"Exception: type ( {self.type} ), message ( {self.message} )"


@dataclass
class TestModel:
    # The name field can be derived from the short_name field easily.
    # however, it is needed as a unique key in some cases.
    # It's thus kept for convenience.
    name: str
    # The name that doesn't include the test_<optiontal function name> prefix
    # It makes it easier to update the test name after the target function name
    # is changed and the function name is used in the test name prefix.
    # The name is required since it is better not to have to derive it from
    # the name attribute.
    short_name: str
    description: str
    target_func_name: str
    target_class_name: str
    init_parameters: NamedValues
    # parameters to the function/method. If there is an exception in the constructor
    # this value will be None
    parameters: Optional[NamedValues]
    exception: Optional[ExceptionModel]
    result: Any

    # Favor list over dictionary because the order of the list is stable.
    # When a new test is added, don't want to introduce unnecssary changes
    # to existing tests.
    mocks: List[MockModel]
    patches: List[PatchModel]


def get_mock_by_name(mocks: List[MockModel], name: str) -> Optional[MockModel]:
    for m in mocks:
        if m.name == name:
            return m
    return None


def sort_tests(tests: List[TestModel]) -> List[TestModel]:
    # sort tests based on the target
    # It's expected that most of the time, it is beneficial to have
    # these tests to be close to each other.
    return sorted(tests, key=get_test_sort_key)


def get_test_sort_key(test: TestModel) -> str:
    return test.target_class_name + test.target_func_name


def build_name_to_index_dict(tests: List[TestModel]) -> dict:
    return {t.name: index for index, t in enumerate(tests)}


@dataclass
class AllTests:
    tests: List[TestModel]
    module: str
    name_to_index: Dict[str, int]

    def __init__(self, module: str, tests: List[TestModel]):
        self.module = module
        self.tests = sort_tests(tests)
        self.name_to_index = build_name_to_index_dict(self.tests)
        logger.debug(f"Test name to index dict: {self.name_to_index}")

    def get_test_index_by_name(self, test_name: str) -> int:
        index = self.name_to_index.get(test_name, INVALID_TEST_INDEX)
        assert index == INVALID_TEST_INDEX or test_name == self.tests[index].name
        return index

    def does_test_exist(self, test_name: str) -> bool:
        return self.get_test_index_by_name(test_name) != INVALID_TEST_INDEX


def add_test(all_tests: AllTests, test: TestModel) -> AllTests:
    # Return a new AllTest to allow the constructor to maintain
    # the integrety of the internal cache and sorted properties.
    logger.info(f"Add test: {test.name}")
    # Add new tests before old tests
    # This behavior is assumed by the logic of guessing the default value
    # to use the latest test targeting the same function.
    new_tests = [test] + all_tests.tests
    return AllTests(module=all_tests.module, tests=new_tests)


def update_test(all_tests: AllTests, index: int, test: TestModel) -> AllTests:
    # make a copy of the list to avoid modifying the existing list
    new_tests = list(all_tests.tests)
    new_tests[index] = test
    return AllTests(module=all_tests.module, tests=new_tests)


def delete_test_by_name(all_tests: AllTests, name: str) -> AllTests:
    new_tests = [t for t in all_tests.tests if t.name != name]
    return AllTests(module=all_tests.module, tests=new_tests)


MODEL_TYPE_TO_STR: Dict[type, str] = {
    # More user friendly/readable type names.
    CallableModel: "Callable",
    MockNameModel: "Mock",
    ExpressionModel: "Expression",
    ModuleModel: "Module",
    SetModel: "Set",
    ExceptionModel: "Exception",
}


def get_type_str(v: Any) -> str:
    if isinstance(v, ObjectModel):
        t = v.type
    else:
        t = type(v)
    return MODEL_TYPE_TO_STR.get(t, str(t))
