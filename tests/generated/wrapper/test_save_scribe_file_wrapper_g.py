import test_data.person
import test_data.simple
import test_data.value
import testscribe.model_type
from wrapper.save_scribe_file_wrapper import save_obj_to_yaml, save_object_model


def test_save_multi_line_string_to_yaml():
    result = save_obj_to_yaml(obj='first\nsecond line')
    assert result == """\
|-
  first
  second line
"""


def test_save_one_line_string_to_yaml():
    result = save_obj_to_yaml(obj='short')
    assert result == """\
short
...
"""


def test_save_obj_to_yaml_preserve_the_key_order():
    result = save_obj_to_yaml(obj={'b': 1, 'a': 2, 'c': 3})
    assert result == """\
b: 1
a: 2
c: 3
"""


def test_save_obj_to_yaml_set():
    result = save_obj_to_yaml(obj=testscribe.model_type.SetModel([1, 2]))
    assert result == """\
!testscribe/set
- 1
- 2
"""


def test_save_obj_to_yaml_module_model():
    result = save_obj_to_yaml(obj=testscribe.model_type.ModuleModel("m"))
    assert result == "!testscribe/module 'm'\n"


def test_save_obj_to_yaml_callable_model():
    result = save_obj_to_yaml(obj=test_data.value.callable_model_foo)
    assert result == """\
!testscribe/callable
name: foo
module: test_data.simple
"""


def test_save_obj_to_yaml_expression_model():
    result = save_obj_to_yaml(obj=testscribe.model_type.ExpressionModel("a"))
    assert result == "!testscribe/expression 'a'\n"


def test_save_obj_to_yaml_mock_name_model():
    result = save_obj_to_yaml(obj=testscribe.model_type.MockNameModel("a"))
    assert result == "!testscribe/mock 'a'\n"


def test_save_object_model_has_custom_repr():
    result = save_object_model(v=test_data.person.Person("a", 1))
    assert result == """\
!testscribe/object
type: test_data.person.Person
repr: Person(name='a', age=1)
"""


def test_save_object_model_no_custom_repr():
    result = save_object_model(v=test_data.simple.C(a=1))
    assert result == """\
!testscribe/object
type: test_data.simple.C
members:
  a: 1
"""
