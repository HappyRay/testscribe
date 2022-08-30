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
from pathlib import Path
from typing import List, Tuple, Optional, Any

from yaml import full_load

from testscribe import scribe_file_key as key
from testscribe.log import log
from testscribe.model_type import (
    MockCallModel,
    MockModel,
    PatchModel,
    ExceptionModel,
    TestModel,
    AllTests,
)
from testscribe.namedvalues import NamedValues
from testscribe.yaml_tag import add_constructor_for_custom_tags

logger = logging.getLogger(__name__)


def load_or_create_model(file_path: Path, full_module_name: str):
    if file_path.exists():
        logger.info(f"Load exsiting scribe file {file_path}.")
        return load_scribe_file(file_path)
    else:
        log(f"There is no existing test scribe file at {file_path}")
        return AllTests(module=full_module_name, tests=[])


def load_scribe_file(scribe_file: Path) -> AllTests:
    logger.debug(f"Loading the scribe file from: {scribe_file}")
    with scribe_file.open(mode="r") as f:
        content = load_from_yaml(stream=f)
        all_tests = load_model(content)
        return all_tests


def load_from_yaml(stream):
    add_constructor_for_custom_tags()
    return full_load(stream=stream)


def load_model(d: dict) -> AllTests:
    tests = [load_test(t) for t in d[key.TESTS]]
    return AllTests(
        module=d[key.MODULE],
        tests=tests,
    )


def load_test(d: dict) -> TestModel:
    description = load_test_description(d)
    target_func_name, target_class_name = load_target(d)
    init_parameters = load_named_values(d, key.INIT_PARAMETERS)
    parameters = load_named_values(d, key.PARAMETERS)
    mocks = load_mocks(d)
    patches = load_patches(d)
    exception_model = load_exception_model(d)
    result = load_result(d)
    return TestModel(
        name=load_required_name_key_value(d),
        short_name=load_short_name(d),
        description=description,
        target_func_name=target_func_name,
        target_class_name=target_class_name,
        init_parameters=init_parameters,
        parameters=parameters,
        result=result,
        exception=exception_model,
        mocks=mocks,
        patches=patches,
    )


def load_short_name(d: dict) -> str:
    return d[key.SHORT_NAME]


def load_result(d: dict) -> Any:
    return d.get(key.RESULT, None)


def load_target(d: dict) -> Tuple[str, str]:
    target = d[key.TARGET]
    return load_required_name_key_value(target), load_target_class_name(target)


def load_target_class_name(d: dict) -> str:
    return d.get(key.CLASS_NAME, "")


def load_test_description(d: dict) -> str:
    return d.get(key.DESCRIPTION, "")


def load_named_values(d: dict, key_name: str) -> NamedValues:
    """
    Load a NamedValues from YAML

    :param d:
    :param key_name:
    :return:
    """
    param_dict_list = d.get(key_name, [])
    name_value_list = [
        (load_optional_name_key_value(d), get_named_value_element_value(d))
        for d in param_dict_list
    ]
    return NamedValues(name_value_list)


def get_named_value_element_value(d: dict) -> str:
    return d[key.VALUE]


def load_mocks(d: dict) -> List[MockModel]:
    return [load_mock_model(m) for m in d.get(key.MOCKS, [])]


def load_mock_model(m: dict) -> MockModel:
    return MockModel(
        name=load_required_name_key_value(m),
        spec_str=m[key.SPEC],
        calls=load_mock_calls(m),
        attributes=load_mock_attributes(m),
    )


def load_mock_calls(m: dict) -> List[MockCallModel]:
    return [load_mock_call_model(c) for c in m.get(key.CALLS, [])]


def load_mock_attributes(m: dict) -> dict:
    return m.get(key.ATTRIBUTES, {})


def load_mock_call_model(c: dict) -> MockCallModel:
    return MockCallModel(
        name=load_optional_name_key_value(c),
        parameters=load_named_values(c, key.PARAMETERS),
        return_value=c.get(key.RETURN_VALUE, None),
    )


def load_patches(d: dict) -> List[PatchModel]:
    return [load_one_patch(p) for p in d.get(key.PATCHES, [])]


def load_one_patch(d: dict) -> PatchModel:
    return PatchModel(target=d[key.TARGET], replacement=d[key.PATCH_REPLACEMENT])


def load_exception_model(d: dict) -> Optional[ExceptionModel]:
    if key.EXCEPTION in d:
        return load_exception_internal(d[key.EXCEPTION])
    else:
        return None


def load_exception_internal(d: dict) -> ExceptionModel:
    return ExceptionModel(type=d[key.TYPE], message=d[key.MESSAGE])


def load_required_name_key_value(d: dict) -> str:
    return d[key.NAME]


def load_optional_name_key_value(d: dict) -> str:
    return d.get(key.NAME, "")
