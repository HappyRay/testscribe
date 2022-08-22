import testscribe.model_type
from wrapper.load_scribe_file_wrapper import load_object_model


def test_load_object_model_set():
    result = load_object_model(yaml_str='!testscribe/set \n  - 1 \n  - 2')
    assert isinstance(result, testscribe.model_type.SetModel)
    assert repr(result) == 'set([1, 2])'


def test_load_object_model_module_model():
    result = load_object_model(yaml_str="!testscribe/module 'm'")
    assert isinstance(result, testscribe.model_type.ModuleModel)
    assert repr(result) == "ModuleModel(name='m')"


def test_load_object_model_expression_model():
    result = load_object_model(yaml_str="!testscribe/expression 'a'")
    assert isinstance(result, testscribe.model_type.ExpressionModel)
    assert repr(result) == 'a'


def test_load_object_model_callable_model():
    result = load_object_model(yaml_str='!testscribe/callable\n    name: foo\n    module: test_data.simple')
    assert isinstance(result, testscribe.model_type.CallableModel)
    assert repr(result) == 'test_data.simple.foo'


def test_load_object_model_mock_name_model():
    result = load_object_model(yaml_str="!testscribe/mock 'a'")
    assert isinstance(result, testscribe.model_type.MockNameModel)
    assert repr(result) == 'a'


def test_load_object_model_without_custom_repr():
    result = load_object_model(yaml_str='!testscribe/object\n     type: test_data.simple.C\n     members:\n       a: 1')
    assert isinstance(result, testscribe.model_type.ObjectModel)
    assert repr(result) == "Object(type (test_data.simple.C), members ({'a': 1}))"


def test_load_object_model_with_custom_repr():
    result = load_object_model(yaml_str="!testscribe/object\n    type: test_data.person.Person\n    repr: Person(name='a', age=1)")
    assert isinstance(result, testscribe.model_type.ObjectModel)
    assert repr(result) == "test_data.person.Person(name='a', age=1)"
