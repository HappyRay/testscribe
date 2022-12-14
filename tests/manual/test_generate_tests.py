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

from unittest.mock import Mock

from pytest import fixture

from testscribe.generate_imports import generate_import_statement_str
from testscribe.model_type import MockModel, AllTests
# Import TestModel as a different name without Test prefix to avoid
# a pytest warning
# PytestCollectionWarning:
# cannot collect test class 'TestModel' because it has a __init__ constructor
from testscribe.model_type import TestModel as TModel
from testscribe.namedvalues import NamedValues


def create_mock_test_model() -> TModel:
    t: TModel = Mock(TModel)
    t.target_class_name = ""
    t.mocks = []
    t.init_parameters = NamedValues()
    t.patches = []
    t.exception = None
    t.description = ""
    t.parameters = NamedValues()
    t.init_parameters = NamedValues()
    return t


@fixture
def t1() -> TModel:
    t = create_mock_test_model()
    t.name = "test1"
    t.target_func_name = "f1"
    t.result = 1
    return t


@fixture
def t2() -> TModel:
    t = create_mock_test_model()
    t.name = "test2"
    t.target_func_name = "f2"
    t.result = 2
    return t


@fixture
def all_tests() -> AllTests:
    a: AllTests = Mock(AllTests)
    a.module = "module_a"
    a.tests = []
    return a


def create_mock_mock_model() -> MockModel:
    m: MockModel = Mock(MockModel)
    m.calls = []
    m.attributes = {}
    return m


@fixture
def mock1():
    m = create_mock_mock_model()
    m.name = "mock1"
    m.spec_str = "foo.Service"
    return m


@fixture
def mock2():
    m = create_mock_mock_model()
    m.name = "mock2"
    m.spec_str = "foo.Bar"
    return m


def test_generate_import_statements_target_function(all_tests, t1):
    """
    Kept here for comparison with the generated test
    generated.testscribe.test_generate_imports_g.test_generate_import_statements
    only.

    The generated test has better coverage for the combine statemets aspect of the
    logic. It has similar amount of setup work. However, the tool provides
    step-by-step guidance on what to set.

    """
    all_tests.tests = [t1]
    r = generate_import_statement_str(all_tests)
    expected = """\
from module_a import f1
"""
    assert r == expected
