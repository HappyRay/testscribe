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

from yaml import add_representer, add_constructor, Dumper, Loader

from testscribe.model_type import (
    ObjectModel,
    MockNameModel,
    ExpressionModel,
    CallableModel,
    ModuleModel,
    SetModel,
)

# Use representer functions instead of a subclass of YAMLObject
# to represent objects to avoid translating the classes.

MOCK_NAME_YAML_TAG = "!testscribe/mock"


def mock_name_model_representer(dumper, mock_name_model: MockNameModel):
    # This method has the added benefit of generating a one line representation
    # When using a YAMLObject based approach, the result looks like
    # !testscribe/mock 'm_mock_call_model'
    return dumper.represent_scalar(MOCK_NAME_YAML_TAG, mock_name_model.name)


def mock_name_model_constructor(loader, node):
    name = loader.construct_scalar(node)
    return MockNameModel(name=name)


CALLABLE_YAML_TAG = "!testscribe/callable"
CALLABLE_YAML_KEY_NAME = "name"
CALLABLE_YAML_KEY_MODULE = "module"


def callable_model_representer(dumper, callable_model: CallableModel):
    value = {
        CALLABLE_YAML_KEY_NAME: callable_model.name,
        CALLABLE_YAML_KEY_MODULE: callable_model.module,
    }
    return dumper.represent_mapping(CALLABLE_YAML_TAG, value)


def callable_model_constructor(loader, node):
    value = loader.construct_mapping(node)
    return CallableModel(
        name=value[CALLABLE_YAML_KEY_NAME], module=value[CALLABLE_YAML_KEY_MODULE]
    )


EXPRESSION_YAML_TAG = "!testscribe/expression"


def expression_model_representer(dumper, expression_model: ExpressionModel):
    return dumper.represent_scalar(EXPRESSION_YAML_TAG, expression_model.expression)


def expression_model_constructor(loader, node):
    expression = loader.construct_scalar(node)
    return ExpressionModel(expression=expression)


OBJECT_YAML_TAG = "!testscribe/object"
OBJECT_YAML_KEY_TYPE = "type"
OBJECT_YAML_KEY_REPR = "repr"
OBJECT_YAML_KEY_MEMBERS = "members"


def object_model_representer(dumper, object_model: ObjectModel):
    """
    Use representer functions instead of a subclass of YAMLObject
    to represent ObjectModel object to skip fields that are empty.

    :param dumper:
    :param object_model:
    :return:
    """
    value = {OBJECT_YAML_KEY_TYPE: object_model.type}
    if object_model.repr:
        value[OBJECT_YAML_KEY_REPR] = object_model.repr
    else:
        value[OBJECT_YAML_KEY_MEMBERS] = object_model.members
    return dumper.represent_mapping(OBJECT_YAML_TAG, value)


def object_model_constructor(loader, node):
    value = loader.construct_mapping(node)
    t = value[OBJECT_YAML_KEY_TYPE]
    represantation = value.get(OBJECT_YAML_KEY_REPR, "")
    members = value.get(OBJECT_YAML_KEY_MEMBERS, {})
    return ObjectModel(type=t, repr=represantation, members=members)


MODULE_YAML_TAG = "!testscribe/module"


def module_model_representer(dumper, module_model: ModuleModel):
    return dumper.represent_scalar(MODULE_YAML_TAG, module_model.name)


def module_model_constructor(loader, node):
    name = loader.construct_scalar(node)
    return ModuleModel(name=name)


SET_YAML_TAG = "!testscribe/set"


def set_model_representer(dumper: Dumper, set_model: SetModel):
    return dumper.represent_sequence(SET_YAML_TAG, set_model.elements)


def set_model_constructor(loader: Loader, node):
    elements = loader.construct_sequence(node)
    return SetModel(elements=elements)


def add_representer_for_custom_tags():
    add_representer(ObjectModel, object_model_representer)
    add_representer(MockNameModel, mock_name_model_representer)
    add_representer(CallableModel, callable_model_representer)
    add_representer(ExpressionModel, expression_model_representer)
    add_representer(ModuleModel, module_model_representer)
    add_representer(SetModel, set_model_representer)


def add_constructor_for_custom_tags():
    add_constructor(OBJECT_YAML_TAG, object_model_constructor)
    add_constructor(MOCK_NAME_YAML_TAG, mock_name_model_constructor)
    add_constructor(EXPRESSION_YAML_TAG, expression_model_constructor)
    add_constructor(CALLABLE_YAML_TAG, callable_model_constructor)
    add_constructor(MODULE_YAML_TAG, module_model_constructor)
    add_constructor(SET_YAML_TAG, set_model_constructor)
