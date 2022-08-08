import test_data.value
import test_scribe.ignore
import test_scribe.model_type
import test_scribe.special_type
import test_scribe.user_triggered_exception
import typing
from test_scribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from test_scribe.value_input_util import eval_special_value, get_possible_fully_qualified_names, get_string_value, import_module, import_modules_from_expression, is_simple_value, transform_default_value, transform_mock_names_to_mock_expression, transform_no_default_value, transform_real_default_value, try_import_module


def test_eval_special_value_ignore():
    result = eval_special_value(value_str='ignore')
    assert isinstance(result, test_scribe.ignore.IgnoreReturnValue)
    assert repr(result) == "'Ignored'"


def test_eval_special_value_default_exception():
    result = eval_special_value(value_str='throw()')
    assert isinstance(result, test_scribe.user_triggered_exception.UserTriggeredException)
    assert repr(result) == 'Exception()'


def test_eval_special_value_throw_custom_exception():
    result = eval_special_value(value_str="throw(Exception('foo'))")
    assert isinstance(result, test_scribe.user_triggered_exception.UserTriggeredException)
    assert repr(result) == "Exception('foo')"


def test_eval_special_value_non_special_value():
    result = eval_special_value(value_str='1')
    assert result is None


def test_eval_special_value_invalid_input():
    result = eval_special_value(value_str='a')
    assert result is None


def test_get_possible_fully_qualified_names_has_class_name():
    result = get_possible_fully_qualified_names(expression='a.b.C(a=d.E, b=1)')
    assert result == ['a.b.C', 'd.E']


def test_get_possible_fully_qualified_names_no_class_name():
    result = get_possible_fully_qualified_names(expression='1 + 2')
    assert result == []


def test_get_possible_fully_qualified_names_name_without_dot():
    result = get_possible_fully_qualified_names(expression='foo')
    assert result == []


def test_get_string_value_escape_leading_single_quote():
    result = get_string_value(value="\\'a")
    assert result == "'a"


def test_get_string_value_escape_leading_double_quote():
    result = get_string_value(value='\\"a')
    assert result == '"a'


def test_get_string_value_multi_line_single_quote():
    result = get_string_value(value="'a\\nb'")
    assert result == """\
a
b"""


def test_get_string_value_multi_line_double_quote():
    result = get_string_value(value='"a\\nb"')
    assert result == """\
a
b"""


def test_get_string_value():
    result = get_string_value(value='a')
    assert result == 'a'


def test_import_module():
    result = import_module(module_name='test_data.simple')
    from types import ModuleType
    assert type(result) == ModuleType
    result.__name__ == 'test_data'


def test_import_module_incorrect_module_name():
    result = import_module(module_name='foo')
    assert result is None


def test_import_modules_from_expression():
    result = import_modules_from_expression(user_input='test_data.simple.C')
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], dict)
    assert len(result[0]) == 1
    from types import ModuleType
    assert type(result[0]['test_data']) == ModuleType
    result[0]['test_data'].__name__ == 'test_data'
    assert result[1] == ['test_data.simple']


def test_import_modules_from_expression_float_input():
    """
    A float input should not be interpreted as a module although it may have a .
    """
    result = import_modules_from_expression(user_input='1.1')
    assert result == ({}, [])


def test_is_simple_value_none():
    result = is_simple_value(v=None)
    assert result is True


def test_is_simple_value_dict():
    result = is_simple_value(v={'a': 1})
    assert result is True


def test_is_simple_value_tuple_with_object():
    result = is_simple_value(v=(1, test_data.value.object_model_c))
    assert result is False


def test_is_simple_value_dict_with_object():
    result = is_simple_value(v={'a': test_data.value.object_model_c})
    assert result is False


def test_transform_default_value_has_default():
    result = transform_default_value(default=1, t=typing.Any)
    assert result == '1'


def test_transform_default_value_no_default():
    result = transform_default_value(default=test_scribe.special_type.NoDefault, t=str)
    assert result == ''


def test_transform_mock_names_to_mock_expression_mock_name_in_a_tuple():
    m_test_model: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    m_mock_model: test_scribe.model_type.MockModel = create_autospec(spec=test_scribe.model_type.MockModel)
    m_test_model.mocks = [m_mock_model]
    m_mock_model.name = 'm1_2'
    m_mock_model.spec_str = 'spec'
    result = transform_mock_names_to_mock_expression(v=(1, test_scribe.model_type.MockNameModel("m1_2")), test_to_infer_default_inputs=m_test_model)
    assert result == "(1, m(spec, 'm1'))"
    m_test_model.assert_not_called()
    m_mock_model.assert_not_called()


def test_transform_mock_names_to_mock_expression_simple_mock_name():
    m_test_model: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    m_mock_model: test_scribe.model_type.MockModel = create_autospec(spec=test_scribe.model_type.MockModel)
    m_test_model.mocks = [m_mock_model]
    m_mock_model.name = 'm1_2'
    m_mock_model.spec_str = 'spec'
    result = transform_mock_names_to_mock_expression(v=test_scribe.model_type.MockNameModel("m1_2"), test_to_infer_default_inputs=m_test_model)
    assert result == "m(spec, 'm1')"
    m_test_model.assert_not_called()
    m_mock_model.assert_not_called()


def test_transform_mock_names_to_mock_expression_no_test():
    result = transform_mock_names_to_mock_expression(v=1, test_to_infer_default_inputs=None)
    assert result == '1'


def test_transform_mock_names_to_mock_expression_no_test_to_infer_default():
    result = transform_mock_names_to_mock_expression(v=1, test_to_infer_default_inputs=None)
    assert result == '1'


def test_transform_no_default_value_non_bool():
    result = transform_no_default_value(t=int)
    assert result == ''


def test_transform_no_default_value_bool():
    result = transform_no_default_value(t=bool)
    assert result == 'False'


def test_transform_real_default_value_none():
    result = transform_real_default_value(default=None)
    assert result == 'None'


def test_transform_real_default_value_str():
    result = transform_real_default_value(default='a')
    assert result == 'a'


def test_transform_real_default_value_float():
    result = transform_real_default_value(default=1.1)
    assert result == '1.1'


def test_transform_real_default_value_bool():
    result = transform_real_default_value(default=True)
    assert result == 'True'


def test_transform_real_default_value_int():
    result = transform_real_default_value(default=1)
    assert result == '1'


def test_transform_real_default_value_expression():
    result = transform_real_default_value(default=test_scribe.model_type.ExpressionModel("e"))
    assert result == 'e'


def test_transform_real_default_value_set():
    result = transform_real_default_value(default=test_scribe.model_type.SetModel([1, 2]))
    assert result == 'set([1, 2])'


def test_transform_real_default_value_tuple():
    result = transform_real_default_value(default=(1, 2))
    assert result == '(1, 2)'


def test_try_import_module_invalid_module():
    result = try_import_module(name='a.b')
    assert result == (None, None)


def test_try_import_module():
    result = try_import_module(name='test_data.simple.C')
    assert isinstance(result, tuple)
    assert len(result) == 2
    from types import ModuleType
    assert type(result[0]) == ModuleType
    result[0].__name__ == 'test_data'
    assert result[1] == 'test_data.simple'


def test_try_import_module_object_has_more_than_one_part():
    result = try_import_module(name='inspect.Parameter.empty')
    assert isinstance(result, tuple)
    assert len(result) == 2
    from types import ModuleType
    assert type(result[0]) == ModuleType
    result[0].__name__ == 'inspect'
    assert result[1] == 'inspect'
