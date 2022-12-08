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
from pathlib import Path
from string import Template
from typing import Optional

from testscribe.code_gen_util import add_indentation
from testscribe.execution_util import remove_file_if_no_test
from testscribe.gen_mock_code import generate_mocks_str
from testscribe.gen_mock_verification_code import (
    generate_mock_call_verification_str,
)
from testscribe.gen_patch_code import generate_patch_str
from testscribe.generate_imports import generate_import_statement_str
from testscribe.log import log
from testscribe.model_type import (
    ExceptionModel,
    TestModel,
    AllTests,
)
from testscribe.namedvalues import NamedValues
from testscribe.result_assertion import generate_result_assertion

logger = logging.getLogger(__name__)


def generate_unit_test_file(test_file_path: Path, all_tests: AllTests):
    if remove_file_if_no_test(file_path=test_file_path, tests=all_tests.tests):
        return
    generated_test_str = generate_tests_output_string(all_tests=all_tests)
    # log(f"Generated test:\n{generated_test_str}")
    with test_file_path.open(mode="w") as f:
        f.write(generated_test_str)
    log(f"Wrote the generated test file to: {test_file_path}")


def generate_tests_output_string(all_tests: AllTests) -> str:
    import_statement_str = generate_import_statement_str(all_tests=all_tests)
    test_functions = [generate_one_test_function(t) for t in all_tests.tests]
    output_str = "\n\n".join([import_statement_str] + test_functions)
    return output_str


def generate_one_test_function(test: TestModel) -> str:
    template_str = """\
def $test_name():$docstring$mock_str$invocation$result_assertion$mock_call_verification
"""
    template = Template(template_str)
    docstring = generate_docstring(test.description)
    mocks = test.mocks
    mock_str = generate_mocks_str(mocks)
    mock_call_verification_str = generate_mock_call_verification_str(mocks)
    invocation = gen_invocation_str_with_patch(test)
    result_assertion = generate_result_assertion_str(test)
    output_str = template.substitute(
        test_name=test.name,
        docstring=docstring,
        func_name=test.target_func_name,
        mock_str=mock_str,
        invocation=invocation,
        result_assertion=result_assertion,
        mock_call_verification=mock_call_verification_str,
    )
    return output_str


def generate_docstring(description: str) -> str:
    if not description:
        return ""
    docstring_raw = f'"""\n{description}\n"""'
    docstring = add_indentation(docstring_raw, 1)
    return "\n" + docstring


def gen_invocation_str_with_patch(test: TestModel) -> str:
    patch_str = generate_patch_str(test.patches)
    create_and_invocation_str = gen_invocation_str_with_exception(test)
    indent_level = get_invocation_indent_level(patch_str)
    indented_invocation_str = add_indentation(create_and_invocation_str, indent_level)
    return f"{patch_str}\n{indented_invocation_str}"


def gen_invocation_str_with_exception(test: TestModel) -> str:
    inner_statement = gen_create_invocation_str(test)
    return wrap_exception_assertion(
        exception_model=test.exception, inner_statement=inner_statement
    )


def gen_create_invocation_str(test: TestModel) -> str:
    create_instance_statement = generate_create_instance_statement(
        target_class_name=test.target_class_name,
        init_parameters=test.init_parameters,
    )
    invocation_statement = generate_invocation_statement(test)
    return create_instance_statement + invocation_statement


def generate_create_instance_statement(
    target_class_name: str, init_parameters: NamedValues
) -> str:
    if target_class_name == "":
        return ""
    param_str = init_parameters.as_arg_str()
    return f"instance = {target_class_name}({param_str})\n"


def generate_invocation_statement(test: TestModel) -> str:
    parameters = test.parameters
    if parameters is None:
        # there is an exception in the constructor.
        return ""
    param_str = parameters.as_arg_str()
    instance_str = generate_target_instance_str(test.target_class_name)
    result_str = generate_result_assignment_str(does_test_have_exception(test))
    return f"{result_str}{instance_str}{test.target_func_name}({param_str})"


def does_test_have_exception(test: TestModel) -> bool:
    return test.exception is not None


def generate_result_assignment_str(has_exception: bool) -> str:
    result_str = "" if has_exception else "result = "
    return result_str


def generate_target_instance_str(target_class_name: str) -> str:
    instance_str = "instance." if target_class_name else ""
    return instance_str


def wrap_exception_assertion(
    exception_model: Optional[ExceptionModel], inner_statement: str
) -> str:
    if exception_model is None:
        return inner_statement
    template_str = """\
with pytest.raises($type) as exception_info:
$inner_statement
assert str(exception_info.value) == $message"""
    template = Template(template_str)
    output_str = template.substitute(
        type=exception_model.type,
        inner_statement=add_indentation(inner_statement, 1),
        message=repr(exception_model.message),
    )
    return output_str


def get_invocation_indent_level(patch_str: str) -> int:
    indent_level = 2 if patch_str else 1
    return indent_level


def generate_result_assertion_str(test: TestModel) -> str:
    result_assertion = "" if test.exception else generate_result_assertion(test.result)
    return result_assertion
